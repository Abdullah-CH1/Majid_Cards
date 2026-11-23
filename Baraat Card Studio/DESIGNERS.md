# Baraat Card Studio - designer brief and contract

## The job
Premium **static** invitation cards (5x7 portrait, 1000 x 1400 CSS px) for a Pakistani Muslim **Baraat**.
Client details are already filled in by the editor: hosts Mr. & Mrs. Col Asim · groom **Abdul Aleem** *with* bride **Laiba** ·
Thursday 31st December 2026 · 2:00 pm · Noor Mahal Marquee, G.T Road, Islamabad · Bismillah · optional Urdu line.

A previous attempt was rejected as "very bad": it used hand-drawn flat SVG flowers, cartoonish lotus shapes, toy-like
lanterns and red rose clusters. **Do not repeat that.** The client explicitly said: decent, elegant, not "shitty"; roses only rarely.

## What the client chose and why (read carefully)
Reference A (their favourite): `F:\Wedding Card\images\1.jpeg`. Reference B (also liked): `F:\Wedding Card\images\2.jpeg`. Look at both.
- **Real illustration, not clip-art.** A has softly painted, realistic watercolour lotus flowers and leaves. B has a finely
  *engraved* vintage botanical frame. Both look hand-made by an artist. Flat vector shapes look cheap next to them.
- **Quiet, warm ground.** Cream parchment with faint texture, or white cotton paper. Lots of breathing space.
- **Thin gold line-work.** A delicate cusped Mughal arch and faint gold mandala line art (corners and behind the base). Hairlines, never chunky.
- **Classic centred hierarchy.** Bismillah calligraphy → hosts → invitation line → names → date → venue. Serif plus an elegant script.
- **Restrained palette.** Cream, antique gold, dusty pink, sage green (A); white, sage, ochre-gold (B).
- **Cultural fit.** Bismillah, Mughal arch, lotus/jasmine, jaali. Dignified, not kitsch.

What the client wants now: **better, more varied options in that spirit.** Baraat can be richer (deep emerald, maroon,
midnight, black-gold), but elegance first. Every card must be readable on a phone (WhatsApp) and printable.

## Craft rules
1. **Art comes from real images.** Use the photos, paintings, borders, botanical plates and cut-outs in `assets/`
   (browse `assets/_contact_*.jpg`, read `assets/catalog.json`). Use blend modes (`mix-blend-mode: multiply` for art
   on cream; `screen` for gold on dark), masks, gradients and crops to integrate them. Your own SVG is for **hairline
   gold geometry only**: arches, rules, frames, fine mandalas, corner filigree. No hand-drawn flowers, figures or lanterns.
2. **Typography is the hero.** One script for the names (Pinyon Script, Corinthia, Ephesis, Italianno, Great Vibes,
   Monsieur La Doulaise, Mea Culpa, Rouge Script, WindSong, Imperial Script, Petit Formal Script...) plus refined serifs
   (Cormorant Garamond / SC / Upright, Cinzel, Marcellus, Bodoni Moda, Playfair, Italiana, Gilda Display, Prata, Bellefair...).
   Full list in `build.py` FONTS. Use generous tracking for caps, italic for the invitation line, and clear size steps.
3. **Contrast.** Body text must be easy to read: no gold-on-cream for small text, and no small text over busy photo areas
   (add a soft panel or gradient behind text if needed).
4. **Breathing room.** Keep 70px+ margins. Never let text touch frames or art.
5. **Gold.** Gold-foil text classes `foil foil-light` (on dark), `foil foil-deep` (on light), `foil-rose`, `foil-silver`.
   SVG gradients `url(#gold)`, `url(#goldBright)`, `url(#roseGold)`, `url(#silver)` (user space = card px) and `url(#goldB)` (bounding box).
6. **Each design is distinct** in concept, layout or palette, not a recolour of another. Give each a short evocative
   name (Urdu/Persian words welcome, e.g. "Sheesh", "Zarbaft", "Mehtab") and a one-sentence `idea` a designer could say to the client.
