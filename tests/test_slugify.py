"""Tests for scripts/slugify.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from slugify import slugify_heading, slugify_headings


class TestSlugifyHeading:
    def test_basic(self):
        assert slugify_heading("Event Types") == "event-types"

    def test_lowercase(self):
        assert slugify_heading("OVERVIEW") == "overview"

    def test_trim(self):
        assert slugify_heading("  Extra Spaces  ") == "extra-spaces"

    def test_punctuation_replaced(self):
        assert slugify_heading("CLAUDE.md files") == "claude-md-files"

    def test_numbers_preserved(self):
        assert slugify_heading("Top 10 things") == "top-10-things"

    def test_consecutive_nonalpha_collapsed(self):
        assert slugify_heading("foo  --  bar") == "foo-bar"

    def test_no_leading_trailing_dash(self):
        assert slugify_heading("!Event Types!") == "event-types"

    def test_already_slug(self):
        assert slugify_heading("event-types") == "event-types"

    def test_complex_heading(self):
        assert slugify_heading("How Claude Code works") == "how-claude-code-works"

    def test_apostrophe(self):
        assert slugify_heading("What's next") == "what-s-next"


class TestSlugifyHeadings:
    def test_unique_headings(self):
        assert slugify_headings(["Overview", "Event Types"]) == ["overview", "event-types"]

    def test_duplicate_first_occurrence_has_no_suffix(self):
        result = slugify_headings(["Overview", "Details", "Overview"])
        assert result[0] == "overview"
        assert result[2] == "overview-2"

    def test_triple_duplicate(self):
        result = slugify_headings(["A", "A", "A"])
        assert result == ["a", "a-2", "a-3"]

    def test_mixed_duplicates(self):
        result = slugify_headings(["A", "B", "A", "A"])
        assert result == ["a", "b", "a-2", "a-3"]

    def test_empty_list(self):
        assert slugify_headings([]) == []

    def test_single_heading(self):
        assert slugify_headings(["Event Types"]) == ["event-types"]
