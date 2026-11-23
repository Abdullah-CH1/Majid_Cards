/* A2 - Nazakat : blush paper, a gold star-jaali border band, and the names in tall serif capitals */
registerDesign({
  id: "a2-nazakat",
  name: "Nazakat",
  idea: "Soft blush paper framed by a band of gold eight-pointed jaali stars, with the names set in tall gold capitals and a flowing script for 'with' and 'Baraat': quiet, refined and very easy to read.",
  css: H => `
    [data-d="a2-nazakat"] { background: #f3d8cc; color: #3a1f1a; }
    [data-d="a2-nazakat"] .paper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: multiply; opacity: .28; filter: brightness(1.1) contrast(1.1); }
    [data-d="a2-nazakat"] .tint { background:
        radial-gradient(ellipse 52% 44% at 50% 47%, rgba(255,244,238,.72), rgba(255,244,238,0) 74%),
        radial-gradient(ellipse 120% 90% at 50% 50%, rgba(0,0,0,0) 58%, rgba(120,60,50,.16) 100%); }
    [data-d="a2-nazakat"] .tb { left: 140px; right: 140px; top: 206px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="a2-nazakat"] .bism { font-family: Amiri, serif; font-size: calc(48px * var(--kt)); line-height: 1.4; color: #4a2418; }
    [data-d="a2-nazakat"] .hosts { font: 600 calc(44px * var(--kt))/1.2 'Cormorant SC', serif; letter-spacing: .07em; margin-top: 22px; color: #3a1f1a; }
    [data-d="a2-nazakat"] .inv { font: italic 500 calc(37px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 8px; color: #3a1f1a; }
    [data-d="a2-nazakat"] .nm { font: 600 calc(94px * var(--kn))/1.08 'Cormorant Garamond', serif; letter-spacing: .05em; text-transform: uppercase; white-space: nowrap; filter: drop-shadow(0 1px 0 rgba(70,30,15,.3)); }
    [data-d="a2-nazakat"] .nm.g { margin-top: 50px; }
    [data-d="a2-nazakat"] .with { font: 400 calc(70px * var(--kt))/1 'Great Vibes', cursive; color: #4a2418; margin: -4px 0 -2px; }
    [data-d="a2-nazakat"] .bp { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #3a1f1a; margin-top: 4px; }
    [data-d="a2-nazakat"] .ev { display: flex; align-items: center; gap: 22px; margin-top: 46px; }
    [data-d="a2-nazakat"] .ev .f { font: 400 calc(84px * var(--kt))/1.05 'Great Vibes', cursive; filter: drop-shadow(0 1px 0 rgba(70,30,15,.28)); }
    [data-d="a2-nazakat"] .ev svg { width: 34px; height: 34px; flex: none; }
    [data-d="a2-nazakat"] .dt { font: 600 calc(44px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 22px; color: #3a1f1a; }
    [data-d="a2-nazakat"] .vn { font: 600 calc(40px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 6px; color: #3a1f1a; }
    [data-d="a2-nazakat"] .vn .pl { font-weight: 500; font-size: .95em; }
    [data-d="a2-nazakat"] .rs { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 6px; color: #3a1f1a; }
    [data-d="a2-nazakat"] .ur { font-size: calc(38px * var(--kt)); line-height: 1.9; color: #3a1f1a; margin-top: 10px; }
  `,
  render: (H, D) => {
    const G = "url(#a2gold)";
    const n = (H.has("brideParents") ? 1 : 0) + (H.has("rsvp") ? 1 : 0);    // optional lines: start the text a little higher
    const star = (R, cx = 0, cy = 0) => {
      let d = "";
      for (let i = 0; i < 16; i++) { const a = (i * 22.5 - 90) * Math.PI / 180, r = i % 2 ? R * .765 : R; d += (i ? "L" : "M") + (cx + Math.cos(a) * r).toFixed(1) + "," + (cy + Math.sin(a) * r).toFixed(1); }
      return d + "Z";
    };
    const B = 70, R = 19;                       // band centre line and star radius
    const parts = [];
    const run = (x1, y1, x2, y2) => {           // stars along a side, chained by a rule
      const L = Math.hypot(x2 - x1, y2 - y1), n = Math.round(L / 74), ux = (x2 - x1) / L, uy = (y2 - y1) / L;
      for (let i = 0; i <= n; i++) {
        const t = L * i / n, x = x1 + ux * t, y = y1 + uy * t;
        if (i > 0 && i < n) parts.push(`<path d="${star(R, x, y)}"/><circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="4" fill="${G}" stroke="none"/>`);
        if (i < n) { const a = t + (i ? R + 6 : 34), b = L * (i + 1) / n - (i + 1 < n ? R + 6 : 34); parts.push(`<path d="M${(x1 + ux * a).toFixed(1)},${(y1 + uy * a).toFixed(1)} L${(x1 + ux * b).toFixed(1)},${(y1 + uy * b).toFixed(1)}"/>`); }
      }
    };
    run(B, B, 1000 - B, B); run(B, 1400 - B, 1000 - B, 1400 - B); run(B, B, B, 1400 - B); run(1000 - B, B, 1000 - B, 1400 - B);
    const corner = (x, y) => `<g><path d="${star(30, x, y)}" fill="#f3d8cc"/><path d="${star(18, x, y)}"/><circle cx="${x}" cy="${y}" r="5" fill="${G}" stroke="none"/></g>`;
    const clasp = (x, y) => `<g><circle cx="${x}" cy="${y}" r="44" fill="#f3d8cc" stroke="none"/><path d="${star(42, x, y)}" stroke-width="3"/><path d="${star(26, x, y)}"/><circle cx="${x}" cy="${y}" r="8" fill="${G}" stroke="none"/></g>`;
    const evStar = `<svg viewBox="-20 -20 40 40"><path d="${star(17)}" fill="none" stroke="#8a5a2a" stroke-width="2.4"/><circle r="4" fill="#8a5a2a"/></svg>`;
    return `
    <div class="layer paper"></div>
    <div class="layer tint"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <defs>
        <linearGradient id="a2gold" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1000" y2="1400"><stop offset="0" stop-color="#7e561c"/><stop offset=".18" stop-color="#c39a48"/><stop offset=".36" stop-color="#8c6326"/><stop offset=".52" stop-color="#cfa755"/><stop offset=".7" stop-color="#875f22"/><stop offset=".86" stop-color="#bd9142"/><stop offset="1" stop-color="#73501a"/></linearGradient>
      </defs>
      <g fill="none" stroke="${G}" stroke-linejoin="round">
        <rect x="30" y="30" width="940" height="1340" stroke-width="5"/>
        <rect x="40" y="40" width="920" height="1320" stroke-width="1.8"/>
        <rect x="100" y="100" width="800" height="1200" stroke-width="1.8"/>
        <rect x="110" y="110" width="780" height="1180" stroke-width="4.5"/>
        <g stroke-width="2.3">${parts.join("")}</g>
        <g stroke-width="2.5">${clasp(500, 105)}${clasp(500, 1295)}${corner(B, B)}${corner(1000 - B, B)}${corner(B, 1400 - B)}${corner(1000 - B, 1400 - B)}</g>
      </g>
    </svg></div>
    <div class="tb" style="top: ${206 - 30 * n}px">
      ${H.bism('class="bism"')}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="680"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="680"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="ev">${evStar}${H.f("event", "span", 'class="foil foil-deep"')}${evStar}</div>
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`;
  },
});
