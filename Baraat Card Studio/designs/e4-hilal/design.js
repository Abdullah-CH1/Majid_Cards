/* E4 - Hilal: a tall Mughal arch window holds a dusk sky, a new crescent and a marble jali parapet; editorial type alongside. */
registerDesign((() => {
  const ID = "e4-hilal", S = `[data-d="${ID}"]`;
  const WX = 64, WW = 224, WT = 100, WB = 1300, K = .62, WH = WB - WT;
  const spring = (apex, w) => apex - H.archApex(w, 0, K);
  const local = H.archD(0, WW, spring(0, WW), WH, K, 7);
  return {
    id: ID,
    name: "Hilal",
    idea: "A tall Mughal window opens onto a dusk sky with the new crescent, glowing through a marble jali; the wording stands beside it, large and clear, in a calm column.",
    css: H => `
      ${S} { background: #f4efe6; color: #1c2340; }
      ${S} .paper { background: url(${H.img("textured-ivory-paper.webp")}) center / cover; mix-blend-mode: multiply; opacity: .28; }
      ${S} .win { position: absolute; left: ${WX}px; top: ${WT}px; width: ${WW}px; height: ${WH}px; clip-path: path("${local}");
        background: url(${H.img("crescent-moon-dusk.webp")}) 50% 0 / auto ${WH + 120}px no-repeat; }
      ${S} .win::before { content: ""; position: absolute; inset: 0; background: linear-gradient(rgba(14,18,36,.25), rgba(14,18,36,0) 40%); }
      ${S} .win img { position: absolute; width: 300px; left: -38px; bottom: -150px; filter: brightness(1.02) contrast(1.05) drop-shadow(0 -6px 14px rgba(20,10,30,.35)); }
      ${S} .win::after { content: ""; position: absolute; inset: 0; box-shadow: inset 0 0 22px 4px rgba(20,16,30,.35); }
      ${S} .tb { left: 336px; right: 64px; top: 120px; height: 1170px; text-align: center; display: flex; flex-direction: column; justify-content: space-between; }
      ${S} .grp { display: flex; flex-direction: column; align-items: center; }
      ${S} .bism { font-size: calc(48px * var(--kt)); color: #3e2a10; line-height: 1.2; }
      ${S} .hosts { font: 400 calc(44px * var(--kt))/1.2 Marcellus, serif; letter-spacing: .03em; margin-top: 24px; }
      ${S} .inv { font: italic 500 calc(38px * var(--kt))/1.28 'Cormorant Garamond', serif; margin-top: 10px; }
      ${S} .nm { font: 400 calc(162px * var(--kn))/1.02 'Rouge Script', cursive; white-space: nowrap; filter: drop-shadow(0 1px 0 rgba(60,40,10,.3)); }
      ${S} .with { font: italic 500 calc(46px * var(--kt))/1 'Cormorant Garamond', serif; color: #5a3e10; margin: 0; }
      ${S} .bp { font: italic 500 calc(36px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 4px; }
      ${S} .ev { font: 400 calc(50px * var(--kt))/1.2 Marcellus, serif; letter-spacing: .14em; padding-left: .14em; text-transform: uppercase; filter: drop-shadow(0 1px 0 rgba(60,40,10,.3)); }
      ${S} .dt { font: 600 calc(44px * var(--kt))/1.25 'Cormorant Garamond', serif; margin-top: 8px; }
      ${S} .vn { font: 600 calc(40px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 6px; }
      ${S} .vn .p { font-weight: 500; font-size: calc(38px * var(--kt)); }
      ${S} .ur { font-size: calc(38px * var(--kt)); line-height: 1.8; white-space: nowrap; color: #232a3d; margin-top: 2px; }
      ${S} .rs { font: italic 500 calc(34px * var(--kt)) 'Cormorant Garamond', serif; margin-top: 0; }
    `,
    render: (H, D) => {
      const arch = (o, sw, op, st = "url(#gold)") => { const w = WW + 2 * o; return `<path d="${H.archD(WX - o, w, spring(WT - o, w), WB + o, K, 7)}" fill="none" stroke="${st}" stroke-width="${sw}" opacity="${op}"/>`; };
      return `
      <div class="layer paper"></div>
      <div class="win"><img src="${H.img("marble-jali-screen-cut.png")}" alt=""></div>
      <div class="layer"><svg viewBox="0 0 1000 1400">
        ${arch(9, 6.6, .3, "#6b4c14")}${arch(20, 2.8, .22, "#6b4c14")}${arch(9, 5, 1)}${arch(20, 1.8, 1)}
      </svg></div>
      <div class="tb">
        <div class="grp">${H.bism()}
        ${H.f("hosts", "div", 'class="hosts"')}
        <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div></div>
        <div class="grp">${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="596"')}
        ${H.f("joiner", "div", 'class="with"')}
        ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="596"')}
        ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
        </div>
        <div class="grp">${H.f("event", "div", 'class="ev foil foil-deep"')}
        <div class="dt">${H.dateLine()}</div>
        <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br><span class="p">${H.f("place")}</span></div>
        ${H.urdu()}
        ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}</div>
      </div>`;
    },
  };
})());
