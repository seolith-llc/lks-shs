#!/usr/bin/env python3
"""Post a Bluesky thread from a copy file (publish/copy/bluesky-thread.md).

Credential-gated: requires BSKY_HANDLE and BSKY_APP_PASSWORD (Settings → App
passwords on bsky.app). Defaults to --dry-run; pass --post to actually send.
Each "**N/** ..."-delimited block becomes one skeet in a reply-thread.
"""
import argparse
import json
import os
import re
import sys
import urllib.request

API = "https://bsky.social/xrpc"


def parse_blocks(path: str) -> list[str]:
    text = open(path).read()
    blocks = re.split(r"\n\*\*\d+/\*\*", text)[1:]  # drop preamble
    posts = []
    for b in blocks:
        t = re.sub(r"^/ [\s\S]*?\n\n", "", b.strip(), count=1)  # drop guidance quote
        t = re.sub(r"^>.*\n+", "", t.strip(), flags=re.M)
        t = re.sub(r"\n+", "\n", t).strip()
        posts.append(t[:300])
    return posts


def post(token: str, did: str, text: str, reply_to: dict | None) -> dict:
    body = {
        "collection": "app.bsky.feed.post",
        "repo": did,
        "record": {
            "text": text, "createdAt": __import__("datetime").datetime.now(
                __import__("datetime").timezone.utc).isoformat(),
            "$type": "app.bsky.feed.post",
            **({"reply": reply_to} if reply_to else {}),
        },
    }
    req = urllib.request.Request(
        f"{API}/com.atproto.repo.createRecord", data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("copy_file")
    ap.add_argument("--post", action="store_true", help="actually send (default: dry-run)")
    args = ap.parse_args()

    posts = parse_blocks(args.copy_file)
    if not posts:
        sys.exit("no posts parsed — expected '**N/**' blocks")
    handle = os.environ.get("BSKY_HANDLE")
    password = os.environ.get("BSKY_APP_PASSWORD")
    if not args.post or not handle or not password:
        print(f"DRY-RUN ({len(posts)} skeets):")
        for i, p in enumerate(posts, 1):
            print(f"\n--- {i} ({len(p)} chars) ---\n{p}")
        if not args.post:
            print("\n(dry run only — pass --post with BSKY_HANDLE/BSKY_APP_PASSWORD to send)")
        return

    req = urllib.request.Request(
        f"{API}/com.atproto.server.createSession",
        data=json.dumps({"identifier": handle, "password": password}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        sess = json.loads(r.read())
    token, did = sess["accessJwt"], sess["did"]

    reply_to = None
    for i, p in enumerate(posts, 1):
        res = post(token, did, p, reply_to)
        uri, cid = res["uri"], res["cid"]
        print(f"[{i}/{len(posts)}] {uri}")
        reply_to = {"root": {"uri": reply_to["root"]["uri"], "cid": reply_to["root"]["cid"]}
                    if reply_to else {"uri": uri, "cid": cid},
                    "parent": {"uri": uri, "cid": cid}}
    print("thread posted.")


if __name__ == "__main__":
    main()
