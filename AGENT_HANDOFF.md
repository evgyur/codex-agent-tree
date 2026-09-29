# Maintainer handoff

- Read `SKILL.md` first. The reference in `references/lean-sol-tree.md` explains the included example.
- The example under `examples/lean-sol-tree/` is synthetic. Never replace a user's complete `config.toml` with it.
- Run `python -m unittest discover -s tests -v`, `python scripts/public_hygiene.py`, and `python scripts/validate_tree.py --codex-home examples/lean-sol-tree/codex-home --project examples/lean-sol-tree/project` before publishing.
- Confirm a public fresh clone and the CI run for the published commit. A successful file validator does not prove a custom agent actually spawned with its selected model.
- Do not add live configuration, credentials, personal paths, private chat text, session logs, or screenshots from signed-in clients to this repository.
