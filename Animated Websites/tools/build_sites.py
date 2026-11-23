"""Builds the 88 animated invitation websites from the Wedding Invite Studio.

Run:  python "Animated Websites/tools/build_sites.py"      (from F:\\Wedding Card)

Reads   ..\\..\\wedding_invite_studio_fully_customizable.html  and  ..\\..\\studio\\samples.json
Writes  shared/engine.css, shared/engine.js, shared/config.js, NN-design-name.html (x88), index.html
Change the wedding details in WEDDING below, run this again, and every site updates.
"""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
ROOT = OUT.parent
STUDIO = ROOT / 'wedding_invite_studio_fully_customizable.html'
SAMPLES = ROOT / 'studio' / 'samples.json'

WEDDING = {
    'groom': 'Abdul Aleem',
    'bride': 'Laiba',
    'event': 'Baraat',
    'dateDisplay': 'Thursday, 31 December 2026',
    'dateShort': '31 · 12 · 2026',
    'day': 'Thu', 'dayNum': '31', 'month': 'Dec',
    'timeDisplay': '2:00 PM',
    'start': '2026-12-31T14:00:00+05:00',
    'end': '2026-12-31T17:00:00+05:00',
    'venue': 'Noor Mahal Marquee',
    'address': 'G.T Road, Islamabad',
    'mapsQuery': 'Noor Mahal Marquee, G.T Road, Islamabad',
    'closing': 'Aap ki shirkat hamare liye baais-e-musarrat hogi',
    'hostWhatsApp': '',          # family WhatsApp number, e.g. '923001234567' -> RSVPs go straight to it
}

# fallback palette used by the studio when a design does not set a colour (PAL.espresso)
ESPRESSO = {'bg': '#3B2A20', 'it': '#F3E6CC', 'ef': '#F4EAD8', 'cd': '#FBF4E6', 'ink': '#2E2018',
            'ink2': '#7A5A24', 'acc': '#B8913F', 'bl': '#9E3B3B', 'lv': '#5E6B3A'}

esc = html.escape


def slug(name):
    s = name.lower().replace('&', ' and ')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def must_replace(text, old, new, label, regex=False):
    if regex:
        out, n = re.subn(old, lambda m: new, text, count=1, flags=re.S)
    else:
        n = text.count(old)
        out = text.replace(old, new, 1)
    if n < 1:
        raise SystemExit(f'Studio patch failed ({label}): pattern not found')
    return out


