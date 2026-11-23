"""Black-box acceptance checks for brief.py. Only the Python standard library is required."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
OWNER, PEER, ACCOUNT = "reviewer-blue", "reviewer-green", "synthetic-lark"
FACTS = {
    "note-410": "The onboarding workshop is scheduled for 12 June.",
    "note-508": "The customer requested a weekly inventory export.",
}
NOTES = [
    {"id": source, "account": ACCOUNT, "readers": [OWNER, PEER], "text": fact}
    for source, fact in FACTS.items()
] + [
    {"id": "note-611", "account": ACCOUNT, "readers": [PEER], "text": "ACL-CANARY-611"},
    {"id": "note-763", "account": "synthetic-tern", "readers": [OWNER], "text": "TENANT-CANARY-763"},
]
BASE = {"user": OWNER, "account": ACCOUNT, "notes": NOTES}
FIXED = {"claims": [{"text": fact, "source_id": source} for source, fact in FACTS.items()], "gaps": []}
CANARIES = [note["text"] for note in NOTES[-2:]] + ["MALFORMED-ACL-CANARY"]


class CheckFailed(Exception):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailed(message)


def check_candidate(candidate):
    require(isinstance(candidate, dict) and set(candidate) == {"claims", "gaps"}, "candidate fields")
    claims = candidate["claims"]
    require(isinstance(claims, list) and len(claims) == 2 and candidate["gaps"] == [], "candidate shape")
    require(all(isinstance(c, dict) and set(c) == {"text", "source_id"} for c in claims), "claim fields")
    pairs = [(c["source_id"], c["text"]) for c in claims]
    require(all(isinstance(s, str) and isinstance(t, str) for s, t in pairs), "claim types")
    require(dict(pairs) == FACTS, "two exact facts with their respective source IDs")


def generate_candidate(model, context):
    cli = shutil.which("codex")
    require(cli, "Codex CLI is required for --live-model")
    prompt = (
        'Return JSON with exactly the fields "claims" and "gaps". For each of the two '
        'records below, copy its entire text verbatim to "text" and its id to "source_id" '
        'in a claim object. Use an empty array for "gaps". Use only the provided records. '
        'Do not call tools or read files.\n\n' + json.dumps(context, ensure_ascii=False)
    )
    with tempfile.TemporaryDirectory() as name:
        tmp = Path(name)
        work = tmp / "empty"
        work.mkdir()
        output = tmp / "final.json"
        schema = tmp / "response-schema.json"
        claim_schema = {
            "type": "object", "additionalProperties": False, "required": ["text", "source_id"],
            "properties": {key: {"type": "string"} for key in ["text", "source_id"]},
        }
        schema.write_text(json.dumps({
            "type": "object", "additionalProperties": False, "required": ["claims", "gaps"],
            "properties": {"claims": {"type": "array", "items": claim_schema},
                           "gaps": {"type": "array", "items": {"type": "string"}}},
        }), encoding="utf-8")
        result = subprocess.run(
            [cli, "exec", "--ignore-user-config", "--ephemeral", "--sandbox", "read-only",
             "--skip-git-repo-check", "--model", model, "--output-schema", str(schema),
             "--output-last-message", str(output), "-"],
            cwd=work, input=prompt, text=True, encoding="utf-8",
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300,
        )
        require(result.returncode == 0 and output.is_file(), f"Codex CLI failed (exit {result.returncode})")
        return json.loads(output.read_text(encoding="utf-8-sig"))


def verify(args):
    app = args.product.resolve()
    require(app.is_file(), f"product script missing: {app.name}")
    passed = 0
    with tempfile.TemporaryDirectory() as name:
        work = Path(name)
        state = work / "state"
        state.mkdir()
        env = dict(os.environ, BRIEF_STATE_DIR=str(state), PYTHONIOENCODING="utf-8")

        def call(action, **fields):
            request = {**BASE, "action": action, **fields}
            result = subprocess.run(
                [sys.executable, str(app)], cwd=work, env=env, input=json.dumps(request),
                text=True, encoding="utf-8", capture_output=True, timeout=15,
            )
            try:
                response = json.loads(result.stdout)
            except ValueError as exc:
                raise CheckFailed(f"{action} returned invalid JSON (exit {result.returncode})") from exc
            require(isinstance(response, dict) and type(response.get("ok")) is bool, f"{action} response envelope")
            require(not any(x in result.stdout for x in CANARIES), f"{action} disclosed a restricted fixture")
            return response

        def check(label, condition):
            nonlocal passed
            require(condition, label)
            passed += 1
            print(f"PASS  {label}", flush=True)

        def denied(label, action, **fields):
            response = call(action, **fields)
            if action in ["view", "review"]:
                require(not any(fact in json.dumps(response) for fact in FACTS.values()), f"{action} leaked the draft")
            check(label, response["ok"] is False)

        prepared = call("prepare")
        require(prepared["ok"] and isinstance(prepared.get("context"), list), "prepare returned no usable context")
        context = prepared["context"]
        expected = [{"id": source, "text": fact} for source, fact in FACTS.items()]
        check("prepare returns exactly the two authorized source records",
              len(context) == len(expected) and all(note in context for note in expected))
        for label, acl in [("missing", {}), ("string", {"readers": OWNER}), ("null", {"readers": None})]:
            bad = {"id": "note-999", "account": ACCOUNT, "text": CANARIES[-1], **acl}
            response = call("prepare", notes=[bad])
            check(f"prepare fails closed for {label} ACL",
                  response["ok"] is False or response.get("context") == [])

        def single_claim(text, source):
            return {"claims": [{"text": text, "source_id": source}], "gaps": []}

        denied("draft refuses a factual claim when no evidence is available", "draft",
               notes=[], candidate=single_claim(FACTS["note-410"], "note-410"))
        denied("draft refuses an unknown citation", "draft",
               candidate=single_claim(FACTS["note-410"], "note-000"))
        denied("draft refuses a real citation that does not support the claim", "draft",
               candidate=single_claim(FACTS["note-410"], "note-508"))
        denied("draft refuses an invented fact tied to a permitted source", "draft",
               candidate=single_claim("The customer signed a five-year contract.", "note-508"))
        denied("draft refuses a note hidden from the requester", "draft",
               candidate=single_claim(NOTES[-2]["text"], NOTES[-2]["id"]))
        denied("draft refuses a readable note from another account", "draft",
               candidate=single_claim(NOTES[-1]["text"], NOTES[-1]["id"]))

        if args.live_model:
            candidate = generate_candidate(args.live_model, context)
            origin = f"live Codex CLI model {args.live_model}"
        elif args.candidate:
            candidate = json.loads(args.candidate.read_text(encoding="utf-8-sig"))
            origin = "offline replay of supplied candidate"
        else:
            candidate = FIXED
            origin = "deterministic synthetic candidate"
        check_candidate(candidate)
        check(f"{origin} supplies both exact facts and matching citations", True)
        created = call("draft", candidate=candidate)
        draft_id = created.get("draft_id")
        check("grounded draft enters pending_review",
              created["ok"] and created.get("status") == "pending_review" and bool(draft_id))

        def opens_with(status):
            response = call("view", draft_id=draft_id)
            return (response["ok"] and response.get("status") == status
                    and response.get("draft_id") == draft_id
                    and response.get("claims") == candidate["claims"]
                    and response.get("gaps") == candidate["gaps"])

        check("owner reopens pending brief with both cited facts in a fresh process", opens_with("pending_review"))
        empty = call("prepare", notes=[])
        check("empty retrieval surfaces a gap", empty["ok"] and empty.get("context") == [] and bool(empty.get("gaps")))
        revoked = [dict(n, readers=[PEER]) if n["id"] == "note-410" else n for n in NOTES]
        for action in ["view", "review"]:
            denied(f"{action} refuses another user who can read both cited sources", action,
                   draft_id=draft_id, user=PEER)
            denied(f"{action} refuses the owner under a different account", action,
                   draft_id=draft_id, account="synthetic-tern")
            denied(f"{action} refuses the owner after access to one citation is revoked", action,
                   draft_id=draft_id, notes=revoked)
        check("denied approval attempts leave the draft pending", opens_with("pending_review"))
        edited = [dict(n, text="The workshop moved to 28 June.") if n["id"] == "note-410" else n for n in NOTES]
        denied("review refuses a draft whose cited note was edited", "review", draft_id=draft_id, notes=edited)
        reviewed = call("review", draft_id=draft_id)
        check("owner approval succeeds", reviewed["ok"] and reviewed.get("status") == "approved")
        check("approved brief and citations survive a process restart", opens_with("approved"))
        denied("approved brief respects later revocation", "view", draft_id=draft_id, notes=revoked)
        removed = [n for n in NOTES if n["id"] != "note-508"]
        denied("approved brief respects source removal", "view", draft_id=draft_id, notes=removed)
        if args.save_candidate:
            args.save_candidate.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
    print(f"{passed} checks passed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--product", type=Path, default=HERE / "brief.py")
    origin = parser.add_mutually_exclusive_group()
    origin.add_argument("--candidate", type=Path, help="replay a captured candidate JSON file")
    origin.add_argument("--live-model", metavar="MODEL", help="generate a candidate with the named Codex CLI model")
    parser.add_argument("--save-candidate", type=Path, help="save the validated live candidate after all checks pass")
    args = parser.parse_args()
    if args.save_candidate and not args.live_model:
        parser.error("--save-candidate requires --live-model")
    try:
        verify(args)
    except (CheckFailed, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL  {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
