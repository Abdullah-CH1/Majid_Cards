/* B1 - Shamsa: Shah Jahan's gold-and-lapis rosette as a single medallion on a midnight-navy ground. */
registerDesign({
  id: "b1-shamsa",
  name: "Shamsa",
  idea: "A royal Mughal sun-medallion in gold and lapis glows on a midnight-blue ground, framed by fine gold rules - regal, calm and unmistakably evening.",
  css: H => `
    [data-d="b1-shamsa"] { background: #07122a; color: #efe6d2; }
    [data-d="b1-shamsa"] .sky { background: url(${H.img("starry-night-sky.webp")}) center 30%/cover; filter: brightness(.62) saturate(.9); }
    [data-d="b1-shamsa"] .wash { background:
        radial-gradient(ellipse 60% 34% at 50% 23%, rgba(40,62,120,.45), transparent 70%),
        radial-gradient(ellipse 90% 70% at 50% 55%, transparent 40%, rgba(2,6,18,.75) 100%); }
    [data-d="b1-shamsa"] .ros { position: absolute; left: 50%; top: 146px; width: 392px; height: 392px; translate: -50% 0;
        background: url(${H.img("mughal-shamsa-rosette-cut.png")}) center/contain no-repeat;
        -webkit-mask-image: radial-gradient(circle closest-side, #000 74%, rgba(0,0,0,.45) 84%, transparent 94%);
                mask-image: radial-gradient(circle closest-side, #000 74%, rgba(0,0,0,.45) 84%, transparent 94%);
        filter: drop-shadow(0 0 30px rgba(0,0,0,.6)); }
    [data-d="b1-shamsa"] .tb { left: 120px; right: 120px; top: 574px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="b1-shamsa"] .bism { position: absolute; left: 0; right: 0; top: 88px; text-align: center; font-size: calc(34px * var(--kt)); color: #e2c57e; }
    [data-d="b1-shamsa"] .hosts { white-space: nowrap; font: 500 calc(30px * var(--kt)) 'Cormorant SC', serif; letter-spacing: .16em; color: #f3ead6; }
    [data-d="b1-shamsa"] .inv { font: italic 400 calc(26px * var(--kt))/1.38 'Cormorant Garamond', serif; margin-top: 10px; color: #d9cfbb; }
    [data-d="b1-shamsa"] .nm { font: 400 calc(108px * var(--kn))/1.12 'Pinyon Script', cursive; white-space: nowrap; }
    [data-d="b1-shamsa"] .nm.g { margin-top: 26px; }
    [data-d="b1-shamsa"] .with { font: italic 400 calc(28px * var(--kt))/1 'Cormorant Garamond', serif; color: #e2c57e; margin: 2px 0 4px; }
    [data-d="b1-shamsa"] .bp { font: italic 400 calc(22px * var(--kt)) 'Cormorant Garamond', serif; color: #d9cfbb; margin-top: 2px; }
    [data-d="b1-shamsa"] .ev { display: flex; align-items: center; gap: 22px; margin-top: 36px; color: #e2c57e;
        font: 500 calc(22px * var(--kt)) Cinzel, serif; letter-spacing: .55em; padding-left: .55em; }
    [data-d="b1-shamsa"] .ev i { display: block; width: 70px; height: 1px; background: linear-gradient(90deg, transparent, #d9b866); }
    [data-d="b1-shamsa"] .ev i:last-child { transform: scaleX(-1); }
    [data-d="b1-shamsa"] .dt { font: 400 calc(25px * var(--kt)) Marcellus, serif; letter-spacing: .12em; text-transform: uppercase; margin-top: 20px; color: #f3ead6; }
    [data-d="b1-shamsa"] .vn { font: 500 calc(26px * var(--kt))/1.45 'Cormorant Garamond', serif; margin-top: 12px; color: #e6dcc6; }
    [data-d="b1-shamsa"] .vn b { font-weight: 600; color: #f3ead6; }
    [data-d="b1-shamsa"] .ur { font-size: calc(22px * var(--kt)); color: #cdbf9f; margin-top: 14px; }
    [data-d="b1-shamsa"] .rs { font: 400 calc(20px * var(--kt)) 'Cormorant Garamond', serif; letter-spacing: .12em; color: #cdbf9f; margin-top: 6px; }
  `,
  render: (H, D) => {
    const corner = (x, y, sx, sy) => `<g transform="translate(${x},${y}) scale(${sx},${sy})">
        <path d="M0,26 L0,0 L26,0" /><path d="M7,32 L7,7 L32,7" stroke-width=".7"/>
        <rect x="-3.2" y="-3.2" width="6.4" height="6.4" transform="rotate(45)" fill="url(#goldBright)" stroke="none"/></g>`;
    return `
    <div class="layer sky"></div>
    <div class="layer wash"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none" stroke="url(#gold)">
        <rect x="46" y="46" width="908" height="1308" stroke-width="1.6"/>
        <rect x="58" y="58" width="884" height="1284" stroke-width=".7" opacity=".8"/>
        ${corner(70, 70, 1, 1)}${corner(930, 70, -1, 1)}${corner(70, 1330, 1, -1)}${corner(930, 1330, -1, -1)}
      </g>
      <g fill="url(#goldBright)">
        <rect x="496" y="1324" width="8" height="8" transform="rotate(45 500 1328)"/>
      </g>
      <circle cx="500" cy="342" r="206" fill="none" stroke="url(#gold)" stroke-width=".8" opacity=".55"/>
    </svg></div>
    ${H.bism('class="bism"')}
    <div class="ros"></div>
    <div class="tb">
      ${H.f("hosts", "div", 'class="hosts" data-fit="700"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-light" data-fit="700"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-light" data-fit="700"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="ev"><i></i>${H.f("event")}<i></i></div>
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;&middot;&nbsp; <b>${H.f("venue")}</b><br>${H.f("place")}</div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`;
  },
});
