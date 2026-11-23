# Discovery: understand the work before routing it

Use for incomplete requests, call preparation, or transcript synthesis. First extract what is already available. Ask for one concrete instance of the current workflow and an example of a good output; this often resolves more than a feature wishlist.

## Four layers

| Layer | Establish | Questions that change the design |
|---|---|---|
| User and workflow | User, trigger, current steps, pain, output, business outcome | Who does what today? Where does delay occur? Who uses the output? What observable improvement matters? |
| Context and data | Necessary information, sources, owners, quality, sensitivity, access, movement, retention | Which source is authoritative? Can each intended user access it? What happens when records conflict or are stale? |
| Runtime and tools | Interaction surface, scheduling, state, integrations, reads and writes | Is this live assistance or delegated work? Must it update anything? What must resume after interruption? |
| Governance and observability | Reviewer, approval policy, failure handling, operator, evidence | Which errors matter most? Who can approve consequential actions? Who investigates and stops a faulty run? |

Identify the **least clear layer that affects the next step**. There is no fixed weakest layer for every customer. Avoid choosing hosting solely from sensitivity or calling a workflow agentic solely because it has multiple steps.

## Prioritize questions

Rank unknowns by the consequence of being wrong and their effect on the proposed route. Ask the few that unblock a decision now. Supply tentative options if helpful, clearly labeled as hypotheses. Keep remaining questions in a backlog.

Examples:

- “Show me the brief someone currently prepares and the decision it supports.” Establishes the output and a baseline.
- “Should the assistant draft a recommendation, or change the underlying record?” Establishes the action boundary.
- “Do two users have different access to the same account documents?” Establishes per-user authorization needs.
- “What must stay inside your infrastructure: source storage, tool execution, model inference, or all three?” Separates hosting requirements.

## Deliver

Produce a compact workflow statement, evidence ledger, prioritized next questions with their decision impact, and a proposed validation step. Offer a tentative route only where supported. For call preparation, add a short agenda and the evidence to request; do not fabricate client answers.

When the client answers, reconcile changed assumptions, explain any changed recommendation, and move to routing or design. Discovery is not a prerequisite to every reversible prototype task; safe synthetic work can proceed while production dependencies remain open.
