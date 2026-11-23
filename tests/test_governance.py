"""Protect the published owner and CI invariants in declarative ruleset files."""

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class GovernanceTests(unittest.TestCase):
    def test_only_owner_has_pr_scoped_merge_and_review_bypass(self):
        rulesets = [json.loads(p.read_text(encoding="utf-8")) for p in (ROOT / ".github/rulesets").glob("*.json")]
        self.assertEqual(len(rulesets), 3)
        rules = {r["name"]: r for r in rulesets}
        for name in ("Owner-only PR merges", "Owner review"):
            self.assertEqual(rules[name]["bypass_actors"], [
                {"actor_id": 6375192, "actor_type": "User", "bypass_mode": "pull_request"}
            ])
            self.assertEqual(rules[name]["enforcement"], "active")
            self.assertEqual(rules[name]["conditions"]["ref_name"]["include"], ["refs/heads/main"])
        self.assertTrue(any(r["type"] == "update" for r in rules["Owner-only PR merges"]["rules"]))
        review = rules["Owner review"]["rules"][0]["parameters"]
        self.assertTrue(review["require_code_owner_review"])
        self.assertEqual(review["required_approving_review_count"], 1)

    def test_integrity_has_no_bypass_and_requires_ci(self):
        config = json.loads((ROOT / ".github/rulesets/03-main-integrity.json").read_text(encoding="utf-8"))
        self.assertEqual(config["bypass_actors"], [])
        rules = {r["type"]: r for r in config["rules"]}
        for kind in ("pull_request", "deletion", "non_fast_forward", "required_linear_history", "required_status_checks"):
            self.assertIn(kind, rules)
        checks = rules["required_status_checks"]["parameters"]
        self.assertTrue(checks["strict_required_status_checks_policy"])
        self.assertEqual(checks["required_status_checks"], [{"context": "Required checks", "integration_id": 15368}])
        self.assertTrue(rules["pull_request"]["parameters"]["required_review_thread_resolution"])
