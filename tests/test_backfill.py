import subprocess
from pathlib import Path
import pytest

from scripts.skillary import parse_description


def test_backfill_provenance_on_fixture_repo(tmp_path):
    from scripts.backfill_provenance import backfill_repo

    repo_dir = tmp_path / "skills-fixture"
    skills_dir = repo_dir / "skills"
    skills_dir.mkdir(parents=True)

    # 1. Skill with tests/
    s1 = skills_dir / "skill-tests"
    s1.mkdir()
    (s1 / "tests").mkdir()
    (s1 / "SKILL.md").write_text(
        "---\nname: skill-tests\ndescription: >-\n  Has automated tests.\n  Use when testing.\n---\n# Skill Tests\nBody\n",
        encoding="utf-8",
    )

    # 2. Skill with examples/
    s2 = skills_dir / "skill-examples"
    s2.mkdir()
    (s2 / "examples").mkdir()
    (s2 / "SKILL.md").write_text(
        "---\nname: skill-examples\ndescription: Use when testing examples.\n---\n# Skill Examples\nBody\n",
        encoding="utf-8",
    )

    # 3. Plain skill without tests or examples
    s3 = skills_dir / "skill-plain"
    s3.mkdir()
    (s3 / "SKILL.md").write_text(
        "---\nname: skill-plain\ndescription: Use when testing plain.\n---\n# Skill Plain\nBody\n",
        encoding="utf-8",
    )

    # 4. Complex multiline block scalar description
    s4 = skills_dir / "skill-multiline"
    s4.mkdir()
    s4_raw = (
        "---\n"
        "name: skill-multiline\n"
        "description: >-\n"
        "  First line of description with special characters $ and &.\n"
        "  Second line of description.\n"
        "  Use when testing multiline block scalars.\n"
        "---\n"
        "# Multiline Skill\n"
        "Body content.\n"
    )
    (s4 / "SKILL.md").write_text(s4_raw, encoding="utf-8")

    # Initialize git repo and commit
    subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo_dir, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_dir, check=True)
    import os
    env = dict(os.environ)
    env["GIT_COMMITTER_DATE"] = "2026-09-08T10:00:00Z"
    env["GIT_AUTHOR_DATE"] = "2026-09-08T10:00:00Z"
    (repo_dir / ".gitignore").write_text("*.tmp\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
    res = subprocess.run(
        ["git", "commit", "--no-verify", "-m", "initial", "--date", "2026-09-08T10:00:00Z"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        env=env,
    )
    if res.returncode != 0:
        raise RuntimeError(f"git commit failed: stdout={res.stdout}, stderr={res.stderr}")

    # Run backfill
    backfill_repo(repo_dir)

    # Assert skill-tests has last_reviewed and tested_with
    s1_text = (s1 / "SKILL.md").read_text(encoding="utf-8")
    assert "last_reviewed: 2026-09-08" in s1_text
    assert "tested_with: claude-code 2.1" in s1_text

    # Assert skill-examples has tested_with
    s2_text = (s2 / "SKILL.md").read_text(encoding="utf-8")
    assert "last_reviewed: 2026-09-08" in s2_text
    assert "tested_with: claude-code 2.1" in s2_text

    # Assert skill-plain has last_reviewed but NOT tested_with
    s3_text = (s3 / "SKILL.md").read_text(encoding="utf-8")
    assert "last_reviewed: 2026-09-08" in s3_text
    assert "tested_with:" not in s3_text

    # Assert description block scalar in s4 is completely byte-identical
    s4_text = (s4 / "SKILL.md").read_text(encoding="utf-8")
    assert "last_reviewed: 2026-09-08" in s4_text
    # Check that description parsing yields the exact same parsed description
    assert parse_description(s4_raw) == parse_description(s4_text)
    # Check that the description block lines are preserved verbatim
    desc_block = (
        "description: >-\n"
        "  First line of description with special characters $ and &.\n"
        "  Second line of description.\n"
        "  Use when testing multiline block scalars."
    )
    assert desc_block in s4_text