7. Roses: at most one of your designs may feature roses, and only delicately.

## Technical contract
Each design is a folder `designs/<id>/` with `design.js` (folder name == id, lowercase-dashes, prefix with your letter, e.g. `a3-mehtab`).
Copy the pattern from `designs/_example-paper-arch/design.js`.

```js
registerDesign({
  id: "a3-mehtab",                // == folder name
  name: "Mehtab",                 // shown in gallery
  idea: "One sentence for the client.",
  css: H => `  [data-d="a3-mehtab"] ...  `,   // ALL selectors must start with [data-d="<id>"]
  render: (H, D) => `...html...`,           // markup inside the 1000x1400 .card
});
```
- **Editable text:** every piece of wording must come from `H.f(key, tag, attrs)` (which makes it click-to-edit), e.g.
  `H.f("groom", "div", 'class="nm foil foil-deep" data-fit="620"')`. Keys: hosts, invite1, invite2, groom, joiner,
  bride, brideParents, event, day, dateNum, dateSup, month, year, time, venue, place, urdu, rsvp, monoG, monoB.
  Helpers: `H.bism(attrs)` (Bismillah glyph, honours its checkbox; size with font-size, about 11.5 x font-size wide),
  `H.urdu(attrs)` (optional Urdu line), `H.dateLine()` (Thursday, 31st December 2026 from editable parts),
  `H.when("brideParents", html)` and `H.when("rsvp", html)` (render only if filled), `H.monoG()` / `H.monoB()`.
  Must show: Bismillah, hosts, both invite lines, groom, joiner, bride, event, day+date, time, venue, place. brideParents and rsvp via `H.when`. Urdu optional.
- **Name fitting:** put `data-fit="<max px>"` on the name elements so long names shrink automatically.
- **User size sliders:** the text wrapper must have class `tb` (it gets `translate: 0 var(--dy)`). Write font sizes as
  `calc(110px * var(--kn))` for names and `calc(28px * var(--kt))` for other text.
- **Images:** only through `H.img("file.webp")` with a **literal** file name from `assets/` (the build embeds only
  literally referenced files). Use them as CSS `background-image: url(${H.img("x.webp")})` in the `css` function or as `<img src="...">`.
  **Do not use SVG `<image>`** (it breaks the in-browser download). CSS `mask-image`, `clip-path`, `mix-blend-mode`, `filter` are fine.
- Layers: use `<div class="layer">` (absolute, inset 0) for backgrounds and art; `<div class="layer"><svg viewBox="0 0 1000 1400">...</svg></div>` for gold geometry.
- Geometry helpers: `H.archD(x,w,ySpring,yBase,k=.62,lobes=7,open)` (cusped Mughal arch path), `H.archApex(w,ySpring,k)`,
  `H.pointedD(...)`, `H.ogeeD(x,w,ySpring,yBase,h)`, `H.mandala(R,{sw,stroke})` (gold line mandala at 0,0), `H.flourish(w, flip)` (inline svg divider in currentColor).
  Filters available in SVG: `url(#grain)`, `url(#mottle)` (paper texture), `url(#softshadow)`.
- Do NOT edit `core/`, `build.py`, `render.py`, or other designers' folders.

## Preview loop (do this many times)
```
cd "F:\Wedding Card\Baraat Card Studio"
python build.py --only a1-x,a2-y --out "<your scratch>\t.html"
python render.py --html "<your scratch>\t.html" --out "<your scratch>\shots" --scale 1 --sheet
```
Then **look** at every PNG with the Read tool, at full size and in the sheet. Also look at crops at `--scale 2`
for fine detail. Iterate until each card would sell on a luxury stationery shop. Compare against reference A side by side.
Fix overlaps, cramped spacing, weak contrast, awkward crops and anything that looks clip-art. `render.py` prints page errors; there must be none.
