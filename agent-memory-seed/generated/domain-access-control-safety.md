# Domain: Access Control & Safety

## What this domain covers
Controlling what Claude Code can access and do: permission modes, tool allow/deny rules, sandboxing, network configuration, and security best practices.

## Decision rules
- Configure permissions in `settings.json` under the `permissions` key
- Use permission rules to allow safe commands and block dangerous ones
- Use sandboxing when Claude needs internet access or file system isolation
- Use `sandbox.filesystem.allowRead` to re-allow specific paths inside denied read regions
- In project settings, `allowRead: ["."]` resolves to project root; in user settings it resolves to `~/.claude`
- Use network config for corporate proxy or certificate requirements
- For Team/Enterprise remote and web session access, use Claude Code admin settings (not managed permission keys)

## Fast answers
- **Permission modes:** `default` (prompt for risky), `acceptEdits` (auto-approve edits), `plan` (read-only planning), `auto` (classifier-guarded autonomy), `dontAsk` (deny unless pre-allowed), `bypassPermissions` (skip checks except protected-directory writes)
- **Where do permissions live?** `.claude/settings.json` or `~/.claude/settings.json` under `permissions`
- **Can I allow specific bash commands?** Yes — `allowedTools` with bash command patterns
- **Can I block Claude from editing certain files?** Yes — `denyTools` or path-based rules
- **How does auto mode decide?** Rules resolve first (`deny` -> `ask` -> `allow`), then safe local reads/edits auto-approve, then a classifier evaluates remaining actions
- **Where do auto mode rules live?** `autoMode` is read from user/local/managed settings; not from shared project `.claude/settings.json`
- **Can admins disable risky modes?** Yes — set `permissions.disableBypassPermissionsMode` and/or `disableAutoMode` to `"disable"` (strongest in managed settings)
- **Can I deny broad reads but allow the workspace?** Yes — combine `sandbox.filesystem.denyRead` with `sandbox.filesystem.allowRead`
- **Does bypass mode still prompt anywhere?** Yes — writes to `.git`, `.claude`, `.vscode`, and `.idea` still prompt; `.claude/commands`, `.claude/agents`, and `.claude/skills` are exempt
- **Does `Read(...)` deny block `cat` in Bash?** No — Read/Edit denies apply to Claude file tools; use sandboxing for OS-level path enforcement
- **How do Read/Edit patterns work on Windows?** Paths are normalized to POSIX form (for example `C:\\Users\\alice` -> `/c/Users/alice`)
- **Do hook approvals override deny rules?** No — hooks can skip interactive prompts, but deny/ask rules still take precedence
- **Can managed `permissions` disable Remote Control or web sessions?** No — admins control those in Claude Code admin settings
- **Does sandboxing cover every Claude tool boundary?** No — sandboxing isolates Bash subprocesses; Read/Edit/Write permission behavior and Desktop computer-use controls are separate boundaries

## Fast comparisons
- **allowedTools vs denyTools:** Allow is a whitelist; deny is a blacklist; deny takes precedence
- **Project permissions vs user permissions:** Project overrides user for that project
- **Permission prompt vs bypassPermissions:** Prompt asks each time; bypass skips most prompts but still protects critical config/repo directories
- **auto vs bypassPermissions:** Both reduce prompts; `auto` applies background classifier checks, `bypassPermissions` skips permission safety checks entirely

## Common tasks
- "Allow Claude to run npm test without asking" → allowedTools with bash pattern
- "Prevent Claude from editing .env files" → denyTools with file path pattern
- "Run Claude in CI without prompts" → bypassPermissions mode with restricted allowedTools
- "Isolate Claude's network access" → sandboxing.md
- "Deny broad reads but allow repo files" → use `denyRead` with `allowRead: ["."]` in project settings

## When you must read source docs
- Exact mode switching behavior per surface (CLI/VS Code/Desktop/Web)
- Auto mode eligibility limits (plan/model/provider/admin gating)
- Auto mode fallback thresholds and non-interactive abort behavior
- Auto mode classifier configuration (`environment`, `allow`, `soft_deny`) and override risks
- Exact permission rule syntax and pattern matching
- Read/Edit deny limitations for Bash subprocesses
- What sandboxing does and does not cover (Bash sandbox vs built-in file tools and Desktop computer use)
- Windows Read/Edit pattern syntax examples (`//c/**`, `//**`)
- Full list of tool names for allow/deny rules
- Sandboxing setup and limitations
- Network proxy configuration syntax

## Source map
- permission-modes.md
- permissions.md
- settings.md
- server-managed-settings.md
- sandboxing.md
- security.md
- network-config.md
- llm-gateway.md
