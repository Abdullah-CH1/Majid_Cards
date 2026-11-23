/* C1 - Muraqqa : a Shah Jahan Album page - gold-sprinkled (zar-afshan) buff margins, bands of coloured rulings, gold corner illumination, ivory panel */
registerDesign({
  id: "c1-muraqqa",
  name: "Muraqqa",
  idea: "A page from the Shah Jahan Album: buff margins sprinkled with flakes of gold leaf (zar-afshan), a calm ivory panel framed by bands of gold, lapis and vermilion rulings with gilded geometric corner pieces, and the names written in deep gold.",
  css: H => {
    const P = '[data-d="c1-muraqqa"]';
    return `
    ${P} { background: #b48a5c; color: #2b1d12; }
    ${P} .buff { background: radial-gradient(ellipse 80% 70% at 50% 50%, #bc9264, #ab8053 100%); }
    ${P} .grain { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: multiply; opacity: .5; filter: contrast(1.4); }
    ${P} .panel { position: absolute; left: 112px; top: 112px; width: 776px; height: 1176px; background: #f6eedc;
        box-shadow: 0 2px 12px rgba(60,35,10,.3); }
    ${P} .panel::before { content: ""; position: absolute; inset: 0; background: url(${H.img("textured-ivory-paper.webp")}) center/cover;
        mix-blend-mode: multiply; opacity: .3; filter: brightness(1.12) contrast(1.15); }
    ${P} .panel::after { content: ""; position: absolute; inset: 0;
        background: radial-gradient(ellipse 70% 60% at 50% 45%, rgba(255,251,240,.55), rgba(255,251,240,0) 75%),
                    radial-gradient(ellipse 110% 100% at 50% 50%, transparent 62%, rgba(150,110,60,.16)); }
    ${P} .tb { left: 150px; right: 150px; top: calc(178px - 16px * var(--x, 0)); text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(48px * var(--kt)); line-height: 1.2; color: #5e4210; }
    ${P} .hosts { white-space: nowrap; font: 600 calc(46px * var(--kt))/1.2 'Cormorant SC', serif; letter-spacing: .05em; margin-top: 32px; color: #2b1d12; }
    ${P} .inv { font: italic 500 calc(39px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 10px; color: #2b1d12; }
    ${P} .nm { font: 400 calc(140px * var(--kn) * (1 - .03 * var(--x, 0)))/1.12 'Great Vibes', cursive; white-space: nowrap;
        --foil: linear-gradient(100deg,#5a3e0e 0%,#8a6620 22%,#a8822f 36%,#6e4f15 54%,#977226 72%,#553a0c 100%);
        filter: drop-shadow(0 1px 0 rgba(60,40,10,.3)); }
    ${P} .nm.g { margin-top: calc(24px - 8px * var(--x, 0)); }
    ${P} .with { font: italic 500 calc(46px * var(--kt))/1 'Cormorant Garamond', serif; color: #2b1d12; margin: -4px 0 0; }
    ${P} .bp { font: italic 500 calc(34px * var(--kt))/1.25 'Cormorant Garamond', serif; color: #2b1d12; margin-top: 4px; }
    ${P} .ev { display: flex; align-items: center; gap: 16px; margin-top: calc(30px - 7px * var(--x, 0)); }
    ${P} .ev .f { font: 600 calc(50px * var(--kt))/1.1 Cinzel, serif; letter-spacing: .16em; margin-right: -.16em; color: #1c2a5a; }
    ${P} .ev i { display: block; width: 13px; height: 13px; background: #a8432c; transform: rotate(45deg); flex: none; }
    ${P} .ev b { display: block; width: 70px; height: 3px; background: linear-gradient(90deg, rgba(122,90,24,0), #7a5a18); flex: none; }
    ${P} .ev b.r { background: linear-gradient(270deg, rgba(122,90,24,0), #7a5a18); }
    ${P} .dt { font: 400 calc(44px * var(--kt))/1.25 Marcellus, serif; margin-top: 16px; color: #2b1d12; white-space: nowrap; }
    ${P} .vn { font: 600 calc(42px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 10px; color: #2b1d12; }
    ${P} .vn .pl { font-size: .92em; }
    ${P} .rs { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 4px; color: #2b1d12; }
    ${P} .ur { font-size: calc(40px * var(--kt)); line-height: calc(1.9 - .2 * var(--x, 0)); color: #2b1d12; margin-top: calc(12px - 6px * var(--x, 0)); }
  `;
  },
  render: (H, D) => {
    const x = 112, y = 112, w = 776, h = 1176;
    const r = (o, sw, st) => `<rect x="${x - o}" y="${y - o}" width="${w + 2 * o}" height="${h + 2 * o}" fill="none" stroke="${st}" stroke-width="${sw}"/>`;
    const inner = (o, sw, st) => `<rect x="${x + o}" y="${y + o}" width="${w - 2 * o}" height="${h - 2 * o}" fill="none" stroke="${st}" stroke-width="${sw}"/>`;
    /* zar-afshan: deterministic flakes of gold leaf scattered over the margin only */
    let seed = 7;
    const rnd = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
    const golds = ["#f3dc96", "#e2c477", "#d1ad5c", "#f8e8b4", "#c49a48"];
    let flakes = "";
    for (let n = 0; n < 3200; n++) {
      const px = rnd() * 1000, py = rnd() * 1400;
      if (px > x - 30 && px < x + w + 30 && py > y - 30 && py < y + h + 30) continue;
      if (px < 26 || px > 974 || py < 26 || py > 1374) continue;
      const big = rnd() < .1, s = big ? 3.5 + rnd() * 3.5 : 1.5 + rnd() * 2.8, k = 4 + Math.floor(rnd() * 3);
      let d = "";
      for (let i = 0; i < k; i++) { const ang = (i / k) * 6.283 + rnd() * .8, rr = s * (.55 + rnd() * .6); d += (i ? "L" : "M") + (px + rr * Math.cos(ang)).toFixed(1) + "," + (py + rr * Math.sin(ang)).toFixed(1); }
      flakes += `<path d="${d}Z" fill="${golds[Math.floor(rnd() * golds.length)]}" opacity="${(.7 + rnd() * .3).toFixed(2)}"/>`;
    }
    /* gilded geometric corner piece (lachak): stepped triangle with an eight-point star, lapis ground */
    const corner = (cx, cy, sx, sy) => {
      const L = 110, c = L * .3;
      const t = `transform="translate(${cx} ${cy}) scale(${sx} ${sy})"`;
      let st = "";
      for (let i = 0; i < 16; i++) { const ang = Math.PI * i / 8 - Math.PI / 2, rr = i % 2 ? 12 : 20; st += (i ? "L" : "M") + (c + rr * Math.cos(ang)).toFixed(1) + "," + (c + rr * Math.sin(ang)).toFixed(1); }
      return `<g ${t}>
        <path d="M0,0 H${L} Q${L * .55},${L * .12} ${L * .42},${L * .42} Q${L * .12},${L * .55} 0,${L} Z" fill="#1f3366"/>
        <path d="M0,0 H${L} Q${L * .55},${L * .12} ${L * .42},${L * .42} Q${L * .12},${L * .55} 0,${L} Z" fill="none" stroke="url(#gold)" stroke-width="3.5" stroke-linejoin="round"/>
        <path d="${st}Z" fill="url(#gold)" stroke="#5e4210" stroke-width="1"/>
        <circle cx="${c}" cy="${c}" r="6.5" fill="#a8432c" stroke="#5e4210" stroke-width="1"/>
        <path d="M${L * .62},${L * .1} l7,7 l-7,7 l-7,-7z M${L * .1},${L * .62} l7,7 l-7,7 l-7,-7z" fill="url(#gold)" stroke="#5e4210" stroke-width=".8"/>
      </g>`;
    };
    const ix = x + 14, iy = y + 14, iw = w - 28, ih = h - 28;
    return `
    <div class="layer buff"></div>
    <div class="layer grain"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g>${flakes}</g>
      <rect x="26" y="26" width="948" height="1348" fill="none" stroke="url(#gold)" stroke-width="5"/>
      <rect x="36" y="36" width="928" height="1328" fill="none" stroke="#1f3366" stroke-width="2"/>
    </svg></div>
    <div class="panel"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      ${r(22, 2, "#a8432c")}
      ${r(13, 10, "#1f3366")}
      ${r(13, 2, "url(#goldBright)")}
      ${r(4, 6, "url(#gold)")}
      ${r(0.6, 1.5, "#3a2614")}
      ${inner(14, 2, "#7a5a18")}
      ${corner(ix, iy, 1, 1)}${corner(ix + iw, iy, -1, 1)}${corner(ix, iy + ih, 1, -1)}${corner(ix + iw, iy + ih, -1, -1)}
    </svg></div>
    <div class="tb" style="--x:${(H.has("brideParents") ? 1 : 0) + (H.has("rsvp") ? 1 : 0)}">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts" data-fit="640"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil" data-fit="660"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil" data-fit="660"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="ev"><b></b><i></i>${H.f("event")}<i></i><b class="r"></b></div>
      <div class="dt" data-fit="660">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`;
  },
});
