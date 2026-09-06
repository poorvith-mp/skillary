"""Check that version numbers are strictly synchronized across all repositories and files.

Asserts:
1. Hub VERSION exists and is non-empty.
2. Every category repo's VERSION matches Hub VERSION.
3. skillary-agents VERSION matches Hub VERSION.
4. Hub README.md matches Hub VERSION.
5. Every category README.md matches Hub VERSION.
6. Hub CHANGELOG.md newest release heading matches Hub VERSION.
7. Hub marketplace.json version matches Hub VERSION.
8. Every category plugin.json version matches Hub VERSION.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CATEGORIES = [
    "developer", "marketing", "gamedev", "business", "design", "education",
    "agents", "personal", "writing", "sales", "finance", "legal"
]


def main() -> int:
    hub = Path(__file__).resolve().parent.parent
    root = hub.parent

    vfile = hub / "VERSION"
    if not vfile.is_file():
        print("ERROR: Hub VERSION file not found", file=sys.stderr)
        return 1

    hub_version = vfile.read_text(encoding="utf-8").strip()
    print(f"Checking version synchronization against Hub VERSION: {hub_version}")

    errors = []

    # 1. Check skillary-agents
    agents_vfile = root / "skillary-agents" / "VERSION"
    if agents_vfile.is_file():
        av = agents_vfile.read_text(encoding="utf-8").strip()
        if av != hub_version:
            errors.append(f"skillary-agents/VERSION ({av}) != {hub_version}")

    # 2. Check each category repo
    for cat in CATEGORIES:
        repo_dir = root / f"skills-{cat}"
        if not repo_dir.is_dir():
            continue

        cv_file = repo_dir / "VERSION"
        if cv_file.is_file():
            cv = cv_file.read_text(encoding="utf-8").strip()
            if cv != hub_version:
                errors.append(f"{repo_dir.name}/VERSION ({cv}) != {hub_version}")

        # Check README.md
        readme = repo_dir / "README.md"
        if readme.is_file():
            text = readme.read_text(encoding="utf-8")
            m = re.search(r"-\s+\*\*Version\*\*:\s+`v?([0-9.]+)`", text)
            if not m or m.group(1) != hub_version:
                errors.append(f"{repo_dir.name}/README.md version ({m.group(1) if m else 'missing'}) != {hub_version}")

        # Check plugin.json
        plugin_file = repo_dir / ".claude-plugin" / "plugin.json"
        if plugin_file.is_file():
            try:
                pj = json.loads(plugin_file.read_text(encoding="utf-8"))
                if pj.get("version") != hub_version:
                    errors.append(f"{repo_dir.name}/plugin.json version ({pj.get('version')}) != {hub_version}")
            except Exception as e:
                errors.append(f"{repo_dir.name}/plugin.json parse error: {e}")

    # 3. Check Hub README.md
    hub_readme = hub / "README.md"
    if hub_readme.is_file():
        text = hub_readme.read_text(encoding="utf-8")
        m = re.search(r"-\s+Version:\s+\*\*v?([0-9.]+)\*\*", text)
        if not m or m.group(1) != hub_version:
            errors.append(f"skillary/README.md version ({m.group(1) if m else 'missing'}) != {hub_version}")

    # 4. Check Hub CHANGELOG.md newest heading
    hub_changelog = hub / "CHANGELOG.md"
    if hub_changelog.is_file():
        text = hub_changelog.read_text(encoding="utf-8")
        m = re.search(r"^##\s+v?([0-9.]+)\s+—", text, re.M)
        if not m or m.group(1) != hub_version:
            errors.append(f"skillary/CHANGELOG.md latest heading ({m.group(1) if m else 'missing'}) != {hub_version}")

    # 5. Check Hub marketplace.json
    market_file = hub / ".claude-plugin" / "marketplace.json"
    if market_file.is_file():
        try:
            mj = json.loads(market_file.read_text(encoding="utf-8"))
            mv = mj.get("metadata", {}).get("version") or mj.get("version")
            if mv != hub_version:
                errors.append(f"skillary/marketplace.json version ({mv}) != {hub_version}")
        except Exception as e:
            errors.append(f"skillary/marketplace.json parse error: {e}")

    if errors:
        print(f"FAIL: {len(errors)} version drift error(s) found:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("OK: All repositories, READMEs, changelogs, and manifests are synchronized.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
