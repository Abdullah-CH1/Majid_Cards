/* E2 - Mumtaz: an 1880 watercolour elevation of the Taj Mahal set like an architectural plate between bold Didone typography. */
registerDesign((() => {
  const ID = "e2-mumtaz", S = `[data-d="${ID}"]`;
  // plate size: the painting's drawn area (finial to platform) is roughly 8%..82% of its height
  const TW = 640, TX = (1000 - TW) / 2, TH = Math.round(TW * 1404 / 2000), TT = 680;
  return {
    id: ID,
    name: "Mumtaz",
    idea: "The Taj Mahal, drawn in watercolour in 1880, sits on ivory paper like a museum plate between large Bodoni capitals, a script 'with' and a bold gold double frame.",
    css: H => `
      ${S} { background: #f3ede1; color: #241c14; }
      ${S} .paper { background: url(${H.img("textured-ivory-paper.webp")}) center / cover; mix-blend-mode: multiply; opacity: .22; }
      ${S} .tone { background: radial-gradient(ellipse 75% 55% at 50% 40%, rgba(255,251,242,.85), rgba(255,251,242,0) 75%); }
      ${S} .taj { position: absolute; left: ${TX}px; top: ${TT}px; width: ${TW}px; height: ${TH}px;
        background: url(${H.img("taj-mahal-elevation-painting.webp")}) 0 0 / ${TW}px auto no-repeat; mix-blend-mode: multiply;
        filter: saturate(.7) brightness(1.03) contrast(1.35);
        -webkit-mask-image: linear-gradient(90deg, transparent 12%, #000 14.9%, #000 85.1%, transparent 88%), linear-gradient(transparent 6.2%, #000 7.6%, #000 77%, transparent 87%), linear-gradient(323deg, #000 79%, transparent 84%);
        -webkit-mask-composite: source-in, source-in;
        mask-image: linear-gradient(90deg, transparent 12%, #000 14.9%, #000 85.1%, transparent 88%), linear-gradient(transparent 6.2%, #000 7.6%, #000 77%, transparent 87%), linear-gradient(323deg, #000 79%, transparent 84%);
        mask-composite: intersect; }
      ${S} .tb { left: 96px; right: 96px; top: 92px; text-align: center; display: flex; flex-direction: column; align-items: center; }
      ${S} .bism { font-size: calc(48px * var(--kt)); color: #3e2a10; line-height: 1.2; margin-bottom: 8px; }
      ${S} .hosts { font: 400 calc(42px * var(--kt))/1.2 Prata, serif; letter-spacing: .08em; padding-left: .08em; margin-top: 24px; text-transform: uppercase; }
      ${S} .inv { font: italic 400 calc(36px * var(--kt))/1.3 'Playfair Display', serif; margin-top: 8px; }
      ${S} .nm { font: 500 calc(88px * var(--kn))/1.08 'Bodoni Moda', serif; letter-spacing: .07em; padding-left: .07em; text-transform: uppercase; white-space: nowrap;
        filter: drop-shadow(0 1px 0 rgba(60,40,10,.3)); }
      ${S} .g { margin-top: 26px; }
      ${S} .with { font: 400 calc(64px * var(--kt))/1 Allura, cursive; color: #5a3e10; margin: 0; }
      ${S} .bp { font: italic 400 calc(34px * var(--kt))/1.25 'Playfair Display', serif; margin-top: 6px; }
      ${S} .ev { font: 500 calc(48px * var(--kt))/1.2 'Bodoni Moda', serif; letter-spacing: .16em; padding-left: .16em; margin-top: 26px; text-transform: uppercase;
        filter: drop-shadow(0 1px 0 rgba(60,40,10,.3)); }
      ${S} .info { position: absolute; left: 80px; right: 80px; top: 1068px; translate: 0 var(--dy); text-align: center; display: flex; flex-direction: column; align-items: center; }
      ${S} .dt { font: 400 calc(42px * var(--kt))/1.25 Prata, serif; }
      ${S} .vn { font: 400 calc(38px * var(--kt))/1.32 Prata, serif; margin-top: 8px; }
      ${S} .vn .p { font-size: calc(36px * var(--kt)); }
      ${S} .ur { font-size: calc(38px * var(--kt)); line-height: 1.8; white-space: nowrap; color: #241c14; margin-top: 4px; }
      ${S} .rs { font: italic 400 calc(34px * var(--kt)) 'Playfair Display', serif; margin-top: 0; }
    `,
    render: (H, D) => `
      <div class="layer paper"></div>
      <div class="layer tone"></div>
      <div class="taj"></div><div class="taj"></div><div class="taj"></div>
      <div class="layer"><svg viewBox="0 0 1000 1400">
        <g fill="none" stroke="#6b4c14" opacity=".28"><rect x="34" y="34" width="932" height="1332" stroke-width="6.6"/><rect x="48" y="48" width="904" height="1304" stroke-width="2.8"/></g>
        <rect x="34" y="34" width="932" height="1332" fill="none" stroke="url(#gold)" stroke-width="5"/>
        <rect x="48" y="48" width="904" height="1304" fill="none" stroke="url(#gold)" stroke-width="1.8"/>
        ${[[34,34],[966,34],[34,1366],[966,1366]].map(([x,y]) => `<rect x="${x-9}" y="${y-9}" width="18" height="18" transform="rotate(45 ${x} ${y})" fill="url(#gold)"/>`).join("")}
        <path d="M330,1046 H670" stroke="url(#gold)" stroke-width="2.5"/>
        <rect x="494" y="1040" width="12" height="12" transform="rotate(45 500 1046)" fill="url(#gold)"/>
      </svg></div>
      <div class="tb">
        ${H.bism()}
        ${H.f("hosts", "div", 'class="hosts"')}
        <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
        ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="800"')}
        ${H.f("joiner", "div", 'class="with"')}
        ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="800"')}
        ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
        ${H.f("event", "div", 'class="ev foil foil-deep"')}
      </div>
      <div class="info">
        <div class="dt">${H.dateLine()}</div>
        <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="p">${H.f("place")}</span></div>
        ${H.urdu()}
        ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      </div>
    `,
  };
})());
