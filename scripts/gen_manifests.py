"""Generate the plugin and marketplace manifests.

Thirteen JSON files with skill counts in them is thirteen things that drift.
They are generated from what is actually on disk instead, same as the index.

    python scripts/gen_manifests.py --check
    python scripts/gen_manifests.py --write
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

from build_index import LABELS, OWNER, collect  # noqa: E402
from skillary import get_version, repo_root  # noqa: E402

MARKETPLACE = "skillary"
VERSION = get_version()
AUTHOR = {"name": "Poorvith M P", "url": f"https://github.com/{OWNER}"}

# What each category is for, in the words someone browsing a marketplace needs.
BLURBS = {
    "skills-developer": "Software engineering: architecture, security, CI/CD, data, mobile, SRE and debugging.",
    "skills-marketing": "Campaigns, SEO and AEO, social, paid media, lifecycle email and content.",
    "skills-gamedev": "Game development across Unity, Unreal, and Blender, plus art and audio pipelines.",
    "skills-business": "Operations, strategy, product management, governance and freelancing.",
    "skills-design": "Visual and product design: design systems, UX, brand, typography and accessibility.",
    "skills-education": "Teaching, learning design, study systems, research and academic writing.",
    "skills-agents": "Agent and automation infrastructure: multi-agent protocols, tool curation, evals and runtimes.",
    "skills-personal": "Personal productivity, knowledge management, career tracks and life systems.",
    "skills-writing": "Long-form and professional writing: books, technical docs, screenplays and copy.",
    "skills-sales": "Sales execution, discovery, proposals, pipeline health and customer retention.",
    "skills-finance": "FP&A, treasury, tax, cap tables, investment research and bookkeeping.",
    "skills-legal": "Legal, compliance, data privacy, contracts, and regulatory operations.",
}

KEYWORDS = {
    "skills-developer": ["engineering", "devops", "security", "architecture"],
    "skills-marketing": ["marketing", "seo", "content", "growth"],
    "skills-gamedev": ["gamedev", "unity", "unreal", "blender"],
    "skills-business": ["business", "operations", "product", "strategy"],
    "skills-design": ["design", "ux", "accessibility", "brand"],
    "skills-education": ["education", "learning", "research"],
    "skills-agents": ["agents", "automation", "evals", "mcp"],
    "skills-personal": ["productivity", "pkm", "career"],
    "skills-writing": ["writing", "documentation", "copywriting"],
    "skills-sales": ["sales", "pipeline", "discovery", "bids"],
    "skills-finance": ["finance", "fpa", "accounting", "tax"],
    "skills-legal": ["legal", "compliance", "privacy", "contracts"],
}


def plugin_manifest(repo: str, count: int) -> dict:
    # `skills` is deliberately omitted: skills/ at the plugin root is
    # auto-discovered, and an explicit list is one more thing to drift.
    return {
        "name": repo,
        "displayName": f"{LABELS[repo]} Skills",
        "version": VERSION,
        "description": f"{count} {LABELS[repo].lower()} skills. {BLURBS[repo]}",
        "author": AUTHOR,
        "homepage": f"https://github.com/{OWNER}/{MARKETPLACE}",
        "repository": f"https://github.com/{OWNER}/{repo}",
        "license": "MIT",
        "keywords": KEYWORDS[repo] + ["agent-skills"],
    }


def marketplace_manifest(grouped: dict) -> dict:
    total = sum(len(v) for v in grouped.values())
    return {
        "name": MARKETPLACE,
        "owner": AUTHOR,
        "metadata": {
            "description": f"{total} Agent Skills across {len(grouped)} domains, "
            "every one validated for trigger precision.",
            "version": VERSION,
        },
        # Each category lives in its own repo, so users install only what they
        # want and each versions independently.
        "plugins": [
            {
                "name": repo,
                "source": {"source": "github", "repo": f"{OWNER}/{repo}"},
                "description": f"{len(items)} skills. {BLURBS[repo]}",
                "category": LABELS[repo].lower().replace(" & ", "-").replace(" ", "-"),
            }
            for repo, items in grouped.items()
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    hub = Path(__file__).resolve().parent.parent
    grouped = collect()
    root = repo_root()

    targets: list[tuple[Path, dict]] = [
        (hub / ".claude-plugin" / "marketplace.json", marketplace_manifest(grouped))
    ]
    for repo, items in grouped.items():
        targets.append((root / repo / ".claude-plugin" / "plugin.json", plugin_manifest(repo, len(items))))

    drift = 0
    for path, data in targets:
        text = json.dumps(data, indent=2) + "\n"
        current = path.read_text(encoding="utf-8") if path.exists() else None
        # Compare parsed JSON, not bytes: line endings differ by platform and
        # would otherwise report permanent drift.
        if current is not None and json.loads(current) == data:
            continue
        drift += 1
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            print(f"wrote {path.relative_to(root)}")
        else:
            print(f"DRIFT: {path.relative_to(root)}")

    if not drift:
        print(f"manifests current: 1 marketplace, {len(grouped)} plugins")
        return 0
    return 0 if args.write else 1


if __name__ == "__main__":
    raise SystemExit(main())
