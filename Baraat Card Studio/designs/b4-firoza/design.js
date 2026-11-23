/* B4 - Firoza: deep turquoise card with two gold geometric illumination margins (interlaced ogee lattice and eight-point stars), serif-caps names. */
registerDesign({
  id: "b4-firoza",
  name: "Firoza",
  idea: "A deep turquoise field between two illuminated margins of interlaced gold ogee lattice and eight-pointed stars, like the gilded tile and manuscript borders of Isfahan and Lahore, with the names set in stately gold capitals.",
  css: H => {
    const P = '[data-d="b4-firoza"]';
    return `
    ${P} { background: #0c3237; color: #f7efdc; }
    ${P} .gr { background:
        radial-gradient(ellipse 55% 42% at 50% 45%, rgba(34,96,100,.6), transparent 75%),
        linear-gradient(180deg, #0f383d 0%, #0b2d32 100%); }
    ${P} .gr::after { content: ""; position: absolute; inset: 0; opacity: .26;
        background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: soft-light; }
    ${P} .tb { left: 166px; right: 166px; top: calc(152px - 14px * var(--x, 0)); text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(48px * var(--kt)); line-height: 1.2; color: #f1d98f; }
    ${P} .hosts { white-space: nowrap; font: 400 calc(46px * var(--kt))/1.2 'Gilda Display', serif; letter-spacing: .03em; margin-top: 36px; color: #f7efdc; }
    ${P} .inv { font: italic 500 calc(39px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 12px; color: #f7efdc; }
    ${P} .nm { font: 600 calc(94px * var(--kn))/1.08 'Cormorant Garamond', serif; letter-spacing: .04em; text-transform: uppercase; white-space: nowrap;
        filter: drop-shadow(0 2px 0 rgba(0,20,22,.55)); }
    ${P} .nm.g { margin-top: calc(50px - 12px * var(--x, 0)); }
    ${P} .with { font: 400 calc(66px * var(--kt))/1 'Great Vibes', cursive; color: #f1d98f; margin: 0 0 4px; }
    ${P} .bp { font: italic 500 calc(34px * var(--kt))/1.25 'Cormorant Garamond', serif; color: #f7efdc; margin-top: 6px; }
    ${P} .rule { width: 300px; height: 30px; margin-top: calc(46px - 12px * var(--x, 0)); overflow: visible; }
    ${P} .ev { font: 400 calc(92px * var(--kt))/1.05 'Great Vibes', cursive; margin-top: 12px; }
    ${P} .dt { font: 400 calc(44px * var(--kt))/1.25 'Gilda Display', serif; margin-top: 14px; color: #f7efdc; white-space: nowrap; }
    ${P} .vn { font: 600 calc(42px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 12px; color: #f7efdc; }
    ${P} .vn .pl { font-size: .92em; }
    ${P} .ur { font-size: calc(40px * var(--kt)); line-height: 1.9; color: #f7efdc; margin-top: 16px; }
    ${P} .rs { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #f7efdc; margin-top: 4px; }
  `;
  },
  render: (H, D) => {
    /* one illuminated margin band: interlaced ogee lattice (double gold line), roundels at the crossings, eight-point stars in the cells */
    const bx0 = 50, W = 96, y0 = 50, y1 = 1350, Pp = 162, a = 54;
    const ogee = (cx, yt) => {
      const r = s => (cx + s * a).toFixed(1), y = t => (yt + t * Pp).toFixed(1);
      const half = s => `C${cx},${y(.12)} ${r(s * .5)},${y(.15)} ${r(s * .8)},${y(.3)} C${r(s * 1.04)},${y(.43)} ${r(s * 1.04)},${y(.57)} ${r(s * .8)},${y(.7)} C${r(s * .5)},${y(.85)} ${cx},${y(.88)} ${cx},${y(1)}`;
      return `M${cx},${y(0)} ${half(1)} M${cx},${y(0)} ${half(-1)}`;
    };
    const star = (cx, cy, R) => {
      let d = "";
      for (let i = 0; i < 16; i++) { const ang = Math.PI * i / 8 - Math.PI / 2, rr = i % 2 ? R * .62 : R; d += (i ? "L" : "M") + (cx + rr * Math.cos(ang)).toFixed(1) + "," + (cy + rr * Math.sin(ang)).toFixed(1); }
      return d + "Z";
    };
    const band = (bx, id) => {
      const cx = bx + W / 2, start = 700 - Pp * 5;
      let lat = "", stars = "", rings = "";
      for (let k = 0; k < 10; k++) {
        const yt = start + k * Pp;
        lat += ogee(cx, yt) + " " + ogee(bx, yt - Pp / 2) + " " + ogee(bx + W, yt - Pp / 2) + " ";
        stars += `<path d="${star(cx, yt + Pp / 2, 17)}"/>`;
        rings += `<circle cx="${cx}" cy="${yt}" r="13"/>`;
      }
      return `
        <clipPath id="${id}"><rect x="${bx}" y="${y0}" width="${W}" height="${y1 - y0}"/></clipPath>
        <rect x="${bx}" y="${y0}" width="${W}" height="${y1 - y0}" fill="#082427" opacity=".72"/>
        <g clip-path="url(#${id})" fill="none" stroke-linejoin="round">
          <path d="${lat}" stroke="url(#goldBright)" stroke-width="8"/>
          <path d="${lat}" stroke="#0b2b2f" stroke-width="3.2"/>
          <g fill="#0b2b2f" stroke="url(#goldBright)" stroke-width="2.5">${rings}</g>
          <g fill="url(#goldBright)">${rings.replace(/r="13"/g, 'r="4.5"')}</g>
          <g stroke="url(#goldBright)" stroke-width="2.5">${stars}</g>
        </g>
        <rect x="${bx}" y="${y0}" width="${W}" height="${y1 - y0}" fill="none" stroke="url(#goldBright)" stroke-width="2.5"/>`;
    };
    return `
    <div class="layer gr"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <defs></defs>
      ${band(bx0, "b4cl")}
      ${band(1000 - bx0 - W, "b4cr")}
      ${[y0, y1 - 46].map(fy => {
        const fx = bx0 + W, fw = 1000 - 2 * fx, cy = fy + 23;
        let s = "";
        for (let i = 0; i < 9; i++) { const sx = fx + fw * (i + .5) / 9; s += `<path d="${star(sx, cy, 13)}"/>`; if (i) s += `<path d="M${(sx - fw / 18).toFixed(1)},${cy - 6} l6,6 l-6,6 l-6,-6z" fill="url(#goldBright)" stroke="none"/>`; }
        return `<rect x="${fx}" y="${fy}" width="${fw}" height="46" fill="#082427" opacity=".72"/>
          <g fill="none" stroke="url(#goldBright)" stroke-width="2.5">${s}<rect x="${fx}" y="${fy}" width="${fw}" height="46"/></g>`;
      }).join("")}
      <g fill="none" stroke="url(#goldBright)">
        <rect x="30" y="30" width="940" height="1340" stroke-width="5"/>
        <rect x="40" y="40" width="920" height="1320" stroke-width="1.8"/>
      </g>
    </svg></div>
    <div class="tb" style="--x:${(H.has("brideParents") ? 1 : 0) + (H.has("rsvp") ? 1 : 0)}">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts" data-fit="620"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-light" data-fit="660"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-light" data-fit="660"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <svg class="rule" viewBox="0 0 300 30"><g fill="none" stroke="#f1d98f" stroke-width="2.5"><path d="M0,15 H118"/><path d="M182,15 H300"/><path d="${star(150, 15, 15)}"/></g><circle cx="150" cy="15" r="3.5" fill="#f1d98f"/></svg>
      ${H.f("event", "div", 'class="ev foil foil-light"')}
      <div class="dt" data-fit="660">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;&middot;&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`;
  },
});
