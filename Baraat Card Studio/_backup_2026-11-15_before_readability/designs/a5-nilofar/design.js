/* A5 - Nilofar : a deckle-edged cotton card floating on a sage ground, with a hand-coloured water-lily plate */
registerDesign({
  id: "a5-nilofar",
  name: "Shabnam",
  idea: "A torn-edge cotton paper card floats on soft sage, a hand-coloured water lily blooming up from its corner and the names in gold foil.",
  css: H => {
    // deterministic deckle edge
    let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    const X0 = 78, Y0 = 84, X1 = 922, Y1 = 1316, st = 7, pts = [];
    const j = () => (rnd() * 3.6 + (rnd() < .12 ? 2.2 : 0)).toFixed(1);
    for (let x = X0; x < X1; x += st) pts.push(`${x}px ${(Y0 + +j()).toFixed(1)}px`);
    for (let y = Y0; y < Y1; y += st) pts.push(`${(X1 - j()).toFixed(1)}px ${y}px`);
    for (let x = X1; x > X0; x -= st) pts.push(`${x}px ${(Y1 - j()).toFixed(1)}px`);
    for (let y = Y1; y > Y0; y -= st) pts.push(`${(X0 + +j()).toFixed(1)}px ${y}px`);
    const poly = `polygon(${pts.join(",")})`;
    return `
    [data-d="a5-nilofar"] { background: #a9b39c; color: #2d3a2e; }
    [data-d="a5-nilofar"] .ground { background:
        radial-gradient(ellipse 70% 55% at 50% 45%, rgba(236,236,220,.35), rgba(236,236,220,0) 70%),
        radial-gradient(ellipse 120% 90% at 50% 50%, rgba(0,0,0,0) 55%, rgba(40,52,38,.35) 100%); }
    [data-d="a5-nilofar"] .gpaper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: multiply; opacity: .55; filter: contrast(1.2); }
    [data-d="a5-nilofar"] .lift { filter: drop-shadow(0 16px 22px rgba(35,48,32,.34)) drop-shadow(0 2px 3px rgba(35,48,32,.25)); }
    [data-d="a5-nilofar"] .sheet { clip-path: ${poly}; background: #f7f1e4; }
    [data-d="a5-nilofar"] .spaper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: multiply; opacity: .32; filter: brightness(1.12) contrast(1.08); }
    [data-d="a5-nilofar"] .sglow { background: radial-gradient(ellipse 60% 45% at 52% 40%, rgba(255,253,246,.75), rgba(255,253,246,0) 72%); }
    [data-d="a5-nilofar"] .wl { position: absolute; top: 66px; width: 340px; mix-blend-mode: multiply; filter: saturate(.8) brightness(1.1) contrast(.92);
        -webkit-mask-image: linear-gradient(180deg, #000 84%, rgba(0,0,0,0) 97%); mask-image: linear-gradient(180deg, #000 84%, rgba(0,0,0,0) 97%); }
    [data-d="a5-nilofar"] .wl.r { left: 602px; }
    [data-d="a5-nilofar"] .wl.l { left: 58px; transform: scaleX(-1); }
    [data-d="a5-nilofar"] .bism { position: absolute; left: 0; right: 0; top: 118px; text-align: center; font-family: 'Noto Nastaliq Urdu', serif; font-size: calc(40px * var(--kt)); line-height: 2.2; color: #8a6526; }
    [data-d="a5-nilofar"] .tb { left: 170px; right: 150px; top: 606px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="a5-nilofar"] .hosts { font: 400 calc(25px * var(--kt))/1.3 Cinzel, serif; letter-spacing: .14em; color: #2d3a2e; }
    [data-d="a5-nilofar"] .inv { font: italic 400 calc(24px * var(--kt))/1.45 'Bodoni Moda', serif; margin-top: 14px; color: #4a5a4a; }
    [data-d="a5-nilofar"] .nm { font: 400 calc(100px * var(--kn))/1.12 Allura, cursive; white-space: nowrap; }
    [data-d="a5-nilofar"] .nm.g { margin-top: 20px; }
    [data-d="a5-nilofar"] .with { font: italic 400 calc(26px * var(--kt))/1 'Bodoni Moda', serif; color: #8a6526; margin: 2px 0 6px; }
    [data-d="a5-nilofar"] .bp { font: italic 400 calc(20px * var(--kt))/1.3 'Bodoni Moda', serif; color: #4a5a4a; margin-top: 2px; }
    [data-d="a5-nilofar"] .ev { display: flex; align-items: center; gap: 18px; margin-top: 30px; color: #a8843f; }
    [data-d="a5-nilofar"] .ev .f { font: 400 calc(23px * var(--kt))/1 Cinzel, serif; letter-spacing: .5em; margin-right: -.5em; color: #7d5d22; }
    [data-d="a5-nilofar"] .dt { font: 400 calc(25px * var(--kt))/1.3 'Cormorant Garamond', serif; font-weight: 600; letter-spacing: .14em; text-transform: uppercase; margin-top: 16px; color: #2d3a2e; }
    [data-d="a5-nilofar"] .vn { font: italic 400 calc(25px * var(--kt))/1.45 'Bodoni Moda', serif; margin-top: 6px; color: #2d3a2e; }
    [data-d="a5-nilofar"] .rs { font: italic 400 calc(19px * var(--kt))/1.3 'Bodoni Moda', serif; margin-top: 8px; color: #4a5a4a; }
    [data-d="a5-nilofar"] .ur { font-size: calc(21px * var(--kt)); color: #7d5d22; margin-top: 4px; }
  `;
  },
  render: (H, D) => {
    const fr = (i, r) => `M${78 + i + r},${84 + i} H${922 - i - r} A${r},${r} 0 0 0 ${922 - i},${84 + i + r} V${1316 - i - r} A${r},${r} 0 0 0 ${922 - i - r},${1316 - i} H${78 + i + r} A${r},${r} 0 0 0 ${78 + i},${1316 - i - r} V${84 + i + r} A${r},${r} 0 0 0 ${78 + i + r},${84 + i}Z`;
    return `
    <div class="layer gpaper"></div>
    <div class="layer ground"></div>
    <div class="layer lift"><div class="layer sheet">
      <div class="layer spaper"></div>
      <div class="layer sglow"></div>
      <div class="layer"><svg viewBox="0 0 1000 1400">
                <g fill="none" stroke="url(#gold)">
          <path d="${fr(34, 18)}" stroke-width="1.3"/>
          <path d="${fr(43, 12)}" stroke-width=".6"/>
        </g>
      </svg></div>
      <img class="wl l" src="${H.img("waterlily-bouchard-cut.png")}" alt=""><img class="wl r" src="${H.img("waterlily-bouchard-cut.png")}" alt="">
      ${H.bism()}
      <div class="tb">
        ${H.f("hosts", "div", 'class="hosts"')}
        <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
        ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="600"')}
        ${H.f("joiner", "div", 'class="with"')}
        ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="600"')}
        ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
        <div class="ev">${H.flourish(64, true)}${H.f("event")}${H.flourish(64)}</div>
        <div class="dt">${H.dateLine()}</div>
        <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br>${H.f("place")}</div>
        ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
        ${H.urdu()}
      </div>
    </div></div>`;
  },
});
