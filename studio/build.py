#!/usr/bin/env python3
"""
Build the Wedding Invite Studio - one self-contained HTML file - from the pieces in this folder.

    python studio/build.py                              -> wedding_invite_studio_fully_customizable.html
    python studio/build.py --out C:/tmp/t.html --only intros:curtain   core + just that module (for testing)
    python studio/build.py --check                      validate everything, write nothing

Layout (details in MODULES.md):
    base_head.html  template.html  core/core.css  core/core.js
    fonts.json  palettes.json  samples.json
    modules/<type>/<id>/meta.json  + optional stage.html card.html defs.svg style.css script.js <image>
"""
from __future__ import annotations

import argparse
import base64
import html.parser
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_DEFAULT = ROOT.parent / "wedding_invite_studio_fully_customizable.html"
TYPES = ["art", "images", "intros", "scenes", "borders", "patterns", "effects", "ornaments"]
ALWAYS = {"art", "images"}           # shared building blocks, included even with --only
ROLES = ["bg", "it", "ef", "cd", "ink", "ink2", "acc", "bl", "lv"]
SCOPE = {   # every CSS selector of a module must contain one of these (so modules never clash)
    "intros": ["ix-{id}", "s-{id}"], "scenes": ["sc-{id}", "scn-{id}"], "borders": ["bdx-{id}", "bd-{id}"],
    "patterns": ["ptx-{id}", "pt-{id}"], "ornaments": ["orx-{id}", "or-{id}"], "effects": ["fx-{id}"],
    "art": ["art-"], "images": ["bg-{id}"],
}
WRAP = {"intros": "ix", "scenes": "sc", "borders": "bdx", "patterns": "ptx", "ornaments": "orx"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
MIME = {".webp": "image/webp", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".avif": "image/avif",
        ".svg": "image/svg+xml"}

errors: list[str] = []
warnings: list[str] = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8-sig") if p.exists() else ""      # -sig: tolerate a BOM


def load_json(p: Path, default):
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as e:
        err(f"{p.relative_to(ROOT)}: invalid JSON (line {e.lineno}): {e.msg}")
        return default


class TagChecker(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.problems = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.problems.append(f"<{self.stack.pop()}> not closed")
            self.stack.pop()
        else:
            self.problems.append(f"stray </{tag}>")


def check_html(snippet: str, where: str):
    t = TagChecker()
    t.feed(snippet)
    t.close()
    probs = t.problems + [f"<{x}> not closed" for x in t.stack]
    for p in probs[:5]:
        err(f"{where}: {p}")


def strip_css_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def lint_css(css: str, mtype: str, mid: str, where: str):
    css = strip_css_comments(css)
    tokens = [s.format(id=mid) for s in SCOPE.get(mtype, [])]
    for name in re.findall(r"@keyframes\s+([\w-]+)", css):
        if not name.lower().startswith(mid.lower().replace("-", "")) and not name.lower().startswith(mid.lower()):
            warn(f"{where}: @keyframes '{name}' should start with '{mid}' to avoid clashes")
    # remove keyframes / font-face bodies, then look at selectors
    body = re.sub(r"@keyframes\s+[\w-]+\s*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", css)
    body = re.sub(r"@font-face\s*\{[^}]*\}", "", body)
    for sel, _ in re.findall(r"([^{}@]+)\{([^{}]*)\}", body):
        for s in sel.split(","):
            s = s.strip()
            if s and not any(tok in s for tok in tokens):
                warn(f"{where}: selector '{s[:70]}' is not scoped with {' or '.join('.' + t for t in tokens)}")


def gfont_family(param: str) -> str:
    return param.split(":")[0].replace("+", " ").strip()


def build(args) -> int:
    only = None
    if args.only:
        only = set()
        for part in args.only.split(","):
            part = part.strip()
            if part:
                only.add(part if ":" in part else part + ":*")

    head = read(ROOT / "base_head.html")
    tpl = read(ROOT / "template.html")
    core_css = read(ROOT / "core" / "core.css")
    core_js = read(ROOT / "core" / "core.js")
    if not head or not tpl or not core_js:
        err("missing base_head.html, template.html or core/core.js")
        return report()

    fonts = load_json(ROOT / "fonts.json", {"names": [], "text": [], "extra": []})
    palettes = load_json(ROOT / "palettes.json", {})
    samples = []
    for sp in (args.samples.split(";") if args.samples else [str(ROOT / "samples.json")]):
        sp = sp.strip()
        if sp:
            got = load_json(Path(sp), [])
            if not isinstance(got, list):
                err(f"{sp}: must be a JSON list of samples")
                got = []
            samples += got

    slots = {k: [] for k in ("STAGE_BACK", "INTROS", "SCENES", "CARD_BACK", "CARD_FRONT", "STAGE_FRONT", "DEFS")}
    css_parts, js_parts, vis = [], [], []
    reg = {"intros": [], "scenes": [], "borders": [], "patterns": [], "effects": [], "ornaments": [], "images": []}
    extra_fonts: list[str] = []
    all_ids: dict[str, str] = {}
    sizes = []

    for mtype in TYPES:
        tdir = ROOT / "modules" / mtype
        if not tdir.is_dir():
            continue
        mods = []
        for d in sorted(p for p in tdir.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))):
            meta = load_json(d / "meta.json", None)
            if meta is None:
                warn(f"modules/{mtype}/{d.name}: no meta.json - skipped")
                continue
            if meta.get("id", d.name) != d.name:
                err(f"modules/{mtype}/{d.name}: meta id '{meta.get('id')}' must equal the folder name")
                continue
            meta["id"] = d.name
            if meta.get("disabled"):
                continue
            if only is not None and mtype not in ALWAYS and f"{mtype}:{d.name}" not in only and f"{mtype}:*" not in only:
                continue
            mods.append((meta.get("order", 100), meta.get("name", d.name), d, meta))
        for _, _, d, meta in sorted(mods, key=lambda m: (m[0], m[1])):
            mid, where = meta["id"], f"modules/{mtype}/{meta['id']}"
            if not re.fullmatch(r"[a-z][a-z0-9-]*", mid):
                err(f"{where}: id must be lowercase letters, digits and dashes")
                continue
            # Snapshot so a broken shared module (art/images being edited by someone else) can be dropped
            # from a test build instead of failing it.
            snap = ({k: len(v) for k, v in slots.items()}, len(css_parts), len(js_parts), len(vis),
                    len(reg.get(mtype, [])), len(extra_fonts), set(all_ids), len(sizes), len(errors))
            process_module(mtype, d, meta, mid, where, args, slots, css_parts, js_parts, vis, reg, extra_fonts,
                           all_ids, sizes)
            if len(errors) > snap[8] and only is not None and mtype in ALWAYS:
                for k, n in snap[0].items():
                    del slots[k][n:]
                del css_parts[snap[1]:], js_parts[snap[2]:], vis[snap[3]:], extra_fonts[snap[5]:], sizes[snap[7]:]
                if mtype in reg:
                    del reg[mtype][snap[4]:]
                for k in set(all_ids) - snap[6]:
                    del all_ids[k]
                for e in errors[snap[8]:]:
                    warn(f"(skipped {mtype}:{mid} in this test build) {e}")
                del errors[snap[8]:]

    return finish(args, only, head, tpl, core_css, core_js, fonts, palettes, samples, slots, css_parts, js_parts, vis,
                  reg, extra_fonts, sizes)


