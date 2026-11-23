# Round 2 – client feedback (2026-11-15): readability, bolder borders, no flowers on 1–11

Read `DESIGNERS.md` first (contract, helpers, preview loop). Its rules still apply, except where this file overrides them.

The client looked at the 25 cards on a phone and said:
1. **"Typography is very difficult to read for people with weak eyesight."** The cards go out on WhatsApp and are seen
   about 400 px wide, which is 0.4× the 1000×1400 card. Text at 22–28 px ends up as 9–11 px on the phone. Wedding guests include elderly relatives.
2. **"Your borders are very thin."** The 1–1.5 px gold hairlines disappear on a phone.
3. **Cards 1–11: remove the flowers.** See the last section.

Look at `All new designs.jpg` (the current 25) to see the problem, then make every card in your list pass the rules below.

## A. Typography rules (base sizes, with --kt = --kn = 1, on the 1000×1400 card)
| element | minimum |
|---|---|
| every piece of text, including invite lines, place, RSVP, small labels | **34 px** |
| hosts (Mr. & Mrs. Col Asim) | **42 px** |
| event word (Baraat) | **46 px** |
| date line | **42 px** |
| time, venue | **38 px** |
| Urdu line (Noto Nastaliq / Amiri) | **38 px** |
| names (script) | **130 px** before data-fit shrinks them; in serif caps **84 px** |
| joiner (with / &) | **44 px** |
| Bismillah | at least **520 px wide** (H.bism: width ≈ 11.5 × font-size) |

- Write sizes as `calc(<n>px * var(--kt))` for text and `calc(<n>px * var(--kn))` for names, as before.
- **Weight:** never 300/light. Serif body text at 500–600 (Cormorant Garamond 600, Cormorant Upright 500, EB Garamond 500,
  Lora 500, Prata, Marcellus, Playfair 500, Gilda Display). Invitation lines may be italic, but in a sturdy italic
  (EB Garamond / Lora / Cormorant 500 italic).
- **Scripts:** use sturdy, legible scripts: Great Vibes, Parisienne, Alex Brush, Allura, Rouge Script, Imperial Script, Tangerine 700.
  Do not use hairline or fussy scripts (Mea Culpa, WindSong, Monsieur La Doulaise, Ephesis, Corinthia 400, Italianno, Pinyon Script)
  for the names. Serif capitals for the names are fine where they suit the design.
- **Caps tracking** at most .16em. Line-height 1.2–1.4. No text narrower than 560 px column unless it is one short word.
- **Contrast:** every line except the names and the event word must be solid, high-contrast ink:
  dark ink (#2b1d12 / #1f2a1f / #1c2340 style) on light grounds, ivory (#f7efdc) on dark grounds, at a contrast ratio of at least 7:1.
  Gold foil (the `.foil` classes) is allowed only on names, the event word and monograms. On light grounds use `foil-deep`
  and make sure it is dark enough to read (add `filter: drop-shadow(0 1px 0 rgba(60,40,10,.25))` or use a darker solid gold such as #7a5a18).
  Never put text over busy art. Give it a solid panel.
- **Less clutter, more size:** drop decorative extras (small rules, dots, secondary ornaments) if they are what stops the text from
  being big. Hierarchy stays: Bismillah → hosts → invitation → NAMES → Baraat → date → time/venue → Urdu.
- Side-column layouts (text squeezed beside art) must be re-arranged so the text column is wide enough for the sizes above.

## B. Border / line rules
- Main frame or arch outline: **4–6 px** stroke, paired where it suits with an inner companion line of **1.5–2 px** (the classic
  foil "thick and thin" frame). It must read clearly at 0.4× size.
- Mandalas, filigree, corner ornaments, dividers: **at least 2–2.5 px** strokes, and fewer, bigger elements rather than many fine ones.
- Gold on cream must be deep enough to see (`url(#gold)` / `url(#goldB)` are fine at these widths; consider a darker stop
  or a faint dark outline). Gold on dark: `url(#goldBright)`.
- Elegant still: bold and crisp like foil stamping, not heavy or clunky.

## C. Cards 1–11 only (a1 … a5, b1 … b5, c1): NO FLOWERS
Remove every flower and floral motif: lotus, water lily, peony, lily, rose, marigold, painted floral margins, floral embroidery,
flowering trees, vines, leaves. Do **not** replace them with other flowers.
Allowed: gold Mughal arches, geometric gold mandalas/rosettes (line geometry), jaali/lattice, marble, architecture
(Taj elevation, marble jali photos), textures (handmade paper, ivory satin, emerald velvet, crimson silk, black/white marble,
gold glitter), Shah Jahan shamsa rosette and unwan cartouche (arabesque illumination, not flower pictures), crescent and stars, calligraphy,
strong typography and space. Check images in `assets/_contact_*.jpg` / `assets/catalog.json`.
Each card must still be distinct from the others and still feel premium. The freed space should go to bigger text.
Card 1 (a1) is the client's favourite look (cream, gold cusped arch, gold mandalas). Keep that look, minus the lotus, with bolder lines.
Keep each card's `name`, except where the name literally means a flower (a1 "Noor Kanwal": kanwal = lotus; give it a fitting new
Urdu/Persian name). Update `idea` to match the new design.

## D. Verify (required)
- Preview loop from DESIGNERS.md; look at every card at full size **and** shrink-test it: open the PNG and judge whether every line is
  readable at phone size (the sheet tiles are a good proxy). Check the client's text fits with no overlap and no page errors.
- Edit only your own `designs/<id>/design.js` files. Do not touch core/, build.py, render.py, or other folders.
- Video renders may be running on this PC, so be patient with render times. Use your own scratch folder for preview builds.
- Report: per card, what changed (fonts and sizes, border widths, what replaced the flowers), any new name, and anything you are unsure about.
