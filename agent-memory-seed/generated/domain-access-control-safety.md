# Domain: Access Control & Safety

## What this domain covers
Controlling what Claude Code can access and do: permission modes, tool allow/deny rules, sandboxing, network configuration, and security best practices.

## Decision rules
- Configure permissions in `settings.json` under the `permissions` key
- Use permission rules to allow safe commands and block dangerous ones
- Use sandboxing when Claude needs internet access or file system isolation
- Use `sandbox.filesystem.allowRead` to re-allow specific paths inside denied read regions
- Use network config for corporate proxy or certificate requirements

## Fast answers
- **Permission modes:** `default` (prompt for risky), `acceptEdits` (auto-approve edits), `bypassPermissions` (auto-approve all — use with care)
- **Where do permissions live?** `.claude/settings.json` or `~/.claude/settings.json` under `permissions`
- **Can I allow specific bash commands?** Yes — `allowedTools` with bash command patterns
- **Can I block Claude from editing certain files?** Yes — `denyTools` or path-based rules
- **Can I deny broad reads but allow the workspace?** Yes — combine `sandbox.filesystem.denyRead` with `sandbox.filesystem.allowRead`
- **Does `Read(...)` deny block `cat` in Bash?** No — Read/Edit denies apply to Claude file tools; use sandboxing for OS-level path enforcement
- **How do Read/Edit patterns work on Windows?** Paths are normalized to POSIX form (for example `C:\\Users\\alice` -> `/c/Users/alice`)
- **Do hook approvals override deny rules?** No — hooks can skip interactive prompts, but deny/ask rules still take precedence

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
- Read/Edit deny limitations for Bash subprocesses
- Windows Read/Edit pattern syntax examples (`//c/**`, `//**`)
- Full list of tool names for allow/deny rules
- Sandboxing setup and limitations
- Network proxy configuration syntax

## Source map
- permissions.md
- sandboxing.md
- security.md
- network-config.md
- llm-gateway.md
