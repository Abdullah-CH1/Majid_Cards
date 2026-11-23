/* D4 Sosan - Koson's lily key-block drawing, printed in gold, climbing the right side of a deep emerald card. */
registerDesign({
  id: "d4-sosan",
  name: "Sosan",
  idea: "Ohara Koson's original lily drawing printed in fine gold line, climbing up one side of a deep emerald card - a quiet, evening-rich Baraat card with gold-foil names.",
  css: H => `
    [data-d="d4-sosan"] { background: #0f2620; color: #ece2cc; }
    [data-d="d4-sosan"] .bg { background: radial-gradient(ellipse 70% 60% at 34% 46%, #1a3a30 0%, #11291f 55%, #0a1c16 100%); }
    [data-d="d4-sosan"] .clip { position: absolute; inset: 54px; overflow: hidden; }
    [data-d="d4-sosan"] .lily { position: absolute; left: 318px; top: -24px; width: 904px; height: 1424px;
      background: url(${H.img("lily-line-drawing-gold-cut.png")}) center/100% 100% no-repeat;
      filter: brightness(1.12) saturate(1.05); opacity: .95; }
    [data-d="d4-sosan"] .tb { left: 84px; width: 420px; top: 520px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="d4-sosan"] .bism { font-size: calc(32px * var(--kt)); line-height: 1.25; }
    [data-d="d4-sosan"] .hosts { font: 500 calc(26px * var(--kt)) 'Cormorant SC', serif; letter-spacing: .12em; margin-top: 30px; color: #f2e9d6; }
    [data-d="d4-sosan"] .inv { font: italic 400 calc(24px * var(--kt))/1.42 'Cormorant Garamond', serif; margin-top: 8px; color: #d9cdb3; }
    [data-d="d4-sosan"] .nm { font: 400 calc(104px * var(--kn))/1.12 'Corinthia', cursive; white-space: nowrap; }
    [data-d="d4-sosan"] .nm.g { margin-top: 26px; }
    [data-d="d4-sosan"] .with { font: italic 400 calc(26px * var(--kt))/1 'Cormorant Garamond', serif; color: #d9cdb3; margin: -2px 0 2px; }
    [data-d="d4-sosan"] .bp { font: italic 400 calc(20px * var(--kt)) 'Cormorant Garamond', serif; color: #d9cdb3; margin-top: 4px; }
    [data-d="d4-sosan"] .rule { width: 220px; height: 14px; margin-top: 28px; }
    [data-d="d4-sosan"] .ev { font: 500 calc(21px * var(--kt)) Cinzel, serif; letter-spacing: .5em; margin: 16px 0 0 .5em; color: #d8b866; }
    [data-d="d4-sosan"] .dt { font: 400 calc(25px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 14px; letter-spacing: .03em; color: #f2e9d6; font-weight: 500; }
    [data-d="d4-sosan"] .tm { font: 400 calc(18px * var(--kt)) Marcellus, serif; letter-spacing: .24em; text-transform: uppercase; margin-top: 10px; color: #d9cdb3; }
    [data-d="d4-sosan"] .vn { font: 500 calc(23px * var(--kt))/1.4 'Cormorant Garamond', serif; margin-top: 14px; color: #f2e9d6; }
    [data-d="d4-sosan"] .vn .pl { font-weight: 400; color: #d9cdb3; }
    [data-d="d4-sosan"] .ur { font-size: calc(17px * var(--kt)); color: #d8b866; margin-top: 10px; }
    [data-d="d4-sosan"] .rs { font: italic calc(17px * var(--kt)) 'Cormorant Garamond', serif; color: #d9cdb3; margin-top: 4px; }
  `,
  render: (H, D) => `
    <div class="layer bg"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400"><rect width="1000" height="1400" filter="url(#grain)" opacity=".22"/><rect width="1000" height="1400" filter="url(#mottle)" opacity=".18"/></svg></div>
    <div class="lily"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none" stroke="url(#goldBright)">
        <rect x="44" y="44" width="912" height="1312" stroke-width="1.4"/>
        <rect x="54" y="54" width="892" height="1292" stroke-width=".6" opacity=".7"/>
      </g>
    </svg></div>
    <div class="tb">
      ${H.bism('class="bism foil foil-light"')}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-light" data-fit="420"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-light" data-fit="420"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <svg class="rule" viewBox="0 0 220 14"><g fill="none" stroke="#c9a552" stroke-width="1"><path d="M0,7 H92"/><path d="M128,7 H220"/><path d="M110,1 L116,7 L110,13 L104,7 Z"/></g><circle cx="98" cy="7" r="1.5" fill="#c9a552"/><circle cx="122" cy="7" r="1.5" fill="#c9a552"/></svg>
      ${H.f("event", "div", 'class="ev"')}
      <div class="dt">${H.dateLine()}</div>
      ${H.f("time", "div", 'class="tm"')}
      <div class="vn">${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`,
});
