#!/usr/bin/env python3
"""
html2mp4.py - turn an animated HTML page (like the wedding invites in this folder)
into a super-high-quality MP4 video.

How it works
------------
The page is opened in headless Chromium. Every CSS / Web animation is paused and the
timeline is stepped exactly one frame at a time, so nothing stutters or drops no matter
how slow the PC is. Each frame is captured as a lossless PNG at the final resolution
(text and lines are drawn natively at 1080x1920, 1440x2560 or 4K - never upscaled) and
piped straight into ffmpeg.

Quick start
-----------
  python html2mp4.py                       menu: pick a file, set options, render
  python html2mp4.py design  card.html     open the card in a browser window, set every
                                           option visually, press Enter -> video
  python html2mp4.py scan    card.html     list every option the page has and write
                                           card.config.json (edit the "value" fields)
  python html2mp4.py render  card.html     render, using card.config.json if present

Render / design options (all optional)
--------------------------------------
  --set "Opening animation=Palace doors"   change any page option, by label or id
  --set inB=Sara --set "Show Bismillah=no"
  --quality high|whatsapp|ultra|4k|prores  (default high = 1080x1920, 60 fps)
  --width 1080 --height 1920 --fps 60 --crf 14 --codec h264|h265|prores
  --hold 4            seconds to keep the finished card on screen at the end
  --duration 15       exact video length (overrides the automatic length)
  --audio song.mp3 --audio-start 12 --audio-volume 0.8
  --out my_video.mp4
  --workers 3         browser tabs rendering in parallel (default: auto)

A different --height than the card's 9:16 shape (e.g. --width 1920 --height 1080)
centres the card on a background colour (--background "#1b130e").

Requirements: pip install playwright ; python -m playwright install chromium ; ffmpeg
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import json
import math
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    sys.exit("Playwright is not installed. Run:\n"
             "  pip install playwright\n"
             "  python -m playwright install chromium")

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = Path(__file__).resolve().parent

PRESETS = {
    "high":     {"width": 1080, "fps": 60, "crf": 14, "codec": "h264", "preset": "slow"},
    "whatsapp": {"width": 1080, "fps": 30, "crf": 20, "codec": "h264", "preset": "slow"},
    "ultra":    {"width": 1440, "fps": 60, "crf": 12, "codec": "h264", "preset": "slow"},
    "4k":       {"width": 2160, "fps": 60, "crf": 12, "codec": "h264", "preset": "slow"},
    "prores":   {"width": 1080, "fps": 60, "crf": None, "codec": "prores", "preset": None},
}
PRESET_INFO = {
    "high":     "High     - 1080x1920, 60 fps, H.264. Crisp, plays everywhere (recommended)",
    "whatsapp": "WhatsApp - 1080x1920, 30 fps, smaller file for WhatsApp / Instagram",
    "ultra":    "Ultra    - 1440x2560, 60 fps. Extra sharp",
    "4k":       "4K       - 2160x3840, 60 fps. Maximum detail (slowest)",
    "prores":   "ProRes   - 1080x1920, 60 fps, ProRes 4444 .mov for video editors (huge file)",
}
VIDEO_DEFAULTS = {
    "quality": "high", "width": None, "height": None, "fps": None, "crf": None,
    "codec": None, "preset": None,
    "hold": 4.0, "duration": None, "start": 0.0,
    "audio": None, "audio_start": 0.0, "audio_volume": 1.0,
    "corners": "auto", "background": None, "poster": True,
    "workers": 0, "gpu": True, "seed": 7, "out": None,
}
PAGE_DEFAULTS = {"stage": None, "replay": None, "virtual_time": False, "design_width": 360}
LAUNCH_ARGS = ["--force-color-profile=srgb", "--disable-lcd-text", "--font-render-hinting=none",
               "--mute-audio"]
# GPU rasterisation (what desktop Chrome normally uses) renders frames ~2x faster.
GPU_ARGS = ["--enable-gpu", "--enable-gpu-rasterization", "--ignore-gpu-blocklist"] + \
           (["--use-angle=d3d11"] if sys.platform == "win32" else [])
SETTLE_MS = 1500   # let the page finish any work triggered by applying options


class UserError(Exception):
    pass


# --------------------------------------------------------------------------- page scripts

# Runs before the page's own scripts: deterministic Math.random (identical falling
# petals in every render and every parallel tab) plus a helper that builds a selector.
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
  window.__h2mPath = (el) => {
    const parts = [];
    for (; el && el.nodeType === 1; el = el.parentElement) {
      if (el.id) { parts.unshift('#' + CSS.escape(el.id)); break; }
      if (el === document.body) { parts.unshift('body'); break; }
      let i = 1;
      for (let s = el.previousElementSibling; s; s = s.previousElementSibling) i++;
      parts.unshift(el.tagName.toLowerCase() + ':nth-child(' + i + ')');
    }
    return parts.join(' > ');
  };
})();
"""

# Every form control on the page = every option the card offers.
JS_SCAN = r"""
() => {
  const heads = [...document.querySelectorAll('.grp, legend, h3, h4, h5, h6, [class*="group-title"], [class*="section-title"]')]
    .filter(h => !h.closest('.sr-only') && h.textContent.trim() && !h.querySelector('input, select, textarea'));
  const out = [], seen = new Set();
  for (const el of document.querySelectorAll('input, select, textarea')) {
    if (el.closest('dialog, [data-h2m-ignore]')) continue;
    const type = el.tagName === 'SELECT' ? 'select' : el.tagName === 'TEXTAREA' ? 'text'
               : (el.getAttribute('type') || 'text').toLowerCase();
    if (/^(button|submit|reset|file|hidden|image|password)$/.test(type)) continue;
    const key = el.id || el.name;
    if (!key || seen.has(key)) continue;
    seen.add(key);
    let label = '';
    const lab = (el.labels && el.labels[0]) || el.closest('label');
    if (lab) {
      const c = lab.cloneNode(true);
      c.querySelectorAll('input, select, textarea, button').forEach(n => n.remove());
      label = c.textContent.replace(/\s+/g, ' ').trim();
    }
    label = label || el.getAttribute('aria-label') || el.placeholder || el.title || key;
    let group = '';
    for (const h of heads) if (h.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING) group = h.textContent.replace(/\s+/g, ' ').trim();
    const it = { key, type, label, group };
    if (type === 'select') {
      it.value = el.value;
      it.choices = [...el.options].map(o => [o.value, o.textContent.replace(/\s+/g, ' ').trim()]);
    } else if (type === 'checkbox' || type === 'radio') {
      it.value = el.checked;
    } else if (type === 'range' || type === 'number') {
      it.value = el.value === '' ? null : Number(el.value);
    } else {
      it.value = el.value;
    }
    out.push(it);
  }
  return out;
}
"""

# Set controls exactly like a person would (value + input/change events), in page order,
# repeating until stable so options that reset other options still end up as requested.
JS_APPLY = r"""
(values) => {
  const has = el => Object.prototype.hasOwnProperty.call(values, el.id || el.name);
  const want = el => values[el.id || el.name];
  const same = (el, v) => {
    if (el.type === 'checkbox' || el.type === 'radio') return el.checked === !!v;
    if (el.type === 'color') return el.value.toLowerCase() === String(v).toLowerCase();
    return el.value === String(v);
  };
  const fire = el => {
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
  };
  for (let pass = 0; pass < 4; pass++) {
    let changed = 0;
    for (const el of document.querySelectorAll('input, select, textarea')) {
      if (!has(el) || want(el) === null || same(el, want(el))) continue;
      if (el.type === 'checkbox' || el.type === 'radio') el.checked = !!want(el);
      else el.value = String(want(el));
      fire(el);
      changed++;
    }
    if (!changed) break;
  }
  return [...document.querySelectorAll('input, select, textarea')]
    .filter(el => has(el) && want(el) !== null && !same(el, want(el)))
    .map(el => el.id || el.name);
}
"""

