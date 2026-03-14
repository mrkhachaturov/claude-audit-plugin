---
globs: agents/*.md
---

Agent files use YAML frontmatter with these fields: name, description, tools, memory.

Both agents are read-only on target projects — they may only write to their own memory directories under `~/.claude/agent-memory/`. This constraint is enforced by natural language in the agent body.

Reference files for automation-analyst live in `agents/automation-analyst-refs/` and are the source of truth for lookup tables. Never duplicate their content inline in the agent body.
