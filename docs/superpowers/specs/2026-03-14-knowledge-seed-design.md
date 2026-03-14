# Knowledge Seed System — Design Spec

**Date:** 2026-03-14
**Status:** Approved
**Scope:** claude-audit plugin v1.2.x

---

## Problem

`claude-code-expert` currently bootstraps by reading all 68 docs on first invocation. This is slow, expensive, and repeats work on every new install. The agent also has no fast routing mechanism — it either reads everything or guesses which doc to open.

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

The agent copies `installPath/agent-memory-seed/generated/` into `~/.claude/agent-memory/claude-audit-claude-code-expert/generated/`. It creates `agent-notes/` if missing and never overwrites it. It records `seed_version` from the manifest in `MEMORY.md`. No doc reading occurs.

### On Plugin Update

Only `generated/` is replaced. `agent-notes/` is always preserved. If the shipped `seed_manifest.json` cannot be read, the agent continues using its locally copied seed without rebuilding from docs.

### At Runtime (Q&A)

1. Read `navigation.md` → match question to a `route_id`
2. Read `domain_file` → answer if `answer_from_domain_if` applies
3. If `read_source_docs_if` applies → read `primary_doc`, then `secondary_doc` only if needed
4. Cite authoritative source doc(s) from `docs/*.md` in the final answer (never cite seed files)

**Fallback:** If no route matches confidently, use `strong_terms` to pick the best candidate. If ambiguity remains, read `primary_doc` for the top 2 candidates and answer conservatively with citations.

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

### `seed_manifest.json` — Schema

```json
{
  "schema_version": 1,
  "seed_version": "ISO-8601 timestamp",
  "source_docs": {
    "hooks.md": {
      "file_hash": "sha256",
      "headings_hash": "sha256",
      "sections": {
        "event-types": {
          "hash": "sha256",
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

Section-level hashing enables precise invalidation: only domain files and routes whose source sections changed get rebuilt. `outputs` tracks which generated files depend on which sections, enabling skips when Codex produces identical output.

---

## Build Pipeline

### New Scripts

**`scripts/check_significance.py`**
- Uses `git diff --numstat` against the previous commit for line counts
- Derives affected sections from prior `seed_manifest.json` section metadata (heading trees, not just hashes)
- Outputs: `rebuild=true/false`, `affected_routes`, `affected_domains`, `changed_docs`
- Triggers rebuild if: new doc files added, headings changed in any doc, or 30+ lines changed across docs

**`scripts/bump_version.py`**
- Runs only after post-Codex validation passes
- Only increments patch version if `git diff --name-only agent-memory-seed/generated/` shows actual changes
- Prepends CHANGELOG entry listing which docs triggered the rebuild

### Updated `update-docs.yml`

Two new steps added after "Fetch latest documentation":

```yaml
- name: Check seed significance
  id: seed-check
  run: python scripts/check_significance.py >> $GITHUB_OUTPUT

- name: Rebuild seed with Codex
  if: steps.seed-check.outputs.rebuild == 'true'
  uses: openai/codex-action@v1
  with:
    openai-api-key: ${{ secrets.OPENAI_API_KEY }}
    prompt-file: .github/prompts/build-seed.md
    output-file: codex-seed-output.md
    safety-strategy: drop-sudo
    sandbox: workspace-write

- name: Validate seed output
  if: steps.seed-check.outputs.rebuild == 'true'
  run: python scripts/validate_seed.py
  # Fails if: anything outside agent-memory-seed/generated/ was modified,
  # agent-notes/ was touched, manifest/navigation drift detected,
  # or manifest references missing routes/files/sections

- name: Bump version if seed changed
  if: steps.seed-check.outputs.rebuild == 'true'
  run: python scripts/bump_version.py
```

**Codex failure behavior:** non-destructive. Docs commit proceeds unchanged. A GitHub issue is opened (mirrors existing fetch-failure pattern).

**Commit:** all staged together — `docs/`, `agent-memory-seed/generated/`, `plugin.json`, `CHANGELOG.md`.

### `.github/prompts/build-seed.md` — Codex Prompt Contract

Passes Codex only:
- Current `navigation.md` and affected `domain-*.md` files
- Current `seed_manifest.json`
- Changed doc contents + per-doc diff summary + old/new heading trees
- 6-domain taxonomy
- Hard output constraints: file delimiters, no `agent-notes/` touches, rebuild only affected files, stable `route_id`s

---

## Agent Changes — `claude-code-expert.md`

### Bootstrap (replaces current 68-doc read)

```
On first invocation:
1. Find installPath from ~/.claude/plugins/installed_plugins.json
2. Copy installPath/agent-memory-seed/generated/ → ~/.claude/agent-memory/claude-audit-claude-code-expert/generated/
3. Create agent-notes/ if missing (never overwrite)
4. Write seed_version from manifest into MEMORY.md

If installPath or seed_manifest.json cannot be read:
- Continue using locally copied seed
- Preserve agent-notes/
- Do not fall back to reading all docs
```

### Q&A Mode (new section)

```
When answering a question:
1. Read navigation.md → match to route_id by intent, match phrases, and strong_terms
2. Read domain_file
3. Answer from domain file if answer_from_domain_if applies
4. If read_source_docs_if applies → read primary_doc, then secondary_doc if needed
5. Cite source docs from docs/*.md (never cite navigation.md or domain files)

Fallback:
- No confident match → use strong_terms to select best candidate
- Still ambiguous → read primary_doc for top 2 candidates, answer conservatively

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
  agent-notes/                     ← agent-written, never overwritten
    qa-patterns.md
```

---

## New Skill — `skills/ask-claude-code/SKILL.md`

Thin dispatcher. Receives user question, passes verbatim to `claude-audit:claude-code-expert` in Q&A mode, relays full response.

```yaml
name: ask-claude-code
description: Ask any question about Claude Code — CLAUDE.md, memory, hooks, skills,
  agents, plugins, MCP, settings, permissions, or best practices.
  Answers are backed by official documentation.
```

---

## Key Invariants

| Invariant | Enforcement |
|---|---|
| `agent-notes/` never touched by CI | Validation step + prompt constraint |
| Citations always point to `docs/*.md` | Agent instruction |
| Version bump only on validated changes | `bump_version.py` checks git diff |
| Codex failure is non-destructive | Workflow `continue-on-error` + issue creation |
| Seed unreadable → use local copy | Agent bootstrap fallback |
| `navigation.md` generated from manifest routes | Codex prompt constraint |

---

## Files Changed / Created

| File | Action |
|---|---|
| `agent-memory-seed/generated/navigation.md` | New (Codex-generated) |
| `agent-memory-seed/generated/domain-*.md` (×6) | New (Codex-generated) |
| `agent-memory-seed/generated/seed_manifest.json` | New |
| `agent-memory-seed/agent-notes/.gitkeep` | New |
| `scripts/check_significance.py` | New |
| `scripts/validate_seed.py` | New |
| `scripts/bump_version.py` | New |
| `.github/prompts/build-seed.md` | New |
| `.github/workflows/update-docs.yml` | Updated |
| `agents/claude-code-expert.md` | Updated |
| `skills/ask-claude-code/SKILL.md` | New |
| `scripts/requirements.txt` | Updated (openai or anthropic SDK if needed) |
