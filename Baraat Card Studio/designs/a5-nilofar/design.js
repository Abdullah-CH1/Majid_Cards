/* A5 - Shabnam : a deckle-edged cotton card floating on a sage ground, letterpress-style type, bold thick-and-thin gold frame
   with geometric eight-point-star corners. Round 2: no flowers - the water lilies are gone and the space goes to big type. */
registerDesign({
  id: "a5-nilofar",
  name: "Shabnam",
  idea: "A torn-edge cotton paper card floats on soft sage like a letterpress keepsake - a bold gold frame with eight-point Mughal stars at its corners, and big, clear lettering with the names in gold foil.",
  css: H => {
    // deterministic deckle edge
    let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    const X0 = 70, Y0 = 70, X1 = 930, Y1 = 1330, st = 7, pts = [];
    const j = () => (rnd() * 3.6 + (rnd() < .12 ? 2.2 : 0)).toFixed(1);
    for (let x = X0; x < X1; x += st) pts.push(`${x}px ${(Y0 + +j()).toFixed(1)}px`);
    for (let y = Y0; y < Y1; y += st) pts.push(`${(X1 - j()).toFixed(1)}px ${y}px`);
    for (let x = X1; x > X0; x -= st) pts.push(`${x}px ${(Y1 - j()).toFixed(1)}px`);
    for (let y = Y1; y > Y0; y -= st) pts.push(`${(X0 + +j()).toFixed(1)}px ${y}px`);
    const poly = `polygon(${pts.join(",")})`;
    const P = '[data-d="a5-nilofar"]';
    return `
    ${P} { background: #a9b39c; color: #1f2a1f; font-variant-numeric: lining-nums; font-feature-settings: "lnum" 1; }
    ${P} .ground { background:
        radial-gradient(ellipse 70% 55% at 50% 45%, rgba(236,236,220,.35), rgba(236,236,220,0) 70%),
        radial-gradient(ellipse 120% 90% at 50% 50%, rgba(0,0,0,0) 55%, rgba(40,52,38,.35) 100%); }
    ${P} .gpaper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: multiply; opacity: .55; filter: contrast(1.2); }
    ${P} .lift { filter: drop-shadow(0 16px 22px rgba(35,48,32,.34)) drop-shadow(0 2px 3px rgba(35,48,32,.25)); }
    ${P} .sheet { clip-path: ${poly}; background: #f8f3e7; }
    ${P} .spaper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: multiply; opacity: .28; filter: brightness(1.12) contrast(1.05); }
    ${P} .sglow { background: radial-gradient(ellipse 60% 45% at 52% 40%, rgba(255,253,246,.7), rgba(255,253,246,0) 72%); }
    ${P} .tb { left: 150px; right: 150px; top: 206px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(50px * var(--kt)); line-height: 1.25; color: #6e5016; }
    ${P} .hosts { font: 600 calc(44px * var(--kt))/1.25 'Cormorant SC', serif; letter-spacing: .08em; color: #1f2a1f; margin-top: 26px; white-space: nowrap; }
    ${P} .inv { font: italic 500 calc(37px * var(--kt))/1.28 'Cormorant Garamond', serif; margin-top: 8px; color: #1f2a1f; }
    ${P} .nm { font: 400 calc(138px * var(--kn))/1.06 'Great Vibes', cursive; white-space: nowrap;
        --foil: linear-gradient(100deg,#5a3f10 0%,#8f6b25 20%,#b08a3a 34%,#6f4f1a 52%,#a07a30 70%,#5a3f10 88%,#8a6624 100%);
        filter: drop-shadow(0 1px 0 rgba(60,40,10,.25)); }
    ${P} .nm.g { margin-top: 34px; }
    ${P} .with { font: italic 500 calc(46px * var(--kt))/1 'Cormorant Garamond', serif; color: #2b3d2c; margin: 0 0 6px; }
    ${P} .bp { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #1f2a1f; margin-top: 2px; }
    ${P} .ev { display: flex; align-items: center; gap: 22px; margin-top: 40px; color: #7a5a18; }
    ${P} .ev .f { font: 600 calc(50px * var(--kt))/1.15 Cinzel, serif; letter-spacing: .14em; margin-right: -.14em;
        --foil: linear-gradient(100deg,#5a3f10 0%,#8f6b25 25%,#a8823a 45%,#6f4f1a 65%,#94702a 85%,#5a3f10 100%);
        filter: drop-shadow(0 1px 0 rgba(60,40,10,.22)); }
    ${P} .ev i { display: block; width: 12px; height: 12px; background: #7a5a18; transform: rotate(45deg); }
    ${P} .dt { font: 500 calc(42px * var(--kt))/1.25 'EB Garamond', serif; margin-top: 12px; color: #1f2a1f; white-space: nowrap; }
    ${P} .vn { font: 500 calc(39px * var(--kt))/1.28 'EB Garamond', serif; margin-top: 6px; color: #1f2a1f; }
    ${P} .vn .pl { font-size: calc(36px * var(--kt)); font-weight: 500; }
    ${P} .rs { font: italic 400 calc(34px * var(--kt))/1.3 'EB Garamond', serif; margin-top: 6px; color: #1f2a1f; }
    ${P} .ur { font-size: calc(38px * var(--kt)); line-height: 1.9; color: #1f2a1f; margin-top: 14px; }
  `;
  },
  render: (H, D) => {
    const X0 = 70, Y0 = 70, X1 = 930, Y1 = 1330;
    const fr = (i, r) => `M${X0 + i + r},${Y0 + i} H${X1 - i - r} A${r},${r} 0 0 1 ${X1 - i},${Y0 + i + r} V${Y1 - i - r} A${r},${r} 0 0 1 ${X1 - i - r},${Y1 - i} H${X0 + i + r} A${r},${r} 0 0 1 ${X0 + i},${Y1 - i - r} V${Y0 + i + r} A${r},${r} 0 0 1 ${X0 + i + r},${Y0 + i}Z`;
    // eight-point star (two overlapping squares) outline
    const star = (R, k = .765) => { let d = ""; for (let i = 0; i < 16; i++) { const a = (i * 22.5 - 90) * Math.PI / 180, r = i % 2 ? R * k : R; d += (i ? "L" : "M") + (r * Math.cos(a)).toFixed(2) + "," + (r * Math.sin(a)).toFixed(2); } return d + "Z"; };
    const corner = (x, y) => `<g transform="translate(${x},${y})">
        <path d="${star(30)}" stroke-width="3"/><path d="${star(17)}" stroke-width="2"/><circle r="5" fill="url(#a5g)" stroke="none"/></g>`;
    const ci = 54; // corner star centres sit on the frame
    return `
    <div class="layer gpaper"></div>
    <div class="layer ground"></div>
    <div class="layer lift"><div class="layer sheet">
      <div class="layer spaper"></div>
      <div class="layer sglow"></div>
      <div class="layer"><svg viewBox="0 0 1000 1400">
        <defs><linearGradient id="a5g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1000" y2="1400">
          <stop offset="0" stop-color="#7a5a1c"/><stop offset=".2" stop-color="#b8923f"/><stop offset=".38" stop-color="#8a6626"/>
          <stop offset=".55" stop-color="#c29c4c"/><stop offset=".75" stop-color="#7f5e20"/><stop offset="1" stop-color="#a8823a"/></linearGradient></defs>
        <g fill="none" stroke="url(#a5g)">
          <path d="${fr(32, 4)}" stroke-width="5"/>
          <path d="${fr(46, 2)}" stroke-width="1.8"/>
        </g>
        <g fill="#f8f3e7" stroke="url(#a5g)" stroke-linejoin="miter">
          ${corner(X0 + ci - 15, Y0 + ci - 15)}${corner(X1 - ci + 15, Y0 + ci - 15)}${corner(X0 + ci - 15, Y1 - ci + 15)}${corner(X1 - ci + 15, Y1 - ci + 15)}
        </g>
        <g fill="none" stroke="url(#a5g)" stroke-linecap="round">
          <path d="M370,150 H458" stroke-width="2.5"/><path d="M542,150 H630" stroke-width="2.5"/>
          <g transform="translate(500,150)" fill="#f8f3e7"><path d="${star(26)}" stroke-width="3"/><path d="${star(13)}" stroke-width="2"/><circle r="4" fill="url(#a5g)" stroke="none"/></g>
          <path d="M370,1250 H458" stroke-width="2.5"/><path d="M542,1250 H630" stroke-width="2.5"/>
          <g transform="translate(500,1250)" fill="#f8f3e7"><path d="${star(26)}" stroke-width="3"/><path d="${star(13)}" stroke-width="2"/><circle r="4" fill="url(#a5g)" stroke="none"/></g>
        </g>
      </svg></div>
      <div class="tb">
        ${H.bism()}
        ${H.f("hosts", "div", 'class="hosts" data-fit="680"')}
        <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
        ${H.f("groom", "div", 'class="nm g foil" data-fit="660"')}
        ${H.f("joiner", "div", 'class="with"')}
        ${H.f("bride", "div", 'class="nm foil" data-fit="660"')}
        ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
        <div class="ev"><i></i>${H.f("event", "span", 'class="foil"')}<i></i></div>
        <div class="dt" data-fit="690">${H.dateLine()}</div>
        <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
        ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
        ${H.urdu()}
      </div>
    </div></div>`;
  },
});
