/* A2 - Nazakat : one large hand-tinted lotus stem framing the text asymmetrically */
registerDesign({
  id: "a2-nazakat",
  name: "Nazakat",
  idea: "A single tall hand-tinted lotus rises along the right edge in front of a faint gold sun-mandala, leaving a calm column of ivory for your words.",
  css: H => `
    [data-d="a2-nazakat"] { background: #f6f0e4; color: #3e3122; }
    [data-d="a2-nazakat"] .paper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: multiply; opacity: .2; filter: brightness(1.14) contrast(1.04); }
    [data-d="a2-nazakat"] .tint { background:
        radial-gradient(ellipse 50% 40% at 30% 46%, rgba(255,252,244,.8), rgba(255,252,244,0) 75%),
        radial-gradient(ellipse 60% 45% at 78% 52%, rgba(232,205,190,.28), rgba(232,205,190,0) 70%),
        radial-gradient(ellipse 120% 90% at 50% 50%, rgba(0,0,0,0) 62%, rgba(110,80,40,.13) 100%); }
    [data-d="a2-nazakat"] .lotus { position: absolute; right: -196px; bottom: -40px; width: 720px; filter: saturate(.9) drop-shadow(0 10px 22px rgba(80,55,25,.10)); }
    [data-d="a2-nazakat"] .tb { left: 88px; width: 430px; top: 204px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="a2-nazakat"] .bism { font-family: 'Noto Nastaliq Urdu', serif; font-size: calc(50px * var(--kt)); line-height: 2; color: #8a6526; }
    [data-d="a2-nazakat"] .hosts { font: 500 calc(30px * var(--kt))/1.25 'Cormorant SC', serif; letter-spacing: .1em; margin-top: 30px; color: #3e3122; }
    [data-d="a2-nazakat"] .inv { font: italic 400 calc(25px * var(--kt))/1.45 'Cormorant Garamond', serif; margin-top: 12px; color: #5b4730; }
    [data-d="a2-nazakat"] .nm { font: 400 calc(118px * var(--kn))/1.02 Corinthia, cursive; white-space: nowrap; }
    [data-d="a2-nazakat"] .nm.g { margin-top: 56px; }
    [data-d="a2-nazakat"] .with { font: 400 calc(22px * var(--kt))/1 Italiana, serif; letter-spacing: .3em; text-transform: uppercase; color: #8a6526; margin: 8px 0 10px; display: flex; align-items: center; gap: 14px; }
    [data-d="a2-nazakat"] .with::before, [data-d="a2-nazakat"] .with::after { content: ""; width: 46px; height: 1px; background: linear-gradient(90deg, rgba(160,122,52,0), #a07a34, rgba(160,122,52,0)); }
    [data-d="a2-nazakat"] .bp { font: italic 400 calc(20px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #5b4730; margin-top: 4px; }
    [data-d="a2-nazakat"] .ev { font: 400 calc(26px * var(--kt))/1 Cinzel, serif; letter-spacing: .44em; margin-right: -.44em; text-transform: uppercase; margin-top: 64px; color: #7a5a22; }
    [data-d="a2-nazakat"] .dt { font: 500 calc(25px * var(--kt))/1.4 'Cormorant SC', serif; letter-spacing: .1em; margin-top: 22px; color: #3e3122; }
    [data-d="a2-nazakat"] .dt sup { font-size: .55em; }
    [data-d="a2-nazakat"] .tm { font: 500 calc(25px * var(--kt))/1.4 'Cormorant SC', serif; letter-spacing: .1em; color: #3e3122; }
    [data-d="a2-nazakat"] .vn { font: italic 500 calc(26px * var(--kt))/1.4 'Cormorant Garamond', serif; margin-top: 14px; color: #3e3122; }
    [data-d="a2-nazakat"] .rs { font: italic 400 calc(20px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 8px; color: #5b4730; }
    [data-d="a2-nazakat"] .ur { font-size: calc(22px * var(--kt)); color: #7a5a22; margin-top: 18px; }
  `,
  render: (H, D) => `
    <div class="layer paper"></div>
    <div class="layer tint"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g transform="translate(772,668)" opacity=".5">${H.mandala(330, { sw: 1 })}<g transform="rotate(7.5)">${H.mandala(205, { sw: .8 })}</g></g>
      <g fill="none" stroke="url(#gold)">
        <rect x="46" y="46" width="908" height="1308" stroke-width="1.4"/>
        <rect x="56" y="56" width="888" height="1288" stroke-width=".7" opacity=".8"/>
      </g>
      <g fill="url(#gold)">
        ${[[46, 46], [954, 46], [46, 1354], [954, 1354]].map(([x, y]) => `<rect x="${x - 5}" y="${y - 5}" width="10" height="10" transform="rotate(45 ${x} ${y})"/>`).join("")}
      </g>
    </svg></div>
    <img class="lotus" src="${H.img("lotus-ogawa-handcoloured-cut.png")}" alt="">
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="450"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="450"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      ${H.f("event", "div", 'class="ev"')}
      <div class="dt">${H.dateLine({ sep: "" }).replace("</span>", "</span><br>")}</div>
      <div class="tm">${H.f("time")}</div>
      <div class="vn">${H.f("venue")}<br>${H.f("place")}</div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`,
});
