# Responses after the first guidance change

## urgent-failures

**Hold the automated launch at the current threshold.** I’m confident in that recommendation because your team reports missed urgent cases at the threshold you plan to use. Keep the current routing workflow in place while you test alternatives in shadow mode, where router decisions have no effect on live tickets.

**Evidence and open decisions.** Your team reports strong average performance and missed urgent cases. The urgent-case count, severity, and miss rate are unknown, as are the current workflow’s miss rate and the review queue’s capacity. Confirm what qualifies as urgent and how quickly those tickets need human attention. I propose that the accountable support operations owner approve the launch criteria before held-out results are reviewed.

**Comparison.** Replay the same labeled tickets through the current routing workflow, the router at its chosen threshold, and the same router at a lower threshold. Keep the model and prompt fixed. Use development data to select the lower threshold, then freeze it and evaluate on a separate, untouched set. Record the model and prompt versions, thresholds, ticket data version, and run date. Have support reviewers label independently and adjudicate disagreements. Include representative historical tickets to estimate queue load and a separate set of rare urgent cases to test failure modes.

| Case | Input fixture and risk | Expected behavior and pass check |
|---|---|---|
| U1 | Known missed urgent ticket, including indirect wording | Reopen as a regression case. Pass if it reaches the urgent queue or receives review within the agreed urgent response window. |
| U2 | Held-out urgent ticket with incomplete details | Escalate or abstain into priority review. Fail if it lands in the routine queue. |
| R1 | Routine ticket with alarming wording | Pass if routed correctly. Count unnecessary escalation toward review burden. |
| F1 | Synthetic scoring timeout | Pass if the ticket enters human review with its original arrival time preserved and no silent routine assignment. |

Run each case using only the context available to the production router. Label synthetic cases and report them separately.

**Proposed launch gate.** Require zero misses on the agreed highest-severity held-out cases and enough urgent examples to bound the overall miss rate against an owner-approved tolerance. Report urgent recall and miss counts by severity, uncertainty, false escalations, peak review volume, and end-to-end time to triage. Review load and triage delay must fit staffed capacity and the agreed response window. If the review queue cannot meet that window, use the existing routing workflow.

**Next step.** Have the support operations owner commission the replay and review a side-by-side results table against the agreed gates. This evaluation is unrun, and launch approval is pending.

## crm-brief-source-audit

### Private Finance review

**1 of 4 claims can be shared unchanged.**

| Claim | Classification | Disposition |
|---|---|---|
| 1. June 4 kickoff | Stale. S1 records the original date, and S2 explicitly supersedes it. | Replace with June 18 and cite S2. |
| 2. Mira Chen is the sponsor | Current, supported by S2, and authorized for Sales. | Share unchanged. |
| 3. Approved 12% renewal discount | Unsupported. S2 contains no discount approval, and the complete packet supplies none. | Omit. |
| 4. Finance routing marker | Supported by F1 and restricted to Finance. | Omit from the Sales brief. |

Before sharing, the account owner should verify who can actually view the destination, including through inherited permissions or sharing links, and confirm that recipients can access the cited S2. Share only the replacement copy there. If the destination includes viewers outside the intended audience, narrow access or use an authorized destination.

### Sales-facing replacement

Cedar Quay’s agreed kickoff is June 18 [S2]. Mira Chen remains the customer sponsor [S2].

## shift-board-release

**Crew-facing correction**

Report to Bay D at 19:30 tonight. (Source H2)

**Supervisor**

Hold the post. H2 is the signed replacement for tonight and supersedes H1’s Bay B assignment. The batch marker is Payroll-only and must stay out of the crew handoff.

Verify who can actually view the Evening Packing board, including anyone with inherited or contractor access. Post the correction only once you confirm that every viewer is authorized to receive the evening packing notice. If the board includes other viewers, restrict access or use an authorized destination.
