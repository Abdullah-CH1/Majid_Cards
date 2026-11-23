/* C3 - Nadir : a Mansur-style flower study (Mughal, c.1630) set in its own navy-and-gold album border (round 2: one wide centred column, the plant as a centrepiece between names and details) */
registerDesign({
  id: "c3-nadir",
  name: "Nadir",
  idea: "Inspired by Ustad Mansur, Nadir-ul-Asr: a real Mughal flower painting, rose-pink on buff paper, inside its original navy-and-gold album border - the names above, the flower study at the heart, the details below like a museum label.",
  css: H => {
    const P = '[data-d="c3-nadir"]';
    const s = .6, pw = 1321 * s, ph = 2000 * s, o = 20 * s;   // painting at 60%; its border's outer corner is at native 20,20
    const q = (pos, bp) => `${P} .q.${pos} { background: url(${H.img("mughal-flower-study-pink.webp")}) ${bp} / ${pw}px ${ph}px no-repeat; }`;
    /* plant crop: native x 160..1080, y 190..1250 (blooms, buds and upper leaves); its paper is colour-matched to the field (#c3wb) and feathered */
    const k = .38;
    return `
    ${P} { background: #d1b590; color: #241d2e; }
    ${P} .q { position: absolute; width: 500px; height: 700px; }
    ${P} .q.tl { left: 0; top: 0; } ${P} .q.tr { right: 0; top: 0; } ${P} .q.bl { left: 0; bottom: 0; } ${P} .q.br { right: 0; bottom: 0; }
    ${q("tl", `${-o}px ${-o}px`)}
    ${q("tr", `${-(1273 * s - 500)}px ${-o}px`)}
    ${q("bl", `${-o}px ${-(1972 * s - 700)}px`)}
    ${q("br", `${-(1273 * s - 500)}px ${-(1972 * s - 700)}px`)}
    ${P} .field { position: absolute; left: 66px; top: 66px; right: 66px; bottom: 66px; overflow: hidden;
        background: #dcc4a0 url(${H.img("mughal-flower-study-pink.webp")}) ${-140 * 2.49}px ${-130 * 2.49}px / ${1321 * 2.49}px auto no-repeat; }
    ${P} .field::before { content: ""; position: absolute; inset: 0; background: url(${H.img("textured-ivory-paper.webp")}) center/cover;
        mix-blend-mode: multiply; opacity: .2; filter: contrast(1.2); }
    ${P} .field::after { content: ""; position: absolute; inset: 0;
        background: radial-gradient(ellipse 70% 60% at 50% 48%, rgba(248,238,216,.62), rgba(248,238,216,.3) 70%, rgba(248,238,216,.1)),
                    radial-gradient(ellipse 120% 100% at 50% 50%, transparent 60%, rgba(120,85,45,.16)); }
    ${P} .plant { width: ${Math.round(920 * k)}px; height: ${Math.round(1060 * k)}px; margin: 8px 0 0; flex: none;
        background: url(${H.img("mughal-flower-study-pink.webp")}) ${-160 * k}px ${-190 * k}px / ${1321 * k}px ${2000 * k}px no-repeat;
        filter: url(#c3wb);
        -webkit-mask-image: linear-gradient(90deg, transparent, #000 9%, #000 91%, transparent), linear-gradient(180deg, transparent, #000 5%, #000 76%, transparent);
        -webkit-mask-composite: source-in;
                mask-image: linear-gradient(90deg, transparent, #000 9%, #000 91%, transparent), linear-gradient(180deg, transparent, #000 5%, #000 76%, transparent);
                mask-composite: intersect; }
    ${P} .tb:has(.bp) .plant, ${P} .tb:has(.rs) .plant { zoom: .8; }
    ${P} .tb:has(.bp):has(.rs) .plant { zoom: .56; }
    ${P} .tb { left: 110px; right: 110px; top: 112px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(48px * var(--kt)); font-weight: 700; line-height: 1.25; color: #1c2244; }
    ${P} .hosts { font: 600 calc(44px * var(--kt))/1.2 'Cormorant SC', serif; letter-spacing: .06em; margin-top: 10px; color: #241d2e; }
    ${P} .inv { font: italic 500 calc(36px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 2px; color: #241d2e; }
    ${P} .nm { font: 400 calc(132px * var(--kn))/1.02 'Rouge Script', cursive; white-space: nowrap; color: #64203b; }
    ${P} .nm.g { margin-top: 12px; }
    ${P} .with { font: italic 500 calc(46px * var(--kt))/1 'Cormorant Garamond', serif; color: #2e2232; margin: -4px 0 -2px; }
    ${P} .bp { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #241d2e; margin-top: 2px; }
    ${P} .ev { font: 600 calc(48px * var(--kt))/1 Cinzel, serif; letter-spacing: .14em; margin-right: -.14em; color: #64203b; }
    ${P} .dt { font: 600 calc(42px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 14px; color: #241d2e; }
    ${P} .vn { font: 600 calc(38px * var(--kt))/1.28 'Cormorant Garamond', serif; margin-top: 2px; color: #241d2e; }
    ${P} .dot { margin: 0 .35em; }
    ${P} .rs { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 4px; color: #241d2e; }
    ${P} .ur { font-size: calc(40px * var(--kt)); line-height: 1.75; color: #1c2244; margin-top: 2px; }
  `;
  },
  render: (H, D) => `
    <div class="q tl"></div><div class="q tr"></div><div class="q bl"></div><div class="q br"></div>
    <div class="field"></div>
    <svg width="0" height="0" style="position:absolute"><filter id="c3wb" color-interpolation-filters="sRGB"><feComponentTransfer>
      <feFuncR type="linear" slope="1.071"/><feFuncG type="linear" slope="1.133"/><feFuncB type="linear" slope="1.201"/></feComponentTransfer></filter></svg>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <rect x="66" y="66" width="868" height="1268" fill="none" stroke="#1c2244" stroke-width="5"/>
      <rect x="80" y="80" width="840" height="1240" fill="none" stroke="#8a6420" stroke-width="2"/>
      ${[[500, 33], [500, 1367], [33, 700], [967, 700]].map(([x, y]) => `<g transform="translate(${x},${y})">
        <circle r="19" fill="#1c2244" stroke="url(#goldB)" stroke-width="3"/><circle r="11" fill="none" stroke="url(#goldB)" stroke-width="2"/>
        <path d="M0,-8 L2.4,-2.4 8,0 2.4,2.4 0,8 -2.4,2.4 -8,0 -2.4,-2.4Z" fill="url(#goldB)"/></g>`).join("")}
    </svg></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g" data-fit="740"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm" data-fit="740"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="plant"></div>
      ${H.f("event", "div", 'class="ev"')}
      <div class="dt">${H.dateLine()}<span class="dot">·</span>${H.f("time")}</div>
      <div class="vn">${H.f("venue")}, ${H.f("place")}</div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`,
});
