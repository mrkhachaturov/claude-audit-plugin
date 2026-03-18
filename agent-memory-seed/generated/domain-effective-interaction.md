# Domain: Effective Interaction

## What this domain covers
Working well with Claude Code as an agentic tool: prompting strategies, common workflows, built-in slash commands, output configuration, model selection, fast mode, IDE integrations, remote/headless operation, and checkpointing.

## Decision rules
- Use explore-plan-implement workflow for complex or risky tasks
- Use `/clear` to reset context when it gets too large or polluted
- Use headless mode (`claude -p`) for CI/CD and scripted automation
- Use checkpointing for long tasks where you might want to roll back
- Use Remote Control when you want to continue a local session from browser/mobile while keeping work on your machine

## Fast answers
- **Built-in commands:** `/clear`, `/memory`, `/cost`, `/stats`, `/model`, `/hooks`, `/agents`, `/plugin`, `/feedback`, `/branch` (alias: `/fork`), `/voice`
- **Copy prior responses:** use `/copy [N]` (for example `/copy 2` for the second-latest response)
- **Plan acceptance naming:** accepting a plan auto-names the session unless a name is already set via `--name` or `/rename`
- **How to use a skill:** type `/skill-name` or ask Claude to use it
- **Model selection:** `/model` command or `model` in settings.json
- **Fast mode:** lower latency, same model, uses extra usage credits on subscription plans
- **Headless mode:** `claude -p "your prompt"` for non-interactive scripted use
- **Enable Remote Control:** `claude remote-control`, `claude --remote-control`, or `/remote-control`
- **Remote session title order:** explicit name flag/command, then `/rename`, then last meaningful message, then first prompt
- **Remote auth/provider limits:** requires claude.ai login; unsupported with API key auth or Bedrock/Vertex/Foundry provider modes
- **Remote Control on Team/Enterprise:** off by default; admin must enable the Remote Control toggle in Claude Code admin settings
- **Remote policy errors:** check auth mode (claude.ai OAuth vs API key), org admin toggle state, and org compliance/data-retention policy constraints

## Fast comparisons
- **Interactive vs headless:** Interactive is conversational; headless is single-shot for automation
- **fast mode vs standard:** Fast mode has lower latency; standard may be more thorough on complex tasks
- **`/clear` vs new session:** `/clear` resets context in same session; new session is fully fresh
- **Remote Control vs Claude Code on the web:** Remote Control runs on your machine; web sessions run in Anthropic-managed cloud

## Common tasks
- "Run Claude without interaction" → headless.md
- "Reduce context window usage" → `/clear`, or use subagents
- "Run parallel Claude sessions" → best-practices.md (parallel sessions section)
- "Continue a local session from phone/browser" → remote-control.md
- "Fix Remote Control policy/account errors" → remote-control.md (troubleshooting section)
- "Configure Claude for VSCode" → vs-code.md
- "Configure Claude for JetBrains" → jetbrains.md
- "Check token usage and costs" → `/cost` command, monitoring-usage.md

## When you must read source docs
- Full list of slash commands and their arguments
- Exact headless mode flags and options
- Output style configuration options
- Remote control API details
- Remote Control eligibility and org-policy troubleshooting matrix
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
