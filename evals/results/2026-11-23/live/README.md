# Live practitioner evaluation and build trial

On November 23, 2026, Codex produced **32 responses** to synthetic practitioner requests across three rounds. All **15 final responses** met their written criteria. A separate coding session used the installed build-handoff playbook to implement a small account-brief application. The application passed **26 acceptance checks** with actual model-generated content.

Use these results to judge whether the skill can help a practitioner discover requirements, design a workflow, and implement a supervised first slice. Client-specific accuracy, permissions, and operating targets require evidence from the deployment.

## What changed after reading the answers

| Round | Cases meeting all criteria | What the reviewers saw |
|---|---:|---|
| Baseline | 12 of 14 | All existing cases passed. The Cedar Quay brief correctly classified four claims and produced a safe Sales draft. Its handoff omitted an explicit destination-access check. The shift handoff correctly held publication but gave the supervisor no remedy for an unauthorized viewer. |
| First revision | 2 of 3 | The shift case now included a safe destination and urgent routing still passed. Cedar Quay's owner was told to check the audience and its access to the source. The response omitted explicitly asking the owner to verify the final wording against that source. |
| Final revision | 15 of 15 | Every case ran again with the final installed package. Both handoffs covered the exact copy and its actual viewers. A new case with current approvals correctly permitted publication and preserved the authorized sentence verbatim. |

The baseline CRM answer received a 2 from one AI reviewer and a 1 from another. Both agreed that the outward draft was accurate and contained no restricted detail. The stricter judgment was used because the task asked what the releasing owner should verify. The final guidance asks that person to compare the exact outgoing claims with the authoritative source and confirm who can view the destination.

The 15 final cases consist of 12 established regressions across all six playbooks, two cases used to improve the guidance, and one final-only transfer case. Each ran in a fresh Windows Codex CLI session (version `0.171.0-alpha.13`) requesting `gpt-6.2-sol`. Each session received the skill entry point, the relevant playbook, and the request. The grading criteria were withheld. The recorded events showed zero tool-execution items in these 32 sessions. Separate AI readers scored the generated texts. One sampled answer per case gives limited evidence about consistency across runs, models, or languages.

Read the actual responses in the [baseline](responses-baseline.md), [first revision](responses-retest.md), and [final revision](responses-final.md). The [run records](runs.json) and [case rubrics](../../../cases.jsonl) identify the test conditions and expectations.

## Native Claude Code check

In a fresh Windows Claude desktop Code session, the tester invoked `/ai-practitioner` for the shift-board case and explicitly requested the project-local skill and evaluation playbook. The UI showed both file reads. The playbook hash matched the final Codex run. The selected model was Sonnet 5.5 Medium.

The response met the case rubric. The designated crew copy gave Bay D at 19:30 with H2 as its source. The supervisor was told to hold posting, verify the wording and actual group and contractor access, and narrow access or use an authorized channel if needed. An adjacent reviewer explanation repeated the synthetic Payroll marker. For a product that offers a Copy or Share button, scope it to the approved passage. Copying the entire assistant response would also copy the private review.

This single explicit native invocation was scored separately from the 15-case Codex run. Automatic selection and native macOS and Linux sessions remain unmeasured.

## What the product actually did

A coding agent was given a trusted synthetic CRM adapter contract and the installed build-handoff playbook. It implemented a Python CLI with SQLite draft storage. A separate agent wrote black-box acceptance tests against the contract without reading the implementation. This measures delivery from an explicit, scoped handoff. The test supplied the interface and required behaviors.

The fixture contains four notes. The application sends the generator two authorized notes for the requested account. One other note belongs to a different account, and one is restricted to another reader. A real Codex model returned two exact facts with matching source IDs. The verifier submitted the candidate to the application, reopened the pending draft in a fresh process, simulated the owner's review, and reopened the approved draft.

The 26 checks include missing or malformed access data, empty retrieval, invalid references, an invented fact with a valid source ID, cross-account and cross-user reads, changed source text before approval, and revoked or removed evidence after approval. The review action is a simulated owner action. The fixture supplies identity and permissions directly. The quality check compares extractive facts with source text; broader summarization quality needs a separate evaluation. [Application](build/brief.py) · [Acceptance tests](build/verify.py) · [Captured generator response](build/captured-candidate.json)

### Replay from the repository root

With Python 3.10 or later, run the captured response through the complete workflow. Each application request starts in a separate process and uses a temporary state directory.

```sh
cd evals/results/2026-11-23/live/build
python verify.py --candidate captured-candidate.json
```

For another live generation, run the following from the same directory with an authenticated Codex CLI and a model available to your account. It uses the filtered synthetic context and consumes normal model usage.

```sh
python verify.py --live-model gpt-6.2-sol
```

## Readiness for a client product

This trial supports proceeding to a supervised prototype. A real pilot still needs verified identity and CRM authorization, suitable handling of copied drafts, and representative account managers checking factual accuracy, required omissions, and review effort. A production decision also needs measured traffic, latency and cost, an operating owner, and tested monitoring and recovery. No live CRM or customer records were used.
