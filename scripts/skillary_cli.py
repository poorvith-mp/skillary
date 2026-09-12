"""Skillary CLI — search, lock, verify, and audit AI agent skills.

Commands:
    find       Search the skill index with token scoring and synonym expansion
    lock       Generate skillary.lock from an installed skills directory
    verify     Verify installed skills against skillary.lock
    doctor     Audit installed skills for collisions, risky patterns, and staleness
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

# Add scripts directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from overlap import find_collisions
from security import scan_skills
from skillary import Skill, load_skill, repo_root


def default_index_path() -> Path:
    hub = Path(__file__).resolve().parent.parent
    local_dist = hub / "dist" / "skills.json"
    if local_dist.is_file():
        return local_dist
    return Path("dist") / "skills.json"


def default_skills_root() -> Path:
    local_claude = Path.cwd() / ".claude" / "skills"
    if local_claude.is_dir():
        return local_claude
    return Path.home() / ".claude" / "skills"


def load_domain_synonyms(hub_dir: Path | None = None) -> dict[str, list[str]]:
    hub = hub_dir or Path(__file__).resolve().parent.parent
    domain_map = hub / "taxonomy" / "domain_map.yaml"
    if not domain_map.is_file():
        return {}
    try:
        import yaml
        data = yaml.safe_load(domain_map.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "synonyms" in data and isinstance(data["synonyms"], dict):
            return {k.lower(): [s.lower() for s in v] for k, v in data["synonyms"].items()}
    except Exception:
        pass
    return {}


def load_index(index_arg: str | None) -> list[dict]:
    if index_arg and (index_arg.startswith("http://") or index_arg.startswith("https://")):
        with urllib.request.urlopen(index_arg) as response:
            return json.loads(response.read().decode("utf-8"))

    index_path = Path(index_arg) if index_arg else default_index_path()
    if not index_path.is_file():
        sys.stderr.write(f"Error: index file not found at {index_path}\n")
        sys.exit(2)

    return json.loads(index_path.read_text(encoding="utf-8"))


# --- Command: find ---

def tokenize(text: str) -> list[str]:
    return [t.lower() for t in re.findall(r"[a-z0-9]+", text)]


def score_record(
    record: dict,
    query_tokens: list[str],
    synonym_tokens: set[str],
) -> float:
    slug = record.get("slug", "").lower()
    title = record.get("title", "").lower()
    desc = record.get("description", "").lower()

    slug_toks = set(tokenize(slug))
    title_toks = set(tokenize(title))
    desc_toks = set(tokenize(desc))

    # Also handle plurals/stems
    slug_stems = {t.rstrip("s") for t in slug_toks}
    title_stems = {t.rstrip("s") for t in title_toks}
    desc_stems = {t.rstrip("s") for t in desc_toks}

    score = 0.0

    for tok in query_tokens:
        tok_stem = tok.rstrip("s")
        # Direct slug match (weight 3)
        if tok in slug_toks or tok in slug or tok_stem in slug_stems:
            score += 3.0
        # Title match (weight 2)
        if tok in title_toks or tok_stem in title_stems:
            score += 2.0
        # Description match (weight 1)
        if tok in desc_toks or tok_stem in desc_stems:
            score += 1.0

    for syn in synonym_tokens:
        syn_stem = syn.rstrip("s")
        if syn in slug_toks or syn in slug or syn_stem in slug_stems:
            score += 3.0
        if syn in title_toks or syn_stem in title_stems:
            score += 2.0
        if syn in desc_toks or syn_stem in desc_stems:
            score += 1.0

    return score


def cmd_find(args: argparse.Namespace) -> int:
    records = load_index(args.index)
    synonyms_map = load_domain_synonyms()

    query_tokens = tokenize(args.query)
    synonym_tokens: set[str] = set()
    for tok in query_tokens:
        if tok in synonyms_map:
            synonym_tokens.update(synonyms_map[tok])

    category_filter = args.category.strip().lower() if args.category else None

    scored = []
    for r in records:
        if category_filter:
            cat = r.get("category", "").lower()
            repo = r.get("repo", "").lower()
            if category_filter not in cat and category_filter not in repo:
                continue

        score = score_record(r, query_tokens, synonym_tokens)
        if score > 0:
            scored.append({
                "slug": r.get("slug", ""),
                "category": r.get("category", ""),
                "score": score,
                "description": r.get("description", ""),
            })

    scored.sort(key=lambda x: (-x["score"], x["slug"]))
    results = scored[: args.limit]

    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    if not results:
        print(f"No skills matching '{args.query}' found.")
        return 0

    # Table output: slug  category  score  description[:100]
    col_w_slug = max(len("SLUG"), max(len(r["slug"]) for r in results))
    col_w_cat = max(len("CATEGORY"), max(len(r["category"]) for r in results))

    header = f"{'SLUG':<{col_w_slug}}  {'CATEGORY':<{col_w_cat}}  {'SCORE':>5}  DESCRIPTION"
    print(header)
    print("-" * len(header))
    for r in results:
        desc_preview = r["description"][:100].replace("\n", " ")
        print(f"{r['slug']:<{col_w_slug}}  {r['category']:<{col_w_cat}}  {r['score']:>5.1f}  {desc_preview}")

    return 0


# --- Command: lock ---

def get_sibling_commit(repo_name: str, slug: str) -> str | None:
    try:
        import subprocess
        root = repo_root()
        repo_dir = root / repo_name
        if not repo_dir.is_dir() or not (repo_dir / ".git").is_dir():
            return None
        res = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", f"skills/{slug}/SKILL.md"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        sha = res.stdout.strip()
        if sha and re.match(r"^[0-9a-fA-F]{40}$", sha):
            return sha
    except Exception:
        pass
    return None


def cmd_lock(args: argparse.Namespace) -> int:
    records = load_index(args.index)
    index_by_slug = {r["slug"]: r for r in records}

    root_dir = Path(args.root) if args.root else default_skills_root()
    if not root_dir.is_dir():
        sys.stderr.write(f"Error: skills directory not found at {root_dir}\n")
        return 1

    locked_skills = {}
    for folder in sorted(root_dir.iterdir()):
        if not folder.is_dir():
            continue
        skill_file = folder / "SKILL.md"
        if not skill_file.is_file():
            continue

        raw = skill_file.read_text(encoding="utf-8", errors="replace")
        name_match = re.search(r"^name:[ \t]*(.+)$", raw, re.M)
        slug = name_match.group(1).strip().strip("\"'") if name_match else folder.name

        if slug in index_by_slug:
            idx_rec = index_by_slug[slug]
            sha256_hash = hashlib.sha256(skill_file.read_bytes()).hexdigest()
            source_commit = get_sibling_commit(idx_rec["repo"], slug)
            locked_skills[slug] = {
                "repo": idx_rec["repo"],
                "category": idx_rec.get("category", ""),
                "sha256": sha256_hash,
                "source_commit": source_commit,
                "last_reviewed": idx_rec.get("last_reviewed"),
            }

    lock_data = {
        "version": 1,
        "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "skills": {k: locked_skills[k] for k in sorted(locked_skills.keys())},
    }

    out_path = Path(args.out)
    out_path.write_text(json.dumps(lock_data, indent=2) + "\n", encoding="utf-8")
    print(f"Locked {len(locked_skills)} skills to {out_path}")
    return 0


# --- Command: verify ---

def cmd_verify(args: argparse.Namespace) -> int:
    lock_path = Path(args.lock)
    if not lock_path.is_file():
        sys.stderr.write(f"Error: lockfile not found at {lock_path}\n")
        return 1

    lock_data = json.loads(lock_path.read_text(encoding="utf-8"))
    locked_skills = lock_data.get("skills", {})

    root_dir = Path(args.root) if args.root else default_skills_root()
    index_records = []
    try:
        index_records = load_index(args.index)
    except Exception:
        pass
    index_by_slug = {r["slug"]: r for r in index_records}

    results = {}
    has_mismatch = False

    # Check all locked skills
    for slug, info in locked_skills.items():
        skill_file = root_dir / slug / "SKILL.md"
        if not skill_file.is_file():
            results[slug] = "missing"
            has_mismatch = True
            continue

        sha256_hash = hashlib.sha256(skill_file.read_bytes()).hexdigest()
        if sha256_hash == info.get("sha256"):
            results[slug] = "unchanged"
        else:
            results[slug] = "modified locally"
            has_mismatch = True

    # Check for installed skills not in lock
    if root_dir.is_dir():
        for folder in sorted(root_dir.iterdir()):
            if not folder.is_dir() or not (folder / "SKILL.md").is_file():
                continue
            raw = (folder / "SKILL.md").read_text(encoding="utf-8", errors="replace")
            name_match = re.search(r"^name:[ \t]*(.+)$", raw, re.M)
            slug = name_match.group(1).strip().strip("\"'") if name_match else folder.name
            if slug not in locked_skills and slug in index_by_slug:
                results[slug] = "not in lock (new)"
                has_mismatch = True

    if args.json:
        grouped = {
            "unchanged": [s for s, st in results.items() if st == "unchanged"],
            "modified locally": [s for s, st in results.items() if st == "modified locally"],
            "missing": [s for s, st in results.items() if st == "missing"],
            "not in lock (new)": [s for s, st in results.items() if st == "not in lock (new)"],
        }
        print(json.dumps(grouped, indent=2))
    else:
        for slug in sorted(results.keys()):
            status = results[slug]
            print(f"  {slug}: {status}")

    return 1 if has_mismatch else 0


# --- Command: doctor ---

def cmd_doctor(args: argparse.Namespace) -> int:
    root_dir = Path(args.root) if args.root else default_skills_root()
    if not root_dir.is_dir():
        sys.stderr.write(f"Error: skills directory not found at {root_dir}\n")
        return 1

    records = []
    try:
        records = load_index(args.index)
    except Exception:
        pass
    index_by_slug = {r["slug"]: r for r in records}

    installed_skills: list[Skill] = []
    unknown_folders: list[str] = []

    for folder in sorted(root_dir.iterdir()):
        if not folder.is_dir():
            continue
        skill_file = folder / "SKILL.md"
        if not skill_file.is_file():
            unknown_folders.append(folder.name)
            continue

        raw = skill_file.read_text(encoding="utf-8", errors="replace")
        name_match = re.search(r"^name:[ \t]*(.+)$", raw, re.M)
        slug = name_match.group(1).strip().strip("\"'") if name_match else folder.name

        if slug not in index_by_slug:
            unknown_folders.append(slug)

        skill_obj = load_skill("installed", folder)
        installed_skills.append(skill_obj)

    # 1. Collisions
    collisions = find_collisions(installed_skills)

    # 2. Risky patterns
    findings = scan_skills(installed_skills)

    # 3. Stale (last_reviewed > 180 days)
    cutoff = datetime.date.today() - datetime.timedelta(days=180)
    stale_skills = []
    for s in installed_skills:
        if not s.last_reviewed:
            stale_skills.append(s.slug)
        else:
            try:
                d = datetime.date.fromisoformat(s.last_reviewed)
                if d < cutoff:
                    stale_skills.append(s.slug)
            except ValueError:
                stale_skills.append(s.slug)

    if args.json:
        doctor_data = {
            "collisions": collisions,
            "risky_patterns": [f.__dict__ for f in findings],
            "stale": sorted(stale_skills),
            "unknown": sorted(unknown_folders),
        }
        print(json.dumps(doctor_data, indent=2))
    else:
        print(f"Auditing {len(installed_skills)} installed skills in {root_dir}...\n")

        print(f"## Collisions ({len(collisions)})")
        for c in collisions:
            print(f"  - {c['pair'][0]} <-> {c['pair'][1]}: {', '.join(repr(w) for w in c['words'])}")
        if not collisions:
            print("  None")

        print(f"\n## Risky patterns ({len(findings)})")
        for f in findings:
            print(f"  - [{f.severity.upper()}] {f.skill}: {f.indicator} — {f.message}")
        if not findings:
            print("  None")

        print(f"\n## Stale ({len(stale_skills)})")
        for s in stale_skills:
            print(f"  - {s}")
        if not stale_skills:
            print("  None")

        print(f"\n## Unknown ({len(unknown_folders)})")
        for u in unknown_folders:
            print(f"  - {u}")
        if not unknown_folders:
            print("  None")

    # Exit 0 if no collisions or risky patterns, 1 otherwise
    return 1 if (collisions or findings) else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="skillary",
        description="Skillary CLI — search, lock, verify, and audit AI agent skills.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # find
    p_find = subparsers.add_parser("find", help="Find skills matching query")
    p_find.add_argument("query", help="Search query string")
    p_find.add_argument("--category", help="Filter by category")
    p_find.add_argument("--limit", type=int, default=10, help="Max results to return (default 10)")
    p_find.add_argument("--json", action="store_true", help="Output results as JSON")
    p_find.add_argument("--index", help="Path or URL to skills.json")

    # lock
    p_lock = subparsers.add_parser("lock", help="Generate skillary.lock from installed skills")
    p_lock.add_argument("--root", help="Installed skills directory")
    p_lock.add_argument("--out", default="skillary.lock", help="Lockfile output path (default skillary.lock)")
    p_lock.add_argument("--index", help="Path to skills.json")

    # verify
    p_verify = subparsers.add_parser("verify", help="Verify installed skills against skillary.lock")
    p_verify.add_argument("--root", help="Installed skills directory")
    p_verify.add_argument("--lock", default="skillary.lock", help="Lockfile path (default skillary.lock)")
    p_verify.add_argument("--index", help="Path to skills.json")
    p_verify.add_argument("--json", action="store_true", help="Output verification as JSON")

    # doctor
    p_doc = subparsers.add_parser("doctor", help="Audit installed skills for collisions and risks")
    p_doc.add_argument("--root", help="Installed skills directory")
    p_doc.add_argument("--index", help="Path to skills.json")
    p_doc.add_argument("--json", action="store_true", help="Output audit report as JSON")

    args = parser.parse_args()

    if args.command == "find":
        return cmd_find(args)
    elif args.command == "lock":
        return cmd_lock(args)
    elif args.command == "verify":
        return cmd_verify(args)
    elif args.command == "doctor":
        return cmd_doctor(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
