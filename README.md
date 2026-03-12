# claude-audit

AI-readiness audit plugin for Claude Code. Run `/audit-project` inside any project to get a structured report on what's good, what's missing, and what to add.

## Install

```
/plugin install claude-audit
```

> Requires `claude-code-setup` plugin for full automation recommendations:
> `/plugin install claude-code-setup`

## Usage

Run from inside the project you want to audit:

```
/audit-project
```

## What It Produces

```
## AI-Readiness Audit: <path>

### Project Profile
### What's Already Good
### Structure Gaps
### Recommended Automations
### Suggested Plugins to Install
### Priority Actions
```

## Contents

- `skills/audit-project/` — `/audit-project` skill
- `agents/claude-code-expert.md` — subagent with persistent Claude Code knowledge base
