"""Structured catalog loader for Skillary v4.

Reads personal-brand/ideas/skillary/v4-catalog.md and exposes the authoritative
277-skill, 12-repo catalog specification.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_NAME_MAP = {
    "Developer": "skills-developer",
    "Marketing": "skills-marketing",
    "Game Development": "skills-gamedev",
    "Business & Operations": "skills-business",
    "Design": "skills-design",
    "Education & Research": "skills-education",
    "Agents & Automation": "skills-agents",
    "Personal & Career": "skills-personal",
    "Writing": "skills-writing",
    "Sales & Support": "skills-sales",
    "Finance": "skills-finance",
    "Legal & Compliance": "skills-legal",
}

REPO_DISPLAY_MAP = {v: k for k, v in REPO_NAME_MAP.items()}


def get_catalog_path() -> Path:
    base = Path(__file__).resolve().parent.parent.parent.parent
    path = base / "personal-brand" / "ideas" / "skillary" / "v4-catalog.md"
    if not path.exists():
        raise FileNotFoundError(f"Catalog file not found at {path}")
    return path


def load_v4_catalog() -> dict[str, dict[str, list[dict[str, str]]]]:
    """Returns {repo_name: {group_name: [{'slug': ..., 'description': ...}]}}"""
    text = get_catalog_path().read_text(encoding="utf-8")
    current_repo = None
    current_group = None
    catalog: dict[str, dict[str, list[dict[str, str]]]] = {}

    for line in text.splitlines():
        if line.startswith("## 13."):
            break
        m_repo = re.match(r"^## \d+\.\s+(.*?)\s+—\s+(\d+)", line)
        if m_repo:
            section_name = m_repo.group(1).strip()
            current_repo = REPO_NAME_MAP.get(section_name)
            if current_repo:
                catalog[current_repo] = {}
            continue
        m_group = re.match(r"^\*\*([^*]+)\*\*", line)
        if m_group and current_repo:
            current_group = m_group.group(1).strip()
            if current_group not in catalog[current_repo]:
                catalog[current_repo][current_group] = []
            continue
        m_skill = re.match(r"^\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|", line)
        if m_skill and current_repo and current_group:
            slug = m_skill.group(1).strip()
            desc = m_skill.group(2).strip()
            catalog[current_repo][current_group].append({"slug": slug, "description": desc})

    return catalog


def get_all_v4_skills() -> list[dict[str, str]]:
    """Returns flat list of all 277 skills with repo, group, slug, description."""
    catalog = load_v4_catalog()
    all_skills = []
    for repo, groups in catalog.items():
        for group, skills in groups.items():
            for s in skills:
                all_skills.append({
                    "repo": repo,
                    "group": group,
                    "slug": s["slug"],
                    "description": s["description"],
                })
    return all_skills


if __name__ == "__main__":
    cat = load_v4_catalog()
    total = sum(len(skills) for groups in cat.values() for skills in groups.values())
    print(f"Loaded {len(cat)} repos, {total} total skills.")
    for repo, groups in cat.items():
        count = sum(len(skills) for skills in groups.values())
        print(f"  {repo}: {count} skills across {len(groups)} groups")
