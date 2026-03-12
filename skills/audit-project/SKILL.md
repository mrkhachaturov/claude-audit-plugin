---
name: audit-project
description: Audit any project for AI-readiness. Analyzes Claude Code structure and suggests improvements. Invoked by user with /audit-project /path.
---

# audit-project

Analyze a project's AI-readiness and produce a structured improvement report.

**Announce at start:** "Running AI-readiness audit on `<path>`..."

## Usage

```
/audit-project /absolute/path/to/project
```

If no path provided, use the current working directory.

## Prerequisite Check

Before running, verify `claude-code-setup` plugin is installed with the skill available:

```bash
find ~/.claude/plugins/cache -name "SKILL.md" -path "*/claude-automation-recommender/*" 2>/dev/null | head -1 || echo "NOT FOUND"
```

If not found: inform the user to run `/plugin install claude-code-setup@ccode-personal-plugins`, then restart the session.

## Workflow

### Step 1: Expert analysis

Dispatch the `claude-code-expert` subagent with this exact context:

> Analyze the project at `<path>` for AI-readiness. Read its CLAUDE.md, .claude/ structure, settings.json, and .mcp.json. Cross-reference against your knowledge of best practices. Return: (1) what's already good, (2) structure gaps, (3) anti-patterns found.

### Step 2: Automation gap analysis

Invoke the `claude-code-setup:claude-automation-recommender` skill using the Skill tool directly (not as a subagent). The skill runs in the current session context and will analyze the current project directory.

Note: Steps 1 and 2 run sequentially — Step 1 as a subagent, Step 2 as a skill in the main context.

### Step 3: Compile report

Merge outputs into this format:

```markdown
## AI-Readiness Audit: <path>

### Project Profile
- Type: [detected stack — languages, frameworks, IaC tools]
- Secrets management: [how secrets are handled]
- Existing Claude setup: [summary of what's already configured]

### What's Already Good
| Area | Detail |
|------|--------|
| [area] | [what's well done] |

### Structure Gaps
| Gap | Recommended Fix | Priority |
|-----|----------------|----------|
| [gap] | [fix] | 🔴/🟡/🟢 |

### Recommended Automations
[output from claude-automation-recommender — top 1-2 per category with code snippets]

### Suggested Plugins to Install
| Plugin | Reason |
|--------|--------|
| [plugin] | [reason] |

### Priority Actions
| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 1 | [highest impact first] | High/Med/Low | High/Med/Low |
| 2 | ... | | |
```

Print the report to the session. Do not write it to disk unless the user asks.

### Step 4: Next steps prompt

After printing the report, ask:

> Would you like me to:
> 1. Generate an implementation plan for the Priority Actions (`superpowers:writing-plans`)
> 2. Save audit findings to project memory
> 3. Done
