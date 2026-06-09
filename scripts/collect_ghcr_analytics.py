import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


OWNER = "vrtnis"
PACKAGES = ["browsergym-miniwob"]
OUT_DIR = Path("analytics/ghcr")


def gh_api(path):
    token = os.environ["GH_TOKEN"]
    request = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def versions_for(package):
    endpoints = [
        f"/user/packages/container/{package}/versions?per_page=100",
        f"/users/{OWNER}/packages/container/{package}/versions?per_page=100",
    ]
    errors = []
    for endpoint in endpoints:
        try:
            return endpoint, gh_api(endpoint)
        except urllib.error.HTTPError as exc:
            errors.append({"endpoint": endpoint, "status": exc.code, "reason": exc.reason})
    raise RuntimeError(json.dumps(errors))


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    index = {"generated_at": generated_at, "packages": []}

    for package in PACKAGES:
        endpoint, versions = versions_for(package)
        normalized_versions = []
        total_downloads = 0
        for version in versions:
            downloads = version.get("download_count")
            if isinstance(downloads, int):
                total_downloads += downloads
            normalized_versions.append(
                {
                    "id": version.get("id"),
                    "name": version.get("name"),
                    "tags": version.get("metadata", {})
                    .get("container", {})
                    .get("tags", []),
                    "created_at": version.get("created_at"),
                    "updated_at": version.get("updated_at"),
                    "download_count": downloads,
                    "html_url": version.get("html_url"),
                }
            )

        payload = {
            "package": package,
            "owner": OWNER,
            "generated_at": generated_at,
            "source_endpoint": endpoint,
            "version_count": len(normalized_versions),
            "total_downloads": total_downloads,
            "versions": normalized_versions,
        }
        (OUT_DIR / f"{package}.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        index["packages"].append(
            {
                "package": package,
                "version_count": payload["version_count"],
                "total_downloads": payload["total_downloads"],
            }
        )

    (OUT_DIR / "index.json").write_text(
        json.dumps(index, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"collect_ghcr_analytics failed: {exc}", file=sys.stderr)
        raise
