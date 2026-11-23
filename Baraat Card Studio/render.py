#!/usr/bin/env python3
"""Render designs from a built studio HTML to images.

    python render.py                    -> all designs of "Baraat Card Studio.html" into Print/ (2000x2800) and WhatsApp/ (1080x1512)
    python render.py --html C:/tmp/t.html --only a1-foo --out C:/tmp/shots --scale 1   (quick preview, 1000x1400 PNG)
"""
import argparse, asyncio, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent


async def run(a):
    html = Path(a.html).resolve()
    q = "?render" + (f"&only={a.only}" if a.only else "")
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
        pg = await b.new_page(viewport={"width": 1100, "height": 1500}, device_scale_factor=a.scale)
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(html.as_uri() + q)
        await pg.wait_for_selector("body[data-ready='1']", timeout=120000)
        await pg.wait_for_timeout(500)
        cards = await pg.eval_on_selector_all("#renderroot .card", "els => els.map(e => e.dataset.d)")
        names = await pg.evaluate("Object.fromEntries(DESIGNS.map((d,i)=>[d.id,[i+1,d.name]]))")
        out = []
        for cid in cards:
            n, name = names[cid]
            fname = re.sub(r'[\\/:*?"<>|]', "", f"{n:02d} {name}")
            loc = pg.locator(f'#renderroot .card[data-d="{cid}"]')
            if a.out:
                Path(a.out).mkdir(parents=True, exist_ok=True)
                path = Path(a.out) / f"{fname}.png"
                await loc.screenshot(path=str(path))
            else:
                (HERE / "Print").mkdir(exist_ok=True)
                (HERE / "WhatsApp").mkdir(exist_ok=True)
                path = HERE / "Print" / f"{fname}.png"
                await loc.screenshot(path=str(path))
                Image.open(path).convert("RGB").resize((1080, 1512), Image.LANCZOS).save(
                    HERE / "WhatsApp" / f"{fname}.jpg", quality=92, subsampling=0)
            out.append((fname, path))
            print("made", fname)
        for e in errs:
            print("PAGE:", e)
        await b.close()
    if a.sheet or not a.out:
        sheet(out, Path(a.out) / "_sheet.jpg" if a.out else HERE / "All new designs.jpg")


def sheet(items, dest, cols=5, tw=400):
    if not items:
        return
    th, pad, lab = int(tw * 1.4), 24, 44
    rows = (len(items) + cols - 1) // cols
    S = Image.new("RGB", (cols * tw + (cols + 1) * pad, rows * (th + lab) + (rows + 1) * pad), (34, 30, 26))
    d = ImageDraw.Draw(S)
    try:
        font = ImageFont.truetype("georgia.ttf", 20)
    except OSError:
        font = ImageFont.load_default()
    for k, (name, path) in enumerate(items):
        r, c = divmod(k, cols)
        x, y = pad + c * (tw + pad), pad + r * (th + lab + pad)
        S.paste(Image.open(path).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
        d.text((x + tw / 2, y + th + 22), name, fill=(232, 210, 160), font=font, anchor="mm")
    S.save(dest, quality=88)
    print("sheet", dest)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", default=str(HERE / "Baraat Card Studio.html"))
    ap.add_argument("--only", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--scale", type=float, default=2)
    ap.add_argument("--sheet", action="store_true")
    asyncio.run(run(ap.parse_args()))
