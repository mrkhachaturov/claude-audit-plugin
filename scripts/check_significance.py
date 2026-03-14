#!/usr/bin/env python3
"""
Check whether doc changes are significant enough to trigger a seed rebuild.

Inputs:
  - agent-memory-seed/generated/seed_manifest.json  (prior headings + section hashes)
  - git diff -U0 HEAD~1 -- docs/                    (changed files and heading diffs)

Outputs GitHub Actions output variables to stdout (append to $GITHUB_OUTPUT):
  rebuild=true/false
  affected_routes=comma,separated
  affected_domains=comma,separated
  changed_docs=comma,separated

Rebuild triggers (v1 — heading-change + threshold detection):
  - Any new doc file added to docs/
  - Any heading changed in a tracked doc (detected via +/- lines starting with #)
  - 30+ lines changed across docs/ in a single run

Usage: python scripts/check_significance.py >> $GITHUB_OUTPUT
"""

import json
import re
import subprocess
import sys
from pathlib import Path

from slugify import slugify_heading


LINES_CHANGED_THRESHOLD = 30


def load_seed_manifest(repo_root: str) -> dict:
    """Load seed_manifest.json, or return empty dict if missing."""
    path = Path(repo_root) / "agent-memory-seed" / "generated" / "seed_manifest.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def parse_git_diff(diff_output: str) -> dict:
    """
    Parse unified diff output (git diff -U0) into per-file change info.

    Returns:
        {
            "filename.md": {
                "is_new": bool,
                "lines_changed": int,
                "changed_headings": [str],   # raw heading text from +/- lines
            }
        }

    Only files under docs/ are included.
    """
    result = {}
    current_file = None

    for line in diff_output.splitlines():
        if line.startswith("diff --git"):
            match = re.search(r'b/docs/(.+\.md)$', line)
            if match:
                current_file = match.group(1)
                result[current_file] = {
                    "is_new": False,
                    "lines_changed": 0,
                    "changed_headings": [],
                }
            else:
                current_file = None
            continue

        if current_file is None:
            continue

        if line.startswith("new file mode"):
            result[current_file]["is_new"] = True

        if line.startswith("+") and not line.startswith("+++"):
            result[current_file]["lines_changed"] += 1
            heading_match = re.match(r'^\+#{1,4}\s+(.+)', line)
            if heading_match:
                result[current_file]["changed_headings"].append(heading_match.group(1).strip())

        elif line.startswith("-") and not line.startswith("---"):
            result[current_file]["lines_changed"] += 1
            heading_match = re.match(r'^-#{1,4}\s+(.+)', line)
            if heading_match:
                result[current_file]["changed_headings"].append(heading_match.group(1).strip())

    return result


def identify_affected_routes_and_domains(
    changed_files: dict, seed_manifest: dict
) -> tuple[list, list]:
    """
    Return affected route_ids and domain_ids given per-file change info and the manifest.

    A doc is considered to affect its routes when:
    - It is new (not yet in the manifest), or
    - Any of its known headings changed (compared as slugs), or
    - Its total lines_changed >= LINES_CHANGED_THRESHOLD
    """
    if not seed_manifest:
        return [], []

    affected_routes = set()
    affected_domains = set()
    routes = seed_manifest.get("routes", {})
    source_docs = seed_manifest.get("source_docs", {})

    for filename, change_info in changed_files.items():
        if filename not in source_docs:
            # Unknown or new doc — conservatively mark all routes affected
            for route_id, route in routes.items():
                affected_routes.add(route_id)
                affected_domains.add(route["domain_id"])
            continue

        doc_meta = source_docs[filename]
        known_heading_slugs = {slugify_heading(h) for h in doc_meta.get("headings", [])}
        changed_heading_slugs = {slugify_heading(h) for h in change_info["changed_headings"]}
        heading_overlap = known_heading_slugs & changed_heading_slugs

        if heading_overlap or change_info["lines_changed"] >= LINES_CHANGED_THRESHOLD or change_info["is_new"]:
            for section_id, section in doc_meta.get("sections", {}).items():
                for route_id in section.get("routes", []):
                    if route_id in routes:
                        affected_routes.add(route_id)
                        affected_domains.add(routes[route_id]["domain_id"])

    return sorted(affected_routes), sorted(affected_domains)


def analyze_changes(repo_root: str, git_diff: str, seed_manifest: dict) -> dict:
    """
    Core analysis function — separated from I/O for testability.

    Returns dict with keys: rebuild, affected_routes, affected_domains, changed_docs
    """
    changed_files = parse_git_diff(git_diff)

    if not changed_files:
        return {
            "rebuild": False,
            "affected_routes": [],
            "affected_domains": [],
            "changed_docs": []
        }

    should_rebuild = False
    for filename, info in changed_files.items():
        if info["is_new"] or info["changed_headings"]:
            should_rebuild = True
            break
        if info["lines_changed"] >= LINES_CHANGED_THRESHOLD:
            should_rebuild = True
            break

    affected_routes, affected_domains = identify_affected_routes_and_domains(
        changed_files, seed_manifest
    )

    return {
        "rebuild": should_rebuild,
        "affected_routes": affected_routes,
        "affected_domains": affected_domains,
        "changed_docs": sorted(changed_files.keys())
    }


def main():
    repo_root = Path(__file__).parent.parent
    seed_manifest = load_seed_manifest(str(repo_root))

    try:
        result = subprocess.run(
            ["git", "diff", "-U0", "HEAD~1", "--", "docs/"],
            capture_output=True, text=True, cwd=repo_root
        )
        git_diff = result.stdout
    except Exception as e:
        print(f"Warning: could not run git diff: {e}", file=sys.stderr)
        git_diff = ""

    analysis = analyze_changes(str(repo_root), git_diff, seed_manifest)

    print(f"rebuild={'true' if analysis['rebuild'] else 'false'}")
    print(f"affected_routes={','.join(analysis['affected_routes'])}")
    print(f"affected_domains={','.join(analysis['affected_domains'])}")
    print(f"changed_docs={','.join(analysis['changed_docs'])}")


if __name__ == "__main__":
    main()
