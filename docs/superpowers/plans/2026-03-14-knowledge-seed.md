# Knowledge Seed System Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pre-build a navigation and knowledge seed that ships with the plugin so `claude-code-expert` answers questions without reading all 65 docs on first invocation.

**Architecture:** Two-layer seed under `agent-memory-seed/` — `generated/` owned by GitHub Actions (Codex rebuilds incrementally on doc changes), `agent-notes/` owned by the agent at runtime and never touched by scripts. The agent copies `generated/` on install and consults `navigation.md` → `domain-*.md` → source docs in order, stopping as early as possible.

**Tech Stack:** Python 3.11, pytest, openai/codex-action@v1, GitHub Actions, Claude Code agent/skill markdown format.

---

## Chunk 1: Seed Directory Structure + Initial Content

**Files:**
- Create: `agent-memory-seed/generated/seed_manifest.json`
- Create: `agent-memory-seed/generated/navigation.md`
- Create: `agent-memory-seed/generated/domain-foundation.md`
- Create: `agent-memory-seed/generated/domain-configuration-persistence.md`
- Create: `agent-memory-seed/generated/domain-automation-control.md`
- Create: `agent-memory-seed/generated/domain-extension-capability.md`
- Create: `agent-memory-seed/generated/domain-access-control-safety.md`
- Create: `agent-memory-seed/generated/domain-effective-interaction.md`
- Create: `agent-memory-seed/agent-notes/.gitkeep`

### Task 1: Create directory structure

- [ ] **Step 1: Create directories**

```bash
mkdir -p /Volumes/storage/Projects/Git/Github/mrkhachaturov/claude-audit-plugin/agent-memory-seed/generated
mkdir -p /Volumes/storage/Projects/Git/Github/mrkhachaturov/claude-audit-plugin/agent-memory-seed/agent-notes
touch /Volumes/storage/Projects/Git/Github/mrkhachaturov/claude-audit-plugin/agent-memory-seed/agent-notes/.gitkeep
```

- [ ] **Step 2: Verify structure**

```bash
find agent-memory-seed -type f | sort
```

Expected output:
```
agent-memory-seed/agent-notes/.gitkeep
```

- [ ] **Step 3: Commit skeleton**

```bash
git add agent-memory-seed/agent-notes/.gitkeep
git commit -m "feat: add agent-memory-seed directory structure"
```

---

### Task 2: Create initial seed_manifest.json

Read `docs/docs_manifest.json` to understand the doc inventory. Then create the manifest with the full routes table covering all 6 domains.

- [ ] **Step 1: Read the docs manifest to understand available docs**

```bash
cat docs/docs_manifest.json | python3 -c "import json,sys; m=json.load(sys.stdin); [print(k) for k in sorted(m['files'].keys())]"
```

- [ ] **Step 2: Create seed_manifest.json**

Create `agent-memory-seed/generated/seed_manifest.json` with this structure (fill in real sha256 hashes after content is created in Tasks 3-9):

```json
{
  "schema_version": 1,
  "seed_version": "2026-03-14T00:00:00Z",
  "source_docs": {
    "how-claude-code-works.md": {
      "file_hash": "placeholder",
      "headings_hash": "placeholder",
      "headings": [],
      "sections": {}
    },
    "memory.md": {
      "file_hash": "placeholder",
      "headings_hash": "placeholder",
      "headings": [],
      "sections": {}
    },
    "settings.md": {
      "file_hash": "placeholder",
      "headings_hash": "placeholder",
      "headings": [],
      "sections": {}
    },
    "hooks.md": {
      "file_hash": "placeholder",
      "headings_hash": "placeholder",
      "headings": [],
      "sections": {}
    },
    "hooks-guide.md": {
      "file_hash": "placeholder",
      "headings_hash": "placeholder",
      "headings": [],
      "sections": {}
    },
    "skills.md": {
      "file_hash": "placeholder",
      "headings_hash": "placeholder",
      "headings": [],
      "sections": {}
    },
    "sub-agents.md": {
      "file_hash": "placeholder",
      "headings_hash": "placeholder",
      "headings": [],
      "sections": {}
    },
    "mcp.md": {
      "file_hash": "placeholder",
      "headings_hash": "placeholder",
      "headings": [],
      "sections": {}
    },
    "plugins.md": {
      "file_hash": "placeholder",
      "headings_hash": "placeholder",
      "headings": [],
      "sections": {}
    },
    "permissions.md": {
      "file_hash": "placeholder",
      "headings_hash": "placeholder",
      "headings": [],
      "sections": {}
    },
    "best-practices.md": {
      "file_hash": "placeholder",
      "headings_hash": "placeholder",
      "headings": [],
      "sections": {}
    }
  },
  "routes": {
    "how-claude-code-works": {
      "domain_id": "foundation",
      "domain_file": "domain-foundation.md",
      "primary_doc": "how-claude-code-works.md",
      "secondary_doc": "overview.md",
      "depends_on_sections": ["how-claude-code-works.md::agentic-loop"]
    },
    "configure-memory": {
      "domain_id": "configuration-persistence",
      "domain_file": "domain-configuration-persistence.md",
      "primary_doc": "memory.md",
      "secondary_doc": "settings.md",
      "depends_on_sections": ["memory.md::memory-types"]
    },
    "claude-md-structure": {
      "domain_id": "configuration-persistence",
      "domain_file": "domain-configuration-persistence.md",
      "primary_doc": "memory.md",
      "secondary_doc": "settings.md",
      "depends_on_sections": ["memory.md::claude-md"]
    },
    "configure-hooks": {
      "domain_id": "automation-control",
      "domain_file": "domain-automation-control.md",
      "primary_doc": "hooks.md",
      "secondary_doc": "hooks-guide.md",
      "depends_on_sections": ["hooks.md::event-types"]
    },
    "hooks-vs-skills": {
      "domain_id": "automation-control",
      "domain_file": "domain-automation-control.md",
      "primary_doc": "hooks.md",
      "secondary_doc": "skills.md",
      "depends_on_sections": ["hooks.md::overview"]
    },
    "configure-skills": {
      "domain_id": "extension-capability",
      "domain_file": "domain-extension-capability.md",
      "primary_doc": "skills.md",
      "secondary_doc": null,
      "depends_on_sections": ["skills.md::configure-skills"]
    },
    "skills-vs-claudemd": {
      "domain_id": "extension-capability",
      "domain_file": "domain-extension-capability.md",
      "primary_doc": "features-overview.md",
      "secondary_doc": "skills.md",
      "depends_on_sections": ["features-overview.md::compare-similar-features"]
    },
    "configure-agents": {
      "domain_id": "extension-capability",
      "domain_file": "domain-extension-capability.md",
      "primary_doc": "sub-agents.md",
      "secondary_doc": null,
      "depends_on_sections": ["sub-agents.md::configure-subagents"]
    },
    "configure-mcp": {
      "domain_id": "extension-capability",
      "domain_file": "domain-extension-capability.md",
      "primary_doc": "mcp.md",
      "secondary_doc": "settings.md",
      "depends_on_sections": ["mcp.md::installing-mcp-servers"]
    },
    "configure-plugins": {
      "domain_id": "extension-capability",
      "domain_file": "domain-extension-capability.md",
      "primary_doc": "plugins.md",
      "secondary_doc": "plugin-marketplaces.md",
      "depends_on_sections": ["plugins.md::plugin-structure-overview"]
    },
    "configure-permissions": {
      "domain_id": "access-control-safety",
      "domain_file": "domain-access-control-safety.md",
      "primary_doc": "permissions.md",
      "secondary_doc": "settings.md",
      "depends_on_sections": ["permissions.md::permission-rules"]
    },
    "best-practices": {
      "domain_id": "effective-interaction",
      "domain_file": "domain-effective-interaction.md",
      "primary_doc": "best-practices.md",
      "secondary_doc": "common-workflows.md",
      "depends_on_sections": ["best-practices.md::explore-plan-implement"]
    }
  },
  "outputs": {
    "domain-foundation.md": {
      "content_hash": "placeholder",
      "depends_on_sections": ["how-claude-code-works.md::agentic-loop"]
    },
    "domain-configuration-persistence.md": {
      "content_hash": "placeholder",
      "depends_on_sections": ["memory.md::memory-types", "memory.md::claude-md", "settings.md::configuration-scopes"]
    },
    "domain-automation-control.md": {
      "content_hash": "placeholder",
      "depends_on_sections": ["hooks.md::event-types", "hooks-guide.md::common-patterns"]
    },
    "domain-extension-capability.md": {
      "content_hash": "placeholder",
      "depends_on_sections": ["skills.md::configure-skills", "sub-agents.md::configure-subagents", "mcp.md::installing-mcp-servers", "plugins.md::plugin-structure-overview"]
    },
    "domain-access-control-safety.md": {
      "content_hash": "placeholder",
      "depends_on_sections": ["permissions.md::permission-rules"]
    },
    "domain-effective-interaction.md": {
      "content_hash": "placeholder",
      "depends_on_sections": ["best-practices.md::explore-plan-implement"]
    },
    "navigation.md": {
      "content_hash": "placeholder",
      "depends_on_routes": ["how-claude-code-works", "configure-memory", "claude-md-structure", "configure-hooks", "hooks-vs-skills", "configure-skills", "skills-vs-claudemd", "configure-agents", "configure-mcp", "configure-plugins", "configure-permissions", "best-practices"]
    }
  }
}
```

- [ ] **Step 3: Commit**

```bash
git add agent-memory-seed/generated/seed_manifest.json
git commit -m "feat: add initial seed_manifest.json schema"
```

---

### Task 3: Create domain-foundation.md

