/* D3 Nilofar - an Ohara Koson lotus woodblock seen through a cusped Mughal arch window, text set below like a gallery caption (round 2: compact window, big solid text, bold gold arch and frame) */
registerDesign({
  id: "d3-nilofar",
  name: "Nilofar",
  idea: "A real Japanese woodblock lotus by Ohara Koson, framed in a cusped Mughal arch window traced in bold gold - the lotus and arch you loved, presented like a fine art print on cream cotton with a large, clear caption.",
  css: H => {
    const P = '[data-d="d3-nilofar"]';
    const W = H.archD(310, 380, 310, 494, .53, 7);
    return `
    ${P} { background: #f6f0e4; color: #2b1d12; }
    ${P} .paper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; filter: saturate(0) contrast(.42) brightness(1.5); mix-blend-mode: multiply; opacity: .42; }
    ${P} .win { clip-path: path('${W}');
      background: url(${H.img("lotus-koson-pink.webp")}) no-repeat; background-size: 520px auto; background-position: 200px 86px; mix-blend-mode: multiply; filter: saturate(.95) brightness(1.04); }
    ${P} .winshade { clip-path: path('${W}'); box-shadow: inset 0 0 22px rgba(60,40,20,.28); background: linear-gradient(transparent 70%, rgba(80,60,30,.08)); }
    ${P} .tb { left: 100px; right: 100px; top: 536px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(46px * var(--kt)); font-weight: 700; color: #6a4c1c; line-height: 1.25; }
    ${P} .hosts { font: 600 calc(42px * var(--kt))/1.2 'Cormorant SC', serif; letter-spacing: .06em; margin-top: 8px; }
    ${P} .inv { font: italic 500 calc(35px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 2px; color: #2b1d12; }
    ${P} .nm { font: 400 calc(130px * var(--kn))/1.06 'Allura', cursive; white-space: nowrap; color: #7e3a4a; }
    ${P} .nm.g { margin-top: 8px; }
    ${P} .with { font: italic 500 calc(44px * var(--kt))/1 'Cormorant Garamond', serif; color: #3a2a1e; margin: -8px 0 -6px; }
    ${P} .bp { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #2b1d12; margin-top: 2px; }
    ${P} .ev { font: 600 calc(46px * var(--kt))/1 Cinzel, serif; letter-spacing: .14em; margin: 14px 0 0 .14em; color: #6a4c1c; }
    ${P} .dt { font: 600 calc(42px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 12px; }
    ${P} .vn { font: 600 calc(38px * var(--kt))/1.28 'Cormorant Garamond', serif; margin-top: 2px; color: #2b1d12; }
    ${P} .vn .pl { font-weight: 500; }
    ${P} .dot { margin: 0 .35em; }
    ${P} .ur { font-size: calc(38px * var(--kt)); line-height: 1.75; color: #5e4218; margin-top: 2px; }
    ${P} .rs { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #2b1d12; margin-top: 2px; }
  `;
  },
  render: (H, D) => `
    <div class="layer paper"></div>
    <div class="layer win"></div>
    <div class="layer winshade"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none">
        <path d="${H.archD(310, 380, 310, 494, .53, 7)}" stroke="#8a6420" stroke-width="5"/>
        <path d="${H.archD(310, 380, 310, 494, .53, 7)}" stroke="url(#gold)" stroke-width="3"/>
        <path d="${H.archD(296, 408, 310, 508, .53, 7)}" stroke="#8a6420" stroke-width="2"/>
        <rect x="46" y="46" width="908" height="1308" stroke="#8a6420" stroke-width="5"/>
        <rect x="46" y="46" width="908" height="1308" stroke="url(#gold)" stroke-width="3"/>
        <rect x="60" y="60" width="880" height="1280" stroke="#8a6420" stroke-width="2"/>
      </g>
      <g fill="#8a6420"><circle cx="500" cy="${H.archApex(408, 310, .53) - 14}" r="5"/></g>
    </svg></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g" data-fit="760"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm" data-fit="760"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      ${H.f("event", "div", 'class="ev"')}
      <div class="dt">${H.dateLine()}<span class="dot">·</span>${H.f("time")}</div>
      <div class="vn">${H.f("venue")}, <span class="pl">${H.f("place")}</span></div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`,
});
