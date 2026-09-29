#!/usr/bin/env python3
"""Scan publishable files for common credentials and private workspace traces."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BS = chr(92)
TOKEN_PREFIXES = ("sk" + "-", "ghp" + "_", "github" + "_pat" + "_")
HOME_PREFIXES = ("C:" + BS + "Users" + BS, "/" + "home" + "/", "/" + "Users" + "/")
FORBIDDEN_NAMES = {"auth.json", ".env", "credentials.json"}


def scan_text(content: str) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    for number, line in enumerate(content.splitlines(), 1):
        if any(re.search(re.escape(prefix) + r"[A-Za-z0-9_-]{20,}", line) for prefix in TOKEN_PREFIXES):
            findings.append((number, "credential-format"))
        if re.search(r"(?i)bearer\s+[A-Za-z0-9._-]{20,}", line):
            findings.append((number, "bearer-credential"))
        if re.search(r"(?i)(api_key|access_token|password|secret)\s*[:=]\s*['\"][^'\"]{12,}['\"]", line):
            findings.append((number, "secret-assignment"))
        if re.search(r"(?i)\b[A-Z][A-Z0-9_]*(?:API_KEY|ACCESS_KEY|TOKEN|SECRET|PASSWORD|CREDENTIALS?)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}", line):
            findings.append((number, "environment-credential"))
        if re.search(r"[a-z][a-z0-9+.-]*://[^\s/@:]+:[^\s/@]+@[^\s/]+", line, re.I):
            findings.append((number, "credentialed-url"))
        if any(re.search(re.escape(prefix) + r"[A-Za-z0-9._-]+", line) for prefix in HOME_PREFIXES):
            findings.append((number, "private-home-path"))
        if line.startswith(("<<<<<<< ", "=======", ">>>>>>> ")):
            findings.append((number, "conflict-marker"))
    return findings


def publishable_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return sorted(ROOT / Path(raw.decode("utf-8")) for raw in result.stdout.split(b"\0") if raw)
    return sorted(path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)


def scan_repo() -> list[str]:
    findings: list[str] = []
    for path in publishable_files():
        relative = path.relative_to(ROOT)
        if path.name in FORBIDDEN_NAMES or path.suffix in {".sqlite", ".db", ".key", ".pem"}:
            findings.append(f"{relative}:0:forbidden-file-type")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeError:
            findings.append(f"{relative}:0:non-text-file")
            continue
        for number, rule in scan_text(content):
            findings.append(f"{relative}:{number}:{rule}")
    return findings


def main() -> int:
    findings = scan_repo()
    if findings:
        print("\n".join(findings), file=sys.stderr)
        return 1
    print(f"PASS: scanned {len(publishable_files())} publishable files; no credential or private-path markers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
