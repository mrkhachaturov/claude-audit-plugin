# Claude Code Navigation Seed

## How to use
1. Match the user's question to exactly one `route_id` using `intent`, `match` phrases, and `strong_terms`.
2. Read `domain_file` first. Answer from it if `answer_from_domain_if` applies — cite `primary_doc` by name without reading it.
3. Read `primary_doc` from `installPath/docs/` only if `read_source_docs_if` applies. Read `secondary_doc` only if still needed.
4. **Fallback:** If no route matches confidently, use `strong_terms` to pick the best candidate. If still ambiguous, read `primary_doc` for the top 2 candidates. If ambiguity persists, return both answers with explicit uncertainty and cite all docs consulted.

---

### route_id: how-claude-code-works
domain_id: foundation
domain_file: domain-foundation.md
intent: understand how Claude Code operates internally
match:
  - "how does Claude Code work"
  - "what is the agentic loop"
  - "what tools does Claude have"
  - "how does Claude make decisions"
strong_terms: [agentic loop, tool use, context window, agents, how it works]
avoid: [authentication, billing, MCP, hooks]
answer_from_domain_if:
  - conceptual overview
  - what the agentic loop is
  - what tools are available
read_source_docs_if:
  - specific tool behavior details
  - execution environment differences
primary_doc: how-claude-code-works.md
secondary_doc: overview.md

---

### route_id: configure-memory
domain_id: configuration-persistence
domain_file: domain-configuration-persistence.md
intent: understand or configure Claude's memory across sessions
match:
  - "how does memory work"
  - "how do I make Claude remember something"
  - "what goes in MEMORY.md"
  - "difference between CLAUDE.md and memory"
  - "managed CLAUDE.md vs managed settings"
strong_terms: [memory, MEMORY.md, /memory, remember, persist, cross-session]
avoid: [hooks, skills, permissions]
answer_from_domain_if:
  - what memory is and how it works
  - when to use memory vs CLAUDE.md
  - how to save something to memory
read_source_docs_if:
  - exact memory file format
  - memory scopes (user/project/local)
primary_doc: memory.md
secondary_doc: settings.md

---

### route_id: claude-md-structure
domain_id: configuration-persistence
domain_file: domain-configuration-persistence.md
intent: understand or write a CLAUDE.md file
match:
  - "what goes in CLAUDE.md"
  - "how to write CLAUDE.md"
  - "CLAUDE.md structure"
  - "how does Claude read CLAUDE.md"
  - "should this go in CLAUDE.md"
strong_terms: [CLAUDE.md, project instructions, always-on, project context]
avoid: [memory, hooks, skills]
answer_from_domain_if:
  - what CLAUDE.md is for
  - what kinds of content belong in it
  - CLAUDE.md vs memory
read_source_docs_if:
  - import syntax (@path)
  - precedence between project and user CLAUDE.md
primary_doc: memory.md
secondary_doc: settings.md

---

### route_id: configure-hooks
domain_id: automation-control
domain_file: domain-automation-control.md
intent: run code automatically at tool lifecycle events
match:
  - "how do hooks work"
  - "run a command after Claude edits a file"
  - "block a dangerous command"
  - "auto-format on save"
  - "auto-approve permission prompts"
  - "PostToolUse hook"
  - "notification hook"
  - "Elicitation hook"
  - "PostCompact hook"
strong_terms: [hook, PostToolUse, PreToolUse, PermissionRequest, ExitPlanMode, Notification, Stop, StopFailure, Elicitation, ElicitationResult, PostCompact, matcher, blocking]
avoid: [scheduled tasks, cron, skills]
answer_from_domain_if:
  - what hooks are
  - when to use hooks vs other primitives
  - hooks vs skills or CLAUDE.md
read_source_docs_if:
  - exact matcher syntax
  - Stop vs StopFailure behavior and payloads
  - blocking semantics and exit codes
  - PermissionRequest decision schema and updatedPermissions entries
  - matcher support on InstructionsLoaded/Elicitation/ElicitationResult events
  - plugin path variables (`CLAUDE_PLUGIN_ROOT` vs `CLAUDE_PLUGIN_DATA`)
  - specific hook event payload format
primary_doc: hooks.md
secondary_doc: hooks-guide.md

---

### route_id: hooks-vs-skills
domain_id: automation-control
domain_file: domain-automation-control.md
intent: decide between hooks and skills for a given use case
match:
  - "hooks vs skills"
  - "should I use a hook or a skill"
  - "difference between hooks and skills"
strong_terms: [hook, skill, automatic, on-demand, deterministic]
avoid: [MCP, agents, plugins]
answer_from_domain_if:
  - conceptual comparison
  - when to choose one over the other
read_source_docs_if:
  - implementation details of either
primary_doc: hooks.md
secondary_doc: skills.md

---

### route_id: configure-skills
domain_id: extension-capability
domain_file: domain-extension-capability.md
intent: create or configure a reusable skill
match:
  - "how do I create a skill"
  - "what is a skill"
  - "SKILL.md format"
  - "user-invocable skill"
  - "how to write a skill"
strong_terms: [skill, SKILL.md, slash command, reusable, on-demand, user-invocable]
avoid: [CLAUDE.md, hooks, agents, MCP]
answer_from_domain_if:
  - what a skill is
  - skill vs CLAUDE.md
  - when to use a skill
read_source_docs_if:
  - exact SKILL.md frontmatter fields
  - `effort` frontmatter options and precedence
  - skill scoping (project vs personal vs plugin)
  - how skills load into context
primary_doc: skills.md
secondary_doc: null

---

### route_id: skills-vs-claudemd
domain_id: extension-capability
domain_file: domain-extension-capability.md
intent: decide whether content belongs in CLAUDE.md or a skill
match:
  - "should this go in CLAUDE.md or a skill"
  - "when do I use a skill vs CLAUDE.md"
  - "difference between CLAUDE.md and skills"
