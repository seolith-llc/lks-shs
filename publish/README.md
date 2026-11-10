# Publish — the distribution pack (`#Step008`)

Everything needed to ship the PULSE series across publications and platforms. Two kinds of assets:

1. **Paste-ready** (manual upload, no credentials needed): copy below + `youtube/` metadata/thumbnails + `articles/devto/` exports.
2. **Automatable** (needs YOUR credentials, in `auto/`): Bluesky and dev.to have clean APIs; the rest (X, Threads/IG, TikTok, YouTube uploads) are manual or need their developer apps.

## Asset map

| Platform | What to post | Where it lives | How |
|---|---|---|---|
| **dev.to** | 9-part series (canonical mirror) | [`articles/devto/`](articles/devto/) | import each file, or `auto/devto_publish.py` with `DEVTO_API_KEY` |
| **Medium / Hashnode / Substack** | same 9 posts | import from `docs/posts/` | paste markdown; keep `canonical_url` pointing at the GitHub post |
| **Hacker News** | Show HN | [`copy/hackernews-reddit.md`](copy/hackernews-reddit.md) | manual |
| **Reddit** | r/SRE, then r/programming | same file | manual, spaced days apart |
| **YouTube** | 8 episodes (playlist) + 4 Shorts | [`youtube/README.md`](youtube/README.md) + `thumbs/` | manual upload; descriptions paste-ready |
| **TikTok / Reels / Shorts** | 4 vertical videos (46–54 s) | `docs/video/shorts/*.mp4` + captions in [`copy/instagram-tiktok.md`](copy/instagram-tiktok.md) | manual upload |
| **X / Twitter** | 10-post launch thread | [`copy/x-thread.md`](copy/x-thread.md) | manual (API is paid tier) |
| **Bluesky** | 6-skeet thread | [`copy/bluesky-thread.md`](copy/bluesky-thread.md) | manual, or `auto/bluesky_post.py` with an app password |
| **Threads / Instagram** | Reels + 10-slide carousel | [`copy/instagram-tiktok.md`](copy/instagram-tiktok.md) | manual (Meta API needs a business app) |
| **LinkedIn** | launch article/post | [`copy/linkedin.md`](copy/linkedin.md) | manual |

## Launch order (recommended cadence)

1. **Day 0:** dev.to mirror live → Show HN → X thread → Bluesky thread → LinkedIn post.
2. **Day 1:** r/SRE. YouTube playlist (all 8 + shorts). Pin the repo README link to the series overview.
3. **Day 2–5:** one TikTok/Reels short per day (S4 first — the framework explainer — then S1, S2, S3).
4. **Week 2:** r/programming (different angle: the prototype) + Medium/Hashnode mirrors with canonical URLs.
5. **Ongoing:** reply with specific dossier citations; the repo's `docs/research/` is the receipts folder.

## Rules encoded here (from the project's own reference rules)

- **R4 attribution:** posts credit originators (Armstrong, Kephart & Chess, Nygard, Basiri et al.) — keep those credits when reposting.
- **R1 honesty:** every number in the copy traces to a dossier citation. Vendor claims are labeled vendor claims. No L4 autonomy claims anywhere.
- Canonical URL for cross-posted articles: the GitHub `docs/posts/` file.

## Automation (`auto/`) — credential-gated

```bash
# Bluesky (needs an app password: Settings → App passwords)
export BSKY_HANDLE="you.bsky.social" BSKY_APP_PASSWORD="xxxx-xxxx-xxxx"
python3 auto/bluesky_post.py auto/../copy/bluesky-thread.md --dry-run   # preview first

# dev.to (needs an API key: Settings → Extensions → Community)
export DEVTO_API_KEY="..."
python3 auto/devto_publish.py articles/devto/00-series-overview.md --dry-run
```

Neither script posts anything without credentials, and both default to `--dry-run`. X, Threads/Instagram, TikTok, and YouTube uploads remain manual: their APIs require paid tiers or per-app review — paste-ready assets above cover them.
