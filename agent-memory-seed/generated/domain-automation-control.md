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
- **Hook events (common):** `PreToolUse`, `PostToolUse`, `Notification`, `Stop`, `StopFailure`, `SubagentStop`; newer lifecycle events include `PostCompact`, `Elicitation`, and `ElicitationResult` — see hooks.md for the full list
- **Can hooks block Claude?** Yes — `PreToolUse` hooks that exit non-zero can block the tool call
- **Can hooks auto-approve permission prompts?** Yes — `PermissionRequest` hooks can return JSON `decision.behavior: "allow"` and optionally `updatedPermissions` entries, but deny/ask permission rules still apply
- **When do Stop vs StopFailure run?** `Stop` runs when Claude finishes normally; API errors fire `StopFailure` instead and ignore hook output/exit code
- **Where do hooks live?** `.claude/settings.json` under the `hooks` key
- **Plugin hook paths:** Use `${CLAUDE_PLUGIN_ROOT}` for bundled scripts and `${CLAUDE_PLUGIN_DATA}` for dependencies/state that should survive plugin updates

## Fast comparisons
- **Hooks vs skills:** Hooks run automatically on events; skills run when explicitly invoked
- **Hooks vs CLAUDE.md:** Hooks are deterministic shell commands; CLAUDE.md is natural language instructions
- **Hooks vs scheduled tasks:** Hooks respond to tool events; scheduled tasks run on time intervals
- **PreToolUse vs PostToolUse:** Pre can block/modify; Post observes and reacts
- **PreCompact vs PostCompact:** Pre runs before compaction; Post runs after compaction with access to the compact summary

## Common tasks
- "Auto-format code after every file write" → PostToolUse hook on Write tool
- "Block dangerous shell commands" → PreToolUse hook on Bash tool
- "Get notified when Claude finishes a task" → Notification hook
- "Run linting after edits" → PostToolUse hook on Edit/Write tools
- "Auto-approve only plan-exit prompts" → PermissionRequest hook matched on `ExitPlanMode`
- "Auto-handle MCP auth/input prompts" → Elicitation hook (or validate/override with ElicitationResult)
- "Alert on API failures (rate limit/auth/server)" → StopFailure hook matched by error type
- "Run a script every night" → scheduled-tasks.md

## When you must read source docs
- Exact hook matcher syntax (tool name patterns, regex)
- Matcher target fields for InstructionsLoaded (`load_reason`), Elicitation, ElicitationResult, and StopFailure
- Blocking hook exit code semantics
- PermissionRequest decision output fields (including `updatedPermissions` entry types and destinations)
- Full list of hookable events and their payloads
- Scheduled task cron expression format and limits

## Source map
- hooks.md
- hooks-guide.md
- scheduled-tasks.md
