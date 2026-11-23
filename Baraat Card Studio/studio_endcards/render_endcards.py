"""
render_endcards.py - still image of the FINISHED card (last frame of the animation) for every
sample in the wedding invite studio, filled in with one client's details.

    python render_endcards.py                 all samples
    python render_endcards.py 1 5 12          only these sample numbers
    python render_endcards.py --sheets-only   just rebuild the contact sheets from existing PNGs
    python render_endcards.py --particles     keep falling petals / gold dust in the stills
    python render_endcards.py 54 --set kSpk=false --out variants/no_sparkles
                                              override any studio control (by element id) after the sample
    python render_endcards.py 25 66 --closing "" --venue "Noor Mahal Marquee, Islamabad" --out variants/short
                                              alternative text settings, written to another folder

Output (next to this script, or in --out):
    "<NN> <Sample Name>.png"   1080x1920 end card for each sample
    endcards.json              [{index, name, cat, file, hash}] - open the studio with
                               "wedding_invite_studio_fully_customizable.html<hash>" to edit that design
                               with the client's details already filled in
    _sheet_1.jpg ...           contact sheets (4 rows x 6)

How the end state is captured: the studio's own controls are set exactly like a person would
(sample picker, Event = Baraat, text fields), fonts/images are loaded, the animation is restarted
(.play), then every Web Animation on the page is paused and seeked to 0.6 s after the last finite
animation ends (the same technique html2mp4.py uses). The fade-to-black overlay is excluded and
hidden; falling particles (petals / dust frozen mid-air) are hidden too
(pass --particles to keep them).
"""
from __future__ import annotations

import base64
import json
import math
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE                                 # changed by --out
STUDIO = Path(r"F:\Wedding Card\wedding_invite_studio_fully_customizable.html")
SAMPLES = json.loads((Path(r"F:\Wedding Card\studio\samples.json")).read_text(encoding="utf-8"))

# ---- client details (Baraat) -------------------------------------------------------------
CLIENT = {
    "inE": "baraat",
    # Groom's-family Baraat card: the groom's name must come first. The studio always prints the
    # "bride" field first and has no name-order option, so the two fields are deliberately swapped
    # (monograms then read "A & L"). The end card has no "Bride"/"Groom" labels (checked per card).
    "inB": "Abdul Aleem",           # studio's bride field  = printed first
    "inG": "Laiba",                 # studio's groom field  = printed second
    "in_date": "Thursday, 31st December 2026",
    "in_time": "2:00 PM",
    "in_venue": "Noor Mahal Marquee, G.T Road, Islamabad",
    # closing line: studio default kept ("Aap ki shirkat hamare liye baais-e-musarrat hogi")
    "inBism": True,
}
# The studio's built-in Walima defaults (kept so the saved state is complete if someone switches event).
WALIMA_D = {"date": "Sunday, 13 December 2026", "time": "8:00 PM onwards", "venue": "Rose Garden Marquee, Lahore"}

CSS_W, CSS_H, SCALE = 360, 640, 3          # 360x640 CSS px x3 = 1080x1920
HOLD_MS = 600                              # how far past the last finite animation to freeze
SEED = 7

JS_INIT = r"""
(() => {
  let seed = %SEED% >>> 0;
  Math.random = function () {
    seed = (seed + 0x6D2B79F5) >>> 0;
    let t = seed;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
})();
"""

# Studio's own recording layout (html.recording -> stage fills the viewport, square corners);
# everything else on the page is hidden so only the 9:16 stage is rendered.
JS_SETUP = r"""
(noParticles) => {
  document.documentElement.classList.add('recording');
  const css = document.createElement('style');
  css.id = 'endcard-css';
  css.textContent = 'html,body{margin:0!important;overflow:hidden!important;background:#000!important}' +
    '#gal,.btns,.hint,.ctl,.chead,.evsw,.snav,.toast,dialog,.recmsg{display:none!important}' +
    '#st .fo{display:none!important}' + (noParticles ? '#st .fall{display:none!important}' : '');
  document.head.appendChild(css);
  return document.getElementById('st').getBoundingClientRect().toJSON();
}
"""

