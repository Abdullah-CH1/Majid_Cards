/* E2 - Mumtaz: an 1880 watercolour elevation of the Taj Mahal set like an architectural plate between Didone typography. */
registerDesign((() => {
  const ID = "e2-mumtaz", S = `[data-d="${ID}"]`;
  const TW = 860, TX = (1000 - TW) / 2, TT = 600, TH = Math.round(TW * 1404 / 2000);
  return {
    id: ID,
    name: "Mumtaz",
    idea: "The Taj Mahal, drawn in fine watercolour in 1880, sits on ivory paper like a museum plate, framed by crisp Bodoni capitals and a single gold script 'with'.",
    css: H => `
      ${S} { background: #f3ede1; color: #2e2822; }
      ${S} .paper { background: url(${H.img("textured-ivory-paper.webp")}) center / cover; mix-blend-mode: multiply; opacity: .22; }
      ${S} .tone { background: radial-gradient(ellipse 75% 55% at 50% 40%, rgba(255,251,242,.85), rgba(255,251,242,0) 75%); }
      ${S} .taj { position: absolute; left: ${TX}px; top: ${TT}px; width: ${TW}px; height: ${TH}px;
        background: url(${H.img("taj-mahal-elevation-painting.webp")}) 0 0 / ${TW}px auto no-repeat; mix-blend-mode: multiply;
        filter: saturate(.42) brightness(1.05) contrast(1.2);
        -webkit-mask-image: linear-gradient(90deg, transparent 9.5%, #000 14.2%, #000 85.8%, transparent 90.5%), linear-gradient(transparent 37px, #000 46px, #000 77%, transparent 88%);
        -webkit-mask-composite: source-in;
        mask-image: linear-gradient(90deg, transparent 9.5%, #000 14.2%, #000 85.8%, transparent 90.5%), linear-gradient(transparent 37px, #000 46px, #000 77%, transparent 88%);
        mask-composite: intersect; }
      ${S} .tb { left: 110px; right: 110px; top: 112px; text-align: center; display: flex; flex-direction: column; align-items: center; }
      ${S} .bism { font-size: calc(38px * var(--kt)); color: #6b5226; }
      ${S} .hosts { font: 400 calc(26px * var(--kt)) Italiana, serif; letter-spacing: .3em; padding-left: .3em; margin-top: 22px; text-transform: uppercase; }
      ${S} .inv { font: italic 400 calc(24px * var(--kt))/1.45 'Bodoni Moda', serif; margin-top: 10px; color: #4a4036; }
      ${S} .nm { font: 400 calc(64px * var(--kn))/1.1 'Bodoni Moda', serif; letter-spacing: .1em; padding-left: .1em; text-transform: uppercase; white-space: nowrap; }
      ${S} .g { margin-top: 30px; }
      ${S} .with { font: 400 calc(46px * var(--kt))/1 'Pinyon Script', cursive; color: #8a6a2e; margin: 6px 0 4px; }
      ${S} .bp { font: italic 400 calc(20px * var(--kt)) 'Bodoni Moda', serif; margin-top: 6px; color: #4a4036; }
      ${S} .ev { font: 500 calc(19px * var(--kt)) 'Bodoni Moda', serif; letter-spacing: .7em; padding-left: .7em; margin-top: 26px; color: #6b5226; text-transform: uppercase; }
      ${S} .info { position: absolute; left: 90px; right: 90px; top: 1140px; translate: 0 var(--dy); display: grid; grid-template-columns: 1fr 1px 1fr; column-gap: 44px; align-items: center; }
      ${S} .info .rule { height: 100%; min-height: 96px; background: linear-gradient(transparent, #b0904f 20%, #b0904f 80%, transparent); }
      ${S} .col { text-align: center; }
      ${S} .cap { font: 500 calc(18px * var(--kt)) 'Bodoni Moda', serif; letter-spacing: .32em; padding-left: .32em; text-transform: uppercase; color: #6b5226; }
      ${S} .big { font: 400 calc(29px * var(--kt))/1.3 'Bodoni Moda', serif; margin-top: 6px; }
      ${S} .sm { font: italic 400 calc(21px * var(--kt))/1.35 'Bodoni Moda', serif; color: #4a4036; }
      ${S} .ur { position: absolute; left: 0; right: 0; top: 1254px; translate: 0 var(--dy); text-align: center; font-size: calc(20px * var(--kt)); color: #6b5226; }
      ${S} .rs { position: absolute; left: 0; right: 0; top: 1306px; translate: 0 var(--dy); text-align: center; font: 500 calc(15px * var(--kt)) 'Bodoni Moda', serif; letter-spacing: .25em; color: #6b5226; }
    `,
    render: (H, D) => `
      <div class="layer paper"></div>
      <div class="layer tone"></div>
      <div class="taj"></div>
      <div class="layer"><svg viewBox="0 0 1000 1400">
        <rect x="40" y="40" width="920" height="1320" fill="none" stroke="url(#gold)" stroke-width="1.4"/>
        <rect x="50" y="50" width="900" height="1300" fill="none" stroke="url(#gold)" stroke-width=".6" opacity=".7"/>
        ${[[40,40],[960,40],[40,1360],[960,1360]].map(([x,y]) => `<rect x="${x-5}" y="${y-5}" width="10" height="10" transform="rotate(45 ${x} ${y})" fill="url(#gold)"/>`).join("")}
      </svg></div>
      <div class="tb">
        ${H.bism()}
        ${H.f("hosts", "div", 'class="hosts"')}
        <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
        ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="760"')}
        ${H.f("joiner", "div", 'class="with"')}
        ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="760"')}
        ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
        ${H.f("event", "div", 'class="ev"')}
      </div>
      <div class="info">
        <div class="col">${H.f("day", "div", 'class="cap"')}<div class="big">${H.f("dateNum")}<sup>${H.f("dateSup")}</sup> ${H.f("month")}</div>${H.f("year", "div", 'class="sm"')}</div>
        <div class="rule"></div>
        <div class="col">${H.f("time", "div", 'class="cap"')}${H.f("venue", "div", 'class="big"')}${H.f("place", "div", 'class="sm"')}</div>
      </div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    `,
  };
})());
