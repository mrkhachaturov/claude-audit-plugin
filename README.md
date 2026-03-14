# claude-audit

AI-readiness audit plugin for Claude Code. Analyzes any project's Claude Code setup and produces a structured report with prioritized improvements.

## Install

```
/plugin install claude-audit
```

## Skills

### `/audit-project`

Run from inside the project you want to audit:

```
/audit-project
```

Produces a report covering:

- **Project Profile** — detected stack, secrets management, existing Claude setup
- **What's Already Good** — areas where the project follows best practices
- **Structure Gaps** — missing CLAUDE.md, hooks, rules, etc. with priority ratings
- **Recommended Automations** — MCP servers, hooks, subagents, skills, plugins
- **Priority Actions** — ranked by impact and effort

The report is saved to `.artifacts/specs/YYYY-MM-DD-ai-readiness-audit.md`.

### `/claude-audit:ask <question>`

Ask any question about Claude Code — CLAUDE.md, memory, hooks, skills, agents, plugins, MCP, settings, permissions, or best practices. Answers are backed by official documentation.

```
/claude-audit:ask how do hooks work?
```

## Architecture

- `agents/claude-code-expert.md` — Claude Code expertise subagent with persistent knowledge base
- `agents/automation-analyst.md` — automation gap analyst subagent
- `agents/automation-analyst-refs/` — reference lookup tables for automation recommendations
- `agent-memory-seed/` — pre-built knowledge seed, updated by CI every 3 hours
- `scripts/` — CI build pipeline for knowledge seed (slugify, validation, significance detection)
- `tests/` — pytest tests for build scripts