# Set controls like a person would (value + input/change events).
JS_SET = r"""
(values) => {
  for (const [id, v] of Object.entries(values)) {
    const el = document.getElementById(id);
    if (!el) continue;
    if (el.type === 'checkbox') el.checked = !!v; else el.value = String(v);
    el.dispatchEvent(new Event('input', {bubbles: true}));
    el.dispatchEvent(new Event('change', {bubbles: true}));
  }
}
"""

# Load the fonts actually used by visible text on the stage (and any background images).
JS_LOAD = r"""
async () => {
  const st = document.getElementById('st');
  const jobs = new Map();
  for (const el of [st, ...st.querySelectorAll('*')]) {
    if (!el.getClientRects || !el.getClientRects().length) continue;
    let text = '';
    for (const n of el.childNodes) if (n.nodeType === 3) text += n.nodeValue;
    text = text.replace(/\s+/g, ' ').trim();
    if (!text) continue;
    const cs = getComputedStyle(el);
    const key = cs.fontStyle + ' ' + cs.fontWeight + ' 40px ' + cs.fontFamily;
    jobs.set(key, (jobs.get(key) || '') + text);
  }
  await Promise.all([...jobs].map(([f, t]) => document.fonts.load(f, t.slice(0, 2000)).catch(() => null)));
  await document.fonts.ready;
  const urls = new Set();
  for (const el of st.querySelectorAll('*')) {
    const v = getComputedStyle(el).backgroundImage;
    if (v && v !== 'none') for (const m of v.matchAll(/url\(\s*(['"]?)(.*?)\1\s*\)/g)) urls.add(m[2]);
  }
  await Promise.all([...urls].map(u => new Promise(res => {const i = new Image(); i.onload = i.onerror = res; i.src = u;})));
  return {failed: [...new Set([...document.fonts].filter(f => f.status === 'error').map(f => f.family))]};
}
"""

# Restart the animation, freeze everything and seek to the finished card.
JS_FINISH = r"""
(hold) => {
  const st = document.getElementById('st');
  // Drop the previous sample's paused animations (Chrome keeps API-paused CSS animations alive on
  // elements that became hidden), then let every animation be created fresh, as on a newly loaded page.
  document.getAnimations().forEach(a => a.cancel());
  const k = document.createElement('style');
  k.textContent = '#st,#st *,#st *::before,#st *::after{animation:none!important}';
  document.head.appendChild(k);
  st.classList.remove('play'); void st.offsetWidth; getComputedStyle(st).opacity;
  k.remove(); void st.offsetWidth;
  st.classList.add('play');
  const anims = document.getAnimations();
  anims.forEach(a => a.pause());
  let end = 0, infinite = 0;
  for (const a of anims) {
    const tg = a.effect && a.effect.target;
    if (tg && tg.classList && tg.classList.contains('fo')) continue;        // fade-out to black
    const t = a.effect && a.effect.getComputedTiming ? a.effect.getComputedTiming() : null;
    if (!t) continue;
    if (!isFinite(t.endTime)) { infinite++; continue; }
    if (t.endTime > end) end = t.endTime;
  }
  const at = end + hold;
  anims.forEach(a => { try { a.currentTime = at; } catch (e) {} });
  return {count: anims.length, infinite, end: end / 1000, at: at / 1000};
}
"""

