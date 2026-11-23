#!/usr/bin/env python3
"""
Turn a downloaded photo into a studio background-photo module.

    python studio/tools/add_image.py SOURCE.jpg red-roses "Red roses" --credit "Photo by X on Unsplash" \
        --source https://unsplash.com/photos/... --license "Unsplash License" [--focus 0.5,0.4] [--quality 78]

Crops to 9:16 around the focus point (x,y in 0..1), resizes to 1080x1920, saves WebP and writes
studio/modules/images/<id>/{image.webp, meta.json}.
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("id")
    ap.add_argument("name")
    ap.add_argument("--credit", default="")
    ap.add_argument("--source-url", dest="source_url", default="")
    ap.add_argument("--license", default="")
    ap.add_argument("--focus", default="0.5,0.5", help="crop centre x,y as fractions")
    ap.add_argument("--quality", type=int, default=78)
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--order", type=int, default=100)
    a = ap.parse_args()

    im = ImageOps.exif_transpose(Image.open(a.source)).convert("RGB")
    W, H = im.size
    fx, fy = (float(v) for v in a.focus.split(","))
    target = 9 / 16
    if W / H > target:          # too wide: crop width
        cw, ch = round(H * target), H
    else:                       # too tall: crop height
        cw, ch = W, round(W / target)
    x0 = min(max(round(fx * W - cw / 2), 0), W - cw)
    y0 = min(max(round(fy * H - ch / 2), 0), H - ch)
    im = im.crop((x0, y0, x0 + cw, y0 + ch))
    out_w = min(a.width, cw)
    im = im.resize((out_w, round(out_w / target)), Image.LANCZOS)

    d = ROOT / "modules" / "images" / a.id
    d.mkdir(parents=True, exist_ok=True)
    dest = d / "image.webp"
    im.save(dest, "WEBP", quality=a.quality, method=6)
    meta = {"name": a.name, "file": "image.webp", "credit": a.credit, "source": a.source_url,
            "license": a.license, "order": a.order}
    (d / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{a.id}: {im.size[0]}x{im.size[1]} {dest.stat().st_size / 1024:.0f} KB  (crop from {W}x{H} at {x0},{y0})")


if __name__ == "__main__":
    main()
