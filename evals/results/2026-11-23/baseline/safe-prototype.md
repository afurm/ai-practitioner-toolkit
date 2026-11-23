Build a local draft preview using the approved synthetic fixtures while retention and production hosting reviews continue. Confidence is high that this slice can validate the draft workflow. Production readiness remains open.

**Scope and decisions**

The client confirmed the synthetic fixtures and draft-only scope. Use the existing application stack and inspect its entry point and generation interface before placing the change. The proposed slice returns a preview in the current session. Persistent drafts, real records, external delivery, business-system write-back, and production deployment are deferred. If generation requires a remote service, verify authorization for that service and its handling of fixture data before sending inputs.

**Implementation sequence**

1. **Define the fixture and draft contracts.** Map each approved fixture to the inputs the task needs. Define a result containing either a reviewable draft or a clear error. Use the agreed draft format if one exists. Otherwise, propose a minimal format based on the fixture fields. Acceptance: a valid fixture produces a usable input, and an unknown fixture or one missing a required field returns an error before generation. Proposed owner: implementation engineer. Evidence: contract checks against the approved fixtures and malformed inputs.

2. **Connect fixture selection to draft preview.** Run the draft task from the application’s existing entry point and present the result for human review. Keep inputs and outputs out of persistent application storage and content logs. Acceptance: a reviewer can select a fixture and see a draft clearly marked as such. If generation fails, the interface shows an error and clears any stale preview. Proposed owner: implementation engineer. Evidence: an end-to-end walkthrough, a simulated generation failure, and a check of storage, logging, and outbound calls.

3. **Review draft quality and close the handoff.** Compare the drafts with their fixtures for factual support, required content, and treatment of missing information. Include a fixture with incomplete information and verify that the draft handles it without inventing details. Proposed owner: workflow owner, to be confirmed. Record the fixtures exercised, checks run or skipped, failures, and open decisions.

The slice is complete when a reviewer can generate and inspect a fixture-backed draft, the failure cases behave as specified, and the team has recorded the evidence. If the preview needs to be withdrawn, disable or revert its entry point. Release remains gated on the retention and production hosting reviews.