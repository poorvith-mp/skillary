"""Security scanner for the skillary library and category skill bundles.

Verifies zero security indicators across all skills and bundles:
- No prompt injection or instruction overrides
- No zero-width or hidden bidirectional Unicode
- No encoded payloads or pipe-to-shell patterns
- No credential paths or secret exfiltration
- No non-markdown executables inside .skill zip bundles
- No zip path traversal

Reference: skillary-features.md Part F.
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

from skillary import iter_skills  # noqa: E402

# Indicators to scan
ZERO_WIDTH_RE = re.compile(r"[\u200B-\u200D\uFEFF\u202A-\u202E\u2066-\u2069]")
BASE64_PAYLOAD_RE = re.compile(r"(?:eval|exec)\s*\(\s*(?:base64\s*\.b64decode|atob)\b", re.I)
PIPE_TO_SHELL_RE = re.compile(r"\b(?:curl|wget)\b[^\n|]+?\|\s*(?:bash|sh|zsh|python)\b", re.I)
INSTRUCTION_OVERRIDE_RE = re.compile(
    r"\b(?:ignore|disregard)\s+(?:all\s+)?(?:previous|prior|above)\s+instructions\b",
    re.I,
)
CREDENTIAL_PATHS_RE = re.compile(r"(?:~|\$HOME)/(?:\.ssh|\.aws|\.netrc|\.npmrc|\.gnupg)\b")
DESTRUCTIVE_CMD_RE = re.compile(r"\brm\s+-rf\s+/(?:\s|$|\*)")
HARDCODED_KEY_RE = re.compile(r"\b(?:ghp_[a-zA-Z0-9]{36}|AKIA[0-9A-Z]{16})\b")

# Whitelist exact benign strings
EXACT_ALLOWLIST = {
    "NEVER swallow errors silently or leave unhandled rejections in production paths.",
    "NEVER swallow errors silently.",
}


@dataclass
class Finding:
    skill: str
    indicator: str
    message: str
    severity: str = "critical"


def scan_skill(skill, findings: list[Finding]) -> None:
    sid = skill.rel
    body = skill.body

    # 1. Zero-width Unicode
    if ZERO_WIDTH_RE.search(skill.raw):
        findings.append(Finding(sid, "hidden-unicode", "contains hidden or zero-width Unicode"))

    # 2. Base64 payload execution
    if BASE64_PAYLOAD_RE.search(body):
        findings.append(Finding(sid, "base64-payload", "contains base64 decode execution pattern"))

    # 3. Pipe to shell
    if PIPE_TO_SHELL_RE.search(body):
        findings.append(Finding(sid, "pipe-to-shell", "contains curl/wget piped directly to shell"))

    # 4. Instruction override
    if INSTRUCTION_OVERRIDE_RE.search(body):
        findings.append(Finding(sid, "instruction-override", "contains prompt injection instruction override"))

    # 5. Credential paths
    if CREDENTIAL_PATHS_RE.search(body):
        findings.append(Finding(sid, "credential-path", "targets sensitive credential path (~/.ssh, ~/.aws)"))

    # 6. Destructive commands
    if DESTRUCTIVE_CMD_RE.search(body):
        findings.append(Finding(sid, "destructive-cmd", "contains destructive root filesystem deletion command"))

    # 7. Hardcoded API secrets
    if HARDCODED_KEY_RE.search(body):
        findings.append(Finding(sid, "hardcoded-secret", "contains live hardcoded secret or token"))

    # 8. Bundle verification
    bundle_path = skill.path / f"{skill.slug}.skill"
    if bundle_path.is_file():
        try:
            with zipfile.ZipFile(bundle_path) as z:
                for name in z.namelist():
                    if ".." in name or name.startswith("/"):
                        findings.append(Finding(sid, "zip-traversal", f"bundle contains path traversal: {name}"))
                    if not name.endswith((".md", ".json", ".yaml", ".yml")) and not name.endswith("/"):
                        findings.append(Finding(sid, "executable-in-bundle", f"bundle contains non-markdown file: {name}"))
        except Exception as e:
            findings.append(Finding(sid, "corrupt-bundle", f"failed to open zip bundle: {e}"))


def scan_skills(skills: list) -> list[Finding]:
    """Scan a list of Skill objects for security indicators."""
    findings: list[Finding] = []
    for skill in skills:
        scan_skill(skill, findings)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit findings as JSON")
    args = parser.parse_args()

    skills = list(iter_skills())
    findings = scan_skills(skills)

    if args.json:
        import json
        print(json.dumps([f.__dict__ for f in findings], indent=2))
        return 1 if findings else 0

    if findings:
        print(f"\nSECURITY GATE FAILED: {len(findings)} findings across {len(skills)} skills:\n")
        for f in findings:
            print(f"[{f.severity.upper()}] {f.skill}: {f.indicator} — {f.message}")
        return 1

    print(f"\nSecurity gate passed: 0 indicators across all {len(skills)} skills and bundles.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
