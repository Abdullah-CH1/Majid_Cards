/* A1 - Noor Mehrab : the client's favourite (cream, gold cusped arch, gold mandalas), rebuilt bold and flower-free */
registerDesign({
  id: "a1-noor-kanwal",
  name: "Noor Mehrab",
  idea: "Your favourite card, made bolder: handmade ivory paper, a strong foil-gold cusped Mughal arch, gold mandalas in the corners and a great gold mandala rising at the base, with large, easy-to-read lettering.",
  css: H => `
    [data-d="a1-noor-kanwal"] { background: #f2e6cf; color: #2b1d12; }
    [data-d="a1-noor-kanwal"] .paper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: multiply; opacity: .22; filter: brightness(1.1) contrast(1.08); }
    [data-d="a1-noor-kanwal"] .glow { background:
        radial-gradient(ellipse 46% 40% at 50% 48%, rgba(255,250,238,.8), rgba(255,250,238,0) 72%),
        radial-gradient(ellipse 120% 90% at 50% 50%, rgba(0,0,0,0) 60%, rgba(120,84,40,.18) 100%); }
    [data-d="a1-noor-kanwal"] .tb { left: 150px; right: 150px; top: 266px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="a1-noor-kanwal"] .bism { font-family: Amiri, serif; font-size: calc(46px * var(--kt)); line-height: 1.38; color: #5c4012; }
    [data-d="a1-noor-kanwal"] .hosts { font: 600 calc(44px * var(--kt))/1.2 'Cormorant SC', serif; letter-spacing: .07em; margin-top: 2px; color: #2b1d12; }
    [data-d="a1-noor-kanwal"] .inv { font: italic 500 calc(36px * var(--kt))/1.28 'Cormorant Garamond', serif; margin-top: 4px; color: #2b1d12; }
    [data-d="a1-noor-kanwal"] .nm { font: 400 calc(132px * var(--kn))/1.0 'Great Vibes', cursive; white-space: nowrap; filter: drop-shadow(0 1px 0 rgba(60,40,10,.28)); }
    [data-d="a1-noor-kanwal"] .nm.g { margin-top: 12px; }
    [data-d="a1-noor-kanwal"] .with { font: italic 500 calc(46px * var(--kt))/1 'Cormorant Garamond', serif; color: #2b1d12; margin: -2px 0 2px; }
    [data-d="a1-noor-kanwal"] .bp { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #2b1d12; margin-top: 2px; }
    [data-d="a1-noor-kanwal"] .ev { display: flex; align-items: center; gap: 20px; margin-top: 12px; }
    [data-d="a1-noor-kanwal"] .ev .f { font: 600 calc(48px * var(--kt))/1.15 Cinzel, serif; letter-spacing: .14em; margin-right: -.14em; filter: drop-shadow(0 1px 0 rgba(60,40,10,.25)); }
    [data-d="a1-noor-kanwal"] .ev i { display: block; width: 64px; height: 3px; background: linear-gradient(90deg, rgba(122,85,24,0), #8a6420); position: relative; }
    [data-d="a1-noor-kanwal"] .ev i:last-child { transform: scaleX(-1); }
    [data-d="a1-noor-kanwal"] .ev i::after { content: ""; position: absolute; right: -6px; top: -4.5px; width: 12px; height: 12px; background: #8a6420; transform: rotate(45deg); }
    [data-d="a1-noor-kanwal"] .dt { font: 600 calc(44px * var(--kt))/1.25 'Cormorant Garamond', serif; letter-spacing: .01em; margin-top: 10px; color: #2b1d12; }
    [data-d="a1-noor-kanwal"] .vn { font: 600 calc(40px * var(--kt))/1.28 'Cormorant Garamond', serif; margin-top: 4px; color: #2b1d12; }
    [data-d="a1-noor-kanwal"] .vn .pl { font-weight: 500; font-size: .95em; }
    [data-d="a1-noor-kanwal"] .rs { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 4px; color: #2b1d12; }
    [data-d="a1-noor-kanwal"] .ur { font-size: calc(38px * var(--kt)); line-height: 1.9; color: #3a2814; margin-top: 2px; }
  `,
  render: (H, D) => {
    const G = "url(#a1gold)";
    const n = (H.has("brideParents") ? 1 : 0) + (H.has("rsvp") ? 1 : 0);    // optional lines push the base mandala down
    const corner = (x, y) => `<g transform="translate(${x},${y})">${H.mandala(250, { sw: 2.2, stroke: G })}</g>`;
    const archO = H.archD(96, 808, 560, 1352, .6, 7, true);
    const archI = H.archD(110, 780, 562, 1352, .6, 7, true);
    const apex = H.archApex(808, 560, .6);
    const side = x => `<g transform="translate(${x},700)"><path d="M0,-30 C11,-13 11,13 0,30 C-11,13 -11,-13 0,-30Z" fill="#f2e6cf" stroke="${G}" stroke-width="2.6"/><circle r="4.5" fill="${G}"/></g>`;
    return `
    <div class="layer paper"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <defs>
        <linearGradient id="a1gold" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1000" y2="1400"><stop offset="0" stop-color="#7f5a1c"/><stop offset=".18" stop-color="#c49a45"/><stop offset=".34" stop-color="#8f6824"/><stop offset=".5" stop-color="#d0aa55"/><stop offset=".66" stop-color="#8a6322"/><stop offset=".82" stop-color="#bf9440"/><stop offset="1" stop-color="#76521a"/></linearGradient>
        <clipPath id="a1base"><circle r="364"/></clipPath>
        <clipPath id="a1clip"><rect x="46" y="46" width="908" height="1308"/></clipPath>
      </defs>
      <g clip-path="url(#a1clip)">
        ${corner(46, 46)}${corner(954, 46)}
        <g transform="translate(500,${1484 + 46 * n})" clip-path="url(#a1base)">${H.mandala(440, { sw: 2.4, stroke: G })}</g>
      </g>
    </svg></div>
    <div class="layer glow"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none" stroke="${G}">
        <rect x="32" y="32" width="936" height="1336" stroke-width="5"/>
        <rect x="46" y="46" width="908" height="1308" stroke-width="2"/>
        <path d="${archO}" stroke-width="5"/>
        <path d="${archI}" stroke-width="2"/>
      </g>
      <g fill="${G}">
        <path d="M500,${apex - 52} C509,${apex - 34} 518,${apex - 22} 500,${apex - 3} C482,${apex - 22} 491,${apex - 34} 500,${apex - 52}Z"/>
        <circle cx="500" cy="${apex - 64}" r="5"/>
        ${side(32)}${side(968)}
      </g>
    </svg></div>
    <div class="tb">
      ${H.bism('class="bism"')}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="660"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="660"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="ev"><i></i>${H.f("event", "span", 'class="foil foil-deep"')}<i></i></div>
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`;
  },
});
