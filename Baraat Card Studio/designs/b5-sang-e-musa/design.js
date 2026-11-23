/* B5 - Sang-e-Musa: black marble (the black stone of Mughal inlay), one tall bold gold doorway arch, crescent and foil type. */
registerDesign({
  id: "b5-sang-e-musa",
  name: "Sang-e-Musa",
  idea: "Polished black marble, as in the inlaid floors of Mughal palaces, with one tall gold doorway arch in thick-and-thin foil, a crescent at its crown and bold ivory lettering - dramatic, modern and very grand.",
  css: H => {
    const P = '[data-d="b5-sang-e-musa"]';
    const arch = H.pointedD(96, 808, 640, 1460, .62);
    return `
    ${P} { background: #060606; color: #f7efdc; }
    ${P} .mb { background: url(${H.img("black-marble.webp")}) center 40%/cover; filter: brightness(.55) contrast(1.1) saturate(.7); }
    ${P} .vig { background: radial-gradient(ellipse 80% 70% at 50% 50%, rgba(0,0,0,.05) 40%, rgba(0,0,0,.7) 100%); }
    ${P} .in { position: absolute; inset: 0; clip-path: path("${arch}");
        background: radial-gradient(ellipse 70% 50% at 50% 45%, rgba(24,21,17,.95), rgba(7,6,5,.97) 80%); }
    ${P} .tb { left: 130px; right: 130px; top: calc(330px - 8px * var(--x, 0)); text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(48px * var(--kt)); line-height: 1.2; color: #f1d98f; }
    ${P} .hosts { white-space: nowrap; font: 500 calc(44px * var(--kt))/1.2 Cinzel, serif; letter-spacing: .07em; margin-top: 28px; color: #f7efdc; }
    ${P} .inv { font: italic 500 calc(39px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 10px; color: #f7efdc; }
    ${P} .nm { font: 400 calc(138px * var(--kn) * (1 - .03 * var(--x, 0)))/1.1 'Imperial Script', cursive; white-space: nowrap;
        filter: drop-shadow(0 2px 0 rgba(0,0,0,.6)); }
    ${P} .nm.g { margin-top: calc(22px - 8px * var(--x, 0)); }
    ${P} .with { font: italic 500 calc(46px * var(--kt))/1 'Cormorant Garamond', serif; color: #f1d98f; margin: -6px 0 -2px; }
    ${P} .bp { font: italic 500 calc(34px * var(--kt))/1.25 'Cormorant Garamond', serif; color: #f7efdc; margin-top: 4px; }
    ${P} .rule { width: 340px; height: 24px; margin-top: calc(22px - 10px * var(--x, 0)); overflow: visible; }
    ${P} .ev { font: 600 calc(52px * var(--kt))/1.1 Cinzel, serif; letter-spacing: .16em; padding-left: .16em; text-transform: uppercase; margin-top: calc(12px - 4px * var(--x, 0)); }
    ${P} .dt { font: 400 calc(43px * var(--kt))/1.25 Prata, serif; letter-spacing: 0; margin-top: calc(12px - 4px * var(--x, 0)); color: #f7efdc; white-space: nowrap; }
    ${P} .vn { font: 600 calc(42px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 8px; color: #f7efdc; }
    ${P} .vn .pl { font-size: .92em; }
    ${P} .ur { font-size: calc(40px * var(--kt)); line-height: calc(1.9 - .2 * var(--x, 0)); color: #f7efdc; margin-top: calc(6px - 4px * var(--x, 0)); }
    ${P} .rs { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #f7efdc; margin-top: 4px; }
  `;
  },
  render: (H, D) => `
    <div class="layer mb"></div>
    <div class="layer vig"></div>
    <div class="in"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none">
        <path d="${H.pointedD(96, 808, 640, 1460, .62, true)}" stroke="url(#goldBright)" stroke-width="5.5"/>
        <path d="${H.pointedD(112, 776, 640, 1460, .62, true)}" stroke="url(#goldBright)" stroke-width="2"/>
      </g>
      <g fill="url(#goldBright)">
        <path d="M0,-24 A24,24 0 1,0 0,24 A31,31 0 1,1 0,-24Z" transform="translate(500 92) rotate(-90)"/>
        <path d="M500,121 l7,15 l-7,15 l-7,-15z"/>
      </g>
    </svg></div>
    <div class="tb" style="--x:${(H.has("brideParents") ? 1 : 0) + (H.has("rsvp") ? 1 : 0)}">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts" data-fit="600"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-light" data-fit="680"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-light" data-fit="680"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <svg class="rule" viewBox="0 0 340 24"><defs><linearGradient id="b5r" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="340" y2="0"><stop offset="0" stop-color="#c9a24e" stop-opacity="0"/><stop offset=".5" stop-color="#f3dc96"/><stop offset="1" stop-color="#c9a24e" stop-opacity="0"/></linearGradient></defs><path d="M0,12 H146 M194,12 H340" stroke="url(#b5r)" stroke-width="2.5"/><path d="M170,1 l11,11 l-11,11 l-11,-11z" fill="none" stroke="#f1d98f" stroke-width="2.5"/><path d="M170,7 l5,5 l-5,5 l-5,-5z" fill="#f1d98f"/></svg>
      ${H.f("event", "div", 'class="ev foil foil-light"')}
      <div class="dt" data-fit="700">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;&middot;&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`,
});
