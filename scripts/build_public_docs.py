from pathlib import Path
import html
import re
import shutil

import markdown

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "research" / "documents"

DOCUMENTS = [
    {
        "id": "pl-001",
        "label": "PL-001",
        "title": "Loom Research Charter / Core Specification",
        "source": ROOT / "specifications" / "PL-001_Spec PL-001.md",
        "description": "The foundational specification governing the Loom research system, its purpose, structure, epistemic discipline, and research governance.",
    },
    {
        "id": "pl-307",
        "label": "PL-307",
        "title": "Claims, Epistemic Status, Verification & Promotion Specification",
        "source": ROOT / "specifications" / "PL-307_PL-307 — Claims, Epistemic Status, Verification & Promotion Specification.md",
        "description": "The specification that separates workflow status, epistemic status, verification level, and promotion stage—and defines how claims move through evidence, review, contradiction, correction, and governance.",
    },
]

PAGE_CSS = r"""
:root{--paper:#f4f0e8;--ink:#171714;--muted:#6b675f;--rule:#cfc7b8;--teal:#146b68;--rust:#9a4d32;--white:#fffdf8;}
body{background:var(--paper);color:var(--ink);font-family:Georgia,'Times New Roman',serif;margin:0;line-height:1.72}
a{color:var(--teal)}
.doc-shell{max-width:1180px;margin:0 auto;padding:0 28px 80px}
.doc-top{border-bottom:1px solid var(--rule);padding:28px 0 18px;display:flex;justify-content:space-between;gap:24px;align-items:center;font-family:Arial,sans-serif;font-size:.82rem;letter-spacing:.08em;text-transform:uppercase}
.doc-top a{text-decoration:none}.wordmark{font-weight:800;color:var(--ink)}.wordmark span{color:var(--rust)}
.doc-head{padding:76px 0 48px;max-width:900px;border-bottom:4px solid var(--ink)}
.eyebrow{font:700 .76rem/1.3 Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:var(--teal)}
.doc-head h1{font-size:clamp(2.4rem,5vw,4.8rem);line-height:1.02;margin:.25em 0 .35em;letter-spacing:-.035em}
.doc-dek{font-size:1.22rem;color:var(--muted);max-width:760px;margin:0}
.doc-meta{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px;font:700 .72rem Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase}
.doc-meta span{border:1px solid var(--rule);padding:7px 10px;background:rgba(255,253,248,.55)}
.doc-body{max-width:850px;padding-top:48px;font-size:1.03rem}
.doc-body h1{font-size:2.6rem;line-height:1.08;margin:1.4em 0 .5em}.doc-body h2{font-size:2rem;line-height:1.15;margin:1.7em 0 .55em}.doc-body h3{font-size:1.35rem;margin:1.5em 0 .4em}
.doc-body p{margin:.8em 0}.doc-body li{margin:.25em 0}.doc-body blockquote{border-left:4px solid var(--teal);padding:.2em 1.3em;margin:1.5em 0;background:rgba(20,107,104,.06);font-size:1.12em}.doc-body blockquote p{margin:.4em 0}
.doc-body table{width:100%;border-collapse:collapse;margin:1.6em 0;font-size:.94em;background:var(--white)}.doc-body th,.doc-body td{border:1px solid var(--rule);padding:10px 12px;text-align:left;vertical-align:top}.doc-body th{font-family:Arial,sans-serif;font-size:.75rem;text-transform:uppercase;letter-spacing:.06em}
.doc-body pre{overflow:auto;background:#20211e;color:#f4f0e8;padding:18px;border-left:4px solid var(--rust);font:.83rem/1.55 'SFMono-Regular',Consolas,monospace}.doc-body code{font-family:'SFMono-Regular',Consolas,monospace;font-size:.88em;background:rgba(0,0,0,.05);padding:.12em .28em}.doc-body pre code{background:none;padding:0}
.doc-body hr{border:0;border-top:1px solid var(--rule);margin:3em 0}.doc-body img{max-width:100%}
.doc-footer{margin-top:70px;padding-top:20px;border-top:1px solid var(--rule);font:.78rem/1.5 Arial,sans-serif;color:var(--muted);display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}
@media(max-width:700px){.doc-shell{padding:0 18px 50px}.doc-head{padding:52px 0 34px}.doc-body{font-size:1rem}.doc-top{align-items:flex-start;flex-direction:column}}
"""


def clean_source(text: str) -> str:
    # PL-307 currently contains an internal drafting instruction before its title.
    # It is not part of the specification and should not appear in the public document.
    text = re.sub(r"^\ufeff?Assess this as if you are an advisor to a post doctoral student: Pick apart all issues/inconsistencies\.\s*", "", text, count=1)
    return text.strip()


def first_heading(text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def render(doc):
    if not doc["source"].exists():
        raise SystemExit(f"Missing public document source: {doc['source']}")
    source = clean_source(doc["source"].read_text(encoding="utf-8"))
    rendered = markdown.markdown(source, extensions=["extra", "tables", "fenced_code", "toc"], output_format="html5")
    title = first_heading(source, doc["title"])
    source_name = doc["source"].name
    out_dir = OUT / doc["id"]
    out_dir.mkdir(parents=True, exist_ok=True)

    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{html.escape(doc['description'])}">
<title>{html.escape(doc['label'] + ' — ' + title)} · Project Loom</title>
<style>{PAGE_CSS}</style>
</head>
<body>
<div class="doc-shell">
<header class="doc-top">
  <a class="wordmark" href="../../">LOOM<span>.</span></a>
  <nav><a href="../record/">Research Record</a> &nbsp;·&nbsp; <a href="../">Research</a></nav>
</header>
<section class="doc-head">
  <div class="eyebrow">PUBLIC RESEARCH DOCUMENT · {html.escape(doc['label'])}</div>
  <h1>{html.escape(title)}</h1>
  <p class="doc-dek">{html.escape(doc['description'])}</p>
  <div class="doc-meta"><span>Source: {html.escape(source_name)}</span><span>Rendered from the current repository document</span></div>
</section>
<article class="doc-body">
{rendered}
</article>
<footer class="doc-footer">
  <span>PROJECT LOOM · PUBLIC RESEARCH RECORD</span>
  <span>This page publishes the document itself; the repository remains the underlying source of record.</span>
</footer>
</div>
</body>
</html>
'''
    (out_dir / "index.html").write_text(page, encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for child in OUT.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
    for doc in DOCUMENTS:
        render(doc)
    print("Generated public documents:")
    for doc in DOCUMENTS:
        print(f" - {doc['label']}: /research/documents/{doc['id']}/")


if __name__ == "__main__":
    main()
