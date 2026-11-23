/* A4 - Haala : gold-leaf mandala halo around the Bismillah, ink-painted lotus at the foot */
registerDesign({
  id: "a4-haala",
  name: "Haala",
  idea: "The Bismillah glows inside a fine gold-leaf halo, and an ink-and-colour lotus drifts across the foot of the card like a brushstroke on rice paper.",
  css: H => `
    [data-d="a4-haala"] { background: #f5eee1; color: #2f3a39; }
    [data-d="a4-haala"] .paper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: multiply; opacity: .2; filter: brightness(1.13) contrast(1.05); }
    [data-d="a4-haala"] .tint { background:
        radial-gradient(circle 260px at 50% 258px, rgba(222,186,104,.30), rgba(222,186,104,.10) 55%, rgba(222,186,104,0) 100%),
        radial-gradient(ellipse 120% 90% at 50% 50%, rgba(0,0,0,0) 62%, rgba(110,80,40,.13) 100%); }
    [data-d="a4-haala"] .ink { position: absolute; left: 30px; top: 928px; width: 820px; height: 722px; background: url(${H.img("lotus-chinese-painting.webp")}) center/100% 100% no-repeat;
        mix-blend-mode: multiply; filter: brightness(1.17) contrast(1.15);
        -webkit-mask-image: linear-gradient(180deg, rgba(0,0,0,0) 15%, #000 31%), radial-gradient(ellipse 48% 44% at 50% 50%, #000 70%, rgba(0,0,0,0) 100%); -webkit-mask-composite: source-in;
        mask-image: linear-gradient(180deg, rgba(0,0,0,0) 15%, #000 31%), radial-gradient(ellipse 48% 44% at 50% 50%, #000 70%, rgba(0,0,0,0) 100%); mask-composite: intersect; }
    [data-d="a4-haala"] .bism { position: absolute; left: 0; right: 0; top: 196px; text-align: center; font-family: 'Scheherazade New', serif; font-size: calc(84px * var(--kt)); line-height: 1.3; color: #7d5a1e; }
    [data-d="a4-haala"] .tb { left: 140px; right: 140px; top: 478px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="a4-haala"] .hosts { font: 400 calc(30px * var(--kt))/1.2 'Gilda Display', serif; letter-spacing: .12em; text-transform: uppercase; color: #2f3a39; }
    [data-d="a4-haala"] .inv { font: italic 400 calc(25px * var(--kt))/1.42 'Cormorant Garamond', serif; margin-top: 10px; color: #4c5857; }
    [data-d="a4-haala"] .nm { font: 400 calc(98px * var(--kn))/1.08 'Imperial Script', cursive; white-space: nowrap; }
    [data-d="a4-haala"] .nm.g { margin-top: 18px; }
    [data-d="a4-haala"] .with { font: italic 400 calc(27px * var(--kt))/1 'Cormorant Garamond', serif; color: #9b4a4a; margin: 0 0 2px; }
    [data-d="a4-haala"] .bp { font: italic 400 calc(20px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #4c5857; }
    [data-d="a4-haala"] .ev { font: 400 calc(22px * var(--kt))/1 'Gilda Display', serif; letter-spacing: .55em; margin-right: -.55em; text-transform: uppercase; margin-top: 26px; color: #9b4a4a; }
    [data-d="a4-haala"] .line { width: 260px; height: 1px; margin-top: 16px; background: linear-gradient(90deg, rgba(170,130,60,0), #b08a45 30%, #b08a45 70%, rgba(170,130,60,0)); }
    [data-d="a4-haala"] .dt { font: 400 calc(24px * var(--kt))/1.3 'Gilda Display', serif; letter-spacing: .06em; margin-top: 16px; color: #2f3a39; }
    [data-d="a4-haala"] .vn { font: 500 calc(25px * var(--kt))/1.42 'Cormorant Garamond', serif; margin-top: 6px; color: #2f3a39; }
    [data-d="a4-haala"] .rs { font: italic 400 calc(20px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 6px; color: #4c5857; }
    [data-d="a4-haala"] .ur { font-size: calc(21px * var(--kt)); color: #7d5a1e; margin-top: 4px; }
  `,
  render: (H, D) => {
    const rays = Array.from({ length: 96 }, (_, i) => { const a = i * Math.PI * 2 / 96, r1 = 176, r2 = i % 2 ? 186 : 198; return `M${(Math.cos(a) * r1).toFixed(1)},${(Math.sin(a) * r1).toFixed(1)} L${(Math.cos(a) * r2).toFixed(1)},${(Math.sin(a) * r2).toFixed(1)}`; }).join(" ");
    return `
    <div class="layer paper"></div>
    <div class="layer tint"></div>
    <div class="ink"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <defs><radialGradient id="a4glow"><stop offset="0" stop-color="#fffaf0" stop-opacity=".97"/><stop offset=".7" stop-color="#fbf3e2" stop-opacity=".92"/><stop offset="1" stop-color="#ead6a6" stop-opacity=".55"/></radialGradient></defs>
      <g transform="translate(500,258)">
        <g opacity=".85">${H.mandala(178, { sw: .9 })}</g>
        <g transform="rotate(11.25)" opacity=".5">${H.mandala(128, { sw: .65 })}</g>
        <circle r="116" fill="url(#a4glow)"/>
        <path d="${rays}" stroke="url(#gold)" stroke-width=".75" fill="none" opacity=".75"/>
        <circle r="204" fill="none" stroke="url(#gold)" stroke-width=".7" opacity=".7"/>
        <circle r="116" fill="none" stroke="url(#gold)" stroke-width="1.1"/>
        <circle r="110" fill="none" stroke="url(#gold)" stroke-width=".5"/>
      </g>
      <defs><clipPath id="a4fr"><rect x="50" y="50" width="900" height="1300"/></clipPath></defs>
      <g clip-path="url(#a4fr)"><g transform="translate(950,1350)" opacity=".38">${H.mandala(250, { sw: .85 })}<g transform="rotate(7.5)">${H.mandala(150, { sw: .65 })}</g></g></g>
      <g fill="none" stroke="url(#gold)">
        <rect x="40" y="40" width="920" height="1320" stroke-width="1.3"/>
        <rect x="50" y="50" width="900" height="1300" stroke-width=".6"/>
      </g>
    </svg></div>
    ${H.bism('class="bism foil foil-deep"')}
    <div class="tb">
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="660"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="660"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      ${H.f("event", "div", 'class="ev"')}
      <div class="line"></div>
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br>${H.f("place")}</div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`;
  },
});
