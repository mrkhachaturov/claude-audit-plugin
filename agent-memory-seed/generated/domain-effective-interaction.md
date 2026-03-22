# Domain: Effective Interaction

## What this domain covers
Working well with Claude Code as an agentic tool: prompting strategies, common workflows, built-in slash commands, output configuration, model selection, fast mode, IDE integrations, remote/headless operation, and checkpointing.

## Decision rules
- Use explore-plan-implement workflow for complex or risky tasks
- Use `/clear` to reset context when it gets too large or polluted
- Use headless mode (`claude -p`) with `--bare` for deterministic CI/CD and scripted automation
- Use checkpointing for long tasks where you might want to roll back
- Use Remote Control when you want to continue a local session from browser/mobile while keeping work on your machine

## Fast answers
- **Built-in commands:** `/clear`, `/memory`, `/cost`, `/stats`, `/model`, `/hooks`, `/agents`, `/plugin`, `/feedback`, `/branch` (alias: `/fork`), `/voice`
- **Copy prior responses:** use `/copy [N]` (for example `/copy 2` for the second-latest response)
- **Plan acceptance naming:** accepting a plan auto-names the session unless a name is already set via `--name` or `/rename`
- **How to use a skill:** type `/skill-name` or ask Claude to use it
- **Model selection:** `/model` command or `model` in settings.json
- **Effort controls:** `/effort`, `--effort`, `effortLevel` setting, and `CLAUDE_CODE_EFFORT_LEVEL`; skill/subagent frontmatter can override session effort while active
- **Fast mode:** lower latency, same model, uses extra usage credits on subscription plans
- **Headless mode:** `claude -p "your prompt"` for non-interactive scripted use; add `--bare` to skip local auto-discovery and make runs deterministic
- **Enable Remote Control:** `claude remote-control`, `claude --remote-control`, or `/remote-control`
- **Stay reactive while away:** combine Remote Control with channels to forward Telegram/Discord/webhook events into the live session
- **tmux passthrough requirement:** for notifications and terminal progress updates to reach your outer terminal while inside tmux, set `set -g allow-passthrough on`
- **Verbose toggle behavior:** `Ctrl+O` expands detailed tool output, including MCP read/search calls that are collapsed to one-line summaries by default.
- **Remote session title order:** explicit name flag/command, then `/rename`, then last meaningful message, then first prompt
- **Remote auth/provider limits:** requires claude.ai login; unsupported with API key auth or Bedrock/Vertex/Foundry provider modes
- **Remote Control on Team/Enterprise:** off by default; admin must enable the Remote Control toggle in Claude Code admin settings
- **Remote policy errors:** run `/status` first, then check auth mode (claude.ai OAuth vs API key), org admin Remote Control toggle state (server-side), and org compliance/data-retention policy constraints
- **Status line trust requirement:** `statusLine` commands run only after workspace trust is accepted; otherwise you'll see `statusline skipped · restart to fix`
- **Built-in VS Code IDE MCP server:** extension runs hidden local server `ide` (auto-connected by CLI; not listed in `/mcp`)
- **IDE MCP tools visible to Claude:** `mcp__ide__getDiagnostics` (read-only diagnostics) and `mcp__ide__executeCode` (Jupyter cell execution with VS Code confirmation)
- **Jupyter execution safety:** `mcp__ide__executeCode` always requires a native Quick Pick confirm/cancel in VS Code and fails if notebook/kernel prerequisites are missing

## Fast comparisons
- **Interactive vs headless:** Interactive is conversational; headless is single-shot for automation (prefer `--bare` in scripts)
- **fast mode vs standard:** Fast mode has lower latency; standard may be more thorough on complex tasks
- **`/clear` vs new session:** `/clear` resets context in same session; new session is fully fresh
- **Remote Control vs Claude Code on the web:** Remote Control runs on your machine; web sessions run in Anthropic-managed cloud

## Common tasks
- "Run Claude without interaction" → headless.md
- "Reduce context window usage" → `/clear`, or use subagents
- "Run parallel Claude sessions" → best-practices.md (parallel sessions section)
- "Continue a local session from phone/browser" → remote-control.md
- "Have Claude react to incoming chat/alert events while remote" → channels.md + remote-control.md
- "Fix Remote Control policy/account errors" → remote-control.md (troubleshooting section)
- "Configure Claude for VSCode" → vs-code.md
- "Configure Claude for JetBrains" → jetbrains.md
- "Check token usage and costs" → `/cost` command, monitoring-usage.md
- "Segment telemetry by account/user identity" → monitoring-usage.md (`user.account_uuid`, `user.account_id`, `organization.id`)

## When you must read source docs
- Full list of slash commands and their arguments
- Exact headless mode flags and options
- Output style configuration options
- Status line execution/trust requirements and troubleshooting
- Remote control API details
- Remote Control eligibility and org-policy troubleshooting matrix
- Channels setup and integration with active sessions
- Telemetry attributes and cardinality controls (`OTEL_METRICS_INCLUDE_ACCOUNT_UUID`, `user.account_id`, event-only fields like `prompt.id`)
- VS Code built-in `ide` MCP server behavior and local auth model
- `PreToolUse` allowlist implications for hidden `mcp__ide__*` tools
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
- channels.md
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
