/* E5 - Siyah Jaali: black card, a backlit Mughal jaali glowing champagne-gold around the wording. */
registerDesign((() => {
  const ID = "e5-siyah-jaali", S = `[data-d="${ID}"]`;
  return {
    id: ID,
    name: "Siyah Jaali",
    idea: "Black-and-gold evening luxe: a backlit Mughal stone jaali glows champagne around the names, as if the wording stood inside the window itself.",
    css: H => `
      ${S} { background: #0b0a09; color: #f7efdc; }
      ${S} .jaali { background: url(${H.img("mughal-jaali-arch.webp")}) 50% -40px / 1040px auto no-repeat;
        filter: grayscale(1) brightness(.72) contrast(1.15); }
      ${S} .tint { background: linear-gradient(160deg, #a77f33 0%, #e2c47a 30%, #b8913f 55%, #d9bb6d 78%, #94702c 100%); mix-blend-mode: multiply; }
      ${S} .shade { background: radial-gradient(ellipse 60% 50% at 50% 50%, rgba(11,10,9,.15) 40%, rgba(11,10,9,.55) 100%),
        linear-gradient(rgba(11,10,9,.35), rgba(11,10,9,0) 18%, rgba(11,10,9,0) 82%, rgba(11,10,9,.8) 100%); }
      ${S} .tb { left: 140px; right: 140px; top: 336px; text-align: center; display: flex; flex-direction: column; align-items: center; }
      ${S} .bism { font-size: calc(48px * var(--kt)); color: #f1e2b8; line-height: 1.2; }
      ${S} .hosts { font: 600 calc(43px * var(--kt))/1.2 Cinzel, serif; letter-spacing: .05em; margin-top: 18px; }
      ${S} .inv { font: italic 500 calc(37px * var(--kt))/1.27 'Cormorant Garamond', serif; margin-top: 6px; color: #f7efdc; }
      ${S} .nm { font: 400 calc(138px * var(--kn))/1.06 'Great Vibes', cursive; white-space: nowrap; }
      ${S} .g { margin-top: 20px; }
      ${S} .with { font: italic 500 calc(46px * var(--kt))/1 'Cormorant Garamond', serif; color: #f7efdc; margin: 0; }
      ${S} .bp { font: italic 500 calc(36px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 2px; color: #f7efdc; }
      ${S} .ev { font: 600 calc(50px * var(--kt))/1.2 Cinzel, serif; letter-spacing: .14em; padding-left: .14em; margin-top: 24px; }
      ${S} .dt { font: 600 calc(44px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 6px; }
      ${S} .vn { font: 600 calc(40px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 4px; color: #f7efdc; }
      ${S} .vn .p { font-weight: 500; font-size: calc(38px * var(--kt)); }
      ${S} .ur { font-size: calc(38px * var(--kt)); line-height: 1.8; white-space: nowrap; color: #f7efdc; margin-top: 2px; }
      ${S} .rs { font: italic 500 calc(34px * var(--kt)) 'Cormorant Garamond', serif; margin-top: 0; color: #f7efdc; }
    `,
    render: (H, D) => `
      <div class="layer jaali"></div>
      <div class="layer tint"></div>
      <div class="layer shade"></div>
      <div class="layer"><svg viewBox="0 0 1000 1400">
        <path d="${H.archD(126, 748, 146 - H.archApex(748, 0), 1300, .62, 9)}" fill="#0b0a09" fill-opacity=".96"/>
        <path d="${H.archD(114, 772, 134 - H.archApex(772, 0), 1312, .62, 9)}" fill="none" stroke="url(#goldBright)" stroke-width="5"/>
        <path d="${H.archD(140, 720, 160 - H.archApex(720, 0), 1286, .62, 9)}" fill="none" stroke="url(#goldBright)" stroke-width="1.8"/>
        <rect x="30" y="30" width="940" height="1340" fill="none" stroke="url(#goldBright)" stroke-width="4"/>
        <rect x="42" y="42" width="916" height="1316" fill="none" stroke="url(#goldBright)" stroke-width="1.5" opacity=".9"/>
      </svg></div>
      <div class="tb">
        ${H.bism()}
        ${H.f("hosts", "div", 'class="hosts"')}
        <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
        ${H.f("groom", "div", 'class="nm g foil foil-light" data-fit="680"')}
        ${H.f("joiner", "div", 'class="with"')}
        ${H.f("bride", "div", 'class="nm foil foil-light" data-fit="680"')}
        ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
        ${H.f("event", "div", 'class="ev foil foil-light"')}
        <div class="dt">${H.dateLine()}</div>
        <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="p">${H.f("place")}</span></div>
        ${H.urdu()}
        ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      </div>`,
  };
})());
