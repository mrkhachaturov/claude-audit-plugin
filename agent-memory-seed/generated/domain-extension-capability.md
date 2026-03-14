# Domain: Extension & Capability

## What this domain covers
Extending Claude Code beyond the base agentic loop: skills (reusable workflows), subagents (isolated workers), agent teams (coordinating sessions), MCP servers (external tool integrations), and plugins (packaged distributions of the above).

## Decision rules
- Use `CLAUDE.md` for always-on project rules that Claude should always follow
- Use `skills` for reusable workflows or knowledge loaded on demand
- Use `subagents` for isolated work that shouldn't pollute the main context
- Use `agent teams` when multiple workers need to coordinate with shared state
- Use `MCP` to connect Claude to external tools, APIs, or data sources
- Use `plugins` to package and distribute skills/agents/hooks across projects

## Fast answers
- **What is a skill?** A `SKILL.md` file that defines a reusable workflow; invoked by user or Claude
- **What is a subagent?** A Claude instance dispatched via the Agent tool with its own context and tools
- **What is MCP?** Model Context Protocol — lets Claude connect to external servers that expose tools/resources
- **What is MCP elicitation?** A structured input request from an MCP server; Claude shows a form/URL dialog and can be auto-handled by hooks
- **What is a plugin?** A packaged collection of skills, agents, and hooks distributed via a registry
- **Skill location:** `.claude/skills/<name>/SKILL.md` (project) or `~/.claude/skills/` (personal)

## Fast comparisons
- **Skill vs CLAUDE.md:** Skill is on-demand; CLAUDE.md is always loaded
- **Skill vs subagent:** Skill provides instructions; subagent is an isolated Claude instance with its own context
- **Subagent vs agent team:** Subagent returns a summary; agent teams maintain independent sessions
- **MCP vs plugin:** MCP connects to external services; plugin packages internal Claude Code primitives
- **Plugin vs skill:** Plugin is a distributable bundle; skill is a single reusable workflow file

## Common tasks
- "Teach Claude our API conventions" → write a skill
- "Run deployment without polluting context" → dispatch a subagent
- "Connect Claude to Jira/Notion/GitHub" → add an MCP server
- "Handle MCP mid-task auth/input requests" → use built-in elicitation dialog, optionally automate with hooks
- "Share our hooks and skills with teammates" → package as a plugin
- "Invoke a workflow manually" → make it a user-invocable skill

## When you must read source docs
- Exact SKILL.md frontmatter fields (name, description, tools, memory)
- Subagent tool and memory configuration
- MCP transport options (stdio, SSE, HTTP) and auth setup
- Plugin manifest format and namespace rules
- Agent team coordination patterns

## Source map
- skills.md
- sub-agents.md
- agent-teams.md
- mcp.md
- plugins.md
- plugins-reference.md
- plugin-marketplaces.md
- discover-plugins.md
- features-overview.md
