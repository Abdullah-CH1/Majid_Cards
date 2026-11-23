/* C4 - Gul-e-Jafari : Mughal marigold plants flanking an ivory cusped-arch window on Baraat maroon */
registerDesign({
  id: "c4-jafari",
  name: "Gul-e-Jafari",
  idea: "Baraat red with gold: two real Mughal marigold paintings (gul-e-jafari) stand either side of an ivory cusped arch, like a jharokha opened on a celebration.",
  css: H => {
    const P = '[data-d="c4-jafari"]';
    const arch = H.archD(222, 556, 600, 1268, .6, 7);
    return `
    ${P} { background: #4e1219; color: #3a2214; }
    ${P} .ground { background:
        radial-gradient(ellipse 80% 62% at 50% 44%, #5c1520 0%, #4a1019 50%, #2c080d 100%); }
    ${P} .zar { background: url(${H.img("mughal-gold-margin-flowers.webp")}) -200px 0 / auto 700px repeat; mix-blend-mode: overlay; opacity: .6; }
    ${P} .grain { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: multiply; opacity: .5; filter: contrast(1.5); }
    ${P} .win { clip-path: path('${arch}'); background: #f6ecd8; }
    ${P} .win::before { content: ""; position: absolute; inset: 0; background: url(${H.img("textured-ivory-paper.webp")}) center/cover;
        mix-blend-mode: multiply; opacity: .3; filter: brightness(1.1) contrast(1.2); }
    ${P} .win::after { content: ""; position: absolute; inset: 0;
        background: radial-gradient(ellipse 34% 40% at 50% 62%, rgba(255,251,240,.6), rgba(255,251,240,0)),
                    linear-gradient(180deg, rgba(160,110,50,.12), transparent 30%, transparent 80%, rgba(160,110,50,.14)); }
    ${P} .mg { position: absolute; bottom: 50px; height: 604px; filter: drop-shadow(0 3px 5px rgba(20,0,0,.35)); }
    ${P} .mg.l { left: 34px; }
    ${P} .mg.r { right: 34px; transform: scaleX(-1); }
    ${P} .tb { left: 262px; right: 262px; top: 452px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(31px * var(--kt)); color: #7a1f26; }
    ${P} .hosts { font: 500 calc(27px * var(--kt))/1.2 'Cormorant SC', serif; letter-spacing: .1em; margin-top: 34px; color: #2e1a10; }
    ${P} .inv { font: italic 400 calc(23px * var(--kt))/1.42 'Cormorant Garamond', serif; margin-top: 6px; color: #523822; }
    ${P} .nm { font: 400 calc(86px * var(--kn))/1.14 'Great Vibes', cursive; white-space: nowrap; }
    ${P} .nm.g { margin-top: 30px; }
    ${P} .with { font: italic 400 calc(24px * var(--kt))/1 'Cormorant Garamond', serif; color: #6b4a2a; margin: 2px 0 4px; }
    ${P} .bp { font: italic 400 calc(19px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #6b4a2a; margin-top: 2px; }
    ${P} .ev { margin-top: 38px; font: 600 calc(19px * var(--kt))/1 Cinzel, serif; letter-spacing: .5em; margin-right: -.5em; color: #7a1f26; }
    ${P} .dt { font: 400 calc(21px * var(--kt))/1.3 Marcellus, serif; letter-spacing: .12em; text-transform: uppercase; margin-top: 14px; color: #2e1a10; }
    ${P} .vn { font: 500 calc(24px * var(--kt))/1.42 'Cormorant Garamond', serif; margin-top: 8px; color: #3a2214; }
    ${P} .vn .tm { font-weight: 600; }
    ${P} .vn, ${P} .rs, ${P} .ur, ${P} .bp { max-width: 372px; }
    ${P} .rs { font: italic 400 calc(18px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 6px; color: #6b4a2a; }
    ${P} .ur { font-size: calc(20px * var(--kt)); color: #7a1f26; margin-top: 18px; }
  `;
  },
  render: (H, D) => {
    const archO = H.archD(206, 588, 604, 1284, .6, 7);
    const arch = H.archD(222, 556, 600, 1268, .6, 7);
    const apex = H.archApex(588, 604, .6);
    return `
    <div class="layer ground"></div>
    <div class="layer zar"></div>
    <div class="layer grain"></div>
    <div class="layer win"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none" stroke="url(#goldBright)">
        <rect x="34" y="34" width="932" height="1332" stroke-width="1.6"/>
        <rect x="44" y="44" width="912" height="1312" stroke-width=".8"/>
        <path d="${archO}" stroke-width="2.4"/>
        <path d="${arch}" stroke-width="1"/>
        <path d="${H.archD(234, 532, 598, 1256, .6, 7)}" stroke="url(#gold)" stroke-width=".7" opacity=".8"/>
      </g>
      <g fill="url(#goldBright)">
        <path d="M500,${apex - 52} C507,${apex - 34} 516,${apex - 24} 500,${apex - 4} C484,${apex - 24} 493,${apex - 34} 500,${apex - 52}Z"/>
        <circle cx="500" cy="${apex - 62}" r="3.4"/>
        ${[[34, 34], [966, 34], [34, 1366], [966, 1366]].map(([x, y]) => `<path transform="translate(${x},${y})" d="M0,-9 L9,0 0,9 -9,0Z"/>`).join("")}
      </g>
    </svg></div>
    <img class="mg l" src="${H.img("mughal-marigold-cut.png")}" alt="">
    <img class="mg r" src="${H.img("mughal-marigold-cut.png")}" alt="">
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="450"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="450"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      ${H.f("event", "div", 'class="ev"')}
      <div class="dt">${H.dateLine()}</div>
      <div class="vn"><span class="tm">${H.f("time")}</span> &nbsp;·&nbsp; ${H.f("venue")}<br>${H.f("place")}</div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`;
  },
});
