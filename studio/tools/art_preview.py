#!/usr/bin/env python3
"""
Preview every <symbol> in one or more defs.svg files: each symbol large and small, on several palettes
(dark Baraat, light ivory, Walima taupe, crimson, mint) and all four skin tones, as one PNG.

    python studio/tools/art_preview.py studio/modules/art/couple/defs.svg  OUT.png  [--only art-dulha,art-dulhan]
"""
import argparse
import asyncio
import re
from pathlib import Path

from playwright.async_api import async_playwright

PALETTES = [
    ("Espresso Baraat", dict(bg="#3B2A20", it="#F3E6CC", ef="#F4EAD8", cd="#FBF4E6", ink="#2E2018", ink2="#7A5A24", acc="#B8913F", bl="#9E3B3B", lv="#5E6B3A")),
    ("Crimson Baraat", dict(bg="#4A0E16", it="#F8E7C9", ef="#F3DFC0", cd="#FFF6E9", ink="#3A0A10", ink2="#8C1C2A", acc="#C9A24E", bl="#B3202F", lv="#2F5D46")),
    ("Taupe Walima", dict(bg="#6F5E52", it="#FBF3E8", ef="#FAF3EA", cd="#FFFAF3", ink="#3A2C25", ink2="#8A5E4A", acc="#A97C5F", bl="#C27C80", lv="#7D8B6A")),
    ("Mint Walima", dict(bg="#DDEBE3", it="#24433A", ef="#F6FBF8", cd="#FFFFFF", ink="#1F3A32", ink2="#4E7A68", acc="#A88A4E", bl="#E7A9B4", lv="#6FA58C")),
    ("Light ivory", dict(bg="#E6D6BD", it="#3E2E22", ef="#FBF7F0", cd="#FFFCF6", ink="#3A2A1E", ink2="#876433", acc="#A8834E", bl="#B86E6A", lv="#7A875C")),
]
SKINS = ["#F1CBA8", "#D9A47E", "#B97E57", "#875839"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("defs", nargs="+", help="defs.svg file(s); the last argument is the output PNG")
    ap.add_argument("--only", help="comma list of symbol ids")
    ap.add_argument("--big", type=int, default=260, help="large preview height in px")
    a = ap.parse_args()
    *defs_files, out = a.defs
    defs = "\n".join(Path(f).read_text(encoding="utf-8-sig") for f in defs_files)
    syms = re.findall(r'<symbol\b[^>]*\bid="([^"]+)"[^>]*\bviewBox="([^"]+)"', defs)
    syms += [(i, v) for v, i in re.findall(r'<symbol\b[^>]*\bviewBox="([^"]+)"[^>]*\bid="([^"]+)"', defs)]
    seen, order = set(), []
    for i, v in syms:
        if i not in seen:
            seen.add(i)
            order.append((i, v))
    if a.only:
        keep = set(a.only.split(","))
        order = [s for s in order if s[0] in keep]
    if not order:
        raise SystemExit("no <symbol id=... viewBox=...> found")

    def cell(i, vb, h):
        x, y, w, hh = (float(t) for t in vb.replace(",", " ").split())
        return f'<svg viewBox="{vb}" style="height:{h}px;width:{h * w / hh:.0f}px"><use href="#{i}"/></svg>'

    rows = []
    for pi, (pname, pal) in enumerate(PALETTES):
        vars_ = ";".join(f"--{k}:{v}" for k, v in pal.items())
        for idx, (sid, vb) in enumerate(order):
            skin = SKINS[(pi + idx) % len(SKINS)]
            rows.append(
                f'<div class="row" style="{vars_};--skin:{skin};--hair:#22160F">'
                f'<div class="lab">{pname}<br><b>{sid}</b><br><small>skin {skin}</small></div>'
                f'<div class="on bg">{cell(sid, vb, a.big)}</div>'
                f'<div class="on cd">{cell(sid, vb, a.big)}</div>'
                f'<div class="on bg">{cell(sid, vb, 56)}{cell(sid, vb, 34)}</div></div>')
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#888;font:13px/1.3 Segoe UI,Arial,sans-serif}}
.row{{display:flex;gap:8px;align-items:stretch;padding:6px;border-bottom:1px solid #666}}
.lab{{width:150px;color:#fff}} .lab small{{opacity:.7}}
.on{{display:flex;align-items:flex-end;gap:10px;padding:10px;border-radius:8px}}
.bg{{background:var(--bg)}} .cd{{background:var(--cd)}}
svg{{overflow:visible}}
</style></head><body><svg width="0" height="0" style="position:absolute"><defs>{defs}</defs></svg>
{''.join(rows)}</body></html>"""
    tmp = Path(out).with_suffix(".html")
    tmp.write_text(page, encoding="utf-8")

    async def shot():
        async with async_playwright() as p:
            b = await p.chromium.launch(args=["--force-color-profile=srgb"])
            pg = await b.new_page(viewport={"width": 1100, "height": 800})
            await pg.goto(tmp.resolve().as_uri())
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=out, full_page=True)
            await b.close()
    asyncio.run(shot())
    print(f"{len(order)} symbols x {len(PALETTES)} palettes -> {out}")


if __name__ == "__main__":
    main()
