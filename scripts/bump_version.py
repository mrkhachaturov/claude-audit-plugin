#!/usr/bin/env python3
"""
Bump the patch version in .claude-plugin/plugin.json and prepend a CHANGELOG entry.

Only bumps if there are actual changed docs (passed via CHANGED_DOCS env var).

Usage: python scripts/bump_version.py
       CHANGED_DOCS=hooks.md,skills.md python scripts/bump_version.py
"""

import json
import os
import sys
from datetime import date
from pathlib import Path


def bump(repo_root: str, changed_docs: list[str]) -> None:
    """
    Increment patch version and update CHANGELOG. No-op if changed_docs is empty.
    """
    if not changed_docs:
        print("No changed docs — skipping version bump")
        return

    root = Path(repo_root)
    plugin_json_path = root / ".claude-plugin" / "plugin.json"
    changelog_path = root / "CHANGELOG.md"

    # Load and bump version
    plugin = json.loads(plugin_json_path.read_text())
    old_version = plugin["version"]
    version_parts = plugin["version"].split(".")
    version_parts[2] = str(int(version_parts[2]) + 1)
    new_version = ".".join(version_parts)
    plugin["version"] = new_version
    plugin_json_path.write_text(json.dumps(plugin, indent=2) + "\n")

    # Prepend CHANGELOG entry
    today = date.today().strftime("%Y-%m-%d")
    docs_list = "\n".join(f"  - {doc}" for doc in sorted(changed_docs))
    new_entry = (
        f"## [{new_version}] — {today}\n\n"
        f"### Changed\n"
        f"- Auto-rebuilt knowledge seed from updated docs:\n"
        f"{docs_list}\n\n"
        f"---\n\n"
    )

    existing = changelog_path.read_text()
    # Insert after the first line (the # Changelog header)
    lines = existing.split("\n", 2)
    if len(lines) >= 2:
        updated = lines[0] + "\n\n" + new_entry + ("\n".join(lines[1:])).lstrip("\n")
    else:
        updated = existing + "\n" + new_entry

    changelog_path.write_text(updated)
    print(f"Bumped version {old_version} -> {new_version}")


def main():
    repo_root = Path(__file__).parent.parent
    changed_docs_env = os.environ.get("CHANGED_DOCS", "")
    changed_docs = [d.strip() for d in changed_docs_env.split(",") if d.strip()]
    bump(str(repo_root), changed_docs)


if __name__ == "__main__":
    main()
