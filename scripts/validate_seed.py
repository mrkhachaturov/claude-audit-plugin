#!/usr/bin/env python3
"""
Validate seed output after Codex rebuild.

Checks:
1. No files modified outside agent-memory-seed/generated/ (via changed_files param or git diff)
1b. agent-notes/ not touched
2. All route_ids in navigation.md exist in manifest routes
3. All domain_file references in routes resolve to files in generated/
4. All section IDs in source_docs are valid slugs of the doc's headings (slugify contract)
4b. All depends_on_sections in outputs reference sections that exist in source_docs
5. No route IDs were silently renamed (compare against prior_route_ids)

Exit 0 = valid. Exit 1 = issues found (printed to stdout).

Usage: python scripts/validate_seed.py
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from slugify import slugify_headings


def get_changed_files(repo_root: str) -> list[str]:
    """Return list of files changed vs HEAD using git diff --name-only."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True, text=True, cwd=repo_root
        )
        return [f.strip() for f in result.stdout.splitlines() if f.strip()]
    except Exception:
        return []


def get_prior_route_ids(repo_root: str) -> set[str]:
    """Return route_ids from HEAD's seed_manifest.json (before Codex ran)."""
    try:
        result = subprocess.run(
            ["git", "show", "HEAD:agent-memory-seed/generated/seed_manifest.json"],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode == 0:
            prior = json.loads(result.stdout)
            return set(prior.get("routes", {}).keys())
    except Exception:
        pass
    return set()


def validate(
    repo_root: str,
    changed_files: list[str] | None = None,
    prior_route_ids: set[str] | None = None,
    allowed_prefixes: list[str] | None = None,
) -> list[str]:
    """
    Run all validation checks. Returns list of issue strings (empty = valid).

    Args:
        repo_root: Path to repository root.
        changed_files: Optional explicit list of changed file paths (relative to repo root).
                       If None, determined via git diff --name-only HEAD.
        prior_route_ids: Optional set of route_ids from before the rebuild.
                         If None, loaded from HEAD's seed_manifest.json via git show.
        allowed_prefixes: Optional list of extra path prefixes that are allowed to be
                          modified without failing validation (for example `docs/`).
    """
    root = Path(repo_root)
    generated = root / "agent-memory-seed" / "generated"
    issues = []
    allowed_prefixes = allowed_prefixes or []

    # Check 1: No files modified outside agent-memory-seed/generated/
    if changed_files is None:
        changed_files = get_changed_files(repo_root)
    allowed_prefix = "agent-memory-seed/generated/"
    for f in changed_files:
        if f.startswith(allowed_prefix):
            continue
        if any(f.startswith(extra_prefix) for extra_prefix in allowed_prefixes):
            continue
        else:
            issues.append(
                f"out-of-scope modification: '{f}' is outside '{allowed_prefix}'"
            )

    # Check 1b: agent-notes/ must not be touched
    agent_notes_prefix = "agent-memory-seed/agent-notes/"
    for f in changed_files:
        if f.startswith(agent_notes_prefix):
            issues.append(
                f"agent-notes/ modification: '{f}' — agent-notes/ is agent-owned and must never be modified by CI or scripts"
            )

    # Load manifest
    manifest_path = generated / "seed_manifest.json"
    if not manifest_path.exists():
        return issues + ["seed_manifest.json not found in agent-memory-seed/generated/"]

    manifest = json.loads(manifest_path.read_text())
    routes = manifest.get("routes", {})
    source_docs = manifest.get("source_docs", {})
    outputs = manifest.get("outputs", {})

    # Check 2: All route_ids in navigation.md exist in manifest routes (and vice versa)
    nav_path = generated / "navigation.md"
    if nav_path.exists():
        nav_content = nav_path.read_text()
        nav_route_ids = set(re.findall(r'### route_id: (\S+)', nav_content))
        manifest_route_ids = set(routes.keys())

        for rid in nav_route_ids - manifest_route_ids:
            issues.append(f"route_id '{rid}' in navigation.md not found in manifest routes")

        for rid in manifest_route_ids - nav_route_ids:
            issues.append(f"route_id '{rid}' in manifest routes not found in navigation.md")
    else:
        issues.append("navigation.md not found in agent-memory-seed/generated/")

    # Check 3: All domain_file references in routes resolve to real files
    for route_id, route in routes.items():
        domain_file = route.get("domain_file")
        if domain_file and not (generated / domain_file).exists():
            issues.append(
                f"route '{route_id}' references domain_file '{domain_file}' which does not exist"
            )

    # Check 4: All section IDs in source_docs are valid slugs of the doc's headings
    for doc_name, doc_meta in source_docs.items():
        valid_slugs = set(slugify_headings(doc_meta.get("headings", [])))
        for section_id in doc_meta.get("sections", {}):
            if section_id not in valid_slugs:
                issues.append(
                    f"source_docs['{doc_name}'].sections['{section_id}'] is not a valid slug "
                    f"of any heading in '{doc_name}' — section IDs must be derived via "
                    f"slugify_headings(headings)"
                )

    # Check 4b: All depends_on_sections in outputs reference sections that exist in source_docs
    for output_file, output_meta in outputs.items():
        for section_ref in output_meta.get("depends_on_sections", []):
            parts = section_ref.split("::")
            if len(parts) != 2:
                issues.append(f"Invalid section ref '{section_ref}' in outputs['{output_file}']")
                continue
            doc_name, section_id = parts
            if doc_name not in source_docs:
                issues.append(
                    f"outputs['{output_file}'] depends on '{doc_name}' not in source_docs"
                )
            elif section_id not in source_docs[doc_name].get("sections", {}):
                issues.append(
                    f"outputs['{output_file}'] depends on section '{section_id}' "
                    f"not found in source_docs['{doc_name}'].sections"
                )

    # Check 5: No route IDs were silently renamed
    if prior_route_ids is None:
        prior_route_ids = get_prior_route_ids(repo_root)
    if prior_route_ids:
        current_route_ids = set(routes.keys())
        removed = prior_route_ids - current_route_ids
        added = current_route_ids - prior_route_ids
        if removed and added:
            issues.append(
                f"possible route rename(s): removed={sorted(removed)}, "
                f"added={sorted(added)} — preserved route_ids are required; "
                f"use new IDs only for genuinely new routes"
            )

    return issues


def main():
    parser = argparse.ArgumentParser(description="Validate generated knowledge seed output.")
    parser.add_argument(
        "--allow-prefix",
        action="append",
        default=[],
        help="Additional changed-file prefix allowed during validation, e.g. docs/",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    issues = validate(str(repo_root), allowed_prefixes=args.allow_prefix)

    if issues:
        print("Seed validation FAILED:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("Seed validation PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
