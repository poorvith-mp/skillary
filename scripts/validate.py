"""Validate every skill across the 12 category repos.

This is the gate the rest of the tooling runs behind. It encodes the house rules
that the August 2026 audit found violated at scale, so that once a defect class
is fixed it cannot silently come back.

Usage:
    python scripts/validate.py                  # all repos, human-readable
    python scripts/validate.py --repo finance   # one repo
    python scripts/validate.py --json           # machine-readable
    python scripts/validate.py --baseline       # summary counts only, always exit 0

Exit code is non-zero if any error-severity finding is present, so it can be
dropped straight into CI once remediation has landed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Skill bodies contain emoji; the default Windows console codec (cp1252) raises
# UnicodeEncodeError on them and takes the whole run down.
for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

from skillary import (  # noqa: E402
    BOILERPLATE_TAIL_RES,
    DESCRIPTION_LISTING_LIMIT,
    DESCRIPTION_SPEC_LIMIT,
    NAME_RE,
    STUB_MARKERS,
    Report,
    iter_skills,
)

# Content fingerprints, NOT headings. 313 skills carry the `## Verification`
# heading but only 281 carry the boilerplate; the other 32 are hand-written and
# domain-correct. Same for anti-patterns: 290 headings, 255 boilerplate, 35
# hand-written. Keying on the heading would destroy the 67 best sections in the
# library, so every check below matches on body text.
CODE_CHECKLIST_FP = "Code compiles cleanly and passes all automated tests"
CODE_ANTIPATTERN_FP = "NEVER bypass automated tests or typecheckers"

# Repos whose skills legitimately carry an engineering checklist.
ENGINEERING_REPOS = {"skills-developer", "skills-gamedev"}

TRIGGER_RES = [
    re.compile(r"\buse (this )?when\b", re.I),
    re.compile(r"\btrigger(s|ed)? (when|on)\b", re.I),
    re.compile(r"\buse for\b", re.I),
]

MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
ESCAPE_RE = re.compile(r"\\([*\[\]`|$><~{}_#()\-]|\\)")


def strip_fences(text: str) -> str:
    """Return text with fenced code blocks stripped."""
    lines = []
    in_fence = False
    fence_marker = ""
    for line in text.splitlines():
        stripped = line.strip()
        if not in_fence:
            if stripped.startswith(("```", "~~~")):
                in_fence = True
                fence_marker = stripped[:3]
            else:
                lines.append(line)
        else:
            if stripped.startswith(fence_marker):
                in_fence = False
    return "\n".join(lines)


def check_skill(skill, report: Report) -> None:
    sid = skill.rel

    # --- frontmatter ---------------------------------------------------
    if skill.name is None:
        report.add(sid, "no-frontmatter", "SKILL.md has no parseable YAML frontmatter")
        return

    if skill.name != skill.slug:
        report.add(sid, "name-mismatch", f"name '{skill.name}' != folder '{skill.slug}'")

    if not NAME_RE.match(skill.name):
        report.add(sid, "name-format", f"name '{skill.name}' is not clean kebab-case")

    if len(skill.name) > 30:
        report.add(sid, "name-length", f"name is {len(skill.name)} chars (max 30 in v4)")

    # --- description ---------------------------------------------------
    desc = skill.description
    if not desc:
        report.add(sid, "no-description", "description is empty")
        return

    if len(desc) > 200:
        report.add(
            sid,
            "desc-spec-limit",
            f"description is {len(desc)} chars, over the 200 v4 spec limit",
        )

    for pattern in BOILERPLATE_TAIL_RES:
        if pattern.search(desc):
            report.add(sid, "boilerplate-trigger", "description ends in a generated trigger sentence")
            break

    # A trigger that names the skill itself matches nothing a user would type.
    spaced = skill.slug.replace("-", " ")
    if re.search(rf"asks? about {re.escape(spaced)}\b", desc, re.I):
        report.add(sid, "self-referential-trigger", f"trigger just restates the skill name ('{spaced}')")

    if re.match(r"^\s*(you are|you've|you have)\b", desc, re.I):
        report.add(sid, "persona-description", "description is a persona prompt, not a capability statement")

    if "##" in desc or "\\\\" in desc:
        report.add(sid, "body-leaked-into-frontmatter", "description contains markdown headings or escapes")

    # --- body ----------------------------------------------------------
    body = skill.body
    for marker in STUB_MARKERS:
        if marker in body:
            report.add(sid, "import-stub", "body is a failed-import placeholder, not instructions")
            break

    # Not "is there an H1 anywhere" - several skills embed a template whose own
    # `# Project Name` / `# \[H1: Engaging title\]` satisfies that. The rule is
    # that the body must OPEN with its title, before any prose.
    first_line = next((line for line in body.splitlines() if line.strip()), "")
    if not first_line.lstrip().startswith("# "):
        report.add(sid, "no-opening-h1", f"body opens with prose, not an H1: {first_line.strip()[:60]!r}", "warning")

    clean_body = strip_fences(body)

    if ESCAPE_RE.search(clean_body):
        report.add(sid, "escaped-markdown", "literal backslash escapes outside code fences")

    if "<br>" in clean_body:
        report.add(sid, "br-in-markdown", "HTML line break instead of a newline")

    if re.search(r"\.\.\.\s*\n---\s*\n", body):
        report.add(sid, "truncated-blob", "collapsed preview fragment welded into the body")

    if "${CLAUDE_SKILL_DIR}" in body:
        report.add(sid, "agent-coupling", "${CLAUDE_SKILL_DIR} variable used; use relative paths instead")

    if re.search(r"[~.]/\.claude/", clean_body):
        report.add(sid, "agent-coupling", "references agent-specific ~/.claude path")

    if CODE_CHECKLIST_FP in body and skill.repo not in ENGINEERING_REPOS:
        report.add(sid, "wrong-domain-checklist", "carries the software-engineering QA checklist")

    if CODE_ANTIPATTERN_FP in body and skill.repo not in ENGINEERING_REPOS:
        report.add(sid, "wrong-domain-antipatterns", "carries the software-engineering anti-patterns")

    if body.count("\n") > 500:
        report.add(sid, "body-too-long", f"{body.count(chr(10))} lines; spec guidance is under 500", "warning")

    # --- supporting files ----------------------------------------------
    linked = set(MD_LINK_RE.findall(body)) | set(re.findall(r"references/[\w.-]+", body))

    for link in set(MD_LINK_RE.findall(clean_body)):
        if link.startswith(("http:", "https:", "#", "mailto:")) or not link.endswith(".md"):
            continue
        rel_path = link.split("#")[0].split("?")[0].lstrip("./")
        target_file = skill.path / rel_path
        ref_target = skill.path / "references" / Path(rel_path).name
        if not target_file.exists() and not ref_target.exists():
            report.add(sid, "dangling-reference", f"body links {link}, which does not exist")

    refs_dir = skill.path / "references"
    if refs_dir.is_dir():
        for ref in sorted(refs_dir.glob("*.md")):
            rel = f"references/{ref.name}"
            if not any(rel in link for link in linked):
                report.add(sid, "orphan-reference", f"{rel} is never linked from the body, so it can never load", "warning")

    # Bundles are shipped deliberately, for the Claude.ai drag-and-drop upload
    # path, and are generated by bundle.py. Only a wrongly named one is a
    # problem - that is how crypto-tax-specialist.skill survived inside the
    # crypto-tax-advisor folder after a rename.
    for stray in sorted(skill.path.glob("*.skill")):
        if stray.stem != skill.slug:
            report.add(sid, "misnamed-bundle", f"{stray.name} does not match skill id '{skill.slug}'")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", help="limit to one category, e.g. 'finance'")
    parser.add_argument("--json", action="store_true", help="emit findings as JSON")
    parser.add_argument("--baseline", action="store_true", help="summary counts only; always exit 0")
    parser.add_argument("--code", help="show only this finding code")
    args = parser.parse_args()

    report = Report()
    skills = list(iter_skills())
    if args.repo:
        target = args.repo if args.repo.startswith("skills-") else f"skills-{args.repo}"
        skills = [s for s in skills if s.repo == target]

    if not skills:
        print("No skills found. Are the skills-* repos siblings of this one?", file=sys.stderr)
        return 2

    seen = defaultdict(list)
    for skill in skills:
        check_skill(skill, report)
        if skill.name:
            seen[skill.name].append(skill.rel)

    for name, paths in sorted(seen.items()):
        if len(paths) > 1:
            report.add(", ".join(paths), "duplicate-id", f"skill id '{name}' is used {len(paths)} times")

    findings = report.findings
    if args.code:
        findings = [f for f in findings if f.code == args.code]

    if args.json:
        print(json.dumps([f.__dict__ for f in findings], indent=2))
    elif args.baseline:
        counts = Counter(f.code for f in report.findings)
        print(f"{len(skills)} skills across {len({s.repo for s in skills})} repos\n")
        width = max(len(c) for c in counts) if counts else 10
        for code, count in counts.most_common():
            print(f"  {code:<{width}}  {count}")
    else:
        by_code = defaultdict(list)
        for finding in findings:
            by_code[finding.code].append(finding)
        for code in sorted(by_code, key=lambda c: -len(by_code[c])):
            group = by_code[code]
            print(f"\n{code}  ({len(group)})")
            for finding in group[:12]:
                print(f"  {finding.skill}: {finding.message}")
            if len(group) > 12:
                print(f"  ... and {len(group) - 12} more")
        print(f"\n{len(report.errors)} errors, {len(report.warnings)} warnings across {len(skills)} skills")

    if args.baseline:
        return 0
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
