"""Tests for check_significance.py."""
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


# Interface expected:
# check_significance.analyze_changes(repo_root, git_diff_output, seed_manifest) -> dict with keys:
#   rebuild: bool
#   affected_domains: list[str]
#   affected_routes: list[str]
#   changed_docs: list[str]


def test_no_changes_returns_no_rebuild(tmp_repo, minimal_manifest):
    """When docs haven't changed, rebuild should be False."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    seed_manifest_path = tmp_repo / "agent-memory-seed" / "generated" / "seed_manifest.json"
    seed_manifest_path.write_text(json.dumps(minimal_manifest))

    git_diff = ""

    from check_significance import analyze_changes
    result = analyze_changes(str(tmp_repo), git_diff, minimal_manifest)

    assert result["rebuild"] is False
    assert result["changed_docs"] == []


def test_new_file_triggers_rebuild(tmp_repo, minimal_manifest):
    """Adding a new doc should always trigger rebuild."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    seed_manifest_path = tmp_repo / "agent-memory-seed" / "generated" / "seed_manifest.json"
    seed_manifest_path.write_text(json.dumps(minimal_manifest))

    git_diff = "diff --git a/docs/new-feature.md b/docs/new-feature.md\nnew file mode 100644\n+++ b/docs/new-feature.md\n@@ -0,0 +1,50 @@\n+# New Feature\n"

    from check_significance import analyze_changes
    result = analyze_changes(str(tmp_repo), git_diff, minimal_manifest)

    assert result["rebuild"] is True
    assert "new-feature.md" in result["changed_docs"]


def test_small_change_no_rebuild(tmp_repo, minimal_manifest):
    """A small prose change (< 30 lines, no heading change) should not trigger rebuild."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    seed_manifest_path = tmp_repo / "agent-memory-seed" / "generated" / "seed_manifest.json"
    seed_manifest_path.write_text(json.dumps(minimal_manifest))

    git_diff = (
        "diff --git a/docs/hooks.md b/docs/hooks.md\n"
        "--- a/docs/hooks.md\n+++ b/docs/hooks.md\n"
        "@@ -10,3 +10,3 @@\n"
        "-old sentence here\n"
        "+new sentence here\n"
    )

    from check_significance import analyze_changes
    result = analyze_changes(str(tmp_repo), git_diff, minimal_manifest)

    assert result["rebuild"] is False


def test_heading_change_triggers_rebuild(tmp_repo, minimal_manifest):
    """A changed heading in a tracked doc should trigger rebuild."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    seed_manifest_path = tmp_repo / "agent-memory-seed" / "generated" / "seed_manifest.json"
    seed_manifest_path.write_text(json.dumps(minimal_manifest))

    git_diff = (
        "diff --git a/docs/hooks.md b/docs/hooks.md\n"
        "--- a/docs/hooks.md\n+++ b/docs/hooks.md\n"
        "@@ -5,1 +5,1 @@\n"
        "-## Event Types\n"
        "+## Hook Event Types\n"
    )

    from check_significance import analyze_changes
    result = analyze_changes(str(tmp_repo), git_diff, minimal_manifest)

    assert result["rebuild"] is True
    assert "hooks.md" in result["changed_docs"]


def test_large_change_triggers_rebuild(tmp_repo, minimal_manifest):
    """30+ changed lines should trigger rebuild regardless of heading changes."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    seed_manifest_path = tmp_repo / "agent-memory-seed" / "generated" / "seed_manifest.json"
    seed_manifest_path.write_text(json.dumps(minimal_manifest))

    changed_lines = "\n".join([f"+line {i}" for i in range(35)])
    git_diff = (
        "diff --git a/docs/hooks.md b/docs/hooks.md\n"
        "--- a/docs/hooks.md\n+++ b/docs/hooks.md\n"
        "@@ -20,0 +20,35 @@\n"
        f"{changed_lines}\n"
    )

    from check_significance import analyze_changes
    result = analyze_changes(str(tmp_repo), git_diff, minimal_manifest)

    assert result["rebuild"] is True


def test_affected_routes_identified(tmp_repo, minimal_manifest):
    """Changed doc sections should identify which routes are affected."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    seed_manifest_path = tmp_repo / "agent-memory-seed" / "generated" / "seed_manifest.json"
    seed_manifest_path.write_text(json.dumps(minimal_manifest))

    git_diff = (
        "diff --git a/docs/hooks.md b/docs/hooks.md\n"
        "--- a/docs/hooks.md\n+++ b/docs/hooks.md\n"
        "@@ -5,1 +5,1 @@\n"
        "-## Event Types\n"
        "+## Hook Event Types\n"
    )

    from check_significance import analyze_changes
    result = analyze_changes(str(tmp_repo), git_diff, minimal_manifest)

    assert "configure-hooks" in result["affected_routes"]
    assert "automation-control" in result["affected_domains"]