# Load exactly the fonts and images the card uses (every rendered text element's font, CSS background
# photos, <img> and SVG <image>), so nothing pops in mid-video and unused font families are not fetched.
JS_LOAD_ASSETS = r"""
async (sel) => {
  const root = (sel && document.querySelector(sel)) || null;
  const scope = root || document.body;
  const els = [scope, ...scope.querySelectorAll('*')];
  const jobs = new Map();
  for (const el of els) {
    if (!el.getClientRects || !el.getClientRects().length) continue;
    let text = '';
    for (const n of el.childNodes) if (n.nodeType === 3) text += n.nodeValue;
    text = text.replace(/\s+/g, ' ').trim();
    if (!text) continue;
    const cs = getComputedStyle(el);
    const key = cs.fontStyle + ' ' + cs.fontWeight + ' 40px ' + cs.fontFamily;
    jobs.set(key, (jobs.get(key) || '') + text);
  }
  const tasks = [...jobs].map(([font, text]) => document.fonts.load(font, text.slice(0, 2000)).catch(() => null));
  if (!root) tasks.push(...[...document.fonts].map(f => f.load().catch(() => null)));
  await Promise.all(tasks);
  await document.fonts.ready;
  const urls = new Set();
  for (const el of els) {
    const cs = getComputedStyle(el);
    for (const prop of ['backgroundImage', 'maskImage', 'webkitMaskImage', 'borderImageSource']) {
      const v = cs[prop];
      if (!v || v === 'none') continue;
      for (const m of v.matchAll(/url\(\s*(['"]?)(.*?)\1\s*\)/g)) urls.add(m[2]);
    }
    if (el.tagName && el.tagName.toLowerCase() === 'image' && el.href && el.href.baseVal) urls.add(el.href.baseVal);
  }
  await Promise.all([...urls].map(u => new Promise(res => {
    const i = new Image();
    i.onload = i.onerror = () => res();
    i.src = u;
    if (i.decode) i.decode().then(res, res);
  })));
  await Promise.all([...document.images].map(i => (i.complete && i.naturalWidth) || !i.decode ? null : i.decode().catch(() => null)));
  const faces = [...document.fonts];
  return {
    total: faces.length, jobs: jobs.size, images: urls.size,
    failedFonts: [...new Set(faces.filter(f => f.status === 'error').map(f => f.family.replace(/["']/g, '')))],
    failedSheets: [...document.querySelectorAll('link[rel="stylesheet"]')].filter(l => !l.sheet).map(l => l.href),
  };
}
"""

JS_FIND_STAGE = r"""
(sel) => {
  let el = null;
  if (sel) {
    el = document.querySelector(sel);
    if (!el) return { error: 'The stage selector "' + sel + '" matches nothing on the page.' };
  } else {
    let best = -1;
    for (const e of document.body.querySelectorAll('*')) {
      const r = e.getBoundingClientRect(), area = r.width * r.height;
      if (area < 20000) continue;
      const cs = getComputedStyle(e);
      if (cs.display === 'none' || cs.visibility === 'hidden') continue;
      const name = (e.id || '') + ' ' + (typeof e.className === 'string' ? e.className : '');
      let score = 0;
      if (e.getAttribute('role') === 'img') score += 3;
      if (cs.aspectRatio && cs.aspectRatio !== 'auto') score += 2;
      if (/^(CANVAS|VIDEO)$/.test(e.tagName)) score += 2;
      if (/stage|invite|card|poster|scene/i.test(name)) score += 1;
      if (!score) continue;
      score += area / 1e8;
      if (score > best) { best = score; el = e; }
    }
    if (!el) return { error: 'Could not find the animated card on the page. Add "page": {"stage": "#element-id"} to the config.' };
  }
  el.setAttribute('data-h2m-stage', '');
  const r = el.getBoundingClientRect();
  return { selector: window.__h2mPath(el), w: r.width, h: r.height, bg: getComputedStyle(el).backgroundColor };
}
"""

JS_FIND_REPLAY = r"""
([sel, stageSel]) => {
  const st = document.querySelector(stageSel);
  if (sel === 'none') return { mode: 'none' };
  if (sel && sel.startsWith('class:')) return { mode: 'class', name: sel.slice(6) };
  let el = null;
  if (sel) {
    el = document.querySelector(sel);
    if (!el) return { error: 'The replay selector "' + sel + '" matches nothing on the page.' };
  } else {
    const label = b => [b.textContent, b.value, b.title, b.getAttribute('aria-label')].filter(Boolean).join(' ').replace(/\s+/g, ' ').trim();
    const cands = [...document.querySelectorAll('button, [role="button"], input[type="button"], a')]
      .filter(b => !b.closest('dialog, [data-h2m-ignore]'));
    el = cands.find(b => /^(re-?play|replay animation|play again|restart)$/i.test(label(b)))
      || cands.find(b => /re-?play/i.test(b.id || ''))
      || cands.find(b => /\b(re-?play|restart|play again|play)\b/i.test(label(b)));
  }
  if (el) return { mode: 'button', selector: window.__h2mPath(el), text: (el.textContent || el.value || '').replace(/\s+/g, ' ').trim() };
  if (st) for (const n of ['play', 'playing', 'animate', 'run', 'start']) if (st.classList.contains(n)) return { mode: 'class', name: n };
  return { mode: 'none' };
}
"""

# Make the card the whole frame: fixed to the viewport, everything else hidden.
JS_PREPARE = r"""
(o) => {
  const st = document.querySelector(o.stage);
  st.setAttribute('data-h2m-stage', '');
  if (o.square) {
    // Full-size layers that copy the card's rounded corners get squared off too.
    const r = getComputedStyle(st).borderRadius, W = st.offsetWidth, H = st.offsetHeight;
    if (r && r !== '0px') for (const e of st.querySelectorAll('*')) {
      if (typeof e.offsetWidth !== 'number') continue;
      if (getComputedStyle(e).borderRadius === r && Math.abs(e.offsetWidth - W) < 3 && Math.abs(e.offsetHeight - H) < 3)
        e.setAttribute('data-h2m-square', '');
    }
  }
  for (let n = st; n.parentElement && n !== document.body; n = n.parentElement) {
    for (const s of n.parentElement.children) {
      if (s === n || /^(STYLE|LINK|SCRIPT|TEMPLATE|META|TITLE|BASE|NOSCRIPT)$/i.test(s.tagName)) continue;
      if (s instanceof SVGElement) { const b = s.getBoundingClientRect(); if (b.width < 2 || b.height < 2) continue; }
      s.setAttribute('data-h2m-hide', '');
    }
  }
  const css = document.createElement('style');
  css.textContent =
    'html,body{margin:0!important;padding:0!important;border:0!important;overflow:hidden!important;min-height:0!important;background:' + o.bg + '!important}' +
    '[data-h2m-hide]{display:none!important}' +
    '[data-h2m-stage]{position:fixed!important;left:' + o.x + 'px!important;top:' + o.y + 'px!important;width:' + o.w + 'px!important;height:' + o.h + 'px!important;' +
    'min-width:0!important;max-width:none!important;min-height:0!important;max-height:none!important;aspect-ratio:auto!important;margin:0!important;z-index:2147483647!important' +
    (o.square ? ';border-radius:0!important' : '') + '}' +
    '[data-h2m-square]{border-radius:0!important}';
  document.head.appendChild(css);
  const r = st.getBoundingClientRect();
  return { w: r.width, h: r.height };
}
"""

