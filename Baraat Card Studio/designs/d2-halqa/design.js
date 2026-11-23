/* D2 Halqa - an antique engraved flower wreath in gold, ringing the couple's initials, over classical serif typography (round 2: big Bodoni capitals, solid ink, bold foil frame) */
registerDesign({
  id: "d2-halqa",
  name: "Halqa",
  idea: "A 19th-century engraved flower wreath, printed in antique gold, rings the couple's initials like a family crest - with large classic Bodoni lettering below on warm ivory cotton.",
  css: H => {
    const P = '[data-d="d2-halqa"]';
    const ww = 480;
    return `
    ${P} { background: #f7f1e6; color: #2b1d12; }
    ${P} .paper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; filter: saturate(0) contrast(.42) brightness(1.52); mix-blend-mode: multiply; opacity: .5; }
    ${P} .tb { left: 100px; right: 100px; top: 92px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(46px * var(--kt)); font-weight: 700; color: #5e4416; line-height: 1.25; }
    ${P} .tb { --ww: ${ww}px; }
    ${P} .tb:has(.bp), ${P} .tb:has(.rs) { --ww: ${ww - 40}px; }
    ${P} .tb:has(.bp):has(.rs) { --ww: ${ww - 80}px; }
    ${P} .wr { position: relative; width: var(--ww); height: calc(var(--ww) * ${(1145 / 1578).toFixed(4)}); flex: none; margin-top: 6px;
        background: url(${H.img("engraved-flower-wreath-gold-cut.png")}) center/contain no-repeat; filter: brightness(.72) saturate(1.35) contrast(1.2); }
    ${P} .mono { width: var(--ww); height: calc(var(--ww) * ${(1145 / 1578).toFixed(4)}); margin-top: calc(var(--ww) * ${(-1145 / 1578).toFixed(4)}); flex: none; display: flex; align-items: center; justify-content: center; padding: 0 0 6px 6px; }
    ${P} .mono .ml { font: 400 calc(100px * var(--kn))/1 'Bodoni Moda', serif; filter: drop-shadow(0 1px 0 rgba(60,40,10,.3)); }
    ${P} .mono .md { font: italic 400 calc(52px * var(--kn))/1 'Bodoni Moda', serif; color: #6e5018; margin: 18px 10px 0; }
    ${P} .hosts { font: 500 calc(42px * var(--kt))/1.2 'Bodoni Moda', serif; letter-spacing: .08em; text-transform: uppercase; margin-top: 10px; }
    ${P} .inv { font: italic 400 calc(35px * var(--kt))/1.28 'Bodoni Moda', serif; margin-top: 6px; color: #2b1d12; }
    ${P} .nm { font: 500 calc(88px * var(--kn))/1.12 'Bodoni Moda', serif; letter-spacing: .07em; text-transform: uppercase; white-space: nowrap; margin-left: .07em; color: #24180e; }
    ${P} .nm.g { margin-top: 14px; }
    ${P} .with { font: 400 calc(60px * var(--kt))/.9 'Great Vibes', cursive; color: #58400f; margin: 0 0 2px; }
    ${P} .bp { font: italic 400 calc(34px * var(--kt))/1.3 'Bodoni Moda', serif; color: #2b1d12; margin-top: 4px; }
    ${P} .evrow { display: flex; align-items: center; gap: 22px; margin-top: 18px; color: #8a6420; }
    ${P} .evrow i { display: block; width: 90px; height: 2.5px; background: currentColor; }
    ${P} .ev { font: 500 calc(46px * var(--kt))/1 'Bodoni Moda', serif; letter-spacing: .16em; margin-left: .16em; text-transform: uppercase; color: #6a4c16; }
    ${P} .dt { font: 500 calc(42px * var(--kt))/1.25 'Bodoni Moda', serif; margin-top: 16px; }
    ${P} .tm { font: italic 400 calc(40px * var(--kt))/1.25 'Bodoni Moda', serif; margin-top: 2px; color: #2b1d12; }
    ${P} .vn { font: 500 calc(38px * var(--kt))/1.3 'Bodoni Moda', serif; letter-spacing: .06em; text-transform: uppercase; margin-top: 10px; }
    ${P} .vn .pl { font-size: calc(34px * var(--kt)); letter-spacing: .05em; color: #2b1d12; }
    ${P} .ur { font-size: calc(38px * var(--kt)); line-height: 1.75; color: #4e3812; margin-top: 2px; }
    ${P} .rs { font: italic 400 calc(34px * var(--kt))/1.3 'Bodoni Moda', serif; color: #2b1d12; margin-top: 2px; }
  `;
  },
  render: (H, D) => `
    <div class="layer paper"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none">
        <rect x="40" y="40" width="920" height="1320" stroke="#8a6420" stroke-width="5"/>
        <rect x="40" y="40" width="920" height="1320" stroke="url(#gold)" stroke-width="3"/>
        <rect x="54" y="54" width="892" height="1292" stroke="#8a6420" stroke-width="2"/>
      </g>
      <g fill="#8a6420">
        ${[[40, 40], [960, 40], [40, 1360], [960, 1360]].map(([x, y]) => `<path d="M${x},${y - 12} L${x + 12},${y} L${x},${y + 12} L${x - 12},${y} Z"/>`).join("")}
      </g>
    </svg></div>
    <div class="tb">
      ${H.bism()}
      <div class="wr"></div>
      <div class="mono"><span class="ml foil foil-deep">${H.monoG()}</span><span class="md">&amp;</span><span class="ml foil foil-deep">${H.monoB()}</span></div>
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g" data-fit="780"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm" data-fit="780"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="evrow"><i></i>${H.f("event", "div", 'class="ev"')}<i></i></div>
      <div class="dt">${H.dateLine()}</div>
      ${H.f("time", "div", 'class="tm"')}
      <div class="vn">${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`,
});
