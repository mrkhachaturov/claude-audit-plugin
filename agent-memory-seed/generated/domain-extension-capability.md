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
- **How do I manage subagents interactively?** Use `/agents` to create, edit, and manage available subagents
- **How do I force a specific subagent?** Use an `@` mention (for example `@\"code-reviewer (agent)\"`) for a single task
- **How do I run the whole session as a subagent?** Start with `claude --agent <name>` or set `agent` in `.claude/settings.json` (CLI flag wins)
- **Subagent frontmatter fields:** include `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `initialPrompt`, `memory`, `background`, and `isolation` (plugin agents only support `isolation: "worktree"`)
- **Subagent model resolution order:** `CLAUDE_CODE_SUBAGENT_MODEL` env var, then per-invocation `model`, then subagent frontmatter `model`, then the main conversation model
- **Subagent tool restriction precedence:** when both `disallowedTools` and `tools` are set, deny rules apply first, then the allowlist is resolved from remaining tools
- **Subagent `permissionMode` under parent auto mode:** parent `auto` takes precedence; subagent frontmatter `permissionMode` is ignored and tool calls are checked by the same classifier rules
- **CLI subagent JSON parity:** `--agents` accepts the same frontmatter keys as file-based subagents, including `initialPrompt`, `effort`, `background`, and `isolation`
- **How do I resume a subagent?** Claude sends `SendMessage` to the prior agent ID; stopped agents auto-resume in background on message
- **Subagent memory scope default:** prefer `project` for team-shared repo-specific knowledge; use `user` for cross-project knowledge and `local` for non-committed project memory
- **What is MCP?** Model Context Protocol — lets Claude connect to external servers that expose tools/resources
- **Non-OAuth MCP auth:** for HTTP servers, set `headersHelper` to a shell command that prints JSON headers; it runs at connection time and overrides same-name static headers
- **What is MCP elicitation?** A structured input request from an MCP server; Claude shows a form/URL dialog and can be auto-handled by hooks
- **MCP OAuth discovery:** Claude supports both Dynamic Client Registration and CIMD (Client ID Metadata Document); use pre-configured credentials when automatic discovery fails.
- **What are MCP channels?** MCP servers with the `claude/channel` capability can push external events into your session when you start Claude with `--channels`
- **Which built-in channel plugins exist in preview?** Telegram, Discord, iMessage, and fakechat
- **Can channels relay tool approvals?** Yes. Two-way channels can opt in with `claude/channel/permission` and relay permission prompts (`allow`/`deny`) using request IDs.
- **iMessage channel access model:** self-messages are auto-allowed; other senders are added by handle (for example `/imessage:access allow +15551234567`)
- **Channels policy gate:** channels require claude.ai auth; Team/Enterprise orgs are disabled by default until managed `channelsEnabled` is true, while Pro/Max users without an org are unaffected
- **Channels allowlist override:** Team/Enterprise admins can set `allowedChannelPlugins` to replace the default Anthropic allowlist; if unset, Anthropic defaults apply
- **Remote approvals race behavior:** terminal prompt and relayed channel prompt stay live in parallel; Claude applies whichever verdict arrives first.
- **What is a plugin?** A packaged collection of skills, agents, and hooks distributed via a registry
- **Plugin install says not found in any marketplace:** update marketplace metadata with `/plugin marketplace update claude-plugins-official`, or add it first with `/plugin marketplace add anthropics/claude-plugins-official`, then retry
- **Plugin configure command missing after install:** run `/reload-plugins` to activate newly installed plugin commands
- **Where can I browse official plugins?** `/plugin` Discover tab or https://claude.com/plugins
- **Plugin file paths:** `${CLAUDE_PLUGIN_ROOT}` points at the current installed plugin directory; `${CLAUDE_PLUGIN_DATA}` is persistent across plugin updates
- **Plugin source types:** plugin entries can be declared inline with `source: \"settings\"` in settings.json
- **Plugin `userConfig`:** plugins can prompt for user-entered options at enable time; sensitive values go to keychain/credentials storage and non-sensitive values go in settings
- **Plugin `channels` declarations:** plugins can declare channel bindings to plugin-provided MCP servers and collect channel-specific `userConfig`
- **Plugin marketplace source note:** `url` plugin sources support git URLs with optional `.git` suffix
- **Plugin seed directories:** `CLAUDE_CODE_PLUGIN_SEED_DIR` can layer multiple paths (`:` on Unix, `;` on Windows); first seed containing a marketplace/cache entry wins
- **Plugin subagent caveat:** plugin-provided agents ignore `hooks`, `mcpServers`, and `permissionMode`; copy to project/user agents if those are required
- **Effort precedence:** skill/subagent `effort` overrides the session level while active, but not `CLAUDE_CODE_EFFORT_LEVEL`
- **Skill location:** `.claude/skills/<name>/SKILL.md` (project) or `~/.claude/skills/` (personal)

