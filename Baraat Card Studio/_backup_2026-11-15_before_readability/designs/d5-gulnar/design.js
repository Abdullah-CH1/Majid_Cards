/* D5 Gulnar - an Ohara Koson peony woodblock mounted like a gallery print on blush cotton, text set beside it. */
registerDesign({
  id: "d5-gulnar",
  name: "Gulnar",
  idea: "A complete Ohara Koson peony print, mounted on a cream mat with a fine gold rule, sits beside the wording on soft blush cotton paper - like a framed artwork you would keep.",
  css: H => `
    [data-d="d5-gulnar"] { background: #f3e4dc; color: #432a2c; }
    [data-d="d5-gulnar"] .paper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; filter: saturate(0) contrast(.45) brightness(1.5); mix-blend-mode: multiply; opacity: .5; }
    [data-d="d5-gulnar"] .tint { background: radial-gradient(ellipse 80% 70% at 60% 45%, rgba(255,246,240,.55), rgba(255,246,240,0) 70%); }
    [data-d="d5-gulnar"] .mat { position: absolute; left: 76px; top: 150px; width: 396px; height: 1100px; background: #fbf6ee;
      box-shadow: 0 1px 2px rgba(80,40,30,.18), 0 10px 28px rgba(110,60,50,.16); }
    [data-d="d5-gulnar"] .print { position: absolute; left: 96px; top: 170px; width: 356px; height: 1060px;
      background: url(${H.img("peony-koson-pink.webp")}) 62% 50%/auto 1092px no-repeat; box-shadow: inset 0 0 0 1px rgba(90,60,40,.25); }
    [data-d="d5-gulnar"] .tb { left: 512px; width: 412px; top: 300px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="d5-gulnar"] .bism { font-size: calc(31px * var(--kt)); color: #8a6430; line-height: 1.2; }
    [data-d="d5-gulnar"] .hosts { font: 400 calc(22px * var(--kt)) 'Playfair Display SC', serif; letter-spacing: .1em; margin-top: 40px; color: #3a2325; }
    [data-d="d5-gulnar"] .inv { font: italic 400 calc(22px * var(--kt))/1.45 'Playfair Display', serif; margin-top: 12px; color: #5d4143; }
    [data-d="d5-gulnar"] .nm { font: 400 calc(84px * var(--kn))/1.25 'Great Vibes', cursive; white-space: nowrap; color: #8b3f52; }
    [data-d="d5-gulnar"] .nm.g { margin-top: 40px; }
    [data-d="d5-gulnar"] .with { font: italic 400 calc(21px * var(--kt))/1 'Playfair Display', serif; color: #6e5052; margin: 0 0 4px; }
    [data-d="d5-gulnar"] .bp { font: italic 400 calc(18px * var(--kt)) 'Playfair Display', serif; color: #5d4143; margin-top: 4px; }
    [data-d="d5-gulnar"] .sep { width: 46px; height: 1px; background: #b08a55; margin-top: 46px; }
    [data-d="d5-gulnar"] .ev { font: 400 calc(21px * var(--kt)) 'Italiana', serif; letter-spacing: .5em; margin: 30px 0 0 .5em; color: #8a6430; text-transform: uppercase; }
    [data-d="d5-gulnar"] .dt { font: 400 calc(22px * var(--kt))/1.3 'Playfair Display', serif; margin-top: 20px; }
    [data-d="d5-gulnar"] .tm { font: italic 400 calc(21px * var(--kt)) 'Playfair Display', serif; margin-top: 6px; color: #5d4143; }
    [data-d="d5-gulnar"] .vn { font: 400 calc(18px * var(--kt))/1.6 'Playfair Display', serif; letter-spacing: .12em; text-transform: uppercase; margin-top: 26px; color: #3a2325; }
    [data-d="d5-gulnar"] .vn .pl { color: #5d4143; }
    [data-d="d5-gulnar"] .ur { font-size: calc(16px * var(--kt)); color: #8a6430; margin-top: 22px; }
    [data-d="d5-gulnar"] .rs { font: italic calc(16px * var(--kt)) 'Playfair Display', serif; color: #5d4143; margin-top: 4px; }
  `,
  render: (H, D) => `
    <div class="layer paper"></div>
    <div class="layer tint"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none" stroke="url(#gold)">
        <rect x="40" y="40" width="920" height="1320" stroke-width="1.2"/>
      </g>
    </svg></div>
    <div class="mat"></div>
    <div class="print"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <rect x="86.5" y="160.5" width="375" height="1079" fill="none" stroke="url(#gold)" stroke-width="1"/>
    </svg></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g" data-fit="400"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm" data-fit="400"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="sep"></div>
      ${H.f("event", "div", 'class="ev"')}
      <div class="dt">${H.dateLine()}</div>
      ${H.f("time", "div", 'class="tm"')}
      <div class="vn">${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`,
});
