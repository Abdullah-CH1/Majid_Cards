/* A1 - Noor Kanwal : the client's favourite, rebuilt with real hand-tinted lotus art */
registerDesign({
  id: "a1-noor-kanwal",
  name: "Noor Kanwal",
  idea: "Your favourite card, made properly: handmade ivory paper, a hairline gold Mughal arch, fine gold mandalas and real hand-painted lotus rising from the base.",
  css: H => `
    [data-d="a1-noor-kanwal"] { background: #f1e5cf; color: #4b3722; }
    [data-d="a1-noor-kanwal"] .paper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: multiply; opacity: .2; filter: brightness(1.12) contrast(1.06); }
    [data-d="a1-noor-kanwal"] .glow { background:
        radial-gradient(ellipse 62% 46% at 50% 42%, rgba(255,250,238,.75), rgba(255,250,238,0) 70%),
        radial-gradient(ellipse 120% 90% at 50% 50%, rgba(0,0,0,0) 60%, rgba(120,84,40,.16) 100%); }
    [data-d="a1-noor-kanwal"] .lo { position: absolute; filter: saturate(.86) brightness(1.03) drop-shadow(0 2px 3px rgba(90,60,20,.12)); }
    [data-d="a1-noor-kanwal"] .lo1 { left: -56px; bottom: -168px; width: 400px; }
    [data-d="a1-noor-kanwal"] .lo2 { right: -56px; bottom: -168px; width: 400px; transform: scaleX(-1); }
    [data-d="a1-noor-kanwal"] .lc { position: absolute; left: 349px; bottom: -84px; width: 302px; height: 389px; overflow: hidden; }
    [data-d="a1-noor-kanwal"] .lc img { position: absolute; left: -146px; top: -135px; width: 448px; filter: saturate(.9) drop-shadow(0 2px 3px rgba(90,60,20,.12)); }
    [data-d="a1-noor-kanwal"] .tb { left: 210px; right: 210px; top: 268px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="a1-noor-kanwal"] .bism { font-family: 'Scheherazade New', serif; font-size: calc(118px * var(--kt)); line-height: 1.25; margin: -24px 0 -18px; color: #8a6526; }
    [data-d="a1-noor-kanwal"] .hosts { font: 500 calc(31px * var(--kt))/1.2 'Cormorant SC', serif; letter-spacing: .09em; margin-top: 20px; color: #3f2d1b; }
    [data-d="a1-noor-kanwal"] .inv { font: italic 400 calc(25px * var(--kt))/1.42 'Cormorant Garamond', serif; margin-top: 8px; color: #5a432b; }
    [data-d="a1-noor-kanwal"] .nm { font: 400 calc(100px * var(--kn))/1.12 'Pinyon Script', cursive; white-space: nowrap; }
    [data-d="a1-noor-kanwal"] .nm.g { margin-top: 16px; }
    [data-d="a1-noor-kanwal"] .with { font: italic 400 calc(28px * var(--kt))/1 'Cormorant Garamond', serif; color: #6b5233; margin: 2px 0 4px; }
    [data-d="a1-noor-kanwal"] .bp { font: italic 400 calc(21px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #6b5233; margin-top: 2px; }
    [data-d="a1-noor-kanwal"] .ev { display: flex; align-items: center; gap: 16px; margin-top: 22px; color: #8a6526; }
    [data-d="a1-noor-kanwal"] .ev .f { font: 500 calc(21px * var(--kt))/1 Cinzel, serif; letter-spacing: .48em; margin-right: -.48em; color: #7a5a22; }
    [data-d="a1-noor-kanwal"] .dt { font: 400 calc(23px * var(--kt))/1.3 Marcellus, serif; letter-spacing: .12em; text-transform: uppercase; margin-top: 12px; color: #3f2d1b; }
    [data-d="a1-noor-kanwal"] .vn { font: 500 calc(25px * var(--kt))/1.38 'Cormorant Garamond', serif; margin-top: 6px; color: #4b3722; }
    [data-d="a1-noor-kanwal"] .vn .tm { font-weight: 600; }
    [data-d="a1-noor-kanwal"] .rs { font: italic 400 calc(20px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 6px; color: #6b5233; }
    [data-d="a1-noor-kanwal"] .ur { font-size: calc(22px * var(--kt)); color: #7a5a22; margin-top: 2px; }
  `,
  render: (H, D) => {
    const corner = (x, y) => `<g transform="translate(${x},${y})" opacity=".6">${H.mandala(260, { sw: 1 })}<g transform="rotate(7.5)">${H.mandala(150, { sw: .8 })}</g></g>`;
    const archO = H.archD(176, 648, 560, 1366, .6, 7, true);
    const archI = H.archD(190, 620, 562, 1366, .6, 7, true);
    const apex = H.archApex(648, 560, .6);
    return `
    <div class="layer paper"></div>
    <div class="layer glow"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <defs><clipPath id="a1clip"><rect x="40" y="40" width="920" height="1320"/></clipPath></defs>
      <g clip-path="url(#a1clip)">
        ${corner(40, 40)}${corner(960, 40)}
        <g transform="translate(500,1400)" opacity=".72">${H.mandala(392, { sw: 1.05 })}<g transform="rotate(7.5)">${H.mandala(222, { sw: .85 })}</g></g>
      </g>
      <g fill="none" stroke="url(#gold)">
        <rect x="30" y="30" width="940" height="1340" stroke-width="1.6"/>
        <rect x="40" y="40" width="920" height="1320" stroke-width=".9"/>
        <path d="${archO}" stroke-width="2.2"/>
        <path d="${archI}" stroke-width=".9"/>
      </g>
      <g fill="url(#gold)" stroke="none">
        <path d="M500,${apex - 46} C506,${apex - 30} 514,${apex - 22} 500,${apex - 4} C486,${apex - 22} 494,${apex - 30} 500,${apex - 46}Z"/>
        <circle cx="500" cy="${apex - 56}" r="3.2"/>
        ${[30, 970].map(x => `<g transform="translate(${x},700)"><path d="M0,-20 C7,-9 7,9 0,20 C-7,9 -7,-9 0,-20Z" fill="#f1e5cf" stroke="url(#gold)" stroke-width="1.2"/><circle r="2.6"/></g>`).join("")}
        ${[500].map(x => `<g transform="translate(${x},30)"><path d="M-20,0 C-9,-7 9,-7 20,0 C9,7 -9,7 -20,0Z" fill="#f1e5cf" stroke="url(#gold)" stroke-width="1.2"/><circle r="2.6"/></g>`).join("")}
      </g>
    </svg></div>
    <img class="lo lo1" src="${H.img("lotus-ogawa-handcoloured-cut.png")}" alt="">
    <img class="lo lo2" src="${H.img("lotus-ogawa-handcoloured-cut.png")}" alt="">
    <div class="lc"><img src="${H.img("lotus-ogawa-handcoloured-2-cut.png")}" alt=""></div>
    <div class="tb">
      ${H.bism('class="bism foil foil-deep"')}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="560"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="560"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="ev">${H.flourish(70, true)}${H.f("event")}${H.flourish(70)}</div>
      <div class="dt">${H.dateLine()}</div>
      <div class="vn"><span class="tm">${H.f("time")}</span> &nbsp;·&nbsp; ${H.f("venue")}<br>${H.f("place")}</div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`;
  },
});
