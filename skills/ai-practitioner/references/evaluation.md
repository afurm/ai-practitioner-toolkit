# Evaluation: test the actual decision

An evaluation plan is not a result. Public benchmarks are useful candidate evidence, not acceptance for a customer's workflow. Define who accepts the criteria before interpreting scores as readiness.

## Choose the comparison

State the task and baseline: current manual workflow, deterministic rules, an existing prompt/model, or another implementation. Compare one meaningful change at a time where feasible. Pin the tested model/configuration, prompt, dataset, source versions, tools, and date.

Choose metrics appropriate to the workflow:

| Task | Useful measurements |
|---|---|
| Classification/routing | Per-class precision/recall, confusion matrix, urgent-case false negatives, review volume, abstention |
| Extraction | Field correctness, missing-value handling, schema validity, source evidence, semantic constraints |
| Retrieval Q&A | Retrieval relevance/coverage, freshness, claim support, citation correctness, authorized access, missing-evidence behavior |
| Drafting | Factual support, completeness, reviewer rubric, correction effort, time saved |
| Tool workflow | Correct operation/resource/arguments, authorization, approval coverage, state transitions, duplicate effects, recovery |
| All workflows | End-to-end latency including review/retries, throughput, error rate, cost per completed acceptable outcome |

Do not assume model self-reported confidence is calibrated. Set and validate thresholds on suitable development data, then evaluate on a separate held-out set. Preserve an untouched test set when tuning. Use qualified human reviewers to calibrate subjective or model-based graders and assess disagreement.

## Build representative cases

Include normal, ambiguous, rare/high-consequence, incomplete, stale/conflicting-source, out-of-scope, unauthorized-access, malicious embedded instruction, refusal, tool timeout, partial-failure, retry/duplicate, and changed-approval cases where relevant. Do not add irrelevant categories merely to fill a checklist.

For each case record: ID, input fixture, authorized context/identity, expected behavior, prohibited behavior, metric/rubric, risk slice, and pass criterion. Synthetic fixtures must be labeled; they do not establish real distribution coverage.

Measure critical slices separately from averages. A strong overall score does not excuse missed urgent cases. Do not remove difficult examples to improve reported results. Compare threshold changes against their false-positive burden and the human escalation capacity.

## Deliver

Provide a runnable or human-executable case table, candidate comparison plan, proposed acceptance criteria, failure/abstention/escalation policy, and who accepts results. If tools/data are unavailable, deliver the plan and say it is unrun. Do not invent measured latency, cost, accuracy, or sign-off.

After running, report dataset size/composition, configuration, results by material slice, uncertainty/limitations, observed failure patterns, and the next experiment. Retest affected cases after changes. Select the simplest option that meets the agreed quality, risk, latency, and cost requirements.