# Restart the animation, freeze every animation and expose a seek(ms) function.
JS_START = r"""
(rp) => {
  const st = document.querySelector('[data-h2m-stage]');
  if (rp.mode === 'button') { const b = document.querySelector(rp.selector); if (b) b.click(); }
  else if (rp.mode === 'class') { st.classList.remove(rp.name); void st.offsetWidth; st.classList.add(rp.name); }
  const H = window.__h2m = { tracked: new Map(), t: 0 };
  for (const a of document.getAnimations()) { a.pause(); H.tracked.set(a, 0); }
  window.__h2mSeek = (ms) => {
    for (const a of document.getAnimations()) if (!H.tracked.has(a)) { a.pause(); H.tracked.set(a, H.t); }
    for (const [a, born] of H.tracked) {
      if (a.playState === 'idle') continue;
      a.currentTime = Math.max(0, ms - born);
    }
    H.t = ms;
  };
  const timing = a => (a.effect && a.effect.getComputedTiming) ? a.effect.getComputedTiming() : null;
  let end = 0, last = null, infinite = 0;
  for (const a of H.tracked.keys()) {
    const t = timing(a);
    if (!t) continue;
    if (!isFinite(t.endTime)) { infinite++; continue; }
    if (t.endTime > end) { end = t.endTime; last = a; }
  }
  const res = { count: H.tracked.size, infinite, end, cover: false, coverStart: 0 };
  // Does the animation finish by fading the whole card to a solid colour?
  const tg = last && last.effect.target;
  if (tg && typeof tg.offsetWidth === 'number' && tg.offsetWidth >= st.offsetWidth * 0.95 && tg.offsetHeight >= st.offsetHeight * 0.95) {
    window.__h2mSeek(end);
    const cs = getComputedStyle(tg), m = cs.backgroundColor.match(/[\d.]+/g);
    if (parseFloat(cs.opacity) > 0.98 && m && (m.length < 4 || parseFloat(m[3]) > 0.98)) {
      res.cover = true;
      res.coverStart = timing(last).delay;
    }
    window.__h2mSeek(0);
  }
  return res;
}
"""


# --------------------------------------------------------------------------- small helpers

def say(msg=""):
    print(msg, flush=True)


def norm(s) -> str:
    return re.sub(r"[^0-9a-z]+", "", str(s).lower())


def even(n) -> int:
    n = int(round(float(n)))
    return n if n % 2 == 0 else n + 1


def fmt_value(c, v=None):
    v = c["value"] if v is None else v
    if c["type"] == "select":
        return dict(c["choices"]).get(v, v) or "(none)"
    if c["type"] in ("checkbox", "radio"):
        return "yes" if v else "no"
    return str(v)


def config_path_for(html: Path) -> Path:
    return html.with_suffix(".config.json")


def find_ffmpeg() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        raise UserError("ffmpeg was not found. Install it (for example: winget install Gyan.FFmpeg) "
                        "and open a new terminal.")


def ainput(prompt: str) -> asyncio.Future:
    """input() that does not block the event loop (the browser keeps working meanwhile)."""
    loop = asyncio.get_running_loop()
    fut = loop.create_future()

    def run():
        try:
            res, exc = input(prompt).lstrip("﻿"), None
        except BaseException as e:   # EOFError when stdin is closed
            res, exc = None, e

        def done():
            if not fut.done():
                fut.set_exception(exc) if exc else fut.set_result(res)
        try:
            loop.call_soon_threadsafe(done)
        except RuntimeError:
            pass

    threading.Thread(target=run, daemon=True).start()
    return fut


def ask(prompt: str, default: str = "") -> str:
    try:
        s = input(prompt).lstrip("﻿").strip()
    except EOFError:
        s = ""
    return s or default


def ask_choice(title: str, options: list[tuple[str, str]], default_key: str | None = None) -> str:
    keys = [k for k, _ in options]
    d = keys.index(default_key) if default_key in keys else 0
    say(f"\n{title}")
    for i, (_, text) in enumerate(options, 1):
        say(f"  {i}) {text}")
    while True:
        s = ask(f"Choose 1-{len(options)} [{d + 1}]: ")
        if not s:
            return keys[d]
        if s.isdigit() and 1 <= int(s) <= len(options):
            return keys[int(s) - 1]
        say("  Please type one of the numbers.")


def clean_path_input(s: str) -> str:
    """Paths dragged into a Windows terminal arrive as "C:\\x y.mp3" or & 'C:\\x y.mp3'."""
    s = s.strip()
    if s.startswith("& "):
        s = s[2:].strip()
    return s.strip('"').strip("'")


# --------------------------------------------------------------------------- config

def read_config(path: Path) -> dict:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise UserError(f"{path.name} is not valid JSON (line {e.lineno}, column {e.colno}): {e.msg}")
    opts = {k: (v.get("value") if isinstance(v, dict) else v) for k, v in (raw.get("options") or {}).items()}
    video = dict(raw.get("video") or {})
    for k in ("audio", "out"):      # relative paths in a config are relative to the config file
        if video.get(k):
            p = Path(video[k]).expanduser()
            video[k] = str(p if p.is_absolute() else (path.parent / p).resolve())
    return {"options": opts, "video": video, "page": dict(raw.get("page") or {})}


