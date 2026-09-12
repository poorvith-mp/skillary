import re
from pathlib import Path
import pytest

from scripts.quality_report import generate_report, main as report_main
from scripts.skillary import repo_root


def test_quality_report_fields_and_no_bodies():
    report_content, stats = generate_report()

    # Fields present
    assert "# Skillary Catalog Quality Report" in report_content
    assert "Total Skills" in report_content
    assert "Validation Rate" in report_content
    assert "Freshness" in report_content
    assert "Trigger Overlap Pairs" in report_content
    assert "Security Findings" in report_content
    assert "| Category | Repository | Total Skills | Reviewed (<180d) | Validated |" in report_content

    # Numbers consistency
    assert stats["total_skills"] == 277
    assert stats["valid_count"] == 277
    assert stats["reviewed_180_count"] == 277
    assert stats["security_count"] == 0

    # Assert NO skill body text is included in report
    # Test against a known distinctive sentence from a skill body
    known_body_sentences = [
        "Traditional web security assumes deterministic inputs",
        "Lead with the result the user asked for",
        "Build webhook receivers with signature verification",
    ]
    for sentence in known_body_sentences:
        assert sentence not in report_content


def test_quality_report_matches_readme():
    hub = Path(__file__).resolve().parent.parent
    readme_path = hub / "README.md"
    readme_text = readme_path.read_text(encoding="utf-8")

    report_content, stats = generate_report()

    # Hub README summary line: (277 of 277 reviewed in the last 180 days)
    match = re.search(r"\((\d+) of (\d+) reviewed in the last 180 days\)", readme_text)
    assert match is not None
    reviewed_in_readme = int(match.group(1))
    total_in_readme = int(match.group(2))

    assert total_in_readme == stats["total_skills"]
    assert reviewed_in_readme == stats["reviewed_180_count"]
