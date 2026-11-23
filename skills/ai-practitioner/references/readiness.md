# Readiness: enough evidence for the next stage

Implementation readiness means enough clarity to take the next build step responsibly; it is not synonymous with production release. Name the stage being reviewed.

| Stage | Typical evidence needed |
|---|---|
| Safe prototype | Defined task/output, safe or synthetic inputs, baseline, experiment owner, limited scope |
| Limited pilot | Authorized representative sources/users, access controls, agreed review/escalation, task eval evidence, operator, restricted exposure and recovery |
| Production | Accepted quality and failure evidence, production access/data controls, capacity/service targets, monitoring and incident owner, support, rollback/compensation, release authority |

Requirements depend on workflow risk and organizational policy. Mark each relevant item **evidenced**, **partial**, **unknown**, or **blocking for this stage**, with source/date, consequence, proposed owner, and validation action. Do not manufacture an arbitrary numerical readiness score.

## Review areas

- **Workflow:** named user group, output and audience, success criteria, scope, baseline, training/adoption needs.
- **Data:** owner, authority, freshness, intended use, sensitivity, permissions, movement, retention/deletion, copies in artifacts and logs.
- **Interface and runtime:** input/output contracts, coordinator ownership, state/retry/resume behavior, dependency failures.
- **Security:** least privilege, execution identity, secret storage/rotation, environment separation, authorization and approval enforcement, untrusted input handling.
- **Quality:** representative evals, critical risk slices, thresholds, reviewer calibration, refusal/uncertainty behavior.
- **Operations:** peak traffic and concurrency assumptions, rate limits, load evidence, latency budget, end-to-end cost, alert thresholds and responder.
- **Release/recovery:** staged rollout, stop conditions, rollback limitations, compensating actions for external writes, support/incident responsibility.
- **Specialist validation:** exact unresolved architecture, security, legal/compliance, or platform behavior question; named accountable function and required evidence.

Do not equate faster processing with sufficient peak capacity. A working demo and executive support do not settle data access, controls, monitoring, or ownership. A smaller pilot reduces exposure but does not eliminate controls needed for its actual users and data.

## Important distinctions

- Authentication, funding, business-tool permissions, and action approvals are separate checks.
- Source permissions do not automatically protect copied summaries with a wider audience.
- Customer possession of records is not evidence for access, custody, retention, or configuration of the full workflow.
- A watermark/provenance signal concerns origin; it is not proof of correctness, ownership, or human approval.
- If health/regulated information is involved, validate the exact applicable agreement, eligible feature, configuration, and organizational requirements with the accountable specialist. Do not declare compliance from a product label.
- Keeping secrets in environment configuration does not replace authorization. Keep credentials out of prompts, shared documents, generated deliverables, and repositories.

## Deliver

State what can proceed now, what is blocked for the named stage, and the smallest next validation actions. For each blocker give the evidence needed and a proposed owner. Do not stop all safe implementation merely because production requirements are incomplete; separate a safe experiment from a release decision.
