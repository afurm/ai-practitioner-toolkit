**Recommendation:** Build a read-only internal portal that drafts one account brief per request from notes the signed-in sales user is permitted to read. Confidence is high in this first-version scope. The permission source, section template, draft retention, and hosting still need confirmation.

**Agreed scope:** The client chose an internal portal, fixed sections, references, and sales-user review. Account permissions vary by team. Write-back, voice, scans, and scheduling are out of scope.

### Workflow and responsibilities

1. **Request and authorize.** The sales user selects an account and requests a draft. The backend checks current account permissions before fetching notes. It uses the user’s identity or enforces equivalent permissions server-side, including any note-level restrictions. If the permission check is unavailable, generation stops. Before reopening a draft or following a reference, the portal checks current access again.
2. **Assemble context.** Fetch only authorized notes for the selected account. Include note IDs, dates, and available version metadata. Treat note text as source material. Distinguish an empty result from a source failure, and flag conflicting or undated evidence where it affects the brief.
3. **Draft and validate.** The model fills the agreed sections and attaches references to factual claims. Each section can indicate insufficient or conflicting evidence. The backend validates required sections and checks each reference against the retrieved notes. Sales-user review checks whether the cited text actually supports the claim. Invalid output gets one bounded retry, then a visible failure.
4. **Review and display.** Show the draft and permitted note excerpts side by side. The sales user checks accuracy and relevance and can mark the draft reviewed. The proposed first version keeps drafts visible only to the requester. Track pending, ready, reviewed, and failed states, and deduplicate repeated submissions while generation is pending.

Record request ID, access decision, source versions, generation outcome, latency, and review status in restricted logs. Exclude raw note and draft text. Confirm retention and monitoring ownership before a pilot. The proposed rollback is to disable generation.

### Validation before a pilot

- **Access:** The proposed security or data owner identifies the authoritative permission source and verifies cross-team denial, any note-level restrictions, and access revocation for existing drafts and references. Proposed gate is zero unauthorized disclosures in the test set.
- **Brief quality:** The proposed sales lead approves the section template and reviews sample briefs for completeness, citation support, missing-evidence handling, and time saved versus manual drafting. Capture baseline review time and agree on acceptance thresholds before the pilot.
- **Deployment:** The proposed platform owner confirms where note text, drafts, and logs are processed and stored, who can access them, and how long they persist.

Start with two test users whose account permissions differ. The first slice is complete when each can review a referenced brief for an allowed account and cross-account requests are denied before note retrieval.