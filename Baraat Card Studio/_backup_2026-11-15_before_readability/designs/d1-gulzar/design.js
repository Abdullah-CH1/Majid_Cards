/* D1 Gulzar - the client's sage engraved frame (Reference B), refined for the Baraat with a gold Mughal arch hairline inside. */
registerDesign({
  id: "d1-gulzar",
  name: "Gulzar",
  idea: "A vintage sage-green engraved garden frame on white cotton paper, with a whisper-thin gold Mughal arch inside and the names in warm ochre script - your favourite sage card, made finer for the Baraat.",
  css: H => `
    [data-d="d1-gulzar"] { background: #fcfbf7; color: #4c5e47; }
    [data-d="d1-gulzar"] .paper { background: url(${H.img("textured-ivory-paper.webp")}) center/cover; filter: saturate(.3) contrast(.55) brightness(1.5); mix-blend-mode: multiply; opacity: .9; }
    [data-d="d1-gulzar"] .frame { background: url(${H.img("engraved-floral-frame-sage-cut.png")}) center/100% 100% no-repeat; inset: 8px 10px 4px 10px; opacity: .92; filter: saturate(1.25) brightness(.94); }
    [data-d="d1-gulzar"] .glow { background: radial-gradient(ellipse 34% 38% at 50% 50%, rgba(255,255,254,.75), rgba(255,255,254,0) 100%); }
    [data-d="d1-gulzar"] .tb { left: 262px; right: 262px; top: 362px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="d1-gulzar"] .bism { font-size: calc(28px * var(--kt)); color: #a8792c; line-height: 1.2; }
    [data-d="d1-gulzar"] .hosts { font: 500 calc(27px * var(--kt)) 'Cormorant SC', serif; letter-spacing: .1em; margin-top: 30px; color: #3f5139; }
    [data-d="d1-gulzar"] .inv { font: italic 400 calc(23px * var(--kt))/1.4 'Cormorant Garamond', serif; margin-top: 6px; color: #55684f; }
    [data-d="d1-gulzar"] .nm { font: 400 calc(92px * var(--kn))/1.14 'Ephesis', cursive; white-space: nowrap; color: #a8792c; }
    [data-d="d1-gulzar"] .nm.g { margin-top: 30px; }
    [data-d="d1-gulzar"] .with { font: italic 400 calc(24px * var(--kt))/1 'Cormorant Garamond', serif; color: #5d7257; margin: -4px 0 -2px; }
    [data-d="d1-gulzar"] .bp { font: italic 400 calc(20px * var(--kt)) 'Cormorant Garamond', serif; color: #5d7257; margin-top: 2px; }
    [data-d="d1-gulzar"] .orn { width: 150px; height: 18px; margin-top: 30px; }
    [data-d="d1-gulzar"] .ev { font: 500 calc(21px * var(--kt)) Cinzel, serif; letter-spacing: .48em; margin: 22px 0 0 .48em; color: #3f5139; }
    [data-d="d1-gulzar"] .dt { font: 400 calc(23px * var(--kt))/1.3 'Cormorant Garamond', serif; margin-top: 18px; letter-spacing: .03em; color: #34442f; font-weight: 500; }
    [data-d="d1-gulzar"] .tm { font: 400 calc(18px * var(--kt)) Marcellus, serif; letter-spacing: .22em; text-transform: uppercase; margin-top: 8px; color: #55684f; }
    [data-d="d1-gulzar"] .vn { font: 500 calc(22px * var(--kt))/1.35 'Cormorant Garamond', serif; margin-top: 14px; color: #34442f; }
    [data-d="d1-gulzar"] .vn .pl { font-weight: 400; color: #55684f; }
    [data-d="d1-gulzar"] .ur { font-size: calc(17px * var(--kt)); color: #a8792c; margin-top: 14px; }
    [data-d="d1-gulzar"] .rs { font: italic calc(17px * var(--kt)) 'Cormorant Garamond', serif; color: #55684f; margin-top: 4px; }
  `,
  render: (H, D) => `
    <div class="layer paper"></div>
    <div class="layer frame"></div>
    <div class="layer glow"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none" stroke="url(#gold)">
        <path d="${H.archD(234, 532, 560, 1118, .53, 7)}" stroke-width="1.6"/>
        <path d="${H.archD(243, 514, 560, 1109, .53, 7)}" stroke-width=".7" opacity=".8"/>
      </g>
      <g fill="url(#gold)"><circle cx="500" cy="${H.archApex(532, 560, .53) - 12}" r="2.6"/></g>
    </svg></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g" data-fit="470"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm" data-fit="470"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <svg class="orn" viewBox="0 0 150 18"><g fill="none" stroke="#a8792c" stroke-width="1" stroke-linecap="round"><path d="M4,9 H58"/><path d="M92,9 H146"/><path d="M75,2 L82,9 L75,16 L68,9 Z"/></g><circle cx="62" cy="9" r="1.6" fill="#a8792c"/><circle cx="88" cy="9" r="1.6" fill="#a8792c"/></svg>
      ${H.f("event", "div", 'class="ev"')}
      <div class="dt">${H.dateLine()}</div>
      ${H.f("time", "div", 'class="tm"')}
      <div class="vn">${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`,
});
