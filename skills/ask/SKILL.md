---
name: ask
description: Ask any question about Claude Code — CLAUDE.md, memory, hooks, skills,
  agents, plugins, MCP, settings, permissions, or best practices.
  Answers are backed by official documentation. Usage: /claude-audit:ask <question>
disable-model-invocation: true
context: fork
---

The user has a question about Claude Code. Dispatch the `claude-audit:claude-code-expert` agent to answer it.

Pass the user's question verbatim as the task prompt, prefixed with:

> Mode: Q&A
> Question: <verbatim user question>

The agent will consult its seeded knowledge files and return a doc-backed answer.

Relay the agent's full response to the user.
