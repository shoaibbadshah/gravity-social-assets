#!/usr/bin/env python3
"""Render a post spec (JSON) into 1080x1350 PNG slides.

Usage: python3 tools/render.py posts/<folder>/post.json
Writes slide-01.png, slide-02.png, ... next to post.json.

Spec format:
{
  "slides": [
    {"type": "cover", "eyebrow": "...", "title": "HTML ok", "sub": "...", "pills": ["..."]},
    {"type": "point", "n": "01", "title": "...", "body": "HTML ok"},
    {"type": "list", "eyebrow": "...", "title": "...", "items": ["HTML ok", ...]},
    {"type": "compare", "eyebrow": "...", "title": "...", "cols": [{"k": "label", "name": "...", "text": "..."}]},
    {"type": "myth", "myth": "...", "fact": "..."},
    {"type": "cta", "eyebrow": "...", "title": "...", "sub": "...", "button": "..."}
  ]
}
"""
import json, sys, pathlib, html
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
CSS = (ROOT / "template.css").read_text()
HANDLE = "@gravitymarketingltd"


def frame(inner, idx, total, last):
    counter = f"{idx:02d} / {total:02d}" if total > 1 else "DEV STUDIO"
    hint = "SWIPE →" if total > 1 and not last else "WEB · MOBILE · BACKEND"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="slide">
<div class="br tl"></div><div class="br tr"></div><div class="br bl"></div><div class="br bottomright"></div>
<div class="top"><span class="wordmark">GRAVITY</span><span class="counter">{counter}</span></div>
<div class="content">{inner}</div>
<div class="bottom"><span>{HANDLE}</span><span class="tag">{hint}</span></div>
</div></body></html>"""


def slide_html(s):
    t = s["type"]
    eb = f'<div class="eyebrow">{s["eyebrow"]}</div>' if s.get("eyebrow") else ""
    if t == "cover":
        pills = "".join(f'<span class="pill">{html.escape(p)}</span>' for p in s.get("pills", []))
        pills = f'<div class="pills">{pills}</div>' if pills else ""
        sub = f'<p class="sub">{s["sub"]}</p>' if s.get("sub") else ""
        return f'{eb}<h1>{s["title"]}</h1>{sub}{pills}'
    if t == "point":
        return f'<div class="num">{s["n"]}</div><h2>{s["title"]}</h2><p class="body">{s["body"]}</p>'
    if t == "list":
        items = "".join(f"<li>{i}</li>" for i in s["items"])
        return f'{eb}<h2>{s["title"]}</h2><ul class="items">{items}</ul>'
    if t == "compare":
        cols = "".join(
            f'<div class="col"><div class="k">{c.get("k","")}</div><h3>{c["name"]}</h3><p>{c["text"]}</p></div>'
            for c in s["cols"])
        return f'{eb}<h2>{s["title"]}</h2><div class="cols">{cols}</div>'
    if t == "myth":
        return (f'<div class="myth">✕ MYTH</div><h2>{s["myth"]}</h2>'
                f'<div class="fact" style="margin-top:30px">✓ REALITY</div><p class="body">{s["fact"]}</p>')
    if t == "cta":
        sub = f'<p class="sub">{s["sub"]}</p>' if s.get("sub") else ""
        btn = f'<div class="cta-box">{s["button"]}</div>' if s.get("button") else ""
        return f'{eb}<h1>{s["title"]}</h1>{sub}{btn}'
    raise ValueError(f"unknown slide type {t}")


def main(spec_path):
    spec_path = pathlib.Path(spec_path)
    spec = json.loads(spec_path.read_text())
    slides = spec["slides"]
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, s in enumerate(slides, 1):
            pg.set_content(frame(slide_html(s), i, len(slides), i == len(slides)))
            pg.wait_for_timeout(150)
            f = spec_path.parent / f"slide-{i:02d}.png"
            pg.screenshot(path=str(f), clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
            out.append(f.name)
        b.close()
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1])
