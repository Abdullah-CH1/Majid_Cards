/* A4 - Haala : soft sage paper, a great gold halo (crowned by a crescent) encircling the names */
registerDesign({
  id: "a4-haala",
  name: "Haala",
  idea: "On soft sage paper, a great gold halo crowned with a slim crescent encircles the couple's names like a full moon, with every line of the invitation set large in deep green ink.",
  css: H => `
    [data-d="a4-haala"] { background: #dfe5d0; color: #1f2a1f; }
    [data-d="a4-haala"] .paper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: multiply; opacity: .22; filter: brightness(1.12) contrast(1.1); }
    [data-d="a4-haala"] .tint { background: radial-gradient(ellipse 120% 90% at 50% 50%, rgba(0,0,0,0) 60%, rgba(50,70,50,.16) 100%); }
    [data-d="a4-haala"] .bism { position: absolute; left: 0; right: 0; top: 64px; text-align: center; font-family: Amiri, serif; font-size: calc(48px * var(--kt)); line-height: 1.3; color: #1f2a1f; }
    [data-d="a4-haala"] .tb { left: 120px; right: 120px; top: 146px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="a4-haala"] .tb.mid { justify-content: center; }
    [data-d="a4-haala"] .hosts { font: 400 calc(42px * var(--kt))/1.2 'Gilda Display', serif; letter-spacing: .08em; text-transform: uppercase; color: #1f2a1f; }
    [data-d="a4-haala"] .inv { font: italic 400 calc(34px * var(--kt))/1.3 'Playfair Display', serif; margin-top: 6px; color: #1f2a1f; }
    [data-d="a4-haala"] .nm { font: 400 calc(132px * var(--kn))/1.0 'Alex Brush', cursive; white-space: nowrap; filter: drop-shadow(0 1px 0 rgba(50,40,10,.3)); }
    [data-d="a4-haala"] .with { font: italic 400 calc(44px * var(--kt))/1.1 'Playfair Display', serif; color: #1f2a1f; margin: 2px 0 4px; }
    [data-d="a4-haala"] .bp { font: italic 400 calc(34px * var(--kt))/1.3 'Playfair Display', serif; color: #1f2a1f; }
    [data-d="a4-haala"] .ev { font: 400 calc(50px * var(--kt))/1.1 'Gilda Display', serif; letter-spacing: .16em; margin-right: -.16em; text-transform: uppercase; margin-top: 16px; filter: drop-shadow(0 1px 0 rgba(50,40,10,.25)); }
    [data-d="a4-haala"] .dt { font: 400 calc(42px * var(--kt))/1.25 'Playfair Display', serif; color: #1f2a1f; }
    [data-d="a4-haala"] .vn { font: 500 calc(38px * var(--kt))/1.32 'Playfair Display', serif; margin-top: 6px; color: #1f2a1f; }
    [data-d="a4-haala"] .vn .pl { font-weight: 400; font-size: .95em; }
    [data-d="a4-haala"] .rs { font: italic 400 calc(34px * var(--kt))/1.3 'Playfair Display', serif; margin-top: 4px; color: #1f2a1f; }
    [data-d="a4-haala"] .ur { font-size: calc(38px * var(--kt)); line-height: 1.85; color: #1f2a1f; margin-top: 2px; }
  `,
  render: (H, D) => {
    // an RSVP line needs room at the foot, so the halo shrinks a little when it is filled
    const rs = H.has("rsvp") ? 1 : 0, G = "url(#a4gold)", cy = 700 - 10 * rs, R = 356 - 22 * rs;
    const beads = Array.from({ length: 72 }, (_, i) => {
      const a = (i * 5 - 90) * Math.PI / 180;
      if (i * 5 < 11 || i * 5 > 349) return "";      // leave room for the crescent
      const r = R + 17, big = i % 3 === 0;
      return `<circle cx="${(500 + Math.cos(a) * r).toFixed(1)}" cy="${(cy + Math.sin(a) * r).toFixed(1)}" r="${big ? 4.4 : 2.6}"/>`;
    }).join("");
    const gap = 8 * Math.PI / 180;           // ring opening at the top for the crescent
    const arc = (r) => { const x1 = 500 + Math.sin(gap) * r, y1 = cy - Math.cos(gap) * r, x2 = 500 - Math.sin(gap) * r; return `M${x1.toFixed(1)},${y1.toFixed(1)} A${r},${r} 0 1 1 ${x2.toFixed(1)},${y1.toFixed(1)}`; };
    const corner = (x, y, sx, sy) => `<g transform="translate(${x},${y}) scale(${sx},${sy})"><path d="M0,70 A70,70 0 0 0 70,0" stroke-width="2.4"/><path d="M0,40 A40,40 0 0 0 40,0" stroke-width="2.4"/><circle cx="0" cy="0" r="6" fill="${G}" stroke="none"/></g>`;
    return `
    <div class="layer paper"></div>
    <div class="layer tint"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <defs>
        <linearGradient id="a4gold" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1000" y2="1400"><stop offset="0" stop-color="#7a561a"/><stop offset=".18" stop-color="#bf9442"/><stop offset=".34" stop-color="#876020"/><stop offset=".5" stop-color="#c9a24e"/><stop offset=".66" stop-color="#835c1e"/><stop offset=".82" stop-color="#b98d3c"/><stop offset="1" stop-color="#714e17"/></linearGradient>
        <radialGradient id="a4glow"><stop offset="0" stop-color="#fcfaf0" stop-opacity=".96"/><stop offset=".7" stop-color="#f8f6ea" stop-opacity=".86"/><stop offset="1" stop-color="#f0f0e2" stop-opacity=".5"/></radialGradient>
      </defs>
      <circle cx="500" cy="${cy}" r="${R - 6}" fill="url(#a4glow)"/>
      <g fill="none" stroke="${G}">
        <rect x="32" y="32" width="936" height="1336" stroke-width="5"/>
        <rect x="46" y="46" width="908" height="1308" stroke-width="2"/>
        ${corner(46, 46, 1, 1)}${corner(954, 46, -1, 1)}${corner(46, 1354, 1, -1)}${corner(954, 1354, -1, -1)}
        <path d="${arc(R)}" stroke-width="5.5"/>
        <path d="${arc(R - 13)}" stroke-width="2"/>
      </g>
      <g fill="${G}">${beads}</g>
      <defs><mask id="a4moon" maskUnits="userSpaceOnUse" x="-60" y="-60" width="120" height="120"><circle r="30" fill="#fff"/><circle cx="10" cy="-13" r="25" fill="#000"/></mask></defs>
      <g transform="translate(500,${cy - R + 4})">
        <circle r="30" fill="${G}" mask="url(#a4moon)"/>
        <path d="M0,-11 L2.9,-3.4 L10.9,-3.4 L4.5,1.4 L6.8,9.2 L0,4.6 L-6.8,9.2 L-4.5,1.4 L-10.9,-3.4 L-2.9,-3.4Z" fill="${G}" transform="translate(8,-14)"/>
      </g>
    </svg></div>
    ${H.bism()}
    <div class="tb">
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
    </div>
    <div class="tb mid" style="top: ${cy - R + 24}px; height: ${2 * R - 48}px">
      ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="600"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="600"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      ${H.f("event", "div", 'class="ev foil foil-deep"')}
    </div>
    <div class="tb" style="top: ${cy + R + 36}px">
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`;
  },
});
