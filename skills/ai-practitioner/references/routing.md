# Routing: keep three decisions separate

Use a three-row memo. Each row should contain a provisional choice, supporting evidence, a credible alternative, the condition that would change it, and unresolved validation. “Unknown” is a valid choice.

## 1. User or product surface

These are workflow cues, not guarantees about a particular subscription or feature:

| Signal | Plausible starting surface | Validate |
|---|---|---|
| User stays involved in Q&A, reasoning, and drafting | ChatGPT Chat | Input method, needed context, output handling, permissions |
| User delegates a deliverable or shared recurring knowledge task | ChatGPT Work | Available features, source access, execution identity, scheduling, handover, review |
| Primary work concerns repositories, debugging, tests, or code changes | Codex | Repository access, execution environment, checks, review boundaries |
| AI must operate inside a product or a custom business process | Application/process built with the API | Integration ownership, interfaces, reliability, cost, operations |

A coding agent may help implement a claims application without being the claims user's product surface. A shared document is an artifact, not the entire architecture. Multiple surfaces can coexist when the workflow justifies them.

## 2. Capability and architecture

Select the necessary combination:

- Supplied context plus generation for bounded drafting when all necessary information is present.
- Retrieval-grounded generation when approved knowledge is needed beyond current context; include access enforcement, freshness, source support, and missing-evidence behavior.
- Classification or extraction for bounded labels or fields; define the output contract and business validation.
- Tool integration for live lookup or action; distinguish read and write operations.
- Explicit orchestration for known steps, conditions, retries, and human approval.
- Agentic control when dynamic tool/step selection adds demonstrated value. Several steps alone do not justify it.
- Multimodal processing when images, scans, audio, or other modalities are necessary.
- Voice/realtime interaction when live spoken interaction and its latency requirements matter.

For model selection, compare candidate classes on representative task evidence, hard capability requirements, risk, latency, and total cost. Evaluate a simpler viable candidate before increasing complexity. Larger context is not a substitute for accurate retrieval, and low token price is not total operating cost.

For bounded decision endpoints versus generative endpoints, check current official documentation for supported outputs and availability. Do not hardcode a course-era model name as a universal default. See [sources](sources.md).

## 3. Deployment and operations

Specify separately:

- Where model inference, source data, tool execution, and workflow coordination run.
- Whether application code or a managed runtime coordinates steps. API interface selection does not settle this.
- Identity, data boundaries, retention, secrets, regional/hosting constraints, and output audience.
- Volume, burst/concurrency assumptions, latency, service limits, failure/retry policy, ownership, and recovery.
- Funding and subscription requirements, distinct from system permissions.

If “our own infrastructure” is the only evidence, clarify which components must run there before selecting a surface or model. Customer-managed models require an operating and evaluation plan; sensitivity alone does not decide that route.

## End with a conditional recommendation

“Given [evidence], start by testing [route]. This assumes [assumption]. If [condition], prefer [alternative]. Validate [decision-changing unknown] through [small experiment] before committing to [next stage].”
