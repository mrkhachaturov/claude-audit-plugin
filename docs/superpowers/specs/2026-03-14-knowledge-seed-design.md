# Knowledge Seed System — Design Spec

**Date:** 2026-03-14
**Status:** Approved
**Scope:** claude-audit plugin v1.2.x

---

## Problem

`claude-code-expert` currently bootstraps by reading all docs on first invocation (~65 `.md` files). This is slow, expensive, and repeats work on every new install. The agent also has no fast routing mechanism — it either reads everything or guesses which doc to open.

---

## Goal

Pre-build a navigation and knowledge seed that ships with the plugin. The agent performs zero full-doc bootstrap. At runtime it consults `navigation.md`, answers from domain files when possible, and reads source docs only for exact syntax, edge cases, or citations.

---

## Architecture

### Two Layers, Two Owners

```
agent-memory-seed/
  generated/                  ← owned by GitHub Actions (Codex rebuilds on doc changes)
    navigation.md             ← intent router: question → domain → optional source docs
    domain-foundation.md
    domain-configuration-persistence.md
    domain-automation-control.md
    domain-extension-capability.md
    domain-access-control-safety.md
    domain-effective-interaction.md
    seed_manifest.json        ← section-level hashes, drives incremental rebuilds
  agent-notes/                ← owned by the agent at runtime, never touched by CI or scripts
    .gitkeep
```

`agent-notes/` is excluded from GitHub Actions, from install regeneration, and from update regeneration. This separation is absolute.

### On Install

The agent looks up `installPath` from `~/.claude/plugins/installed_plugins.json` using the key `claude-audit@ccode-personal-plugins`. It copies `installPath/agent-memory-seed/generated/` into `~/.claude/agent-memory/claude-audit-claude-code-expert/generated/`. It creates `agent-notes/` if missing and never overwrites it. It records `seed_version` from the manifest in `MEMORY.md`. No doc reading occurs.

### On Plugin Update

Only `generated/` is replaced. `agent-notes/` is always preserved. If the shipped `seed_manifest.json` cannot be read, the agent continues using its locally copied seed without rebuilding from docs.

### At Runtime (Q&A)

1. Read `navigation.md` → match question to a `route_id`
2. Read `domain_file` → answer if `answer_from_domain_if` applies
3. If `read_source_docs_if` applies → read `primary_doc`, then `secondary_doc` only if needed
4. Cite authoritative source doc(s) from `docs/*.md` in the final answer (never cite seed files)

**Fallback:** If no route matches confidently, use `strong_terms` to pick the best candidate. If ambiguity remains, read `primary_doc` for the top 2 candidates and answer conservatively with citations. If ambiguity persists after reading both primary docs, return both candidate answers explicitly, state the uncertainty, and cite all source docs consulted.

---

## Domain Taxonomy

Six domains cover all docs in `docs/`. Provider-specific, auth, and compliance docs map to the Foundation domain as context-setting material, not primary Q&A targets.

| Domain ID | File | Boundary |
|---|---|---|
| `foundation` | `domain-foundation.md` | How Claude Code works: agentic loop, tools, environments, providers (Bedrock, Vertex, Foundry), authentication, data usage, legal, zero-data-retention |
| `configuration-persistence` | `domain-configuration-persistence.md` | Storing instructions and settings across sessions: CLAUDE.md, memory, settings, env vars, server-managed settings |
| `automation-control` | `domain-automation-control.md` | Deterministic automation: hooks (all event types), scheduled tasks |
| `extension-capability` | `domain-extension-capability.md` | Extending Claude Code: skills, subagents, agent teams, MCP, plugins, plugin marketplaces |
| `access-control-safety` | `domain-access-control-safety.md` | What Claude can access and do: permissions, sandboxing, security, network config, LLM gateway |
| `effective-interaction` | `domain-effective-interaction.md` | Working well with Claude Code: best practices, common workflows, commands, output styles, keybindings, IDE integrations, remote control, headless, checkpointing, fast mode, model config, costs, monitoring |

---

## Seed File Formats

### `navigation.md` — Route Shape

