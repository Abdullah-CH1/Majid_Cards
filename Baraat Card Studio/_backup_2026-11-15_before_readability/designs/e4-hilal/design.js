/* E4 - Hilal: a tall Mughal arch window holds a dusk sky, a new crescent and a marble jali parapet; editorial type alongside. */
registerDesign((() => {
  const ID = "e4-hilal", S = `[data-d="${ID}"]`;
  const WX = 84, WW = 330, WT = 96, WB = 1304, K = .62, WH = WB - WT;
  const spring = (apex, w) => apex - H.archApex(w, 0, K);
  const local = H.archD(0, WW, spring(0, WW), WH, K, 7);
  return {
    id: ID,
    name: "Hilal",
    idea: "A tall Mughal window opens onto a dusk sky with the new crescent, glowing through a marble jali; the wording stands beside it in a calm editorial column.",
    css: H => `
      ${S} { background: #f4efe6; color: #232a3d; }
      ${S} .paper { background: url(${H.img("textured-ivory-paper.webp")}) center / cover; mix-blend-mode: multiply; opacity: .28; }
      ${S} .win { position: absolute; left: ${WX}px; top: ${WT}px; width: ${WW}px; height: ${WH}px; clip-path: path("${local}");
        background: url(${H.img("crescent-moon-dusk.webp")}) 50% 0 / auto ${WH + 120}px no-repeat; }
      ${S} .win::before { content: ""; position: absolute; inset: 0; background: linear-gradient(rgba(14,18,36,.25), rgba(14,18,36,0) 40%); }
      ${S} .win img { position: absolute; width: 420px; left: -45px; bottom: -210px; filter: brightness(1.02) contrast(1.05) drop-shadow(0 -6px 14px rgba(20,10,30,.35)); }
      ${S} .win::after { content: ""; position: absolute; inset: 0; box-shadow: inset 0 0 22px 4px rgba(20,16,30,.35); }
      ${S} .tb { left: 486px; right: 76px; top: 138px; height: 1120px; text-align: left; display: flex; flex-direction: column; justify-content: space-between; }
      ${S} .grp { display: flex; flex-direction: column; align-items: flex-start; }
      ${S} .bism { font-size: calc(33px * var(--kt)); color: #6b5226; }
      ${S} .hosts { font: 500 calc(23px * var(--kt)) Marcellus, serif; letter-spacing: .2em; text-transform: uppercase; margin-top: 34px; }
      ${S} .inv { font: italic 400 calc(25px * var(--kt))/1.42 'Cormorant Garamond', serif; margin-top: 12px; color: #3a4156; }
      ${S} .nm { font: 400 calc(92px * var(--kn))/1.12 'Pinyon Script', cursive; white-space: nowrap; margin-left: -6px; }
      ${S} .g { margin-top: 0; }
      ${S} .with { font: italic 400 calc(28px * var(--kt))/1 'Cormorant Garamond', serif; color: #8a6a2e; margin: 6px 0 6px 6px; }
      ${S} .bp { font: italic 400 calc(21px * var(--kt)) 'Cormorant Garamond', serif; margin-top: 4px; }
      ${S} .rule { width: 120px; height: 1px; background: linear-gradient(90deg, #b39352, rgba(179,147,82,0)); margin: 0 0 26px; }
      ${S} .ev { font: 500 calc(20px * var(--kt)) Marcellus, serif; letter-spacing: .5em; text-transform: uppercase; color: #7b5f2a; }
      ${S} .dt { font: 400 calc(30px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 16px; font-weight: 500; }
      ${S} .dt .d { display: block; font: 500 calc(20px * var(--kt)) Marcellus, serif; letter-spacing: .2em; text-transform: uppercase; }
      ${S} .tm { font: 500 calc(24px * var(--kt)) 'Cormorant Garamond', serif; letter-spacing: .06em; margin-top: 2px; }
      ${S} .vn { font: 500 calc(26px * var(--kt))/1.4 'Cormorant Garamond', serif; margin-top: 18px; }
      ${S} .vn .p { font-style: italic; font-weight: 400; color: #3a4156; }
      ${S} .ur { font-size: calc(20px * var(--kt)); color: #6b5226; margin-top: 22px; }
      ${S} .rs { font: 400 calc(17px * var(--kt)) Marcellus, serif; letter-spacing: .18em; margin-top: 6px; color: #6b5226; }
    `,
    render: (H, D) => {
      const arch = (o, sw, op) => { const w = WW + 2 * o; return `<path d="${H.archD(WX - o, w, spring(WT - o, w), WB + o, K, 7)}" fill="none" stroke="url(#gold)" stroke-width="${sw}" opacity="${op}"/>`; };
      return `
      <div class="layer paper"></div>
      <div class="win"><img src="${H.img("marble-jali-screen-cut.png")}" alt=""></div>
      <div class="layer"><svg viewBox="0 0 1000 1400">
        ${arch(10, 1.8, 1)}${arch(19, .8, .75)}
        <line x1="486" y1="1304" x2="924" y2="1304" stroke="url(#gold)" stroke-width="1" opacity=".7"/>
      </svg></div>
      <div class="tb">
        <div class="grp">${H.bism()}
        ${H.f("hosts", "div", 'class="hosts"')}
        <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div></div>
        <div class="grp">${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="440"')}
        ${H.f("joiner", "div", 'class="with"')}
        ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="440"')}
        ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
        </div>
        <div class="grp"><div class="rule"></div>
        ${H.f("event", "div", 'class="ev"')}
        <div class="dt"><span class="d">${H.f("day")}</span>${H.f("dateNum")}<sup>${H.f("dateSup")}</sup> ${H.f("month")} ${H.f("year")}</div>
        ${H.f("time", "div", 'class="tm"')}
        <div class="vn">${H.f("venue")}<br><span class="p">${H.f("place")}</span></div>
        ${H.urdu()}
        ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}</div>
      </div>`;
    },
  };
})());
