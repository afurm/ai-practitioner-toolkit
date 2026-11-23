# Field guide: durable practitioner distinctions

This is an original synthesis of concepts discussed while studying the OpenAI Technical Practitioner learning material, supplemented by public documentation. It is not the official course, a complete transcript, or certification guidance. Course access and screenshots are not included.

## Six knowledge areas

| Area | Practical judgment |
|---|---|
| Solution architecture | Translate the workflow into a provisional surface, capability combination, operating approach, and blueprint. |
| Model selection | Start from task shape/output requirements, compare viable candidates, and validate tradeoffs with representative evidence. |
| API integration | Define inputs, output contracts, state, tool execution, coordinator ownership, and error/approval boundaries. |
| Retrieval design | Assemble approved, relevant, current, authorized context; evaluate whether claims are supported and gaps handled. |
| Security governance | Establish owners, permissions, enforced boundaries, review, auditability, and escalation proportional to consequence. |
| Data readiness | Establish authority, ownership, sensitivity, access, movement, quality, retention, and permitted output audience. |

## Discovery layers versus routing axes

Discovery gathers evidence through user/workflow, context/data, runtime/tools, and governance/observability. Routing turns that evidence into separate choices about surface, capability/architecture, and deployment/operations. They answer different questions; do not force a one-to-one mapping.

## Request and response vocabulary

- **Input/approved context:** the request and authorized information supplied for the task.
- **Output contract:** expected text or structured fields and their meaning; schema compliance is one part.
- **State:** information needed to continue the workflow, including pending and completed operations.
- **Trace:** recorded model outputs, tool calls/results, approval events, and actions. Do not require private model reasoning.
- **Runtime owner:** the application or managed service coordinating steps, distinct from API interface and tool hosting.
- **Bounded decision:** selection from a fixed allowed set or a defined score. Free-form explanation is a separate output requirement.

## Controls and evidence

- **Structured output:** predictable fields for downstream processing, not a truth guarantee.
- **Guardrail:** an enforced content/action boundary. Prompt wording alone is insufficient for access control.
- **Evaluation:** systematic tests of quality, failure, and task-specific risk against agreed expectations.
- **Observability:** signals used to understand and operate the workflow after launch.
- **Auditability:** evidence sufficient to reconstruct who requested, produced, reviewed, approved, and acted.
- **Human review:** verification or approval where consequences, uncertainty, policy, or action risk require it.
- **Least privilege:** only the access needed for the approved task, rather than broad access narrowed by prompts.
- **Rollback:** restoration of a safe software/configuration state; external actions may need compensation instead.

## Maturity of a recommendation

An early cue suggests a route. A pattern provides a reusable shape. A first-pass blueprint applies it to the client and records validation items. Detailed technical design resolves implementation-specific authentication, data, integration, deployment, support, and control details. Readiness is stage-specific evidence, not confidence in the demo.

## Avoid recurring category errors

- “AI assistant” does not by itself mean an autonomous agent.
- Several steps do not by themselves require agentic orchestration.
- API selection does not determine runtime ownership.
- MCP is an integration option, not mandatory for every external system.
- Sensitivity does not by itself select a model or hosting arrangement.
- A valid schema, citation, watermark, demo, or average score does not establish overall correctness or readiness.
- A model's token price does not include integration, retrieval, retries, human review, and operations.
- Sign-in/subscription usage does not grant access to business tools or prior personal conversations.
- A source link does not inheritably restrict every copy of its content.

## Keep changing platform details outside the mental model

Verify actual feature names, endpoints, models, pricing, capacity, hosting, agreements, and retention against [official sources](sources.md) for the client's environment. Teaching labels are not evidence of current availability. Evidence-backed specialist escalation is part of technical fluency, not a substitute for doing the available discovery work.
