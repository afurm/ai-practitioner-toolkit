# Example: urgent support cases hidden by a strong average

**Synthetic example, not an executed evaluation.**

The client wants an embedded classifier that assigns one support category and drafts an explanation. Simple cases look good, but urgent cases are sometimes sent to the normal queue. They have not agreed a threshold or review capacity.

## Judgment to preserve

An average score is insufficient. Keep urgent-case misses in the evaluation set and measure that slice separately. Do not move to a more complex architecture merely because a failure exists; inspect whether the problem is task definition, examples, threshold, retrieval, or capability.

The category is a bounded output; the explanation is generated text. Define each contract and validate consistency. Verify current endpoint support if choosing specialized bounded-decision and generative APIs; no endpoint name proves suitability.

## Next questions

- What makes a case urgent, who owns that definition, and what is the cost of missing it?
- What review volume can the support team handle, and what is the escalation deadline?
- Does the model need approved policy context or only the message and allowed labels?

## Next experiment

Collect approved, labeled cases across normal, urgent, ambiguous, incomplete, and misleading inputs. Keep threshold tuning separate from a held-out test set. Compare simple candidates and threshold settings using urgent recall, false-positive burden, category correctness, explanation support, latency, and total cost per handled case.

Propose an uncertain-case review route and have the support owner accept the criteria before interpreting results as launch evidence. Record all numbers as proposed until agreed; report measurements only after actually running the experiment.

If later adding ticket updates, validate execution identity, resource scope, actual lookup results, required approval, duplicate prevention, and compensating actions separately from read-only classification.