def process_module(mtype, d, meta, mid, where, args, slots, css_parts, js_parts, vis, reg, extra_fonts, all_ids, sizes):
    if True:
            size = 0
            for part in ("stage", "card", "front"):
                snippet = read(d / f"{part}.html")
                if not snippet.strip():
                    continue
                size += len(snippet)
                check_html(snippet, f"{where}/{part}.html")
                for i in re.findall(r'\bid="([^"]+)"', snippet):
                    if i in all_ids:
                        err(f"{where}/{part}.html: id '{i}' is also used in {all_ids[i]} - prefix ids with '{mid}-'")
                    all_ids[i] = where
                w = WRAP.get(mtype)
                wrapped = f'<div class="{w} {w}-{mid}" data-mod="{mtype}:{mid}">\n{snippet.strip()}\n</div>' if w else snippet
                if mtype == "intros":
                    slots["INTROS"].append(wrapped)
                elif mtype == "scenes":
                    slots["SCENES"].append(wrapped)
                elif mtype == "patterns":
                    slots["STAGE_BACK" if part == "stage" else "CARD_BACK"].append(wrapped)
                elif mtype == "ornaments":
                    slots["STAGE_FRONT" if part == "stage" else ("CARD_FRONT" if part == "front" else "CARD_BACK")].append(wrapped)
                elif mtype == "borders":
                    slots["CARD_BACK"].append(wrapped)
                else:
                    warn(f"{where}: {part}.html is ignored for type {mtype}")
            defs = read(d / "defs.svg")
            if defs.strip():
                size += len(defs)
                check_html(defs, f"{where}/defs.svg")
                for i in re.findall(r'\bid="([^"]+)"', defs):
                    if i in all_ids:
                        err(f"{where}/defs.svg: id '{i}' is also used in {all_ids[i]}")
                    all_ids[i] = where
                slots["DEFS"].append(f"<!-- {mtype}:{mid} -->\n{defs.strip()}")
            css = read(d / "style.css")
            if css.strip():
                size += len(css)
                lint_css(css, mtype, mid, f"{where}/style.css")
                css_parts.append(f"/* ---- {mtype}:{mid} ---- */\n{css.strip()}")
            js = read(d / "script.js")
            if js.strip():
                size += len(js)
                if "</script" in js.lower():
                    err(f"{where}/script.js must not contain '</script'")
                js_parts.append(f"/* ---- {mtype}:{mid} ---- */\ntry {{\n{js.strip()}\n}} catch (e) {{ console.error('{mtype}:{mid}', e) }}")
            for f in meta.get("fonts", []):
                extra_fonts.append(f)
            entry = {"id": mid, "name": meta.get("name", mid)}
            if meta.get("desc"):
                entry["desc"] = meta["desc"]
            if mtype == "intros":
                if not isinstance(meta.get("t0"), (int, float)):
                    err(f"{where}: meta.t0 (seconds until the card appears) is required")
                entry["t0"] = float(meta.get("t0", 5))
                entry["defaults"] = meta.get("defaults", {})
                vis.append(f".s-{mid} .ix-{mid}")
            elif mtype == "scenes":
                if not isinstance(meta.get("dur"), (int, float)):
                    err(f"{where}: meta.dur (scene length in seconds) is required")
                entry["dur"] = float(meta.get("dur", 4))
                vis.append(f".scn-{mid} .sc-{mid}")
            elif mtype == "borders":
                vis.append(f".bd-{mid} .bdx-{mid}")
            elif mtype == "patterns":
                vis.append(f".pt-{mid} .ptx-{mid}")
            elif mtype == "ornaments":
                vis.append(f".or-{mid} .orx-{mid}")
            elif mtype == "images":
                f = d / meta.get("file", "image.webp")
                if not f.exists():
                    err(f"{where}: image file {f.name} missing")
                    return
                if args.no_images:
                    data_uri = None
                else:
                    raw = f.read_bytes()
                    size += len(raw)
                    data_uri = f"data:{MIME.get(f.suffix.lower(), 'image/webp')};base64,{base64.b64encode(raw).decode()}"
                if data_uri:
                    pos = meta.get("position", "center")
                    css_parts.append(f'/* ---- image:{mid} ({meta.get("credit", "")}) ---- */\n'
                                     f'.bg-{mid} .bgimg{{background-image:url("{data_uri}");background-position:{pos}}}')
                entry["credit"] = meta.get("credit", "")
            if mtype in reg:
                reg[mtype].append(entry)
            sizes.append((size, f"{mtype}:{mid}"))


