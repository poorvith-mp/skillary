"""Build a `<skill-id>.skill` zip for every skill, from source.

The 28 bundles previously committed were hand-made and every one of them had
drifted from its SKILL.md. One was named for a skill that no longer exists
(`crypto-tax-specialist.skill` inside the `crypto-tax-advisor` folder), and they
carried `references/NOTE.md` and `assets/NOTE.md` entries that exist nowhere on
disk. Generating them removes the drift: the bundle is a build output, and
rebuilding is the only way it changes.

Bundles exist to support the Claude.ai upload path, where a user drags a single
zip into Settings > Capabilities > Skills.

Usage:
    python scripts/bundle.py --check    # report drift, write nothing
    python scripts/bundle.py --write    # rebuild all 315
    python scripts/bundle.py --clean    # remove stale/misnamed bundles first
"""

from __future__ import annotations

import argparse
import io
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

from skillary import iter_skills  # noqa: E402

# Everything under the skill folder ships except the bundle itself and junk.
EXCLUDE_SUFFIXES = {".skill", ".pyc"}
EXCLUDE_NAMES = {".DS_Store", "Thumbs.db"}

# Zip entries carry an mtime, so byte-comparing a rebuild against the committed
# file would always differ. Pin the timestamp to make bundles reproducible -
# otherwise every rebuild dirties all 315 files in git for no reason.
FIXED_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


def members(skill) -> list[tuple[str, bytes]]:
    out = []
    for path in sorted(skill.path.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix in EXCLUDE_SUFFIXES or path.name in EXCLUDE_NAMES:
            continue
        if "__pycache__" in path.parts:
            continue
        arcname = f"{skill.slug}/{path.relative_to(skill.path).as_posix()}"
        data = path.read_bytes()
        # Normalise line endings for text content. Without this the bundle
        # captures whatever the working tree has - CRLF on Windows, LF on Linux
        # - so the same commit produces different bytes per platform and the
        # check can never pass in CI. Git stores LF, so the bundle stores LF.
        if b"\x00" not in data:
            data = data.replace(b"\r\n", b"\n")
        out.append((arcname, data))
    return out


def contents(path: Path) -> dict[str, bytes]:
    """What a bundle actually holds, ignoring how it was compressed.

    Comparing the zip's raw bytes looks stricter but is wrong: deflate output
    differs between zlib versions, so a bundle written under one Python is
    reported stale under another. CI runs 3.12, this machine runs 3.14, and
    every bundle read as stale until this compared members instead.
    """
    with zipfile.ZipFile(path) as archive:
        return {name: archive.read(name) for name in archive.namelist()}


def build_bytes(skill) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for arcname, data in members(skill):
            info = zipfile.ZipInfo(arcname, date_time=FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    return buffer.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--clean", action="store_true", help="delete bundles that don't match their skill id")
    args = parser.parse_args()

    written = stale = misnamed = 0
    for skill in iter_skills():
        target = skill.path / f"{skill.slug}.skill"

        for existing in skill.path.glob("*.skill"):
            if existing.name != target.name:
                misnamed += 1
                print(f"MISNAMED: {skill.rel}/{existing.name} (skill is '{skill.slug}')")
                if args.clean or args.write:
                    existing.unlink()

        if target.exists() and contents(target) == dict(members(skill)):
            continue
        data = build_bytes(skill)

        if args.write:
            target.write_bytes(data)
            written += 1
        else:
            stale += 1
            state = "stale" if target.exists() else "missing"
            print(f"{state.upper()}: {skill.rel}/{target.name}")

    if args.write:
        import hashlib
        sums = []
        for skill in iter_skills():
            target = skill.path / f"{skill.slug}.skill"
            if target.is_file():
                digest = hashlib.sha256(target.read_bytes()).hexdigest()
                sums.append(f"{digest}  {skill.repo}/skills/{skill.slug}/{target.name}")
        hub = Path(__file__).resolve().parent.parent
        sums_file = hub / "dist" / "SHA256SUMS"
        sums_file.parent.mkdir(exist_ok=True)
        sums_file.write_text("\n".join(sorted(sums)) + "\n", encoding="utf-8")
        print(f"wrote {sums_file} ({len(sums)} hashes)")
        print(f"\nwrote {written} bundles, removed {misnamed} misnamed")
        return 0

    print(f"\n{stale} bundles stale or missing, {misnamed} misnamed")
    return 1 if (stale or misnamed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
