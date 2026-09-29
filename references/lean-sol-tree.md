# Lean Sol tree example

Use these examples only after verifying that the requested models and efforts are available to the user's account and client. Merge keys into existing files; never replace a live `config.toml` or copy its credentials into a shared repository. The complete sanitized example is under [`examples/lean-sol-tree/`](../examples/lean-sol-tree/).

| Role | Model | Effort | Job |
| --- | --- | --- | --- |
| Main | `gpt-6.1-sol` | `high` | Decompose, integrate, verify |
| explorer | `gpt-6.1-sol` | `medium` | Read-only code investigation |
| worker | `gpt-6.1-sol` | `medium` | Bounded implementation and tests |
| researcher | `gpt-6.1-sol` | `medium` | Read-only source lookup |
| reviewer | `gpt-6-astra` | `xhigh` | Optional independent pre-ship review |

Keep simple tasks in the main session. The `reviewer` is used only before a substantial change ships. A three-child concurrency cap covers explorer, worker, and researcher; ask the reviewer after integration when a slot is free.

To verify a real project without changing it:

```text
python scripts/validate_tree.py --codex-home <codex-home> --project <project-root>
```

For another approved tree, pass `--main-model`, `--main-effort`, `--agent-model`, `--agent-effort`, `--reviewer-model`, and `--reviewer-effort`. Add `--no-reviewer` when the tree has only the three working roles. The validator checks files and policy text; a live spawn is still needed to prove runtime selection.
