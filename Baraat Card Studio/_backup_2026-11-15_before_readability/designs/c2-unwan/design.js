/* C2 - Unwan : an illuminated manuscript opening - lapis-and-gold headpiece holding the Bismillah, gold-flower margins */
registerDesign({
  id: "c2-unwan",
  name: "Unwan",
  idea: "Opens like a royal manuscript: a real lapis-and-gold Mughal headpiece holds the Bismillah, the names are written below in lapis ink, all inside gold-painted flower margins.",
  css: H => {
    const P = '[data-d="c2-unwan"]';
    const s = 720 / 905;                       // cartouche crop scale (native x 215..1120, y 128..500)
    return `
    ${P} { background: #b9915f; color: #2a2a3a; }
    ${P} .mg { position: absolute; left: 0; top: 0; width: 1400px; height: 96px; transform-origin: 0 0; filter: saturate(.9) brightness(1.04);
        background: url(${H.img("mughal-gold-margin-flowers.webp")}) -60px -170px / auto 440px repeat-x; }
    ${P} .mg.t { clip-path: polygon(0 0, 1000px 0, 904px 96px, 96px 96px); }
    ${P} .mg.b { top: 1400px; transform: scaleY(-1); background-position: -560px -200px; clip-path: polygon(0 0, 1000px 0, 904px 96px, 96px 96px); }
    ${P} .mg.l { left: 96px; transform: rotate(90deg); background-position: -120px -170px; clip-path: polygon(96px 0, 1304px 0, 1400px 96px, 0 96px); }
    ${P} .mg.r { left: 904px; top: 1400px; transform: rotate(-90deg); background-position: -90px -260px; clip-path: polygon(96px 0, 1304px 0, 1400px 96px, 0 96px); }
    ${P} .field { position: absolute; left: 96px; top: 96px; right: 96px; bottom: 96px; background: #f6eedc; overflow: hidden; }
    ${P} .field::before { content: ""; position: absolute; inset: 0; background: url(${H.img("textured-ivory-paper.webp")}) center/cover;
        mix-blend-mode: multiply; opacity: .3; filter: brightness(1.1) contrast(1.2); }
    ${P} .field::after { content: ""; position: absolute; inset: 0;
        background: radial-gradient(ellipse 120% 100% at 50% 50%, transparent 60%, rgba(160,120,60,.16)); }
    ${P} .cart { position: absolute; left: 140px; top: 136px; width: 720px; height: ${Math.round(372 * s)}px;
        background: url(${H.img("mughal-unwan-cartouche.webp")}) ${-215 * s}px ${-128 * s}px / ${1337 * s}px auto no-repeat; }
    ${P} .tb { left: 150px; right: 150px; top: 136px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bx { height: ${Math.round(372 * s)}px; display: flex; align-items: center; justify-content: center; }
    ${P} .bism { display: flex; align-items: center; justify-content: center;
        font-size: calc(29px * var(--kt)); font-weight: 700; transform: scaleX(.74); color: #16224f; text-shadow: 0 0 1px rgba(255,236,170,.6); padding-top: 4px; }
    ${P} .hosts { font: 500 calc(25px * var(--kt))/1.2 Cinzel, serif; letter-spacing: .14em; margin-top: 58px; color: #2b2418; }
    ${P} .inv { font: italic 400 calc(27px * var(--kt))/1.42 'Cormorant Garamond', serif; margin-top: 12px; color: #4c3d2a; }
    ${P} .nm { font: 400 calc(116px * var(--kn))/1.1 Corinthia, cursive; white-space: nowrap; color: #1f2d63; }
    ${P} .nm.g { margin-top: 34px; }
    ${P} .with { font: italic 400 calc(26px * var(--kt))/1 'Cormorant Garamond', serif; color: #7a5622; margin: 0 0 4px; }
    ${P} .bp { font: italic 400 calc(20px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #5d4a30; margin-top: 2px; }
    ${P} .ev { margin-top: 50px; display: flex; align-items: center; gap: 16px; }
    ${P} .ev .f { font: 600 calc(21px * var(--kt))/1 Cinzel, serif; letter-spacing: .5em; margin-right: -.5em; color: #8a2f22; }
    ${P} .ev svg { width: 70px; height: 14px; }
    ${P} .dt { font: 500 calc(25px * var(--kt))/1.3 'Cormorant SC', serif; letter-spacing: .12em; margin-top: 22px; color: #2b2418; }
    ${P} .vn { font: 500 calc(27px * var(--kt))/1.45 'Cormorant Garamond', serif; margin-top: 10px; color: #33291b; }
    ${P} .vn .tm { font-weight: 600; }
    ${P} .rs { font: italic 400 calc(19px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 6px; color: #5d4a30; }
    ${P} .ur { font-size: calc(22px * var(--kt)); color: #1f2d63; margin-top: 26px; }
  `;
  },
  render: (H, D) => {
    const s = 720 / 905, ch = Math.round(372 * s);
    const box = (x, y, w, h, o, sw, st) => `<rect x="${x - o}" y="${y - o}" width="${w + 2 * o}" height="${h + 2 * o}" fill="none" stroke="${st}" stroke-width="${sw}"/>`;
    const tick = flip => `<svg viewBox="0 0 70 14" style="${flip ? "transform:scaleX(-1)" : ""}"><path d="M0,7 H52" stroke="#a07a34" stroke-width="1"/><path d="M56,7 l6,-5 6,5 -6,5z" fill="#1f2d63"/></svg>`;
    return `
    <div class="mg t"></div><div class="mg b"></div><div class="mg l"></div><div class="mg r"></div>
    <div class="field"></div>
    <div class="cart"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      ${box(96, 96, 808, 1208, 9, 1, "#a8432c")}
      ${box(96, 96, 808, 1208, 5.5, 1.4, "#1f2d63")}
      ${box(96, 96, 808, 1208, 1.5, 3.5, "url(#gold)")}
      ${box(96, 96, 808, 1208, -3, .7, "#2b2418")}
      ${box(96, 96, 808, 1208, -16, 1, "url(#gold)")}
      ${box(140, 136, 720, ch, 2, 3, "url(#gold)")}
      ${box(140, 136, 720, ch, 6, .8, "#1f2d63")}
      ${box(140, 136, 720, ch, 9.5, .8, "url(#gold)")}
    </svg></div>
    <div class="tb">
      <div class="bx">${H.bism()}</div>
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g" data-fit="660"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm" data-fit="660"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="ev">${tick()}${H.f("event")}${tick(1)}</div>
      <div class="dt">${H.dateLine()}</div>
      <div class="vn"><span class="tm">${H.f("time")}</span> &nbsp;·&nbsp; ${H.f("venue")}<br>${H.f("place")}</div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`;
  },
});
