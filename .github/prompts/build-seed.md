# Codex Rebuild Prompt: Knowledge Seed

You are Codex. Your task is to rebuild the affected portions of the Claude Code knowledge seed based on changes to source documentation.

You are running inside the repository workspace with write access. Read the files you need directly from disk and edit the affected files in place. Do not rely on any caller-injected context beyond what is written in this prompt.

---

## Files To Read

Read these files directly from the workspace before editing anything:

- `agent-memory-seed/generated/seed_manifest.json`
- `agent-memory-seed/generated/navigation.md`
- Any `agent-memory-seed/generated/domain-*.md` files affected by the changed docs
- Changed source docs under `docs/`

Use git to inspect the current change set:

- `git diff HEAD~1 -U0 -- docs/`

From that diff and the manifest, determine:

- which docs changed
- which headings changed
- which routes are affected
- which generated outputs need updating

---

## 6-Domain Taxonomy

| Domain ID | File | Boundary |
|---|---|---|
| `foundation` | `domain-foundation.md` | How Claude Code works: agentic loop, tools, environments, providers (Bedrock, Vertex, Foundry), authentication, data usage, legal, zero-data-retention |
| `configuration-persistence` | `domain-configuration-persistence.md` | Storing instructions and settings across sessions: CLAUDE.md, memory, settings, env vars, server-managed settings |
| `automation-control` | `domain-automation-control.md` | Deterministic automation: hooks (all event types), scheduled tasks |
| `extension-capability` | `domain-extension-capability.md` | Extending Claude Code: skills, subagents, agent teams, MCP, plugins, plugin marketplaces |
| `access-control-safety` | `domain-access-control-safety.md` | What Claude can access and do: permissions, sandboxing, security, network config, LLM gateway |
| `effective-interaction` | `domain-effective-interaction.md` | Working well with Claude Code: best practices, common workflows, commands, output styles, keybindings, IDE integrations, remote control, headless, checkpointing, fast mode, model config, costs, monitoring |

---

## Hard Execution Constraints

- **Only rebuild affected files** — do not regenerate domain files whose content is unchanged by the doc edits.
- **Never touch `agent-notes/`** — do not read, write, or output anything under `agent-memory-seed/agent-notes/`.
- **Preserve all existing `route_id` values** — do not rename, merge, or delete any route IDs. A changed route ID is treated as a deletion plus an addition and will fail validation.
- **`route_id` stability rule** — if a concept has changed, update the `intent`, `match`, `strong_terms`, `avoid`, `answer_from_domain_if`, `read_source_docs_if`, `primary_doc`, or `secondary_doc` fields as needed, but keep the `route_id` identical to what it was.
- **Update `seed_manifest.json`** for every run:
  - Set `seed_version` to the current ISO-8601 timestamp (e.g. `2026-03-14T12:00:00Z`).
  - Update `file_hash`, `headings_hash`, `headings`, and per-section hashes for every changed source doc.
  - Update `outputs` content hashes for every domain file you rebuild.

---

## What NOT to Do

- Do not modify files outside:
  - `agent-memory-seed/generated/`
- Do not touch `agent-notes/` in any way.
- Do not rename existing `route_id` values.
- Do not regenerate unaffected domain files.

---

## Route Shape Reminder

Each route entry in `navigation.md` must follow this format exactly:

```
### route_id: configure-hooks
domain_id: automation-control
domain_file: domain-automation-control.md
intent: run code deterministically on tool events
match:
  - "how do hooks work"
strong_terms: [hook, PostToolUse, PreToolUse]
avoid: [scheduled tasks, cron, skills]
answer_from_domain_if:
  - conceptual question
  - overview
read_source_docs_if:
  - exact matcher syntax
primary_doc: hooks.md
secondary_doc: hooks-guide.md
```

---

## Domain File Structure Reminder

Every domain file must use this top-level section structure:

```
# Domain: <Name>
## What this domain covers
## Decision rules
## Fast answers
## Fast comparisons
## Common tasks
## When you must read source docs
## Source map
```

Do not add, remove, or reorder these sections. Content within sections may be updated freely.

## Working Method

1. Read `agent-memory-seed/generated/seed_manifest.json`.
2. Run `git diff HEAD~1 -U0 -- docs/` and identify changed docs and heading changes.
3. Read only the changed source docs plus the generated files whose dependencies overlap those changes.
4. Edit the affected files in place.
5. Keep edits minimal and deterministic so `scripts/validate_seed.py` can validate them.