```markdown
### route_id: configure-hooks
domain_id: automation-control
domain_file: domain-automation-control.md
intent: run code deterministically on tool events
match:
  - "how do hooks work"
  - "block a command"
  - "run on PostToolUse"
  - "notification hook"
strong_terms: [hook, PostToolUse, PreToolUse, matcher, blocking, notification]
avoid: [scheduled tasks, cron, skills]
answer_from_domain_if:
  - conceptual question
  - when-to-use
  - overview
  - hooks vs other primitives (fast comparison)
read_source_docs_if:
  - exact matcher syntax
  - blocking semantics
  - specific event type details
primary_doc: hooks.md
secondary_doc: hooks-guide.md
```

**Design rules:**
- Route by user intent, not doc title
- One `domain_file` per route
- At most one `primary_doc` and one `secondary_doc`
- `avoid` prevents adjacent-concept collisions
- `strong_terms` provide positive routing confidence
- `answer_from_domain_if` and `read_source_docs_if` govern token discipline
- `route_id`s are stable identifiers — Codex must preserve existing IDs across rebuilds; a changed ID is treated as a deletion + addition and invalidates dependent outputs in the manifest

### `domain-*.md` — Structure

```markdown
# Domain: <Name>

## What this domain covers
<One paragraph. Defines the boundary.>

## Decision rules
<Bullet list: use X when Y.>

## Fast answers
<Bullet list: one-liner answers to the most common questions.>

## Fast comparisons
<Bullet list: "A vs B" forms. Covers hooks vs scheduled tasks, skills vs hooks, etc.>

## Common tasks
<"User wants to X" → primitive to use.>

## When you must read source docs
<Bullet list: exact syntax, auth details, frontmatter fields, etc.>

## Source map
<List of doc filenames that back this domain.>
```

Target: covers 60–70% of questions without opening a source doc.

### `agent-notes/qa-patterns.md` — Format

Agent-written. One entry per saved pattern:

```
## <short label>
question shape: <what the user typically asks>
answer rule: <the stable answer or decision heuristic>
docs: [<doc1.md>, <doc2.md>]
caveat: <edge cases, version constraints, or ambiguities>
```

Save only if the note would improve 3+ future questions. Do not save one-off facts, version details, or material already in the generated seed.

### `seed_manifest.json` — Schema

```json
{
  "schema_version": 1,
  "seed_version": "ISO-8601 timestamp",
  "source_docs": {
    "hooks.md": {
      "file_hash": "sha256",
      "headings_hash": "sha256",
      "headings": ["Overview", "Event Types", "Tool Events", "Command Events", "Examples"],
      "sections": {
        "event-types": {
          "hash": "sha256",
          "start_heading": "Event Types",
          "end_heading": "Tool Events",
          "domains": ["automation-control"],
          "routes": ["configure-hooks"]
        }
      }
    }
  },
  "outputs": {
    "domain-automation-control.md": {
      "content_hash": "sha256",
      "depends_on_sections": ["hooks.md::event-types", "hooks-guide.md::common-patterns"]
    },
    "navigation.md": {
      "content_hash": "sha256",
      "depends_on_routes": ["configure-hooks"]
    }
  }
}
```

`headings` array gives `check_significance.py` the prior heading tree per doc without re-reading the file. Section boundaries are defined by `start_heading` / `end_heading` so line-range-to-section mapping is deterministic. Section-level hashing enables precise invalidation. `outputs` tracks which generated files depend on which sections, enabling skips when Codex produces identical output.

---

## Build Pipeline

### New Scripts

**`scripts/check_significance.py`**
- Inputs: `docs/docs_manifest.json` (current hashes), `agent-memory-seed/generated/seed_manifest.json` (prior headings + section hashes), `git diff -U0 HEAD~1 -- docs/` (unified diff with zero context lines, provides exact changed line ranges per file)
- Derives affected sections by comparing current heading trees (extracted from changed docs) against `seed_manifest.json` `headings` arrays
- Maps changed line ranges (from unified diff hunk headers `@@ -L +L @@`) to sections using `start_heading` / `end_heading` boundaries; requires `--depth=2` fetch in the workflow or equivalent to ensure `HEAD~1` is available
- Outputs to `$GITHUB_OUTPUT`: `rebuild=true/false`, `affected_routes` (comma-separated), `affected_domains` (comma-separated), `changed_docs` (comma-separated)
- Triggers rebuild if: new doc files added, any heading changed, or 30+ lines changed across docs

