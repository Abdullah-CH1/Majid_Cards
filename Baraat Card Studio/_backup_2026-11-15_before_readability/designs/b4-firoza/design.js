/* B4 - Firoza: deep teal card with gold-painted Safavid tree margins as side borders, serif-caps names. */
registerDesign({
  id: "b4-firoza",
  name: "Firoza",
  idea: "Two side margins of gold-painted flowering trees from a Persian manuscript frame a deep turquoise field - a garden of paradise in gold, with names set in stately capitals.",
  css: H => {
    const pw = 124, ph = 1296, ih = 208;   // panel width/height, scaled image height
    const half = ph / 2;
    return `
    [data-d="b4-firoza"] { background: #0d2e33; color: #eef0e6; }
    [data-d="b4-firoza"] .gr { background:
        radial-gradient(ellipse 50% 40% at 50% 42%, rgba(38,92,96,.55), transparent 75%),
        linear-gradient(180deg, #0f3439 0%, #0c2a2f 100%); }
    [data-d="b4-firoza"] .gr::after { content: ""; position: absolute; inset: 0; opacity: .28;
        background: url(${H.img("textured-ivory-paper.webp")}) center/cover; mix-blend-mode: soft-light; }
    [data-d="b4-firoza"] .pn { position: absolute; top: 52px; width: ${pw}px; height: ${ph}px; overflow: hidden; }
    [data-d="b4-firoza"] .pn.l { left: 52px; } [data-d="b4-firoza"] .pn.r { right: 52px; }
    [data-d="b4-firoza"] .rot { position: absolute; width: ${ph}px; height: ${pw}px; left: ${(pw - ph) / 2}px; top: ${(ph - pw) / 2}px; display: flex; }
    [data-d="b4-firoza"] .l .rot { transform: rotate(90deg); } [data-d="b4-firoza"] .r .rot { transform: rotate(-90deg); }
    [data-d="b4-firoza"] .rot i { flex: none; width: ${half}px; height: 100%;
        background: url(${H.img("teal-gold-tree-margin.webp")}) 8% 72%/auto ${ih}px no-repeat;
        filter: saturate(1.25) brightness(.95) contrast(1.06) hue-rotate(-6deg); }
    [data-d="b4-firoza"] .rot i + i { transform: scaleX(-1); }
    [data-d="b4-firoza"] .tb { left: 226px; right: 226px; top: 324px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="b4-firoza"] .bism { font-size: calc(30px * var(--kt)); color: #e7cb83; }
    [data-d="b4-firoza"] .hosts { white-space: nowrap; font: 400 calc(27px * var(--kt)) 'Gilda Display', serif; letter-spacing: .06em; margin-top: 40px; color: #f4f1e6; }
    [data-d="b4-firoza"] .inv { font: italic 400 calc(25px * var(--kt))/1.45 'Cormorant Garamond', serif; margin-top: 12px; color: #d4ddd3; }
    [data-d="b4-firoza"] .nm { font: 500 calc(84px * var(--kn))/1.08 'Cormorant Garamond', serif; letter-spacing: .07em; text-transform: uppercase; white-space: nowrap; }
    [data-d="b4-firoza"] .nm.g { margin-top: 56px; }
    [data-d="b4-firoza"] .with { font: 400 calc(54px * var(--kt))/.9 Italianno, cursive; color: #e7cb83; margin: 4px 0 8px; }
    [data-d="b4-firoza"] .bp { font: italic 400 calc(21px * var(--kt)) 'Cormorant Garamond', serif; color: #d4ddd3; margin-top: 4px; }
    [data-d="b4-firoza"] .rule { width: 220px; height: 16px; margin-top: 56px; }
    [data-d="b4-firoza"] .ev { font: 400 calc(64px * var(--kt))/1 Italianno, cursive; margin-top: 22px; color: #e7cb83; }
    [data-d="b4-firoza"] .dt { font: 400 calc(23px * var(--kt)) 'Gilda Display', serif; letter-spacing: .14em; text-transform: uppercase; margin-top: 16px; color: #f4f1e6; }
    [data-d="b4-firoza"] .vn { font: 500 calc(25px * var(--kt))/1.45 'Cormorant Garamond', serif; margin-top: 16px; color: #dfe6dd; }
    [data-d="b4-firoza"] .ur { font-size: calc(21px * var(--kt)); color: #bfcfc6; margin-top: 28px; }
    [data-d="b4-firoza"] .rs { font: italic 400 calc(19px * var(--kt)) 'Cormorant Garamond', serif; color: #bfcfc6; margin-top: 4px; }
  `;
  },
  render: (H, D) => `
    <div class="layer gr"></div>
    <div class="pn l"><div class="rot"><i></i><i></i></div></div>
    <div class="pn r"><div class="rot"><i></i><i></i></div></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none" stroke="url(#gold)">
        <rect x="40" y="40" width="920" height="1320" stroke-width="1.4"/>
        <rect x="52" y="52" width="124" height="1296" stroke-width="1.2"/>
        <rect x="824" y="52" width="124" height="1296" stroke-width="1.2"/>
        <path d="${H.ogeeD(214, 572, 380, 1310, 196)}" stroke-width="1.3"/>
        <path d="${H.ogeeD(224, 552, 384, 1300, 188)}" stroke-width=".6" opacity=".75"/>
      </g>
      <g fill="url(#goldBright)">
        <path d="M500,142 l6,10 l-6,10 l-6,-10z"/><circle cx="500" cy="134" r="2.4"/><rect x="499.5" y="162" width="1" height="18"/>
      </g>
    </svg></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts" data-fit="520"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-light" data-fit="540"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-light" data-fit="540"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <svg class="rule" viewBox="0 0 220 16"><g fill="none" stroke="#d9bb72" stroke-width="1"><path d="M0,8 H92"/><path d="M128,8 H220"/><path d="M110,1 l7,7 l-7,7 l-7,-7z"/></g><circle cx="110" cy="8" r="1.8" fill="#d9bb72"/></svg>
      ${H.f("event", "div", 'class="ev"')}
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;&middot;&nbsp; ${H.f("venue")}<br>${H.f("place")}</div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`,
});
