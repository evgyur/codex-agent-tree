# Example project agent policy

- The main agent decomposes work, integrates results, and verifies the final outcome. Handle simple tasks directly; delegate bounded independent work.
- Use `explorer` for code investigation, `worker` for implementation and tests, and `researcher` for documentation lookup. Ask `reviewer` for independent review only before a substantial change ships.
- When selecting a custom role's model or reasoning effort, set `fork_turns` to `"none"` or a small number of recent turns. Omitting it or using `"all"` can inherit the main model and effort instead of the intended role settings.
