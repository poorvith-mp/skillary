"""Backfill provenance frontmatter (last_reviewed, tested_with) across skills repos."""

from __future__ import annotations

import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from skillary import FRONTMATTER_RE, repo_paths, repo_root


def get_git_commit_date(repo_dir: Path, skill_md: Path) -> str:
    try:
        rel_path = skill_md.relative_to(repo_dir)
        # Use forward slashes for git path
        git_path = str(rel_path).replace("\\", "/")
        res = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", git_path],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        date_str = res.stdout.strip()
        if date_str and re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            return date_str
    except Exception:
        pass
    return datetime.date.today().isoformat()


def backfill_skill(skill_dir: Path, repo_dir: Path) -> bool:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return False
    raw = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(raw)
    if not match:
        return False

    frontmatter = match.group(1)
    body = match.group(2)

    has_reviewed = bool(re.search(r"^last_reviewed:", frontmatter, re.M))
    has_tested = bool(re.search(r"^tested_with:", frontmatter, re.M))

    has_tests = (skill_dir / "tests").is_dir()
    has_examples = (skill_dir / "examples").is_dir()
    should_have_tested = has_tests or has_examples

    if has_reviewed and (has_tested or not should_have_tested):
        return False

    date_str = get_git_commit_date(repo_dir, skill_md)

    extra_lines = []
    if not has_reviewed:
        extra_lines.append(f"last_reviewed: {date_str}")
    if should_have_tested and not has_tested:
        extra_lines.append("tested_with: claude-code 2.1")

    if not extra_lines:
        return False

    extra_block = "\n".join(extra_lines) + "\n"

    name_match = re.search(r"^name:[ \t]*[^\r\n]+", frontmatter, re.M)
    if name_match:
        idx = name_match.end()
        if idx < len(frontmatter) and frontmatter[idx] == "\r":
            idx += 1
        if idx < len(frontmatter) and frontmatter[idx] == "\n":
            idx += 1
        new_fm = frontmatter[:idx] + extra_block + frontmatter[idx:]
    else:
        new_fm = frontmatter + "\n" + extra_block

    if not new_fm.endswith("\n"):
        new_fm += "\n"
    new_raw = f"---\n{new_fm}---\n{body}"
    skill_md.write_text(new_raw, encoding="utf-8")
    return True


def backfill_repo(repo_dir: Path) -> int:
    skills_dir = repo_dir / "skills"
    if not skills_dir.is_dir():
        return 0
    updated = 0
    for folder in sorted(skills_dir.iterdir()):
        if folder.is_dir() and (folder / "SKILL.md").is_file():
            if backfill_skill(folder, repo_dir):
                updated += 1
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", help="Target category repo folder name or path")
    args = parser.parse_args()

    root = repo_root()
    if args.repo:
        repo_path = Path(args.repo) if Path(args.repo).is_dir() else root / args.repo
        count = backfill_repo(repo_path)
        print(f"Updated {count} skills in {repo_path.name}")
    else:
        total = 0
        for p in repo_paths(root):
            count = backfill_repo(p)
            print(f"Updated {count} skills in {p.name}")
            total += count
        print(f"Total updated: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
