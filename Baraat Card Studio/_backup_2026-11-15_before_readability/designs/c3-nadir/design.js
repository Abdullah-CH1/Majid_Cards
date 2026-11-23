/* C3 - Nadir : a Mansur-style flower study (Mughal, c.1630) set in its own navy-and-gold album border */
registerDesign({
  id: "c3-nadir",
  name: "Nadir",
  idea: "Inspired by Ustad Mansur, Nadir-ul-Asr: one real Mughal flower painting, rose-pink on buff paper, inside its original navy-and-gold border - the details sit either side of the plant like a museum label.",
  css: H => {
    const P = '[data-d="c3-nadir"]';
    const s = .6, pw = 1321 * s, ph = 2000 * s, o = 20 * s;   // painting at 60%; its border's outer corner is at native 20,20
    const q = (pos, bp) => `${P} .q.${pos} { background: url(${H.img("mughal-flower-study-pink.webp")}) ${bp} / ${pw}px ${ph}px no-repeat; }`;
    /* plant crop: native x 190..1070, y 250..1900 */
    const k = .42;
    return `
    ${P} { background: #d1b590; color: #2a2238; }
    ${P} .q { position: absolute; width: 500px; height: 700px; }
    ${P} .q.tl { left: 0; top: 0; } ${P} .q.tr { right: 0; top: 0; } ${P} .q.bl { left: 0; bottom: 0; } ${P} .q.br { right: 0; bottom: 0; }
    ${q("tl", `${-o}px ${-o}px`)}
    ${q("tr", `${-(1273 * s - 500)}px ${-o}px`)}
    ${q("bl", `${-o}px ${-(1972 * s - 700)}px`)}
    ${q("br", `${-(1273 * s - 500)}px ${-(1972 * s - 700)}px`)}
    ${P} .field { position: absolute; left: 66px; top: 66px; right: 66px; bottom: 66px; overflow: hidden;
        background: #d6bc97 url(${H.img("mughal-flower-study-pink.webp")}) ${-140 * 2.49}px ${-130 * 2.49}px / ${1321 * 2.49}px auto no-repeat; }
    ${P} .field::before { content: ""; position: absolute; inset: 0; background: url(${H.img("textured-ivory-paper.webp")}) center/cover;
        mix-blend-mode: multiply; opacity: .28; filter: contrast(1.3); }
    ${P} .field::after { content: ""; position: absolute; inset: 0;
        background: radial-gradient(ellipse 60% 34% at 50% 26%, rgba(246,234,210,.55), rgba(246,234,210,0) 80%),
                    radial-gradient(ellipse 120% 100% at 50% 50%, transparent 55%, rgba(120,85,45,.2)); }
    ${P} .plant { position: absolute; left: ${500 - 440 * k}px; bottom: 74px; width: ${880 * k}px; height: ${1650 * k}px;
        background: url(${H.img("mughal-flower-study-pink.webp")}) ${-190 * k}px ${-250 * k}px / ${1321 * k}px ${2000 * k}px no-repeat;
        filter: saturate(.95);
        -webkit-mask-image: radial-gradient(ellipse 50% 52% at 50% 50%, #000 78%, transparent 100%);
                mask-image: radial-gradient(ellipse 50% 52% at 50% 50%, #000 78%, transparent 100%); }
    ${P} .tb.main { left: 140px; right: 140px; top: 136px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(40px * var(--kt)); color: #1f2547; }
    ${P} .hosts { font: 500 calc(30px * var(--kt))/1.2 'Cormorant SC', serif; letter-spacing: .1em; margin-top: 26px; color: #241d2e; }
    ${P} .inv { font: italic 400 calc(25px * var(--kt))/1.4 'Cormorant Garamond', serif; margin-top: 6px; color: #3f3340; }
    ${P} .nm { font: 400 calc(100px * var(--kn))/1.08 Ephesis, cursive; white-space: nowrap; color: #6c2340; }
    ${P} .nm.g { margin-top: 14px; }
    ${P} .with { font: italic 400 calc(26px * var(--kt))/1 'Cormorant Garamond', serif; color: #4a3a44; margin: 0 0 2px; }
    ${P} .bp { font: italic 400 calc(20px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #4a3a44; margin-top: 2px; }
    ${P} .col { top: 900px; width: 214px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .col.l { left: 98px; } ${P} .col.r { right: 98px; }
    ${P} .ev { font: 600 calc(19px * var(--kt))/1 Cinzel, serif; letter-spacing: .42em; margin-right: -.42em; color: #6c2340; }
    ${P} .rule { width: 60px; height: 1px; background: #1f2547; opacity: .5; margin: 14px 0; }
    ${P} .day { font: 400 calc(21px * var(--kt))/1.2 Marcellus, serif; letter-spacing: .18em; text-transform: uppercase; color: #241d2e; }
    ${P} .num { font: 500 calc(64px * var(--kt))/1.05 'Cormorant Garamond', serif; color: #1f2547; margin: 4px 0 0; }
    ${P} .num { font-variant-numeric: lining-nums; }
    ${P} .my { font: 400 calc(20px * var(--kt))/1.3 Marcellus, serif; letter-spacing: .16em; text-transform: uppercase; color: #241d2e; }
    ${P} .tm { font: 600 calc(19px * var(--kt))/1 Cinzel, serif; letter-spacing: .2em; color: #6c2340; }
    ${P} .vn { font: 500 calc(27px * var(--kt))/1.25 'Cormorant Garamond', serif; color: #241d2e; }
    ${P} .pl { font: italic 400 calc(23px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #3f3340; margin-top: 6px; }
    ${P} .rs { font: italic 400 calc(18px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 8px; color: #3f3340; }
    ${P} .ur { font-size: calc(20px * var(--kt)); color: #1f2547; margin-top: 10px; line-height: 1.9; }
  `;
  },
  render: (H, D) => `
    <div class="q tl"></div><div class="q tr"></div><div class="q bl"></div><div class="q br"></div>
    <div class="field"></div>
    <div class="plant"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <rect x="84" y="84" width="832" height="1232" fill="none" stroke="#1f2547" stroke-width=".8" opacity=".55"/>
      ${[[500, 33], [500, 1367], [33, 700], [967, 700]].map(([x, y]) => `<g transform="translate(${x},${y})">
        <circle r="17" fill="#1f2547" stroke="url(#goldB)" stroke-width="2"/><circle r="11" fill="none" stroke="url(#goldB)" stroke-width="1"/>
        <path d="M0,-7 L2,-2 7,0 2,2 0,7 -2,2 -7,0 -2,-2Z" fill="url(#goldB)"/></g>`).join("")}
    </svg></div>
    <div class="tb main">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g" data-fit="700"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm" data-fit="700"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
    </div>
    <div class="tb col l">
      ${H.f("event", "div", 'class="ev"')}
      <div class="rule"></div>
      ${H.f("day", "div", 'class="day"')}
      <div class="num">${H.f("dateNum")}<sup>${H.f("dateSup")}</sup></div>
      <div class="my">${H.f("month")} ${H.f("year")}</div>
    </div>
    <div class="tb col r">
      ${H.f("time", "div", 'class="tm"')}
      <div class="rule"></div>
      ${H.f("venue", "div", 'class="vn"')}
      ${H.f("place", "div", 'class="pl"')}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`,
});
