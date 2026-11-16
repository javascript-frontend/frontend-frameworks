#!/usr/bin/env python3
"""Refresh live GitHub stars/forks and npm weekly downloads in frameworks.json."""

from __future__ import annotations

from datetime import date
import json
import os
from pathlib import Path
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "frameworks.json"
DOCS_DATA_PATH = ROOT / "docs" / "frameworks.json"


def fetch_json(url: str, headers: dict[str, str] | None = None) -> dict:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    dataset = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    gh_headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        gh_headers["Authorization"] = f"Bearer {token}"

    for fw in dataset["frameworks"]:
        repo = fw["github_repo"]
        pkg = urllib.parse.quote(fw["npm_package"], safe="")
        gh = fetch_json(f"https://api.github.com/repos/{repo}", gh_headers)
        fw["stars"] = gh["stargazers_count"]
        fw["forks"] = gh["forks_count"]

        npm_latest = fetch_json(f"https://registry.npmjs.org/{pkg}/latest")
        fw["latest_version"] = npm_latest["version"]

        npm_dl = fetch_json(f"https://api.npmjs.org/downloads/point/last-week/{pkg}")
        fw["npm_weekly_downloads"] = npm_dl["downloads"]
        print(f"Updated {fw['id']}: v{fw['latest_version']} | {fw['stars']} stars | {fw['npm_weekly_downloads']} npm/wk")

    dataset["metadata"]["verified_at"] = date.today().isoformat()
    rendered = json.dumps(dataset, indent=2) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_DATA_PATH.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
