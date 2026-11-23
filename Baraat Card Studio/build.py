#!/usr/bin/env python3
"""Assemble the single-file editor  "Baraat Card Studio.html".

    python build.py                          -> all designs  -> Baraat Card Studio.html
    python build.py --only a1-foo,a2-bar --out C:/tmp/test.html   (designer preview build)
    python build.py --no-end                 -> leave out the video-studio end cards
Design order: designs/order.txt (one folder name per line) if present, else alphabetical.
"""
import argparse, base64, io, json, re, sys
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
FONTS = [
    "Amiri:wght@400;700", "Noto+Nastaliq+Urdu:wght@400;600", "Aref+Ruqaa:wght@400;700", "Scheherazade+New:wght@400;700", "Reem+Kufi:wght@400;600",
    "Great+Vibes", "Pinyon+Script", "Corinthia:wght@400;700", "Ephesis", "Italianno", "Allura", "Parisienne", "Alex+Brush",
    "Monsieur+La+Doulaise", "Rouge+Script", "Mea+Culpa", "Gwendolyn:wght@400;700", "Imperial+Script", "Tangerine:wght@400;700",
    "Petit+Formal+Script", "MonteCarlo", "Beau+Rivage", "Lavishly+Yours", "Birthstone", "WindSong:wght@400;500", "Send+Flowers",
    "Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500", "Cormorant+SC:wght@300;400;500;600", "Cormorant+Upright:wght@300;400;500",
    "Cormorant+Infant:ital,wght@0,400;0,500;1,400", "Cinzel:wght@400;500;600", "Cinzel+Decorative:wght@400;700",
    "Playfair+Display:ital,wght@0,400;0,500;1,400", "Playfair+Display+SC", "Bodoni+Moda:ital,wght@0,400;0,500;1,400",
    "EB+Garamond:ital,wght@0,400;0,500;1,400", "Marcellus", "Marcellus+SC", "Gilda+Display", "Prata", "Italiana", "Forum",
    "Libre+Caslon+Display", "Lora:ital,wght@0,400;0,500;1,400", "Josefin+Sans:wght@300;400", "Tenor+Sans", "Montserrat:wght@300;400;500",
    "Bellefair", "Della+Respira", "Rozha+One", "Yeseva+One",
]
MAX_ASSET = 2000


def asset_uri(path: Path) -> str:
    im = Image.open(path)
    im.load()
    has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    im = im.convert("RGBA" if has_alpha else "RGB")
    if max(im.size) > MAX_ASSET:
        im.thumbnail((MAX_ASSET, MAX_ASSET), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=88 if has_alpha else 84, method=5)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--out", default=str(HERE / "Baraat Card Studio.html"))
    ap.add_argument("--no-end", action="store_true")
    a = ap.parse_args()

    ddir = HERE / "designs"
    folders = sorted(p for p in ddir.iterdir() if (p / "design.js").exists())
    order_f = ddir / "order.txt"
    if order_f.exists():
        order = [l.strip() for l in order_f.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
        folders = [ddir / o for o in order if (ddir / o / "design.js").exists()] + [f for f in folders if f.name not in order]
    if a.only:
        keep = set(a.only.split(","))
        folders = [f for f in folders if f.name in keep]
    else:
        folders = [f for f in folders if not f.name.startswith("_")]  # "_" folders = examples / drafts

    js_parts, used = [], {}
    for f in folders:
        js = (f / "design.js").read_text(encoding="utf-8-sig")
        for name in re.findall(r"""H\.img\(\s*["'`]([^"'`]+)["'`]\s*\)""", js):
            used.setdefault(name, f)
        js_parts.append(f"<script>/* {f.name} */\n{js}\n</script>")

    assets = {}
    for name, f in sorted(used.items()):
        p = HERE / "assets" / name
        if not p.exists():
            p = f / name  # design-local file
        if not p.exists():
            print(f"WARNING: asset not found: {name}", file=sys.stderr)
            continue
        assets[name] = asset_uri(p)

    ends = []
    best = HERE / "studio_endcards" / "best15.json"
    if best.exists() and not a.no_end and not a.only:
        import hashlib
        se = HERE / "studio_endcards"
        md5 = lambda p: hashlib.md5(p.read_bytes()).hexdigest()
        # every rendered set (main + variants) with its own endcards.json
        sets = [se] + [p for p in (se / "variants").glob("*") if (p / "endcards.json").exists()] if (se / "variants").exists() else [se]
        for b in json.loads(best.read_text(encoding="utf-8")):
            i = b["index"] if isinstance(b, dict) else b
            pick = se / "best15" / b.get("file", "") if isinstance(b, dict) else None
            c, src = None, None
            for s in sets:
                for cc in json.loads((s / "endcards.json").read_text(encoding="utf-8")):
                    if cc["index"] != i:
                        continue
                    f = s / Path(cc["file"]).name
                    if f.exists() and (pick is None or not pick.exists() or md5(f) == md5(pick)):
                        c, src = cc, f
                        break
                if c:
                    break
            if not c:
                print(f"WARNING: no matching render for end card {i}", file=sys.stderr)
                continue
            key = f"end-{i:02d}.webp"
            assets[key] = asset_uri(src)
            reason = b.get("reason", "") if isinstance(b, dict) else ""
            ends.append({"name": c["name"], "idea": reason or c.get("cat", ""), "src": key, "hash": c.get("hash", "")})

    shell = (HERE / "core" / "shell.html").read_text(encoding="utf-8")
    out = (shell.replace("{{FONTS}}", "&".join("family=" + f for f in FONTS))
                .replace("{{CSS}}", (HERE / "core" / "core.css").read_text(encoding="utf-8"))
                .replace("{{ASSETS}}", "<script>window.__ASSETS=" + json.dumps(assets) + ";window.__ENDCARDS=" + json.dumps(ends, ensure_ascii=False) + ";</script>")
                .replace("{{CORE_JS}}", (HERE / "core" / "core.js").read_text(encoding="utf-8"))
                .replace("{{DESIGNS}}", "\n".join(js_parts)))
    Path(a.out).write_text(out, encoding="utf-8")
    print(f"built {a.out}  ({len(folders)} designs, {len(ends)} end cards, {len(assets)} images, {len(out)/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
