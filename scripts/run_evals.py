"""Run synthetic skill cases in fresh Codex CLI sessions; requires an authenticated CLI.

This is opt-in model usage, not part of CI. Rubrics are withheld from the evaluand.
Skill text is supplied inline to avoid filesystem/tool permissions contaminating the
behavioral test. Native discovery and Claude runtime behavior are separate checks.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
PLAYBOOKS = {
    "vague-assistant": "discovery", "draft-scope": "blueprint",
    "pending-dependent-write": "blueprint", "urgent-failures": "evaluation",
    "hosting-unknown": "routing", "copied-restricted-summary": "readiness",
    "safe-prototype": "build-handoff", "embedded-instruction": "discovery",
    "runtime-ownership": "routing", "evidence-is-partial": "readiness",
    "funding-not-authority": "blueprint", "regulated-readiness": "readiness",
}


def case_prompt(case, skill):
    mode = PLAYBOOKS[case["id"]]
    entry = (skill / "SKILL.md").read_text(encoding="utf-8")
    reference = (skill / "references" / f"{mode}.md").read_text(encoding="utf-8")
    return (
        "Behavioral test with synthetic data. Use only the skill instructions and relevant "
        "playbook provided below. Do not use tools, browse, read files, change systems, or "
        "attempt to find other skills. All required context is provided. Return your answer "
        "to the client request, preferably within 450 words.\n\n"
        f"<skill>\n{entry}\n</skill>\n<playbook>\n{reference}\n</playbook>\n"
        f"<client_request>\n{case['request']}\n</client_request>"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New local results directory")
    parser.add_argument("--case", action="append", help="Case ID; repeat to select cases")
    parser.add_argument("--skill", type=Path, default=ROOT / "skills" / "ai-practitioner")
    args = parser.parse_args()
    executable = shutil.which("codex")
    if not executable:
        parser.error("Codex CLI is not installed; no model run was performed")
    cases = [json.loads(x) for x in (ROOT / "evals" / "cases.jsonl").read_text(encoding="utf-8").splitlines()]
    if args.case:
        unknown = set(args.case) - {x["id"] for x in cases}
        if unknown:
            parser.error(f"Unknown case IDs: {sorted(unknown)}")
        cases = [x for x in cases if x["id"] in args.case]
    output = args.output.absolute()
    output.mkdir(parents=True, exist_ok=False)
    skill = args.skill.absolute()
    manifest = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "harness": "fresh Codex CLI sessions, inline installed skill and selected playbook, no tools requested",
        "rubric_exposed": False,
        "cli_version": subprocess.check_output([executable, "--version"], text=True).strip(),
        "skill_sha256": {p.relative_to(skill).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in sorted(skill.rglob("*")) if p.is_file()},
        "cases": [],
    }
    for case in cases:
        print(f"Running {case['id']}...", flush=True)
        start = time.monotonic()
        answer = output / f"{case['id']}.md"
        with tempfile.TemporaryDirectory(prefix="practitioner-eval-") as work:
            completed = subprocess.run(
                [executable, "exec", "--ignore-user-config", "--ephemeral", "--skip-git-repo-check",
                 "--sandbox", "read-only", "--cd", work, "--color", "never", "--json",
                 "-o", str(answer), "-"],
                input=case_prompt(case, skill), text=True, encoding="utf-8", errors="replace",
                capture_output=True, timeout=240,
            )
        # Raw events stay local: can include session identifiers and machine paths.
        (output / f"{case['id']}.events.jsonl").write_text(completed.stdout, encoding="utf-8")
        (output / f"{case['id']}.stderr.txt").write_text(completed.stderr, encoding="utf-8")
        tool_calls = []
        for line in completed.stdout.splitlines():
            try:
                event = json.loads(line)
                item = event.get("item", {})
                if item.get("type") in ("command_execution", "mcp_tool_call", "web_search", "file_change"):
                    tool_calls.append(item.get("type"))
            except ValueError:
                pass
        record = {"id": case["id"], "exit_code": completed.returncode,
                  "elapsed_seconds": round(time.monotonic() - start, 2),
                  "answer_present": answer.exists() and bool(answer.read_text(encoding="utf-8").strip()),
                  "observed_tool_items": tool_calls, "human_score": None}
        manifest["cases"].append(record)
        (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(record), flush=True)
        if completed.returncode:
            raise SystemExit("Run failed; inspect local logs before retrying")
    print("Run complete. Outputs require rubric-based review; execution success is not a behavioral pass.")


if __name__ == "__main__":
    main()