def build_engine(src):
    # 1. the studio's own stylesheet (the big <style> inside <body>, with all module CSS and embedded art)
    body = src.index('<body')
    s0 = src.index('<style>', body) + len('<style>')
    s1 = src.index('</style>', s0)
    css = src[s0:s1]
    # 2. markup: everything after that stylesheet up to the main script (art library, stage, hidden editor)
    main_tag = '<script>\n'
    js0 = src.rindex('<script>')
    markup = src[s1 + len('</style>'):js0]
    js1 = src.rindex('</script>')
    js = src[js0 + len('<script>'):js1]
    fonts = re.search(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/css2[^"]+)">', src).group(1)

    if markup.count('<script') != 1:
        raise SystemExit('unexpected scripts inside studio markup')

    # couple's names (date, time and venue come from D below via fillD())
    markup = must_replace(markup, 'id="inB" value="Ayesha"', f'id="inB" value="{esc(WEDDING["bride"])}"', 'bride')
    markup = must_replace(markup, 'id="inG" value="Hamza"', f'id="inG" value="{esc(WEDDING["groom"])}"', 'groom')
    markup = must_replace(markup, 'id="inC" value="Aap ki shirkat hamare liye baais-e-musarrat hogi"',
                          f'id="inC" value="{esc(WEDDING["closing"])}"', 'closing')

    det = json.dumps({'date': WEDDING['dateDisplay'], 'time': WEDDING['timeDisplay'],
                      'venue': f"{WEDDING['venue']}, {WEDDING['address']}"}, ensure_ascii=False)
    js = must_replace(js, r'var D = \{baraat: \{.*?\}\};', f'var D = {{baraat: {det}, walima: {det}}};', 'details', regex=True)
    js = must_replace(js, "var cur = 'walima';", "var cur = 'baraat';", 'event')
    js = must_replace(js, r"var INITIAL = [^;\n]*;", "var INITIAL = '';", 'initial', regex=True)
    js = must_replace(js, "try {PRE = JSON.parse(g('preset').textContent || '{}') || {}} catch (e) {PRE = {}}",
                      "try {PRE = JSON.parse(g('preset').textContent || '{}') || {}} catch (e) {PRE = {}}\n"
                      "if (window.SITE) PRE = Object.assign({}, PRE, window.SITE);", 'preset')
    js = must_replace(js, 'applySample(Math.min(parseInt(hashN, 10) || 1, SAMPLES.length), true)',
                      'applySample(Math.min(parseInt(PRE.sample || hashN, 10) || 1, SAMPLES.length), true)', 'sample')
    js = must_replace(js, 'evButtons(); buildChips(); buildGallery(); nav(); play();',
                      'evButtons(); if (!PRE.site) {buildChips(); buildGallery();} nav(); if (!PRE.site) play();\n'
                      'window.WIS_PLAY = play;', 'start')
    js = must_replace(js, 'function saveHash(){try {', 'function saveHash(){if (window.SITE) return; try {', 'hash')
    js = must_replace(js, "if (tag === 'INPUT' || tag === 'SELECT'", "if (window.SITE) return; if (tag === 'INPUT' || tag === 'SELECT'", 'keys')

    mount = ("(function(){var m=document.getElementById('wis-mount');if(!m)return;"
             "var t=document.createElement('template');t.innerHTML=" + json.dumps(markup) + ";m.replaceWith(t.content);})();\n")
    return css, mount + js, fonts


def palette(smp):
    p = dict(ESPRESSO)
    p.update((smp.get('pal') or {}).get('baraat') or {})
    return p


ORN = ('<svg class="ornament" viewBox="0 0 150 18" aria-hidden="true"><path d="M0 9h56M94 9h56" stroke="currentColor" stroke-width=".8"/>'
       '<path d="M75 2l7 7-7 7-7-7z" fill="none" stroke="currentColor" stroke-width=".9"/><circle cx="75" cy="9" r="1.8" fill="currentColor"/>'
       '<circle cx="62" cy="9" r="1.1" fill="currentColor"/><circle cx="88" cy="9" r="1.1" fill="currentColor"/></svg>')
ICON = {
    'cal': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>',
    'dl': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 4v11m0 0l-4.5-4.5M12 15l4.5-4.5M5 19.5h14"/></svg>',
    'map': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0113 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/></svg>',
    'chat': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4.5 19.5l1.2-3.6A7.5 7.5 0 1112 19.5a7.6 7.6 0 01-3.7-1z"/></svg>',
    'share': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 15V4m0 0L8 8m4-4l4 4M5 13v5.5A1.5 1.5 0 006.5 20h11a1.5 1.5 0 001.5-1.5V13"/></svg>',
    'copy': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5.5A1.5 1.5 0 0014.5 4h-9A1.5 1.5 0 004 5.5v9A1.5 1.5 0 005.5 16H8"/></svg>',
    'replay': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 12a8 8 0 102.3-5.6M4 4v4h4"/></svg>',
    'down': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 9l6 6 6-6"/></svg>',
    'grid': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="4" y="4" width="6.5" height="6.5" rx="1"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1"/></svg>',
}


def page(n, smp, total, fonts):
    w = {k: esc(v) for k, v in WEDDING.items()}
    p = palette(smp)
    st = smp.get('set', {})
    fs = st.get('sFs') or "'Great Vibes'"
    ft = st.get('sFt') or "'Cormorant Garamond'"
    name = esc(smp['name'])
    num = f'{n:02d}'
    initials = f"{WEDDING['groom'][0]}{WEDDING['bride'][0]}"
    site = json.dumps({'site': True, 'sample': n, 'num': n, 'total': total, 'name': smp['name']}, ensure_ascii=False)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{w["groom"]} &amp; {w["bride"]} · {w["event"]} · {name}</title>
<meta name="description" content="You're invited to the {w["event"]} of {w["groom"]} &amp; {w["bride"]} — {w["dateDisplay"]}, {w["venue"]}.">
<meta name="theme-color" content="{p["bg"]}">
<meta property="og:title" content="{w["groom"]} &amp; {w["bride"]} · {w["event"]}">
<meta property="og:description" content="{w["dateDisplay"]} · {w["timeDisplay"]} · {w["venue"]}, {w["address"]}">
<meta property="og:image" content="thumbs/{num}.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}">
<link rel="stylesheet" href="shared/engine.css">
<link rel="stylesheet" href="shared/site.css">
<style>:root{{--bg:{p["bg"]};--on-bg:{p["it"]};--paper:{p["cd"]};--ink:{p["ink"]};--ink2:{p["ink2"]};--acc:{p["acc"]};--fs:{fs},'Great Vibes',cursive;--ft:{ft},'Cormorant Garamond',Georgia,serif}}</style>
<script>document.documentElement.classList.add('js')</script>
</head>
<body class="is-locked">

<div class="cover" id="cover">
  <div class="cover__inner">
    <p class="cover__bism" lang="ar">بسم الله الرحمن الرحيم</p>
    <p class="cover__eyebrow">{w["event"]} Invitation</p>
    <h1 class="cover__names">{w["groom"]}<span>&amp;</span>{w["bride"]}</h1>
    <p class="cover__date">{w["dateDisplay"]}</p>
    <p class="cover__guest" id="guestName"></p>
    <button class="seal-btn" id="openBtn" type="button" aria-label="Open the invitation"><b>{initials}</b><small>Tap to open</small></button>
  </div>
</div>

<main>
  <section class="hero" id="top" aria-label="Animated invitation">
    <div id="wis-mount"></div>
    <div class="hero__bar">
      <button class="pill" id="replay" type="button">{ICON["replay"]}Replay</button>
      <a class="pill scroll-cue" href="#invite">{ICON["down"]}Details</a>
    </div>
  </section>

  <section class="sec sec--paper" id="invite">
    <div class="wrap reveal">
      {ORN}
      <p class="eyebrow">Together with their families</p>
      <div class="couple">
        <p class="script">{w["groom"]}</p>
        <span class="couple-amp">&amp;</span>
        <p class="script">{w["bride"]}</p>
      </div>
      <p class="lead">request the pleasure of your company at their {w["event"]}</p>
      <p class="closing">{w["closing"]}</p>
    </div>
  </section>

  <section class="sec sec--rich" id="countdown">
    <div class="wrap reveal">
      <p class="eyebrow">Counting down to the {w["event"]}</p>
      <div class="count" role="timer" aria-label="Time until the {w["event"]}">
        <div><b id="cdD">00</b><span>Days</span></div>
        <div><b id="cdH">00</b><span>Hours</span></div>
        <div><b id="cdM">00</b><span>Minutes</span></div>
        <div><b id="cdS">00</b><span>Seconds</span></div>
      </div>
      <p class="muted" id="cdMsg">{w["dateDisplay"]} · {w["timeDisplay"]}</p>
    </div>
  </section>

  <section class="sec sec--paper" id="details">
    <div class="wrap reveal">
      <p class="eyebrow">The celebration</p>
      <h2 class="title">{w["event"]}</h2>
      <div class="event">
        <div class="event__date">
          <div class="tile"><small>{w["month"]}</small><b>{w["dayNum"]}</b><small>{w["day"]}</small></div>
          <div><strong>{w["dateDisplay"]}</strong><span>{w["timeDisplay"]} onwards</span></div>
        </div>
        <div class="event__venue"><strong>{w["venue"]}</strong><span class="muted">{w["address"]}</span></div>
        <div class="actions">
          <a class="btn btn--solid" id="googleCal" href="#" target="_blank" rel="noopener">{ICON["cal"]}Add to Google Calendar</a>
          <button class="btn btn--line" id="icsBtn" type="button">{ICON["dl"]}Apple · Outlook</button>
          <a class="btn btn--line" id="directions" href="#" target="_blank" rel="noopener">{ICON["map"]}Get directions</a>
        </div>
      </div>
    </div>
  </section>

  <section class="sec sec--rich" id="rsvp">
    <div class="wrap reveal">
      <p class="eyebrow">Kindly reply</p>
      <h2 class="title">Will you join us?</h2>
      <form class="form" id="rsvpForm" novalidate>
        <p class="note" id="savedNote" hidden>Your last reply is filled in. Send again if anything changed.</p>
        <div class="field"><label for="rsvpName">Your name</label><input id="rsvpName" name="name" type="text" autocomplete="name" maxlength="80" placeholder="Full name" required></div>
        <fieldset class="field"><legend>Your reply</legend>
          <div class="choices">
            <label class="choice"><input type="radio" name="attendance" value="Joyfully accepts" checked><span>Joyfully accepts</span></label>
            <label class="choice"><input type="radio" name="attendance" value="Regretfully declines"><span>Regretfully declines</span></label>
          </div>
        </fieldset>
        <div class="field" id="countField"><label for="rsvpCount">Number of guests</label>
          <select id="rsvpCount" name="guests"><option value="1">1 guest</option><option value="2">2 guests</option><option value="3">3 guests</option><option value="4">4 guests</option><option value="5">5 guests</option><option value="6">6 guests</option></select></div>
        <div class="field"><label for="rsvpMsg">A note for the couple</label><textarea id="rsvpMsg" name="message" maxlength="500" placeholder="Duas and wishes (optional)"></textarea></div>
        <button class="btn btn--solid" type="submit">{ICON["chat"]}Send RSVP on WhatsApp</button>
        <p class="note">WhatsApp opens with your reply written. Tap Send to deliver it.</p>
      </form>
    </div>
  </section>

  <section class="sec sec--paper" id="share">
    <div class="wrap reveal">
      {ORN}
      <p class="eyebrow">Share the joy</p>
      <h2 class="title">Send this invitation</h2>
      <div class="actions">
        <button class="btn btn--solid" id="shareBtn" type="button">{ICON["share"]}Share invitation</button>
        <a class="btn btn--line" id="waShare" href="#" target="_blank" rel="noopener">{ICON["chat"]}Share on WhatsApp</a>
        <button class="btn btn--line" id="copyBtn" type="button">{ICON["copy"]}Copy link</button>
      </div>
    </div>
  </section>

  <footer class="sec sec--rich foot">
    <div class="wrap">
      <p class="monogram">{initials[0]} &amp; {initials[1]}</p>
      <small>{w["dateShort"]}</small>
      <small>Design {num} of {total} · {name}</small>
      <a class="pill" href="index.html">{ICON["grid"]}All {total} designs</a>
    </div>
  </footer>
</main>

<button class="music" id="musicBtn" type="button" aria-pressed="false" aria-label="Play music" hidden>
  <svg class="on" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor"/><path d="M16 8.5a5 5 0 010 7M18.5 6a8.5 8.5 0 010 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
  <svg class="off" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor"/><path d="M16 9l5 6M21 9l-5 6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
</button>
<div class="site-toast" id="siteToast" role="status" aria-live="polite"></div>

<script>window.SITE = {site};</script>
<script src="shared/config.js"></script>
<script src="shared/engine.js"></script>
<script src="shared/site.js"></script>
</body>
</html>
'''


def gallery(samples, fonts):
    w = {k: esc(v) for k, v in WEDDING.items()}
    cats = {}
    for s in samples:
        cats[s.get('cat') or 'Other'] = cats.get(s.get('cat') or 'Other', 0) + 1
    chips = [f'<button class="chip is-on" type="button" data-cat="all">All <span>{len(samples)}</span></button>']
    chips += [f'<button class="chip" type="button" data-cat="{esc(c)}">{esc(c)} <span>{k}</span></button>' for c, k in sorted(cats.items(), key=lambda x: -x[1])]
    cards = []
    for n, s in enumerate(samples, 1):
        p = palette(s)
        num = f'{n:02d}'
        cards.append(
            f'<a class="card" href="{num}-{slug(s["name"])}.html" data-cat="{esc(s.get("cat") or "Other")}" style="--c:{p["bg"]};--a:{p["acc"]}">'
            f'<span class="thumb"><img src="thumbs/{num}.jpg" alt="" loading="{"eager" if n <= 6 else "lazy"}" width="270" height="480"></span>'
            f'<span class="meta"><span class="num">{num}</span><b>{esc(s["name"])}</b><small>{esc(s.get("cat") or "")}</small>'
            f'<span class="desc">{esc(s.get("desc") or "")}</span></span></a>')
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{w["groom"]} &amp; {w["bride"]} · {len(samples)} Invitation Websites</title>
<meta name="theme-color" content="#1c1418">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Pinyon+Script&family=Cinzel:wght@400;500&display=swap">
<style>
:root {{ --bg:#1c1418; --panel:#271c22; --line:rgba(214,182,120,.28); --gold:#d6b678; --text:#f3e9dc; --soft:#bfae9f; }}
* {{ box-sizing:border-box; }}
html {{ background:var(--bg); -webkit-text-size-adjust:100%; }}
body {{ margin:0; background:radial-gradient(120% 50% at 50% 0%, #3a2530 0%, var(--bg) 60%) no-repeat, var(--bg); color:var(--text);
  font-family:'Cormorant Garamond', Georgia, serif; font-size:18px; line-height:1.5; -webkit-font-smoothing:antialiased; }}
a {{ color:inherit; text-decoration:none; }}
:focus-visible {{ outline:2px solid var(--gold); outline-offset:3px; }}
header {{ text-align:center; padding:64px max(20px, env(safe-area-inset-right)) 28px max(20px, env(safe-area-inset-left)); display:grid; gap:10px; justify-items:center; }}
.eyebrow {{ font-family:'Cinzel', serif; font-size:12px; letter-spacing:.32em; text-transform:uppercase; color:var(--gold); margin:0; }}
h1 {{ font-family:'Pinyon Script', cursive; font-weight:400; font-size:clamp(48px, 13vw, 84px); line-height:1.05; margin:0; text-wrap:balance; }}
.sub {{ margin:0; color:var(--soft); font-size:19px; max-width:32em; }}
.chips {{ display:flex; gap:8px; flex-wrap:wrap; justify-content:center; padding:8px 16px 26px; position:sticky; top:0; z-index:5;
  background:linear-gradient(var(--bg) 70%, transparent); }}
.chip {{ font:inherit; font-size:15px; color:var(--text); background:transparent; border:1px solid var(--line); border-radius:999px;
  min-height:40px; padding:0 16px; cursor:pointer; }}
.chip span {{ color:var(--soft); font-size:13px; margin-left:4px; }}
.chip.is-on {{ background:var(--gold); color:#1c1418; border-color:var(--gold); }}
.chip.is-on span {{ color:#4a3a2a; }}
main {{ max-width:1180px; margin:0 auto; padding:0 max(16px, env(safe-area-inset-right)) 80px max(16px, env(safe-area-inset-left)); }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(min(46%, 220px), 1fr)); gap:18px 14px; }}
.card {{ display:grid; gap:10px; min-width:0; }}
.card[hidden] {{ display:none; }}
.thumb {{ position:relative; aspect-ratio:9/16; border-radius:12px; overflow:hidden; background:var(--c);
  box-shadow:0 0 0 1px var(--line), 0 20px 40px -24px #000; transition:transform .3s ease, box-shadow .3s ease; }}
.thumb img {{ width:100%; height:100%; object-fit:cover; display:block; }}
.card:hover .thumb {{ transform:translateY(-4px); box-shadow:0 0 0 1px var(--a), 0 26px 46px -24px #000; }}
.meta {{ display:grid; gap:2px; min-width:0; }}
.num {{ font-family:'Cinzel', serif; font-size:12px; letter-spacing:.2em; color:var(--gold); }}
.meta b {{ font-weight:500; font-size:20px; line-height:1.2; }}
.meta small {{ font-family:'Cinzel', serif; font-size:11px; letter-spacing:.18em; text-transform:uppercase; color:var(--soft); }}
.desc {{ font-size:15px; color:var(--soft); line-height:1.35; }}
@media (max-width:520px) {{ .desc {{ display:none; }} .meta b {{ font-size:17px; }} }}
footer {{ text-align:center; color:var(--soft); padding:0 20px calc(40px + env(safe-area-inset-bottom)); font-size:16px; }}
</style>
</head>
<body>
<header>
  <p class="eyebrow">{w["event"]} · {w["dateDisplay"]}</p>
  <h1>{w["groom"]} &amp; {w["bride"]}</h1>
  <p class="sub">{len(samples)} animated invitation websites. Tap any design to open its full website: the animation, countdown, calendar, directions and RSVP.</p>
</header>
<nav class="chips" aria-label="Filter designs">{''.join(chips)}</nav>
<main><div class="grid" id="grid">{''.join(cards)}</div></main>
<footer>{w["venue"]} · {w["address"]}</footer>
<script>
document.querySelectorAll('.chip').forEach(function (chip) {{
  chip.addEventListener('click', function () {{
    var cat = chip.getAttribute('data-cat');
    document.querySelectorAll('.chip').forEach(function (c) {{ c.classList.toggle('is-on', c === chip); }});
    document.querySelectorAll('.card').forEach(function (card) {{ card.hidden = cat !== 'all' && card.getAttribute('data-cat') !== cat; }});
  }});
}});
</script>
</body>
</html>
'''


def main():
    src = STUDIO.read_text(encoding='utf-8')
    samples = json.loads(SAMPLES.read_text(encoding='utf-8'))
    css, js, fonts = build_engine(src)
    shared = OUT / 'shared'
    shared.mkdir(parents=True, exist_ok=True)
    (shared / 'engine.css').write_text(css, encoding='utf-8')
    (shared / 'engine.js').write_text(js, encoding='utf-8')
    (shared / 'config.js').write_text('// Wedding details used by every site. Edit tools/build_sites.py and rebuild, or edit here directly.\n'
                                      'window.WEDDING = ' + json.dumps(WEDDING, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')
    for old in OUT.glob('[0-9][0-9]-*.html'):
        old.unlink()
    for n, smp in enumerate(samples, 1):
        (OUT / f'{n:02d}-{slug(smp["name"])}.html').write_text(page(n, smp, len(samples), fonts), encoding='utf-8')
    (OUT / 'index.html').write_text(gallery(samples, fonts), encoding='utf-8')
    print(f'engine.css {len(css)//1024} KB, engine.js {len(js)//1024} KB, {len(samples)} sites + gallery written to {OUT}')


if __name__ == '__main__':
    main()