# Anything in the card's text column that is not fully visible after seeking = a problem.
JS_CHECK = r"""
() => {
  const st = document.getElementById('st'), sr = st.getBoundingClientRect();
  const op = el => { let o = 1; for (let n = el; n && n !== st.parentElement; n = n.parentElement) {
      const cs = getComputedStyle(n); if (cs.display === 'none' || cs.visibility === 'hidden') return 0; o *= parseFloat(cs.opacity); } return o; };
  const out = [];
  for (const id of ['bism', 'bn', 'gn', 'ev', 'dt', 'tm', 'vn', 'cl']) {
    const el = document.getElementById(id);
    if (!el || getComputedStyle(el).display === 'none' || !el.textContent.trim()) continue;   // empty = left blank on purpose
    const o = op(el), r = el.getBoundingClientRect();
    let letters = 1;
    const ls = el.querySelectorAll('.l');
    if (ls.length) letters = Math.min(...[...ls].map(op));
    const off = r.width < 1 || r.bottom < sr.top || r.top > sr.bottom || r.right < sr.left || r.left > sr.right;
    if (o < 0.97 || letters < 0.97 || off) out.push(id + (off ? '(offstage)' : '') + '=' + Math.min(o, letters).toFixed(2));
  }
  // twinkling sparkles (.sp) must not sit on any text line
  const pad = 2, hit = (a, b) => a.left - pad < b.right && a.right + pad > b.left && a.top - pad < b.bottom && a.bottom + pad > b.top;
  for (const sp of st.querySelectorAll('.sp')) {
    if (op(sp) < 0.05) continue;
    const r = sp.getBoundingClientRect(); if (r.width < 1) continue;
    for (const id of ['bism', 'bn', 'gn', 'ev', 'dt', 'tm', 'vn', 'cl']) {
      const el = document.getElementById(id); if (!el || !el.textContent.trim()) continue;
      const rg = document.createRange(); rg.selectNodeContents(el);
      if ([...rg.getClientRects()].some(t => hit(r, t))) { out.push('sparkle on ' + id); break; }
    }
  }
  // the card itself must be normal by now
  const card = st.querySelector('.card'), co = card ? op(card) : 0;
  if (co < 0.97) out.push('card=' + co.toFixed(2));
  return out;
}
"""

# Role labels ("Bride", "Dulhan"...) that are not hidden: candidates for the pixel test below.
JS_LABELS = r"""
() => {
  const st = document.getElementById('st'), rx = /\b(bride|groom|dulhan?|dulha)\b/i, out = [];
  const op = el => { let o = 1; for (let n = el; n && n !== st.parentElement; n = n.parentElement) {
      const cs = getComputedStyle(n); if (cs.display === 'none' || cs.visibility === 'hidden') return 0; o *= parseFloat(cs.opacity); } return o; };
  st.querySelectorAll('[data-lbl]').forEach(e => e.removeAttribute('data-lbl'));
  for (const el of st.querySelectorAll('*')) {
    let t = ''; for (const n of el.childNodes) if (n.nodeType === 3) t += n.nodeValue;
    if (!rx.test(t)) continue;
    const r = el.getBoundingClientRect();
    const x = Math.max(0, r.left), y = Math.max(0, r.top), w = Math.min(r.right, innerWidth) - x, h = Math.min(r.bottom, innerHeight) - y;
    if (w < 1 || h < 1 || op(el) < 0.02) continue;
    el.setAttribute('data-lbl', out.length);
    out.push({text: t.trim(), x, y, w, h});
  }
  return out;
}
"""


def visible_labels(page):
    """Labels whose pixels actually show in the frame (hiding them changes the screenshot)."""
    found = []
    for i, c in enumerate(page.evaluate(JS_LABELS)):
        clip = {"x": c["x"], "y": c["y"], "width": c["w"], "height": c["h"]}
        before = page.screenshot(clip=clip)
        page.evaluate("i => document.querySelector('[data-lbl=\"' + i + '\"]').style.visibility = 'hidden'", i)
        after = page.screenshot(clip=clip)
        page.evaluate("i => document.querySelector('[data-lbl=\"' + i + '\"]').style.visibility = ''", i)
        if before != after:
            found.append('label "' + c["text"] + '"')
    return found


