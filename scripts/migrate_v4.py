"""End-to-end migration script for Skillary v4.

Transforms the Skillary ecosystem from v3 (307 skills across 12 repos + specialized + meta)
to v4 (277 skills across 12 modern repos, plus standalone skillary-agents).
"""

from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path

from v4_catalog_data import load_v4_catalog, get_all_v4_skills, REPO_NAME_MAP
from v4_skill_mapper import OLD_TO_NEW

OWN_DIR = Path("c:/Users/poorv/projects/own")
HUB_DIR = OWN_DIR / "skillary"


def title_for(slug: str) -> str:
    acronyms = {
        "Ai": "AI", "Api": "API", "Cd": "CD", "Ci": "CI", "Cms": "CMS",
        "Crm": "CRM", "Ecommerce": "eCommerce", "Esg": "ESG", "Finops": "FinOps",
        "Graphql": "GraphQL", "Iac": "IaC", "Ios": "iOS", "It": "IT", "Mcp": "MCP",
        "N8N": "N8n", "Okr": "OKR", "Pr": "PR", "Qa": "QA", "Seo": "SEO",
        "Sop": "SOP", "Sre": "SRE", "Ui": "UI", "Ux": "UX", "Zk": "ZK",
    }
    words = slug.replace("-", " ").title().split()
    return " ".join(acronyms.get(w, w) for w in words)


def collect_existing_v3_skills() -> dict[str, tuple[str, Path]]:
    """slug -> (repo_name, path)"""
    skills = {}
    for rdir in sorted(OWN_DIR.glob("skills-*")):
        s_dir = rdir / "skills"
        if not s_dir.is_dir():
            continue
        for p in s_dir.iterdir():
            if p.is_dir() and (p / "SKILL.md").is_file():
                skills[p.name] = (rdir.name, p)
    return skills


def generate_greenfield_body(slug: str, desc: str, group: str, repo: str) -> str:
    title = title_for(slug)
    legal_disclaimer = ""
    if repo == "skills-legal":
        legal_disclaimer = (
            "\n> [!IMPORTANT]\n"
            "> **Licensed-Review Requirement**: This skill provides structured analysis, templates, and issue identification. "
            "It does not provide licensed legal counsel, formal legal opinions, or replace attorney review for your specific jurisdiction.\n"
        )

    return f"""# {title}

{desc}.
{legal_disclaimer}
## Process

1. **Intake & Scope Definition**
   - Identify specific objectives, inputs, constraints, and operational context.
   - Inspect existing project documentation, configurations, or relevant repository assets.

2. **Analysis & Strategic Formulation**
   - Evaluate options against best practices, security posture, and domain requirements.
   - Deconstruct complex components into discrete, actionable phases.

3. **Execution & Synthesis**
   - Produce structured, production-grade deliverables matching the required format.
   - Ground all recommendations in concrete project evidence rather than abstract generalities.

4. **Review & Refinement**
   - Validate against the verification checklist and domain edge cases.
   - Highlight open questions, explicit trade-offs, and next milestones.

## Deliverable & Output Format

### 📋 Executive Summary
- **Objective:** Key goal addressed
- **Status:** Complete / Action Required
- **Primary Recommendation:** Core actionable conclusion

### 🛠️ Detailed Implementation / Analysis
- Concrete technical, operational, or strategic specifications.
- Clear code, configuration, or documentation blocks where applicable.

### 📌 Decisions & Next Steps
- [ ] Immediate action items with designated owners.
- [ ] Required dependencies or prerequisite milestones.

## Instructions & Operating Rules

- Lead directly with actionable findings and structured results.
- Never introduce speculative abstractions or unrequested complexity.
- Maintain consistency with existing architecture and naming conventions.
- Provide explicit rationales for non-obvious trade-offs.

## Verification & Quality Checklist

- [ ] Deliverable directly satisfies all stated user requirements and criteria.
- [ ] Edge cases, boundary conditions, and error states are addressed.
- [ ] Output contains zero placeholder tokens, broken references, or unverified claims.
- [ ] All cross-references and formatting comply with repository conventions.

## Anti-Patterns & Constraints

- **NEVER** output generic boilerplate without grounding in specific project inputs.
- **NEVER** silently omit unresolved contradictions or unverified assumptions.
- **NEVER** make unrequested modifications outside the stated deliverable boundary.
"""


def generate_routing_yaml(slug: str, desc: str, repo: str, neighbor_slug: str | None = None) -> str:
    clean_desc = desc.split(":")[0].lower()
    title_lower = slug.replace("-", " ")
    
    expect_target = neighbor_slug or "general-inquiry"
    
    return f"""should_fire:
  - "help with {title_lower}"
  - "{clean_desc}"
  - "run {slug} workflow"
should_not_fire:
  - prompt: "unrelated query outside this domain"
    expect: {expect_target}
"""


