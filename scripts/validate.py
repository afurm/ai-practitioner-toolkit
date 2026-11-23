"""Validate portable packaging and local references; no model calls or network."""

import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "ai-practitioner"
EXCLUDED = {".git", ".venv", "__pycache__", "client-work", "private", "eval-results", "dist"}


def markdown_files(root):
    for directory, folders, files in os.walk(root, followlinks=False):
        folders[:] = [name for name in folders if name not in EXCLUDED]
        for name in files:
            if name.endswith(".md"):
                yield Path(directory) / name


def validate(root=ROOT):
    root = Path(root)
    skill = root / "skills" / "ai-practitioner"
    errors = []
    entry = skill / "SKILL.md"
    text = entry.read_text(encoding="utf-8")
    front = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not front:
        errors.append("Missing LF-delimited skill frontmatter")
    else:
        fields = dict(re.findall(r"^(name|description|license): (.+)$", front.group(1), re.M))
        name = fields.get("name", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append("Invalid skill name")
        if name != skill.name:
            errors.append("Skill name must match folder")
        if not 1 <= len(fields.get("description", "")) <= 1024:
            errors.append("Missing or oversized description")
        if set(re.findall(r"^(\S+):", front.group(1), re.M)) - {"name", "description", "license"}:
            errors.append("Unexpected frontmatter: review portability")
    for path in markdown_files(root):
        if path.is_symlink():
            errors.append(f"Linked Markdown is not supported: {path.relative_to(root)}")
            continue
        content = path.read_text(encoding="utf-8")
        # Links with explicit relative targets; external URLs and in-page anchors are excluded.
        for raw in re.findall(r"\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)", content):
            target = unquote(raw.split("#", 1)[0])
            if not target or urlparse(target).scheme:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                errors.append(f"Broken/escaping link in {path.relative_to(root)}: {raw}")
            if path.is_relative_to(skill) and not resolved.is_relative_to(skill.resolve()):
                errors.append(f"Skill is not self-contained: {path.relative_to(root)} -> {raw}")
        if "__cld_token__" in content or "codex-clipboard-" in content:
            errors.append(f"Private course/clipboard artifact in {path.relative_to(root)}")
    cases = root / "evals" / "cases.jsonl"
    ids = set()
    for number, line in enumerate(cases.read_text(encoding="utf-8").splitlines(), 1):
        try:
            case = json.loads(line)
            if not isinstance(case.get("id"), str) or case["id"] in ids:
                raise ValueError("missing or duplicate case ID")
            ids.add(case["id"])
            if not isinstance(case.get("request"), str) or not case["request"].strip():
                raise ValueError("missing request")
            for key in ("must_demonstrate", "must_avoid"):
                if not isinstance(case.get(key), list) or not case[key] or not all(isinstance(x, str) and x for x in case[key]):
                    raise ValueError(f"missing rubric: {key}")
        except (ValueError, TypeError) as exc:
            errors.append(f"Invalid eval case line {number}: {exc}")
    if not ids:
        errors.append("No behavioral cases")
    return errors


def main():
    errors = validate()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Portable skill, internal links, artifact exclusions, and behavioral case format validated.")
    print("This is structural validation, not a live model behavioral evaluation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
