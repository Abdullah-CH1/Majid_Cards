/* D1 Gulzar - the client's sage engraved frame (Reference B), refined for the Baraat with a gold Mughal arch inside (round 2: frame enlarged to open up a wide text column, big deep-sage text, bold gold arch) */
registerDesign({
  id: "d1-gulzar",
  name: "Gulzar",
  idea: "A vintage sage-green engraved garden frame on white cotton paper, with a bold gold Mughal arch inside and the names in warm ochre script - your favourite sage card, made clear and generous for the Baraat.",
  css: H => {
    const P = '[data-d="d1-gulzar"]';
    /* frame scaled so its opening (native x 257..1160, y 318..1614) is centred and wide */
    const fx = .77, fy = .84, fl = Math.round(500 - 708 * fx), ft = Math.round(700 - 966 * fy);
    return `
    ${P} { background: #fcfbf7; color: #1f2a1f; }
    ${P} .paper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; filter: saturate(.3) contrast(.55) brightness(1.5); mix-blend-mode: multiply; opacity: .9; }
    ${P} .frame { position: absolute; left: ${fl}px; top: ${ft}px; width: ${Math.round(1391 * fx)}px; height: ${Math.round(1960 * fy)}px;
        background: url(${H.img("engraved-floral-frame-sage-cut.png")}) center/100% 100% no-repeat; filter: saturate(1.3) brightness(.86) contrast(1.1); }
    ${P} .glow { background: radial-gradient(ellipse 36% 40% at 50% 50%, rgba(255,255,254,.85), rgba(255,255,254,0) 100%); }
    ${P} .tb { left: 190px; right: 190px; top: 350px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(46px * var(--kt)); font-weight: 700; color: #7c5618; line-height: 1.25; }
    ${P} .hosts { font: 600 calc(42px * var(--kt))/1.2 'Cormorant SC', serif; letter-spacing: .05em; margin-top: 8px; color: #1f2a1f; white-space: nowrap; }
    ${P} .inv { font: italic 500 calc(34px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 2px; color: #1f2a1f; white-space: nowrap; }
    ${P} .nm { font: 400 calc(130px * var(--kn))/1.06 'Parisienne', cursive; white-space: nowrap; color: #84591a; }
    ${P} .nm.g { margin-top: 8px; }
    ${P} .with { font: italic 500 calc(44px * var(--kt))/1 'Cormorant Garamond', serif; color: #2c3a2a; margin: -6px 0 -4px; }
    ${P} .bp { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #1f2a1f; margin-top: 2px; }
    ${P} .ev { font: 600 calc(46px * var(--kt))/1 Cinzel, serif; letter-spacing: .14em; margin: 16px 0 0 .14em; color: #33502e; }
    ${P} .dt { font: 600 calc(42px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 10px; color: #1f2a1f; white-space: nowrap; }
    ${P} .vn { font: 600 calc(38px * var(--kt))/1.28 'Cormorant Garamond', serif; margin-top: 2px; color: #1f2a1f; white-space: nowrap; }
    ${P} .vn .pl { font-size: calc(36px * var(--kt)); font-weight: 500; }
    ${P} .ur { font-size: calc(38px * var(--kt)); line-height: 1.75; color: #6e4c14; margin-top: 2px; max-width: 480px; text-wrap: balance; }
    ${P} .tb:has(.bp) .ur, ${P} .tb:has(.rs) .ur { max-width: none; white-space: nowrap; }
    ${P} .tb:has(.bp):has(.rs) .nm { line-height: .98; }
    ${P} .rs { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #1f2a1f; margin-top: 2px; }
  `;
  },
  render: (H, D) => {
    const A = [172, 656, 536, 1222], apex = H.archApex(A[1], A[2], .53);
    return `
    <div class="layer paper"></div>
    <div class="frame"></div>
    <div class="layer glow"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none">
        <path d="${H.archD(A[0], A[1], A[2], A[3], .53, 7)}" stroke="#8a6420" stroke-width="5"/>
        <path d="${H.archD(A[0], A[1], A[2], A[3], .53, 7)}" stroke="url(#gold)" stroke-width="3"/>
        <path d="${H.archD(A[0] + 11, A[1] - 22, A[2], A[3] - 11, .53, 7)}" stroke="#8a6420" stroke-width="2"/>
      </g>
      <g fill="#8a6420"><circle cx="500" cy="${apex - 16}" r="5"/></g>
    </svg></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g" data-fit="560"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm" data-fit="560"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      ${H.f("event", "div", 'class="ev"')}
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`;
  },
});
