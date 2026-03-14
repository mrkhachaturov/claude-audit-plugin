# claude-audit-plugin

Claude Code plugin that audits projects for AI-readiness. Provides two agents (`claude-code-expert`, `automation-analyst`) and two skills (`audit-project`, `ask`).

## Directory Layout

    agents/                     # Agent definitions (frontmatter + body)
      automation-analyst-refs/  # Reference lookup tables for automation-analyst bootstrap
    agent-memory-seed/
      generated/                # CI-generated seed files — NEVER edit by hand
      agent-notes/              # Agent-written notes (not overwritten by CI)
    skills/                     # User-invocable skills (audit-project, ask)
    scripts/                    # Python build pipeline (slugify, validate, bump, etc.)
    tests/                      # pytest tests for scripts/
    docs/                       # Claude Code documentation (fetched by CI)
    .claude-plugin/             # Plugin manifest (plugin.json)
    .github/                    # CI workflows (update-docs.yml)

## Development

```bash
# Run tests
python -m pytest tests/ -x -q

# Run a specific test
python -m pytest tests/test_slugify.py -v
```

## Key Conventions

- Files in `agent-memory-seed/generated/` are produced by the CI pipeline (`update-docs.yml`). Never edit them by hand.
- The `slugify` function in `scripts/slugify.py` defines the heading-to-ID contract used by seed validation. All section IDs must match its output.
- Both agents are **read-only on target projects**. They may only write to their own memory directories under `~/.claude/agent-memory/`.
- Agent reference files in `agents/automation-analyst-refs/` are the source of truth for automation lookup tables.

## Superpowers Overrides

Plans: `.artifacts/plans/YYYY-MM-DD-<feature-name>.md`

Specs: `.artifacts/specs/YYYY-MM-DD-<topic>-design.md`
