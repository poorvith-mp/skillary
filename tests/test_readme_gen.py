from pathlib import Path
from scripts.gen_category_readmes import main as gen_readmes_main
from scripts.skillary import repo_paths, repo_root


def test_category_readmes_reviewed_column_and_idempotence():
    root = repo_root()
    # Run generator
    assert gen_readmes_main() == 0

    repos = repo_paths(root)
    assert len(repos) >= 1

    snapshots = {}
    for r in repos:
        readme = r / "README.md"
        assert readme.is_file()
        content = readme.read_text(encoding="utf-8")
        assert "| Skill ID | Title | Description | Reviewed |" in content
        snapshots[r.name] = content

    # Second run for idempotence
    assert gen_readmes_main() == 0

    for r in repos:
        content = (r / "README.md").read_text(encoding="utf-8")
        assert content == snapshots[r.name]
