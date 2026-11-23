<div align="center">

# AI Practitioner Toolkit

**Turn client conversations into evidence-backed AI product decisions.**

Discovery → Routing → Blueprint → Evaluation → Readiness → Build

[![Validate](https://github.com/afurm/ai-practitioner-toolkit/actions/workflows/validate.yml/badge.svg)](https://github.com/afurm/ai-practitioner-toolkit/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-2563eb.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-compatible-0d9488.svg)](https://agentskills.io/specification)

[Get started](#get-started) · [See an example](examples/account-brief.md) · [Read the skill](skills/ai-practitioner/SKILL.md) · [Contribute](CONTRIBUTING.md)

</div>

Your client says, “We need an AI assistant.” This toolkit helps you find out what that actually means—and turn the answer into a useful first version.

It gives **Codex and Claude Code** one portable skill with six focused playbooks. Bring client notes, choose a stage, and get targeted questions, a conditional recommendation, or concrete engineering work. No API key, model subscription integration, MCP server, or background agent is required by the toolkit itself. Your chosen assistant has its own access and usage requirements.

## What you get

| Stage | Give it | Get back |
|---|---|---|
| **Discover** | A vague request, call notes, or a transcript | What is known, assumptions, the questions that matter next |
| **Route** | A workflow and constraints | Separate choices for surface, capability/architecture, deployment/operations |
| **Design** | An agreed outcome | Data flow, output contract, tool boundaries, review, failure paths |
| **Evaluate** | A candidate design or model | Representative cases, risk slices, acceptance criteria, comparison plan |
| **Review readiness** | A prototype or launch proposal | Evidence gaps, stage-specific blockers, owners, recovery work |
| **Build** | A validated scope | A thin vertical slice, ordered tasks, acceptance examples, verification |

**One entry point, selective context.** The agent reads the relevant playbook instead of loading a large manual every time. Client decisions can accumulate in a private solution snapshot so the next call starts where the last one ended.

## Get started

Use Git to clone the toolkit and Python 3.10+ to run the optional installer. Substitute `python3` on macOS or Linux, or `py` on Windows, if that is how you launch Python. The skill itself is Markdown.

```sh
git clone https://github.com/afurm/ai-practitioner-toolkit.git
cd ai-practitioner-toolkit
python scripts/install.py --tool both --dry-run
python scripts/install.py --tool both
```

The installer copies the self-contained skill to your personal skill directories:

| Tool | Destination | Invoke |
|---|---|---|
| Codex | `~/.agents/skills/ai-practitioner/` | `$ai-practitioner` |
| Claude Code | `~/.claude/skills/ai-practitioner/` | `/ai-practitioner` |

Use `--tool codex` or `--tool claude` to install just one. Reopen the assistant session if the skill does not appear. Paths and invocation are based on the [OpenAI](https://learn.chatgpt.com/docs/build-skills) and [Claude Code](https://code.claude.com/docs/en/skills) documentation checked on November 23, 2026.

For a team project, install into an existing project directory:

```sh
python scripts/install.py --tool both --project /path/to/client-project --dry-run
python scripts/install.py --tool both --project /path/to/client-project
```

This uses `.agents/skills/` and `.claude/skills/` inside that project. Inspect the copied files before committing them. The installer makes no network requests, changes no agent settings, and refuses to overwrite an existing different skill. See [installation and updates](docs/installation.md) for manual installation and conflict handling.

## Use it on your next client call

In Codex:

```text
$ai-practitioner discovery

My client wants an assistant that helps account managers prepare for meetings.
We know they have CRM notes, but not what data each user may see.
Prepare the questions I should ask on the first call.
Separate facts from assumptions and explain what each question changes.
```

In Claude Code, use the same request with `/ai-practitioner discovery`.

A good response would identify the output and access model as open, ask for a concrete example, and leave the final route provisional. See the [worked account-brief example](examples/account-brief.md).

After the client answers:

```text
$ai-practitioner blueprint

Use our existing private solution snapshot and the answers below.
Update changed assumptions, propose the smallest first version,
and show the data flow, review boundary, and failure behavior.
Do not add CRM write-back; this version only prepares drafts.
```

When ready to implement:

```text
$ai-practitioner build

Use the accepted blueprint in this project. Inspect the existing code,
implement the first safe vertical slice, and verify its acceptance cases.
Report what changed, what was tested, and what still blocks a pilot.
```

The skill supports implementation work, but it is not a prebuilt application or a deployment integration. It relies on the tools and authorization available in your assistant session.

## A practical working rhythm

1. **Before the call:** paste sanitized context and ask for a discovery brief.
2. **After the call:** reconcile answers into a private solution snapshot.
3. **Before choosing a stack/model:** request three-axis routing and alternatives.
4. **Before building:** agree a first-pass blueprint and an evaluation plan.
5. **During delivery:** turn the next slice into implementation and acceptance work.
6. **Before a pilot or release:** review evidence, access, capacity, ownership, monitoring, and recovery for that stage.

The [copyable templates](skills/ai-practitioner/assets/templates.md) help preserve context between sessions. Keep client material in an authorized **private location outside this repository**. Ignored local folders are an extra convenience, not a guarantee against accidental publication.

## Principles that change the recommendation

- Start with the work, not the model name.
- Keep surface, capability/architecture, and deployment/operations separate.
- Distinguish facts, assumptions, unknowns, and accepted decisions.
- Start with the minimum viable capabilities for the current scope.
- Separate read access, write permissions, identity, audience, funding, and approval.
- Treat schema validity, citations, demos, and average scores as partial evidence.
- Validate representative failures and critical risk slices before release.
- Match readiness evidence to the next stage; safe prototypes and production have different gates.
- Escalate a concrete specialist question when the available evidence is insufficient.

## Why a skill instead of a fleet of agents?

The reusable value is the decision process and client context. A skill makes it available on demand without requiring an orchestration service, extra credentials, or repeated copies of a long system prompt. Six playbooks keep specialized guidance available while preserving one installation and one invocation. Add automation or specialist agents later when observed delivery needs justify them.

## Inside the repository

```text
skills/ai-practitioner/
  SKILL.md                 Entry point and evidence rules
  references/              Six playbooks, field guide, source register
  assets/templates.md      Intake, snapshot, call brief, build task
examples/                  Synthetic worked client scenarios
evals/                     Behavioral cases and manual scoring guidance
scripts/                   Local installer and repository validation
tests/                     Installer safety and portability checks
docs/                      Installation and methodology notes
```

## Scope, provenance, and trust

This is an **independent, original community toolkit** informed by study discussions about OpenAI Technical Practitioner and public technical documentation. It is not the official course, a complete course archive, an exam answer collection, or an endorsed OpenAI/Anthropic product. It does not redistribute course screenshots or authenticated course materials.

The [field guide](skills/ai-practitioner/references/field-guide.md) preserves the durable concepts discussed; the [source register](skills/ai-practitioner/references/sources.md) records the public references. Live product details must be rechecked against current documentation and the client's actual environment. The toolkit cannot provide compliance certification or specialist sign-off.

## Validation and contribution

```sh
python scripts/validate.py
python -m unittest discover -s tests -v
```

CI checks packaging, internal links, portable skill metadata, installer behavior, and the declared governance contracts across **Windows, macOS, and Linux**, using Python 3.10 and 3.12. The [behavioral eval pack](evals/README.md) is a separate evaluation; structural CI does not prove recommendation quality.

The [November 23 validation report](evals/results/2026-11-23/report.md) includes twelve synthetic Codex cases and two focused retests. One initially premature hosting recommendation prompted a guidance fix. The final sampled answers met their rubrics under primary-assistant review.

Explicit skill invocation worked in both Windows desktop hosts. Codex loaded the discovery playbook for one request, and Claude Code handled three synthetic cases in one session. A standalone Codex child process hit a runtime provisioning error. On macOS and Linux the checks cover packaging and installation. The evidence supports using the skill to prepare and review client work with a practitioner. [Cross-platform and native test results](evals/results/2026-11-23/cross-platform.md)

To run model evaluations yourself (opt-in, using your authenticated Codex CLI and normal usage):

```sh
python scripts/run_evals.py --output eval-results/my-run
```

The [governance policy](docs/governance.md) documents owner-only PR merges, the owner-authored PR review exception, mandatory CI, and fork workflow approval. All files are code-owned by `@afurm`. Outside contributions are welcome through PRs; only the owner can merge upstream changes.

Bring improvements with a synthetic scenario, observed failure, and expected behavior. See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

**MIT licensed. Built for practitioners who need the next good question—and the next concrete step.**