def save_config(path: Path, html: Path, cfg: dict, controls: list[dict] | None):
    options = {}
    if controls:
        for c in controls:
            o = {"label": c["label"]}
            if c.get("group"):
                o["group"] = c["group"]
            o["type"] = c["type"]
            o["value"] = cfg["options"].get(c["key"], c["value"])
            if c["type"] == "select":
                o["choices"] = {v: t for v, t in c["choices"]}
            options[c["key"]] = o
    else:
        options = dict(cfg.get("options") or {})
    data = {
        "_help": ("Change any \"value\" below (for lists use one of the \"choices\" keys or its text), "
                  "then run:  python html2mp4.py render " + html.name),
        "html": html.name,
        "options": options,
        "video": {**VIDEO_DEFAULTS, **(cfg.get("video") or {})},
        "page": {**PAGE_DEFAULTS, **(cfg.get("page") or {})},
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def effective_video(v: dict) -> dict:
    eff = {**VIDEO_DEFAULTS, **{k: x for k, x in v.items() if x is not None}}
    q = str(eff["quality"]).lower()
    if q not in PRESETS:
        raise UserError(f'Unknown quality "{q}". Use one of: {", ".join(PRESETS)}')
    eff["quality"] = q
    for k, x in PRESETS[q].items():
        if eff.get(k) is None:
            eff[k] = x
    eff["codec"] = str(eff["codec"]).lower()
    if eff["codec"] not in ("h264", "h265", "prores"):
        raise UserError('codec must be h264, h265 or prores')
    if eff["crf"] is None and eff["codec"] != "prores":
        eff["crf"] = 14
    if eff["preset"] is None:
        eff["preset"] = "slow"
    try:
        for k in ("fps", "crf", "hold", "start", "audio_start", "audio_volume", "duration", "width", "height"):
            if eff[k] is not None:
                eff[k] = float(eff[k])
        eff["workers"], eff["seed"] = int(eff["workers"] or 0), int(eff["seed"])
    except (TypeError, ValueError) as e:
        raise UserError(f"A number in the video settings is not valid: {e}")
    if str(eff["corners"]).lower() not in ("auto", "square", "round"):
        raise UserError('corners must be auto, square or round')
    return eff


def find_control(controls: list[dict], name: str) -> dict:
    for c in controls:
        if c["key"] == name:
            return c
    n = norm(name)
    hits = [c for c in controls if norm(c["label"]) == n] or \
           [c for c in controls if n and n in norm(c["label"])]
    if len(hits) == 1:
        return hits[0]
    if hits:
        raise UserError(f'"{name}" matches several options: ' +
                        ", ".join(f'{c["label"]} ({c["key"]})' for c in hits))
    raise UserError(f'This page has no option called "{name}". Run "scan" to list them.')


def coerce(c: dict, raw):
    t, label = c["type"], c["label"]
    if t == "select":
        for v, _ in c["choices"]:
            if str(raw) == v:
                return v
        for v, txt in c["choices"]:
            if norm(raw) in (norm(v), norm(txt)):
                return v
        hits = [v for v, txt in c["choices"] if norm(raw) and norm(raw) in norm(txt)]
        if len(hits) == 1:
            return hits[0]
        raise UserError(f'"{raw}" is not a choice for "{label}". Choices: ' +
                        ", ".join(f"{txt}" for _, txt in c["choices"]))
    if t in ("checkbox", "radio"):
        if isinstance(raw, bool):
            return raw
        s = str(raw).strip().lower()
        if s in ("1", "true", "yes", "y", "on"):
            return True
        if s in ("0", "false", "no", "n", "off"):
            return False
        raise UserError(f'"{label}" needs yes or no, got "{raw}"')
    if t == "color":
        s = str(raw).strip().lstrip("#")
        if re.fullmatch(r"[0-9a-fA-F]{3}", s):
            s = "".join(ch * 2 for ch in s)
        if not re.fullmatch(r"[0-9a-fA-F]{6}", s):
            raise UserError(f'"{label}" needs a colour like #B8913F, got "{raw}"')
        return "#" + s.lower()
    if t in ("range", "number"):
        try:
            f = float(raw)
        except ValueError:
            raise UserError(f'"{label}" needs a number, got "{raw}"')
        return int(f) if f.is_integer() else f
    return str(raw)


def resolve_values(controls, opts: dict, sets: list[str]):
    """Config values (applied together, page order) + --set overrides (applied one by one)."""
    by_key = {c["key"]: c for c in controls}
    base, unknown = {}, []
    for k, raw in (opts or {}).items():
        if raw is None:
            continue
        if k not in by_key:
            unknown.append(k)
            continue
        base[k] = coerce(by_key[k], raw)
    if unknown:
        say(f"  Note: ignoring options this page does not have: {', '.join(unknown)}")
    overrides = []
    for s in sets or []:
        if "=" not in s:
            raise UserError(f'--set needs NAME=VALUE, got "{s}"')
        name, raw = s.split("=", 1)
        c = find_control(controls, name.strip())
        overrides.append((c["key"], coerce(c, raw.strip())))
    return base, overrides


def output_path(html: Path, video: dict) -> Path:
    if video.get("out"):
        p = Path(video["out"])
        if not p.suffix:
            p = p.with_suffix(".mov" if video["codec"] == "prores" else ".mp4")
        return p
    ext = ".mov" if video["codec"] == "prores" else ".mp4"
    folder = html.parent / "videos"
    p = folder / (html.stem + ext)
    i = 2
    while p.exists():
        p = folder / f"{html.stem}_{i}{ext}"
        i += 1
    return p


# --------------------------------------------------------------------------- browser

async def launch(p, headless=True, gpu=False):
    args = LAUNCH_ARGS + (["--hide-scrollbars"] if headless else ["--start-maximized"]) + (GPU_ARGS if gpu else [])
    errors = []
    for channel in (None, "msedge", "chrome"):
        try:
            return await p.chromium.launch(headless=headless, channel=channel, args=args)
        except Exception as e:
            errors.append(f"{channel or 'playwright chromium'}: {str(e).strip().splitlines()[0]}")
    raise UserError("Could not start a browser:\n  " + "\n  ".join(errors) +
                    "\nFix: python -m playwright install chromium")


async def new_page(browser, viewport, scale, seed, virtual=False):
    ctx = await browser.new_context(viewport=viewport, device_scale_factor=scale,
                                    reduced_motion="no-preference", color_scheme="light")
    await ctx.add_init_script(JS_INIT.replace("%SEED%", str(int(seed))))
    page = await ctx.new_page()
    if virtual:
        await page.clock.install()
    return ctx, page


async def goto(page, html: Path):
    try:
        await page.goto(html.as_uri(), wait_until="load", timeout=90_000)
    except Exception as e:
        raise UserError(f"Could not open {html.name}: {str(e).splitlines()[0]}")


class Probe:
    """A normal-sized tab used to read the page's options, find the card and replay button."""

    @classmethod
    async def open(cls, browser, html: Path, pagecfg: dict, seed: int):
        self = cls()
        self.ctx, self.page = await new_page(browser, {"width": 1280, "height": 900}, 1, seed)
        await goto(self.page, html)
        self.controls = await self.page.evaluate(JS_SCAN)
        self.stage = await self.page.evaluate(JS_FIND_STAGE, pagecfg.get("stage"))
        if self.stage.get("error"):
            raise UserError(self.stage["error"])
        self.replay = await self.page.evaluate(JS_FIND_REPLAY, [pagecfg.get("replay"), self.stage["selector"]])
        if self.replay.get("error"):
            raise UserError(self.replay["error"])
        return self

    async def apply(self, base, overrides):
        bad = []
        if base:
            bad += await self.page.evaluate(JS_APPLY, base)
        for k, v in overrides:
            bad += await self.page.evaluate(JS_APPLY, {k: v})
        self.controls = await self.page.evaluate(JS_SCAN)
        return bad


def describe_replay(rp: dict) -> str:
    if rp["mode"] == "button":
        return f'clicks the "{rp["text"] or rp["selector"]}" button ({rp["selector"]})'
    if rp["mode"] == "class":
        return f'toggles the "{rp["name"]}" class on the card'
    return "none (animations are played from when the page loaded)"


def plan_timeline(tl: dict, video: dict):
    end = tl["end"] / 1000.0
    start = float(video["start"] or 0)
    if video["duration"]:
        dur = float(video["duration"])
        why = "length set by you"
    elif tl["cover"]:
        dur = end + 0.5
        why = f"animations end at {end:.1f}s with a fade-out, +0.5s"
    elif end > 0:
        dur = end + float(video["hold"])
        why = f"animations end at {end:.1f}s, +{float(video['hold']):g}s hold on the finished card"
    else:
        dur = 10.0
        why = "no animation end found, using 10s"
    if dur <= start:
        raise UserError(f"The video would be empty: start {start}s is after the end ({dur:.1f}s).")
    poster_t = (tl["coverStart"] / 1000.0 - 0.05) if tl["cover"] else min(end + 0.5, dur)
    return start, dur, why, min(max(poster_t, start), dur)


# --------------------------------------------------------------------------- rendering

def geometry(stage: dict, video: dict, pagecfg: dict) -> dict:
    aspect = stage["w"] / stage["h"]
    out_w = even(video["width"])
    card_h = even(out_w / aspect)
    out_h = even(video["height"]) if video["height"] else card_h
    w0 = float(pagecfg.get("design_width") or 360)       # CSS width the card is laid out at
    h0 = w0 * card_h / out_w
    scale = min(out_w / w0, out_h / h0)
    cw, ch = out_w / scale, out_h / scale
    fills = abs(cw - w0) < 0.5 and abs(ch - h0) < 0.5
    corners = str(video["corners"]).lower()
    square = corners == "square" or (corners == "auto" and fills)
    return {"out_w": out_w, "out_h": out_h, "w0": w0, "h0": h0, "scale": scale, "cw": cw, "ch": ch,
            "vw": math.ceil(cw - 1e-6), "vh": math.ceil(ch - 1e-6),
            "x": (cw - w0) / 2, "y": (ch - h0) / 2, "fills": fills, "square": square}


async def open_worker(browser, html, geo, pagecfg, stage, replay, base, overrides, video):
    virtual = bool(pagecfg.get("virtual_time"))
    ctx, page = await new_page(browser, {"width": geo["vw"], "height": geo["vh"]}, geo["scale"],
                               video["seed"], virtual)
    await goto(page, html)
    if virtual:      # page timers only move when we step the clock, frame by frame
        await page.clock.pause_at(datetime.now() + timedelta(seconds=2))
    bad = []
    if base:
        bad += await page.evaluate(JS_APPLY, base)
    for k, v in overrides:
        bad += await page.evaluate(JS_APPLY, {k: v})
    if virtual:
        await page.clock.run_for(SETTLE_MS)
    else:
        await page.wait_for_timeout(SETTLE_MS)
    # Fonts/photos are loaded for the options now in effect; the page re-measures text when fonts arrive.
    try:
        assets = await asyncio.wait_for(page.evaluate(JS_LOAD_ASSETS, stage["selector"]), 60)
    except asyncio.TimeoutError:
        assets = {"total": 0, "failedFonts": ["(timed out loading fonts)"], "failedSheets": []}
    if virtual:
        await page.clock.run_for(400)
    else:
        await page.wait_for_timeout(400)
    bg = video["background"] or stage["bg"]
    await page.evaluate(JS_PREPARE, {"stage": stage["selector"], "x": geo["x"], "y": geo["y"],
                                     "w": geo["w0"], "h": geo["h0"], "bg": bg, "square": geo["square"]})
    tl = await page.evaluate(JS_START, replay)
    cdp = await ctx.new_cdp_session(page)
    return {"ctx": ctx, "page": page, "cdp": cdp, "assets": assets, "bad": bad, "tl": tl,
            "virtual": virtual, "clock": 0}


def ffmpeg_command(ffmpeg, video, geo, audio: Path | None, dur, out: Path):
    fps = video["fps"]
    cmd = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
           "-f", "image2pipe", "-framerate", f"{fps:g}", "-c:v", "png", "-i", "-"]
    if audio:
        cmd += ["-stream_loop", "-1", "-ss", f"{float(video['audio_start']):g}", "-i", str(audio)]
    pix = "yuv444p10le" if video["codec"] == "prores" else "yuv420p"
    # Chromium frames are sRGB; convert with the BT.709 matrix and tag the video as BT.709 so
    # phones, browsers and editors all show the exact colours (no washed-out / shifted gold).
    cmd += ["-vf", (f"scale={geo['out_w']}:{geo['out_h']}:flags=lanczos+accurate_rnd+full_chroma_int"
                    f":out_color_matrix=bt709:out_range=tv,format={pix},"
                    f"setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709"),
            "-r", f"{fps:g}", "-pix_fmt", pix]
    if video["codec"] == "h264":
        cmd += ["-c:v", "libx264", "-preset", video["preset"], "-crf", f"{video['crf']:g}",
                "-profile:v", "high", "-x264-params", "aq-mode=3"]
    elif video["codec"] == "h265":
        cmd += ["-c:v", "libx265", "-preset", video["preset"], "-crf", f"{video['crf']:g}",
                "-tag:v", "hvc1", "-x265-params", "aq-mode=3:log-level=error"]
    else:
        cmd += ["-c:v", "prores_ks", "-profile:v", "4", "-vendor", "apl0"]
    cmd += ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]
    if audio:
        fade_out = max(0.0, dur - 2.5)
        cmd += ["-map", "0:v:0", "-map", "1:a:0",
                "-af", (f"volume={float(video['audio_volume']):g},afade=t=in:st=0:d=0.6,"
                        f"afade=t=out:st={fade_out:.3f}:d=2.5"),
                "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest"]
    cmd += ["-movflags", "+faststart", str(out)]
    return cmd


