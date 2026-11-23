/* A3 - Jharoka : a gold cusped Mughal window opening onto a 19th-c. painting of the Taj Mahal, navy ink below */
registerDesign({
  id: "a3-jharoka",
  name: "Jharoka",
  idea: "A bold gold Mughal window opens onto a fine 19th-century painting of the Taj Mahal, and the invitation is set beneath it in large, deep navy lettering, like a page from a royal album.",
  css: H => {
    return `
    [data-d="a3-jharoka"] { background: #f5efe3; color: #1c2340; }
    [data-d="a3-jharoka"] .paper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: multiply; opacity: .22; filter: brightness(1.1) contrast(1.08); }
    [data-d="a3-jharoka"] .tint { background:
        radial-gradient(ellipse 60% 42% at 50% 68%, rgba(255,252,245,.8), rgba(255,252,245,0) 75%),
        radial-gradient(ellipse 120% 90% at 50% 50%, rgba(0,0,0,0) 62%, rgba(60,60,90,.13) 100%); }
    [data-d="a3-jharoka"] .win { background: #ebe6d6; }
    [data-d="a3-jharoka"] .win i { position: absolute; inset: 0; background: url(${H.img("taj-mahal-elevation-painting.webp")}) no-repeat; filter: contrast(1.22) saturate(1.1); }
    [data-d="a3-jharoka"] .bism { position: absolute; left: 0; right: 0; top: 54px; text-align: center; font-family: Amiri, serif; font-size: calc(48px * var(--kt)); line-height: 1.3; color: #1c2340; }
    [data-d="a3-jharoka"] .tb { left: 140px; right: 140px; top: 550px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="a3-jharoka"] .hosts { font: 400 calc(42px * var(--kt))/1.2 Marcellus, serif; letter-spacing: .07em; text-transform: uppercase; color: #1c2340; }
    [data-d="a3-jharoka"] .inv { font: italic 400 calc(34px * var(--kt))/1.32 Lora, serif; margin-top: 8px; color: #1c2340; }
    [data-d="a3-jharoka"] .nm { font: 400 calc(130px * var(--kn))/1.0 Parisienne, cursive; white-space: nowrap; filter: drop-shadow(0 1px 0 rgba(60,40,10,.28)); }
    [data-d="a3-jharoka"] .nm.g { margin-top: 12px; }
    [data-d="a3-jharoka"] .with { font: italic 400 calc(44px * var(--kt))/1.1 Lora, serif; color: #1c2340; margin: 0 0 2px; }
    [data-d="a3-jharoka"] .bp { font: italic 400 calc(34px * var(--kt))/1.3 Lora, serif; color: #1c2340; }
    [data-d="a3-jharoka"] .ev { display: flex; align-items: center; gap: 18px; margin-top: 12px; }
    [data-d="a3-jharoka"] .ev .f { font: 400 calc(48px * var(--kt))/1.15 Marcellus, serif; letter-spacing: .16em; margin-right: -.16em; text-transform: uppercase; filter: drop-shadow(0 1px 0 rgba(60,40,10,.25)); }
    [data-d="a3-jharoka"] .ev i { width: 12px; height: 12px; background: #8a6420; transform: rotate(45deg); }
    [data-d="a3-jharoka"] .dt { font: 400 calc(42px * var(--kt))/1.25 Marcellus, serif; margin-top: 10px; color: #1c2340; }
    [data-d="a3-jharoka"] .vn { font: 500 calc(39px * var(--kt))/1.3 Lora, serif; margin-top: 4px; color: #1c2340; }
    [data-d="a3-jharoka"] .vn .pl { font-weight: 400; font-size: .94em; }
    [data-d="a3-jharoka"] .rs { font: italic 400 calc(34px * var(--kt))/1.3 Lora, serif; margin-top: 4px; color: #1c2340; }
    [data-d="a3-jharoka"] .ur { font-size: calc(38px * var(--kt)); line-height: 1.85; color: #1c2340; margin-top: 2px; }
  `;
  },
  render: (H, D) => {
    const G = "url(#a3gold)";
    // optional lines (bride's parents, RSVP) shorten the window so everything still fits
    const n = (H.has("brideParents") ? 1 : 0) + (H.has("rsvp") ? 1 : 0), up = 44 * n;
    const base = 518 - up;
    const o1 = H.archD(250, 500, 418, base, .55, 7, true);
    const inner = H.archD(262, 476, 418, base - 12, .55, 7);
    const sc = (520 - 40 * n) / 2000, px = 500 - 1000 * sc, py = 179 - 110 * sc;       // Taj painting placement
    const m = `linear-gradient(180deg, transparent ${(py + 88 * sc).toFixed(0)}px, #000 ${(py + 88 * sc + 5).toFixed(0)}px, #000 ${base - 56 + 10 * n}px, transparent ${base - 24 + 7 * n}px)`;
    const fr = (i, r) => `M${i + r},${i} H${1000 - i - r} A${r},${r} 0 0 0 ${1000 - i},${i + r} V${1400 - i - r} A${r},${r} 0 0 0 ${1000 - i - r},${1400 - i} H${i + r} A${r},${r} 0 0 0 ${i},${1400 - i - r} V${i + r} A${r},${r} 0 0 0 ${i + r},${i}Z`;
    return `
    <div class="layer paper"></div>
    <div class="layer tint"></div>
    <div class="layer win" style="clip-path: path('${inner}')"><i style="background-size: ${(2000 * sc).toFixed(1)}px auto; background-position: ${px.toFixed(1)}px ${py.toFixed(1)}px; -webkit-mask-image: ${m}; mask-image: ${m}"></i></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <defs>
        <linearGradient id="a3gold" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1000" y2="1400"><stop offset="0" stop-color="#7f5a1c"/><stop offset=".18" stop-color="#c49a45"/><stop offset=".34" stop-color="#8f6824"/><stop offset=".5" stop-color="#d0aa55"/><stop offset=".66" stop-color="#8a6322"/><stop offset=".82" stop-color="#bf9440"/><stop offset="1" stop-color="#76521a"/></linearGradient>
      </defs>
      <defs><clipPath id="a3win"><path d="${inner}"/></clipPath><filter id="a3blur" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="10"/></filter></defs>
      <g clip-path="url(#a3win)"><path d="${inner}" fill="none" stroke="rgba(90,70,40,.42)" stroke-width="26" filter="url(#a3blur)"/></g>
      <g fill="none" stroke="${G}">
        <path d="${fr(32, 34)}" stroke-width="5"/>
        <path d="${fr(46, 22)}" stroke-width="2"/>
        <path d="${inner}" stroke-width="2"/>
        <path d="${o1}" stroke-width="5"/>
        <path d="M206,${base} H794" stroke-width="5"/>
        <path d="M228,${base + 11} H772" stroke-width="2"/>
      </g>
      <g fill="${G}">
        <rect x="193" y="${base - 9}" width="18" height="18" transform="rotate(45 202 ${base})"/><rect x="789" y="${base - 9}" width="18" height="18" transform="rotate(45 798 ${base})"/>
        ${[[500, 32], [500, 1368]].map(([x, y]) => `<rect x="${x - 10}" y="${y - 10}" width="20" height="20" transform="rotate(45 ${x} ${y})" stroke="#f5efe3" stroke-width="5" paint-order="stroke"/>`).join("")}
      </g>
    </svg></div>
    ${H.bism()}
    <div class="tb" style="top: ${550 - up}px">
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="730"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="730"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="ev"><i></i>${H.f("event", "span", 'class="foil foil-deep"')}<i></i></div>
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`;
  },
});
