/* D2 Halqa - an antique engraved flower wreath in gold, ringing the couple's initials, over classical serif typography. */
registerDesign({
  id: "d2-halqa",
  name: "Halqa",
  idea: "A 19th-century engraved flower wreath, printed in antique gold, rings the couple's initials like a family crest - with classic Bodoni lettering below on warm ivory cotton.",
  css: H => `
    [data-d="d2-halqa"] { background: #f7f1e6; color: #2e2519; }
    [data-d="d2-halqa"] .paper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; filter: saturate(0) contrast(.42) brightness(1.52); mix-blend-mode: multiply; opacity: .5; }
    [data-d="d2-halqa"] .wreath { position: absolute; left: 196px; top: 160px; width: 608px; height: 441px;
      background: url(${H.img("engraved-flower-wreath-gold-cut.png")}) center/contain no-repeat; filter: brightness(.78) saturate(1.35) contrast(1.15); }
    [data-d="d2-halqa"] .mono { position: absolute; left: 196px; top: 160px; width: 608px; height: 441px; display: flex; align-items: center; justify-content: center; gap: 4px; }
    [data-d="d2-halqa"] .mono .ml { font: 400 calc(112px * var(--kn))/1 'Bodoni Moda', serif; }
    [data-d="d2-halqa"] .mono .md { font: 400 calc(64px * var(--kn))/1 'Italianno', cursive; color: #9b7634; margin: 22px 6px 0; }
    [data-d="d2-halqa"] .tb { left: 120px; right: 120px; top: 88px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="d2-halqa"] .bism { font-size: calc(33px * var(--kt)); color: #6e5221; line-height: 1.2; }
    [data-d="d2-halqa"] .gap { height: 500px; }
    [data-d="d2-halqa"] .hosts { font: 400 calc(26px * var(--kt)) 'Bodoni Moda', serif; letter-spacing: .16em; text-transform: uppercase; }
    [data-d="d2-halqa"] .inv { font: italic 400 calc(24px * var(--kt))/1.42 'Bodoni Moda', serif; margin-top: 12px; color: #4a3b27; }
    [data-d="d2-halqa"] .nm { font: 400 calc(66px * var(--kn))/1.14 'Bodoni Moda', serif; letter-spacing: .1em; text-transform: uppercase; white-space: nowrap; margin-left: .1em; }
    [data-d="d2-halqa"] .nm.g { margin-top: 34px; }
    [data-d="d2-halqa"] .with { font: 400 calc(54px * var(--kt))/.9 'Italianno', cursive; color: #8f6c2c; margin: 2px 0 4px; }
    [data-d="d2-halqa"] .bp { font: italic 400 calc(19px * var(--kt)) 'Bodoni Moda', serif; color: #4a3b27; margin-top: 6px; }
    [data-d="d2-halqa"] .evrow { display: flex; align-items: center; gap: 22px; margin-top: 40px; color: #9b7634; }
    [data-d="d2-halqa"] .evrow i { display: block; width: 90px; height: 1px; background: currentColor; }
    [data-d="d2-halqa"] .ev { font: 500 calc(20px * var(--kt)) Cinzel, serif; letter-spacing: .5em; margin-left: .5em; color: #7a5b24; }
    [data-d="d2-halqa"] .dt { font: 400 calc(24px * var(--kt))/1.3 'Bodoni Moda', serif; margin-top: 20px; letter-spacing: .02em; }
    [data-d="d2-halqa"] .tm { font: italic 400 calc(22px * var(--kt)) 'Bodoni Moda', serif; margin-top: 6px; color: #4a3b27; }
    [data-d="d2-halqa"] .vn { font: 400 calc(18px * var(--kt))/1.6 'Bodoni Moda', serif; letter-spacing: .2em; text-transform: uppercase; margin-top: 18px; }
    [data-d="d2-halqa"] .vn .pl { letter-spacing: .12em; color: #4a3b27; }
    [data-d="d2-halqa"] .ur { font-size: calc(17px * var(--kt)); color: #6e5221; margin-top: 14px; }
    [data-d="d2-halqa"] .rs { font: italic calc(17px * var(--kt)) 'Bodoni Moda', serif; color: #4a3b27; margin-top: 4px; }
  `,
  render: (H, D) => `
    <div class="layer paper"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none" stroke="url(#gold)">
        <rect x="46" y="46" width="908" height="1308" stroke-width="1.8"/>
        <rect x="56" y="56" width="888" height="1288" stroke-width=".7"/>
      </g>
      <g fill="url(#gold)">
        ${[[46, 46], [954, 46], [46, 1354], [954, 1354]].map(([x, y]) => `<path d="M${x},${y - 7} L${x + 7},${y} L${x},${y + 7} L${x - 7},${y} Z"/>`).join("")}
      </g>
    </svg></div>
    <div class="wreath"></div>
    <div class="mono"><span class="ml foil foil-deep">${H.monoG()}</span><span class="md">&amp;</span><span class="ml foil foil-deep">${H.monoB()}</span></div>
    <div class="tb">
      ${H.bism()}
      <div class="gap"></div>
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g" data-fit="720"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm" data-fit="720"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="evrow"><i></i>${H.f("event", "div", 'class="ev"')}<i></i></div>
      <div class="dt">${H.dateLine()}</div>
      ${H.f("time", "div", 'class="tm"')}
      <div class="vn">${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`,
});