Read `docs/how-claude-code-works.md`, `docs/overview.md`, `docs/authentication.md`, `docs/amazon-bedrock.md`, `docs/google-vertex-ai.md`, `docs/microsoft-foundry.md`, `docs/data-usage.md`, `docs/legal-and-compliance.md`, `docs/zero-data-retention.md`.

- [ ] **Step 1: Read the source docs**

```bash
cat docs/how-claude-code-works.md docs/overview.md docs/authentication.md | head -200
```

- [ ] **Step 2: Create the domain file**

Create `agent-memory-seed/generated/domain-foundation.md`:

```markdown
# Domain: Foundation

## What this domain covers
How Claude Code operates at its core: the agentic loop, available tools, execution environments, authentication methods, provider integrations (Bedrock, Vertex, Foundry), data usage policies, and legal/compliance constraints.

## Decision rules
- Use this domain for questions about how Claude Code works internally
- Use this domain for authentication and subscription setup questions
- Use this domain for provider-specific setup (AWS, GCP, Azure)
- Use this domain for data privacy, retention, and compliance questions

## Fast answers
- **What is the agentic loop?** Claude reads context, decides actions, uses tools, observes results, repeats until done
- **What tools does Claude Code have?** Read, Write, Edit, Bash, Glob, Grep, Agent (subagents), and MCP tools
- **Auth options:** Claude.ai subscription (OAuth), API key (direct), or enterprise providers (Bedrock/Vertex/Foundry)
- **Does Claude send my code to Anthropic?** Depends on plan — see data-usage.md; zero-data-retention available for API users

## Fast comparisons
- **OAuth vs API key:** OAuth uses your Claude.ai subscription; API key uses pay-per-token billing
- **Bedrock vs Vertex vs direct API:** All use Claude models; differ in where inference runs and who manages auth
- **Pro vs Max plan:** Both work with Claude Code; Max has higher usage limits

## Common tasks
- "Set up Claude Code for the first time" → quickstart.md
- "Use Claude Code with AWS" → amazon-bedrock.md
- "Use Claude Code with GCP" → google-vertex-ai.md
- "Understand what data Anthropic sees" → data-usage.md
- "Comply with zero-data-retention requirements" → zero-data-retention.md

## When you must read source docs
- Exact OAuth token setup steps
- Bedrock/Vertex/Foundry IAM and credential configuration
- Specific compliance certifications or legal terms
- Network proxy or certificate configuration for enterprise

## Source map
- how-claude-code-works.md
- overview.md
- authentication.md
- amazon-bedrock.md
- google-vertex-ai.md
- microsoft-foundry.md
- llm-gateway.md
- data-usage.md
- legal-and-compliance.md
- zero-data-retention.md
- analytics.md
- chrome.md
- claude-code-on-the-web.md
```

- [ ] **Step 3: Verify file is well-formed**

```bash
wc -l agent-memory-seed/generated/domain-foundation.md
# Expect: 40-70 lines
```

- [ ] **Step 4: Commit**

```bash
git add agent-memory-seed/generated/domain-foundation.md
git commit -m "feat: add domain-foundation seed file"
```

---

### Task 4: Create domain-configuration-persistence.md

Read `docs/memory.md`, `docs/settings.md`, `docs/env-vars.md`, `docs/server-managed-settings.md`.

- [ ] **Step 1: Read the source docs**

```bash
cat docs/memory.md | head -150
cat docs/settings.md | head -150
```

- [ ] **Step 2: Create the domain file**

Create `agent-memory-seed/generated/domain-configuration-persistence.md`:

```markdown
# Domain: Configuration & Persistence

## What this domain covers
Storing instructions and settings that persist across sessions: CLAUDE.md files (project and personal), auto-memory system, settings.json configuration, environment variables, and server-managed settings for enterprise.

## Decision rules
- Use `CLAUDE.md` for always-on project-level instructions Claude should always follow
- Use `~/.claude/CLAUDE.md` for personal preferences that apply across all projects
- Use auto-memory (`/memory` command) for facts Claude should remember across sessions
- Use `settings.json` for tool permissions, hooks, and UI preferences
- Use environment variables for secrets and CI/CD configuration

## Fast answers
- **Where does CLAUDE.md live?** Project root or `.claude/CLAUDE.md`; personal at `~/.claude/CLAUDE.md`
- **What goes in CLAUDE.md?** Project conventions, coding style, architecture notes, commands to run
- **What is auto-memory?** Claude can save notes to `~/.claude/MEMORY.md` using the `/memory` command
- **Settings precedence:** enterprise > project > user (higher wins)
- **settings.json location:** `.claude/settings.json` (project) or `~/.claude/settings.json` (user)

## Fast comparisons
- **CLAUDE.md vs memory:** CLAUDE.md is manually curated; memory is agent-written via `/memory`
- **CLAUDE.md vs skills:** CLAUDE.md is always loaded; skills are loaded on demand
- **CLAUDE.md vs rules:** Rules are scoped to paths or topics; CLAUDE.md is always-on project-wide
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
```

- [ ] **Step 3: Commit**

```bash
git add agent-memory-seed/generated/domain-configuration-persistence.md
git commit -m "feat: add domain-configuration-persistence seed file"
```

---

### Task 5: Create domain-automation-control.md

Read `docs/hooks.md`, `docs/hooks-guide.md`, `docs/scheduled-tasks.md`.

- [ ] **Step 1: Read the source docs**

```bash
cat docs/hooks.md | head -150
cat docs/hooks-guide.md | head -100
```

- [ ] **Step 2: Create the domain file**

Create `agent-memory-seed/generated/domain-automation-control.md`:

```markdown
# Domain: Automation & Control

## What this domain covers
Deterministic automation triggered at specific lifecycle points: hooks (shell commands run on tool events) and scheduled tasks (recurring commands run on a cron-like schedule).

## Decision rules
- Use hooks when you need to run code **automatically** at a specific tool lifecycle point
- Use hooks for formatting, linting, notifications, blocking unsafe operations
- Use scheduled tasks for recurring maintenance that should run independently
- Use CLAUDE.md instructions instead of hooks when the behavior should be context-dependent

## Fast answers
- **What are hooks?** Shell commands in settings.json that run before/after specific Claude tool uses
- **Hook events:** `PreToolUse`, `PostToolUse`, `Notification`, `Stop`, `SubagentStop`
- **Can hooks block Claude?** Yes — `PreToolUse` hooks that exit non-zero can block the tool call
- **Where do hooks live?** `.claude/settings.json` under the `hooks` key

## Fast comparisons
- **Hooks vs skills:** Hooks run automatically on events; skills run when explicitly invoked
- **Hooks vs CLAUDE.md:** Hooks are deterministic shell commands; CLAUDE.md is natural language instructions
- **Hooks vs scheduled tasks:** Hooks respond to tool events; scheduled tasks run on time intervals
- **PreToolUse vs PostToolUse:** Pre can block/modify; Post observes and reacts

## Common tasks
- "Auto-format code after every file write" → PostToolUse hook on Write tool
- "Block dangerous shell commands" → PreToolUse hook on Bash tool
- "Get notified when Claude finishes a task" → Notification hook
- "Run linting after edits" → PostToolUse hook on Edit/Write tools
- "Run a script every night" → scheduled-tasks.md

## When you must read source docs
- Exact hook matcher syntax (tool name patterns, regex)
- Blocking hook exit code semantics
- Full list of hookable events and their payloads
- Scheduled task cron expression format and limits

## Source map
- hooks.md
- hooks-guide.md
- scheduled-tasks.md
```

- [ ] **Step 3: Commit**

```bash
git add agent-memory-seed/generated/domain-automation-control.md
git commit -m "feat: add domain-automation-control seed file"
```

---

### Task 6: Create domain-extension-capability.md

Read `docs/skills.md`, `docs/sub-agents.md`, `docs/agent-teams.md`, `docs/mcp.md`, `docs/plugins.md`, `docs/plugins-reference.md`, `docs/features-overview.md`.

- [ ] **Step 1: Read source docs**

```bash
cat docs/skills.md | head -120
cat docs/sub-agents.md | head -100
cat docs/mcp.md | head -100
```

- [ ] **Step 2: Create the domain file**

Create `agent-memory-seed/generated/domain-extension-capability.md`:

```markdown
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
```

- [ ] **Step 3: Commit**

```bash
git add agent-memory-seed/generated/domain-extension-capability.md
git commit -m "feat: add domain-extension-capability seed file"
```

---

### Task 7: Create domain-access-control-safety.md

Read `docs/permissions.md`, `docs/sandboxing.md`, `docs/security.md`, `docs/network-config.md`.

- [ ] **Step 1: Read source docs**

```bash
cat docs/permissions.md | head -150
cat docs/sandboxing.md | head -100
```

- [ ] **Step 2: Create the domain file**

Create `agent-memory-seed/generated/domain-access-control-safety.md`:

```markdown
# Domain: Access Control & Safety

## What this domain covers
Controlling what Claude Code can access and do: permission modes, tool allow/deny rules, sandboxing, network configuration, and security best practices.

## Decision rules
- Configure permissions in `settings.json` under the `permissions` key
- Use permission rules to allow safe commands and block dangerous ones
- Use sandboxing when Claude needs internet access or file system isolation
- Use network config for corporate proxy or certificate requirements

## Fast answers
- **Permission modes:** `default` (prompt for risky), `acceptEdits` (auto-approve edits), `bypassPermissions` (auto-approve all — use with care)
- **Where do permissions live?** `.claude/settings.json` or `~/.claude/settings.json` under `permissions`
- **Can I allow specific bash commands?** Yes — `allowedTools` with bash command patterns
- **Can I block Claude from editing certain files?** Yes — `denyTools` or path-based rules

## Fast comparisons
- **allowedTools vs denyTools:** Allow is a whitelist; deny is a blacklist; deny takes precedence
- **Project permissions vs user permissions:** Project overrides user for that project
- **Permission prompt vs bypassPermissions:** Prompt asks each time; bypass auto-approves (risky in CI)

## Common tasks
- "Allow Claude to run npm test without asking" → allowedTools with bash pattern
- "Prevent Claude from editing .env files" → denyTools with file path pattern
- "Run Claude in CI without prompts" → bypassPermissions mode with restricted allowedTools
- "Isolate Claude's network access" → sandboxing.md

## When you must read source docs
- Exact permission rule syntax and pattern matching
- Full list of tool names for allow/deny rules
- Sandboxing setup and limitations
- Network proxy configuration syntax

## Source map
- permissions.md
- sandboxing.md
- security.md
- network-config.md
- llm-gateway.md
```

