/* E5 - Siyah Jaali: black card, a backlit Mughal jaali glowing champagne-gold around the wording. */
registerDesign((() => {
  const ID = "e5-siyah-jaali", S = `[data-d="${ID}"]`;
  return {
    id: ID,
    name: "Siyah Jaali",
    idea: "Black-and-gold evening luxe: a backlit Mughal stone jaali glows champagne around the names, as if the wording stood inside the window itself.",
    css: H => `
      ${S} { background: #0b0a09; color: #efe5cf; }
      ${S} .jaali { background: url(${H.img("mughal-jaali-arch.webp")}) 50% -40px / 1040px auto no-repeat;
        filter: grayscale(1) brightness(.72) contrast(1.15); }
      ${S} .tint { background: linear-gradient(160deg, #a77f33 0%, #e2c47a 30%, #b8913f 55%, #d9bb6d 78%, #94702c 100%); mix-blend-mode: multiply; }
      ${S} .shade { background: radial-gradient(ellipse 60% 50% at 50% 50%, rgba(11,10,9,.15) 40%, rgba(11,10,9,.55) 100%),
        linear-gradient(rgba(11,10,9,.35), rgba(11,10,9,0) 18%, rgba(11,10,9,0) 82%, rgba(11,10,9,.8) 100%); }
      ${S} .tb { left: 150px; right: 150px; top: 372px; text-align: center; display: flex; flex-direction: column; align-items: center; }
      ${S} .bism { font-size: calc(35px * var(--kt)); color: #e6c877; }
      ${S} .hosts { font: 500 calc(25px * var(--kt)) Cinzel, serif; letter-spacing: .18em; margin-top: 28px; }
      ${S} .inv { font: italic 400 calc(25px * var(--kt))/1.42 'Cormorant Garamond', serif; margin-top: 8px; color: #e2d6bd; }
      ${S} .nm { font: 400 calc(110px * var(--kn))/1.12 'Great Vibes', cursive; white-space: nowrap; }
      ${S} .g { margin-top: 40px; }
      ${S} .with { font: italic 400 calc(27px * var(--kt))/1 'Cormorant Garamond', serif; color: #d9bd78; margin: 0 0 2px; }
      ${S} .bp { font: italic 400 calc(21px * var(--kt)) 'Cormorant Garamond', serif; margin-top: 2px; color: #e2d6bd; }
      ${S} .ev { font: 500 calc(20px * var(--kt)) Cinzel, serif; letter-spacing: .62em; padding-left: .62em; margin-top: 44px; color: #e6c877; }
      ${S} .dt { font: 500 calc(24px * var(--kt)) Cinzel, serif; letter-spacing: .1em; margin-top: 20px; }
      ${S} .vn { font: 500 calc(25px * var(--kt))/1.45 'Cormorant Garamond', serif; margin-top: 8px; color: #efe5cf; }
      ${S} .ur { font-size: calc(21px * var(--kt)); color: #e6c877; margin-top: 22px; }
      ${S} .rs { font: 400 calc(17px * var(--kt)) Cinzel, serif; letter-spacing: .2em; margin-top: 6px; color: #d9bd78; }
    `,
    render: (H, D) => `
      <div class="layer jaali"></div>
      <div class="layer tint"></div>
      <div class="layer shade"></div>
      <div class="layer"><svg viewBox="0 0 1000 1400">
        <path d="${H.archD(170, 660, 200 - H.archApex(660, 0), 1250, .62, 9)}" fill="#0b0a09" fill-opacity=".95"/>
        <path d="${H.archD(158, 684, 188 - H.archApex(684, 0), 1262, .62, 9)}" fill="none" stroke="url(#goldBright)" stroke-width="2.4"/>
        <path d="${H.archD(182, 636, 212 - H.archApex(636, 0), 1238, .62, 9)}" fill="none" stroke="url(#goldBright)" stroke-width=".9" opacity=".8"/>
        <rect x="34" y="34" width="932" height="1332" fill="none" stroke="url(#goldBright)" stroke-width="1.2" opacity=".7"/>
      </svg></div>
      <div class="tb">
        ${H.bism()}
        ${H.f("hosts", "div", 'class="hosts"')}
        <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
        ${H.f("groom", "div", 'class="nm g foil foil-light" data-fit="660"')}
        ${H.f("joiner", "div", 'class="with"')}
        ${H.f("bride", "div", 'class="nm foil foil-light" data-fit="660"')}
        ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
        ${H.f("event", "div", 'class="ev"')}
        <div class="dt">${H.dateLine()}</div>
        <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br>${H.f("place")}</div>
        ${H.urdu()}
        ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      </div>`,
  };
})());
