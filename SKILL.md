---
name: codex-agent-tree
description: Configures or audits a Codex model-and-subagent tree when a user asks for specific root and role models, reasoning efforts, delegation rules, or proof of what spawned agents actually ran.
---

# Codex agent tree

Turn a requested agent tree into a working Codex configuration. Keep the main agent responsible for decomposition, integration, and final verification. Delegate bounded independent work; handle small tasks directly.

## Inputs and scope

Identify the target project, root model and effort, each role's model and effort, concurrency limit, and whether the user wants a preview before edits. Preserve explicit model choices. If a requested model cannot be selected in the target client or account, stop the dependent configuration change and ask the user; do not silently substitute a model.

Use the current official [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), [subagent guide](https://learn.chatgpt.com/docs/agent-configuration/subagents), and [model guide](https://learn.chatgpt.com/docs/models) for version-sensitive keys and availability. The [lean Sol example](references/lean-sol-tree.md) is a starting pattern, not a permanent claim about model pricing or benchmarks.

## Inspect before editing

1. Read only the model, effort, and `[agents]` settings needed from the user's `config.toml`. Inventory personal and project custom-agent files by parsing TOML. Do not print or copy the full config: it may contain credentials.
2. List roles other than an intended reviewer that still use a model being replaced. Identify `none` or `minimal` effort on roles moving to a model that does not support it; choose a supported effort and compare a representative task.
3. Check applicable `AGENTS.md` files for delegation rules and model claims. If a model exists only in prose, inspect recent subagent session metadata or run a bounded probe to verify the model and effort actually used. A file readback alone does not prove runtime selection.
4. Confirm the requested model and effort are selectable in the actual client and account. For CLI, a small `codex exec --model ... --config model_reasoning_effort=...` probe can establish this. A stale model cache is not proof of availability.

## Apply the smallest change

- Patch only the relevant root settings and `[agents]` defaults. Preserve unrelated configuration and credentials.
- Reuse matching project roles. Create only missing project role files under `.codex/agents/`; set `name`, `description`, `developer_instructions`, `model`, and `model_reasoning_effort` explicitly. Give investigation and review roles read-only intent and configuration when appropriate. Assign one writer per file set.
- Keep the optional reviewer separate from routine work. Invoke it only at the user's requested gate, and have it report findings without edits.
- Add an `AGENTS.md` rule only when the project needs one. When a spawn must use a role's selected model or effort, pass `fork_turns: "none"` or a small recent-turn count. Full-history inheritance can retain the parent's model and effort and prevent a requested override.
- If the user asked to see changes first, show the exact files and assignments and wait for approval before writing. Approval for one project does not authorize changes to unrelated projects or global role files.

## Output Contract

Parse the changed TOML, run the target client's strict config or equivalent startup check, and inspect a bounded spawned-agent session to confirm its role, model, and effort. Run focused tests for any implementation performed by a worker. The read-only [validator](scripts/validate_tree.py) checks the bundled lean profile or a matching local installation; pass explicit model arguments when adapting it.

Report changed paths, a root-and-role assignment table, exact verification results, and limits such as unavailable models or existing sessions that retain old settings. Never claim that a written role was executed unless a runtime trace confirms it.

## Quick Test Checklist

- A clear two-minute task stays with the main agent.
- A missing model blocks that model's configuration instead of triggering a silent fallback.
- A recent child trace shows the custom role and its selected model and effort.
- A preview-first request produces no config edits before approval.

## Done Criteria

The requested files are present, changed TOML parses, the target client accepts the selected model and effort, and a bounded child trace confirms at least one custom role when runtime verification is available. State exactly which roles were file-checked and which were actually spawned. For public publication, finish the privacy scan, fresh-clone check, and CI check on the published commit.
