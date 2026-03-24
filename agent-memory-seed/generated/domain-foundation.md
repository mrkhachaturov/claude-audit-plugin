# Domain: Foundation

## What this domain covers
How Claude Code operates at its core: the agentic loop, available tools, execution environments, authentication methods, provider integrations (Bedrock, Vertex, Foundry), context composition (including auto memory), data usage policies, and legal/compliance constraints.

## Decision rules
- Use this domain for questions about how Claude Code works internally
- Use this domain for authentication and subscription setup questions
- Use this domain for provider-specific setup (AWS, GCP, Azure)
- Use this domain for data privacy, retention, and compliance questions

## Fast answers
- **What is the agentic loop?** Claude reads context, decides actions, uses tools, observes results, then repeats until done
- **What tools does Claude Code have?** Read, Write, Edit, Bash, Glob, Grep, Agent (subagents), and MCP tools
- **What fills the context window?** Conversation history, file content, command outputs, `CLAUDE.md`, auto memory, loaded skills, and system instructions
- **Permission control baseline:** mode choices include `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, and `bypassPermissions`
- **Auth options:** Claude.ai subscription (OAuth), API key (direct), or enterprise providers (Bedrock/Vertex/Foundry)
- **Auth scope note:** `apiKeyHelper` and API key env vars apply to terminal CLI sessions; Desktop and Remote Control use OAuth
- **Does Claude send my code to Anthropic?** Depends on plan — see data-usage.md; zero-data-retention available for API users
- **How do I send product reports?** Use `/feedback`; disable with `DISABLE_FEEDBACK_COMMAND` (legacy `DISABLE_BUG_COMMAND` is still accepted)

## Fast comparisons
- **OAuth vs API key:** OAuth uses your Claude.ai subscription; API key uses pay-per-token billing
- **Bedrock vs Vertex vs direct API:** All use Claude models; differ in where inference runs and who manages auth
- **Pro vs Max plan:** Both work with Claude Code; Max has higher usage limits

## Common tasks
- "Set up Claude Code for the first time" → quickstart.md
- "Use Claude Code with AWS" → amazon-bedrock.md
- "Use Claude Code with GCP" → google-vertex-ai.md
- "Understand what data Anthropic sees" → data-usage.md
- "Comply with zero-data-retention requirements" → zero-data-retention.md

## When you must read source docs
- Exact OAuth token setup steps
- Bedrock/Vertex/Foundry IAM and credential configuration
- Specific compliance certifications or legal terms
- Network proxy or certificate configuration for enterprise

## Source map
- how-claude-code-works.md
- overview.md
- authentication.md
- amazon-bedrock.md
- google-vertex-ai.md
- microsoft-foundry.md
- llm-gateway.md
- data-usage.md
- legal-and-compliance.md
- zero-data-retention.md
- analytics.md
- chrome.md
- claude-code-on-the-web.md
