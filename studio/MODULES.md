# Wedding Invite Studio - module guide

The studio is ONE html file (`F:\Wedding Card\wedding_invite_studio_fully_customizable.html`) assembled by
`studio/build.py` from a small core plus independent **modules**. Each module is one folder:

    studio/modules/<type>/<id>/meta.json      required
                               stage.html     markup placed on the 9:16 stage        (intros, scenes, patterns, ornaments)
                               card.html      markup placed inside the card           (borders, patterns, ornaments)
                               front.html     inside the card, above the text        (ornaments that must sit on top)
                               defs.svg       <symbol>/<pattern>/<linearGradient>... (art library, any type)
                               style.css      your CSS (scoped - see rules)
                               script.js      optional JS (registration only)

`<id>`: lowercase letters, digits, dashes, e.g. `royal-curtain`. It must equal the folder name.
Write files as UTF-8 (a BOM is tolerated). Never edit core files or other modules.

## The card you are decorating

* The stage is a 9:16 box (`.st`, `#st`). It is laid out ~340-420 CSS px wide in the editor and rendered
  to video at 1080x1920 / 4K by scaling - so **size everything in `cqw`** (1cqw = 1% of the stage width) or `%`.
  Fixed px only for hairlines (1px borders). Text: script names ~13-15cqw, headings 8-10cqw, body >= 4cqw.
* Timeline of one invitation:
  `[story scenes (optional, play first)]` -> `[opening animation = intro]` -> `[the card: text animates in]` -> hold.
* The finished **card** (`.card`, z-index 6, `background: var(--cd)`) holds the text column `.in`
  (Bismillah, "Together with their families", bride, &, groom, "request the pleasure...", EVENT, date, time,
  venue, closing line). Default text box: `left/right 13%, top 14%, bottom 7%` of the card.

## Types

| type | what it is | files | shown when | editor control |
|---|---|---|---|---|
| intros | an opening animation that ends by revealing the card | stage.html, style.css, (script.js) | stage has class `s-<id>` | "Opening animation" |
| scenes | a short story scene that plays BEFORE any opening (e.g. dulha & dulhan pop-ups) | stage.html | stage has `scn-<id>` | checkbox "<name>" |
| borders | frame / border drawn on the card | card.html | `bd-<id>` | "Border" |
| patterns | subtle repeating background | stage.html (behind the opening) + card.html (on the card) | `pt-<id>` | "Background pattern" |
| ornaments | decoration you can toggle (fairy lights, toran, couple portrait...) | card.html / front.html / stage.html | `or-<id>` | checkbox "<name>" (id `kO_<id>`) |
| effects | particles falling / rising over everything | script.js + style.css | `fx-<id>` | "Falling effect" |
| art | shared SVG symbols (dulha, dulhan, flowers, domes...) used by other modules | defs.svg | always | - |
| images | a background photo | meta.json + image file | `bg-<id>` | "Background photo" |

The build wraps your markup: intros in `<div class="ix ix-<id>">`, scenes in `<div class="sc sc-<id>">`,
borders `bdx bdx-<id>`, patterns `ptx ptx-<id>`, ornaments `orx orx-<id>`. Wrappers are `position:absolute;
inset:0` boxes WITHOUT z-index (your children join the stage's / card's stacking order). Scene wrappers are the
exception: `z-index:8; opacity:0` (a scene covers everything while it plays).

### meta.json
(The `//` comments below are explanations only - real JSON files must not contain comments.)

```json
{ "name": "Royal curtains",            // shown in the editor and gallery (Title Case, no word "play")
  "desc": "Velvet curtains part ...",   // one line
  "order": 20,                          // sort position within the type (lower first)
  "t0": 5.2,                            // INTROS ONLY: seconds after the opening starts when the card is fully visible
  "dur": 6.5,                           // SCENES ONLY: scene length in seconds
  "defaults": {"sBorder": "arch", "sName": "letter", "sDet": "wipe", "sFall": "petal", "kLan": false, "kSpk": true},
                                        // INTROS ONLY: options switched on when someone picks this opening
  "fonts": ["Aref+Ruqaa:wght@400;700"]  // extra Google Fonts (css2 'family=' values) your module needs
}
```
Control ids usable in `defaults` (and in samples): `sBorder, sPat, sFall, sName (letter|slide|hand|fade),
sDet (wipe|up|slide), kLan, kSpk, kFdi, kFdo, sImg, sImgOn (stg|crd|both), rImg (10-100), sFs, sFt,
kO_<ornament-id>, kSc_<scene-id>`.

## Timing - CSS variables set on the stage

* `.play` is added to the stage when the animation runs (Replay, sample change, video render).
  **All your animations must be under `.play`**: `.play.s-<id> .x{animation: <id>-x 1.2s ease-out calc(var(--o) + 0.8s) both}`.