- [ ] **Step 3: Commit**

```bash
git add agent-memory-seed/generated/domain-access-control-safety.md
git commit -m "feat: add domain-access-control-safety seed file"
```

---

### Task 8: Create domain-effective-interaction.md

Read `docs/best-practices.md`, `docs/common-workflows.md`, `docs/commands.md`, `docs/interactive-mode.md`, `docs/output-styles.md`, `docs/model-config.md`, `docs/fast-mode.md`.

- [ ] **Step 1: Read source docs**

```bash
cat docs/best-practices.md | head -150
cat docs/common-workflows.md | head -100
cat docs/commands.md | head -100
```

- [ ] **Step 2: Create the domain file**

Create `agent-memory-seed/generated/domain-effective-interaction.md`:

```markdown
# Domain: Effective Interaction

## What this domain covers
Working well with Claude Code as an agentic tool: prompting strategies, common workflows, built-in slash commands, output configuration, model selection, fast mode, IDE integrations, remote/headless operation, and checkpointing.

## Decision rules
- Use explore-plan-implement workflow for complex or risky tasks
- Use `/clear` to reset context when it gets too large or polluted
- Use headless mode (`claude -p`) for CI/CD and scripted automation
- Use checkpointing for long tasks where you might want to roll back

## Fast answers
- **Built-in commands:** `/clear`, `/memory`, `/cost`, `/stats`, `/model`, `/hooks`, `/agents`, `/plugin`
- **How to use a skill:** type `/skill-name` or ask Claude to use it
- **Model selection:** `/model` command or `model` in settings.json
- **Fast mode:** lower latency, same model, uses extra usage credits on subscription plans
- **Headless mode:** `claude -p "your prompt"` for non-interactive scripted use

## Fast comparisons
- **Interactive vs headless:** Interactive is conversational; headless is single-shot for automation
- **fast mode vs standard:** Fast mode has lower latency; standard may be more thorough on complex tasks
- **`/clear` vs new session:** `/clear` resets context in same session; new session is fully fresh

## Common tasks
- "Run Claude without interaction" → headless.md
- "Reduce context window usage" → `/clear`, or use subagents
- "Run parallel Claude sessions" → best-practices.md (parallel sessions section)
- "Configure Claude for VSCode" → vs-code.md
- "Configure Claude for JetBrains" → jetbrains.md
- "Check token usage and costs" → `/cost` command, monitoring-usage.md

## When you must read source docs
- Full list of slash commands and their arguments
- Exact headless mode flags and options
- Output style configuration options
- Remote control API details
- Checkpointing setup and restore process

## Source map
- best-practices.md
- common-workflows.md
- commands.md
- interactive-mode.md
- output-styles.md
- model-config.md
- fast-mode.md
- keybindings.md
- vs-code.md
- jetbrains.md
- remote-control.md
- headless.md
- checkpointing.md
- monitoring-usage.md
- costs.md
- statusline.md
- terminal-config.md
- desktop.md
- desktop-quickstart.md
- slack.md
- third-party-integrations.md
- devcontainer.md
- github-actions.md
- gitlab-ci-cd.md
- quickstart.md
- setup.md
- troubleshooting.md
```

- [ ] **Step 3: Commit**

```bash
git add agent-memory-seed/generated/domain-effective-interaction.md
git commit -m "feat: add domain-effective-interaction seed file"
```

---

### Task 9: Create navigation.md

This is generated from the `routes` object in `seed_manifest.json`. Each route becomes one block in the file.

- [ ] **Step 1: Create navigation.md**

Create `agent-memory-seed/generated/navigation.md`:

```markdown
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
  - "PostToolUse hook"
  - "notification hook"
strong_terms: [hook, PostToolUse, PreToolUse, Notification, Stop, matcher, blocking]
avoid: [scheduled tasks, cron, skills]
answer_from_domain_if:
  - what hooks are
  - when to use hooks vs other primitives
  - hooks vs skills or CLAUDE.md
read_source_docs_if:
  - exact matcher syntax
  - blocking semantics and exit codes
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
intent: create or configure a subagent
match:
  - "how do I create a subagent"
  - "what is a subagent"
  - "agent frontmatter"
  - "dispatch a subagent"
  - "agent memory"
strong_terms: [subagent, agent, Agent tool, dispatch, isolated context, agent memory]
avoid: [MCP, plugins, hooks]
answer_from_domain_if:
  - what a subagent is
  - subagent vs skill
  - when to use subagents
read_source_docs_if:
  - exact agent frontmatter fields
  - tool and memory configuration
  - agent isolation guarantees
primary_doc: sub-agents.md
secondary_doc: null

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
strong_terms: [MCP, stdio, SSE, http, mcp server, claude mcp add, external tool]
avoid: [plugins, hooks, skills]
answer_from_domain_if:
  - what MCP is
  - MCP vs plugins
  - when to use MCP
read_source_docs_if:
  - exact mcp add command syntax
  - transport type selection
  - OAuth and auth configuration
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
  - "plugin manifest"
  - "plugin.json"
  - "share skills across projects"
strong_terms: [plugin, plugin.json, marketplace, install plugin, publish plugin]
avoid: [MCP, skills as standalone, hooks standalone]
answer_from_domain_if:
  - what a plugin is
  - plugin vs skill or MCP
  - how to install a plugin
read_source_docs_if:
  - exact plugin.json manifest format
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
```

- [ ] **Step 2: Verify all route_ids match seed_manifest.json routes**

```bash
python3 -c "
import json, re
manifest = json.load(open('agent-memory-seed/generated/seed_manifest.json'))
nav = open('agent-memory-seed/generated/navigation.md').read()
route_ids_in_manifest = set(manifest['routes'].keys())
route_ids_in_nav = set(re.findall(r'### route_id: (\S+)', nav))
missing_from_nav = route_ids_in_manifest - route_ids_in_nav
missing_from_manifest = route_ids_in_nav - route_ids_in_manifest
print('Missing from navigation:', missing_from_nav)
print('Missing from manifest:', missing_from_manifest)
assert not missing_from_nav and not missing_from_manifest, 'Mismatch!'
print('OK: all route_ids consistent')
"
```

Expected: `OK: all route_ids consistent`

- [ ] **Step 3: Commit**

```bash
git add agent-memory-seed/generated/navigation.md
git commit -m "feat: add initial navigation.md with 12 routes across 6 domains"
```

---

### Task 9.5: Compute real sha256 hashes for seed_manifest.json

Now that all content files (Tasks 3-9) exist, replace the `"placeholder"` hashes in `seed_manifest.json` with real sha256 values.

- [ ] **Step 1: Compute and update file_hash and headings_hash for each source_doc**

```python
import hashlib, json, re
from pathlib import Path

repo = Path(".")
manifest_path = repo / "agent-memory-seed" / "generated" / "seed_manifest.json"
manifest = json.loads(manifest_path.read_text())

docs_dir = repo / "docs"
for filename in manifest["source_docs"]:
    doc_path = docs_dir / filename
    if not doc_path.exists():
        print(f"WARNING: {filename} not found in docs/, skipping")
        continue
    content = doc_path.read_bytes()
    file_hash = hashlib.sha256(content).hexdigest()
    headings = re.findall(r'^#{1,4}\s+(.+)', doc_path.read_text(), re.MULTILINE)
    headings_hash = hashlib.sha256("\n".join(headings).encode()).hexdigest()
    manifest["source_docs"][filename]["file_hash"] = file_hash
    manifest["source_docs"][filename]["headings_hash"] = headings_hash
    manifest["source_docs"][filename]["headings"] = headings
    print(f"  {filename}: {file_hash[:12]}...")

manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
print("Done — seed_manifest.json updated with real hashes")
```

Run with:

```bash
cd /Volumes/storage/Projects/Git/Github/mrkhachaturov/claude-audit-plugin
python3 - <<'EOF'
import hashlib, json, re
from pathlib import Path

repo = Path(".")
manifest_path = repo / "agent-memory-seed" / "generated" / "seed_manifest.json"
manifest = json.loads(manifest_path.read_text())

docs_dir = repo / "docs"
for filename in manifest["source_docs"]:
    doc_path = docs_dir / filename
    if not doc_path.exists():
        print(f"WARNING: {filename} not found in docs/, skipping")
        continue
    content = doc_path.read_bytes()
    file_hash = hashlib.sha256(content).hexdigest()
    headings = re.findall(r'^#{1,4}\s+(.+)', doc_path.read_text(), re.MULTILINE)
    headings_hash = hashlib.sha256("\n".join(headings).encode()).hexdigest()
    manifest["source_docs"][filename]["file_hash"] = file_hash
    manifest["source_docs"][filename]["headings_hash"] = headings_hash
    manifest["source_docs"][filename]["headings"] = headings
    print(f"  {filename}: {file_hash[:12]}...")

manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
print("Done — seed_manifest.json updated with real hashes")
EOF
```

