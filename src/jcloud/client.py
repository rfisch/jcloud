from __future__ import annotations

import json
import os
import sys

import click
import requests
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

V1_BASE = "https://console.jumpcloud.com/api"
V2_BASE = "https://console.jumpcloud.com/api/v2"

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


class JumpCloudClient:
    def __init__(self, api_key: str | None = None, org_id: str | None = None):
        self.api_key = api_key or os.environ.get("JUMPCLOUD_API_KEY")
        if not self.api_key:
            click.echo("Error: JUMPCLOUD_API_KEY not set. Export it or add to .env", err=True)
            sys.exit(1)

        self.org_id = org_id or os.environ.get("JUMPCLOUD_ORG_ID")
        self.session = requests.Session()
        self.session.headers.update({**DEFAULT_HEADERS, "x-api-key": self.api_key})
        if self.org_id:
            self.session.headers["x-org-id"] = self.org_id

    def _url(self, path: str, version: int = 1) -> str:
        base = V1_BASE if version == 1 else V2_BASE
        return f"{base}{path}"

    def get(self, path: str, version: int = 1, **kwargs) -> requests.Response:
        return self.session.get(self._url(path, version), **kwargs)

    def post(self, path: str, version: int = 1, **kwargs) -> requests.Response:
        return self.session.post(self._url(path, version), **kwargs)

    def put(self, path: str, version: int = 1, **kwargs) -> requests.Response:
        return self.session.put(self._url(path, version), **kwargs)

    def patch(self, path: str, version: int = 1, **kwargs) -> requests.Response:
        return self.session.patch(self._url(path, version), **kwargs)

    def delete(self, path: str, version: int = 1, **kwargs) -> requests.Response:
        return self.session.delete(self._url(path, version), **kwargs)

    def paginate(
        self,
        path: str,
        version: int = 1,
        limit: int = 100,
        results_key: str | None = "results",
    ) -> list[dict]:
        """Auto-paginate through all results."""
        all_results: list[dict] = []
        skip = 0
        while True:
            params: dict = {"limit": limit, "skip": skip}
            if version == 1:
                params["sort"] = "_id"
            resp = self.get(path, version=version, params=params)
            resp.raise_for_status()
            data = resp.json()

            if results_key:
                items = data.get(results_key, [])
            else:
                items = data if isinstance(data, list) else []

            if not items:
                break
            all_results.extend(items)
            if len(items) < limit:
                break
            skip += limit
        return all_results

    def paginate_v2(self, path: str, limit: int = 100) -> list[dict]:
        """Auto-paginate V2 endpoints (return lists directly, no wrapper key)."""
        return self.paginate(path, version=2, limit=limit, results_key=None)


def get_client(ctx: click.Context) -> JumpCloudClient:
    """Retrieve or create the client from Click context."""
    if "client" not in ctx.obj:
        ctx.obj["client"] = JumpCloudClient(
            api_key=ctx.obj.get("api_key"),
            org_id=ctx.obj.get("org_id"),
        )
    return ctx.obj["client"]


def output(data: list[dict] | dict, fmt: str = "table", columns: list[str] | None = None):
    """Format and print output as table or JSON."""
    if fmt == "json":
        click.echo(json.dumps(data, indent=2, default=str))
        return

    if isinstance(data, dict):
        rows = [[k, v] for k, v in data.items()]
        click.echo(tabulate(rows, headers=["Field", "Value"], tablefmt="simple"))
        return

    if not data:
        click.echo("No results.")
        return

    if columns:
        rows = [{c: item.get(c, "") for c in columns} for item in data]
    else:
        rows = data

    click.echo(tabulate(rows, headers="keys", tablefmt="simple"))
