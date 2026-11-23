/* B5 - Sang-e-Musa: black marble (the black stone of Mughal inlay), a gold cusped arch and foil type. */
registerDesign({
  id: "b5-sang-e-musa",
  name: "Sang-e-Musa",
  idea: "Polished black marble, as in the inlaid floors of Mughal palaces, with one tall gold doorway arch, a slender crescent and gold-foil lettering - dramatic, modern and very grand.",
  css: H => {
    const arch = H.pointedD(150, 700, 690, 1420, .8);
    return `
    [data-d="b5-sang-e-musa"] { background: #060606; color: #f1ebe0; }
    [data-d="b5-sang-e-musa"] .mb { background: url(${H.img("black-marble.webp")}) center 40%/cover; filter: brightness(.5) contrast(1.08) saturate(.75); }
    [data-d="b5-sang-e-musa"] .vig { background: radial-gradient(ellipse 80% 70% at 50% 50%, rgba(0,0,0,.1) 40%, rgba(0,0,0,.7) 100%); }
    [data-d="b5-sang-e-musa"] .in { position: absolute; inset: 0; clip-path: path("${arch}");
        background: radial-gradient(ellipse 70% 50% at 50% 45%, rgba(26,22,18,.9), rgba(8,7,6,.93) 80%); }
    [data-d="b5-sang-e-musa"] .tb { left: 210px; right: 210px; top: 342px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="b5-sang-e-musa"] .bism { font-size: calc(30px * var(--kt)); color: #e2c57e; }
    [data-d="b5-sang-e-musa"] .hosts { white-space: nowrap; font: 400 calc(23px * var(--kt)) Italiana, serif; letter-spacing: .24em; text-transform: uppercase; margin-top: 42px; color: #f4efe5; }
    [data-d="b5-sang-e-musa"] .inv { font: italic 400 calc(25px * var(--kt))/1.45 'Cormorant Garamond', serif; margin-top: 12px; color: #d8d0c2; }
    [data-d="b5-sang-e-musa"] .nm { font: 400 calc(112px * var(--kn))/1.15 'Imperial Script', cursive; white-space: nowrap; }
    [data-d="b5-sang-e-musa"] .nm.g { margin-top: 50px; }
    [data-d="b5-sang-e-musa"] .with { font: italic 400 calc(26px * var(--kt))/1 'Cormorant Garamond', serif; color: #e2c57e; margin: 2px 0 4px; }
    [data-d="b5-sang-e-musa"] .bp { font: italic 400 calc(21px * var(--kt)) 'Cormorant Garamond', serif; color: #d8d0c2; margin-top: 2px; }
    [data-d="b5-sang-e-musa"] .rule { width: 260px; height: 20px; margin-top: 54px; overflow: visible; }
    [data-d="b5-sang-e-musa"] .ev { font: 400 calc(27px * var(--kt)) Italiana, serif; letter-spacing: .55em; padding-left: .55em; text-transform: uppercase; margin-top: 20px; }
    [data-d="b5-sang-e-musa"] .dt { font: 400 calc(23px * var(--kt)) Prata, serif; letter-spacing: .1em; margin-top: 18px; color: #f4efe5; }
    [data-d="b5-sang-e-musa"] .vn { font: 500 calc(25px * var(--kt))/1.45 'Cormorant Garamond', serif; margin-top: 12px; color: #e2dbcf; }
    [data-d="b5-sang-e-musa"] .ur { font-size: calc(21px * var(--kt)); color: #c9bfae; margin-top: 30px; }
    [data-d="b5-sang-e-musa"] .rs { font: italic 400 calc(19px * var(--kt)) 'Cormorant Garamond', serif; color: #c9bfae; margin-top: 4px; }
  `;
  },
  render: (H, D) => `
    <div class="layer mb"></div>
    <div class="layer vig"></div>
    <div class="in"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none">
        <path d="${H.pointedD(150, 700, 690, 1420, .8, true)}" stroke="url(#goldBright)" stroke-width="2.2"/>
        <path d="${H.pointedD(163, 674, 690, 1420, .8, true)}" stroke="url(#gold)" stroke-width=".8"/>
        <path d="${H.pointedD(180, 640, 690, 1420, .8, true)}" stroke="url(#gold)" stroke-width="1.6" stroke-dasharray="0 7" stroke-linecap="round" opacity=".7"/>
      </g>
      <g fill="url(#goldBright)">
        <path d="M0,-16 A16,16 0 1,0 0,16 A21,21 0 1,1 0,-16Z" transform="translate(500 128) rotate(-90)"/>
        <rect x="499.4" y="145" width="1.2" height="26"/>
      </g>
    </svg></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts" data-fit="470"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-light" data-fit="560"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-light" data-fit="560"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <svg class="rule" viewBox="0 0 260 20"><defs><linearGradient id="b5r" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="260" y2="0"><stop offset="0" stop-color="#c9a24e" stop-opacity="0"/><stop offset=".5" stop-color="#f0d68e"/><stop offset="1" stop-color="#c9a24e" stop-opacity="0"/></linearGradient></defs><path d="M0,10 H112 M148,10 H260" stroke="url(#b5r)" stroke-width="1"/><path d="M130,2 l8,8 l-8,8 l-8,-8z" fill="none" stroke="#e2c57e" stroke-width="1"/><path d="M130,6 l4,4 l-4,4 l-4,-4z" fill="#e2c57e"/></svg>
      ${H.f("event", "div", 'class="ev foil foil-light"')}
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;&middot;&nbsp; ${H.f("venue")}<br>${H.f("place")}</div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`,
});