- [ ] **Step 2: Compute content_hash for each output file**

```bash
python3 - <<'EOF'
import hashlib, json
from pathlib import Path

repo = Path(".")
manifest_path = repo / "agent-memory-seed" / "generated" / "seed_manifest.json"
manifest = json.loads(manifest_path.read_text())

generated_dir = repo / "agent-memory-seed" / "generated"
for output_file in manifest["outputs"]:
    out_path = generated_dir / output_file
    if not out_path.exists():
        print(f"WARNING: {output_file} not found, skipping")
        continue
    content_hash = hashlib.sha256(out_path.read_bytes()).hexdigest()
    manifest["outputs"][output_file]["content_hash"] = content_hash
    print(f"  {output_file}: {content_hash[:12]}...")

manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
print("Done — output content_hashes updated")
EOF
```

- [ ] **Step 3: Verify no placeholders remain**

```bash
python3 -c "
import json
m = json.load(open('agent-memory-seed/generated/seed_manifest.json'))
placeholders = []
for doc, meta in m['source_docs'].items():
    for k in ['file_hash', 'headings_hash']:
        if meta[k] == 'placeholder':
            placeholders.append(f'source_docs[{doc}][{k}]')
for out, meta in m['outputs'].items():
    if meta['content_hash'] == 'placeholder':
        placeholders.append(f'outputs[{out}][content_hash]')
if placeholders:
    print('ERROR: still has placeholders:', placeholders)
    exit(1)
print('OK: all hashes are real sha256 values')
"
```

Expected: `OK: all hashes are real sha256 values`

- [ ] **Step 4: Commit**

```bash
git add agent-memory-seed/generated/seed_manifest.json
git commit -m "feat: populate seed_manifest.json with real sha256 hashes"
```

---

## Chunk 2: Python Build Scripts (TDD)

**Files:**
- Create: `scripts/check_significance.py`
- Create: `scripts/validate_seed.py`
- Create: `scripts/bump_version.py`
- Create: `tests/conftest.py`
- Create: `tests/test_check_significance.py`
- Create: `tests/test_validate_seed.py`
- Create: `tests/test_bump_version.py`
- Modify: `scripts/requirements.txt`

### Task 10: Set up test infrastructure

- [ ] **Step 1: Install pytest**

```bash
cd /Volumes/storage/Projects/Git/Github/mrkhachaturov/claude-audit-plugin
pip install pytest pytest-mock
```

- [ ] **Step 2: Add pytest to requirements-dev.txt**

Create `scripts/requirements-dev.txt`:

```
pytest==8.3.4
pytest-mock==3.14.0
```

- [ ] **Step 3: Create tests/ directory and conftest.py**

Create `tests/conftest.py`:

```python
"""Shared fixtures for claude-audit plugin tests."""
import json
import pytest
from pathlib import Path


@pytest.fixture
def tmp_repo(tmp_path):
    """A minimal fake repo structure for testing scripts."""
    # Create docs/
    docs = tmp_path / "docs"
    docs.mkdir()

    # Create agent-memory-seed/generated/
    seed_generated = tmp_path / "agent-memory-seed" / "generated"
    seed_generated.mkdir(parents=True)

    # Create agent-memory-seed/agent-notes/
    agent_notes = tmp_path / "agent-memory-seed" / "agent-notes"
    agent_notes.mkdir()
    (agent_notes / ".gitkeep").touch()

    return tmp_path


@pytest.fixture
def minimal_manifest():
    """A minimal valid seed_manifest.json."""
    return {
        "schema_version": 1,
        "seed_version": "2026-03-14T00:00:00Z",
        "source_docs": {
            "hooks.md": {
                "file_hash": "abc123",
                "headings_hash": "def456",
                "headings": ["Overview", "Event Types"],
                "sections": {
                    "event-types": {
                        "hash": "ghi789",
                        "start_heading": "Event Types",
                        "end_heading": "Tool Events",
                        "domains": ["automation-control"],
                        "routes": ["configure-hooks"]
                    }
                }
            }
        },
        "routes": {
            "configure-hooks": {
                "domain_id": "automation-control",
                "domain_file": "domain-automation-control.md",
                "primary_doc": "hooks.md",
                "secondary_doc": "hooks-guide.md",
                "depends_on_sections": ["hooks.md::event-types"]
            }
        },
        "outputs": {
            "domain-automation-control.md": {
                "content_hash": "jkl012",
                "depends_on_sections": ["hooks.md::event-types"]
            },
            "navigation.md": {
                "content_hash": "mno345",
                "depends_on_routes": ["configure-hooks"]
            }
        }
    }
```

- [ ] **Step 4: Verify pytest works**

```bash
cd /Volumes/storage/Projects/Git/Github/mrkhachaturov/claude-audit-plugin
python -m pytest tests/ -v
```

