from __future__ import annotations

from jcloud.client import JumpCloudClient

INSIGHTS_BASE = "https://api.jumpcloud.com/insights/directory/v1"


def query_events(
    client: JumpCloudClient,
    service: str = "all",
    start_date: str | None = None,
    end_date: str | None = None,
    search_term: str | None = None,
    limit: int = 100,
) -> list[dict]:
    """Query Directory Insights events.

    service: 'all', 'directory', 'ldap', 'mdm', 'password_manager',
             'radius', 'software', 'sso', 'systems'
    start_date/end_date: ISO 8601 format (e.g. '2024-01-01T00:00:00Z')
    search_term: filter events by keyword
    """
    body: dict = {"service": [service], "limit": limit}
    if start_date:
        body["start_time"] = start_date
    if end_date:
        body["end_time"] = end_date
    resp = client.session.post(f"{INSIGHTS_BASE}/events", json=body)
    resp.raise_for_status()
    results = resp.json()
    if search_term:
        term = search_term.lower()
        results = [e for e in results if term in str(e).lower()]
    return results


def count_events(
    client: JumpCloudClient,
    service: str = "all",
    start_date: str | None = None,
    end_date: str | None = None,
) -> dict:
    """Get event counts."""
    body: dict = {"service": [service]}
    if start_date:
        body["start_time"] = start_date
    if end_date:
        body["end_time"] = end_date
    resp = client.session.post(f"{INSIGHTS_BASE}/events/count", json=body)
    resp.raise_for_status()
    return resp.json()
