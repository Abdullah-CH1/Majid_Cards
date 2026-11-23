/* C1 - Muraqqa : a page from the Shah Jahan Album - painted flowering-plant margins around a ruled ivory panel */
registerDesign({
  id: "c1-muraqqa",
  name: "Muraqqa",
  idea: "A page from the Shah Jahan Album: real 17th-century painted flowering-plant margins on buff paper, framing a calm ivory panel ruled in gold, lapis and vermilion.",
  css: H => {
    const P = '[data-d="c1-muraqqa"]';
    return `
    ${P} { background: #b48a5c; color: #3a2a1a; }
    ${P} .buff { background: linear-gradient(180deg, #b78d5f, #b08657 50%, #b58b5c); }
    ${P} .grain { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: multiply; opacity: .45; filter: contrast(1.4); }
    ${P} .side { position: absolute; top: -40px; bottom: -40px; width: 84px;
        background: url(${H.img("mughal-flower-border-side.webp")}) -24px -30px / auto 1520px no-repeat;
        -webkit-mask-image: linear-gradient(90deg, transparent, #000 8px, #000 70px, transparent 80px);
                mask-image: linear-gradient(90deg, transparent, #000 8px, #000 70px, transparent 80px); }
    ${P} .side.l { left: 20px; }
    ${P} .side.r { right: 20px; transform: scaleX(-1); }
    ${P} .band { position: absolute; left: 112px; right: 112px; height: 168px;
        background: url(${H.img("mughal-flower-border-band.webp")}) -32px -4px / 840px auto no-repeat;
        -webkit-mask-image: linear-gradient(90deg, transparent, #000 18px, #000 calc(100% - 18px), transparent);
                mask-image: linear-gradient(90deg, transparent, #000 18px, #000 calc(100% - 18px), transparent); }
    ${P} .band.t { top: 0; }
    ${P} .band.b { bottom: -4px; transform: scaleX(-1); }
    ${P} .panel { position: absolute; left: 138px; top: 178px; width: 724px; height: 1044px;
        background: #f5ecd9;
        box-shadow: 0 0 0 1px rgba(80,50,20,.25), 0 2px 10px rgba(60,35,10,.25); }
    ${P} .panel::before { content: ""; position: absolute; inset: 0; background: url(${H.img("textured-ivory-paper.webp")}) center/cover;
        mix-blend-mode: multiply; opacity: .32; filter: brightness(1.12) contrast(1.15); }
    ${P} .panel::after { content: ""; position: absolute; inset: 0;
        background: radial-gradient(ellipse 70% 60% at 50% 45%, rgba(255,251,240,.55), rgba(255,251,240,0) 75%),
                    radial-gradient(ellipse 110% 100% at 50% 50%, transparent 62%, rgba(150,110,60,.18)); }
    ${P} .tb { left: 200px; right: 200px; top: 290px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(44px * var(--kt)); color: #7d5a1e; }
    ${P} .hosts { font: 500 calc(33px * var(--kt))/1.2 'Cormorant SC', serif; letter-spacing: .1em; margin-top: 38px; color: #2f2114; }
    ${P} .inv { font: italic 400 calc(26px * var(--kt))/1.42 'Cormorant Garamond', serif; margin-top: 8px; color: #54402a; }
    ${P} .nm { font: 400 calc(108px * var(--kn))/1.14 'Pinyon Script', cursive; white-space: nowrap; }
    ${P} .nm.g { margin-top: 34px; }
    ${P} .with { font: italic 400 calc(28px * var(--kt))/1 'Cormorant Garamond', serif; color: #6a5133; margin: 0 0 2px; }
    ${P} .bp { font: italic 400 calc(20px * var(--kt))/1.3 'Cormorant Garamond', serif; color: #6a5133; margin-top: 2px; }
    ${P} .ev { display: flex; align-items: center; gap: 14px; margin-top: 46px; }
    ${P} .ev .f { font: 500 calc(22px * var(--kt))/1 Cinzel, serif; letter-spacing: .5em; margin-right: -.5em; color: #2d4373; }
    ${P} .ev i { display: block; width: 7px; height: 7px; background: #a8432c; transform: rotate(45deg); }
    ${P} .ev b { display: block; width: 54px; height: 1px; background: linear-gradient(90deg, transparent, #9c7631); }
    ${P} .ev b.r { background: linear-gradient(270deg, transparent, #9c7631); }
    ${P} .dt { font: 400 calc(24px * var(--kt))/1.3 Marcellus, serif; letter-spacing: .13em; text-transform: uppercase; margin-top: 24px; color: #2f2114; }
    ${P} .vn { font: 500 calc(27px * var(--kt))/1.45 'Cormorant Garamond', serif; margin-top: 10px; color: #3a2a1a; }
    ${P} .vn .tm { font-weight: 600; }
    ${P} .rs { font: italic 400 calc(19px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 6px; color: #6a5133; }
    ${P} .ur { font-size: calc(23px * var(--kt)); color: #7d5a1e; margin-top: 24px; }
  `;
  },
  render: (H, D) => {
    /* jadval: the classic Mughal ruling - vermilion hairline, lapis line, gold band, ink hairline */
    const x = 138, y = 178, w = 724, h = 1044;
    const r = (o, sw, st) => `<rect x="${x - o}" y="${y - o}" width="${w + 2 * o}" height="${h + 2 * o}" fill="none" stroke="${st}" stroke-width="${sw}"/>`;
    const inner = (o, sw, st) => `<rect x="${x + o}" y="${y + o}" width="${w - 2 * o}" height="${h - 2 * o}" fill="none" stroke="${st}" stroke-width="${sw}"/>`;
    return `
    <div class="layer buff"></div>
    <div class="layer grain"></div>
    <div class="side l"></div><div class="side r"></div>
    <div class="band t"></div><div class="band b"></div>
    <div class="panel"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      ${r(13, 1, "#a8432c")}
      ${r(9, 1.4, "#2d4373")}
      ${r(4.5, 4, "url(#gold)")}
      ${r(1.5, .8, "#3a2614")}
      ${inner(16, 1, "url(#gold)")}
      ${inner(20, .6, "#2d4373")}
    </svg></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="600"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="600"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="ev"><b></b><i></i>${H.f("event")}<i></i><b class="r"></b></div>
      <div class="dt">${H.dateLine()}</div>
      <div class="vn"><span class="tm">${H.f("time")}</span> &nbsp;·&nbsp; ${H.f("venue")}<br>${H.f("place")}</div>
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
      ${H.urdu()}
    </div>`;
  },
});