Expected: `no tests ran` (no test files yet — that's fine)

- [ ] **Step 5: Commit**

```bash
git add tests/conftest.py scripts/requirements-dev.txt
git commit -m "test: add pytest infrastructure and shared fixtures"
```

---

### Task 11: check_significance.py (TDD)

`check_significance.py` reads `docs_manifest.json` + `seed_manifest.json` + git diff output, and outputs `rebuild`, `affected_domains`, `affected_routes`, `changed_docs` to stdout (for `>> $GITHUB_OUTPUT`).

- [ ] **Step 1: Write failing tests**

Create `tests/test_check_significance.py`:

```python
"""Tests for check_significance.py."""
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


# We'll import the module under test once it exists
# For now, define the interface we expect:
# check_significance.run(repo_root, git_diff_output) -> dict with keys:
#   rebuild: bool
#   affected_domains: list[str]
#   affected_routes: list[str]
#   changed_docs: list[str]


def test_no_changes_returns_no_rebuild(tmp_repo, minimal_manifest):
    """When docs haven't changed, rebuild should be False."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    seed_manifest_path = tmp_repo / "agent-memory-seed" / "generated" / "seed_manifest.json"
    seed_manifest_path.write_text(json.dumps(minimal_manifest))

    # Empty git diff = no changes
    git_diff = ""

    from check_significance import analyze_changes
    result = analyze_changes(str(tmp_repo), git_diff, minimal_manifest)

    assert result["rebuild"] is False
    assert result["changed_docs"] == []


def test_new_file_triggers_rebuild(tmp_repo, minimal_manifest):
    """Adding a new doc should always trigger rebuild."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    seed_manifest_path = tmp_repo / "agent-memory-seed" / "generated" / "seed_manifest.json"
    seed_manifest_path.write_text(json.dumps(minimal_manifest))

    # Git diff showing a new file added
    git_diff = "diff --git a/docs/new-feature.md b/docs/new-feature.md\nnew file mode 100644\n+++ b/docs/new-feature.md\n@@ -0,0 +1,50 @@\n+# New Feature\n"

    from check_significance import analyze_changes
    result = analyze_changes(str(tmp_repo), git_diff, minimal_manifest)

    assert result["rebuild"] is True
    assert "new-feature.md" in result["changed_docs"]


def test_small_change_no_rebuild(tmp_repo, minimal_manifest):
    """A small prose change (< 30 lines, no heading change) should not trigger rebuild."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    seed_manifest_path = tmp_repo / "agent-memory-seed" / "generated" / "seed_manifest.json"
    seed_manifest_path.write_text(json.dumps(minimal_manifest))

    # Small diff: 3 lines changed, no heading change
    git_diff = (
        "diff --git a/docs/hooks.md b/docs/hooks.md\n"
        "--- a/docs/hooks.md\n+++ b/docs/hooks.md\n"
        "@@ -10,3 +10,3 @@\n"
        "-old sentence here\n"
        "+new sentence here\n"
    )

    from check_significance import analyze_changes
    result = analyze_changes(str(tmp_repo), git_diff, minimal_manifest)

    assert result["rebuild"] is False


def test_heading_change_triggers_rebuild(tmp_repo, minimal_manifest):
    """A changed heading in a tracked doc should trigger rebuild."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    seed_manifest_path = tmp_repo / "agent-memory-seed" / "generated" / "seed_manifest.json"
    seed_manifest_path.write_text(json.dumps(minimal_manifest))

    # Diff showing a heading change in hooks.md
    git_diff = (
        "diff --git a/docs/hooks.md b/docs/hooks.md\n"
        "--- a/docs/hooks.md\n+++ b/docs/hooks.md\n"
        "@@ -5,1 +5,1 @@\n"
        "-## Event Types\n"
        "+## Hook Event Types\n"
    )

    from check_significance import analyze_changes
    result = analyze_changes(str(tmp_repo), git_diff, minimal_manifest)

    assert result["rebuild"] is True
    assert "hooks.md" in result["changed_docs"]


def test_large_change_triggers_rebuild(tmp_repo, minimal_manifest):
    """30+ changed lines should trigger rebuild regardless of heading changes."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    seed_manifest_path = tmp_repo / "agent-memory-seed" / "generated" / "seed_manifest.json"
    seed_manifest_path.write_text(json.dumps(minimal_manifest))

    # Simulate 35 lines added/removed in hooks.md (no heading change)
    changed_lines = "\n".join([f"+line {i}" for i in range(35)])
    git_diff = (
        "diff --git a/docs/hooks.md b/docs/hooks.md\n"
        "--- a/docs/hooks.md\n+++ b/docs/hooks.md\n"
        "@@ -20,0 +20,35 @@\n"
        f"{changed_lines}\n"
    )

    from check_significance import analyze_changes
    result = analyze_changes(str(tmp_repo), git_diff, minimal_manifest)

    assert result["rebuild"] is True


def test_affected_routes_identified(tmp_repo, minimal_manifest):
    """Changed doc sections should identify which routes are affected."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    seed_manifest_path = tmp_repo / "agent-memory-seed" / "generated" / "seed_manifest.json"
    seed_manifest_path.write_text(json.dumps(minimal_manifest))

    # Heading change in hooks.md — affects configure-hooks route
    git_diff = (
        "diff --git a/docs/hooks.md b/docs/hooks.md\n"
        "--- a/docs/hooks.md\n+++ b/docs/hooks.md\n"
        "@@ -5,1 +5,1 @@\n"
        "-## Event Types\n"
        "+## Hook Event Types\n"
    )

    from check_significance import analyze_changes
    result = analyze_changes(str(tmp_repo), git_diff, minimal_manifest)

    assert "configure-hooks" in result["affected_routes"]
    assert "automation-control" in result["affected_domains"]
```

- [ ] **Step 2: Run tests to confirm they all fail**

```bash
cd /Volumes/storage/Projects/Git/Github/mrkhachaturov/claude-audit-plugin
python -m pytest tests/test_check_significance.py -v 2>&1 | head -30
```

Expected: `ImportError` or `ModuleNotFoundError` — script doesn't exist yet.

- [ ] **Step 3: Implement check_significance.py**

Create `scripts/check_significance.py`:

```python
#!/usr/bin/env python3
"""
Check whether doc changes are significant enough to trigger a seed rebuild.

Outputs GitHub Actions output variables:
  rebuild=true/false
  affected_routes=comma,separated
  affected_domains=comma,separated
  changed_docs=comma,separated

Usage: python scripts/check_significance.py >> $GITHUB_OUTPUT
"""

import json
import os
import re
import sys
from pathlib import Path


LINES_CHANGED_THRESHOLD = 30


def load_seed_manifest(repo_root: str) -> dict:
    """Load the current seed_manifest.json, or return empty dict if missing."""
    path = Path(repo_root) / "agent-memory-seed" / "generated" / "seed_manifest.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def parse_git_diff(diff_output: str) -> dict:
    """
    Parse unified diff output (git diff -U0) into per-file change info.

    Returns: {
        "filename.md": {
            "is_new": bool,
            "lines_changed": int,
            "changed_headings": [str],  # heading text that was added/removed
            "hunk_line_ranges": [(start, count), ...]
        }
    }
    """
    result = {}
    current_file = None

    for line in diff_output.splitlines():
        # Detect file being diffed
        if line.startswith("diff --git"):
            # Extract filename from "diff --git a/docs/foo.md b/docs/foo.md"
            match = re.search(r'b/docs/(.+\.md)$', line)
            if match:
                current_file = match.group(1)
                result[current_file] = {
                    "is_new": False,
                    "lines_changed": 0,
                    "changed_headings": [],
                    "hunk_line_ranges": []
                }
            else:
                current_file = None
            continue

        if current_file is None:
            continue

        # Detect new file
        if line.startswith("new file mode"):
            result[current_file]["is_new"] = True

        # Count changed lines and detect heading changes
        if line.startswith("+") and not line.startswith("+++"):
            result[current_file]["lines_changed"] += 1
            heading_match = re.match(r'^\+#{1,4}\s+(.+)', line)
            if heading_match:
                result[current_file]["changed_headings"].append(heading_match.group(1).strip())

        elif line.startswith("-") and not line.startswith("---"):
            result[current_file]["lines_changed"] += 1
            heading_match = re.match(r'^-#{1,4}\s+(.+)', line)
            if heading_match:
                result[current_file]["changed_headings"].append(heading_match.group(1).strip())

        # Parse hunk line ranges: @@ -L,N +L,N @@
        hunk_match = re.match(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@', line)
        if hunk_match:
            start = int(hunk_match.group(1))
            count = int(hunk_match.group(2)) if hunk_match.group(2) else 1
            result[current_file]["hunk_line_ranges"].append((start, count))

    return result


def identify_affected_routes_and_domains(
    changed_files: dict, seed_manifest: dict
) -> tuple[list, list]:
    """
    Given changed file info and seed_manifest, return affected route_ids and domain_ids.
    """
    if not seed_manifest:
        return [], []

    affected_routes = set()
    affected_domains = set()
    routes = seed_manifest.get("routes", {})
    source_docs = seed_manifest.get("source_docs", {})

    for filename, change_info in changed_files.items():
        if filename not in source_docs:
            # New or unknown doc — mark all routes as affected
            for route_id, route in routes.items():
                affected_routes.add(route_id)
                affected_domains.add(route["domain_id"])
            continue

        doc_meta = source_docs[filename]

        # Check if any changed headings match known section boundaries
        known_headings = set(doc_meta.get("headings", []))
        changed_headings = set(change_info.get("changed_headings", []))
        heading_overlap = known_headings & changed_headings

        if heading_overlap or change_info["lines_changed"] >= LINES_CHANGED_THRESHOLD or change_info["is_new"]:
            # Find routes that depend on this file
            for section_id, section in doc_meta.get("sections", {}).items():
                for route_id in section.get("routes", []):
                    if route_id in routes:
                        affected_routes.add(route_id)
                        affected_domains.add(routes[route_id]["domain_id"])

    return sorted(affected_routes), sorted(affected_domains)


def analyze_changes(repo_root: str, git_diff: str, seed_manifest: dict) -> dict:
    """
    Core analysis function. Separated from I/O for testability.

    Returns dict with keys: rebuild, affected_routes, affected_domains, changed_docs
    """
    changed_files = parse_git_diff(git_diff)

    if not changed_files:
        return {
            "rebuild": False,
            "affected_routes": [],
            "affected_domains": [],
            "changed_docs": []
        }

    # Determine if rebuild is warranted
    should_rebuild = False
    for filename, info in changed_files.items():
        if info["is_new"]:
            should_rebuild = True
            break
        if info["changed_headings"]:
            should_rebuild = True
            break
        if info["lines_changed"] >= LINES_CHANGED_THRESHOLD:
            should_rebuild = True
            break

    affected_routes, affected_domains = identify_affected_routes_and_domains(
        changed_files, seed_manifest
    )

    return {
        "rebuild": should_rebuild,
        "affected_routes": affected_routes,
        "affected_domains": affected_domains,
        "changed_docs": sorted(changed_files.keys())
    }


def main():
    repo_root = Path(__file__).parent.parent
    seed_manifest = load_seed_manifest(str(repo_root))

    # Read git diff from stdin or run git diff
    try:
        import subprocess
        result = subprocess.run(
            ["git", "diff", "-U0", "HEAD~1", "--", "docs/"],
            capture_output=True, text=True, cwd=repo_root
        )
        git_diff = result.stdout
    except Exception as e:
        print(f"Warning: could not run git diff: {e}", file=sys.stderr)
        git_diff = ""

    analysis = analyze_changes(str(repo_root), git_diff, seed_manifest)

    # Output in GitHub Actions format
    print(f"rebuild={'true' if analysis['rebuild'] else 'false'}")
    print(f"affected_routes={','.join(analysis['affected_routes'])}")
    print(f"affected_domains={','.join(analysis['affected_domains'])}")
    print(f"changed_docs={','.join(analysis['changed_docs'])}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests — all should pass**

```bash
cd /Volumes/storage/Projects/Git/Github/mrkhachaturov/claude-audit-plugin
python -m pytest tests/test_check_significance.py -v
```

Expected: all 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/check_significance.py tests/test_check_significance.py
git commit -m "feat: add check_significance.py with tests"
```

---

### Task 12: validate_seed.py (TDD)

`validate_seed.py` checks the seed files after Codex runs. Exits 0 if valid, 1 if issues found.

- [ ] **Step 1: Write failing tests**

Create `tests/test_validate_seed.py`:

```python
"""Tests for validate_seed.py."""
import json
import pytest
from pathlib import Path


def write_valid_seed(tmp_repo, manifest):
    """Helper: write a complete valid seed to tmp_repo."""
    generated = tmp_repo / "agent-memory-seed" / "generated"
    generated.mkdir(parents=True, exist_ok=True)

    (generated / "seed_manifest.json").write_text(json.dumps(manifest))

    # Create navigation.md with matching route_ids
    route_ids = list(manifest.get("routes", {}).keys())
    nav_content = "# Claude Code Navigation Seed\n\n"
    for rid in route_ids:
        nav_content += f"### route_id: {rid}\ndomain_id: test\ndomain_file: domain-test.md\n\n"
    (generated / "navigation.md").write_text(nav_content)

    # Create domain files listed in routes
    domain_files = {r["domain_file"] for r in manifest.get("routes", {}).values()}
    for df in domain_files:
        (generated / df).write_text(f"# Domain Test\n")

    # Create agent-notes/.gitkeep
    notes = tmp_repo / "agent-memory-seed" / "agent-notes"
    notes.mkdir(parents=True, exist_ok=True)
    (notes / ".gitkeep").touch()


def test_valid_seed_passes(tmp_repo, minimal_manifest):
    """A complete, consistent seed should pass validation."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    write_valid_seed(tmp_repo, minimal_manifest)

    from validate_seed import validate
    issues = validate(str(tmp_repo))
    assert issues == [], f"Expected no issues, got: {issues}"


def test_missing_domain_file_fails(tmp_repo, minimal_manifest):
    """If a route references a domain_file that doesn't exist, validation fails."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    write_valid_seed(tmp_repo, minimal_manifest)
    # Remove the domain file
    generated = tmp_repo / "agent-memory-seed" / "generated"
    (generated / "domain-automation-control.md").unlink()

    from validate_seed import validate
    issues = validate(str(tmp_repo))
    assert any("domain-automation-control.md" in i for i in issues)


def test_route_in_nav_missing_from_manifest_fails(tmp_repo, minimal_manifest):
    """Route in navigation.md not in manifest routes should fail."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    write_valid_seed(tmp_repo, minimal_manifest)
    generated = tmp_repo / "agent-memory-seed" / "generated"

    # Add extra route to navigation.md not in manifest
    nav = (generated / "navigation.md").read_text()
    nav += "\n### route_id: ghost-route\ndomain_id: x\ndomain_file: missing.md\n"
    (generated / "navigation.md").write_text(nav)

    from validate_seed import validate
    issues = validate(str(tmp_repo))
    assert any("ghost-route" in i for i in issues)


def test_agent_notes_not_modified_passes(tmp_repo, minimal_manifest):
    """agent-notes/ can have content — validation only checks generated/."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    write_valid_seed(tmp_repo, minimal_manifest)
    # Add a file to agent-notes — should be fine
    notes = tmp_repo / "agent-memory-seed" / "agent-notes"
    (notes / "qa-patterns.md").write_text("# Q&A Patterns\n")

    from validate_seed import validate
    issues = validate(str(tmp_repo))
    assert issues == []


def test_missing_section_in_depends_on_fails(tmp_repo, minimal_manifest):
    """output depends_on_sections referencing a missing section should fail."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    # Add output with nonexistent section
    manifest = json.loads(json.dumps(minimal_manifest))
    manifest["outputs"]["navigation.md"]["depends_on_sections"] = ["hooks.md::nonexistent-section"]
    write_valid_seed(tmp_repo, manifest)

    from validate_seed import validate
    issues = validate(str(tmp_repo))
    assert any("nonexistent-section" in i for i in issues)


def test_out_of_scope_file_modification_fails(tmp_repo, minimal_manifest):
    """Files modified outside agent-memory-seed/generated/ should fail validation."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    write_valid_seed(tmp_repo, minimal_manifest)

    from validate_seed import validate
    # Pass an explicit list of changed files that includes an out-of-scope path
    changed_files = ["docs/hooks.md", "agent-memory-seed/generated/navigation.md"]
    issues = validate(str(tmp_repo), changed_files=changed_files)
    assert any("out-of-scope" in i or "docs/hooks.md" in i for i in issues)


def test_route_rename_detected(tmp_repo, minimal_manifest):
    """A route_id disappearing from prior manifest while a new one appears should flag as possible rename."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    write_valid_seed(tmp_repo, minimal_manifest)

    # Simulate a rename: prior manifest had 'configure-hooks', new manifest has 'setup-hooks'
    new_manifest = json.loads(json.dumps(minimal_manifest))
    new_manifest["routes"]["setup-hooks"] = new_manifest["routes"].pop("configure-hooks")
    generated = tmp_repo / "agent-memory-seed" / "generated"
    (generated / "seed_manifest.json").write_text(json.dumps(new_manifest))

    # Update navigation.md to match new route_id
    nav = (generated / "navigation.md").read_text()
    nav = nav.replace("configure-hooks", "setup-hooks")
    (generated / "navigation.md").write_text(nav)

    from validate_seed import validate
    issues = validate(str(tmp_repo), prior_route_ids=set(minimal_manifest["routes"].keys()))
    assert any("rename" in i.lower() or "setup-hooks" in i for i in issues)
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
python -m pytest tests/test_validate_seed.py -v 2>&1 | head -20
```

Expected: `ModuleNotFoundError` for `validate_seed`.

- [ ] **Step 3: Implement validate_seed.py**

Create `scripts/validate_seed.py`:

```python
#!/usr/bin/env python3
"""
Validate seed output after Codex rebuild.

Checks:
1. No files modified outside agent-memory-seed/generated/ (via changed_files param or git diff)
2. All route_ids in navigation.md exist in manifest routes
3. All domain_file references in routes resolve to files in generated/
4. All depends_on_sections in outputs reference sections that exist in source_docs
5. No route IDs were silently renamed (compare against prior_route_ids)

Exit 0 = valid. Exit 1 = issues found (printed to stdout).

Usage: python scripts/validate_seed.py
"""

import json
import re
import subprocess
import sys
from pathlib import Path


def get_changed_files(repo_root: str) -> list[str]:
    """Return list of files changed vs HEAD using git diff --name-only."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True, text=True, cwd=repo_root
        )
        return [f.strip() for f in result.stdout.splitlines() if f.strip()]
    except Exception:
        return []


def get_prior_route_ids(repo_root: str) -> set[str]:
    """Return route_ids from HEAD's seed_manifest.json (before Codex ran)."""
    try:
        result = subprocess.run(
            ["git", "show", "HEAD:agent-memory-seed/generated/seed_manifest.json"],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode == 0:
            prior = json.loads(result.stdout)
            return set(prior.get("routes", {}).keys())
    except Exception:
        pass
    return set()


def validate(
    repo_root: str,
    changed_files: list[str] | None = None,
    prior_route_ids: set[str] | None = None,
) -> list[str]:
    """
    Run all validation checks. Returns list of issue strings (empty = valid).

    Args:
        repo_root: Path to repository root.
        changed_files: Optional explicit list of changed file paths (relative to repo root).
                       If None, determined via git diff --name-only HEAD.
        prior_route_ids: Optional set of route_ids from before the rebuild.
                         If None, loaded from HEAD's seed_manifest.json via git show.
    """
    root = Path(repo_root)
    generated = root / "agent-memory-seed" / "generated"
    issues = []

    # Check 1: No files modified outside agent-memory-seed/generated/
    if changed_files is None:
        changed_files = get_changed_files(repo_root)
    allowed_prefix = "agent-memory-seed/generated/"
    for f in changed_files:
        if not f.startswith(allowed_prefix):
            issues.append(
                f"out-of-scope modification: '{f}' is outside '{allowed_prefix}'"
            )

    # Load manifest
    manifest_path = generated / "seed_manifest.json"
    if not manifest_path.exists():
        return issues + ["seed_manifest.json not found in agent-memory-seed/generated/"]

    manifest = json.loads(manifest_path.read_text())
    routes = manifest.get("routes", {})
    source_docs = manifest.get("source_docs", {})
    outputs = manifest.get("outputs", {})

    # Check 2: All route_ids in navigation.md exist in manifest routes
    nav_path = generated / "navigation.md"
    if nav_path.exists():
        nav_content = nav_path.read_text()
        nav_route_ids = set(re.findall(r'### route_id: (\S+)', nav_content))
        manifest_route_ids = set(routes.keys())

        for rid in nav_route_ids - manifest_route_ids:
            issues.append(f"route_id '{rid}' in navigation.md not found in manifest routes")

        for rid in manifest_route_ids - nav_route_ids:
            issues.append(f"route_id '{rid}' in manifest routes not found in navigation.md")
    else:
        issues.append("navigation.md not found in agent-memory-seed/generated/")

    # Check 3: All domain_file references in routes resolve to real files
    for route_id, route in routes.items():
        domain_file = route.get("domain_file")
        if domain_file and not (generated / domain_file).exists():
            issues.append(
                f"route '{route_id}' references domain_file '{domain_file}' which does not exist"
            )

    # Check 4: All depends_on_sections in outputs reference existing sections
    for output_file, output_meta in outputs.items():
        for section_ref in output_meta.get("depends_on_sections", []):
            parts = section_ref.split("::")
            if len(parts) != 2:
                issues.append(f"Invalid section ref '{section_ref}' in outputs['{output_file}']")
                continue
            doc_name, section_id = parts
            if doc_name not in source_docs:
                issues.append(
                    f"outputs['{output_file}'] depends on '{doc_name}' not in source_docs"
                )
            elif section_id not in source_docs[doc_name].get("sections", {}):
                issues.append(
                    f"outputs['{output_file}'] depends on section '{section_id}' "
                    f"not found in source_docs['{doc_name}'].sections"
                )

    # Check 5: No route IDs were silently renamed
    if prior_route_ids is None:
        prior_route_ids = get_prior_route_ids(repo_root)
    if prior_route_ids:
        current_route_ids = set(routes.keys())
        removed = prior_route_ids - current_route_ids
        added = current_route_ids - prior_route_ids
        # If routes were both removed and added, flag as possible renames
        if removed and added:
            issues.append(
                f"possible route rename(s): removed={sorted(removed)}, "
                f"added={sorted(added)} — preserved route_ids are required; "
                f"use new IDs only for genuinely new routes"
            )

    return issues


def main():
    repo_root = Path(__file__).parent.parent
    issues = validate(str(repo_root))

    if issues:
        print("Seed validation FAILED:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("Seed validation PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests — all should pass**

```bash
python -m pytest tests/test_validate_seed.py -v
```

Expected: all 7 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/validate_seed.py tests/test_validate_seed.py
git commit -m "feat: add validate_seed.py with tests"
```

---

### Task 13: bump_version.py (TDD)

`bump_version.py` increments the patch version in `plugin.json` and prepends a CHANGELOG entry. Only runs when `git diff` shows generated files changed.

- [ ] **Step 1: Write failing tests**

Create `tests/test_bump_version.py`:

```python
"""Tests for bump_version.py."""
import json
import pytest
from pathlib import Path


def test_patch_version_incremented(tmp_repo):
    """bump_version increments the patch field in plugin.json."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    plugin_json = tmp_repo / ".claude-plugin" / "plugin.json"
    plugin_json.parent.mkdir(parents=True)
    plugin_json.write_text(json.dumps({"name": "claude-audit", "version": "1.1.1"}))

    changelog = tmp_repo / "CHANGELOG.md"
    changelog.write_text("# Changelog\n\n## [1.1.1] — 2026-03-01\n\n- Previous entry\n")

    from bump_version import bump
    bump(str(tmp_repo), changed_docs=["hooks.md"])

    updated = json.loads(plugin_json.read_text())
    assert updated["version"] == "1.1.2"


def test_changelog_entry_prepended(tmp_repo):
    """bump_version prepends a new CHANGELOG entry above the previous one."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    plugin_json = tmp_repo / ".claude-plugin" / "plugin.json"
    plugin_json.parent.mkdir(parents=True)
    plugin_json.write_text(json.dumps({"name": "claude-audit", "version": "1.1.1"}))

    changelog = tmp_repo / "CHANGELOG.md"
    changelog.write_text("# Changelog\n\n## [1.1.1] — 2026-03-01\n\n- Previous\n")

    from bump_version import bump
    bump(str(tmp_repo), changed_docs=["hooks.md", "skills.md"])

    content = changelog.read_text()
    assert "## [1.1.2]" in content
    assert "hooks.md" in content
    assert "skills.md" in content
    # New entry should come before old entry
    assert content.index("1.1.2") < content.index("1.1.1")


def test_no_change_no_bump(tmp_repo):
    """If changed_docs is empty, version should not be bumped."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    plugin_json = tmp_repo / ".claude-plugin" / "plugin.json"
    plugin_json.parent.mkdir(parents=True)
    plugin_json.write_text(json.dumps({"name": "claude-audit", "version": "1.1.1"}))

    changelog = tmp_repo / "CHANGELOG.md"
    changelog.write_text("# Changelog\n\n## [1.1.1] — 2026-03-01\n")

    from bump_version import bump
    bump(str(tmp_repo), changed_docs=[])

    updated = json.loads(plugin_json.read_text())
    assert updated["version"] == "1.1.1"
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
python -m pytest tests/test_bump_version.py -v 2>&1 | head -20
```

Expected: `ModuleNotFoundError` for `bump_version`.

- [ ] **Step 3: Implement bump_version.py**

Create `scripts/bump_version.py`:

```python
#!/usr/bin/env python3
"""
Bump the patch version in plugin.json and prepend a CHANGELOG entry.

Only bumps if there are actual changed docs (passed via CHANGED_DOCS env var).

Usage: python scripts/bump_version.py
       CHANGED_DOCS=hooks.md,skills.md python scripts/bump_version.py
"""

import json
import os
import sys
from datetime import date
from pathlib import Path


def bump(repo_root: str, changed_docs: list[str]) -> None:
    """
    Increment patch version and update CHANGELOG. No-op if changed_docs is empty.
    """
    if not changed_docs:
        print("No changed docs — skipping version bump")
        return

    root = Path(repo_root)
    plugin_json_path = root / ".claude-plugin" / "plugin.json"
    changelog_path = root / "CHANGELOG.md"

    # Load and bump version
    plugin = json.loads(plugin_json_path.read_text())
    old_version = plugin["version"]
    version_parts = plugin["version"].split(".")
    version_parts[2] = str(int(version_parts[2]) + 1)
    new_version = ".".join(version_parts)
    plugin["version"] = new_version
    plugin_json_path.write_text(json.dumps(plugin, indent=2) + "\n")

    # Prepend CHANGELOG entry
    today = date.today().strftime("%Y-%m-%d")
    docs_list = "\n".join(f"  - {doc}" for doc in sorted(changed_docs))
    new_entry = (
        f"## [{new_version}] — {today}\n\n"
        f"### Changed\n"
        f"- Auto-rebuilt knowledge seed from updated docs:\n"
        f"{docs_list}\n\n"
        f"---\n\n"
    )

    existing = changelog_path.read_text()
    # Insert after the first line (the # Changelog header)
    lines = existing.split("\n", 2)
    if len(lines) >= 2:
        updated = lines[0] + "\n\n" + new_entry + ("\n".join(lines[1:])).lstrip("\n")
    else:
        updated = existing + "\n" + new_entry

    changelog_path.write_text(updated)
    print(f"Bumped version {old_version} -> {new_version}")


def main():
    repo_root = Path(__file__).parent.parent
    changed_docs_env = os.environ.get("CHANGED_DOCS", "")
    changed_docs = [d.strip() for d in changed_docs_env.split(",") if d.strip()]
    bump(str(repo_root), changed_docs)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests — all should pass**

```bash
python -m pytest tests/test_bump_version.py -v
```

Expected: all 3 tests PASS.

- [ ] **Step 5: Run full test suite**

```bash
python -m pytest tests/ -v
```

Expected: all 16 tests PASS.

- [ ] **Step 6: Update requirements.txt**

Modify `scripts/requirements.txt`:

```
requests==2.32.4
openai>=1.0.0
```

- [ ] **Step 7: Commit**

```bash
git add scripts/bump_version.py tests/test_bump_version.py scripts/requirements.txt
git commit -m "feat: add bump_version.py with tests; add openai to requirements"
```

---

## Chunk 3: GitHub Actions + Codex Prompt

**Files:**
- Modify: `.github/workflows/update-docs.yml`
- Create: `.github/prompts/build-seed.md`

### Task 14: Update update-docs.yml

- [ ] **Step 1: Read current workflow**

```bash
cat .github/workflows/update-docs.yml
```

- [ ] **Step 2: Add fetch-depth: 2 to checkout step**

In `.github/workflows/update-docs.yml`, find the checkout step and add `fetch-depth: 2`:

```yaml
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        ref: main
        fetch-depth: 2
```

- [ ] **Step 3: Add four new steps after "Fetch latest documentation"**

Add after the `Fetch latest documentation` step (before `Check for changes`):

```yaml
    - name: Check seed significance
      id: seed-check
      run: python scripts/check_significance.py >> $GITHUB_OUTPUT

    - name: Rebuild seed with Codex
      if: steps.seed-check.outputs.rebuild == 'true'
      id: codex-rebuild
      continue-on-error: true
      uses: openai/codex-action@v1
      with:
        openai-api-key: ${{ secrets.OPENAI_API_KEY }}
        prompt-file: .github/prompts/build-seed.md
        output-file: codex-seed-output.md
        safety-strategy: drop-sudo
        sandbox: workspace-write

    - name: Validate seed output
      if: steps.seed-check.outputs.rebuild == 'true' && steps.codex-rebuild.outcome == 'success'
      id: seed-validate
      run: python scripts/validate_seed.py

    - name: Bump version if seed changed
      if: steps.seed-validate.outcome == 'success'
      env:
        CHANGED_DOCS: ${{ steps.seed-check.outputs.changed_docs }}
      run: python scripts/bump_version.py

    - name: Discard seed changes on failure
      if: steps.codex-rebuild.outcome == 'failure' || steps.seed-validate.outcome == 'failure'
      run: |
        git checkout -- agent-memory-seed/ || true
        git checkout -- .claude-plugin/plugin.json || true
        git checkout -- CHANGELOG.md || true
        git clean -fd agent-memory-seed/ || true

    - name: Create issue on seed failure
      if: steps.codex-rebuild.outcome == 'failure' || steps.seed-validate.outcome == 'failure'
      uses: actions/github-script@v7
      with:
        script: |
          const date = new Date().toISOString().split('T')[0];
          await github.rest.issues.create({
            owner: context.repo.owner,
            repo: context.repo.repo,
            title: `Seed rebuild failed - ${date}`,
            body: `Seed rebuild failed on ${date}. Docs updated normally. See [workflow run](${context.serverUrl}/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}) for details.`,
            labels: ['bug', 'automation']
          })
```

- [ ] **Step 4: Update the "Check for changes" step to also stage seed files when valid**

Find the `Check for changes` step and update it to stage seed files when the rebuild was valid:

```yaml
    - name: Check for changes
      id: verify-changed-files
      run: |
        git add -A docs/
        if [ "${{ steps.seed-validate.outcome }}" = "success" ]; then
          git add -A agent-memory-seed/generated/
          git add .claude-plugin/plugin.json CHANGELOG.md || true
        fi
        git diff --cached --exit-code || echo "changed=true" >> $GITHUB_OUTPUT
```

- [ ] **Step 5: Validate YAML syntax**

```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/update-docs.yml'))" && echo "YAML valid"
```

Expected: `YAML valid`

- [ ] **Step 6: Commit**

```bash
git add .github/workflows/update-docs.yml
git commit -m "feat: add seed rebuild steps to update-docs.yml"
```

---

### Task 15: Create .github/prompts/build-seed.md

This is the prompt Codex receives when rebuilding the seed. It must be a strict contract.

- [ ] **Step 1: Create the prompts directory**

```bash
mkdir -p .github/prompts
```

- [ ] **Step 2: Create build-seed.md**

Create `.github/prompts/build-seed.md`:

````markdown
# Seed Rebuild Task

You are regenerating the Claude Code knowledge seed for the `claude-audit` plugin.

## Your job

Update only the seed files affected by the provided doc changes. Do not regenerate files that don't need updating.

## Inputs available to you

Read the following before starting:

1. **`agent-memory-seed/generated/seed_manifest.json`** — current manifest; your source of truth for routes, sections, and output dependencies. The `source_docs[filename].headings` arrays give you the **old heading trees** (the headings as they existed before this doc update).

2. **`agent-memory-seed/generated/navigation.md`** — current navigation; update only affected routes.

3. **Any `agent-memory-seed/generated/domain-*.md` files** whose `depends_on_sections` overlap with changed sections.

4. **The changed docs in `docs/`** — read each doc that appears in the diff to get its **new heading tree** (extract all `#`-prefixed headings). Compare against the old heading tree from `seed_manifest.json` to identify structural changes.

5. **The git diff** — run `git diff HEAD~1 -U0 -- docs/` to get the unified diff. For each changed doc, produce a brief per-doc diff summary:
   - Which headings were added, removed, or renamed (compare old vs new heading trees)
   - Approximate lines changed per section
   Use this summary to decide which routes and domain files need updating.

## Domain taxonomy

| domain_id | domain_file | Covers |
|---|---|---|
| foundation | domain-foundation.md | How Claude Code works, auth, providers, data usage, compliance |
| configuration-persistence | domain-configuration-persistence.md | CLAUDE.md, memory, settings, env vars |
| automation-control | domain-automation-control.md | Hooks, scheduled tasks |
| extension-capability | domain-extension-capability.md | Skills, subagents, MCP, plugins, agent teams |
| access-control-safety | domain-access-control-safety.md | Permissions, sandboxing, security, network |
| effective-interaction | domain-effective-interaction.md | Best practices, commands, IDE integrations, headless, costs |

## Rules

1. **Route by user intent, not doc title.** Each route should reflect what a user would ask, not what a doc is named.
2. **Preserve existing `route_id`s.** Do not rename a route. Add new routes if needed; remove obsolete ones.
3. **One `primary_doc` per route, at most one `secondary_doc`.** If a route needs more, redesign the route boundary.
4. **Domain files answer ~60-70% of questions without opening source docs.** Keep them concise and decisive.
5. **Do not touch `agent-memory-seed/agent-notes/`.** That directory is agent-owned.
6. **Rebuild only affected outputs.** Check `seed_manifest.json` `outputs[file].depends_on_sections` to know what to rebuild.
7. **Update `seed_manifest.json`** to reflect new section hashes if headings changed.
8. **`navigation.md` must be generated from the manifest's `routes` object** — they must stay in sync.

## Output format

Return complete replacement contents for only the files you changed. Use this exact delimiter format:

```
=== BEGIN FILE: agent-memory-seed/generated/navigation.md ===
<full contents>
=== END FILE ===

=== BEGIN FILE: agent-memory-seed/generated/domain-automation-control.md ===
<full contents>
=== END FILE ===

=== BEGIN FILE: agent-memory-seed/generated/seed_manifest.json ===
<full contents>
=== END FILE ===
```

Do not output any other text outside the file blocks.
````

- [ ] **Step 3: Commit**

```bash
git add .github/prompts/build-seed.md
git commit -m "feat: add Codex build-seed.md prompt"
```

---

## Chunk 4: Agent + Skill Updates + Version Bump

**Files:**
- Modify: `agents/claude-code-expert.md`
- Modify: `skills/ask-claude-code/SKILL.md`
- Modify: `.claude-plugin/plugin.json`
- Modify: `CHANGELOG.md`

### Task 16: Update agents/claude-code-expert.md

- [ ] **Step 1: Read current agent file**

```bash
cat agents/claude-code-expert.md
```

- [ ] **Step 2: Replace bootstrap section**

Find the `## Memory Management` section and replace it entirely:

```markdown
## Memory Management

Your memory lives at `~/.claude/agent-memory/claude-audit-claude-code-expert/`:

```
~/.claude/agent-memory/claude-audit-claude-code-expert/
  MEMORY.md                        ← index + seed_version
  generated/                       ← copied from plugin on install/update
    navigation.md                  ← intent router
    domain-*.md (6 files)          ← domain knowledge summaries
    seed_manifest.json             ← section hashes and route metadata
  agent-notes/                     ← your writable notes, never overwritten by scripts
    qa-patterns.md                 ← patterns worth remembering (see memory rule below)
```

### Bootstrap (first invocation)

On first invocation, `generated/` will not exist. Do this once:

1. Read `~/.claude/plugins/installed_plugins.json`
2. Extract `installPath` for the key `"claude-audit@ccode-personal-plugins"`
3. Copy `installPath/agent-memory-seed/generated/` → `~/.claude/agent-memory/claude-audit-claude-code-expert/generated/`
4. Create `agent-notes/` if missing — **never overwrite it**
5. Write `seed_version` from `generated/seed_manifest.json` into `MEMORY.md`

**If `installed_plugins.json` is missing, the key is not found, or `seed_manifest.json` is unreadable:** continue using the locally copied `generated/` seed if it already exists. Preserve `agent-notes/`. Do not fall back to reading all docs.

### Seed version check (subsequent invocations)

**Frequency:** Check on every invocation before answering any question. The check is two file reads and a string comparison — negligible cost.

On each invocation after bootstrap:

1. Read `seed_version` from your local `generated/seed_manifest.json`
2. Read `seed_version` from `installPath/agent-memory-seed/generated/seed_manifest.json`
3. If plugin seed is newer: re-copy `generated/` only — **never touch `agent-notes/`**
4. Update `seed_version` in `MEMORY.md`
```

- [ ] **Step 3: Add Q&A Mode section after bootstrap**

Add a new section after Memory Management:

```markdown
## Q&A Mode

When answering a question about Claude Code:

1. Read `generated/navigation.md` → match question to a `route_id` using `intent`, `match` phrases, and `strong_terms`
2. Read the matched `domain_file`
3. **If `answer_from_domain_if` applies:** answer from the domain file. Cite the route's `primary_doc` filename as the authoritative source without quoting it directly.
4. **If `read_source_docs_if` applies:** read `primary_doc` from `installPath/docs/`. Read `secondary_doc` only if still needed. Cite the specific doc(s) read with direct reference to the relevant section.

**Fallback (no confident match):**
- Use `strong_terms` from all routes to select the best candidate
- If still ambiguous: read `primary_doc` for the top 2 candidate routes
- If ambiguity persists after reading both: return both candidate answers explicitly, state the uncertainty, and cite all source docs consulted

**Memory rule — `agent-notes/qa-patterns.md`:**

Save a note **only if** it would improve 3 or more future questions. Format each note as:

```
## <short label>
question shape: <what the user typically asks>
answer rule: <the stable answer or decision heuristic>
docs: [<doc1.md>, <doc2.md>]
caveat: <edge cases, version constraints, or ambiguities>
```

Do not save: one-off facts, version details, material already covered in the generated seed.
```

- [ ] **Step 4: Verify file structure looks correct**

```bash
grep -n "^##" agents/claude-code-expert.md
```

Expected sections: `## Your Role`, `## Memory Management`, `## Q&A Mode`, `## Claude Code Primitives Reference`, `## Analysis Approach`, `## Constraint`

- [ ] **Step 5: Commit**

```bash
git add agents/claude-code-expert.md
git commit -m "feat: update claude-code-expert with seed bootstrap and Q&A mode"
```

---

### Task 17: Update skills/ask-claude-code/SKILL.md

- [ ] **Step 1: Read current file**

```bash
cat skills/ask-claude-code/SKILL.md
```

- [ ] **Step 2: Replace with updated version**

Write `skills/ask-claude-code/SKILL.md`:

```markdown
---
name: ask-claude-code
description: Ask any question about Claude Code — CLAUDE.md, memory, hooks, skills, agents, plugins, MCP, settings, permissions, or best practices. Answers are backed by official documentation. Usage: /ask-claude-code <your question>
---

The user has a question about Claude Code. Dispatch the `claude-audit:claude-code-expert` agent to answer it.

Pass to the agent verbatim:

```
Mode: Q&A
Question: <user's exact question>
```

Relay the agent's full response to the user without modification.
```

- [ ] **Step 3: Commit**

```bash
git add skills/ask-claude-code/SKILL.md
git commit -m "feat: update ask-claude-code skill to dispatch Q&A mode"
```

---

### Task 18: Bump version to 1.2.0 and update CHANGELOG

This is a minor version bump (new features: seed system, ask-claude-code skill, Q&A mode).

- [ ] **Step 1: Update plugin.json**

Edit `.claude-plugin/plugin.json`:

```json
{
  "name": "claude-audit",
  "version": "1.2.0",
  "description": "AI-readiness audit for any Claude Code project. Analyzes CLAUDE.md, hooks, skills, agents, MCP setup and produces a structured improvement report with prioritized actions.",
  "author": {
    "name": "mrkhachaturov",
    "email": ""
  }
}
```

- [ ] **Step 2: Prepend CHANGELOG entry**

Add at the top of the changelog entries in `CHANGELOG.md`:

```markdown
## [1.2.0] — 2026-03-14

### Added
- `agent-memory-seed/` — pre-built knowledge seed that ships with the plugin; agents bootstrap from seed instead of reading all docs
- `agent-memory-seed/generated/navigation.md` — intent-based routing table (12 routes across 6 domains)
- `agent-memory-seed/generated/domain-*.md` — 6 domain knowledge files covering all Claude Code docs
- `agent-memory-seed/generated/seed_manifest.json` — section-level hashes enabling incremental Codex rebuilds
- `scripts/check_significance.py` — determines if doc changes warrant a seed rebuild
- `scripts/validate_seed.py` — validates Codex seed output before committing
- `scripts/bump_version.py` — auto-bumps patch version when seed rebuilds
- `.github/prompts/build-seed.md` — Codex prompt for incremental seed regeneration

### Changed
- `skills/ask-claude-code/SKILL.md`: updated skill — now dispatches Q&A mode backed by domain seed files
- `agents/claude-code-expert.md`: replaced 65-doc bootstrap with instant seed copy; added Q&A mode with intent routing and selective memory rule
- `.github/workflows/update-docs.yml`: added seed rebuild pipeline (significance check → Codex → validation → version bump)

---
```

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/plugin.json CHANGELOG.md
git commit -m "release: v1.2.0 — knowledge seed system"
```

- [ ] **Step 4: Verify final state**

```bash
python -m pytest tests/ -v
```

Expected: all 14 tests PASS.

```bash
python scripts/validate_seed.py
```

Expected: `Seed validation PASSED`

```bash
git log --oneline -8
```

Expected: clean linear history with descriptive commit messages.
