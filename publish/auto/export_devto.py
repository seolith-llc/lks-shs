#!/usr/bin/env python3
"""Export docs/posts/*.md to dev.to-ready files in publish/articles/devto/.

Adds dev.to front-matter and rewrites repo-relative links to absolute GitHub
URLs so the cross-post renders standalone. Canonical URL points at the GitHub
original (keeps SEO attribution to the repo).
"""
import os
import re
import sys

REPO = "https://github.com/seolith-llc/lks-shs"
RAW = f"{REPO}/raw/main"

TAGS = {
    "01": "erlang, reliability, softwareengineering, history",
    "02": "linux, kernel, ebpf, systems",
    "03": "ai, aiops, llm, devops",
    "04": "architecture, systemdesign, softwareengineering, reliability",
    "05": "python, tutorial, opensource, reliability",
    "06": "smallbusiness, devops, selfhosting, reliability",
    "07": "devops, leadership, governance, aiops",
    "08": "ai, security, sre, bestpractices",
}

TITLES = {
    "01": "Self-Healing Software, Part 1: Seventy Years of Self-Healing",
    "02": "Self-Healing Software, Part 2: The Systems Layer",
    "03": "Self-Healing Software, Part 3: What Actually Shipped in the AI Era",
    "04": "Self-Healing Software, Part 4: The PULSE Framework",
    "05": "Self-Healing Software, Part 5: PULSE in ~600 Lines of Python",
    "06": "Self-Healing Software, Part 6: The Small-Business Playbook ($0–50/month)",
    "07": "Self-Healing Software, Part 7: The Enterprise Playbook",
    "08": "Self-Healing Software, Part 8: Risks, Anti-Patterns, and the Road to L4",
}


def absolutize(text: str, src_dir: str) -> str:
    def repl(m):
        url = m.group(1)
        if url.startswith(("http://", "https://", "mailto:", "#")):
            return m.group(0)
        rel = os.path.normpath(os.path.join(src_dir, url)).replace("\\", "/")
        kind = "raw" if re.search(r"\.(svg|png|jpg|gif|mp4)$", rel) else "blob"
        return f"]({REPO}/{kind}/main/{rel})"
    text = re.sub(r"\]\(([^)]+)\)", repl, text)
    # strip the series-nav line + video-file mentions that read oddly off-repo
    text = re.sub(r"\*Series:.*?\*\n", "", text)
    return text


def main() -> None:
    src = "docs/posts"
    dst = "publish/articles/devto"
    os.makedirs(dst, exist_ok=True)
    for f in sorted(os.listdir(src)):
        if not re.match(r"\d\d-.*\.md$", f):
            continue
        n = f[:2]
        if n == "00":
            continue  # overview stays as the repo landing page
        body = absolutize(open(os.path.join(src, f)).read(), src)
        front = (
            "---\n"
            f'title: "{TITLES[n]}"\n'
            "published: false\n"
            f"description: Part {int(n)} of an evidence-first series on self-healing "
            "software — 180 verified sources, the PULSE framework, a runnable prototype.\n"
            f"tags: {TAGS[n]}\n"
            f"canonical_url: {REPO}/blob/main/{src}/{f}\n"
            "series: self-healing-software\n"
            "---\n\n"
        )
        out = os.path.join(dst, f)
        open(out, "w").write(front + body)
        print(f"  {out}")
    print(f"OK -> {dst} (8 exports)")


if __name__ == "__main__":
    main()
