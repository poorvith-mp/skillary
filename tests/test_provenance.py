import datetime
from pathlib import Path
from unittest.mock import MagicMock
import pytest

from scripts.skillary import Report, Skill, load_skill
from scripts.validate import check_skill


def create_skill(frontmatter_extra: str = "") -> Skill:
    fm = f"name: my-skill\ndescription: Use when testing provenance.\n{frontmatter_extra}".strip()
    raw = f"---\n{fm}\n---\n# My Skill\n\nValid body instructions.\n"
    skill = Skill(
        repo="skills-developer",
        path=Path("/fake/skills-developer/skills/my-skill"),
        name="my-skill",
        description="Use when testing provenance.",
        body="# My Skill\n\nValid body instructions.\n",
        raw=raw,
        frontmatter=fm,
    )
    # Parse provenance fields if present in frontmatter
    for line in fm.splitlines():
        if line.startswith("last_reviewed:"):
            skill.last_reviewed = line.split(":", 1)[1].strip().strip("\"'")
        if line.startswith("tested_with:"):
            skill.tested_with = line.split(":", 1)[1].strip().strip("\"'")
    return skill


def test_provenance_missing_emits_prov001():
    skill = create_skill()
    report = Report()
    check_skill(skill, report)
    prov001 = [f for f in report.findings if f.code == "PROV001"]
    assert len(prov001) == 1
    assert prov001[0].severity == "warning"


def test_provenance_invalid_date_emits_prov002():
    skill = create_skill("last_reviewed: 2026-99-99")
    report = Report()
    check_skill(skill, report)
    prov002 = [f for f in report.findings if f.code == "PROV002"]
    assert len(prov002) == 1
    assert prov002[0].severity == "error"


def test_provenance_invalid_tested_with_emits_prov003():
    today = datetime.date.today().isoformat()
    skill = create_skill(f"last_reviewed: {today}\ntested_with: InvalidHostName")
    report = Report()
    check_skill(skill, report)
    prov003 = [f for f in report.findings if f.code == "PROV003"]
    assert len(prov003) == 1
    assert prov003[0].severity == "error"


def test_provenance_old_date_emits_prov004():
    old_date = (datetime.date.today() - datetime.timedelta(days=200)).isoformat()
    skill = create_skill(f"last_reviewed: {old_date}\ntested_with: claude-code 2.1")
    report = Report()
    check_skill(skill, report)
    prov004 = [f for f in report.findings if f.code == "PROV004"]
    assert len(prov004) == 1
    assert prov004[0].severity == "warning"
    # PROV002 and PROV003 should not be present
    assert not [f for f in report.findings if f.code in ("PROV002", "PROV003")]


def test_provenance_valid_emits_no_prov_findings():
    recent = (datetime.date.today() - datetime.timedelta(days=10)).isoformat()
    skill = create_skill(f"last_reviewed: {recent}\ntested_with: claude-code 2.1")
    report = Report()
    check_skill(skill, report)
    prov = [f for f in report.findings if f.code.startswith("PROV")]
    assert len(prov) == 0


def test_load_skill_parses_provenance(tmp_path):
    skill_dir = tmp_path / "skills" / "demo-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: demo-skill\ndescription: Use when demonstrating.\nlast_reviewed: 2026-09-08\ntested_with: claude-code 2.1\n---\n# Demo\nBody\n",
        encoding="utf-8",
    )
    skill = load_skill("skills-developer", skill_dir)
    assert skill.last_reviewed == "2026-09-08"
    assert skill.tested_with == "claude-code 2.1"
