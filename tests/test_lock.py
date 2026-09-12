import hashlib
import io
import json
import sys
from pathlib import Path
import pytest

from scripts.skillary_cli import main as cli_main


@pytest.fixture
def installed_fixture(tmp_path):
    installed = tmp_path / "installed"
    installed.mkdir()

    # 3 known skills (matching slugs from dist/skills.json)
    s1 = installed / "webhooks"
    s1.mkdir()
    (s1 / "SKILL.md").write_text("---\nname: webhooks\n---\n# Webhooks\nContent 1\n", encoding="utf-8")

    s2 = installed / "database"
    s2.mkdir()
    (s2 / "SKILL.md").write_text("---\nname: database\n---\n# Database\nContent 2\n", encoding="utf-8")

    s3 = installed / "ci-pipelines"
    s3.mkdir()
    (s3 / "SKILL.md").write_text("---\nname: ci-pipelines\n---\n# CI\nContent 3\n", encoding="utf-8")

    # 1 unknown folder (not in dist/skills.json)
    u = installed / "my-custom-tool"
    u.mkdir()
    (u / "SKILL.md").write_text("---\nname: my-custom-tool\n---\n# Custom\nContent 4\n", encoding="utf-8")

    return installed


def test_lock_creation_and_properties(monkeypatch, installed_fixture, tmp_path):
    lock_file = tmp_path / "skillary.lock"
    args = ["skillary", "lock", "--root", str(installed_fixture), "--out", str(lock_file)]
    monkeypatch.setattr(sys, "argv", args)
    monkeypatch.setattr(sys, "stdout", io.StringIO())

    ret = cli_main()
    assert ret == 0
    assert lock_file.is_file()

    data = json.loads(lock_file.read_text(encoding="utf-8"))
    assert data["version"] == 1
    assert "generated" in data
    assert "skills" in data

    skills = data["skills"]
    # Only 3 known skills locked (unknown folder excluded)
    assert len(skills) == 3
    assert list(skills.keys()) == sorted(skills.keys())
    assert set(skills.keys()) == {"ci-pipelines", "database", "webhooks"}

    # Assert SHA256 matches actual file bytes
    for slug in skills:
        skill_md = installed_fixture / slug / "SKILL.md"
        expected_sha = hashlib.sha256(skill_md.read_bytes()).hexdigest()
        assert skills[slug]["sha256"] == expected_sha
        assert "repo" in skills[slug]
        assert "category" in skills[slug]
        assert "last_reviewed" in skills[slug]


def test_lock_determinism(monkeypatch, installed_fixture, tmp_path):
    lock1 = tmp_path / "lock1.json"
    lock2 = tmp_path / "lock2.json"

    args1 = ["skillary", "lock", "--root", str(installed_fixture), "--out", str(lock1)]
    monkeypatch.setattr(sys, "argv", args1)
    monkeypatch.setattr(sys, "stdout", io.StringIO())
    assert cli_main() == 0

    args2 = ["skillary", "lock", "--root", str(installed_fixture), "--out", str(lock2)]
    monkeypatch.setattr(sys, "argv", args2)
    monkeypatch.setattr(sys, "stdout", io.StringIO())
    assert cli_main() == 0

    d1 = json.loads(lock1.read_text(encoding="utf-8"))
    d2 = json.loads(lock2.read_text(encoding="utf-8"))

    # Only 'generated' timestamp might differ; skills dict must be identical
    assert d1["version"] == d2["version"]
    assert d1["skills"] == d2["skills"]


def test_verify_untouched(monkeypatch, installed_fixture, tmp_path):
    lock_file = tmp_path / "skillary.lock"
    # Lock first
    monkeypatch.setattr(sys, "argv", ["skillary", "lock", "--root", str(installed_fixture), "--out", str(lock_file)])
    monkeypatch.setattr(sys, "stdout", io.StringIO())
    assert cli_main() == 0

    # Verify untouched
    monkeypatch.setattr(sys, "argv", ["skillary", "verify", "--root", str(installed_fixture), "--lock", str(lock_file), "--json"])
    captured = io.StringIO()
    monkeypatch.setattr(sys, "stdout", captured)
    ret = cli_main()
    assert ret == 0

    res = json.loads(captured.getvalue())
    assert set(res["unchanged"]) == {"ci-pipelines", "database", "webhooks"}
    assert res["modified locally"] == []
    assert res["missing"] == []
    assert res["not in lock (new)"] == []


def test_verify_states_modified_missing_new(monkeypatch, installed_fixture, tmp_path):
    lock_file = tmp_path / "skillary.lock"
    # Lock with initial 3
    monkeypatch.setattr(sys, "argv", ["skillary", "lock", "--root", str(installed_fixture), "--out", str(lock_file)])
    monkeypatch.setattr(sys, "stdout", io.StringIO())
    assert cli_main() == 0

    # 1. Modify webhooks locally
    (installed_fixture / "webhooks" / "SKILL.md").write_text("Modified content", encoding="utf-8")

    # 2. Delete database (missing)
    import shutil
    shutil.rmtree(installed_fixture / "database")

    # 3. Add a known skill not in lock (deployment)
    new_skill = installed_fixture / "deployment"
    new_skill.mkdir()
    (new_skill / "SKILL.md").write_text("---\nname: deployment\n---\n# Deploy\nContent\n", encoding="utf-8")

    # Verify
    monkeypatch.setattr(sys, "argv", ["skillary", "verify", "--root", str(installed_fixture), "--lock", str(lock_file), "--json"])
    captured = io.StringIO()
    monkeypatch.setattr(sys, "stdout", captured)
    ret = cli_main()
    assert ret == 1

    res = json.loads(captured.getvalue())
    assert res["modified locally"] == ["webhooks"]
    assert res["missing"] == ["database"]
    assert res["not in lock (new)"] == ["deployment"]
    assert res["unchanged"] == ["ci-pipelines"]