def main() -> int:
    print("=== Starting Skillary v4 Migration ===")
    
    existing_skills = collect_existing_v3_skills()
    print(f"Collected {len(existing_skills)} existing v3 skills.")

    catalog = load_v4_catalog()
    all_v4_skills = get_all_v4_skills()
    print(f"Target catalog: {len(all_v4_skills)} skills across {len(catalog)} repos.")

    # Invert OLD_TO_NEW to find sources for target slugs
    target_to_sources = {}
    for old_slug, target_slug in OLD_TO_NEW.items():
        if old_slug in existing_skills:
            target_to_sources.setdefault(target_slug, []).append(old_slug)

    # 1. Migrate / Create all 277 skills in their target repos
    created_count = 0
    migrated_count = 0

    for item in all_v4_skills:
        target_repo = item["repo"]
        target_slug = item["slug"]
        desc = item["description"]
        group = item["group"]

        target_dir = OWN_DIR / target_repo / "skills" / target_slug
        target_dir.mkdir(parents=True, exist_ok=True)
        evals_dir = target_dir / "evals"
        evals_dir.mkdir(exist_ok=True)

        sources = target_to_sources.get(target_slug, [])
        source_skill_info = None

        # Prefer exact match or first listed source
        if target_slug in existing_skills:
            source_skill_info = existing_skills[target_slug]
        elif sources:
            source_skill_info = existing_skills[sources[0]]

        if source_skill_info:
            src_repo, src_path = source_skill_info
            src_skill_md = src_path / "SKILL.md"
            body = ""
            if src_skill_md.is_file():
                raw = src_skill_md.read_text(encoding="utf-8", errors="replace")
                # extract body after frontmatter
                m = re.match(r"\A---\r?\n.*?\r?\n---\r?\n?(.*)\Z", raw, re.S)
                if m:
                    body = m.group(1).strip()
                else:
                    body = raw.strip()

            # If body has old title, ensure H1 title matches new slug
            body = re.sub(r"^#\s+[^\n]+", f"# {title_for(target_slug)}", body, count=1)
            
            # Copy any references/ from source
            src_refs = src_path / "references"
            if src_refs.is_dir() and src_path.resolve() != target_dir.resolve():
                target_refs = target_dir / "references"
                if target_refs.exists():
                    shutil.rmtree(target_refs)
                shutil.copytree(src_refs, target_refs)

            skill_content = f"""---
name: {target_slug}
description: >-
  {desc}
---
{body}
"""
            (target_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")
            migrated_count += 1
        else:
            # Greenfield creation
            body = generate_greenfield_body(target_slug, desc, group, target_repo)
            skill_content = f"""---
name: {target_slug}
description: >-
  {desc}
---
{body}
"""
            (target_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")
            created_count += 1

        # Write routing evals
        routing_yaml = generate_routing_yaml(target_slug, desc, target_repo)
        (evals_dir / "routing.yaml").write_text(routing_yaml, encoding="utf-8")

    print(f"Installed 277 skills: {migrated_count} migrated from existing bodies, {created_count} greenfield.")

    # 2. Write deprecation stubs for any old skills that are not active v4 skills
    stubs_count = 0
    active_v4_by_repo = {}
    for item in all_v4_skills:
        active_v4_by_repo.setdefault(item["repo"], set()).add(item["slug"])

    for old_slug, (old_repo, old_path) in existing_skills.items():
        # Check if this slug is an active v4 skill in this same repo
        if old_slug in active_v4_by_repo.get(old_repo, set()):
            continue  # Active skill, do not stub

        # Find target
        target_slug = OLD_TO_NEW.get(old_slug)
        target_repo = "skillary"
        if target_slug:
            for s in all_v4_skills:
                if s["slug"] == target_slug:
                    target_repo = s["repo"]
                    break

        stub_content = f"""---
name: {old_slug}
description: Moved to {target_slug or 'modernized catalog'} in {target_repo}. Removed in v4.1.
deprecated: true
---
# Deprecated: {old_slug}

This skill has moved to `{target_slug or 'skillary'}` in `{target_repo}` as part of the Skillary v4 catalog modernization.
"""
        stub_skill_md = old_path / "SKILL.md"
        stub_skill_md.write_text(stub_content, encoding="utf-8")
        stubs_count += 1

    print(f"Created/updated {stubs_count} deprecation redirect stubs.")

    # 3. Update VERSION files to 4.0.0 across all repos
    all_repos = list(catalog.keys()) + ["skillary", "skills-specialized", "skills-meta"]
    for r in all_repos:
        rdir = OWN_DIR / r
        if rdir.is_dir():
            (rdir / "VERSION").write_text("4.0.0\n", encoding="utf-8")

    print("Updated VERSION to 4.0.0 across all repositories.")
    return 0


if __name__ == "__main__":
    main()
