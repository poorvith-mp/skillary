from pathlib import Path
import pytest

from scripts.skillary import repo_root


def test_agents_lock_rule_in_contracts():
    root = repo_root()
    agents_repo = root / "skillary-agents"
    if not agents_repo.is_dir():
        pytest.skip("skillary-agents repository not found in sibling checkout")

    roles_dir = agents_repo / "roles"
    assert roles_dir.is_dir()

    expected_roles = ["scout", "planner", "worker", "verifier", "security-auditor", "shipper"]
    for role in expected_roles:
        role_file = roles_dir / f"{role}.md"
        assert role_file.is_file(), f"Missing role contract: {role_file}"
        content = role_file.read_text(encoding="utf-8")
        assert "skillary.lock" in content
        assert "restrict skill selection to locked slugs" in content
        assert "using skillary.lock" in content

    # Also assert Scout step in AGENTS.md has it
    agents_md = agents_repo / "AGENTS.md"
    assert agents_md.is_file()
    agents_content = agents_md.read_text(encoding="utf-8")
    assert "skillary.lock" in agents_content
    assert "using skillary.lock" in agents_content
