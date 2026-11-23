/* REFERENCE EXAMPLE - shows the contract. Not part of the final set (folders starting with "_" are skipped). */
registerDesign({
  id: "_example-paper-arch",
  name: "Example - Paper Arch",
  idea: "Handmade paper, one thin gold cusped arch, generous space - typography does the work.",
  css: H => `
    [data-d="_example-paper-arch"] { background: #f3ebdd; color: #4a3826; }
    [data-d="_example-paper-arch"] .bg { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; }
    [data-d="_example-paper-arch"] .tb { left: 200px; right: 200px; top: 250px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="_example-paper-arch"] .bism { font-size: calc(44px * var(--kt)); color: #8a6a2f; }
    [data-d="_example-paper-arch"] .hosts { font: 500 calc(34px * var(--kt)) 'Cormorant SC', serif; letter-spacing: .06em; margin-top: 26px; }
    [data-d="_example-paper-arch"] .inv { font: italic 400 calc(27px * var(--kt))/1.35 'Cormorant Garamond', serif; margin-top: 6px; }
    [data-d="_example-paper-arch"] .nm { font: 400 calc(110px * var(--kn))/1.15 'Pinyon Script', cursive; white-space: nowrap; margin-top: 18px; }
    [data-d="_example-paper-arch"] .with { font: italic calc(30px * var(--kt)) 'Cormorant Garamond', serif; }
    [data-d="_example-paper-arch"] .ev { font: 500 calc(24px * var(--kt)) Cinzel, serif; letter-spacing: .5em; margin-top: 34px; color: #8a6a2f; }
    [data-d="_example-paper-arch"] .dt { font: 400 calc(27px * var(--kt)) Marcellus, serif; letter-spacing: .14em; text-transform: uppercase; margin-top: 16px; }
    [data-d="_example-paper-arch"] .vn { font: 500 calc(27px * var(--kt))/1.4 'Cormorant Garamond', serif; margin-top: 12px; }
  `,
  render: (H, D) => `
    <div class="layer bg"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <path d="${H.archD(160, 680, 560, 1290, .6, 7)}" fill="none" stroke="url(#gold)" stroke-width="2.5"/>
    </svg></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm foil foil-deep" data-fit="600"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="600"')}
      ${H.f("event", "div", 'class="ev"')}
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;·&nbsp; ${H.f("venue")}<br>${H.f("place")}</div>
      ${H.urdu()}
    </div>`,
});
