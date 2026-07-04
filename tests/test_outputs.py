import json
import re
from collections import Counter
from pathlib import Path


def _expected_from_log(log_path: Path) -> dict:
    paths, ips, total = Counter(), set(), 0
    with log_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0],
    }


def test_criterion_1_out_json_schema():
    """Success criterion 1: /app/out.json exists with valid JSON and exactly total_requests, unique_ips, top_path."""
    report_path = Path("/app/out.json")
    assert report_path.exists(), "no out.json found at /app/out.json"

    data = json.loads(report_path.read_text())
    assert set(data.keys()) == {"total_requests", "unique_ips", "top_path"}, (
        f"expected keys total_requests, unique_ips, top_path; got {sorted(data.keys())}"
    )
    assert isinstance(data["total_requests"], int), "total_requests must be an integer"
    assert isinstance(data["unique_ips"], int), "unique_ips must be an integer"
    assert isinstance(data["top_path"], str), "top_path must be a string"


def test_criterion_2_values_match_access_log():
    """Success criterion 2: values reflect the actual contents of /app/access.log."""
    data = json.loads(Path("/app/out.json").read_text())
    expected = _expected_from_log(Path("/app/access.log"))
    assert data["total_requests"] == expected["total_requests"], "total_requests mismatch"
    assert data["unique_ips"] == expected["unique_ips"], "unique_ips mismatch"
    assert data["top_path"] == expected["top_path"], "top_path mismatch"
