#!/usr/bin/env python3
"""Render every card in _source/baraat_cards.html to images.

    python make_cards.py            -> all cards
    python make_cards.py noor shahi -> only these

Output (in this folder):
    Print/<n> <Name>.png      2000 x 2800  (5x7 inch print at 400 dpi)
    WhatsApp/<n> <Name>.jpg   1080 x 1512  (light, for sending on phone)
    All designs.jpg           contact sheet of every design
"""
import asyncio, sys
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
SRC = HERE / "_source" / "baraat_cards.html"
NAMES = {
    "noor": "Noor Lotus",
    "shahi": "Shahi Maroon",
    "zumurrud": "Zumurrud Jharokha",
    "pichwai": "Pichwai Night Lotus",
    "jaali": "Ivory Jaali",
    "gulesurkh": "Gul-e-Surkh",
}


async def main(only):
    (HERE / "Print").mkdir(exist_ok=True)
    (HERE / "WhatsApp").mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
        pg = await b.new_page(viewport={"width": 1100, "height": 1500}, device_scale_factor=2)
        await pg.goto(SRC.as_uri())
        await pg.wait_for_selector("body[data-ready='1']", timeout=60000)
        await pg.wait_for_timeout(800)
        ids = await pg.eval_on_selector_all(".card", "els => els.map(e => e.id)")
        done = []
        for i, cid in enumerate(ids, 1):
            if only and cid not in only:
                continue
            name = f"{i} {NAMES.get(cid, cid)}"
            png = HERE / "Print" / f"{name}.png"
            await pg.locator(f"#{cid}").screenshot(path=str(png))
            im = Image.open(png).convert("RGB")
            im.resize((1080, 1512), Image.LANCZOS).save(HERE / "WhatsApp" / f"{name}.jpg", quality=92, subsampling=0)
            done.append((name, im))
            print("made", name)
        await b.close()
    if not only:
        sheet(done)


def sheet(items):
    cols, tw, th, pad, lab = 3, 600, 840, 40, 60
    rows = (len(items) + cols - 1) // cols
    W, H = cols * tw + (cols + 1) * pad, rows * (th + lab) + (rows + 1) * pad
    S = Image.new("RGB", (W, H), (43, 38, 34))
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(S)
    try:
        font = ImageFont.truetype("georgia.ttf", 30)
    except OSError:
        font = ImageFont.load_default()
    for k, (name, im) in enumerate(items):
        r, c = divmod(k, cols)
        x, y = pad + c * (tw + pad), pad + r * (th + lab + pad)
        S.paste(im.resize((tw, th), Image.LANCZOS), (x, y))
        d.text((x + tw / 2, y + th + 30), name, fill=(232, 210, 160), font=font, anchor="mm")
    S.save(HERE / "All designs.jpg", quality=90)
    print("made All designs.jpg")


if __name__ == "__main__":
    asyncio.run(main(set(sys.argv[1:])))
