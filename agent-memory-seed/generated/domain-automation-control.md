# Domain: Automation & Control

## What this domain covers
Deterministic automation triggered at specific lifecycle points: hooks (shell commands run on tool events) and scheduled tasks (recurring runs in-session, on Desktop, or in cloud infrastructure).

## Decision rules
- Use hooks when you need to run code **automatically** at a specific tool lifecycle point
- Use hooks for formatting, linting, notifications, blocking unsafe operations
- Use `/loop` for lightweight recurring checks that only need to run while the current CLI session is open
- Use Desktop scheduled tasks for recurring work that needs local files/tools
- Use cloud scheduled tasks (`/schedule` or web UI) for unattended recurring work that must continue when your machine is off
- Use CLAUDE.md instructions instead of hooks when the behavior should be context-dependent

## Fast answers
- **What are hooks?** Shell commands in settings.json that run before/after specific Claude tool uses
- **Hook shell selection:** command hooks support `shell: "bash"` (default) or `shell: "powershell"`; PowerShell hook execution does not require `CLAUDE_CODE_USE_POWERSHELL_TOOL`
- **Hook events (common):** `PreToolUse`, `PostToolUse`, `Notification`, `Stop`, `StopFailure`, `SubagentStop`; newer lifecycle events include `PostCompact`, `Elicitation`, `ElicitationResult`, `CwdChanged`, and `FileChanged` — see hooks.md for the full list
- **Hook payload `permission_mode`:** may be `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, or `bypassPermissions` (event-dependent)
- **SessionEnd `reason` values:** include `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, and `other`
- **Can hooks block Claude?** Yes — `PreToolUse` hooks that exit non-zero can block the tool call
- **Can hooks auto-approve permission prompts?** Yes — `PermissionRequest` hooks can return JSON `decision.behavior: "allow"` and optionally `updatedPermissions` entries, but deny/ask permission rules still apply
- **WorktreeCreate return format:** command hooks print the worktree path on stdout; HTTP hooks return `hookSpecificOutput.worktreePath`
- **`CwdChanged` vs `FileChanged`:** `CwdChanged` runs on every directory change (no matcher support); `FileChanged` watches files and uses `matcher` as the filename filter
- **`CLAUDE_ENV_FILE` hook support:** available in `SessionStart`, `CwdChanged`, and `FileChanged` hooks for persisting environment variables into later Bash commands
- **When do Stop vs StopFailure run?** `Stop` runs when Claude finishes normally; API errors fire `StopFailure` instead and ignore hook output/exit code
- **SessionEnd timeout default:** 1.5s via `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS`; applies to exit, `/clear`, and interactive `/resume` session switches
- **Where do hooks live?** `.claude/settings.json` under the `hooks` key
- **Plugin hook paths:** Use `${CLAUDE_PLUGIN_ROOT}` for bundled scripts and `${CLAUDE_PLUGIN_DATA}` for dependencies/state that should survive plugin updates
- **How do I create cloud scheduled tasks?** Use `/schedule` in CLI or create from web/Desktop Schedule UI
- **How do I create session-scoped scheduled tasks?** Use `/loop` for recurring prompts inside the current CLI session

## Fast comparisons
- **Hooks vs skills:** Hooks run automatically on events; skills run when explicitly invoked
- **Hooks vs CLAUDE.md:** Hooks are deterministic shell commands; CLAUDE.md is natural language instructions
- **Hooks vs scheduled tasks:** Hooks respond to tool events; scheduled tasks run on time intervals
- **Cloud vs Desktop scheduled tasks:** Cloud runs on Anthropic-managed infrastructure; Desktop runs on your machine with local file/tool access
- **`/schedule` vs `/loop`:** `/schedule` creates durable cloud tasks; `/loop` creates session-scoped polling in the current CLI process
- **Scheduled tasks vs channels:** Scheduled tasks poll on an interval; channels push events as they happen
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
- "Reload direnv/venv when Claude changes directories or `.env` files" → `CwdChanged`/`FileChanged` hooks that append exports to `CLAUDE_ENV_FILE`
- "Run a quick recurring check while I stay in-session" → scheduled-tasks.md (`/loop`)
- "Run daily reviews even when my machine is off" → web-scheduled-tasks.md (`/schedule`)
- "Run recurring tasks with direct local repo access" → desktop.md (local scheduled tasks)
- "React immediately to CI/webhook/chat events without polling" → channels.md (via MCP channels)

## When you must read source docs
- Exact hook matcher syntax (tool name patterns, regex)
- Command-hook `shell` field behavior and PowerShell limitations
- Matcher target fields for InstructionsLoaded (`load_reason`), Elicitation, ElicitationResult, and StopFailure
- Blocking hook exit code semantics
- PermissionRequest decision output fields (including `updatedPermissions` entry types and destinations)
- Full list of hookable events and their payloads
- WorktreeCreate/WorktreeRemove path return semantics for command vs HTTP hooks
- `CwdChanged`/`FileChanged` payloads and `watchPaths` behavior
- `/schedule` lifecycle and task-management commands (`list`, `update`, `run`)
- Scheduled task cadence options and cloud/desktop/session behavior differences
- Scheduled task cron expression format and limits for session-scoped `/loop` scheduling
- Whether your use case should use polling (`/loop`) or event push (channels)

## Source map
- hooks.md
- hooks-guide.md
- scheduled-tasks.md
- web-scheduled-tasks.md
- desktop.md
- commands.md
- channels.md