async def render(html: Path, cfg: dict, sets: list[str] | None = None) -> Path:
    video = effective_video(cfg.get("video") or {})
    pagecfg = {**PAGE_DEFAULTS, **(cfg.get("page") or {})}
    ffmpeg = find_ffmpeg()
    audio = Path(video["audio"]) if video["audio"] else None
    if audio and not audio.exists():
        raise UserError(f"Audio file not found: {audio}")
    out = output_path(html, video)

    say(f"\nRendering {html.name}")
    async with async_playwright() as p:
        browser = await launch(p, gpu=bool(video["gpu"]))
        browsers = [browser]
        try:
            pr = await Probe.open(browser, html, pagecfg, video["seed"])
            defaults = {c["key"]: c["value"] for c in pr.controls}
            base, overrides = resolve_values(pr.controls, cfg.get("options") or {}, sets or [])
            await pr.apply(base, overrides)
            changed = [c for c in pr.controls if c["value"] != defaults.get(c["key"])]
            await pr.ctx.close()

            geo = geometry(pr.stage, video, pagecfg)
            n_workers = int(video["workers"] or 0) or max(1, min(3, (os.cpu_count() or 4) // 2))
            say(f"  Card     : {pr.stage['selector']}   replay: {describe_replay(pr.replay)}")
            if changed:
                say("  Options  : " + "; ".join(f"{c['label']} = {fmt_value(c)}" for c in changed))
            else:
                say("  Options  : page defaults")
            say(f"  Preparing {n_workers} renderer(s) ...")
            # One browser per worker: tabs inside a single browser share its compositor and barely
            # run in parallel; separate browsers do.
            browsers += await asyncio.gather(*(launch(p, gpu=bool(video["gpu"])) for _ in range(n_workers - 1)))
            workers = await asyncio.gather(*(open_worker(b, html, geo, pagecfg, pr.stage, pr.replay,
                                                         base, overrides, video) for b in browsers))
            w0 = workers[0]
            if w0["assets"]["failedSheets"] or w0["assets"]["failedFonts"]:
                say("  WARNING: some fonts/styles did not load (are you online?) - text may use a fallback font:")
                for x in w0["assets"]["failedSheets"] + w0["assets"]["failedFonts"]:
                    say(f"           {x}")
            if w0["bad"]:
                say("  WARNING: these options could not be set as requested: " + ", ".join(sorted(set(w0["bad"]))))

            start, dur, why, poster_t = plan_timeline(w0["tl"], video)
            fps = video["fps"]
            n = max(1, round((dur - start) * fps))
            poster_i = min(n - 1, max(0, round((poster_t - start) * fps)))
            q = ("ProRes 4444" if video["codec"] == "prores"
                 else f"{video['codec'].upper().replace('H', 'H.')} CRF {video['crf']:g} ({video['preset']})")
            say(f"  Timeline : {why} = {dur - start:.2f}s")
            say(f"  Output   : {geo['out_w']}x{geo['out_h']}, {fps:g} fps, {q}, {n} frames"
                + (f", music: {audio.name}" if audio else ""))
            say(f"  File     : {out}")

            out.parent.mkdir(parents=True, exist_ok=True)
            part = out.with_name(out.stem + ".part" + out.suffix)
            cmd = ffmpeg_command(ffmpeg, video, geo, audio, dur - start, part)
            proc = await asyncio.create_subprocess_exec(*cmd, stdin=subprocess.PIPE,
                                                        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            err_task = asyncio.create_task(proc.stderr.read())
            queues = [asyncio.Queue(maxsize=6) for _ in workers]
            clip = {"x": 0, "y": 0, "width": geo["cw"], "height": geo["ch"], "scale": geo["scale"]}

            async def produce(k, w):
                try:
                    for i in range(k, n, len(workers)):
                        t = (start + i / fps) * 1000.0
                        if w["virtual"]:
                            target = round(t)
                            if target > w["clock"]:
                                await w["page"].clock.run_for(target - w["clock"])
                                w["clock"] = target
                        await w["page"].evaluate("t => window.__h2mSeek(t)", t)
                        r = await w["cdp"].send("Page.captureScreenshot", {
                            "format": "png", "optimizeForSpeed": True, "captureBeyondViewport": False, "clip": clip})
                        await queues[k].put(base64.b64decode(r["data"]))
                except Exception as e:
                    await queues[k].put(e)

            tasks = [asyncio.create_task(produce(k, w)) for k, w in enumerate(workers)]
            poster_png = None
            t0 = last = time.time()
            ok = False
            try:
                for i in range(n):
                    item = await queues[i % len(workers)].get()
                    if isinstance(item, Exception):
                        raise item
                    if i == poster_i:
                        poster_png = item
                    try:
                        proc.stdin.write(item)
                        await proc.stdin.drain()
                    except (BrokenPipeError, ConnectionResetError):
                        await proc.wait()
                        raise UserError("ffmpeg stopped:\n" + (await err_task).decode(errors="replace"))
                    now = time.time()
                    if now - last > 0.25 or i == n - 1:
                        last = now
                        done = i + 1
                        rate = done / max(now - t0, 1e-6)
                        bar = "#" * int(28 * done / n)
                        sys.stdout.write(f"\r  [{bar:<28}] {done}/{n} frames  {rate:5.1f} fps  "
                                         f"ETA {(n - done) / max(rate, 1e-6):4.0f}s ")
                        sys.stdout.flush()
                proc.stdin.close()
                rc = await proc.wait()
                err = (await err_task).decode(errors="replace").strip()
                if rc != 0:
                    raise UserError(f"ffmpeg failed (exit code {rc}):\n{err}")
                ok = True
            finally:
                for t in tasks:
                    t.cancel()
                if not ok:
                    if proc.returncode is None:
                        proc.kill()
                        await proc.wait()
                    try:
                        part.unlink()
                    except OSError:
                        pass
            say("")
            part.replace(out)
            if video["poster"] and poster_png:
                out.with_name(out.stem + "_poster.png").write_bytes(poster_png)
        finally:
            for b in browsers:
                try:
                    await b.close()
                except Exception:
                    pass

    size = out.stat().st_size / 1e6
    say(f"\n  Done in {time.time() - t0:.0f}s  ->  {out}  ({size:.1f} MB)")
    if video["poster"]:
        say(f"  Still image of the finished card: {out.with_name(out.stem + '_poster.png')}")
    return out


# --------------------------------------------------------------------------- snap (still frames + contact sheet)

def parse_times(spec, every, count, start, dur, end_s, fps):
    pts = []
    if spec:
        for part in str(spec).split(","):
            part = part.strip().lower()
            if not part:
                continue
            if part in ("end", "card"):
                pts.append(min(dur, end_s + 0.4))
            elif part in ("last", "dur"):
                pts.append(dur - 1.0 / fps)
            else:
                try:
                    pts.append(float(part))
                except ValueError:
                    raise UserError(f'--times: "{part}" is not a number, "end" or "last"')
    elif every:
        t = start
        while t < dur - 1e-6:
            pts.append(t)
            t += float(every)
        pts.append(dur - 1.0 / fps)
    else:
        n = max(1, int(count or 12))
        lo, hi = start + 0.25, dur - 0.05
        pts = [lo + (hi - lo) * i / (n - 1) for i in range(n)] if n > 1 else [hi]
    return sorted({round(min(max(t, 0.0), dur), 3) for t in pts})


def make_sheet(shots, cols, dest: Path, tile_w=270):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return None
    ims = [(t, Image.open(pth).convert("RGB")) for t, pth in shots]
    w0, h0 = ims[0][1].size
    tw = min(tile_w, w0)
    th = round(h0 * tw / w0)
    lab, gap = 26, 8
    cols = max(1, min(cols, len(ims)))
    rows = math.ceil(len(ims) / cols)
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * gap, rows * (th + lab) + (rows + 1) * gap), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 17)
    except Exception:
        font = ImageFont.load_default()
    for i, (t, im) in enumerate(ims):
        x = gap + (i % cols) * (tw + gap)
        y = gap + (i // cols) * (th + lab + gap)
        d.text((x + 4, y + 4), f"{t:.2f}s", fill=(235, 235, 235), font=font)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y + lab))
    sheet.save(dest)
    return dest


