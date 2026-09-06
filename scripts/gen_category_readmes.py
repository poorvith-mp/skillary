"""Generate README.md for all 12 category repositories in Skillary v4.
"""

from __future__ import annotations

from pathlib import Path
from v4_catalog_data import load_v4_catalog, REPO_DISPLAY_MAP

OWN_DIR = Path("c:/Users/poorv/projects/own")


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


def main() -> int:
    catalog = load_v4_catalog()

    for repo, groups in catalog.items():
        repo_dir = OWN_DIR / repo
        if not repo_dir.is_dir():
            print(f"Skipping {repo} (dir not found)")
            continue

        display_name = REPO_DISPLAY_MAP.get(repo, repo)
        total_skills = sum(len(skills) for skills in groups.values())

        lines = [
            f"# {repo}",
            "",
            f"{display_name} skills collection for Claude Code, Cursor, Codex, Gemini CLI, and `npx skills` — part of [Skillary](https://github.com/poorvith-mp/skillary) by [Poorvith M P](https://github.com/poorvith-mp).",
            "",
            "- **Version**: `v3.0.0`",
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
            lines.append("| Skill ID | Title | Description |")
            lines.append("|:---------|:------|:------------|")
            for s in sorted(skills, key=lambda x: x["slug"]):
                slug = s["slug"]
                title = title_for(slug)
                desc = s["description"].replace("|", "\\|")
                lines.append(f"| `{slug}` | [{title}](skills/{slug}/SKILL.md) | {desc} |")
            lines.append("")

        lines.extend([
            "## License",
            "",
            "MIT © [Poorvith M P](https://github.com/poorvith-mp)",
            "",
        ])

        readme_path = repo_dir / "README.md"
        readme_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"Generated {readme_path} ({total_skills} skills)")

    return 0


if __name__ == "__main__":
    main()
