#!/usr/bin/env python3
"""Read-only checks for the lean Codex agent tree."""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path


def load_toml(path: Path, failures: list[str], label: str) -> dict:
    if not path.is_file():
        failures.append(f"{label}: missing file")
        return {}
    try:
        with path.open("rb") as stream:
            return tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError):
        failures.append(f"{label}: invalid TOML")
        return {}


def check_equal(data: dict, key: str, expected: object, failures: list[str], label: str) -> None:
    if data.get(key) != expected:
        failures.append(f"{label}: {key} differs from expected profile")


def validate(args: argparse.Namespace) -> list[str]:
    failures: list[str] = []
    config = load_toml(args.codex_home / "config.toml", failures, "main config")
    check_equal(config, "model", args.main_model, failures, "main config")
    check_equal(config, "model_reasoning_effort", args.main_effort, failures, "main config")

    defaults = config.get("agents", {})
    if not isinstance(defaults, dict):
        failures.append("main config: agents must be a table")
        defaults = {}
    check_equal(defaults, "enabled", True, failures, "agent defaults")
    check_equal(defaults, "max_concurrent_threads_per_session", args.max_subagents, failures, "agent defaults")
    check_equal(defaults, "default_subagent_model", args.agent_model, failures, "agent defaults")
    check_equal(defaults, "default_subagent_reasoning_effort", args.agent_effort, failures, "agent defaults")

    names = ("explorer", "worker", "researcher")
    if not args.no_reviewer:
        names += ("reviewer",)
    for name in names:
        role = load_toml(args.project / ".codex" / "agents" / f"{name}.toml", failures, name)
        model = args.reviewer_model if name == "reviewer" else args.agent_model
        effort = args.reviewer_effort if name == "reviewer" else args.agent_effort
        check_equal(role, "name", name, failures, name)
        check_equal(role, "model", model, failures, name)
        check_equal(role, "model_reasoning_effort", effort, failures, name)
        if not isinstance(role.get("description"), str) or not role["description"].strip():
            failures.append(f"{name}: missing description")
        if not isinstance(role.get("developer_instructions"), str) or not role["developer_instructions"].strip():
            failures.append(f"{name}: missing developer instructions")
        if name in ("explorer", "researcher", "reviewer"):
            check_equal(role, "sandbox_mode", "read-only", failures, name)

    policy = args.project / "AGENTS.md"
    if not policy.is_file():
        failures.append("project policy: missing AGENTS.md")
    else:
        text = policy.read_text(encoding="utf-8", errors="replace").lower()
        if not all(term in text for term in ("fork_turns", '"none"', '"all"')):
            failures.append("project policy: missing bounded fork_turns rule")
        if "simple tasks directly" not in text:
            failures.append("project policy: missing simple-task direct handling rule")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", required=True, type=Path)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--main-model", default="gpt-6.1-sol")
    parser.add_argument("--main-effort", default="high")
    parser.add_argument("--agent-model", default="gpt-6.1-sol")
    parser.add_argument("--agent-effort", default="medium")
    parser.add_argument("--reviewer-model", default="gpt-6-astra")
    parser.add_argument("--reviewer-effort", default="xhigh")
    parser.add_argument("--no-reviewer", action="store_true", help="Validate a three-role tree without an optional reviewer")
    parser.add_argument("--max-subagents", default=3, type=int)
    args = parser.parse_args()
    failures = validate(args)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("PASS: configured lean agent tree matches the requested profile")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