async def snap(html: Path, cfg: dict, sets: list[str], opts: dict):
    video = effective_video(cfg.get("video") or {})
    pagecfg = {**PAGE_DEFAULTS, **(cfg.get("page") or {})}
    outdir = Path(opts["outdir"]) if opts.get("outdir") else html.parent / "videos" / "snaps" / html.stem
    outdir.mkdir(parents=True, exist_ok=True)
    prefix = opts.get("prefix") or ""
    async with async_playwright() as p:
        browser = await launch(p, gpu=bool(video["gpu"]))
        try:
            pr = await Probe.open(browser, html, pagecfg, video["seed"])
            defaults = {c["key"]: c["value"] for c in pr.controls}
            base, overrides = resolve_values(pr.controls, cfg.get("options") or {}, sets or [])
            await pr.apply(base, overrides)
            changed = [c for c in pr.controls if c["value"] != defaults.get(c["key"])]
            await pr.ctx.close()
            geo = geometry(pr.stage, video, pagecfg)
            w = await open_worker(browser, html, geo, pagecfg, pr.stage, pr.replay, base, overrides, video)
            if w["assets"]["failedSheets"] or w["assets"]["failedFonts"]:
                say("  WARNING: fonts/styles failed to load: " + ", ".join(w["assets"]["failedSheets"] + w["assets"]["failedFonts"]))
            if w["bad"]:
                say("  WARNING: could not set: " + ", ".join(sorted(set(w["bad"]))))
            start, dur, why, _ = plan_timeline(w["tl"], video)
            times = parse_times(opts.get("times"), opts.get("every"), opts.get("count"), start, dur,
                                w["tl"]["end"] / 1000.0, video["fps"])
            clip = {"x": 0, "y": 0, "width": geo["cw"], "height": geo["ch"], "scale": geo["scale"]}
            shots = []
            if opts.get("static"):
                # The card exactly as the editor and the gallery thumbnails show it (no animation running).
                await w["page"].evaluate("() => document.querySelector('[data-h2m-stage]').classList.remove('play')")
                await w["page"].wait_for_timeout(200)
                times = [0.0]
                prefix = prefix + "static_"
            for t in times:
                ms = t * 1000.0
                if w["virtual"]:
                    target = round(ms)
                    if target > w["clock"]:
                        await w["page"].clock.run_for(target - w["clock"])
                        w["clock"] = target
                if not opts.get("static"):
                    await w["page"].evaluate("t => window.__h2mSeek(t)", ms)
                r = await w["cdp"].send("Page.captureScreenshot", {
                    "format": "png", "optimizeForSpeed": True, "captureBeyondViewport": False, "clip": clip})
                path = outdir / f"{prefix}{t:07.3f}s.png"
                path.write_bytes(base64.b64decode(r["data"]))
                shots.append((t, path))
        finally:
            await browser.close()
    sheet = Path(opts["sheet"]) if opts.get("sheet") else outdir / f"{prefix}sheet.png"
    made = make_sheet(shots, int(opts.get("cols") or 4), sheet) if shots else None
    say(f"{html.name}: {why} = {dur - start:.2f}s; {w['tl']['count']} animations ({w['tl']['infinite']} looping)")
    if changed:
        say("  options: " + "; ".join(f"{c['label']} = {fmt_value(c)}" for c in changed))
    say(f"  {len(shots)} frames ({geo['out_w']}x{geo['out_h']}) in {outdir}")
    if made:
        say(f"  contact sheet: {made}")
    return shots


# --------------------------------------------------------------------------- scan / design / terminal editing

