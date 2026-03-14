# Knowledge Seed System — Plan 02: Build Scripts

> Split from [2026-03-14-knowledge-seed.md](/Volumes/storage/Projects/Git/Github/mrkhachaturov/claude-audit-plugin/superpowers/plans/2026-03-14-knowledge-seed.md). Covers original Chunk 2.

## Goal

Implement the Python automation that decides when to rebuild the seed, validates generated output, and bumps plugin version metadata when seed files change.

## Files

- Create `scripts/check_significance.py`
- Create `scripts/validate_seed.py`
- Create `scripts/bump_version.py`
- Create `tests/conftest.py`
- Create `tests/test_check_significance.py`
- Create `tests/test_validate_seed.py`
- Create `tests/test_bump_version.py`
- Update `scripts/requirements.txt`
- Create `scripts/requirements-dev.txt` if you keep test dependencies separate

## Tasks

### Task 1: Test infrastructure

- [x] Add pytest test setup
- [x] Add shared fixtures in `tests/conftest.py`
- [x] Make a minimal fake repo fixture with:
  - `docs/`
  - `agent-memory-seed/generated/`
  - `agent-memory-seed/agent-notes/`
- [x] Add a minimal valid manifest fixture

### Task 2: `check_significance.py`

- [x] Write failing tests first
- [x] Implement change analysis for:
  - no changes
  - new docs
  - heading changes
  - 30+ changed lines
  - affected routes/domains derivation
- [x] Parse `git diff -U0 HEAD~1 -- docs/`
- [x] Load prior `seed_manifest.json`
- [x] Output:
  - `rebuild`
  - `affected_routes`
  - `affected_domains`
  - `changed_docs`

### Task 3: `validate_seed.py`

- [x] Write failing tests first
- [x] Implement validation for:
  - no changes outside `agent-memory-seed/generated/`
  - no touches under `agent-notes/`
  - route IDs in navigation vs manifest
  - valid `depends_on_sections`
  - valid `domain_file` references
  - silent route rename detection
- [x] Exit non-zero on failure

### Task 4: `bump_version.py`

- [x] Write failing tests first
- [x] Implement patch bump behavior
- [x] Implement changelog prepend behavior
- [x] Make it a no-op when there are no relevant generated changes

### Task 5: Dependencies

- [x] Update runtime requirements if the scripts need new packages
- [x] Keep test-only packages out of runtime requirements if possible

## Verification

- [x] `python -m pytest tests/test_check_significance.py -v`
- [x] `python -m pytest tests/test_validate_seed.py -v`
- [x] `python -m pytest tests/test_bump_version.py -v`
- [x] `python -m pytest tests/ -v`

## Reference

Use the original plan for the long-form test and script examples:
[2026-03-14-knowledge-seed.md](/Volumes/storage/Projects/Git/Github/mrkhachaturov/claude-audit-plugin/superpowers/plans/2026-03-14-knowledge-seed.md)
