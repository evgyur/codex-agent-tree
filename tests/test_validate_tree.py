from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "lean-sol-tree"
VALIDATOR = ROOT / "scripts" / "validate_tree.py"


class AgentTreeValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.sample = Path(self.temp.name) / "sample"
        shutil.copytree(EXAMPLE, self.sample)

    def run_validator(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--codex-home",
                str(self.sample / "codex-home"),
                "--project",
                str(self.sample / "project"),
                *extra,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_complete_example_passes(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_old_worker_model_fails(self) -> None:
        role = self.sample / "project" / ".codex" / "agents" / "worker.toml"
        role.write_text(role.read_text(encoding="utf-8").replace("gpt-6.1-sol", "gpt-6-sol"), encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("worker: model differs", result.stderr)

    def test_missing_fork_rule_fails(self) -> None:
        policy = self.sample / "project" / "AGENTS.md"
        policy.write_text("# Example\n\nHandle simple tasks directly.\n", encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("bounded fork_turns rule", result.stderr)

    def test_three_role_tree_passes_when_reviewer_is_disabled(self) -> None:
        (self.sample / "project" / ".codex" / "agents" / "reviewer.toml").unlink()
        self.assertNotEqual(self.run_validator().returncode, 0)
        result = self.run_validator("--no-reviewer")
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
