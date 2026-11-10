#!/usr/bin/env python3
"""Publish a dev.to article export (publish/articles/devto/*.md) via the dev.to API.

Credential-gated: requires DEVTO_API_KEY (Settings → Extensions → Community API
keys). Defaults to --dry-run; --post creates an UNLISTED draft (review, add
images, then publish in the UI). Files already carry dev.to front-matter.
"""
import argparse
import json
import os
import re
import sys
import urllib.request

API = "https://dev.to/api/articles"


def split_front_matter(path: str) -> tuple[dict, str]:
    text = open(path).read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        sys.exit(f"{path}: missing front-matter")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    return meta, m.group(2)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--post", action="store_true", help="create a draft on dev.to (default: dry-run)")
    args = ap.parse_args()

    meta, body = split_front_matter(args.file)
    tags = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()][:4]
    payload = {"article": {"title": meta.get("title", ""), "body_markdown": body,
                           "published": False, "tags": tags}}
    if "canonical" in meta:
        payload["article"]["canonical_url"] = meta["canonical"]

    if not args.post or not os.environ.get("DEVTO_API_KEY"):
        print("DRY-RUN payload:")
        print(json.dumps({**payload, "article": {**payload["article"],
                                                 "body_markdown": body[:300] + " ..."}}, indent=2))
        if not args.post:
            print("\n(dry run only — pass --post with DEVTO_API_KEY to create an unlisted draft)")
        return

    req = urllib.request.Request(
        API, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "api-key": os.environ["DEVTO_API_KEY"]})
    with urllib.request.urlopen(req, timeout=60) as r:
        res = json.loads(r.read())
    print(f"created draft: {res.get('url')} (published=false — review, then publish in the UI)")


if __name__ == "__main__":
    main()
