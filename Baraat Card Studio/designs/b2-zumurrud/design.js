/* B2 - Zumurrud: emerald velvet with an inset ivory Mughal arch, edged in a band of burnished gold.
   Round 2: wider arch so the type can be big, solid gold edge (no patterned leaf), bold thick-and-thin arch lines. */
registerDesign({
  id: "b2-zumurrud",
  name: "Zumurrud",
  idea: "Deep emerald velvet opens into a wide ivory paper arch edged in burnished gold - the richness of a Baraat evening with the clean calm of a classic card, and lettering large enough for everyone to read.",
  css: H => {
    const P = '[data-d="b2-zumurrud"]';
    const outer = H.archD(96, 808, 540, 1314, .53, 7);
    const inner = H.archD(104, 792, 540, 1306, .53, 7);
    return `
    ${P} { background: #06261d; color: #10291f; }
    ${P} .vel { background: url(${H.img("emerald-velvet.webp")}) center/cover; filter: brightness(.95) saturate(1.05); transform: scaleX(-1); }
    ${P} .lift { background: linear-gradient(160deg, #0d4a35, #08301f 60%, #0b3b2a); mix-blend-mode: screen; opacity: .55; }
    ${P} .vig { background: radial-gradient(ellipse 45% 40% at 88% 30%, rgba(20,110,80,.28), transparent 70%), radial-gradient(ellipse 50% 40% at 15% 85%, rgba(20,110,80,.18), transparent 70%), radial-gradient(ellipse 75% 65% at 50% 50%, transparent 45%, rgba(0,10,6,.55) 100%); }
    ${P} .sh { filter: drop-shadow(0 18px 26px rgba(0,0,0,.55)) drop-shadow(0 2px 3px rgba(0,0,0,.4)); }
    ${P} .leaf { position: absolute; inset: 0; clip-path: path("${outer}");
        background: linear-gradient(115deg, #8a6424 0%, #e9cd80 16%, #b48c3e 30%, #f6e2a2 46%, #a27a32 60%, #e3c473 76%, #8e6a2a 100%); }
    ${P} .ivory { position: absolute; inset: 0; clip-path: path("${inner}");
        background: radial-gradient(ellipse 75% 60% at 50% 42%, #fcf8ee 0%, #f6efdf 60%, #eee4cd 100%); }
    ${P} .ivory::before { content: ""; position: absolute; inset: 0; opacity: .26; mix-blend-mode: multiply;
        background: url(${H.img("textured-ivory-paper.webp")}) center/700px auto; filter: contrast(.8); }
    ${P} .tb { left: 160px; right: 160px; top: 300px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(48px * var(--kt)); line-height: 1.2; color: #5e4512; }
    ${P} .hosts { white-space: nowrap; font: 400 calc(42px * var(--kt))/1.2 Prata, serif; letter-spacing: .04em; margin-top: 26px; color: #10291f; }
    ${P} .inv { font: italic 400 calc(35px * var(--kt))/1.3 Lora, serif; margin-top: 8px; color: #10291f; }
    ${P} .nm { font: 400 calc(132px * var(--kn))/1.1 Parisienne, cursive; white-space: nowrap; -webkit-text-stroke: .9px rgba(95,66,16,.55);
        --foil: linear-gradient(100deg,#5a3f10 0%,#94702a 22%,#b38d3c 36%,#6a4a14 54%,#a07a30 72%,#55390d 90%,#8a6624 100%);
        filter: drop-shadow(0 1px 0 rgba(60,40,10,.25)); }
    ${P} .nm.g { margin-top: 26px; }
    ${P} .with { font: italic 400 calc(44px * var(--kt))/1 Lora, serif; color: #1d3d30; margin: -2px 0 4px; }
    ${P} .bp { font: italic 400 calc(34px * var(--kt))/1.25 Lora, serif; color: #10291f; margin-top: 2px; }
    ${P} .ev { display: flex; align-items: center; gap: 20px; margin-top: 36px; }
    ${P} .ev .f { font: 600 calc(48px * var(--kt))/1.15 Cinzel, serif; letter-spacing: .14em; margin-right: -.14em;
        --foil: linear-gradient(100deg,#5a3f10 0%,#8f6b25 25%,#a8823a 45%,#6f4f1a 65%,#94702a 85%,#5a3f10 100%);
        filter: drop-shadow(0 1px 0 rgba(60,40,10,.22)); }
    ${P} .ev i { display: block; width: 52px; height: 2.5px; background: #8a6624; }
    ${P} .dt { font: 500 calc(42px * var(--kt))/1.25 Lora, serif; margin-top: 10px; color: #10291f; white-space: nowrap; }
    ${P} .vn { font: 500 calc(38px * var(--kt))/1.3 Lora, serif; margin-top: 4px; color: #10291f; }
    ${P} .vn .pl { font-size: calc(35px * var(--kt)); font-weight: 400; }
    ${P} .ur { font-size: calc(38px * var(--kt)); line-height: 1.85; color: #10291f; margin-top: 14px; }
    ${P} .rs { font: italic 400 calc(34px * var(--kt))/1.25 Lora, serif; color: #10291f; margin-top: 2px; }
  `;
  },
  render: (H, D) => {
    const star = (R, k = .765) => { let d = ""; for (let i = 0; i < 16; i++) { const a = (i * 22.5 - 90) * Math.PI / 180, r = i % 2 ? R * k : R; d += (i ? "L" : "M") + (r * Math.cos(a)).toFixed(2) + "," + (r * Math.sin(a)).toFixed(2); } return d + "Z"; };
    return `
    <div class="layer vel"></div>
    <div class="layer lift"></div>
    <div class="layer vig"></div>
    <div class="layer sh"><div class="leaf"></div><div class="ivory"></div></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <defs><linearGradient id="b2g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1000" y2="1400">
        <stop offset="0" stop-color="#7a5a1c"/><stop offset=".2" stop-color="#b08a3a"/><stop offset=".38" stop-color="#7f5e20"/>
        <stop offset=".55" stop-color="#b8923f"/><stop offset=".75" stop-color="#76561a"/><stop offset="1" stop-color="#a07a30"/></linearGradient></defs>
      <path d="${H.archD(122, 756, 540, 1288, .53, 7)}" fill="none" stroke="url(#b2g)" stroke-width="2"/>
      <g transform="translate(500,206)" fill="none" stroke="url(#b2g)">
        <path d="${star(30)}" stroke-width="2.8"/><path d="${star(15)}" stroke-width="2"/><circle r="4" fill="url(#b2g)" stroke="none"/>
      </g>
      <g stroke="url(#goldBright)" fill="url(#goldBright)">
        <line x1="500" y1="62" x2="500" y2="112" stroke-width="3"/>
        <path d="M500,70 l10,15 l-10,15 l-10,-15z" stroke="none"/>
        <circle cx="500" cy="56" r="5" stroke="none"/>
      </g>
    </svg></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts" data-fit="660"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil" data-fit="640"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil" data-fit="640"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="ev"><i></i>${H.f("event", "span", 'class="foil"')}<i></i></div>
      <div class="dt" data-fit="660">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;&middot;&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`;
  },
});
