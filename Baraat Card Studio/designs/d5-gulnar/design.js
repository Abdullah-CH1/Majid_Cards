/* D5 Gulnar - an Ohara Koson peony woodblock mounted like a tall pillar print on blush cotton, the wording set large beside it. */
registerDesign({
  id: "d5-gulnar",
  name: "Gulnar",
  idea: "Ohara Koson's peony print, mounted as a tall pillar print on a cream mat with a gold rule, stands beside large, clear wording on soft blush cotton paper - like a framed artwork you would keep.",
  css: H => `
    [data-d="d5-gulnar"] { background: #f3e4dc; color: #2e1c1e; }
    [data-d="d5-gulnar"] .paper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; filter: saturate(0) contrast(.45) brightness(1.5); mix-blend-mode: multiply; opacity: .5; }
    [data-d="d5-gulnar"] .tint { background: radial-gradient(ellipse 70% 70% at 64% 48%, rgba(255,246,240,.6), rgba(255,246,240,0) 72%); }
    [data-d="d5-gulnar"] .mat { position: absolute; left: 66px; top: 96px; width: 252px; height: 1208px; background: #fbf6ee;
      box-shadow: 0 1px 2px rgba(80,40,30,.2), 0 10px 28px rgba(110,60,50,.18); }
    [data-d="d5-gulnar"] .print { position: absolute; left: 82px; top: 112px; width: 220px; height: 1176px;
      background: url(${H.img("peony-koson-pink.webp")}) -118px 0/auto 1176px no-repeat; box-shadow: inset 0 0 0 1px rgba(90,60,40,.3); }
    [data-d="d5-gulnar"] .tb { left: 344px; width: 584px; top: 178px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="d5-gulnar"] .bism { font-size: calc(48px * var(--kt)); color: #4a2a1c; line-height: 1.25; }
    [data-d="d5-gulnar"] .hosts { font: 500 calc(44px * var(--kt))/1.2 'Playfair Display', serif; letter-spacing: .02em; margin-top: 30px; color: #2e1c1e; }
    [data-d="d5-gulnar"] .inv { font: italic 500 calc(38px * var(--kt))/1.28 'Cormorant Garamond', serif; margin-top: 10px; color: #2e1c1e; }
    [data-d="d5-gulnar"] .nm { font: 400 calc(136px * var(--kn))/1.12 'Great Vibes', cursive; white-space: nowrap; color: #7e3046; }
    [data-d="d5-gulnar"] .nm.g { margin-top: 40px; }
    [data-d="d5-gulnar"] .with { font: italic 500 calc(46px * var(--kt))/1 'Cormorant Garamond', serif; color: #2e1c1e; margin: 0 0 4px; }
    [data-d="d5-gulnar"] .bp { font: italic 500 calc(36px * var(--kt))/1.25 'Cormorant Garamond', serif; color: #2e1c1e; margin-top: 4px; }
    [data-d="d5-gulnar"] .sep { width: 120px; height: 3px; background: #a07a3e; margin-top: 44px; }
    [data-d="d5-gulnar"] .ev { font: 500 calc(50px * var(--kt))/1.2 'Playfair Display', serif; letter-spacing: .14em; padding-left: .14em; margin-top: 30px; color: #7e3046; text-transform: uppercase; }
    [data-d="d5-gulnar"] .dt { font: 600 calc(44px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 14px; }
    [data-d="d5-gulnar"] .vn { font: 600 calc(40px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 8px; color: #2e1c1e; }
    [data-d="d5-gulnar"] .vn .pl { font-weight: 500; font-size: calc(38px * var(--kt)); }
    [data-d="d5-gulnar"] .ur { font-size: calc(38px * var(--kt)); line-height: 1.9; white-space: nowrap; color: #2e1c1e; margin-top: 18px; }
    [data-d="d5-gulnar"] .rs { font: italic 500 calc(34px * var(--kt)) 'Cormorant Garamond', serif; color: #2e1c1e; margin-top: 2px; }
  `,
  render: (H, D) => `
    <div class="layer paper"></div>
    <div class="layer tint"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none" stroke="#6b4c14" opacity=".3">
        <rect x="30" y="30" width="940" height="1340" stroke-width="6.6"/>
        <rect x="44" y="44" width="912" height="1312" stroke-width="2.8"/>
      </g>
      <g fill="none" stroke="url(#gold)">
        <rect x="30" y="30" width="940" height="1340" stroke-width="5"/>
        <rect x="44" y="44" width="912" height="1312" stroke-width="1.8"/>
      </g>
    </svg></div>
    <div class="mat"></div>
    <div class="print"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <rect x="74" y="104" width="236" height="1192" fill="none" stroke="#6b4c14" stroke-width="3.6" opacity=".25"/>
      <rect x="74" y="104" width="236" height="1192" fill="none" stroke="url(#gold)" stroke-width="2.5"/>
    </svg></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g" data-fit="584"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm" data-fit="584"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="sep"></div>
      ${H.f("event", "div", 'class="ev"')}
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`,
});
