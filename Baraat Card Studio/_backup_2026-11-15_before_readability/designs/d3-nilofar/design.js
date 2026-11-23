/* D3 Nilofar - an Ohara Koson lotus woodblock seen through a cusped Mughal arch window, text set below like a gallery caption. */
registerDesign({
  id: "d3-nilofar",
  name: "Nilofar",
  idea: "A real Japanese woodblock lotus by Ohara Koson, framed in a cusped Mughal arch window traced in gold - the lotus and arch you loved, presented like a fine art print on cream cotton.",
  css: H => `
    [data-d="d3-nilofar"] { background: #f6f0e4; color: #3d2f24; }
    [data-d="d3-nilofar"] .paper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; filter: saturate(0) contrast(.42) brightness(1.5); mix-blend-mode: multiply; opacity: .42; }
    [data-d="d3-nilofar"] .win { clip-path: path('${H.archD(260, 480, 380, 680, .53, 7)}');
      background: url(${H.img("lotus-koson-pink.webp")}) no-repeat; background-size: 620px auto; background-position: 134px 100px; mix-blend-mode: multiply; filter: saturate(.92) brightness(1.05); }
    [data-d="d3-nilofar"] .winshade { clip-path: path('${H.archD(260, 480, 380, 680, .53, 7)}'); box-shadow: inset 0 0 26px rgba(60,40,20,.28); background: linear-gradient(transparent 70%, rgba(80,60,30,.08)); }
    [data-d="d3-nilofar"] .tb { left: 130px; right: 130px; top: 722px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="d3-nilofar"] .bism { font-size: calc(30px * var(--kt)); color: #7a5a26; line-height: 1.2; }
    [data-d="d3-nilofar"] .hosts { font: 500 calc(25px * var(--kt)) 'Cormorant SC', serif; letter-spacing: .12em; margin-top: 20px; }
    [data-d="d3-nilofar"] .inv { font: italic 400 calc(23px * var(--kt))/1.38 'Cormorant Garamond', serif; margin-top: 4px; color: #5a4636; }
    [data-d="d3-nilofar"] .nm { font: 400 calc(86px * var(--kn))/1.1 'Pinyon Script', cursive; white-space: nowrap; color: #8d4b5a; }
    [data-d="d3-nilofar"] .nm.g { margin-top: 18px; }
    [data-d="d3-nilofar"] .with { font: italic 400 calc(24px * var(--kt))/1 'Cormorant Garamond', serif; color: #6e5a48; margin: 0 0 2px; }
    [data-d="d3-nilofar"] .bp { font: italic 400 calc(19px * var(--kt)) 'Cormorant Garamond', serif; color: #5a4636; margin-top: 2px; }
    [data-d="d3-nilofar"] .ev { font: 500 calc(19px * var(--kt)) Cinzel, serif; letter-spacing: .5em; margin: 24px 0 0 .5em; color: #7a5a26; }
    [data-d="d3-nilofar"] .dt { font: 500 calc(23px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 12px; letter-spacing: .03em; }
    [data-d="d3-nilofar"] .vn { font: 400 calc(21px * var(--kt))/1.4 'Cormorant Garamond', serif; margin-top: 4px; color: #4b3a2c; }
    [data-d="d3-nilofar"] .vn b { font-weight: 600; }
    [data-d="d3-nilofar"] .dot { color: #b08a4a; margin: 0 .5em; }
    [data-d="d3-nilofar"] .ur { font-size: calc(16px * var(--kt)); color: #7a5a26; margin-top: 10px; }
    [data-d="d3-nilofar"] .rs { font: italic calc(17px * var(--kt)) 'Cormorant Garamond', serif; color: #5a4636; margin-top: 2px; }
  `,
  render: (H, D) => `
    <div class="layer paper"></div>
    <div class="layer win"></div>
    <div class="layer winshade"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none" stroke="url(#gold)">
        <path d="${H.archD(260, 480, 380, 680, .53, 7)}" stroke-width="2"/>
        <path d="${H.archD(245, 510, 380, 695, .53, 7)}" stroke-width=".8"/>
        <rect x="52" y="52" width="896" height="1296" stroke-width="1.2"/>
      </g>
      <g fill="url(#gold)"><circle cx="500" cy="${H.archApex(510, 380, .53) - 14}" r="3"/></g>
    </svg></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g" data-fit="700"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm" data-fit="700"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      ${H.f("event", "div", 'class="ev"')}
      <div class="dt">${H.dateLine()}<span class="dot">·</span>${H.f("time")}</div>
      <div class="vn"><b>${H.f("venue")}</b>, ${H.f("place")}</div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`,
});
