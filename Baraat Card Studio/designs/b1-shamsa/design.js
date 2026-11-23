/* B1 - Shamsa: Shah Jahan's gold-and-lapis rosette as a single medallion on a midnight-navy ground.
   Round 2: bold thick-and-thin gold frame, big ivory type, rosette slightly smaller so the words can grow. */
registerDesign({
  id: "b1-shamsa",
  name: "Shamsa",
  idea: "A royal Mughal sun-medallion in gold and lapis glows on a midnight-blue ground inside a bold gold frame, with large, clear ivory lettering - regal, calm and unmistakably evening.",
  css: H => {
    const P = '[data-d="b1-shamsa"]';
    return `
    ${P} { background: #07122a; color: #f7efdc; font-variant-numeric: lining-nums; font-feature-settings: "lnum" 1; }
    ${P} .sky { background: url(${H.img("starry-night-sky.webp")}) center 30%/cover; filter: brightness(.55) saturate(.9); }
    ${P} .wash { background:
        radial-gradient(ellipse 60% 26% at 50% 19%, rgba(40,62,120,.42), transparent 70%),
        radial-gradient(ellipse 70% 50% at 50% 66%, rgba(4,10,28,.55), transparent 80%),
        radial-gradient(ellipse 90% 70% at 50% 55%, transparent 40%, rgba(2,6,18,.75) 100%); }
    ${P} .ros { position: absolute; left: 50%; top: 164px; width: 276px; height: 276px; translate: -50% 0;
        background: url(${H.img("mughal-shamsa-rosette-cut.png")}) center/contain no-repeat;
        -webkit-mask-image: radial-gradient(circle closest-side, #000 80%, rgba(0,0,0,.35) 86%, transparent 90%);
                mask-image: radial-gradient(circle closest-side, #000 80%, rgba(0,0,0,.35) 86%, transparent 90%);
        filter: drop-shadow(0 0 26px rgba(0,0,0,.6)) brightness(1.06); }
    ${P} .bism { position: absolute; left: 0; right: 0; top: 84px; text-align: center; font-size: calc(48px * var(--kt)); line-height: 1.2; color: #f1d98f; }
    ${P} .tb { left: 110px; right: 110px; top: 462px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .hosts { white-space: nowrap; font: 600 calc(44px * var(--kt))/1.2 'Cormorant SC', serif; letter-spacing: .08em; color: #f7efdc; }
    ${P} .inv { font: italic 500 calc(37px * var(--kt))/1.26 'Cormorant Garamond', serif; margin-top: 6px; color: #f7efdc; }
    ${P} .nm { font: 400 calc(128px * var(--kn))/1.08 'Alex Brush', cursive; white-space: nowrap; }
    ${P} .nm.g { margin-top: 18px; }
    ${P} .with { font: italic 500 calc(46px * var(--kt))/1 'Cormorant Garamond', serif; color: #f7efdc; margin: -4px 0 2px; }
    ${P} .bp { font: italic 500 calc(34px * var(--kt))/1.25 'Cormorant Garamond', serif; color: #f7efdc; margin-top: 2px; }
    ${P} .ev { display: flex; align-items: center; gap: 22px; margin-top: 22px; }
    ${P} .ev .f { font: 600 calc(50px * var(--kt))/1.15 Cinzel, serif; letter-spacing: .14em; margin-right: -.14em; }
    ${P} .ev i { display: block; width: 13px; height: 13px; background: #e6c877; transform: rotate(45deg); }
    ${P} .dt { font: 500 calc(42px * var(--kt))/1.22 'EB Garamond', serif; margin-top: 10px; color: #f7efdc; white-space: nowrap; }
    ${P} .vn { font: 500 calc(39px * var(--kt))/1.27 'EB Garamond', serif; margin-top: 4px; color: #f7efdc; }
    ${P} .vn .pl { font-size: calc(36px * var(--kt)); font-weight: 500; }
    ${P} .ur { font-size: calc(38px * var(--kt)); line-height: 1.85; color: #f7efdc; margin-top: 8px; }
    ${P} .rs { font: 500 calc(34px * var(--kt))/1.25 'EB Garamond', serif; color: #f7efdc; margin-top: 2px; }
  `;
  },
  render: (H, D) => {
    const corner = (x, y, sx, sy) => `<g transform="translate(${x},${y}) scale(${sx},${sy})">
        <path d="M0,46 L0,0 L46,0" stroke-width="3"/>
        <rect x="-7" y="-7" width="14" height="14" transform="rotate(45)" fill="url(#goldBright)" stroke="none"/></g>`;
    return `
    <div class="layer sky"></div>
    <div class="layer wash"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none" stroke="url(#goldBright)">
        <rect x="40" y="40" width="920" height="1320" stroke-width="5.5"/>
        <rect x="54" y="54" width="892" height="1292" stroke-width="2"/>
        ${corner(72, 72, 1, 1)}${corner(928, 72, -1, 1)}${corner(72, 1328, 1, -1)}${corner(928, 1328, -1, -1)}
      </g>
      <circle cx="500" cy="302" r="141" fill="none" stroke="url(#goldBright)" stroke-width="2.5"/>
      <circle cx="500" cy="302" r="151" fill="none" stroke="url(#goldBright)" stroke-width="3" stroke-dasharray="0 12" stroke-linecap="round" opacity=".9"/>
    </svg></div>
    ${H.bism('class="bism"')}
    <div class="ros"></div>
    <div class="tb">
      ${H.f("hosts", "div", 'class="hosts" data-fit="740"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-light" data-fit="720"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-light" data-fit="720"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="ev"><i></i>${H.f("event", "span", 'class="foil foil-light"')}<i></i></div>
      <div class="dt" data-fit="760">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;&middot;&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`;
  },
});
