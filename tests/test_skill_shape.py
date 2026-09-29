from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SkillShapeTests(unittest.TestCase):
    def test_frontmatter_and_direct_links(self) -> None:
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: codex-agent-tree\n"))
        self.assertRegex(content, r"(?m)^description: .+")
        for relative in re.findall(r"\]\((references/[^)]+|scripts/[^)]+)\)", content):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_required_public_files(self) -> None:
        for name in ("README.md", "LICENSE", ".gitignore", "AGENT_HANDOFF.md", ".github/workflows/ci.yml"):
            self.assertTrue((ROOT / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
