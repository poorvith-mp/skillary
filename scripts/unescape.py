"""Unescape markdown artifacts and replace literal <br> in tables outside code fences.

Reference: skillary-features.md Part A1.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CHARS_TO_UNESCAPE = set(r"*[]`|$><~{}_#()-")
ESCAPE_RE = re.compile(r"\\([*\[\]`|$><~{}_#()\-]|\\)")


def unescape_chunk(text: str) -> str:
    # First replace <br> with newline
    text = text.replace("<br>", "\n")
    # Replace \X with X
    return ESCAPE_RE.sub(r"\1", text)


def process_skill_content(content: str) -> tuple[str, bool]:
    lines = content.splitlines(keepends=True)
    out = []
    in_fence = False
    fence_marker = ""
    changed = False

    for line in lines:
        stripped = line.strip()
        if not in_fence:
            if stripped.startswith(("```", "~~~")):
                in_fence = True
                fence_marker = stripped[:3]
                out.append(line)
            else:
                new_line = unescape_chunk(line)
                if new_line != line:
                    changed = True
                out.append(new_line)
        else:
            if stripped.startswith(fence_marker):
                in_fence = False
            out.append(line)

    result = "".join(out)
    return result, changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write changes to disk")
    args = parser.parse_args()

    hub_root = Path(__file__).resolve().parent.parent
    repos_dir = hub_root.parent

    modified_files = []
    total_files = 0

    for skill_path in sorted(repos_dir.glob("skills-*/skills/*/SKILL.md")):
        total_files += 1
        content = skill_path.read_text(encoding="utf-8", errors="replace")
        new_content, changed = process_skill_content(content)
        if changed:
            modified_files.append(skill_path)
            if args.write:
                skill_path.write_text(new_content, encoding="utf-8")

    print(f"Scanned {total_files} files across repos.")
    print(f"{'Modified' if args.write else 'Would modify'} {len(modified_files)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
