/* D4 Sosan - Koson's lily key-block drawing, printed in gold, leaning in from the top right of a deep emerald card. */
registerDesign({
  id: "d4-sosan",
  name: "Sosan",
  idea: "Ohara Koson's original lily drawing printed in gold line, leaning in from the top right of a deep emerald card above large, clear ivory wording and gold-foil names - a quiet, evening-rich Baraat card.",
  css: H => `
    [data-d="d4-sosan"] { background: #0f2620; color: #f7efdc; }
    [data-d="d4-sosan"] .bg { background: radial-gradient(ellipse 70% 60% at 34% 56%, #1a3a30 0%, #11291f 55%, #0a1c16 100%); }
    [data-d="d4-sosan"] .lily { position: absolute; left: 486px; top: -64px; width: 750px; height: 1250px;
      background: url(${H.img("lily-line-drawing-gold-cut.png")}) center/100% 100% no-repeat;
      filter: brightness(1.18) saturate(1.05) drop-shadow(0 0 .6px #e8c979); opacity: 1;
      -webkit-mask-image: linear-gradient(#000 0%, #000 70%, transparent 97%); mask-image: linear-gradient(#000 0%, #000 70%, transparent 97%); }
    [data-d="d4-sosan"] .tb { left: 108px; width: 572px; top: 384px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="d4-sosan"] .bism { font-size: calc(48px * var(--kt)); line-height: 1.25; color: #f3e6c4; }
    [data-d="d4-sosan"] .hosts { font: 600 calc(44px * var(--kt))/1.2 'Cormorant SC', serif; letter-spacing: .05em; margin-top: 20px; }
    [data-d="d4-sosan"] .inv { font: italic 500 calc(36px * var(--kt))/1.28 'Cormorant Garamond', serif; margin-top: 4px; }
    [data-d="d4-sosan"] .nm { font: 400 calc(138px * var(--kn))/1.08 'Alex Brush', cursive; white-space: nowrap; }
    [data-d="d4-sosan"] .nm.g { margin-top: 22px; }
    [data-d="d4-sosan"] .with { font: italic 500 calc(46px * var(--kt))/1 'Cormorant Garamond', serif; margin: -4px 0 0; }
    [data-d="d4-sosan"] .bp { font: italic 500 calc(34px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 2px; }
    [data-d="d4-sosan"] .ev { font: 600 calc(50px * var(--kt))/1.2 Cinzel, serif; letter-spacing: .14em; padding-left: .14em; margin-top: 30px; }
    [data-d="d4-sosan"] .dt { font: 600 calc(44px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 4px; }
    [data-d="d4-sosan"] .vn { font: 600 calc(40px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 4px; }
    [data-d="d4-sosan"] .vn .pl { font-weight: 500; font-size: calc(38px * var(--kt)); }
    [data-d="d4-sosan"] .ur { font-size: calc(38px * var(--kt)); line-height: 1.9; white-space: nowrap; color: #f7efdc; margin-top: 2px; }
    [data-d="d4-sosan"] .rs { font: italic 500 calc(34px * var(--kt)) 'Cormorant Garamond', serif; margin-top: 0; }
  `,
  render: (H, D) => `
    <div class="layer bg"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400"><rect width="1000" height="1400" filter="url(#grain)" opacity=".22"/><rect width="1000" height="1400" filter="url(#mottle)" opacity=".18"/></svg></div>
    <div class="lily"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none" stroke="url(#goldBright)">
        <rect x="38" y="38" width="924" height="1324" stroke-width="5"/>
        <rect x="54" y="54" width="892" height="1292" stroke-width="1.8"/>
      </g>
    </svg></div>
    <div class="tb">
      ${H.bism('class="bism"')}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-light" data-fit="572"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-light" data-fit="572"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      ${H.f("event", "div", 'class="ev foil foil-light"')}
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`,
});
