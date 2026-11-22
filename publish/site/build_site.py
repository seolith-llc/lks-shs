#!/usr/bin/env python3
"""Build the PULSE publication site (static HTML) from docs/ content.

Reads docs/posts/*.md + docs/articles/*.md + docs/animations/*, renders a
self-designed static site into publish/site/site/ (stdlib only). Repo-relative
links are absolutized to GitHub; post-to-post links become site pages; mermaid
blocks render via the mermaid CDN with a <pre> fallback.

Usage: python3 build_site.py   (from anywhere; paths resolved from repo root)
"""
import html
import os
import re
import shutil

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
REPO = "https://github.com/seolith-llc/lks-shs"
OUT = os.path.join(ROOT, "publish", "site", "site")

POSTS = sorted(f for f in os.listdir(os.path.join(ROOT, "docs/posts")) if re.match(r"0[1-8]-", f))
ARTICLES = ["eli5", "entry-level", "professional", "c-suite"]


# ---------------- markdown subset → HTML ----------------
def inline(t: str) -> str:
    t = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" loading="lazy">', t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\w)\*([^*\n]+)\*(?!\w)", r"<em>\1</em>", t)
    return t


def md_to_html(md: str, base_dir: str, for_posts: bool = True) -> tuple[str, bool]:
    """Convert our markdown subset. Returns (html, has_mermaid)."""
    has_mermaid = False
    out, i, lines = [], 0, md.splitlines()
    list_stack = []  # "ul"|"ol"

    def close_lists():
        while list_stack:
            out.append(f"</{list_stack.pop()}>")

    def link(url: str, text: str) -> str:
        if url.startswith(("http", "mailto:", "#")):
            return url
        pm = re.match(r"0(\d)-[a-z0-9-]+\.md", url.split("#")[0])
        if pm and for_posts:
            return f"posts/0{pm.group(1)}.html"
        if url.startswith("animations/") and for_posts:
            return url
        rel = os.path.normpath(os.path.join(base_dir, url)).replace(os.sep, "/")
        kind = "raw" if re.search(r"\.(svg|png|mp4|gif)$", rel) else "blob"
        return f"{REPO}/{kind}/main/{rel}"

    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            lang = ln[3:].strip()
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i]); i += 1
            i += 1
            if lang == "mermaid":
                has_mermaid = True
                out.append('<pre class="mermaid">' + html.escape("\n".join(block)) + "</pre>")
            else:
                out.append("<pre><code>" + html.escape("\n".join(block)) + "</code></pre>")
            continue
        if re.match(r"^\s*\|", ln) and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body_rows = rows[0], rows[2:]
            t = "<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
            for r in body_rows:
                t += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
            out.append(t + "</tbody></table>")
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", ln)
        if m:
            close_lists()
            lvl = min(len(m.group(1)) + 1, 5)  # h1->h2 (page title is h1)
            out.append(f"<h{lvl} id='s{i}'>{inline(m.group(2))}</h{lvl}>")
            i += 1; continue
        if re.match(r"^\s*[-*]\s+\[[ x]\]", ln):
            close_lists()
            done = "[x]" in ln
            txt = re.sub(r"^\s*[-*]\s+\[[ x]\]\s*", "", ln)
            out.append(f'<div class="task {"done" if done else ""}">{"✅" if done else "☐"} {inline(txt)}</div>')
            i += 1; continue
        if re.match(r"^\s*[-*]\s+", ln):
            if not list_stack or list_stack[-1] != "ul":
                close_lists(); out.append("<ul>"); list_stack.append("ul")
            out.append("<li>" + inline(re.sub(r"^\s*[-*]\s+", "", ln).strip()) + "</li>")
            i += 1; continue
        if re.match(r"^\s*\d+\.\s+", ln):
            if not list_stack or list_stack[-1] != "ol":
                close_lists(); out.append("<ol>"); list_stack.append("ol")
            out.append("<li>" + inline(re.sub(r"^\s*\d+\.\s+", "", ln).strip()) + "</li>")
            i += 1; continue
        if ln.startswith(">"):
            close_lists()
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip("> ")); i += 1
            out.append("<blockquote>" + inline(" ".join(q for q in quote if q)) + "</blockquote>")
            continue
        if re.match(r"^\s*(---|\*\*\*)\s*$", ln):
            close_lists(); out.append("<hr>"); i += 1; continue
        if not ln.strip():
            close_lists(); i += 1; continue
        close_lists()
        para = [ln]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|>|\s*[-*]\s|\s*\d+\.\s|\||```|---)", lines[i]):
            para.append(lines[i]); i += 1
        # linkify after inline(): rewrite hrefs
        seg = inline(" ".join(para))
        seg = re.sub(r'href="([^"]+)"', lambda m: f'href="{link(m.group(1), "")}"', seg)
        out.append(f"<p>{seg}</p>")
    close_lists()
    return "\n".join(out), has_mermaid


# ---------------- page chrome ----------------
CSS = """
:root{--bg:#0B2545;--bg2:#071A31;--card:#0A1F3D;--stroke:#3D5A80;--accent:#FFD166;--white:#E0FBFC;--muted:#8DA9C4}
*{box-sizing:border-box;margin:0;padding:0}
body{background:radial-gradient(1100px 600px at 88% -8%,rgba(255,209,102,.09),transparent 60%),
  radial-gradient(900px 500px at 4% 108%,rgba(76,201,240,.09),transparent 60%),
  linear-gradient(135deg,#16396A,#0B2545 55%,#071A31);color:var(--white);
  font:17px/1.65 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;min-height:100vh}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:900px;margin:0 auto;padding:34px 22px 80px}
header.site{display:flex;flex-wrap:wrap;align-items:baseline;gap:14px;margin-bottom:26px;
  border-bottom:1px solid var(--stroke);padding-bottom:16px}
.wordmark{font-size:26px;font-weight:800;letter-spacing:.28em;color:var(--white)}
.wordmark b{color:var(--accent)}
nav.crumbs{color:var(--muted);font-size:14px}
main h1{font-size:34px;line-height:1.2;margin:8px 0 14px}
main h2{font-size:24px;margin:34px 0 10px;color:var(--accent)}
main h3{font-size:19px;margin:24px 0 8px}
main p{margin:10px 0}
ul,ol{margin:10px 0 10px 24px}li{margin:4px 0}
code{background:#071A31;border:1px solid var(--stroke);border-radius:6px;padding:1px 6px;font-size:.86em;
  font-family:ui-monospace,Menlo,Consolas,monospace}
pre{background:#071A31;border:1px solid var(--stroke);border-radius:11px;padding:14px 16px;overflow-x:auto;
  margin:12px 0}pre code{border:0;background:none;padding:0;font-size:.86em;line-height:1.5}
blockquote{border-left:4px solid var(--accent);background:rgba(255,209,102,.06);border-radius:0 11px 11px 0;
  padding:12px 16px;margin:14px 0}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:.94em}
th,td{border:1px solid var(--stroke);padding:8px 10px;text-align:left;vertical-align:top}
th{background:#12305A;color:var(--white)}
tr:nth-child(even) td{background:rgba(10,31,61,.55)}
img{max-width:100%;border-radius:12px;border:1px solid var(--stroke);margin:10px 0;display:block}
.task{margin:6px 0;color:var(--white)}.task.done{color:var(--muted)}
.hero{background:var(--card);border:1px solid var(--stroke);border-radius:16px;padding:26px 28px;margin:14px 0 8px}
.hero h1{font-size:30px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin:16px 0}
.card{background:var(--card);border:1px solid var(--stroke);border-radius:14px;padding:16px 18px}
.card h3{margin:0 0 6px;font-size:17px}
.card p{color:var(--muted);font-size:14.5px;margin:0}
.btn{display:inline-block;background:#12305A;border:1px solid var(--stroke);border-radius:11px;
  padding:10px 18px;margin:8px 8px 8px 0;font-weight:600;color:var(--white)!important}
.btn:hover{border-color:var(--accent);text-decoration:none}
.btn.gold{border-color:var(--accent);color:var(--accent)!important}
footer{margin-top:44px;color:var(--muted);font-size:14px;border-top:1px solid var(--stroke);padding-top:16px}
.series-nav{color:var(--muted);font-size:14px;margin-bottom:8px}
"""

MERMAID_JS = """
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
mermaid.initialize({startOnLoad:true, theme:'base', securityLevel:'loose',
  themeVariables:{darkMode:true, background:'#0A1F3D', primaryColor:'#12305A',
    primaryTextColor:'#E0FBFC', primaryBorderColor:'#3D5A80', lineColor:'#8DA9C4',
    secondaryColor:'#0B2545', tertiaryColor:'#071A31'}});
</script>
"""


def page(title: str, body: str, has_mermaid: bool, crumbs: str) -> str:
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="Self-healing software, engineered with AI — the PULSE series. 180 verified sources, a runnable prototype, and one rule: nothing is healed until an oracle that isn't the healer says so.">
<style>{CSS}</style></head><body><div class="wrap">
<header class="site"><span class="wordmark">PULSE</span>
<span class="crumbs">{crumbs}</span></header>
<main>{body}</main>
<footer>The full evidence trail — 180 verified sources, 7 decision records, the runnable prototype, the complete build audit — lives at
<a href="{REPO}">github.com/seolith-llc/lks-shs</a>.</footer>
</div>{MERMAID_JS if has_mermaid else ""}</body></html>"""


def build() -> None:
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "posts"))
    os.makedirs(os.path.join(OUT, "articles"))
    shutil.copytree(os.path.join(ROOT, "docs/posts/animations"), os.path.join(OUT, "animations"))

    # ---------- index ----------
    idx_body = """
<div class="hero">
<h1>Self-healing software, engineered with AI</h1>
<p>Systems that detect, diagnose, and repair themselves — from kernel mechanisms to LLM agents.
The complete evidence-first series: <strong>180 verified sources</strong>, a framework (<strong>PULSE</strong>),
a runnable prototype, and one rule above all: <em>nothing is healed until an oracle that isn't the healer says so.</em></p>
<a class="btn gold" href="interactive.html">🎛️ Try the live simulator</a>
<a class="btn" href="%s">▶ The repo (prototype + videos + dossiers)</a>
</div>
<h2>The series</h2>""" % REPO
    rows = []
    for f in POSTS:
        n = f[:2]
        title = open(os.path.join(ROOT, "docs/posts", f)).readline().lstrip("# ").strip()
        rows.append(f'<div class="card"><h3><a href="posts/{n}.html">{html.escape(title)}</a></h3>'
                    f'<p>Part {int(n)}</p></div>')
    idx_body += '<div class="cards">' + "".join(rows) + "</div>"
    idx_body += """
<h2>Four altitudes, one story</h2>
<div class="cards">
<div class="card"><h3><a href="articles/eli5.html">Explained like you're five</a></h3><p>Bodies, bikes, and the robot doctor who needs a signature.</p></div>
<div class="card"><h3><a href="articles/entry-level.html">Entry-level programmer</a></h3><p>Six terms, the PULSE model, a runnable demo, a first-week checklist.</p></div>
<div class="card"><h3><a href="articles/professional.html">Seasoned professional</a></h3><p>The precise claim, three corpus verdicts, design-review numbers.</p></div>
<div class="card"><h3><a href="articles/c-suite.html">C-level executives</a></h3><p>Three numbers, three vendor questions, a 90-day plan, a risk register.</p></div>
</div>
<h2>Watch instead</h2>
<p>Eight narrated episodes (2–3 min each) and four vertical shorts live in the
<a href="%s/tree/main/docs/video">repo's video folder</a> — every post links its companion.</p>
""" % REPO
    open(os.path.join(OUT, "index.html"), "w").write(
        page("PULSE — self-healing software, engineered with AI", idx_body, False, "the series at a glance"))

    # ---------- posts ----------
    for f in POSTS:
        n = f[:2]
        md = open(os.path.join(ROOT, "docs/posts", f)).read()
        md = re.sub(r"\*Series:[^\n]*\n", "", md)  # nav line: site has its own crumbs
        body, mm = md_to_html(md, "docs/posts")
        title = md.splitlines()[0].lstrip("# ").strip()
        prev = f"posts/0{int(n)-1}.html" if int(n) > 1 else None
        nxt = f"posts/0{int(n)+1}.html" if int(n) < 8 else None
        nav = '<p class="series-nav">' + (f'<a href="{prev}">← part {int(n)-1}</a> · ' if prev else "") + \
              f'<a href="../index.html">series</a>' + (f' · <a href="{nxt}">part {int(n)+1} →</a></p>' if nxt else "</p>")
        open(os.path.join(OUT, "posts", f"{n}.html"), "w").write(
            page(title, nav + body, mm, f'<a href="../index.html">series</a> · part {int(n)}'))

    # ---------- articles ----------
    for a in ARTICLES:
        md = open(os.path.join(ROOT, "docs/articles", a + ".md")).read()
        body, mm = md_to_html(md, "docs/articles", for_posts=False)
        title = md.splitlines()[0].lstrip("# ").strip()
        open(os.path.join(OUT, "articles", a + ".html"), "w").write(
            page(title, body, mm, f'<a href="../index.html">series</a> · article'))

    # ---------- interactive page (fix repo-relative md links -> GitHub) ----------
    ip = open(os.path.join(ROOT, "docs/animations/pulse-interactive.html")).read()
    ip = ip.replace('../architecture/state-workflow-model.md',
                    f"{REPO}/blob/main/docs/architecture/state-workflow-model.md")
    open(os.path.join(OUT, "interactive.html"), "w").write(ip)

    n_files = sum(len(fs) for _, _, fs in os.walk(OUT))
    print(f"OK site -> {OUT} ({n_files} files)")


if __name__ == "__main__":
    build()
