# Changelog

All notable changes to `claude-audit` are documented here.

---

## [1.1.0] — 2026-03-12

### Added
- `agents/automation-analyst-refs/` — 5 reference files ported from `claude-code-setup`: `mcp-servers.md`, `hooks-patterns.md`, `subagent-templates.md`, `skills-reference.md`, `plugins-reference.md`

### Changed
- `agents/automation-analyst.md`: add `memory: user`, bootstrap from reference files via `installed_plugins.json` (mirrors `claude-code-expert`); add `projects.md` accumulation after each audit; enriched fallback tables (LSP plugins, notification hooks, model selection for subagents)

---

## [1.0.5] — 2026-03-12

### Added
- `agents/automation-analyst.md` — self-contained automation gap analyzer with all lookup tables inline (MCP servers, hooks, subagents, skills, plugins). No external plugin dependencies.

### Changed
- `skills/audit-project/SKILL.md`:
  - Steps 1 & 2 now run **in parallel** (two Agent dispatches in one message)
  - Step 2 dispatches `automation-analyst` agent instead of `claude-code-setup:claude-automation-recommender` skill
  - Step 3 writes full report to `.claude/specs/YYYY-MM-DD-ai-readiness-audit.md` inside the audited project; terminal shows brief summary only
  - Step 4 offers to invoke `superpowers:writing-plans` using the saved spec file as requirements
  - Added Quick Wins and Long-term Improvements sections to report template

### Removed
- Prerequisite check for `claude-code-setup` plugin — `claude-audit` is now fully self-contained

---

## [1.0.4] — 2026-03-11

### Fixed
- Step 2: corrected to use Skill tool directly (skill cannot be dispatched as subagent)
- Prerequisite check: now verifies `SKILL.md` presence, not just directory
- Report template: enriched with more structured sections
- Added Step 4 next steps prompt

---

## [1.0.3] — 2026-03-11

### Fixed
- `agents/claude-code-expert.md`: corrected remaining old memory path in Constraint section

---

## [1.0.2] — 2026-03-11

### Fixed
- `agents/claude-code-expert.md`: corrected agent memory path to `~/.claude/agent-memory/claude-audit-claude-code-expert/`

---

## [1.0.1] — 2026-03-11

### Fixed
- Bootstrap: resolve docs path via `installed_plugins.json` instead of glob wildcard

---

## [1.0.0] — 2026-03-11

### Added
- Initial release
- `skills/audit-project/SKILL.md` — AI-readiness audit skill
- `agents/claude-code-expert.md` — Claude Code expertise subagent with cross-session memory
- `docs/` — 60 Claude Code docs, auto-updated every 3h via GitHub Actions
- `scripts/fetch_claude_docs.py` — docs sync script
