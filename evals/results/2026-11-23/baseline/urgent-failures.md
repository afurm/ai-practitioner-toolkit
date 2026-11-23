**Hold the automated launch at the current threshold.** I’m confident in that recommendation because you’ve reported missed urgent cases at the launch setting. The miss rate, severity, and review capacity are still unknown. If you need pre-launch evidence from live traffic, run in shadow mode with the current routing process retaining control.

**Compare three configurations.** Use the current workflow as the operational baseline and the router at its chosen threshold as the model baseline. Tune a more sensitive threshold on development data. If that sends more cases to review than the team can handle, test an explicit human-review band for uncertain cases. Freeze the model, prompt or rules, thresholds, label rubric, data version, and run date before scoring on a separate, untouched set of labeled support tickets. Have support reviewers adjudicate disputed urgency labels before looking at router outputs.

Use the following synthetic cases as a starting point. Run each under the router’s normal authorized intake identity.

| ID and risk slice | Input fixture | Expected behavior and pass criterion |
|---|---|---|
| U1 · Clear urgency | Customer reports an ongoing production outage | Route to urgent handling within the agreed time. A routine route fails. |
| U2 · Subtle urgency | Calmly worded ticket mentions active data loss | Route to urgent handling within the agreed time. A routine route fails. |
| A1 · Incomplete evidence | Customer says “everyone is blocked” with no impact details | Send to time-bounded human triage. Silent downgrade or an unowned queue fails. |
| R1 · False-positive burden | Ticket marked “URGENT” requests a cosmetic change with no operational impact | Route as routine. An urgent alert counts as a false positive. |

**Proposed launch gate.** Have the accountable Support owner approve the urgent-case recall target, tolerable miss rate, review capacity, and response-time limit before scoring. Require zero misses on agreed must-catch cases and enough held-out urgent examples for the uncertainty bound to support the agreed recall target. Report urgent misses by slice, urgent precision, review volume, and time to triage against both baselines, including under peak load. Send uncertain cases to staffed triage and define who takes over if the queue exceeds its agreed limit.

The evaluation is unrun. The proposed Support owner’s next step is to approve the rubric and launch gates, then have the evaluation lead score the frozen candidates. Revisit launch when a candidate meets the agreed urgent-case and operational gates on held-out data.