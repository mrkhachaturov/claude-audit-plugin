# Domain: Configuration & Persistence

## What this domain covers
Storing instructions and settings that persist across sessions: CLAUDE.md files (project and personal), auto-memory system, settings.json configuration, environment variables, and server-managed settings for enterprise.

## Decision rules
- Use `CLAUDE.md` for always-on project-level instructions Claude should always follow
- Use `~/.claude/CLAUDE.md` for personal preferences that apply across all projects
- Use auto-memory (`/memory` command) for facts Claude should remember across sessions
- Use `settings.json` for tool permissions, hooks, and session/tool configuration
- Use `~/.claude.json` for global display preferences like turn duration and terminal progress bar
- Use environment variables for secrets and CI/CD configuration

## Fast answers
- **Where does CLAUDE.md live?** Project root or `.claude/CLAUDE.md`; personal at `~/.claude/CLAUDE.md`
- **What goes in CLAUDE.md?** Project conventions, coding style, architecture notes, commands to run
- **What is auto-memory?** Session notes are auto-saved to `~/.claude/MEMORY.md`; use `/memory` to view and edit what was saved
- **`/init` interactive flow:** set `CLAUDE_CODE_NEW_INIT=true` to run a guided setup for `CLAUDE.md`, skills, hooks, and memory files
- **Settings precedence:** enterprise > project > user (higher wins)
- **settings.json location:** `.claude/settings.json` (project) or `~/.claude/settings.json` (user)
- **Global display settings location:** `~/.claude.json` (for example `showTurnDuration`, `terminalProgressBarEnabled`)
- **Enterprise channels control:** managed `channelsEnabled` gates channel message delivery for Team/Enterprise regardless of user `--channels` flags

## Fast comparisons
- **CLAUDE.md vs memory:** CLAUDE.md is manually curated; memory is agent-written via `/memory`
- **CLAUDE.md vs skills:** CLAUDE.md is always loaded; skills are loaded on demand
- **CLAUDE.md vs rules:** Rules are scoped to paths or topics; CLAUDE.md is always-on project-wide
- **Managed settings vs managed CLAUDE.md:** Settings enforce hard technical controls (`permissions`, `sandbox`, `env`, login lock); managed CLAUDE.md provides behavioral guidance
- **Project settings vs user settings:** Project overrides user for the specific project

## Common tasks
- "Tell Claude about my project's coding style" → write it in CLAUDE.md
- "Remember something across sessions" → use `/memory` command
- "Configure which tools Claude can use" → settings.json permissions
- "Set an API key for CI" → env-vars.md
- "Enforce org-wide settings" → server-managed-settings.md

## When you must read source docs
- Exact CLAUDE.md syntax and import system (`@path/to/file`)
- Memory file location and format details
- Full settings.json schema and all available keys
- Enterprise policy enforcement via server-managed-settings

## Source map
- memory.md
- settings.md
- env-vars.md
- server-managed-settings.md
