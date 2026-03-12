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

## Prerequisite Check

Before running, verify `claude-code-setup` plugin is installed and enabled:

```bash
find ~/.claude/plugins/cache -type d -name "claude-code-setup" 2>/dev/null | head -1 || echo "NOT INSTALLED"
```

If not installed: inform the user to run `/plugin install claude-code-setup` from the `mrkhachaturov/ccode-personal-plugins` marketplace, then restart the session.

If installed but `claude-automation-recommender` is not responding: the plugin may need to be enabled. Ask the user to verify with `/plugin list`.

## Workflow

### Step 1: Expert analysis

Dispatch the `claude-code-expert` subagent with this exact context:

> Analyze the project at `<path>` for AI-readiness. Read its CLAUDE.md, .claude/ structure, settings.json, and .mcp.json. Cross-reference against your knowledge of best practices. Return: (1) what's already good, (2) structure gaps, (3) anti-patterns found.

### Step 2: Automation gap analysis

Invoke the `claude-automation-recommender` skill by dispatching it as a subagent with the target project path as context:

```
Use the claude-automation-recommender skill to analyze the project at <path>.
Focus on hooks, MCP servers, subagents, skills, and plugins. Return the top 1-2 recommendations per category.
```

### Step 3: Compile report

Merge outputs into this format (6 sections):

```markdown
## AI-Readiness Audit: <path>

### Project Profile
- Type: [detected stack]
- Existing Claude setup: [summary]

### What's Already Good
- [item]

### Structure Gaps
- [gap] — [recommended fix]

### Recommended Automations
[output from claude-automation-recommender — top 1-2 per category]

### Suggested Plugins to Install
- [plugin] — [reason]

### Priority Actions
1. [highest impact first]
2. ...
```

Print the report to the session. Do not write it to disk unless the user asks.
