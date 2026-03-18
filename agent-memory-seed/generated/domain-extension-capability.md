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
- For plugin subagents, avoid relying on `hooks`, `mcpServers`, or `permissionMode` frontmatter (ignored in plugin scope)

## Fast answers
- **What is a skill?** A `SKILL.md` file that defines a reusable workflow; invoked by user or Claude
- **What is a subagent?** A Claude instance dispatched via the Agent tool with its own context and tools
- **How do I force a specific subagent?** Use an `@` mention (for example `@\"code-reviewer (agent)\"`) for a single task
- **How do I run the whole session as a subagent?** Start with `claude --agent <name>` or set `agent` in `.claude/settings.json` (CLI flag wins)
- **How do I resume a subagent?** Claude sends `SendMessage` to the prior agent ID; stopped agents auto-resume in background on message
- **What is MCP?** Model Context Protocol — lets Claude connect to external servers that expose tools/resources
- **What is MCP elicitation?** A structured input request from an MCP server; Claude shows a form/URL dialog and can be auto-handled by hooks
- **What is a plugin?** A packaged collection of skills, agents, and hooks distributed via a registry
- **Plugin file paths:** `${CLAUDE_PLUGIN_ROOT}` points at the current installed plugin directory; `${CLAUDE_PLUGIN_DATA}` is persistent across plugin updates
- **Plugin marketplace source note:** `url` plugin sources support git URLs with optional `.git` suffix
- **Plugin subagent caveat:** plugin-provided agents ignore `hooks`, `mcpServers`, and `permissionMode`; copy to project/user agents if those are required
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
- "Force one task through a specific subagent" → `@`-mention that subagent in the prompt
- "Run every turn with one subagent persona/tools/model" → `claude --agent <name>` or `agent` setting
- "Background subagent hit a permissions wall" → launch a new foreground subagent with the same task
- "Connect Claude to Jira/Notion/GitHub" → add an MCP server
- "Handle MCP mid-task auth/input requests" → use built-in elicitation dialog, optionally automate with hooks
- "Share our hooks and skills with teammates" → package as a plugin
- "Persist plugin-installed dependencies across updates" → install into `${CLAUDE_PLUGIN_DATA}` and keep scripts in `${CLAUDE_PLUGIN_ROOT}`
- "Need per-subagent hooks/MCP/permission mode from a plugin agent" → move that agent into `.claude/agents/` or `~/.claude/agents/`
- "Invoke a workflow manually" → make it a user-invocable skill

## When you must read source docs
- Exact SKILL.md frontmatter fields (name, description, tools, memory)
- Subagent tool and memory configuration
- Exact explicit-invocation syntax (`@` mentions, `--agent`, and `agent` setting behavior)
- Plugin subagent frontmatter limitations (`hooks`, `mcpServers`, `permissionMode`)
- Plugin persistent data directory lifecycle and uninstall behavior
- MCP transport options (stdio, SSE, HTTP) and auth setup
- Plugin manifest format and namespace rules
- Agent team coordination patterns

## Source map
- skills.md
- sub-agents.md
- settings.md
- agent-teams.md
- mcp.md
- plugins.md
- plugins-reference.md
- plugin-marketplaces.md
- discover-plugins.md
- features-overview.md
