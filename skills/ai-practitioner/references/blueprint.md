# Blueprint: apply a pattern to the client's workflow

A pattern is reusable; a blueprint specifies the particular users, sources, data flow, tools, controls, and success measures. A first-pass blueprint can retain explicit validation items. It does not certify final security or production design.

## Describe the flow

Start with a short sequence, adding a diagram only if useful:

`trigger -> identity/access check -> approved context -> model task -> validation -> human review when required -> permitted action/output -> trace and monitoring`

Adapt this to the workflow; human approval is risk/policy dependent, not automatically necessary for every read or draft. Do not add write-back, realtime, or agent orchestration without a concrete need.

Cover the relevant boundaries:

1. **Inputs and sources:** user request, authoritative data, ownership, refresh/version, sensitivity, permitted users and destinations.
2. **Context assembly:** supplied context versus retrieval, authorization before context assembly, source references, conflicting or missing records, provenance of externally supplied text.
3. **Model task and contract:** expected fields or text, bounded labels, supported references, uncertainty/refusal/incomplete behavior, semantic/business checks beyond schema.
4. **Tools:** operation, execution identity, allowed resources, input validation, read/write distinction, timeout and failure behavior, action scope.
5. **State and orchestration:** who runs the loop, what persists, pending/completed/failed statuses, retry limits, deduplication/idempotency for effects, resume behavior.
6. **Review and action:** reviewer role, what evidence they see, what they approve, expiry or changes that invalidate approval, escalation path, safe fallback.
7. **Operations and evidence:** redacted traces, access and retention for logs, measurable quality and service targets, monitoring owner, rollback or compensating action.

## Make retrieval failures visible

Do not equate a citation with an accurate answer. Evaluate retrieval relevance, source freshness, claim support, and access enforcement separately. Missing authority should produce an explicit gap, request for clarification, or agreed escalation—not a plausible invented policy.

Access to source records does not automatically authorize publication of copied details. Re-check the generated artifact's audience. Disconnecting a source does not prove existing copies have been removed.

## Make side effects explicit

A CRM lookup and a forecast update need different permissions and tests. Keep dependent writes pending until actual lookup evidence is available and any required approval is recorded. Execute controls in application/tool code where possible; a policy paragraph in a prompt is not an authorization boundary.

Record requested action, caller identity, source/version, proposed change, decision, approval reference, actual tool result, and failure outcome as needed for auditability. Minimize sensitive content in logs; define who can see it and how long it remains.

## Deliver

Return the flow, component responsibilities, contracts, failure paths, minimum viable capabilities, deliberately deferred capabilities, success measures, and a short validation backlog. For final design questions beyond available evidence, name the specialist and exact unresolved issue.
