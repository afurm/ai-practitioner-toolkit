"""Validate failure detection, not generated document wording."""

import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "scripts" / "validate.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "skills", self.root / "skills")
        (self.root / "evals").mkdir()
        shutil.copyfile(ROOT / "evals/cases.jsonl", self.root / "evals/cases.jsonl")

    def test_portable_skill_and_cases_are_valid(self):
        self.assertEqual(validator.validate(self.root), [])

    def test_missing_internal_reference_is_reported(self):
        (self.root / "README.md").write_text("[missing](missing.md)", encoding="utf-8")
        self.assertTrue(any("Broken/escaping link" in e for e in validator.validate(self.root)))

    def test_skill_cannot_depend_on_repo_only_reference(self):
        (self.root / "repo-only.md").write_text("Reference", encoding="utf-8")
        with (self.root / "skills/ai-practitioner/SKILL.md").open("a", encoding="utf-8") as f:
            f.write("\n[External dependency](../../repo-only.md)\n")
        self.assertTrue(any("not self-contained" in e for e in validator.validate(self.root)))

    def test_duplicate_eval_id_is_reported(self):
        file = self.root / "evals/cases.jsonl"
        first = file.read_text(encoding="utf-8").splitlines()[0]
        with file.open("a", encoding="utf-8") as f:
            f.write(first + "\n")
        self.assertTrue(any("duplicate" in e for e in validator.validate(self.root)))

    def test_private_generated_folders_are_not_read(self):
        for folder in ("private", "eval-results", ".venv"):
            path = self.root / folder
            path.mkdir()
            (path / "invalid.md").write_bytes(b"\xff\xfe")
        self.assertEqual(validator.validate(self.root), [])