strong_terms: [CLAUDE.md, skill, always-on, on-demand, reusable]
avoid: [hooks, agents, MCP]
answer_from_domain_if:
  - conceptual comparison
  - decision rule for always-on vs on-demand
read_source_docs_if:
  - frontmatter or precedence details
primary_doc: features-overview.md
secondary_doc: skills.md

---

### route_id: configure-agents
domain_id: extension-capability
domain_file: domain-extension-capability.md
intent: create, configure, or explicitly invoke a subagent
match:
  - "how do I create a subagent"
  - "how do I use /agents"
  - "what is a subagent"
  - "agent frontmatter"
  - "dispatch a subagent"
  - "resume a subagent"
  - "how do I @mention a subagent"
  - "run session with --agent"
  - "agent setting in settings.json"
  - "agent memory"
  - "plugin subagent fields are ignored"
strong_terms: [subagent, agent, Agent tool, SendMessage, dispatch, resume, @agent, --agent, agent setting, isolated context, agent memory]
avoid: [MCP, plugins, hooks]
answer_from_domain_if:
  - what a subagent is
  - subagent vs skill
  - natural language vs @-mention vs session-wide agent selection
  - when to use subagents
read_source_docs_if:
  - exact agent frontmatter fields
  - explicit invocation syntax (`@` mention forms)
  - session-wide agent config (`--agent` and `agent` setting precedence)
  - plugin subagent field limitations
  - tool and memory configuration (including recommended `project` memory scope)
  - `tools` vs `disallowedTools` precedence when both are set
  - resume behavior details (SendMessage, background auto-resume)
  - agent isolation guarantees
primary_doc: sub-agents.md
secondary_doc: settings.md

---

### route_id: configure-mcp
domain_id: extension-capability
domain_file: domain-extension-capability.md
intent: connect Claude Code to an external tool via MCP
match:
  - "how do I add an MCP server"
  - "connect Claude to Notion"
  - "connect Claude to Jira"
  - "stdio vs SSE"
  - "MCP configuration"
  - "MCP elicitation"
  - "MCP channels"
  - "channels vs remote control"
  - "how do I use --channels"
strong_terms: [MCP, stdio, SSE, http, mcp server, claude mcp add, external tool, elicitation, channel, --channels]
avoid: [plugins, hooks, skills]
answer_from_domain_if:
  - what MCP is
  - MCP vs plugins
  - when to use MCP
read_source_docs_if:
  - exact mcp add command syntax
  - transport type selection
  - OAuth and auth configuration
  - channel capability (`claude/channel`) and startup flags (`--channels`)
  - channels vs web sessions/slack/remote-control behavior differences
  - plugin MCP path variables (`CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA`)
primary_doc: mcp.md
secondary_doc: settings.md

---

### route_id: configure-plugins
domain_id: extension-capability
domain_file: domain-extension-capability.md
intent: install, create, or publish a plugin
match:
  - "how do I install a plugin"
  - "how do I create a plugin"
  - "plugin not found in any marketplace"
  - "plugin manifest"
  - "plugin.json"
  - "what is CLAUDE_PLUGIN_DATA"
  - "share skills across projects"
strong_terms: [plugin, plugin.json, marketplace, install plugin, publish plugin, CLAUDE_PLUGIN_ROOT, CLAUDE_PLUGIN_DATA]
avoid: [MCP, skills as standalone, hooks standalone]
answer_from_domain_if:
  - what a plugin is
  - plugin vs skill or MCP
  - how to install a plugin
  - plugin root path vs persistent data path
read_source_docs_if:
  - exact plugin.json manifest format
  - plugin marketplace source schema details (url/ref/sha and URL suffix behavior)
  - plugin seed directory layering semantics (`CLAUDE_CODE_PLUGIN_SEED_DIR` with `:`/`;` path lists)
  - plugin persistent data directory behavior and uninstall semantics
  - plugin namespace and scoping
  - publishing to a registry
primary_doc: plugins.md
secondary_doc: plugin-marketplaces.md

---

### route_id: configure-permissions
domain_id: access-control-safety
domain_file: domain-access-control-safety.md
intent: control what tools and commands Claude can use
match:
  - "how do I allow a command"
  - "block Claude from editing a file"
  - "permission rules"
  - "allowedTools"
  - "denyTools"
  - "run Claude without prompts"
strong_terms: [permissions, allowedTools, denyTools, bypassPermissions, allow, deny, block]
avoid: [sandboxing, network]
answer_from_domain_if:
  - what permission modes are available
  - allow vs deny
  - permissions in CI
read_source_docs_if:
  - exact rule syntax and pattern matching
  - bypassPermissions protected-directory prompt exceptions
  - Read/Edit rule limits vs Bash subprocess access
  - Windows path normalization examples for Read/Edit rules
  - full tool name list
  - enterprise policy enforcement
primary_doc: permissions.md
secondary_doc: settings.md

---

### route_id: best-practices
domain_id: effective-interaction
domain_file: domain-effective-interaction.md
intent: work effectively with Claude Code on complex tasks
match:
  - "best practices for Claude Code"
  - "how to prompt Claude effectively"
  - "explore plan implement"
  - "context window getting large"
  - "parallel Claude sessions"
strong_terms: [best practices, explore plan implement, context, prompting, workflow]
avoid: [hooks, skills, permissions]
answer_from_domain_if:
  - what the explore-plan-implement workflow is
  - how to manage context
  - parallel sessions
read_source_docs_if:
  - specific workflow patterns
  - exact command syntax
primary_doc: best-practices.md
secondary_doc: common-workflows.md
