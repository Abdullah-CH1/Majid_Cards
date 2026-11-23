/* E1 - Sang-e-Marmar: a carved marble jali window at the top, white marble below, quiet gold hairlines. */
registerDesign((() => {
  const ID = "e1-sang-e-marmar", S = `[data-d="${ID}"]`;
  // arch window geometry (card px)
  const WX = 330, WW = 340, WT = 92, WH = 416, K = .62;
  const spring = (top, w) => top - H.archApex(w, 0, K);
  const local = H.archD(0, WW, spring(0, WW), WH, K, 7);
  return {
    id: ID,
    name: "Sang-e-Marmar",
    idea: "A carved white-marble jali becomes a lit window at the head of the card; below it, calm marble, hairline gold and classic Mughal-era typography.",
    css: H => `
      ${S} { background: #f8f5ef; color: #3a3127; }
      ${S} .veil { background: url(${H.img("white-marble-gold.webp")}) 42% 0 / 2600px auto no-repeat; filter: grayscale(1) contrast(1.15); opacity: .55; mix-blend-mode: multiply;
        -webkit-mask-image: linear-gradient(#000 0%, #000 52%, transparent 70%); mask-image: linear-gradient(#000 0%, #000 52%, transparent 70%); }
      ${S} .marble { background: url(${H.img("white-marble-gold.webp")}) center 100% / 1000px auto no-repeat;
        opacity: 1; filter: saturate(.9) contrast(1.05);
        -webkit-mask-image: radial-gradient(ellipse 40% 26% at 50% 84%, transparent 60%, #000 100%), linear-gradient(to top, #000 0%, #000 8%, transparent 38%); -webkit-mask-composite: source-in;
        mask-image: radial-gradient(ellipse 40% 26% at 50% 84%, transparent 60%, #000 100%), linear-gradient(to top, #000 0%, #000 8%, transparent 38%); mask-composite: intersect; }
      ${S} .warm { background: radial-gradient(ellipse 80% 60% at 50% 45%, rgba(255,252,246,.7), rgba(255,252,246,0) 70%); }
      ${S} .win { position: absolute; left: ${WX}px; top: ${WT}px; width: ${WW}px; height: ${WH}px; clip-path: path("${local}");
        background: radial-gradient(ellipse 70% 60% at 50% 38%, #8f7a5f 0%, #5d4c39 60%, #3e3226 100%); }
      ${S} .win img { position: absolute; width: 590px; left: -125px; top: -350px; filter: brightness(1.04) saturate(.85) contrast(1.05); }
      ${S} .win::after { content: ""; position: absolute; inset: 0; box-shadow: inset 0 0 26px 6px rgba(40,28,16,.45); background: radial-gradient(ellipse 60% 40% at 50% 30%, rgba(255,236,200,.18), transparent 70%); }
      ${S} .tb { left: 140px; right: 140px; top: 566px; text-align: center; display: flex; flex-direction: column; align-items: center; }
      ${S} .bism { font-size: calc(40px * var(--kt)); color: #6e5528; }
      ${S} .hosts { font: 500 calc(27px * var(--kt)) Cinzel, serif; letter-spacing: .16em; margin-top: 24px; }
      ${S} .inv { font: italic 400 calc(25px * var(--kt))/1.4 'Cormorant Garamond', serif; margin-top: 8px; color: #4a3f33; }
      ${S} .nm { font: 400 calc(96px * var(--kn))/1.12 'Pinyon Script', cursive; white-space: nowrap; }
      ${S} .g { margin-top: 26px; }
      ${S} .with { font: italic 400 calc(28px * var(--kt))/1 'Cormorant Garamond', serif; color: #7a6334; margin: 2px 0 4px; }
      ${S} .bp { font: italic 400 calc(22px * var(--kt)) 'Cormorant Garamond', serif; margin-top: 2px; }
      ${S} .ev { font: 500 calc(20px * var(--kt)) Cinzel, serif; letter-spacing: .6em; padding-left: .6em; margin-top: 30px; color: #7a6334;
        display: flex; align-items: center; gap: 22px; }
      ${S} .ev::before, ${S} .ev::after { content: ""; width: 70px; height: 1px; background: linear-gradient(90deg, transparent, #b39352); }
      ${S} .ev::after { background: linear-gradient(90deg, #b39352, transparent); }
      ${S} .dt { font: 500 calc(25px * var(--kt)) 'Cormorant Garamond', serif; letter-spacing: .14em; text-transform: uppercase; margin-top: 18px; }
      ${S} .vn { font: 400 calc(25px * var(--kt))/1.45 'Cormorant Garamond', serif; margin-top: 6px; }
      ${S} .vn .t { font-weight: 600; letter-spacing: .04em; }
      ${S} .ur { font-size: calc(21px * var(--kt)); color: #6e5528; margin-top: 14px; }
      ${S} .rs { font: 400 calc(18px * var(--kt)) Cinzel, serif; letter-spacing: .2em; margin-top: 6px; color: #6e5528; }
    `,
    render: (H, D) => {
      const o = 14, ow = WW + o * 2;
      const outer = H.archD(WX - o, ow, spring(WT - o - 2, ow), WT + WH + o, K, 7);
      const o2 = 22, ow2 = WW + o2 * 2;
      const outer2 = H.archD(WX - o2, ow2, spring(WT - o2 - 3, ow2), WT + WH + o2, K, 7);
      return `
      <div class="layer veil"></div>
      <div class="layer warm"></div>
      <div class="layer marble"></div>
      <div class="win"><img src="${H.img("marble-jali-arch-cut.png")}" alt=""></div>
      <div class="layer"><svg viewBox="0 0 1000 1400">
        <path d="${outer}" fill="none" stroke="url(#gold)" stroke-width="2"/>
        <path d="${outer2}" fill="none" stroke="url(#gold)" stroke-width=".9" opacity=".8"/>
        <rect x="46" y="46" width="908" height="1308" fill="none" stroke="url(#gold)" stroke-width="1.2" opacity=".75"/>
        <rect x="56" y="56" width="888" height="1288" fill="none" stroke="url(#gold)" stroke-width=".6" opacity=".6"/>
      </svg></div>
      <div class="tb">
        ${H.bism()}
        ${H.f("hosts", "div", 'class="hosts"')}
        <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
        ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="680"')}
        ${H.f("joiner", "div", 'class="with"')}
        ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="680"')}
        ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
        ${H.f("event", "div", 'class="ev"')}
        <div class="dt">${H.dateLine()}</div>
        <div class="vn"><span class="t">${H.f("time")}</span> &nbsp;·&nbsp; ${H.f("venue")}<br>${H.f("place")}</div>
        ${H.urdu()}
        ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      </div>`;
    },
  };
})());
