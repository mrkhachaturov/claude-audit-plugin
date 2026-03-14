"""Tests for validate_seed.py."""
import json
import pytest
from pathlib import Path


def write_valid_seed(tmp_repo, manifest):
    """Helper: write a complete valid seed to tmp_repo."""
    generated = tmp_repo / "agent-memory-seed" / "generated"
    generated.mkdir(parents=True, exist_ok=True)

    (generated / "seed_manifest.json").write_text(json.dumps(manifest))

    # Create navigation.md with matching route_ids
    route_ids = list(manifest.get("routes", {}).keys())
    nav_content = "# Claude Code Navigation Seed\n\n"
    for rid in route_ids:
        nav_content += f"### route_id: {rid}\ndomain_id: test\ndomain_file: domain-test.md\n\n"
    (generated / "navigation.md").write_text(nav_content)

    # Create domain files listed in routes
    domain_files = {r["domain_file"] for r in manifest.get("routes", {}).values()}
    for df in domain_files:
        (generated / df).write_text(f"# Domain Test\n")

    # Create agent-notes/.gitkeep
    notes = tmp_repo / "agent-memory-seed" / "agent-notes"
    notes.mkdir(parents=True, exist_ok=True)
    (notes / ".gitkeep").touch()


def test_valid_seed_passes(tmp_repo, minimal_manifest):
    """A complete, consistent seed should pass validation."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    write_valid_seed(tmp_repo, minimal_manifest)

    from validate_seed import validate
    issues = validate(str(tmp_repo))
    assert issues == [], f"Expected no issues, got: {issues}"


def test_missing_domain_file_fails(tmp_repo, minimal_manifest):
    """If a route references a domain_file that doesn't exist, validation fails."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    write_valid_seed(tmp_repo, minimal_manifest)
    generated = tmp_repo / "agent-memory-seed" / "generated"
    (generated / "domain-automation-control.md").unlink()

    from validate_seed import validate
    issues = validate(str(tmp_repo))
    assert any("domain-automation-control.md" in i for i in issues)


def test_route_in_nav_missing_from_manifest_fails(tmp_repo, minimal_manifest):
    """Route in navigation.md not in manifest routes should fail."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    write_valid_seed(tmp_repo, minimal_manifest)
    generated = tmp_repo / "agent-memory-seed" / "generated"

    nav = (generated / "navigation.md").read_text()
    nav += "\n### route_id: ghost-route\ndomain_id: x\ndomain_file: missing.md\n"
    (generated / "navigation.md").write_text(nav)

    from validate_seed import validate
    issues = validate(str(tmp_repo))
    assert any("ghost-route" in i for i in issues)


def test_agent_notes_not_modified_passes(tmp_repo, minimal_manifest):
    """agent-notes/ can have content — validation only checks generated/."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    write_valid_seed(tmp_repo, minimal_manifest)
    notes = tmp_repo / "agent-memory-seed" / "agent-notes"
    (notes / "qa-patterns.md").write_text("# Q&A Patterns\n")

    from validate_seed import validate
    issues = validate(str(tmp_repo))
    assert issues == []


def test_missing_section_in_depends_on_fails(tmp_repo, minimal_manifest):
    """output depends_on_sections referencing a missing section should fail."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    manifest = json.loads(json.dumps(minimal_manifest))
    manifest["outputs"]["navigation.md"]["depends_on_sections"] = ["hooks.md::nonexistent-section"]
    write_valid_seed(tmp_repo, manifest)

    from validate_seed import validate
    issues = validate(str(tmp_repo))
    assert any("nonexistent-section" in i for i in issues)


def test_out_of_scope_file_modification_fails(tmp_repo, minimal_manifest):
    """Files modified outside agent-memory-seed/generated/ should fail validation."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    write_valid_seed(tmp_repo, minimal_manifest)

    from validate_seed import validate
    changed_files = ["docs/hooks.md", "agent-memory-seed/generated/navigation.md"]
    issues = validate(str(tmp_repo), changed_files=changed_files)
    assert any("out-of-scope" in i or "docs/hooks.md" in i for i in issues)


def test_agent_notes_modification_fails(tmp_repo, minimal_manifest):
    """A file added to agent-notes/ appearing in changed_files should fail validation."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    write_valid_seed(tmp_repo, minimal_manifest)

    from validate_seed import validate
    changed_files = [
        "agent-memory-seed/generated/navigation.md",
        "agent-memory-seed/agent-notes/qa-patterns.md",
    ]
    issues = validate(str(tmp_repo), changed_files=changed_files)
    assert any("agent-notes" in i for i in issues)


def test_route_rename_detected(tmp_repo, minimal_manifest):
    """A route_id disappearing from prior manifest while a new one appears should flag as possible rename."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    write_valid_seed(tmp_repo, minimal_manifest)

    new_manifest = json.loads(json.dumps(minimal_manifest))
    new_manifest["routes"]["setup-hooks"] = new_manifest["routes"].pop("configure-hooks")
    generated = tmp_repo / "agent-memory-seed" / "generated"
    (generated / "seed_manifest.json").write_text(json.dumps(new_manifest))

    nav = (generated / "navigation.md").read_text()
    nav = nav.replace("configure-hooks", "setup-hooks")
    (generated / "navigation.md").write_text(nav)

    from validate_seed import validate
    issues = validate(str(tmp_repo), prior_route_ids=set(minimal_manifest["routes"].keys()))
    assert any("rename" in i.lower() or "setup-hooks" in i for i in issues)
