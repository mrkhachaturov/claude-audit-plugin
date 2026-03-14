"""Tests for bump_version.py."""
import json
import pytest
from pathlib import Path
from unittest.mock import patch


def test_patch_version_incremented(tmp_repo):
    """bump_version increments the patch field in plugin.json."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    plugin_json = tmp_repo / ".claude-plugin" / "plugin.json"
    plugin_json.parent.mkdir(parents=True)
    plugin_json.write_text(json.dumps({"name": "claude-audit", "version": "1.1.1"}))

    changelog = tmp_repo / "CHANGELOG.md"
    changelog.write_text("# Changelog\n\n## [1.1.1] — 2026-03-01\n\n- Previous entry\n")

    from bump_version import bump
    bump(str(tmp_repo), changed_docs=["hooks.md"])

    updated = json.loads(plugin_json.read_text())
    assert updated["version"] == "1.1.2"


def test_changelog_entry_prepended(tmp_repo):
    """bump_version prepends a new CHANGELOG entry above the previous one."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    plugin_json = tmp_repo / ".claude-plugin" / "plugin.json"
    plugin_json.parent.mkdir(parents=True)
    plugin_json.write_text(json.dumps({"name": "claude-audit", "version": "1.1.1"}))

    changelog = tmp_repo / "CHANGELOG.md"
    changelog.write_text("# Changelog\n\n## [1.1.1] — 2026-03-01\n\n- Previous\n")

    from bump_version import bump
    bump(str(tmp_repo), changed_docs=["hooks.md", "skills.md"])

    content = changelog.read_text()
    assert "## [1.1.2]" in content
    assert "hooks.md" in content
    assert "skills.md" in content
    # New entry should come before old entry
    assert content.index("1.1.2") < content.index("1.1.1")


def test_no_change_no_bump(tmp_repo):
    """If changed_docs is empty, version should not be bumped."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    plugin_json = tmp_repo / ".claude-plugin" / "plugin.json"
    plugin_json.parent.mkdir(parents=True)
    plugin_json.write_text(json.dumps({"name": "claude-audit", "version": "1.1.1"}))

    changelog = tmp_repo / "CHANGELOG.md"
    changelog.write_text("# Changelog\n\n## [1.1.1] — 2026-03-01\n")

    from bump_version import bump
    bump(str(tmp_repo), changed_docs=[])

    updated = json.loads(plugin_json.read_text())
    assert updated["version"] == "1.1.1"


def test_no_generated_changes_no_bump(tmp_repo):
    """If git diff shows no changes to generated/, version should not be bumped even with changed_docs."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    plugin_json = tmp_repo / ".claude-plugin" / "plugin.json"
    plugin_json.parent.mkdir(parents=True, exist_ok=True)
    plugin_json.write_text(json.dumps({"name": "claude-audit", "version": "1.1.1"}))

    changelog = tmp_repo / "CHANGELOG.md"
    changelog.write_text("# Changelog\n\n## [1.1.1] — 2026-03-01\n")

    # Mock get_generated_changes to return empty list (no actual generated file changes)
    with patch("bump_version.get_generated_changes", return_value=[]):
        from bump_version import bump
        bump(str(tmp_repo), changed_docs=["hooks.md"])

    updated = json.loads(plugin_json.read_text())
    assert updated["version"] == "1.1.1"
