from pathlib import Path
import pytest

from scripts.check_version_sync import main as check_sync_main
from scripts.skillary import repo_paths, repo_root


def test_version_sync_across_repositories():
    root = repo_root()
    siblings = repo_paths(root)
    if not siblings:
        pytest.skip("Sibling repositories not present in environment")

    # check_version_sync main must exit 0
    ret = check_sync_main()
    assert ret == 0