def print_controls(controls):
    group = object()
    for c in controls:
        if c["group"] != group:
            group = c["group"]
            say(f"\n  {group or 'Options'}")
        name = f"{c['label']} ({c['key']})"
        if c["type"] == "select":
            val = "  |  ".join(f"[{t}]" if v == c["value"] else t for v, t in c["choices"])
        else:
            val = fmt_value(c)
        say(f"    {name:<36} {val}")


async def scan(html: Path, cfg: dict, write: bool = True):
    pagecfg = {**PAGE_DEFAULTS, **(cfg.get("page") or {})}
    video = effective_video(cfg.get("video") or {})
    async with async_playwright() as p:
        browser = await launch(p)
        try:
            pr = await Probe.open(browser, html, pagecfg, video["seed"])
            base, _ = resolve_values(pr.controls, cfg.get("options") or {}, [])
            bad = await pr.apply(base, [])
            tl = await pr.page.evaluate(JS_START, pr.replay)
        finally:
            await browser.close()
    start, dur, why, _ = plan_timeline(tl, video)
    say(f"\n{html.name}")
    say(f"  Card      : {pr.stage['selector']}  ({pr.stage['w']:.0f}x{pr.stage['h']:.0f} on screen)")
    say(f"  Replay    : {describe_replay(pr.replay)}")
    say(f"  Animations: {tl['count']} ({tl['infinite']} looping)   video length: {why} = {dur - start:.1f}s")
    if bad:
        say("  WARNING: could not set: " + ", ".join(bad))
    print_controls(pr.controls)
    if write:
        cp = config_path_for(html)
        cfg = {**cfg, "options": {c["key"]: c["value"] for c in pr.controls}}
        save_config(cp, html, cfg, pr.controls)
        say(f"\nSaved all options to {cp}")
        say(f'Edit the "value" fields (or run: python html2mp4.py design "{html.name}"), then:')
        say(f'  python html2mp4.py render "{html.name}"')
    return pr.controls


async def design(html: Path, cfg: dict):
    """Open the real page in a visible browser; the user sets options with the page's own editor."""
    pagecfg = {**PAGE_DEFAULTS, **(cfg.get("page") or {})}
    async with async_playwright() as p:
        browser = await launch(p, headless=False)
        ctx = await browser.new_context(no_viewport=True, color_scheme="light")
        await ctx.add_init_script(JS_INIT.replace("%SEED%", "7"))
        page = await ctx.new_page()
        await goto(page, html)
        controls = await page.evaluate(JS_SCAN)
        base, _ = resolve_values(controls, cfg.get("options") or {}, [])
        if base:
            await page.evaluate(JS_APPLY, base)
            stage = await page.evaluate(JS_FIND_STAGE, pagecfg.get("stage"))
            if not stage.get("error"):
                rp = await page.evaluate(JS_FIND_REPLAY, [pagecfg.get("replay"), stage["selector"]])
                if rp.get("mode") == "button":
                    await page.evaluate("s => document.querySelector(s).click()", rp["selector"])
        say("\n  A browser window is open with your card and its editor.")
        say("  Change anything you like there: animation style, border, fonts, colours, names, dates...")
        say("  Use Replay in the page to preview.")
        fut = ainput("\n  >> When it looks right, come back here and press Enter ")
        snap, closed = await page.evaluate(JS_SCAN), False
        while not fut.done():
            try:
                snap = await page.evaluate(JS_SCAN)
            except Exception:
                if not closed:
                    closed = True
                    say("\n  The browser window was closed - your last settings were kept. Press Enter.")
            await asyncio.sleep(0.4)
        try:
            await fut
        except EOFError:
            pass
        try:
            await browser.close()
        except Exception:
            pass
    return {c["key"]: c["value"] for c in snap}, snap


async def ask_control(c: dict):
    label, cur = c["label"], fmt_value(c)
    while True:
        if c["type"] == "select":
            say(f"    {label}:  " + "   ".join(f"{i}={t}" for i, (_, t) in enumerate(c["choices"], 1)))
            prompt = f"    {label} [{cur}]: "
        elif c["type"] in ("checkbox", "radio"):
            prompt = f"    {label} (y/n) [{cur}]: "
        elif c["type"] == "color":
            prompt = f"    {label} colour, e.g. #B8913F [{cur}]: "
        else:
            prompt = f"    {label} [{cur}]: "
        try:
            s = (await ainput(prompt)).strip()
        except EOFError:
            return None
        if not s:
            return None
        if c["type"] == "select" and s.isdigit() and 1 <= int(s) <= len(c["choices"]):
            return c["choices"][int(s) - 1][0]
        try:
            return coerce(c, s)
        except UserError as e:
            say(f"      {e}")


async def edit_in_terminal(html: Path, cfg: dict):
    pagecfg = {**PAGE_DEFAULTS, **(cfg.get("page") or {})}
    async with async_playwright() as p:
        browser = await launch(p)
        try:
            pr = await Probe.open(browser, html, pagecfg, 7)
            base, _ = resolve_values(pr.controls, cfg.get("options") or {}, [])
            await pr.apply(base, [])
            controls = pr.controls
            say("\n  Press Enter to keep the value shown in [brackets].")
            group = None
            for i in range(len(controls)):
                c = controls[i]
                if c["group"] != group:
                    group = c["group"]
                    if group:
                        say(f"\n  -- {group} --")
                new = await ask_control(c)
                if new is not None and new != c["value"]:
                    # Apply live so options that change others (styles, themes) update the next questions.
                    await pr.page.evaluate(JS_APPLY, {c["key"]: new})
                    controls = await pr.page.evaluate(JS_SCAN)
        finally:
            await browser.close()
    return {c["key"]: c["value"] for c in controls}, controls


# --------------------------------------------------------------------------- menu + CLI

def pick_html() -> Path:
    files = sorted({f.resolve() for d in (Path.cwd(), HERE) for f in d.glob("*.html")})
    if not files:
        s = clean_path_input(ask("Path to your HTML file: "))
        return Path(s).resolve()
    if len(files) == 1:
        say(f"\nUsing {files[0].name}")
        return files[0]
    key = ask_choice("Which HTML file?", [(str(f), f.name) for f in files])
    return Path(key)


def menu():
    say("=" * 64)
    say("  HTML -> MP4   (high-quality video from an animated HTML page)")
    say("=" * 64)
    html = pick_html()
    if not html.exists():
        raise UserError(f"File not found: {html}")
    cp = config_path_for(html)
    cfg = read_config(cp) if cp.exists() else {"options": {}, "video": {}, "page": {}}
    modes = [("design", "Set the options visually in a browser window (recommended)")]
    if cp.exists():
        modes.append(("saved", f"Use my saved settings ({cp.name})"))
    modes += [("terminal", "Answer questions about each option here in the terminal"),
              ("defaults", "Use the page exactly as it is (default options)")]
    mode = ask_choice("How do you want to set the card's options?", modes,
                      "saved" if cp.exists() else "design")
    controls = None
    if mode == "design":
        cfg["options"], controls = asyncio.run(design(html, cfg))
    elif mode == "terminal":
        cfg["options"], controls = asyncio.run(edit_in_terminal(html, cfg))
    elif mode == "defaults":
        cfg["options"] = {}

    v = cfg.setdefault("video", {})
    q = ask_choice("Video quality?", [(k, PRESET_INFO[k]) for k in PRESETS], v.get("quality") or "high")
    if q != v.get("quality"):
        for k in ("width", "height", "fps", "crf", "codec", "preset"):
            v.pop(k, None)
    v["quality"] = q
    hold = ask(f"\nSeconds to keep the finished card on screen at the end [{v.get('hold', 4.0):g}]: ")
    if hold:
        try:
            v["hold"] = float(hold)
        except ValueError:
            say("  Not a number - keeping the old value.")
    cur_audio = v.get("audio")
    s = clean_path_input(ask("Background music file (drag it here, Enter = "
                             + (f"keep {Path(cur_audio).name}, type none to remove" if cur_audio else "no music")
                             + "): "))
    if s.lower() == "none":
        v["audio"] = None
    elif s:
        a = Path(s).expanduser().resolve()
        if not a.exists():
            say(f"  Not found: {a} - continuing without music.")
            v["audio"] = None
        else:
            v["audio"] = str(a)
            st = ask("Start the music from second [0]: ")
            v["audio_start"] = float(st) if st.replace(".", "", 1).isdigit() else 0.0

    if mode == "saved":
        raw = json.loads(cp.read_text(encoding="utf-8"))
        raw["video"] = {**VIDEO_DEFAULTS, **v}
        cp.write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if mode in ("design", "terminal"):
        save_config(cp, html, cfg, controls)
        say(f"\nSettings saved to {cp.name} (next time pick \"Use my saved settings\").")

    out = asyncio.run(render(html, cfg))
    if sys.platform == "win32" and ask("\nOpen the video now? [Y/n]: ", "y").lower().startswith("y"):
        os.startfile(out)