def finish(args, only, head, tpl, core_css, core_js, fonts, palettes, samples, slots, css_parts, js_parts, vis, reg,
           extra_fonts, sizes):
    # ---------- fonts ----------
    seen, fam_params = {}, []
    for f in [x["g"] for x in fonts.get("names", []) + fonts.get("text", [])] + fonts.get("extra", []) + extra_fonts:
        fam = gfont_family(f)
        if fam in seen:
            if len(f) > len(fam_params[seen[fam]]):
                fam_params[seen[fam]] = f
            continue
        seen[fam] = len(fam_params)
        fam_params.append(f)
    fonts_url = "https://fonts.googleapis.com/css2?" + "&amp;".join("family=" + p for p in fam_params) + "&amp;display=swap"
    reg_fonts = {"names": [{"name": x["name"], "css": x["css"]} for x in fonts.get("names", [])],
                 "text": [{"name": x["name"], "css": x["css"]} for x in fonts.get("text", [])]}
    if not reg_fonts["names"] or not reg_fonts["text"]:
        err("fonts.json needs at least one 'names' and one 'text' font")

    # ---------- palettes ----------
    for k, p in palettes.items():
        missing = [r for r in ROLES if not re.fullmatch(r"#[0-9a-fA-F]{6}", str(p.get(r, "")))]
        if missing:
            err(f"palettes.json '{k}': missing/invalid roles {missing}")

    # ---------- samples ----------
    ids = {t: {e["id"] for e in reg[t]} for t in reg}
    ids["intros"] |= {"env", "door", "med"}
    ids["borders"] |= {"arch", "double", "single", "corner", "garland", "none"}
    ids["patterns"] |= {"dia", "dot", "none"}
    ids["effects"] |= {"petal", "dust", "none"}
    ids["images"] |= {"none"}
    fn_css = {x["css"] for x in reg_fonts["names"]}
    ft_css = {x["css"] for x in reg_fonts["text"]}
    allowed = {"sStyle": ("intros", None), "sBorder": ("borders", None), "sPat": ("patterns", None),
               "sFall": ("effects", None), "sImg": ("images", None)}
    ok_samples = []
    for n, smp in enumerate(samples, 1):
        where = f"samples.json #{n} '{smp.get('name', '?')}'"
        problems, missing_mod = [], False
        for k, val in (smp.get("set") or {}).items():
            if k in allowed:
                t = allowed[k][0]
                if val not in ids[t]:
                    if only is not None:
                        missing_mod = True
                    problems.append(f"{k}='{val}' is not a known {t[:-1]}")
            elif k == "sImgOn":
                if val not in ("stg", "crd", "both"):
                    problems.append("sImgOn must be stg, crd or both")
            elif k == "rImg":
                if not isinstance(val, (int, float)) or not 10 <= val <= 100:
                    problems.append("rImg must be a number 10-100")
            elif k == "sName":
                if val not in ("letter", "slide", "hand", "fade"):
                    problems.append("sName must be letter/slide/hand/fade")
            elif k == "sDet":
                if val not in ("wipe", "up", "slide"):
                    problems.append("sDet must be wipe/up/slide")
            elif k == "sFs":
                if val not in fn_css:
                    problems.append(f"sFs {val} is not in fonts.json names")
            elif k == "sFt":
                if val not in ft_css:
                    problems.append(f"sFt {val} is not in fonts.json text")
            elif k in ("kFdi", "kFdo", "kLan", "kSpk"):
                if not isinstance(val, bool):
                    problems.append(f"{k} must be true/false")
            elif k.startswith("kO_"):
                if k[3:] not in ids["ornaments"]:
                    if only is not None:
                        missing_mod = True
                    problems.append(f"{k}: no ornament '{k[3:]}'")
            elif k.startswith("kSc_"):
                if k[4:] not in ids["scenes"]:
                    if only is not None:
                        missing_mod = True
                    problems.append(f"{k}: no scene '{k[4:]}'")
            else:
                problems.append(f"unknown setting '{k}'")
        for ev in ("baraat", "walima"):
            p = (smp.get("pal") or {}).get(ev)
            if not p:
                problems.append(f"pal.{ev} missing")
                continue
            bad = [r for r in ROLES if not re.fullmatch(r"#[0-9a-fA-F]{6}", str(p.get(r, "")))]
            if bad:
                problems.append(f"pal.{ev} missing/invalid {bad}")
        if missing_mod:
            continue          # test build without that module: silently leave the sample out
        for p in problems:
            err(f"{where}: {p}")
        ok_samples.append({k: smp[k] for k in ("name", "desc", "cat", "set", "pal") if k in smp})

    # ---------- assemble ----------
    vis_css = (",".join(vis) + "{display:block}") if vis else ""
    module_css = "\n".join(([f"/* ---- module visibility ---- */\n{vis_css}"] if vis_css else []) + css_parts)
    registry = {"intros": reg["intros"], "scenes": reg["scenes"], "borders": reg["borders"], "patterns": reg["patterns"],
                "effects": reg["effects"], "ornaments": reg["ornaments"], "images": reg["images"],
                "fonts": reg_fonts, "palettes": palettes, "samples": ok_samples}
    reg_js = ("window.WIS = {reg: " + json.dumps(registry, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
              + ", ix: {}, sc: {}, orn: {}, bd: {}, pt: {}, fx: {}};")
    out = tpl
    rep = {
        "@FONTS_URL@": fonts_url,
        "/*@CORE_CSS@*/": core_css.strip(),
        "/*@MODULE_CSS@*/": module_css,
        "<!--@DEFS@-->": "\n".join(slots["DEFS"]),
        "<!--@STAGE_BACK@-->": "\n".join(slots["STAGE_BACK"]),
        "<!--@INTROS@-->": "\n".join(slots["INTROS"] + slots["SCENES"]),
        "<!--@CARD_BACK@-->": "\n".join(slots["CARD_BACK"]),
        "<!--@CARD_FRONT@-->": "\n".join(slots["CARD_FRONT"]),
        "<!--@STAGE_FRONT@-->": "\n".join(slots["STAGE_FRONT"]),
        "/*@REGISTRY@*/": reg_js,
        "/*@MODULE_JS@*/": "\n".join(js_parts),
        "/*@CORE_JS@*/": core_js.strip(),
    }
    for k, val in rep.items():
        if k not in out:
            err(f"template.html is missing the placeholder {k}")
        out = out.replace(k, val)
    page = head + out
    if "</style" in module_css.lower():
        err("a module style.css contains '</style'")

    stats = (f"{len(reg['intros'])} intros, {len(reg['scenes'])} scenes, {len(reg['borders'])} borders, "
             f"{len(reg['patterns'])} patterns, {len(reg['effects'])} effects, {len(reg['ornaments'])} ornaments, "
             f"{len(reg['images'])} images, {len(ok_samples)} samples")
    if args.verbose:
        for s, name in sorted(sizes, reverse=True)[:15]:
            print(f"  {s / 1024:8.1f} KB  {name}")
    code = report()
    if code:
        return code
    if args.check:
        print(f"OK ({stats}) - not written (--check)")
        return 0
    dest = Path(args.out).resolve() if args.out else OUT_DEFAULT
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".tmp")
    tmp.write_text(page, encoding="utf-8")
    os.replace(tmp, dest)
    print(f"Built {dest}  ({len(page.encode('utf-8')) / 1e6:.2f} MB; {stats})")
    return 0


def report() -> int:
    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("ERROR:", e)
    return 1 if errors else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build the Wedding Invite Studio HTML")
    ap.add_argument("--out", help="output file (default: ../wedding_invite_studio_fully_customizable.html)")
    ap.add_argument("--only", help="comma list of type:id (or type:*) to include; art and images are always included")
    ap.add_argument("--no-images", action="store_true", help="leave photos out (faster test builds)")
    ap.add_argument("--samples", help="sample list file(s) to use instead of samples.json (separate several with ;)")
    ap.add_argument("--check", action="store_true", help="validate only")
    ap.add_argument("-v", "--verbose", action="store_true", help="list the biggest modules")
    sys.exit(build(ap.parse_args()))
