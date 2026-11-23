/* C2 - Unwan : an illuminated manuscript opening - lapis-and-gold headpiece crowning the page, gold-flower margins (round 2: big lapis text, bold foil frame) */
registerDesign({
  id: "c2-unwan",
  name: "Unwan",
  idea: "Opens like a royal manuscript: a real lapis-and-gold Mughal headpiece crowns the page with your initials in its gold heart, and the Bismillah and names follow below in large lapis ink, all inside gold-painted flower margins.",
  css: H => {
    const P = '[data-d="c2-unwan"]';
    /* cartouche crop: native x 98..1242, y 100..508 (inner lapis panel with its green band) */
    const cw = 600, s = cw / 1144, ch = Math.round(408 * s);
    return `
    ${P} { background: #b9915f; color: #2b1d12; }
    ${P} .mg { position: absolute; left: 0; top: 0; width: 1400px; height: 96px; transform-origin: 0 0; filter: saturate(.9) brightness(1.04);
        background: url(${H.img("mughal-gold-margin-flowers.webp")}) -60px -170px / auto 440px repeat-x; }
    ${P} .mg.t { clip-path: polygon(0 0, 1000px 0, 904px 96px, 96px 96px); }
    ${P} .mg.b { top: 1400px; transform: scaleY(-1); background-position: -560px -200px; clip-path: polygon(0 0, 1000px 0, 904px 96px, 96px 96px); }
    ${P} .mg.l { left: 96px; transform: rotate(90deg); background-position: -120px -170px; clip-path: polygon(96px 0, 1304px 0, 1400px 96px, 0 96px); }
    ${P} .mg.r { left: 904px; top: 1400px; transform: rotate(-90deg); background-position: -90px -260px; clip-path: polygon(96px 0, 1304px 0, 1400px 96px, 0 96px); }
    ${P} .field { position: absolute; left: 96px; top: 96px; right: 96px; bottom: 96px; background: #f7f0df; overflow: hidden; }
    ${P} .field::before { content: ""; position: absolute; inset: 0; background: url(${H.img("textured-ivory-paper.webp")}) center/cover;
        mix-blend-mode: multiply; opacity: .22; filter: brightness(1.12) contrast(1.15); }
    ${P} .field::after { content: ""; position: absolute; inset: 0;
        background: radial-gradient(ellipse 120% 100% at 50% 50%, transparent 66%, rgba(160,120,60,.12)); }
    ${P} .cart { position: absolute; left: ${500 - cw / 2}px; top: 134px; width: ${cw}px; height: ${ch}px;
        background: url(${H.img("mughal-unwan-cartouche.webp")}) ${-98 * s}px ${-100 * s}px / ${1337 * s}px auto no-repeat; }
    ${P} .mono { position: absolute; left: ${500 - cw / 2}px; top: 134px; width: ${cw}px; height: ${ch}px;
        display: flex; align-items: center; justify-content: center; gap: 14px; padding-left: 6px;
        font: 600 calc(64px * var(--kn))/1 Cinzel, serif; color: #16224f; text-shadow: 0 1px 0 rgba(255,236,170,.55); }
    ${P} .mono i { width: 11px; height: 11px; background: #16224f; transform: rotate(45deg); }
    ${P} .tb { left: 130px; right: 130px; top: ${134 + ch + 26}px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(48px * var(--kt)); font-weight: 700; line-height: 1.25; color: #16224f; }
    ${P} .hosts { font: 600 calc(42px * var(--kt))/1.2 Cinzel, serif; letter-spacing: .06em; margin-top: 14px; color: #2b1d12; }
    ${P} .inv { font: italic 500 calc(36px * var(--kt))/1.26 'Cormorant Garamond', serif; margin-top: 6px; color: #2b1d12; }
    ${P} .nm { font: 400 calc(132px * var(--kn))/1.08 'Alex Brush', cursive; white-space: nowrap; color: #1a2860; }
    ${P} .nm.g { margin-top: 14px; }
    ${P} .with { font: italic 500 calc(46px * var(--kt))/1 'Cormorant Garamond', serif; color: #3a2a14; margin: -6px 0 -4px; }
    ${P} .bp { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #2b1d12; margin-top: 2px; }
    ${P} .ev { margin-top: 18px; display: flex; align-items: center; gap: 18px; }
    ${P} .ev .f { font: 600 calc(48px * var(--kt))/1 Cinzel, serif; letter-spacing: .14em; margin-right: -.14em; color: #8a2a1c; }
    ${P} .ev svg { width: 78px; height: 18px; }
    ${P} .dt { font: 600 calc(42px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 14px; color: #2b1d12; }
    ${P} .vn { font: 600 calc(40px * var(--kt))/1.28 'Cormorant Garamond', serif; margin-top: 2px; color: #2b1d12; }
    ${P} .vn .pl { font-size: calc(36px * var(--kt)); font-weight: 500; }
    ${P} .rs { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 4px; color: #2b1d12; }
    ${P} .ur { font-size: calc(40px * var(--kt)); line-height: 1.75; color: #16224f; margin-top: 4px; }
  `;
  },
  render: (H, D) => {
    const cw = 600, s = cw / 1144, ch = Math.round(408 * s), cx = 500 - cw / 2;
    const box = (x, y, w, h, o, sw, st) => `<rect x="${x - o}" y="${y - o}" width="${w + 2 * o}" height="${h + 2 * o}" fill="none" stroke="${st}" stroke-width="${sw}"/>`;
    const tick = flip => `<svg viewBox="0 0 78 18" style="${flip ? "transform:scaleX(-1)" : ""}"><path d="M0,9 H56" stroke="#8a6420" stroke-width="2.5"/><path d="M60,9 l8,-7 8,7 -8,7z" fill="#1a2860"/></svg>`;
    return `
    <div class="mg t"></div><div class="mg b"></div><div class="mg l"></div><div class="mg r"></div>
    <div class="field"></div>
    <div class="cart"></div>
    <div class="mono">${H.monoG()}<i></i>${H.monoB()}</div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      ${box(96, 96, 808, 1208, 10, 2, "#9a3a24")}
      ${box(96, 96, 808, 1208, 6, 2.5, "#1a2860")}
      ${box(96, 96, 808, 1208, 0, 5, "#9a7428")}
      ${box(96, 96, 808, 1208, 0, 3, "url(#gold)")}
      ${box(96, 96, 808, 1208, -16, 2, "#9a7428")}
      ${box(cx, 134, cw, ch, 3, 5, "#9a7428")}
      ${box(cx, 134, cw, ch, 3, 3, "url(#gold)")}
      ${box(cx, 134, cw, ch, 10, 2, "#1a2860")}
    </svg></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g" data-fit="690"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm" data-fit="690"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="ev">${tick()}${H.f("event")}${tick(1)}</div>
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`;
  },
});
