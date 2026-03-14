"""
Shared heading-to-section-ID slugification for the claude-audit build pipeline.

Used by:
  - manifest generation (Plan 01)
  - check_significance.py (heading comparison)
  - validate_seed.py (section ID checks)

Section ID rules:
  - lowercase and trim
  - replace runs of non-alphanumeric characters with a single '-'
  - strip leading/trailing '-'
  - if a doc has duplicate headings, suffix later occurrences: 'foo', 'foo-2', 'foo-3'
"""

import re


def slugify_heading(heading: str) -> str:
    """
    Convert a single Markdown heading string to a section ID slug.

    Examples:
      "Event Types"         -> "event-types"
      "CLAUDE.md files"     -> "claude-md-files"
      "Top 10 things"       -> "top-10-things"
      "  Extra  Spaces  "   -> "extra-spaces"
    """
    text = heading.strip().lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


def slugify_headings(headings: list[str]) -> list[str]:
    """
    Convert a list of headings to section ID slugs, appending '-2', '-3', ...
    for duplicate headings within the same document.

    Examples:
      ["A", "B", "A", "A"] -> ["a", "b", "a-2", "a-3"]
    """
    counts: dict[str, int] = {}
    result = []
    for h in headings:
        base = slugify_heading(h)
        if base not in counts:
            counts[base] = 1
            result.append(base)
        else:
            counts[base] += 1
            result.append(f"{base}-{counts[base]}")
    return result
