/* C5 - Gulzar : a garden of Lucknow scrolling vines (1755) with an ivory lobed cartouche for the text */
registerDesign({
  id: "c5-gulzar",
  name: "Gulistan",
  idea: "A garden in full bloom: a real 1755 Lucknow painting of scrolling flowers wraps the card, and the words sit in a calm ivory cartouche with onion-domed ends, ruled in gold.",
  css: H => {
    const P = '[data-d="c5-gulzar"]';
    const top = H.ogeeD(150, 700, 340, 702, 150);
    const k = .87;   // two copies of the vine panel stacked (painted area native y ~62..935), the lower one mirrored and feathered in
    return `
    ${P} { background: #c9a679; color: #33231a; }
    ${P} .vine { position: absolute; left: 0; width: 1000px; height: ${Math.round(1013 * k)}px;
        background: url(${H.img("mughal-floral-vine-panel.webp")}) ${500 - 1000 * k}px 0 / ${2000 * k}px auto no-repeat;
        filter: saturate(.86) contrast(.97) brightness(1.02); }
    ${P} .vine.a { top: -70px; }
    ${P} .vine.b { top: 612px; transform: scaleX(-1);
        -webkit-mask-image: linear-gradient(180deg, transparent 70px, #000 110px);
                mask-image: linear-gradient(180deg, transparent 70px, #000 110px); }
    ${P} .veil { background: radial-gradient(ellipse 62% 54% at 50% 50%, rgba(201,166,121,.0) 40%, rgba(120,80,40,.18) 100%); }
    ${P} .halo { background: radial-gradient(ellipse 46% 46% at 50% 50%, rgba(60,30,10,.28), rgba(60,30,10,0) 70%); filter: blur(8px); }
    ${P} .win { background: #f7efdf; }
    ${P} .win.t { clip-path: path('${top}'); }
    ${P} .win.b { clip-path: path('${top}'); transform: scaleY(-1); }
    ${P} .win::before { content: ""; position: absolute; inset: 0; background: url(${H.img("textured-ivory-paper.webp")}) center/cover;
        mix-blend-mode: multiply; opacity: .28; filter: brightness(1.1) contrast(1.2); }
    ${P} .tb { left: 210px; right: 210px; top: 318px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(38px * var(--kt)); color: #8e2a1e; }
    ${P} .hosts { font: 400 calc(30px * var(--kt))/1.2 'Gilda Display', serif; letter-spacing: .08em; margin-top: 30px; color: #2e2017; }
    ${P} .inv { font: italic 400 calc(25px * var(--kt))/1.42 'Cormorant Garamond', serif; margin-top: 6px; color: #574231; }
    ${P} .nm { font: 400 calc(98px * var(--kn))/1.12 'Imperial Script', cursive; white-space: nowrap; color: #87281c; }
    ${P} .nm.g { margin-top: 32px; }
    ${P} .with { font: italic 400 calc(26px * var(--kt))/1 'Cormorant Garamond', serif; color: #3f5a35; margin: 0 0 4px; }
    ${P} .bp { font: italic 400 calc(20px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #574231; margin-top: 2px; }
    ${P} .ev { margin-top: 42px; display: flex; align-items: center; gap: 14px; }
    ${P} .ev .f { font: 500 calc(21px * var(--kt))/1 Cinzel, serif; letter-spacing: .5em; margin-right: -.5em; color: #3f5a35; }
    ${P} .ev svg { width: 64px; height: 12px; }
    ${P} .dt { font: 400 calc(23px * var(--kt))/1.3 'Gilda Display', serif; letter-spacing: .14em; text-transform: uppercase; margin-top: 18px; color: #2e2017; }
    ${P} .vn { font: 500 calc(26px * var(--kt))/1.45 'Cormorant Garamond', serif; margin-top: 8px; color: #33231a; }
    ${P} .vn .tm { font-weight: 600; }
    ${P} .rs { font: italic 400 calc(19px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 6px; color: #574231; }
    ${P} .ur { font-size: calc(22px * var(--kt)); color: #8e2a1e; margin-top: 22px; }
  `;
  },
  render: (H, D) => {
    const o = (d, sw, st, extra = "") => `<path d="${d}" fill="none" stroke="${st}" stroke-width="${sw}" ${extra}/>`;
    const both = (d, sw, st) => o(d, sw, st) + o(d, sw, st, 'transform="matrix(1 0 0 -1 0 1400)"');
    const mid = H.ogeeD(150, 700, 340, 703, 150, true), midC = H.ogeeD(150, 700, 340, 703, 150);
    const M = 'transform="matrix(1 0 0 -1 0 1400)"';
    /* parallel inner hairline: a 22px stroke masked down to its outermost 1px ring, clipped to the inside of the cartouche */
    const ring = `<path d="${mid}" fill="none" stroke="url(#gold)" stroke-width="24" mask="url(#c5ring)" clip-path="url(#c5in)"/>`;
    const leaf = flip => `<svg viewBox="0 0 64 12" style="${flip ? "transform:scaleX(-1)" : ""}"><path d="M0,6 H44" stroke="#a07a34" stroke-width="1"/><path d="M46,6 C52,0 58,1 63,6 C58,11 52,12 46,6Z" fill="#87281c"/></svg>`;
    return `
    <div class="vine a"></div><div class="vine b"></div>
    <div class="layer veil"></div>
    <div class="layer halo"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">${o(mid, 8, "#8e2a1e")}${o(mid, 8, "#8e2a1e", M)}</svg></div>
    <div class="layer win t"></div><div class="layer win b"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <defs>
        <mask id="c5ring" maskUnits="userSpaceOnUse" x="0" y="0" width="1000" height="1400"><path d="${mid}" fill="none" stroke="#fff" stroke-width="24"/><path d="${mid}" fill="none" stroke="#000" stroke-width="21.6"/></mask>
        <clipPath id="c5in"><path d="${midC}"/></clipPath>
      </defs>
      ${both(mid, 3.4, "url(#gold)")}
      ${ring}<g ${M}>${ring}</g>
      <g fill="url(#gold)">${[[500, 190], [500, 1210]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="3"/>`).join("")}</g>
    </svg></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g" data-fit="600"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm" data-fit="600"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="ev">${leaf()}${H.f("event")}${leaf(1)}</div>
      <div class="dt">${H.dateLine()}</div>
      <div class="vn"><span class="tm">${H.f("time")}</span> &nbsp;·&nbsp; ${H.f("venue")}<br>${H.f("place")}</div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`;
  },
});
