/* C5 - Gulzar (gallery: Gulistan) : a garden of Lucknow scrolling vines (1755) with a wide ivory lobed cartouche for the text (round 2: bigger cartouche, big text, bold gold rule) */
registerDesign({
  id: "c5-gulzar",
  name: "Gulistan",
  idea: "A garden in full bloom: a real 1755 Lucknow painting of scrolling flowers wraps the card, and the words sit large and clear in a calm ivory cartouche with onion-domed ends, ruled in bold gold.",
  css: H => {
    const P = '[data-d="c5-gulzar"]';
    const top = H.ogeeD(96, 808, 296, 702, 128);
    const k = .87;   // two copies of the vine panel stacked (painted area native y ~62..935), the lower one mirrored and feathered in
    return `
    ${P} { background: #c9a679; color: #2b1d12; }
    ${P} .vine { position: absolute; left: 0; width: 1000px; height: ${Math.round(1013 * k)}px;
        background: url(${H.img("mughal-floral-vine-panel.webp")}) ${500 - 1000 * k}px 0 / ${2000 * k}px auto no-repeat;
        filter: saturate(.86) contrast(.97) brightness(1.02); }
    ${P} .vine.a { top: -70px; }
    ${P} .vine.b { top: 612px; transform: scaleX(-1);
        -webkit-mask-image: linear-gradient(180deg, transparent 70px, #000 110px);
                mask-image: linear-gradient(180deg, transparent 70px, #000 110px); }
    ${P} .veil { background: radial-gradient(ellipse 62% 54% at 50% 50%, rgba(201,166,121,.0) 40%, rgba(120,80,40,.18) 100%); }
    ${P} .halo { background: radial-gradient(ellipse 50% 48% at 50% 50%, rgba(60,30,10,.3), rgba(60,30,10,0) 72%); filter: blur(8px); }
    ${P} .win { background: #f8f0e0; }
    ${P} .win.t { clip-path: path('${top}'); }
    ${P} .win.b { clip-path: path('${top}'); transform: scaleY(-1); }
    ${P} .win::before { content: ""; position: absolute; inset: 0; background: url(${H.img("textured-ivory-paper.webp")}) center/cover;
        mix-blend-mode: multiply; opacity: .2; filter: brightness(1.12) contrast(1.15); }
    ${P} .tb { left: 140px; right: 140px; top: 278px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(46px * var(--kt)); font-weight: 700; line-height: 1.25; color: #7e2216; }
    ${P} .hosts { font: 400 calc(44px * var(--kt))/1.2 'Gilda Display', serif; letter-spacing: .04em; margin-top: 12px; color: #2b1d12; }
    ${P} .inv { font: italic 500 calc(36px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 2px; color: #2b1d12; }
    ${P} .nm { font: 400 calc(130px * var(--kn))/1.08 'Imperial Script', cursive; white-space: nowrap; color: #7e2216; }
    ${P} .nm.g { margin-top: 10px; }
    ${P} .with { font: italic 500 calc(44px * var(--kt))/1 'Cormorant Garamond', serif; color: #263b20; margin: -8px 0 -4px; }
    ${P} .bp { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #2b1d12; margin-top: 2px; }
    ${P} .ev { margin-top: 14px; display: flex; align-items: center; gap: 16px; }
    ${P} .ev .f { font: 600 calc(46px * var(--kt))/1 Cinzel, serif; letter-spacing: .14em; margin-right: -.14em; color: #34502c; }
    ${P} .ev svg { width: 72px; height: 16px; }
    ${P} .dt { font: 600 calc(42px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 12px; color: #2b1d12; }
    ${P} .vn { font: 600 calc(38px * var(--kt))/1.28 'Cormorant Garamond', serif; margin-top: 2px; color: #2b1d12; }
    ${P} .vn .pl { font-size: calc(36px * var(--kt)); font-weight: 500; }
    ${P} .rs { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 4px; color: #2b1d12; }
    ${P} .ur { font-size: calc(38px * var(--kt)); line-height: 1.75; color: #7e2216; margin-top: 2px; }
  `;
  },
  render: (H, D) => {
    const o = (d, sw, st, extra = "") => `<path d="${d}" fill="none" stroke="${st}" stroke-width="${sw}" ${extra}/>`;
    const both = (d, sw, st) => o(d, sw, st) + o(d, sw, st, 'transform="matrix(1 0 0 -1 0 1400)"');
    const mid = H.ogeeD(96, 808, 296, 703, 128, true);
    const M = 'transform="matrix(1 0 0 -1 0 1400)"';
    /* inner companion line: the same outline scaled about the card centre (about 13px inside), stroke kept at 2px */
    const ring = `<path d="${mid}" fill="none" stroke="#8a6420" stroke-width="2" vector-effect="non-scaling-stroke" transform="matrix(.968 0 0 .9756 16 17.08)"/>`;
    const leaf = flip => `<svg viewBox="0 0 72 16" style="${flip ? "transform:scaleX(-1)" : ""}"><path d="M0,8 H48" stroke="#8a6420" stroke-width="2.5"/><path d="M50,8 C57,1 64,2 71,8 C64,14 57,15 50,8Z" fill="#7e2216"/></svg>`;
    return `
    <div class="vine a"></div><div class="vine b"></div>
    <div class="layer veil"></div>
    <div class="layer halo"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">${o(mid, 12, "#7e2216")}${o(mid, 12, "#7e2216", M)}</svg></div>
    <div class="layer win t"></div><div class="layer win b"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      ${both(mid, 6, "#8a6420")}
      ${both(mid, 4, "url(#gold)")}
      ${ring}<g ${M}>${ring}</g>
      <g fill="#8a6420">${[[500, 150], [500, 1250]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="5"/>`).join("")}</g>
    </svg></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g" data-fit="680"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm" data-fit="680"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="ev">${leaf()}${H.f("event")}${leaf(1)}</div>
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`;
  },
});