**`scripts/validate_seed.py`**
- Inputs: git working tree state after Codex runs
- Checks (exits non-zero on any failure):
  1. No files modified outside `agent-memory-seed/generated/`
  2. `agent-notes/` not touched
  3. All `route_id`s in `navigation.md` exist in `seed_manifest.json` routes
  4. All `depends_on_sections` in `outputs` reference sections that exist in `source_docs`
  5. All `domain_file` references in routes resolve to files in `generated/`
  6. No route IDs were silently renamed (compare against prior manifest)
- Exit 0 = valid, exit 1 = issues found (printed to stdout for issue body)

**`scripts/bump_version.py`**
- Inputs: `git diff --name-only agent-memory-seed/generated/`, `plugin.json` (semver patch field), `CHANGELOG.md`, `$CHANGED_DOCS` env var (forwarded from `check_significance.py` step output via workflow `env:` block)
- Only runs if generated files actually changed
- Increments patch version in `plugin.json` (format: `MAJOR.MINOR.PATCH`). Note: `seed_version` in `seed_manifest.json` is the ISO-8601 timestamp of the last Codex run and is independent of the semver release version — they serve different consumers (agent reads `seed_version`; plugin installers and marketplace read `plugin.json` semver).
- Prepends CHANGELOG entry listing which docs triggered the rebuild

### Updated `update-docs.yml`

Four new steps added after "Fetch latest documentation":

```yaml
- name: Check seed significance
  id: seed-check
  run: python scripts/check_significance.py >> $GITHUB_OUTPUT

- name: Rebuild seed with Codex
  if: steps.seed-check.outputs.rebuild == 'true'
  id: codex-rebuild
  continue-on-error: true
  uses: openai/codex-action@v1
  with:
    openai-api-key: ${{ secrets.OPENAI_API_KEY }}
    prompt-file: .github/prompts/build-seed.md
    output-file: codex-seed-output.md
    safety-strategy: drop-sudo
    sandbox: workspace-write

- name: Validate seed output
  if: steps.seed-check.outputs.rebuild == 'true' && steps.codex-rebuild.outcome == 'success'
  id: seed-validate
  run: python scripts/validate_seed.py

- name: Bump version if seed changed
  if: steps.seed-validate.outcome == 'success'
  env:
    CHANGED_DOCS: ${{ steps.seed-check.outputs.changed_docs }}
  run: python scripts/bump_version.py

- name: Create issue on Codex failure
  if: steps.codex-rebuild.outcome == 'failure' || steps.seed-validate.outcome == 'failure'
  uses: actions/github-script@v7
  with:
    script: |
      const date = new Date().toISOString().split('T')[0];
      await github.rest.issues.create({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: `Seed rebuild failed - ${date}`,
        body: `Seed rebuild failed on ${date}. Docs updated normally. See workflow run for details.`,
        labels: ['bug', 'automation']
      })
```

**Codex failure behavior:** non-destructive. `continue-on-error: true` ensures the docs commit always proceeds. Validation and version bump are skipped. A GitHub issue is opened.

**Commit:** all staged together — `docs/`, `agent-memory-seed/generated/`, `plugin.json`, `CHANGELOG.md`.

### `.github/prompts/build-seed.md` — Codex Prompt Contract

Passes Codex only:
- Current `navigation.md` and affected `domain-*.md` files
- Current `seed_manifest.json`
- Changed doc contents + per-doc diff summary + old/new heading trees
- 6-domain taxonomy (from spec table above)
- Hard output constraints: file delimiters (`=== BEGIN FILE: <path> ===` / `=== END FILE ===`), no `agent-notes/` touches, rebuild only affected files, preserve existing `route_id`s