* `--o` = when the opening starts (seconds, includes units) = total length of the enabled story scenes. **Intros
  must offset every delay with `calc(var(--o) + Xs)`.**
* `--po` = when YOUR scene starts (set on the scene wrapper). **Scenes offset every delay with `calc(var(--po) + Xs)`.**
* `--t0` = when the card is fully revealed (= `--o` + your intro's `t0`). Card-level modules (borders, ornaments,
  patterns) animate in relative to it: `calc(var(--t0) + .3s)`. Or put `data-o="1.2"` on an element and use
  `var(--d)` - the core sets `--d = t0 + 1.2s`.
* Use `animation-fill-mode: both` so elements sit at their first keyframe before they start.
* Infinite ambient loops (twinkle, sway, float) are fine; everything else must END (the video length is the end of
  the last finite animation + a hold).
* No JS timers, `requestAnimationFrame`, `setTimeout`, transitions triggered by JS, or `Date` - videos are rendered by
  pausing and seeking CSS animations frame by frame. Plain CSS keyframes only.

### Rules per type
* **Intro**: without `.play` your elements must be invisible (`opacity:0` on your top-level pieces) so the editor shows
  the static card. You must hide the card until your reveal and then reveal it, e.g.
  `.play.s-<id> .card{animation:<id>-reveal 1.1s cubic-bezier(.2,.8,.2,1) calc(var(--o) + 4.2s) both}` (from
  `opacity:0`/clip/scale to normal) - **or** put your pieces ABOVE the card (z-index 7) and move them away, revealing it.
  The card must be completely normal (no transform/opacity/clip) by `t0`. Typical intro: 4-6.5 s, text readable for >= 1.5 s.
  Use the intro text hooks so names/event appear: "We cordially invite you to the" / `.xev` / `.xnm`.
* **Scene**: give the wrapper a life animation that STARTS and ENDS at opacity 0, e.g.
  `.play.scn-<id> .sc-<id>{animation:<id>-life <dur>s linear var(--po) both}` with
  `@keyframes <id>-life{0%{opacity:0}5%,94%{opacity:1}100%{opacity:0}}`. Draw your own full background (the scene
  covers the stage). It may be followed by ANY opening.
* **Border / pattern / ornament**: must look finished WITHOUT `.play` (gallery thumbnails and the editor show the
  static card) and animate in under `.play` with backwards fill. Never cover the text column - keep to the margins
  (top ~0-12%, bottom ~93-100%, sides ~0-12%) or adjust the text box: `.bd-<id> .in{top:17%;bottom:8%}`.
  Card ornaments go in card.html (behind the text) or front.html (above it).
* **Effect**: register a generator that fills the `.fall` overlay (z-index 7) with ~12-20 particles:
  ```js
  WIS.fx['<id>'] = function (box, c) {        // box = the empty overlay element, c = context (below)
    for (var i = 0; i < 16; i++) { var e = document.createElement('i'); e.className = '<id>-p'; ...
      e.style.animationDelay = (c.t0 + .4 + c.rand() * 4).toFixed(2) + 's'; box.appendChild(e); }
  };
  ```
  CSS: `.play.fx-<id> .<id>-p{animation:<id>-fall 7s linear infinite backwards}`. Start after `c.t0`.

## Colours (always use the variables - every design is shown in many palettes)

`--bg` scene background, `--it` text on bg, `--ef` paper / envelope / door surface, `--cd` card, `--ink` names & text
on card, `--ink2` highlight text on card, `--acc` metallic gold/silver lines, `--bl` flowers & bridal accent,
`--lv` leaves & second accent, `--skin` / `--hair` for the dulha & dulhan. Derived helpers: `--dr` (acc on bg),
`--lt` (light gold), `--p2` (pale accent). Mix freely: `color-mix(in srgb, var(--acc) 60%, #fff)`.
Never hard-code colours (pure `#000`/`#fff` with alpha for shadows/highlights is fine). Check your work on a dark
background palette AND a light one: Baraat defaults are dark (espresso), "Light ivory" theme has a light bg.

## Fonts
`var(--fs)` = the chosen script font (names); `var(--ft)` = the text font. Arabic/Urdu: `Amiri`. Need another
font? List it in meta.json `fonts` and use it by name with a fallback.

## Text hooks (the core fills them; use on any element)
`.xbn` bride name, `.xgn` groom name, `.xnm` "of Bride & Groom", `.xin` "B & G" initials, `.xm1` / `.xm2` bride /
groom initial, `.xev` event (Baraat / Walima), `.xdt` date, `.xtm` time, `.xvn` venue, `.xcl` closing line,
`.xday` day number, `.xmon` month, `.xmon3` "Dec", `.xyr` year, `.xwd` weekday.
Constant phrases you may write: "We cordially invite you to the", "Bismillah ir-Rahman ir-Rahim",
"Save the date", "Shaadi Mubarak", "Together with their families", "Insha'Allah".
SVG `<text data-fit="280" data-fs="40">` is shrunk automatically if it would be wider than 280 user units.

