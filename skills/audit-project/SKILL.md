---
name: audit-project
description: Audit any project for AI-readiness. Analyzes Claude Code structure and suggests improvements. Run /audit-project from within the project you want to audit.
---

# audit-project

Analyze a project's AI-readiness and produce a structured improvement report.

**Announce at start:** "Running AI-readiness audit on `<current directory>`..."

## Usage

Run from within the project directory you want to audit:

```
/audit-project
```

The skill audits the current working directory.

## Workflow

### Steps 1 & 2: Parallel analysis

Dispatch both agents in a **single message** (two Agent tool calls simultaneously):

**Agent 1 — `claude-code-expert`:**
> Analyze the project at `<path>` for AI-readiness. Read its CLAUDE.md, .claude/ structure, settings.json, and .mcp.json. Cross-reference against your knowledge of best practices. Return: (1) what's already good, (2) structure gaps, (3) anti-patterns found.

**Agent 2 — `automation-analyst`:**
> Analyze the project at `<path>` for automation gaps. Detect language, framework, tooling, and CI patterns. Return the Recommended Automations section with top 1-2 picks per category.

Wait for both to complete before proceeding to Step 3.

### Step 3: Compile report

Merge outputs into this format:

```markdown
## AI-Readiness Audit: <path>

### Project Profile
- **Type:** [detected stack — languages, frameworks, IaC tools]
- **Secrets management:** [how secrets are handled]
- **Existing Claude setup:** [summary of what's already configured]

### What's Already Good
| Area | Detail |
|------|--------|
| [area] | [what's well done] |

### Structure Gaps
| Gap | Recommended Fix | Priority |
|-----|----------------|----------|
| [gap] | [fix] | 🔴/🟡/🟢 |

### Recommended Automations
[Full output from automation-analyst — MCP servers, hooks, subagents, skills, plugins]

### Suggested Plugins to Install
| Plugin | Reason |
|--------|--------|
| [plugin] | [reason] |

### Priority Actions
| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 1 | [highest impact first] | High/Med/Low | High/Med/Low |
| 2 | ... | | |

### Quick Wins (do today)
- [action that takes < 30 min and has high impact]

### Long-term Improvements
- [architectural or structural changes worth planning]
```

Print the report to the session. Do not write it to disk unless the user asks.

### Step 4: Next steps prompt

After printing the report, ask:

> Would you like me to:
> 1. Generate an implementation plan for the Priority Actions (`superpowers:writing-plans`)
> 2. Save audit findings to project memory
> 3. Done
