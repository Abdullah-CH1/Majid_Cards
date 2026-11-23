/* C4 - Gul-e-Jafari : Mughal marigold plants flanking an ivory cusped-arch window on Baraat maroon (round 2: wider arch, big text, bold foil frame) */
registerDesign({
  id: "c4-jafari",
  name: "Gul-e-Jafari",
  idea: "Baraat red with gold: two real Mughal marigold paintings (gul-e-jafari) stand at the foot of a wide ivory cusped arch, like a jharokha opened on a celebration.",
  css: H => {
    const P = '[data-d="c4-jafari"]';
    const arch = H.archD(150, 700, 560, 1300, .6, 7);
    return `
    ${P} { background: #4e1219; color: #2b1a10; }
    ${P} .ground { background:
        radial-gradient(ellipse 80% 62% at 50% 44%, #5c1520 0%, #4a1019 50%, #2c080d 100%); }
    ${P} .zar { background: url(${H.img("mughal-gold-margin-flowers.webp")}) -200px 0 / auto 700px repeat; mix-blend-mode: overlay; opacity: .6; }
    ${P} .grain { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: multiply; opacity: .5; filter: contrast(1.5); }
    ${P} .win { clip-path: path('${arch}'); background: #f8efdc; }
    ${P} .win::before { content: ""; position: absolute; inset: 0; background: url(${H.img("textured-ivory-paper.webp")}) center/cover;
        mix-blend-mode: multiply; opacity: .22; filter: brightness(1.12) contrast(1.15); }
    ${P} .win::after { content: ""; position: absolute; inset: 0;
        background: linear-gradient(180deg, rgba(160,110,50,.1), transparent 30%, transparent 85%, rgba(160,110,50,.1)); }
    ${P} .mg { position: absolute; bottom: 40px; height: 420px; filter: drop-shadow(0 4px 6px rgba(20,0,0,.4)); }
    ${P} .mg.l { left: 10px; }
    ${P} .mg.r { right: 10px; transform: scaleX(-1); }
    ${P} .tb { left: 200px; right: 200px; top: 342px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(46px * var(--kt)); font-weight: 700; line-height: 1.25; color: #6e1820; }
    ${P} .hosts { font: 600 calc(42px * var(--kt))/1.2 'Cormorant SC', serif; letter-spacing: .06em; margin-top: 12px; color: #2b1a10; }
    ${P} .inv { font: italic 500 calc(35px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 2px; color: #2b1a10; }
    ${P} .nm { font: 400 calc(130px * var(--kn))/1.06 'Great Vibes', cursive; white-space: nowrap;
        filter: drop-shadow(0 1px 0 rgba(60,30,5,.35)); }
    ${P} .nm.foil-deep { --foil: linear-gradient(100deg,#6a4712 0%,#9c7428 22%,#b8913f 36%,#7a5818 54%,#a8822f 72%,#5e400f 90%,#8c6a24 100%); }
    ${P} .nm.g { margin-top: 10px; }
    ${P} .with { font: italic 500 calc(44px * var(--kt))/1 'Cormorant Garamond', serif; color: #3d2414; margin: -6px 0 -4px; }
    ${P} .bp { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #2b1a10; margin-top: 2px; }
    ${P} .ev { margin-top: 16px; font: 600 calc(46px * var(--kt))/1 Cinzel, serif; letter-spacing: .14em; margin-right: -.14em; color: #7a1a22; }
    ${P} .dt { font: 600 calc(42px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 12px; color: #2b1a10; }
    ${P} .vn { font: 600 calc(38px * var(--kt))/1.28 'Cormorant Garamond', serif; margin-top: 2px; color: #2b1a10; }
    ${P} .vn .pl { font-size: calc(36px * var(--kt)); font-weight: 500; }
    ${P} .rs { font: italic 500 calc(34px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 4px; color: #2b1a10; }
    ${P} .ur { font-size: calc(38px * var(--kt)); line-height: 1.75; color: #6e1820; margin-top: 2px; max-width: 460px; text-wrap: balance; }
  `;
  },
  render: (H, D) => {
    const archO = H.archD(134, 732, 564, 1316, .6, 7);
    const arch = H.archD(150, 700, 560, 1300, .6, 7);
    const apex = H.archApex(732, 564, .6);
    return `
    <div class="layer ground"></div>
    <div class="layer zar"></div>
    <div class="layer grain"></div>
    <div class="layer win"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none" stroke="url(#goldBright)">
        <rect x="30" y="30" width="940" height="1340" stroke-width="5"/>
        <rect x="44" y="44" width="912" height="1312" stroke-width="2"/>
        <path d="${archO}" stroke-width="5.5"/>
        <path d="${arch}" stroke-width="2"/>
      </g>
      <path d="${H.archD(164, 672, 558, 1286, .6, 7)}" fill="none" stroke="#9a7428" stroke-width="2"/>
      <g fill="url(#goldBright)">
        <path d="M500,${apex - 62} C509,${apex - 40} 520,${apex - 28} 500,${apex - 6} C480,${apex - 28} 491,${apex - 40} 500,${apex - 62}Z"/>
        <circle cx="500" cy="${apex - 74}" r="5"/>
        ${[[30, 30], [970, 30], [30, 1370], [970, 1370]].map(([x, y]) => `<path transform="translate(${x},${y})" d="M0,-13 L13,0 0,13 -13,0Z"/>`).join("")}
      </g>
    </svg></div>
    <img class="mg l" src="${H.img("mughal-marigold-cut.png")}" alt="">
    <img class="mg r" src="${H.img("mughal-marigold-cut.png")}" alt="">
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="580"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="580"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      ${H.f("event", "div", 'class="ev"')}
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`;
  },
});
