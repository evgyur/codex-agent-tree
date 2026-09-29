from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import public_hygiene  # noqa: E402


class PublicHygieneTests(unittest.TestCase):
    def test_repository_is_clean(self) -> None:
        self.assertEqual(public_hygiene.scan_repo(), [])

    def test_secret_and_private_path_are_caught(self) -> None:
        secret = "sk" + "-" + ("A" * 24)
        path = "C:" + chr(92) + "Users" + chr(92) + "person" + chr(92) + "file"
        rules = {rule for _, rule in public_hygiene.scan_text(secret + "\n" + path)}
        self.assertIn("credential-format", rules)
        self.assertIn("private-home-path", rules)

    def test_unquoted_env_secret_and_credentialed_url_are_caught(self) -> None:
        value = "example" + "value" + ("1" * 20)
        env_line = "OPENAI_API_KEY=" + value
        url_line = "https://user:" + value + "@example.invalid/path"
        rules = {rule for _, rule in public_hygiene.scan_text(env_line + "\n" + url_line)}
        self.assertIn("environment-credential", rules)
        self.assertIn("credentialed-url", rules)


if __name__ == "__main__":
    unittest.main()