## Fast comparisons
- **Skill vs CLAUDE.md:** Skill is on-demand; CLAUDE.md is always loaded
- **Skill vs subagent:** Skill provides instructions; subagent is an isolated Claude instance with its own context
- **Subagent vs agent team:** Subagent returns a summary; agent teams maintain independent sessions
- **MCP vs plugin:** MCP connects to external services; plugin packages internal Claude Code primitives
- **Channels vs Remote Control vs web sessions:** Channels push external events into your current local session; Remote Control steers that same session from another device; web sessions run work in a fresh cloud sandbox
- **Plugin vs skill:** Plugin is a distributable bundle; skill is a single reusable workflow file

## Common tasks
- "Teach Claude our API conventions" → write a skill
- "Run deployment without polluting context" → dispatch a subagent
- "Force one task through a specific subagent" → `@`-mention that subagent in the prompt
- "Run every turn with one subagent persona/tools/model" → `claude --agent <name>` or `agent` setting
- "Background subagent hit a permissions wall" → launch a new foreground subagent with the same task
- "Connect Claude to Jira/Notion/GitHub" → add an MCP server
- "Use short-lived/custom auth for an HTTP MCP server" → configure `headersHelper` in `.mcp.json`
- "React to CI alerts, webhooks, or chat messages in-session" → enable channels (`--channels`) for a channel-capable MCP server
- "Handle MCP mid-task auth/input requests" → use built-in elicitation dialog, optionally automate with hooks
- "Share our hooks and skills with teammates" → package as a plugin
- "Prompt users for API keys/endpoints when enabling a plugin" → plugin `userConfig`
- "Persist plugin-installed dependencies across updates" → install into `${CLAUDE_PLUGIN_DATA}` and keep scripts in `${CLAUDE_PLUGIN_ROOT}`
- "Need per-subagent hooks/MCP/permission mode from a plugin agent" → move that agent into `.claude/agents/` or `~/.claude/agents/`
- "Preload plugins in container/CI images from multiple mounts" → set `CLAUDE_CODE_PLUGIN_SEED_DIR` to a `:`/`;` separated list; order controls precedence
- "Invoke a workflow manually" → make it a user-invocable skill

## When you must read source docs
- Exact SKILL.md frontmatter fields (name, description, tools, memory)
- Subagent tool and memory configuration
- Exact explicit-invocation syntax (`@` mentions, `--agent`, and `agent` setting behavior)
- Full subagent frontmatter field details (`effort`, `background`, `isolation`)
- Parent-mode precedence rules for subagent `permissionMode` (including `auto` and `bypassPermissions`)
- Plugin subagent frontmatter limitations (`hooks`, `mcpServers`, `permissionMode`)
- Full plugin-agent frontmatter support (`model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, `isolation`)
- Plugin persistent data directory lifecycle and uninstall behavior
- Plugin `userConfig` schema and `${user_config.KEY}` substitution rules
- Plugin `channels` field schema and server binding requirements
- MCP transport options (stdio, SSE, HTTP) and auth setup
- `headersHelper` behavior (stdout JSON object format, 10-second shell timeout, trust-gated execution, and static-header override semantics)
- MCP channels capabilities (`claude/channel`, optional `claude/channel/permission`) and `--channels` startup behavior
- Channels notification payload/reply-tool contract, sender allowlist gating, and permission relay request/response schema
- Plugin manifest format and namespace rules
- Agent team coordination patterns

## Source map
- skills.md
- sub-agents.md
- settings.md
- agent-teams.md
- mcp.md
- channels.md
- channels-reference.md
- plugins.md
- plugins-reference.md
- plugin-marketplaces.md
- discover-plugins.md
- features-overview.md
