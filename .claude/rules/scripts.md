---
globs: scripts/*.py
---

Python scripts in this directory are part of the CI build pipeline for the knowledge seed system.

Key contracts:
- `slugify.py` defines the heading-to-section-ID mapping. All section IDs in generated seed files must match its output.
- `validate_seed.py` runs 6 integrity checks on the generated seed. CI will fail if validation fails.
- `check_significance.py` determines if fetched doc changes are significant enough to trigger a seed rebuild.

Tests live in `tests/` and mirror script names (e.g., `test_slugify.py`). Run with `python -m pytest tests/ -x -q`.