## JavaScript (optional, script.js)
Runs once at load, inside try/catch; only REGISTER functions, do not touch the DOM at load time:
```js
WIS.ix['<id>'] = { update: function (c) { /* rebuild dynamic parts of .ix-<id>; must be idempotent */ } };
// also WIS.sc[id], WIS.orn[id], WIS.bd[id], WIS.pt[id], and WIS.fx[id] for effects (above)
```
`c` = `{b, g, ini, b1, g1, ev, evKey, date, time, venue, cl, dp:{day,mon,mon3,year,wd}, t0, o, rand, S, state}`
(`c.S` is the stage element; find your root with `c.S.querySelector('.ix-<id>')`). `c.rand()` is random (seeded in
videos). `update` runs on every change and before every replay.

## Shared art (`studio/modules/art/*/defs.svg`)
Symbols live in one hidden `<svg><defs>`: `<symbol id="art-groom" viewBox="0 0 120 260">...</symbol>`. Use them with
`<svg class="..." viewBox="0 0 120 260"><use href="#art-groom"/></svg>`. Inside symbols colour with inline styles
(`style="fill:var(--bl)"`) - CSS variables inherit into `<use>`; CSS selectors from your module do NOT reach inside.
Animate the `<svg>`/`<use>` element, not the symbol's internals. Each art module lists its symbols in meta.json
`"symbols": [{"id": "art-groom", "viewBox": "0 0 120 260", "desc": "..."}]`.

## Naming & scoping (the build warns otherwise - fix every warning)
* Every selector contains your scope class: intros `.ix-<id>` or `.s-<id>`; scenes `.sc-<id>`/`.scn-<id>`;
  borders `.bdx-<id>`/`.bd-<id>`; patterns `.ptx-<id>`/`.pt-<id>`; ornaments `.orx-<id>`/`.or-<id>`;
  effects `.fx-<id>`; art classes start with `art-`.
* `@keyframes <id>-something`. Element ids (`<pattern id>`, gradients, clipPaths) start with `<id>-`.
* You may style core elements only through your scope: `.play.s-<id> .card{...}`, `.s-<id> .card{z-index:1}`,
  `.bd-<id> .in{...}`.

## Look & feel - the quality bar
Premium, like the best-selling invitation templates: calm composition, consistent stroke weights, gold used with
restraint, generous spacing, nothing touching the edges by accident. Motion: eased (cubic-bezier(.2,.8,.2,1),
ease-out, gentle overshoot for pops), staggered, layered depth, no jank, nothing linear except loops/particles.
Respectful Pakistani Muslim wedding culture: Mughal arches, jharokhas, domes & minarets silhouettes, lanterns, roses,
jasmine (motia), marigold (genda) for mehndi, sehra, doli, ghodi, fairy lights, crescent & stars, truck-art florals,
phulkari. No Hindu-specific religious symbols (Ganesha, om, kalash, mandap, puja diyas). Dulha & dulhan: elegant flat
"icon" style, modest clothing, minimal or no facial features.

Performance: prefer SVG and transforms/opacity; avoid animating big `filter: blur()` layers; keep a module under
~400 elements and ~40 KB.

## Build & test (PowerShell; absolute paths)
```powershell
$S = "C:\Users\Saad\AppData\Local\Temp\claude\f--Wedding-Card\eec7d3db-784a-4324-a6e3-7d20b990b41f\scratchpad\mod\<type>-<id>"
python "F:\Wedding Card\studio\build.py" --only <type>:<id> --no-images --out "$S\test.html"
# animation frames (one every 0.5 s) + contact sheet  -> open "$S\frames\sheet.png" with the Read tool
python "F:\Wedding Card\html2mp4.py" snap "$S\test.html" --set "Opening animation=<Your Name>" --every 0.5 --outdir "$S\frames"
#   scenes:     --set "<Your Scene Name>=yes"        borders: --set "Border=<Name>"        ornaments: --set "<Name>=yes"
#   patterns:   --set "Background pattern=<Name>"    effects: --set "Falling effect=<Name>"
#   palettes:   --set "Colour theme=Light ivory"  /  "Midnight cocoa"  /  "Taupe and rose gold";  --set Event=Walima
#   exact times: --times 0.5,1.2,2,3.5,end      full-size detail: --width 1080      static card: --static
```
`snap` prints the timeline (when animations end). Look at EVERY sheet you make, fix what looks wrong, repeat.
Check: legibility, alignment, overlaps with the card text, the reveal is clean, timing feels right, it works on dark
AND light palettes, Baraat AND Walima, and with a story scene before it (`--set "<scene>=yes"` once scenes exist).