# The studio's snapshot() structure, for the "#sample-N&s=..." hash restore.
JS_SNAPSHOT = r"""
([n, D]) => {
  const ctrls = {};
  document.querySelectorAll('#ctl input, #ctl select, #ctl textarea').forEach(el => {
    if (!el.id) return; ctrls[el.id] = el.type === 'checkbox' ? el.checked : el.value; });
  const smp = window.WIS.reg.samples[n - 1];
  const esp = {name: 'Espresso and gold', bg: '#3B2A20', it: '#F3E6CC', ef: '#F4EAD8', cd: '#FBF4E6', ink: '#2E2018', ink2: '#7A5A24', acc: '#B8913F', bl: '#9E3B3B', lv: '#5E6B3A'};
  const tau = {name: 'Taupe and rose gold', bg: '#6F5E52', it: '#FBF3E8', ef: '#FAF3EA', cd: '#FFFAF3', ink: '#3A2C25', ink2: '#8A5E4A', acc: '#A97C5F', bl: '#C27C80', lv: '#7D8B6A'};
  const pal = ev => Object.assign({}, ev === 'walima' ? tau : esp, (smp.pal && (smp.pal[ev] || smp.pal.baraat)) || {});
  return {sample: n, custom: false, cur: 'baraat', C: {baraat: pal('baraat'), walima: pal('walima')}, D, ctrls};
}
"""


def safe(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]+', "", name).strip()


def b64url(obj) -> str:
    raw = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def file_for(i: int) -> str:
    return f"{i:02d} {safe(SAMPLES[i - 1]['name'])}.png"


EXTRA = {}                                 # --set ID=VALUE design overrides applied after each sample


def render(indices: list[int], no_particles: bool):
    D = {"baraat": {"date": CLIENT["in_date"], "time": CLIENT["in_time"], "venue": CLIENT["in_venue"]},
         "walima": WALIMA_D}
    meta_path = OUT / "endcards.json"
    meta = {m["index"]: m for m in json.loads(meta_path.read_text(encoding="utf-8"))} if meta_path.exists() else {}
    problems = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--force-color-profile=srgb", "--disable-lcd-text",
                                          "--font-render-hinting=none", "--hide-scrollbars", "--mute-audio"])
        ctx = browser.new_context(viewport={"width": CSS_W, "height": CSS_H}, device_scale_factor=SCALE,
                                  reduced_motion="no-preference", color_scheme="light")
        ctx.add_init_script(JS_INIT.replace("%SEED%", str(SEED)))
        page = ctx.new_page()
        page.on("pageerror", lambda e: print("  page error:", e))
        page.goto(STUDIO.as_uri(), wait_until="load", timeout=120_000)
        box = page.evaluate(JS_SETUP, no_particles)
        print(f"stage {box['width']:.0f}x{box['height']:.0f} CSS px -> {box['width']*SCALE:.0f}x{box['height']*SCALE:.0f}")
        # event first (it refills date/time/venue from its defaults), then the text fields
        page.evaluate(JS_SET, {"inE": CLIENT["inE"]})
        page.evaluate(JS_SET, {k: v for k, v in CLIENT.items() if k != "inE"})
        for n in indices:
            smp = SAMPLES[n - 1]
            page.evaluate(JS_SET, {"sSample": str(n)})             # = applySample(n): design + palette, keeps text
            if EXTRA:
                page.evaluate(JS_SET, EXTRA)
            # make sure nothing reset the client's text / event
            page.evaluate("""(c) => { const bad = Object.entries(c).filter(([k, v]) => { const el = document.getElementById(k);
                               return el && (el.type === 'checkbox' ? el.checked !== v : el.value !== String(v)); });
                               if (bad.length) throw new Error('fields changed: ' + bad.map(b => b[0]).join(',')); }""", CLIENT)
            loaded = page.evaluate(JS_LOAD)
            page.wait_for_timeout(250)                               # studio re-fits handwriting text on font load
            page.evaluate(JS_LOAD)                                   # fonts of text that appeared after the first load
            tl = page.evaluate(JS_FINISH, HOLD_MS)
            page.evaluate("() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")
            issues = page.evaluate(JS_CHECK) + visible_labels(page)
            if loaded["failed"]:
                issues.append("fonts failed: " + ", ".join(loaded["failed"]))
            out = OUT / file_for(n)
            page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": CSS_W, "height": CSS_H})
            snap = page.evaluate(JS_SNAPSHOT, [n, D])
            meta[n] = {"index": n, "name": smp["name"], "cat": smp.get("cat", ""), "file": out.name,
                       "hash": f"#sample-{n}&s={b64url(snap)}"}
            if issues:
                problems[n] = issues
            print(f"{n:02d} {smp['name']:<32} end {tl['end']:5.2f}s  anims {tl['count']:3d} ({tl['infinite']} loop)"
                  + (f"  ISSUES: {issues}" if issues else ""), flush=True)
        browser.close()
    meta_path.write_text(json.dumps([meta[k] for k in sorted(meta)], ensure_ascii=False, indent=1), encoding="utf-8")
    return problems


