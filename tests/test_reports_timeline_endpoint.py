from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.api import routes_reports


def test_reports_timeline_endpoint_returns_chronological_items(monkeypatch):
    items = [
        {'id': 'b', 'stored_at_utc': '2026-01-02T00:00:00Z', 'repo_url': 'https://github.com/example/repo-a', 'repo_iq': 75},
        {'id': 'a', 'stored_at_utc': '2026-01-01T00:00:00Z', 'repo_url': 'https://github.com/example/repo-a', 'repo_iq': 60},
    ]
    monkeypatch.setattr(routes_reports, 'list_reports', lambda limit=50: items)

    payload = routes_reports.get_reports_timeline(limit=10)

    assert payload['count'] == 2
    assert payload['items'][0]['id'] == 'a'
    assert payload['items'][1]['id'] == 'b'


def test_reports_timeline_endpoint_repo_filter(monkeypatch):
    items = [
        {'id': 'a', 'repo_url': 'https://github.com/example/repo-a', 'stored_at_utc': '2026-01-01T00:00:00Z'},
        {'id': 'b', 'repo_url': 'https://github.com/example/repo-b', 'stored_at_utc': '2026-01-02T00:00:00Z'},
    ]
    monkeypatch.setattr(routes_reports, 'list_reports', lambda limit=50: items)

    payload = routes_reports.get_reports_timeline(limit=10, repo_url='https://github.com/example/repo-b')

    assert payload['count'] == 1
    assert payload['items'][0]['id'] == 'b'
