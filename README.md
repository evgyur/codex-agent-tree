# Codex agent tree

A Codex skill for setting up and verifying a small, role-based agent tree. It turns a requested model diagram into root defaults, project custom agents, a delegation rule, and runtime checks. The bundled example uses GPT-6.1 Sol for the main session and three working roles, with an optional Astra reviewer.

## Install

Clone this whole repository into your Codex skills directory:

```text
git clone https://github.com/evgyur/codex-agent-tree.git ~/.codex/skills/codex-agent-tree
```

On Windows, clone into `%USERPROFILE%\.codex\skills\codex-agent-tree`. Keep the full directory: `SKILL.md` links to its reference and validator. Start a new Codex session, then ask: `Use $codex-agent-tree to set up my project agents from this tree.`

## Use

The skill inspects current settings, checks model availability in the target client, preserves unrelated configuration, and verifies both TOML and an actual child session. The [example tree](examples/lean-sol-tree/) is sanitized and can be validated locally:

```text
python scripts/validate_tree.py --codex-home examples/lean-sol-tree/codex-home --project examples/lean-sol-tree/project
```

The examples are fragments for adaptation. Do not overwrite your existing `config.toml` with the sample. Model availability and supported reasoning efforts depend on the account and client; check [OpenAI's model guide](https://learn.chatgpt.com/docs/models) before applying a profile.

## Development checks

```text
python -m unittest discover -s tests -v
python scripts/public_hygiene.py
```

See [AGENT_HANDOFF.md](AGENT_HANDOFF.md) for the file map and publication checks. This repository contains no live user configuration, credentials, or session logs.