---

## Agent Changes — `claude-code-expert.md`

### Bootstrap (replaces current full-doc read)

```
On first invocation:
1. Read ~/.claude/plugins/installed_plugins.json
2. Extract installPath for key "claude-audit@ccode-personal-plugins"
3. Copy installPath/agent-memory-seed/generated/ → ~/.claude/agent-memory/claude-audit-claude-code-expert/generated/
4. Create agent-notes/ if missing (never overwrite)
5. Write seed_version from manifest into MEMORY.md

If installed_plugins.json is missing, key not found, or seed_manifest.json unreadable:
- Continue using locally copied generated/ seed if it exists
- Preserve agent-notes/
- Do not fall back to reading all docs
```

### Q&A Mode (new section)

```
When answering a question:
1. Read generated/navigation.md → match to route_id by intent, match phrases, and strong_terms
2. Read domain_file
3. Answer from domain file if answer_from_domain_if applies
4. If read_source_docs_if applies → read primary_doc, then secondary_doc if needed
5. Cite source docs from docs/*.md only (never cite navigation.md or domain files)

Fallback:
- No confident match → use strong_terms to select best candidate
- Still ambiguous → read primary_doc for top 2 candidates, answer conservatively
- Still ambiguous after reading both → return both candidate answers, state uncertainty explicitly, cite all docs consulted

Memory rule:
- Save to agent-notes/qa-patterns.md ONLY if the note would improve 3+ future questions
- Format: question shape → answer rule → docs → caveat
- Do not save: one-off facts, version details, material already in generated seed
```

### Memory Structure

```
~/.claude/agent-memory/claude-audit-claude-code-expert/
  MEMORY.md                        ← index + seed_version
  generated/                       ← copied from plugin, refreshed on update
    navigation.md
    domain-*.md (6 files)
    seed_manifest.json
  agent-notes/                     ← agent-written, never overwritten by scripts or CI
    qa-patterns.md
```

---

## Updated Skill — `skills/ask-claude-code/SKILL.md`

**Action: Updated** (file already exists; current version is replaced wholesale).

Thin dispatcher. Receives user question verbatim, dispatches `claude-audit:claude-code-expert` in Q&A mode, relays full response.

```yaml
name: ask-claude-code
description: Ask any question about Claude Code — CLAUDE.md, memory, hooks, skills,
  agents, plugins, MCP, settings, permissions, or best practices.
  Answers are backed by official documentation. Usage: /ask-claude-code <question>
```

Passes to agent:
```
Mode: Q&A
Question: <verbatim user question>
```

---

## Key Invariants

| Invariant | Enforcement |
|---|---|
| `agent-notes/` never touched by CI | `validate_seed.py` exit + prompt constraint |
| Citations always point to `docs/*.md` | Agent instruction |
| Version bump only on validated changes | Conditional on `seed-validate` outcome |
| Codex failure is non-destructive | `continue-on-error: true` + issue creation |
| Seed unreadable → use local copy | Agent bootstrap fallback |
| `route_id`s stable across rebuilds | `validate_seed.py` rename detection + prompt constraint |
| `navigation.md` and manifest stay in sync | `validate_seed.py` cross-reference check |

---

## Files Changed / Created

| File | Action |
|---|---|
| `agent-memory-seed/generated/navigation.md` | New (Codex-generated, bootstrapped manually first run) |
| `agent-memory-seed/generated/domain-*.md` (×6) | New (Codex-generated, bootstrapped manually first run) |
| `agent-memory-seed/generated/seed_manifest.json` | New |
| `agent-memory-seed/agent-notes/.gitkeep` | New |
| `scripts/check_significance.py` | New |
| `scripts/validate_seed.py` | New |
| `scripts/bump_version.py` | New |
| `.github/prompts/build-seed.md` | New |
| `.github/workflows/update-docs.yml` | Updated |
| `agents/claude-code-expert.md` | Updated |
| `skills/ask-claude-code/SKILL.md` | Updated |
| `scripts/requirements.txt` | Updated (openai SDK) |