def build_parser():
    ap = argparse.ArgumentParser(
        prog="html2mp4", formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Turn an animated HTML page into a high-quality MP4.  Run with no arguments for a menu.",
        epilog=__doc__.split("Render / design options", 1)[-1].split("Requirements", 1)[0].strip(" -\n"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp_scan = sub.add_parser("scan", help="list every option the page has and write <name>.config.json")
    sp_design = sub.add_parser("design", help="set options visually in a browser window, then render")
    sp_render = sub.add_parser("render", help="render the video (uses <name>.config.json if present)")
    sp_snap = sub.add_parser("snap", help="save still frames at chosen times plus a contact sheet")
    for sp in (sp_scan, sp_design, sp_render, sp_snap):
        sp.add_argument("html", help="the HTML file")
        sp.add_argument("--config", help="config file (default: <html name>.config.json)")
        sp.add_argument("--stage", help="CSS selector of the animated card (default: auto-detect)")
        sp.add_argument("--replay", help='replay button selector, "class:play" or "none" (default: auto)')
    sp_snap.add_argument("--times", help='comma list of seconds, "end" (finished card) or "last", e.g. 0.5,2,4,end')
    sp_snap.add_argument("--every", type=float, help="one frame every N seconds")
    sp_snap.add_argument("--count", type=int, help="number of evenly spaced frames (default 12)")
    sp_snap.add_argument("--outdir", help="folder for the PNG frames (default videos/snaps/<name>)")
    sp_snap.add_argument("--prefix", help="file name prefix for the frames")
    sp_snap.add_argument("--sheet", help="contact sheet path (default <outdir>/sheet.png)")
    sp_snap.add_argument("--cols", type=int, default=4, help="contact sheet columns (default 4)")
    sp_snap.add_argument("--static", action="store_true", help="capture the card without animation (editor / gallery look)")
    for sp in (sp_design, sp_render, sp_snap):
        sp.add_argument("--set", action="append", default=[], metavar="NAME=VALUE",
                        help="change a page option (by label or id); repeatable")
        sp.add_argument("--quality", choices=list(PRESETS))
        sp.add_argument("--width", type=int)
        sp.add_argument("--height", type=int)
        sp.add_argument("--fps", type=float)
        sp.add_argument("--crf", type=float, help="lower = better quality, bigger file (12-20 sensible)")
        sp.add_argument("--codec", choices=["h264", "h265", "prores"])
        sp.add_argument("--preset", help="x264/x265 speed preset (default slow)")
        sp.add_argument("--hold", type=float, help="seconds to hold the finished card (default 4)")
        sp.add_argument("--duration", type=float, help="exact video length in seconds")
        sp.add_argument("--start", type=float, help="skip this many seconds at the beginning")
        sp.add_argument("--audio", help="background music file")
        sp.add_argument("--audio-start", type=float, dest="audio_start")
        sp.add_argument("--audio-volume", type=float, dest="audio_volume")
        sp.add_argument("--corners", choices=["auto", "square", "round"])
        sp.add_argument("--background", help="colour around the card when the video shape differs")
        sp.add_argument("--no-poster", action="store_true", help="do not save a still PNG of the final card")
        sp.add_argument("--workers", type=int, help="parallel renderers (default auto)")
        sp.add_argument("--no-gpu", action="store_true", dest="no_gpu",
                        help="render on the CPU only (use if frames look glitchy on your PC)")
        sp.add_argument("--seed", type=int, help="random seed for petals/dust positions")
        sp.add_argument("--virtual-time", action="store_true", dest="virtual_time",
                        help="also control JavaScript timers (for pages animated with JS)")
        sp.add_argument("--out", help="output file (default: videos/<html name>.mp4)")
    return ap


def apply_cli(args, cfg: dict):
    v = cfg.setdefault("video", {})
    if getattr(args, "quality", None):
        for k in ("width", "height", "fps", "crf", "codec", "preset"):
            v.pop(k, None)
    for k in ("quality", "width", "height", "fps", "crf", "codec", "preset", "hold", "duration", "start",
              "audio_start", "audio_volume", "corners", "background", "workers", "seed"):
        val = getattr(args, k, None)
        if val is not None:
            v[k] = val
    for k in ("audio", "out"):
        if getattr(args, k, None):
            v[k] = str(Path(clean_path_input(getattr(args, k))).expanduser().resolve())
    if getattr(args, "no_poster", False):
        v["poster"] = False
    if getattr(args, "no_gpu", False):
        v["gpu"] = False
    pg = cfg.setdefault("page", {})
    if args.stage:
        pg["stage"] = args.stage
    if args.replay:
        pg["replay"] = args.replay
    if getattr(args, "virtual_time", False):
        pg["virtual_time"] = True


def cli(argv):
    args = build_parser().parse_args(argv)
    html = Path(clean_path_input(args.html)).expanduser().resolve()
    if not html.exists():
        raise UserError(f"File not found: {html}")
    cp = Path(args.config).resolve() if args.config else config_path_for(html)
    if args.config and not cp.exists():
        raise UserError(f"Config file not found: {cp}")
    cfg = read_config(cp) if cp.exists() else {"options": {}, "video": {}, "page": {}}
    if cp.exists() and args.cmd != "scan":
        say(f"Using settings from {cp.name}")
    apply_cli(args, cfg)

    if args.cmd == "scan":
        asyncio.run(scan(html, cfg))
    elif args.cmd == "render":
        asyncio.run(render(html, cfg, args.set))
    elif args.cmd == "snap":
        if args.width is None and not args.quality:
            cfg["video"]["width"] = 540
        cfg["video"]["poster"] = False
        asyncio.run(snap(html, cfg, args.set, {"times": args.times, "every": args.every, "count": args.count,
                                               "outdir": args.outdir, "prefix": args.prefix, "sheet": args.sheet,
                                               "cols": args.cols, "static": args.static}))
    else:
        if args.set:
            say("  (--set values are applied after you finish in the browser)")
        cfg["options"], controls = asyncio.run(design(html, cfg))
        save_config(cp, html, cfg, controls)
        say(f"\n  Settings saved to {cp}")
        if ask("  Render the video now? [Y/n]: ", "y").lower().startswith("y"):
            asyncio.run(render(html, cfg, args.set))


def main():
    try:
        if len(sys.argv) == 1:
            menu()
        else:
            cli(sys.argv[1:])
    except UserError as e:
        say(f"\nError: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        say("\nStopped.")
        sys.exit(130)


if __name__ == "__main__":
    main()
