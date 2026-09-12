"""Generate README.md for all 12 category repositories in Skillary v4.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skillary import LABELS, get_version, iter_skills, repo_paths, repo_root

OWN_DIR = repo_root()

ACRONYMS = {
    "Ai": "AI", "Api": "API", "Cd": "CD", "Ci": "CI", "Cms": "CMS",
    "Crm": "CRM", "Ecommerce": "eCommerce", "Esg": "ESG", "Finops": "FinOps",
    "Graphql": "GraphQL", "Iac": "IaC", "Ios": "iOS", "It": "IT", "Mcp": "MCP",
    "N8N": "N8n", "Okr": "OKR", "Pr": "PR", "Qa": "QA", "Seo": "SEO",
    "Sop": "SOP", "Sre": "SRE", "Ui": "UI", "Ux": "UX", "Zk": "ZK",
}


def title_for(slug: str) -> str:
    words = slug.replace("-", " ").title().split()
    return " ".join(ACRONYMS.get(w, w) for w in words)


def main() -> int:
    version = get_version()
    root = repo_root()

    catalog: dict[str, dict[str, list]] = {}
    for skill in iter_skills(root):
        repo_dict = catalog.setdefault(skill.repo, {})
        group_list = repo_dict.setdefault(skill.group or "General", [])
        group_list.append(skill)

    for repo_path in repo_paths(root):
        repo = repo_path.name
        if repo not in catalog:
            continue
        groups = catalog[repo]
        display_name = LABELS.get(repo, repo)
        total_skills = sum(len(skills) for skills in groups.values())

        lines = [
            f"# {repo}",
            "",
            f"{display_name} skills collection for Claude Code, Cursor, Codex, Gemini CLI, and `npx skills` — part of [Skillary](https://github.com/poorvith-mp/skillary) by [Poorvith M P](https://github.com/poorvith-mp).",
            "",
            f"- **Version**: `v{version}`",
            f"- **Total Skills**: `{total_skills}`",
            "- **License**: MIT",
            "- **Hub Repository**: [poorvith-mp/skillary](https://github.com/poorvith-mp/skillary)",
            "",
            "## Install",
            "",
            "Install the entire collection via `npx skills`:",
            "```bash",
            f"npx skills add poorvith-mp/{repo}",
            "```",
            "",
            "Or install individual skills directly:",
            "```bash",
            f"npx skills add poorvith-mp/{repo} --skill <skill-id>",
            "```",
            "",
            "## Skills in this Collection",
            "",
        ]

        for group, skills in groups.items():
            lines.append(f"### {group}")
            lines.append("")
            lines.append("| Skill ID | Title | Description | Reviewed |")
            lines.append("|:---------|:------|:------------|:---------|")
            for s in sorted(skills, key=lambda x: x.slug):
                slug = s.slug
                title = title_for(slug)
                desc = s.description.replace("|", "\\|")
                reviewed = s.last_reviewed or "—"
                lines.append(f"| `{slug}` | [{title}](skills/{slug}/SKILL.md) | {desc} | {reviewed} |")
            lines.append("")

        lines.extend([
            "## License",
            "",
            "MIT © [Poorvith M P](https://github.com/poorvith-mp)",
            "",
        ])

        readme_path = repo_path / "README.md"
        readme_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"Generated {readme_path} ({total_skills} skills)")

    return 0


if __name__ == "__main__":
    main()
