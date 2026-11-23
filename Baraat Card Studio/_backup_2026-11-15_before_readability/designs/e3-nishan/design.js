/* E3 - Nishan: ivory satin, one tall gold-foil cusped arch, and a Didone A·L monogram as the emblem. */
registerDesign((() => {
  const ID = "e3-nishan", S = `[data-d="${ID}"]`;
  const AX = 120, AW = 760, APEX = 178, BASE = 1300, K = .62;
  const spring = (apex, w) => apex - H.archApex(w, 0, K);
  return {
    id: ID,
    name: "Nishan",
    idea: "Ivory satin and a single tall gold-foil Mughal arch, crowned by an A·L monogram in high-contrast Bodoni - modern, monogrammed and quietly regal.",
    css: H => `
      ${S} { background: #f4eee6; color: #3b3129; }
      ${S} .satin { background: url(${H.img("ivory-satin.webp")}) center / cover; filter: brightness(1.04) contrast(.9) saturate(.8); }
      ${S} .lift { background: radial-gradient(ellipse 46% 44% at 50% 55%, rgba(252,249,244,.78), rgba(252,249,244,.35) 70%, rgba(252,249,244,0) 100%); }
      ${S} .bism-t { position: absolute; left: 0; right: 0; top: 74px; text-align: center; translate: 0 var(--dy); }
      ${S} .bism { font-size: calc(34px * var(--kt)); color: #6b5226; display: inline-block; }
      ${S} .mono { position: absolute; left: 300px; width: 400px; top: 262px; height: 210px; translate: 0 var(--dy); }
      ${S} .mono .l { position: absolute; font: italic 400 calc(146px * var(--kt))/1 'Bodoni Moda', serif; }
      ${S} .mono .a { left: 108px; top: 0; }
      ${S} .mono .b { right: 100px; top: 62px; }
      ${S} .tb { left: 150px; right: 150px; top: 548px; text-align: center; display: flex; flex-direction: column; align-items: center; }
      ${S} .hosts { font: 400 calc(25px * var(--kt)) 'Gilda Display', serif; letter-spacing: .22em; padding-left: .22em; text-transform: uppercase; }
      ${S} .inv { font: italic 400 calc(25px * var(--kt))/1.42 'Cormorant Garamond', serif; margin-top: 10px; color: #4a3f35; }
      ${S} .nm { font: 400 calc(108px * var(--kn))/1.1 Corinthia, cursive; white-space: nowrap; }
      ${S} .g { margin-top: 34px; }
      ${S} .with { font: 400 calc(20px * var(--kt)) 'Gilda Display', serif; letter-spacing: .3em; text-transform: uppercase; color: #7a5e2a; margin: 0 0 2px; padding-left: .3em; }
      ${S} .bp { font: italic 400 calc(21px * var(--kt)) 'Cormorant Garamond', serif; margin-top: 4px; }
      ${S} .ev { font: italic 400 calc(30px * var(--kt)) 'Bodoni Moda', serif; margin-top: 34px; color: #6b5226; }
      ${S} .rule { width: 180px; height: 1px; margin: 20px 0 20px; background: linear-gradient(90deg, transparent, #b39352, transparent); }
      ${S} .dt { font: 400 calc(22px * var(--kt)) 'Gilda Display', serif; letter-spacing: .16em; text-transform: uppercase; }
      ${S} .vn { font: 500 calc(25px * var(--kt))/1.45 'Cormorant Garamond', serif; margin-top: 8px; }
      ${S} .ur { font-size: calc(20px * var(--kt)); color: #6b5226; margin-top: 16px; }
      ${S} .rs { font: 400 calc(17px * var(--kt)) 'Gilda Display', serif; letter-spacing: .2em; margin-top: 4px; color: #6b5226; }
    `,
    render: (H, D) => {
      const arch = (o, sw, op) => { const w = AW + 2 * o; return `<path d="${H.archD(AX - o, w, spring(APEX - o, w), BASE + o, K, 9)}" fill="none" stroke="url(#gold)" stroke-width="${sw}" opacity="${op}"/>`; };
      return `
      <div class="layer satin"></div>
      <div class="layer lift"></div>
      <div class="layer"><svg viewBox="0 0 1000 1400">
        ${arch(0, 3.2, 1)}${arch(-11, 1, .85)}${arch(12, .8, .7)}
        <g transform="translate(500 ${APEX - 26})"><path d="M0,-14 L5,0 L0,14 L-5,0Z" fill="url(#gold)"/></g>
        <path d="M420,492 H480 M520,492 H580" stroke="url(#gold)" stroke-width="1"/><path d="M500,485 L506,492 L500,499 L494,492Z" fill="url(#gold)"/>
      </svg></div>
      <div class="bism-t">${H.bism()}</div>
      <div class="mono"><span class="l a foil foil-deep">${H.monoG()}</span><span class="l b foil foil-deep">${H.monoB()}</span></div>
      <div class="tb">
        ${H.f("hosts", "div", 'class="hosts"')}
        <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
        ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="640"')}
        ${H.f("joiner", "div", 'class="with"')}
        ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="640"')}
        ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
        ${H.f("event", "div", 'class="ev"')}
        <div class="rule"></div>
        <div class="dt">${H.dateLine()}</div>
        <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br>${H.f("place")}</div>
        ${H.urdu()}
        ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      </div>`;
    },
  };
})());
