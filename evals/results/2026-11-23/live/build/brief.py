"""Read one account-brief request from stdin and emit one JSON response."""

import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import uuid
from contextlib import closing


class Rejected(ValueError):
    """Carries only a fixed public error code."""


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Rejected("invalid_request")
        result[key] = value
    return result


def reject_constant(_):
    raise Rejected("invalid_request")


def authorized_notes(notes, user, account):
    if not isinstance(notes, list):
        raise Rejected("invalid_notes")
    visible = {}
    seen = set()
    for note in notes:
        if not isinstance(note, dict) or not all(
            nonblank(note.get(key)) for key in ("id", "account", "text")
        ):
            raise Rejected("invalid_notes")
        readers = note.get("readers")
        if not isinstance(readers, list) or not all(nonblank(r) for r in readers):
            raise Rejected("invalid_notes")
        source_id = note["id"]
        if source_id in seen:
            raise Rejected("invalid_notes")
        seen.add(source_id)
        if note["account"] == account and user in readers:
            visible[source_id] = note["text"]
    return visible


def fingerprint(note):
    return hashlib.sha256(note.encode("utf-8")).hexdigest()


def gap_prompts(raw_gaps):
    # The generator can place arbitrary assertions in a gap. Emit only fixed
    # review prompts. A topic match suggests a question, never a fact.
    topics = {
        "budget": "Confirm the budget.",
        "timeline": "Confirm the timeline.",
        "decision maker": "Confirm the decision maker.",
        "next step": "Confirm the next step.",
        "renewal": "Confirm renewal details.",
        "owner": "Confirm the account owner.",
    }
    prompts = []
    for gap in raw_gaps:
        words = gap.casefold().replace("-", " ")
        matches = [prompt for topic, prompt in topics.items() if topic in words]
        prompts.extend(matches or ["Review the available evidence for missing details."])
    return list(dict.fromkeys(prompts))


def validated_candidate(candidate, visible):
    if not isinstance(candidate, dict):
        raise Rejected("invalid_candidate")
    claims, gaps = candidate.get("claims"), candidate.get("gaps")
    if not isinstance(claims, list) or not isinstance(gaps, list):
        raise Rejected("invalid_candidate")
    if not all(nonblank(gap) for gap in gaps):
        raise Rejected("invalid_candidate")
    accepted = []
    snapshots = {}
    for claim in claims:
        if not isinstance(claim, dict) or not nonblank(claim.get("text")):
            raise Rejected("invalid_candidate")
        source_id = claim.get("source_id")
        if not nonblank(source_id) or source_id not in visible:
            raise Rejected("insufficient_evidence")
        note = visible[source_id]
        quote = claim["text"].strip()
        # Accept whole notes or whole sentences, never an arbitrary substring
        # that could drop a leading negation or a trailing qualification.
        sentences = re.split(r"(?<=[.!?])\s+", note.strip())
        if quote != note.strip() and quote not in sentences:
            raise Rejected("insufficient_evidence")
        accepted.append({"text": quote, "source_id": source_id})
        snapshots[source_id] = fingerprint(note)
    if not accepted:
        raise Rejected("insufficient_evidence")
    return {"claims": accepted, "gaps": gap_prompts(gaps), "sources": snapshots}


def connect_state():
    directory = os.environ.get("BRIEF_STATE_DIR")
    if not directory:
        raise Rejected("state_unavailable")
    path = Path(directory)
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    return sqlite3.connect(path / "briefs.sqlite3")


def response(draft_id, status, body):
    return {
        "ok": True, "draft_id": draft_id, "status": status,
        "claims": body["claims"], "gaps": body["gaps"],
    }


def handle(request):
    if not isinstance(request, dict):
        raise Rejected("invalid_request")
    user, account, action = (request.get(k) for k in ("user", "account", "action"))
    if not nonblank(user) or not nonblank(account):
        raise Rejected("invalid_request")
    if action not in ("prepare", "draft", "view", "review"):
        raise Rejected("invalid_request")
    visible = authorized_notes(request.get("notes"), user, account)
    if action == "prepare":
        return {
            "ok": True,
            "context": [{"id": key, "text": value} for key, value in visible.items()],
            "gaps": [] if visible else ["No readable evidence is available."],
        }
    if action == "draft":
        body = validated_candidate(request.get("candidate"), visible)
        draft_id = uuid.uuid4().hex
    else:
        draft_id = request.get("draft_id")
        if not nonblank(draft_id):
            raise Rejected("unavailable")

    with closing(connect_state()) as db, db:
        db.execute(
            """CREATE TABLE IF NOT EXISTS drafts (
                id TEXT PRIMARY KEY, owner TEXT NOT NULL, account TEXT NOT NULL,
                body TEXT NOT NULL, status TEXT NOT NULL
            )"""
        )
        if action == "draft":
            db.execute(
                "INSERT INTO drafts VALUES (?, ?, ?, ?, ?)",
                (draft_id, user, account, json.dumps(body), "pending_review"),
            )
            return response(draft_id, "pending_review", body)
        row = db.execute(
            "SELECT body, status FROM drafts WHERE id = ? AND owner = ? AND account = ?",
            (draft_id, user, account),
        ).fetchone()
        if row is None:
            raise Rejected("unavailable")
        body, status = json.loads(row[0]), row[1]
        for source_id, digest in body["sources"].items():
            if source_id not in visible or fingerprint(visible[source_id]) != digest:
                raise Rejected("unavailable")
        if action == "review" and status == "pending_review":
            db.execute("UPDATE drafts SET status = 'approved' WHERE id = ?", (draft_id,))
            status = "approved"
        return response(draft_id, status, body)


def main():
    try:
        request = json.loads(
            sys.stdin.buffer.read().decode("utf-8-sig"),
            object_pairs_hook=unique_object, parse_constant=reject_constant,
        )
        result = handle(request)
    except Rejected as exc:
        result = {"ok": False, "error": str(exc)}
        if str(exc) == "insufficient_evidence":
            result["gaps"] = ["A claim lacks sufficient readable evidence."]
    except (ValueError, RecursionError):
        result = {"ok": False, "error": "invalid_request"}
    except (sqlite3.Error, OSError):
        result = {"ok": False, "error": "state_unavailable"}
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    main()
