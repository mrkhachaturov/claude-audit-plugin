"""Shared fixtures for claude-audit plugin tests."""
import json
import pytest
from pathlib import Path


@pytest.fixture
def tmp_repo(tmp_path):
    """A minimal fake repo structure for testing scripts."""
    # Create docs/
    docs = tmp_path / "docs"
    docs.mkdir()

    # Create agent-memory-seed/generated/
    seed_generated = tmp_path / "agent-memory-seed" / "generated"
    seed_generated.mkdir(parents=True)

    # Create agent-memory-seed/agent-notes/
    agent_notes = tmp_path / "agent-memory-seed" / "agent-notes"
    agent_notes.mkdir()
    (agent_notes / ".gitkeep").touch()

    return tmp_path


@pytest.fixture
def minimal_manifest():
    """A minimal valid seed_manifest.json."""
    return {
        "schema_version": 1,
        "seed_version": "2026-03-14T00:00:00Z",
        "source_docs": {
            "hooks.md": {
                "file_hash": "abc123",
                "headings_hash": "def456",
                "headings": ["Overview", "Event Types"],
                "sections": {
                    "event-types": {
                        "hash": "ghi789",
                        "start_heading": "Event Types",
                        "end_heading": "Tool Events",
                        "domains": ["automation-control"],
                        "routes": ["configure-hooks"]
                    }
                }
            }
        },
        "routes": {
            "configure-hooks": {
                "domain_id": "automation-control",
                "domain_file": "domain-automation-control.md",
                "primary_doc": "hooks.md",
                "secondary_doc": "hooks-guide.md",
                "depends_on_sections": ["hooks.md::event-types"]
            }
        },
        "outputs": {
            "domain-automation-control.md": {
                "content_hash": "jkl012",
                "depends_on_sections": ["hooks.md::event-types"]
            },
            "navigation.md": {
                "content_hash": "mno345",
                "depends_on_routes": ["configure-hooks"]
            }
        }
    }
