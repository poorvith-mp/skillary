import json
import sys
import time
import urllib.request
from pathlib import Path
import pytest

from scripts.skillary_cli import main as cli_main, cmd_find


def test_find_golden_queries(monkeypatch):
    golden_path = Path(__file__).parent / "find_golden.json"
    queries = json.loads(golden_path.read_text(encoding="utf-8"))

    for item in queries:
        query = item["query"]
        expected = item["expected_top"]

        # Run find via cli_main with --json
        args = ["skillary", "find", query, "--json", "--limit", "5"]
        monkeypatch.setattr(sys, "argv", args)

        import io
        captured = io.StringIO()
        monkeypatch.setattr(sys, "stdout", captured)

        ret = cli_main()
        assert ret == 0

        output = json.loads(captured.getvalue())
        slugs = [r["slug"] for r in output]
        for exp in expected:
            assert exp in slugs, f"Expected {exp} in top results for query '{query}', got {slugs}"


def test_find_category_filter(monkeypatch):
    args = ["skillary", "find", "pipeline", "--category", "Developer", "--json"]
    monkeypatch.setattr(sys, "argv", args)

    import io
    captured = io.StringIO()
    monkeypatch.setattr(sys, "stdout", captured)

    ret = cli_main()
    assert ret == 0

    results = json.loads(captured.getvalue())
    assert len(results) > 0
    for r in results:
        assert r["category"] == "Developer"


def test_find_json_shape_and_limit(monkeypatch):
    limit = 3
    args = ["skillary", "find", "test", "--json", "--limit", str(limit)]
    monkeypatch.setattr(sys, "argv", args)

    import io
    captured = io.StringIO()
    monkeypatch.setattr(sys, "stdout", captured)

    ret = cli_main()
    assert ret == 0

    results = json.loads(captured.getvalue())
    assert len(results) <= limit
    for r in results:
        assert "slug" in r
        assert "category" in r
        assert "score" in r
        assert "description" in r
        assert isinstance(r["score"], (int, float))


def test_find_no_network_by_default(monkeypatch):
    def boom(*args, **kwargs):
        raise RuntimeError("Network touched when local index used!")

    monkeypatch.setattr(urllib.request, "urlopen", boom)

    args = ["skillary", "find", "stripe", "--json"]
    monkeypatch.setattr(sys, "argv", args)

    import io
    monkeypatch.setattr(sys, "stdout", io.StringIO())

    ret = cli_main()
    assert ret == 0


def test_find_missing_index_exit_2(monkeypatch, tmp_path):
    missing_file = tmp_path / "non_existent.json"
    args = ["skillary", "find", "stripe", "--index", str(missing_file)]
    monkeypatch.setattr(sys, "argv", args)

    with pytest.raises(SystemExit) as exc_info:
        cli_main()
    assert exc_info.value.code == 2


def test_find_timing(monkeypatch):
    args = ["skillary", "find", "database", "--json"]
    monkeypatch.setattr(sys, "argv", args)

    import io
    monkeypatch.setattr(sys, "stdout", io.StringIO())

    start = time.perf_counter()
    ret = cli_main()
    elapsed = time.perf_counter() - start

    assert ret == 0
    assert elapsed < 1.0, f"Expected find to run under 1.0s, took {elapsed:.3f}s"