def sheets(cols=6, rows=4, tile_w=300):
    from PIL import Image, ImageDraw, ImageFont
    files = sorted(OUT.glob("[0-9][0-9] *.png"))
    th = round(tile_w * 16 / 9)
    lab, gap = 34, 10
    try:
        font = ImageFont.truetype("arialbd.ttf", 19)
    except Exception:
        font = ImageFont.load_default()
    per = cols * rows
    for old in OUT.glob("_sheet_*.jpg"):
        old.unlink()
    made = []
    for s in range(math.ceil(len(files) / per)):
        chunk = files[s * per:(s + 1) * per]
        r = math.ceil(len(chunk) / cols)
        sheet = Image.new("RGB", (cols * tile_w + (cols + 1) * gap, r * (th + lab) + (r + 1) * gap), (28, 28, 28))
        d = ImageDraw.Draw(sheet)
        for i, f in enumerate(chunk):
            x = gap + (i % cols) * (tile_w + gap)
            y = gap + (i // cols) * (th + lab + gap)
            label = f.stem
            while d.textlength(label, font=font) > tile_w - 4 and len(label) > 4:
                label = label[:-2] + "…" if not label.endswith("…") else label[:-2] + "…"
            d.text((x + 2, y + 6), label, fill=(240, 228, 200), font=font)
            sheet.paste(Image.open(f).convert("RGB").resize((tile_w, th), Image.LANCZOS), (x, y + lab))
        dest = OUT / f"_sheet_{s + 1}.jpg"
        sheet.save(dest, quality=90)
        made.append(dest)
    return made


def take(argv, flag):
    """Remove '--flag VALUE' from argv and return VALUE (None if absent)."""
    if flag not in argv:
        return None
    i = argv.index(flag)
    val = argv[i + 1]
    del argv[i:i + 2]
    return val


def main(argv):
    global OUT
    argv = list(argv)
    closing, venue, out = take(argv, "--closing"), take(argv, "--venue"), take(argv, "--out")
    while "--set" in argv:                     # e.g. --set kSpk=false  (studio control id = value)
        k, _, v = take(argv, "--set").partition("=")
        EXTRA[k] = {"true": True, "false": False}.get(v.lower(), v)
    if closing is not None:
        CLIENT["inC"] = closing
    if venue is not None:
        CLIENT["in_venue"] = venue
    if out:
        OUT = (HERE / out).resolve()
        OUT.mkdir(parents=True, exist_ok=True)
    no_particles = "--particles" not in argv     # frozen petals over the text look messy in a still
    if "--sheets-only" not in argv:
        nums = [int(a) for a in argv if a.isdigit()]
        indices = nums or list(range(1, len(SAMPLES) + 1))
        problems = render(indices, no_particles)
        print(f"\n{len(indices)} cards rendered; {len(problems)} with issues")
        for n, iss in problems.items():
            print(f"  {n:02d} {SAMPLES[n - 1]['name']}: {iss}")
    for s in sheets():
        print("sheet:", s)


if __name__ == "__main__":
    main(sys.argv[1:])
