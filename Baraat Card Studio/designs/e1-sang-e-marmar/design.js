/* E1 - Sang-e-Marmar: a carved marble jali window at the top, white marble below, bold gold foil lines. */
registerDesign((() => {
  const ID = "e1-sang-e-marmar", S = `[data-d="${ID}"]`;
  // arch window geometry (card px)
  const WW = 240, WX = (1000 - WW) / 2, WT = 98, WH = 292, K = .62;
  const spring = (top, w) => top - H.archApex(w, 0, K);
  const local = H.archD(0, WW, spring(0, WW), WH, K, 7);
  return {
    id: ID,
    name: "Sang-e-Marmar",
    idea: "A carved white-marble jali becomes a lit window at the head of the card; below it, calm marble, bold gold foil lines and large, classic Mughal-era typography.",
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
      ${S} .win img { position: absolute; width: 430px; left: -95px; top: -262px; filter: brightness(1.04) saturate(.85) contrast(1.05); }
      ${S} .win::after { content: ""; position: absolute; inset: 0; box-shadow: inset 0 0 26px 6px rgba(40,28,16,.45); background: radial-gradient(ellipse 60% 40% at 50% 30%, rgba(255,236,200,.18), transparent 70%); }
      ${S} .tb { left: 110px; right: 110px; top: 426px; text-align: center; display: flex; flex-direction: column; align-items: center; }
      ${S} .bism { font-size: calc(48px * var(--kt)); color: #4a3418; line-height: 1.2; }
      ${S} .hosts { font: 600 calc(42px * var(--kt))/1.2 Cinzel, serif; letter-spacing: .06em; margin-top: 14px; color: #2b1d12; }
      ${S} .inv { font: italic 500 calc(37px * var(--kt))/1.26 'Cormorant Garamond', serif; margin-top: 6px; color: #2b1d12; }
      ${S} .nm { font: 400 calc(132px * var(--kn))/1.04 Parisienne, cursive; white-space: nowrap; filter: drop-shadow(0 1px 0 rgba(60,40,10,.3)); }
      ${S} .g { margin-top: 18px; }
      ${S} .with { font: italic 500 calc(46px * var(--kt))/1 'Cormorant Garamond', serif; color: #4a3418; margin: 0; }
      ${S} .bp { font: italic 500 calc(36px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 2px; color: #2b1d12; }
      ${S} .ev { font: 600 calc(48px * var(--kt))/1.2 Cinzel, serif; letter-spacing: .14em; margin-top: 20px;
        display: flex; align-items: center; gap: 26px; }
      ${S} .ev .x { padding-left: .14em; filter: drop-shadow(0 1px 0 rgba(60,40,10,.3)); }
      ${S} .ev::before, ${S} .ev::after { content: ""; width: 80px; height: 3px; background: linear-gradient(90deg, rgba(122,90,24,0), #7a5a18); }
      ${S} .ev::after { background: linear-gradient(90deg, #7a5a18, rgba(122,90,24,0)); }
      ${S} .dt { font: 600 calc(44px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 6px; color: #2b1d12; }
      ${S} .vn { font: 600 calc(40px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 2px; color: #2b1d12; }
      ${S} .vn .p { font-weight: 500; font-size: calc(38px * var(--kt)); }
      ${S} .ur { font-size: calc(38px * var(--kt)); line-height: 1.8; white-space: nowrap; color: #2b1d12; margin-top: 2px; }
      ${S} .rs { font: italic 500 calc(34px * var(--kt)) 'Cormorant Garamond', serif; margin-top: 0; color: #2b1d12; }
    `,
    render: (H, D) => {
      const o = 9, ow = WW + o * 2;
      const outer = H.archD(WX - o, ow, spring(WT - o - 1, ow), WT + WH + o, K, 7);
      const o2 = 20, ow2 = WW + o2 * 2;
      const outer2 = H.archD(WX - o2, ow2, spring(WT - o2 - 2, ow2), WT + WH + o2, K, 7);
      return `
      <div class="layer veil"></div>
      <div class="layer warm"></div>
      <div class="layer marble"></div>
      <div class="win"><img src="${H.img("marble-jali-arch-cut.png")}" alt=""></div>
      <div class="layer"><svg viewBox="0 0 1000 1400">
        <g fill="none" stroke="#6b4c14" opacity=".28">
          <path d="${outer}" stroke-width="6.6"/><path d="${outer2}" stroke-width="2.8"/>
          <rect x="30" y="30" width="940" height="1340" stroke-width="6.6"/><rect x="44" y="44" width="912" height="1312" stroke-width="2.8"/>
        </g>
        <path d="${outer}" fill="none" stroke="url(#gold)" stroke-width="5"/>
        <path d="${outer2}" fill="none" stroke="url(#gold)" stroke-width="1.8"/>
        <rect x="30" y="30" width="940" height="1340" fill="none" stroke="url(#gold)" stroke-width="5"/>
        <rect x="44" y="44" width="912" height="1312" fill="none" stroke="url(#gold)" stroke-width="1.8"/>
      </svg></div>
      <div class="tb">
        ${H.bism()}
        ${H.f("hosts", "div", 'class="hosts"')}
        <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
        ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="740"')}
        ${H.f("joiner", "div", 'class="with"')}
        ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="740"')}
        ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
        <div class="ev">${H.f("event", "span", 'class="x foil foil-deep"')}</div>
        <div class="dt">${H.dateLine()}</div>
        <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="p">${H.f("place")}</span></div>
        ${H.urdu()}
        ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      </div>`;
    },
  };
})());
