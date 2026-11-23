/* E3 - Nishan: ivory satin, one tall gold-foil cusped arch, and a Didone A·L monogram as the emblem. */
registerDesign((() => {
  const ID = "e3-nishan", S = `[data-d="${ID}"]`;
  const AX = 110, AW = 780, APEX = 172, BASE = 1328, K = .62;
  const spring = (apex, w) => apex - H.archApex(w, 0, K);
  return {
    id: ID,
    name: "Nishan",
    idea: "Ivory satin and a single tall gold-foil Mughal arch, crowned by an A·L monogram in high-contrast Bodoni - modern, monogrammed and quietly regal, with large, clear wording.",
    css: H => `
      ${S} { background: #f4eee6; color: #2b1d12; }
      ${S} .satin { background: url(${H.img("ivory-satin.webp")}) center / cover; filter: brightness(1.04) contrast(.9) saturate(.8); }
      ${S} .lift { background: radial-gradient(ellipse 50% 50% at 50% 56%, rgba(252,249,244,.9), rgba(252,249,244,.6) 70%, rgba(252,249,244,.1) 100%); }
      ${S} .bism-t { position: absolute; left: 0; right: 0; top: 52px; text-align: center; translate: 0 var(--dy); }
      ${S} .bism { font-size: calc(48px * var(--kt)); color: #3e2a10; display: inline-block; line-height: 1.2; }
      ${S} .mono { position: absolute; left: 340px; width: 320px; top: 200px; height: 170px; translate: 0 var(--dy); }
      ${S} .mono .l { position: absolute; font: italic 500 calc(124px * var(--kt))/1 'Bodoni Moda', serif; filter: drop-shadow(0 1px 0 rgba(60,40,10,.3)); }
      ${S} .mono .a { left: 78px; top: 0; }
      ${S} .mono .b { right: 72px; top: 48px; }
      ${S} .tb { left: 140px; right: 140px; top: 404px; text-align: center; display: flex; flex-direction: column; align-items: center; }
      ${S} .hosts { font: 400 calc(44px * var(--kt))/1.2 'Gilda Display', serif; letter-spacing: .04em; }
      ${S} .inv { font: italic 500 calc(37px * var(--kt))/1.26 'Cormorant Garamond', serif; margin-top: 6px; }
      ${S} .nm { font: 400 calc(140px * var(--kn))/1.04 Allura, cursive; white-space: nowrap; filter: drop-shadow(0 1px 0 rgba(60,40,10,.3)); }
      ${S} .g { margin-top: 30px; }
      ${S} .with { font: 400 calc(44px * var(--kt))/1 'Gilda Display', serif; letter-spacing: .14em; text-transform: uppercase; color: #5a3e10; margin: 0; padding-left: .14em; }
      ${S} .bp { font: italic 500 calc(36px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 4px; }
      ${S} .ev { font: italic 500 calc(54px * var(--kt))/1.15 'Bodoni Moda', serif; margin-top: 30px; filter: drop-shadow(0 1px 0 rgba(60,40,10,.3)); }
      ${S} .dt { font: 400 calc(42px * var(--kt))/1.25 'Gilda Display', serif; margin-top: 10px; }
      ${S} .vn { font: 600 calc(40px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 6px; }
      ${S} .vn .p { font-weight: 500; font-size: calc(38px * var(--kt)); }
      ${S} .ur { font-size: calc(38px * var(--kt)); line-height: 1.8; white-space: nowrap; color: #2b1d12; margin-top: 0; }
      ${S} .rs { font: italic 500 calc(34px * var(--kt)) 'Cormorant Garamond', serif; margin-top: 0; }
    `,
    render: (H, D) => {
      const arch = (o, sw, op, st = "url(#gold)") => { const w = AW + 2 * o; return `<path d="${H.archD(AX - o, w, spring(APEX - o, w), BASE + o, K, 9)}" fill="none" stroke="${st}" stroke-width="${sw}" opacity="${op}"/>`; };
      return `
      <div class="layer satin"></div>
      <div class="layer lift"></div>
      <div class="layer"><svg viewBox="0 0 1000 1400">
        ${arch(0, 6.6, .32, "#6b4c14")}${arch(-14, 2.8, .25, "#6b4c14")}${arch(0, 5, 1)}${arch(-14, 1.8, 1)}
        <g transform="translate(500 ${APEX - 22})"><path d="M0,-16 L7,0 L0,16 L-7,0Z" fill="url(#gold)"/></g>
      </svg></div>
      <div class="bism-t">${H.bism()}</div>
      <div class="mono"><span class="l a foil foil-deep">${H.monoG()}</span><span class="l b foil foil-deep">${H.monoB()}</span></div>
      <div class="tb">
        ${H.f("hosts", "div", 'class="hosts"')}
        <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
        ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="680"')}
        ${H.f("joiner", "div", 'class="with"')}
        ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="680"')}
        ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
        ${H.f("event", "div", 'class="ev foil foil-deep"')}
        <div class="dt">${H.dateLine()}</div>
        <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="p">${H.f("place")}</span></div>
        ${H.urdu()}
        ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      </div>`;
    },
  };
})());
