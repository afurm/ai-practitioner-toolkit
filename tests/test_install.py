"""Exercise installation boundaries in disposable directories."""

import contextlib
import importlib.util
import io
from pathlib import Path
import shutil
import tempfile
import sys
import subprocess
import unittest
from unittest.mock import patch
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("installer", ROOT / "scripts" / "install.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def run_install(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return installer.main(list(args))

    def test_both_project_installs_complete_portable_folders(self):
        self.assertEqual(self.run_install("--tool", "both", "--project", str(self.base)), 0)
        for folder in (".agents", ".claude"):
            installed = self.base / folder / "skills" / "ai-practitioner"
            self.assertEqual(installer.manifest(installed), installer.manifest(installer.SOURCE))
            self.assertTrue((installed / "references" / "sources.md").exists())

    def test_dry_run_has_no_writes(self):
        self.assertEqual(self.run_install("--tool", "both", "--project", str(self.base), "--dry-run"), 0)
        self.assertEqual(list(self.base.iterdir()), [])

    def test_second_identical_install_is_noop(self):
        args = ("--tool", "codex", "--project", str(self.base))
        self.assertEqual(self.run_install(*args), 0)
        target = self.base / ".agents" / "skills" / "ai-practitioner" / "SKILL.md"
        before = target.stat().st_mtime_ns
        self.assertEqual(self.run_install(*args), 0)
        self.assertEqual(target.stat().st_mtime_ns, before)

    def test_conflict_preflight_prevents_other_destination_write(self):
        existing = self.base / ".claude" / "skills" / "ai-practitioner"
        existing.mkdir(parents=True)
        (existing / "SKILL.md").write_text("my custom skill", encoding="utf-8")
        self.assertEqual(self.run_install("--tool", "both", "--project", str(self.base)), 1)
        self.assertFalse((self.base / ".agents").exists())
        self.assertEqual((existing / "SKILL.md").read_text(encoding="utf-8"), "my custom skill")

    def test_extra_installed_file_is_not_overwritten(self):
        args = ("--tool", "codex", "--project", str(self.base))
        self.assertEqual(self.run_install(*args), 0)
        extra = self.base / ".agents" / "skills" / "ai-practitioner" / "custom.md"
        extra.write_text("local instructions", encoding="utf-8")
        self.assertEqual(self.run_install(*args), 1)
        self.assertEqual(extra.read_text(encoding="utf-8"), "local instructions")

    def test_missing_project_does_not_create_it(self):
        missing = self.base / "missing"
        self.assertEqual(self.run_install("--tool", "both", "--project", str(missing)), 1)
        self.assertFalse(missing.exists())

    def test_personal_plan_uses_expected_tool_scopes(self):
        plan = installer.installation_plan("both", home=self.base)
        self.assertEqual([p.relative_to(self.base).as_posix() for p, _ in plan], [
            ".agents/skills/ai-practitioner", ".claude/skills/ai-practitioner"
        ])

    def test_symlink_parent_is_rejected(self):
        real = self.base / "real"
        real.mkdir()
        linked = self.base / ".agents"
        try:
            linked.symlink_to(real, target_is_directory=True)
        except OSError:
            self.skipTest("Host does not allow creating symlinks")
        self.assertEqual(self.run_install("--tool", "codex", "--project", str(self.base)), 1)
        self.assertEqual(list(real.iterdir()), [])

    def test_windows_reparse_attribute_is_rejected(self):
        # Python 3.10 lacks Path.is_junction; the Windows attribute still protects it.
        with patch.object(Path, "lstat", return_value=SimpleNamespace(st_file_attributes=0x400)), \
                patch.object(Path, "is_symlink", return_value=False):
            with self.assertRaises(ValueError):
                installer.reject_links(self.base / "linked")

    def test_copy_failure_does_not_publish_partial_skill(self):
        with patch.object(installer.shutil, "copytree", side_effect=OSError("simulated disk failure")):
            self.assertEqual(self.run_install("--tool", "codex", "--project", str(self.base)), 1)
        parent = self.base / ".agents" / "skills"
        self.assertEqual(list(parent.iterdir()), [])

    def test_incomplete_source_is_rejected(self):
        source = self.base / "source"
        source.mkdir()
        with patch.object(installer, "SOURCE", source):
            self.assertEqual(self.run_install("--tool", "codex", "--project", str(self.base)), 1)
        self.assertFalse((self.base / ".agents").exists())

    def test_missing_playbook_or_template_blocks_both_install_destinations(self):
        project = self.base / "project"
        project.mkdir()
        for resource in ("references/discovery.md", "assets/templates.md"):
            source = self.base / Path(resource).stem / "ai-practitioner"
            shutil.copytree(installer.SOURCE, source)
            (source / resource).unlink()
            with patch.object(installer, "SOURCE", source):
                for flags in (["--dry-run"], []):
                    with self.subTest(resource=resource, flags=flags):
                        error = io.StringIO()
                        with contextlib.redirect_stderr(error), contextlib.redirect_stdout(io.StringIO()):
                            status = installer.main(["--tool", "both", "--project", str(project), *flags])
                        self.assertEqual(status, 1)
                        self.assertIn(resource, error.getvalue())
                        self.assertEqual(list(project.iterdir()), [])

    def test_installing_inside_source_is_rejected(self):
        with self.assertRaises(ValueError):
            installer.installation_plan("codex", project=installer.SOURCE)

    def test_invalid_tool_is_rejected(self):
        with self.assertRaises(ValueError):
            installer.installation_plan("invalid", home=self.base)

    def test_project_with_spaces_and_unicode(self):
        project = self.base / "Client project - caf\u00e9"
        project.mkdir()
        self.assertEqual(self.run_install("--tool", "both", "--project", str(project)), 0)
        for tool in (".agents", ".claude"):
            self.assertEqual(installer.manifest(project / tool / "skills/ai-practitioner"),
                             installer.manifest(installer.SOURCE))

    def test_cli_entrypoint_installs_both_tools(self):
        project = self.base / "CLI project - caf\u00e9"
        project.mkdir()
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts/install.py"), "--tool", "both", "--project", str(project)],
            capture_output=True, text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        for tool in (".agents", ".claude"):
            self.assertEqual(installer.manifest(project / tool / "skills/ai-practitioner"),
                             installer.manifest(installer.SOURCE))

    @unittest.skipUnless(sys.platform == "darwin", "macOS system alias integration test")
    def test_macos_standard_var_alias_supports_installation(self):
        self.assertTrue(Path("/var").is_symlink())
        with tempfile.TemporaryDirectory(dir="/var/tmp") as directory:
            self.assertEqual(self.run_install("--tool", "both", "--project", directory), 0)
            self.assertTrue((Path(directory) / ".claude/skills/ai-practitioner/SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
