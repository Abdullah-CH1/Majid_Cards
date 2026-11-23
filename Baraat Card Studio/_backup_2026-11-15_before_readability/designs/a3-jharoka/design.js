/* A3 - Jharoka : a cusped Mughal window opening onto a hand-tinted lotus, text below */
registerDesign({
  id: "a3-jharoka",
  name: "Jharoka",
  idea: "A gold-rimmed Mughal window opens onto a softly hand-tinted lotus against a pale sky, with the invitation set beneath it like a page of a royal album.",
  css: H => {
    const win = H.archD(296, 408, 410, 680, .55, 7);
    return `
    [data-d="a3-jharoka"] { background: #f4ecdd; color: #3d2f22; }
    [data-d="a3-jharoka"] .paper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: multiply; opacity: .2; filter: brightness(1.13) contrast(1.05); }
    [data-d="a3-jharoka"] .tint { background:
        radial-gradient(ellipse 60% 40% at 50% 66%, rgba(255,251,242,.85), rgba(255,251,242,0) 75%),
        radial-gradient(ellipse 120% 90% at 50% 50%, rgba(0,0,0,0) 62%, rgba(110,80,40,.14) 100%); }
    [data-d="a3-jharoka"] .win { clip-path: path("${win}"); background: url(${H.img("lotus-ogawa-handcoloured-2.webp")}) no-repeat; background-size: 600px auto; background-position: 124px 84px; background-color: rgb(185,196,183); filter: saturate(.92) contrast(.98); }
        [data-d="a3-jharoka"] .bism { position: absolute; left: 0; right: 0; top: 60px; text-align: center; font-family: 'Scheherazade New', serif; font-size: calc(86px * var(--kt)); line-height: .9; color: #8a6526; }
    [data-d="a3-jharoka"] .tb { left: 150px; right: 150px; top: 724px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="a3-jharoka"] .hosts { font: 500 calc(29px * var(--kt))/1.2 'Cormorant SC', serif; letter-spacing: .1em; color: #3d2f22; }
    [data-d="a3-jharoka"] .inv { font: italic 400 calc(24px * var(--kt))/1.42 'Cormorant Garamond', serif; margin-top: 8px; color: #5a4632; }
    [data-d="a3-jharoka"] .nm { font: 400 calc(86px * var(--kn))/1.14 'Great Vibes', cursive; white-space: nowrap; }
    [data-d="a3-jharoka"] .nm.g { margin-top: 14px; }
    [data-d="a3-jharoka"] .with { font: italic 400 calc(26px * var(--kt))/1 'Cormorant Garamond', serif; color: #8d5f55; margin: 0 0 2px; }
    [data-d="a3-jharoka"] .bp { font: italic 400 calc(20px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #5a4632; }
    [data-d="a3-jharoka"] .ev { display: flex; align-items: center; gap: 14px; margin-top: 22px; }
    [data-d="a3-jharoka"] .ev .f { font: 500 calc(20px * var(--kt))/1 Cinzel, serif; letter-spacing: .5em; margin-right: -.5em; color: #95594d; }
    [data-d="a3-jharoka"] .ev i { width: 7px; height: 7px; background: #b48f4a; transform: rotate(45deg); }
    [data-d="a3-jharoka"] .dt { font: 500 calc(25px * var(--kt))/1.3 'Cormorant Garamond', serif; letter-spacing: .06em; margin-top: 14px; color: #3d2f22; }
    [data-d="a3-jharoka"] .vn { font: 400 calc(24px * var(--kt))/1.4 'Cormorant Garamond', serif; margin-top: 4px; color: #3d2f22; }
    [data-d="a3-jharoka"] .vn b { font-weight: 600; }
    [data-d="a3-jharoka"] .rs { font: italic 400 calc(20px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 6px; color: #5a4632; }
    [data-d="a3-jharoka"] .ur { font-size: calc(21px * var(--kt)); color: #7a5a22; margin-top: 4px; }
  `;
  },
  render: (H, D) => {
    const o1 = H.archD(284, 432, 410, 692, .55, 7, true);
    const o2 = H.archD(274, 452, 410, 692, .55, 7, true);
    const inner = H.archD(296, 408, 410, 680, .55, 7);
    const fr = (i, r) => `M${i + r},${i} H${1000 - i - r} A${r},${r} 0 0 0 ${1000 - i},${i + r} V${1400 - i - r} A${r},${r} 0 0 0 ${1000 - i - r},${1400 - i} H${i + r} A${r},${r} 0 0 0 ${i},${1400 - i - r} V${i + r} A${r},${r} 0 0 0 ${i + r},${i}Z`;
    return `
    <div class="layer paper"></div>
    <div class="layer tint"></div>
    <div class="layer win"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none" stroke="url(#gold)">
        <path d="${fr(38, 30)}" stroke-width="1.5"/>
        <path d="${fr(48, 22)}" stroke-width=".7"/>
        <path d="${inner}" stroke-width="1.2"/>
        <path d="${o1}" stroke-width="2"/>
        <path d="${o2}" stroke-width=".8"/>
        <path d="M214,692 H786" stroke-width="1.4"/>
        <path d="M244,700 H756" stroke-width=".6"/>
      </g>
      <g fill="url(#gold)">
        <rect x="205" y="687" width="10" height="10" transform="rotate(45 210 692)"/><rect x="785" y="687" width="10" height="10" transform="rotate(45 790 692)"/>
        ${[[38, 700], [962, 700]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="3"/>`).join("")}
        ${[[500, 38], [500, 1362]].map(([x, y]) => `<rect x="${x - 6}" y="${y - 6}" width="12" height="12" transform="rotate(45 ${x} ${y})" stroke="#f4ecdd" stroke-width="3" paint-order="stroke"/>`).join("")}
      </g>
      <defs>
        <clipPath id="a3fr"><path d="${fr(48, 22)}"/></clipPath>
        <clipPath id="a3win"><path d="${inner}"/></clipPath>
        <filter id="a3blur" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="9"/></filter>
      </defs>
      <g clip-path="url(#a3win)"><path d="${inner}" fill="none" stroke="rgba(70,80,78,.38)" stroke-width="22" filter="url(#a3blur)"/></g>
      <g clip-path="url(#a3fr)">
        <g transform="translate(48,48)" opacity=".42">${H.mandala(200, { sw: .8 })}</g>
        <g transform="translate(952,48)" opacity=".42">${H.mandala(200, { sw: .8 })}</g>
      </g>
    </svg></div>
    ${H.bism()}
    <div class="tb">
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="640"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="640"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="ev"><i></i>${H.f("event")}<i></i></div>
      <div class="dt">${H.dateLine()}</div>
      <div class="vn"><b>${H.f("time")}</b> &nbsp;·&nbsp; ${H.f("venue")}<br>${H.f("place")}</div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`;
  },
});
