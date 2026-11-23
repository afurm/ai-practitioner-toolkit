# Contributing

Improve the next decision a practitioner makes. Prefer a focused change over a longer checklist.

For a behavior change, include a synthetic scenario, observed output or failure, desired behavior, and the reason it matters. Add or update a case in `evals/cases.jsonl` when useful. State which evaluations were actually run and their limitations.

Keep the skill self-contained: references and templates needed after installation belong inside `skills/ai-practitioner/`. Keep provider-specific product facts linked and dated rather than hardcoding a preferred model. Preserve existing user choices and authorization boundaries. Do not add automatic external side effects.

Do not contribute client data, secrets, private transcripts, proprietary course assets, authenticated links, or certification question banks. Use original explanations and synthetic examples. Contributions are under the repository's MIT license.

Run before opening a pull request:

```sh
python scripts/validate.py
python -m unittest discover -s tests -v
```

Structural checks do not replace reviewing actual skill behavior. For the initial version, the behavioral pack is designed for manual or agent-assisted runs; do not represent structural CI as a passed live model eval.
