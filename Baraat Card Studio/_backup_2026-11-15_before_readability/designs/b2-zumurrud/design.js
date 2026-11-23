/* B2 - Zumurrud: emerald velvet with an inset ivory Mughal arch, edged in gold leaf. */
registerDesign({
  id: "b2-zumurrud",
  name: "Zumurrud",
  idea: "Deep emerald velvet opens into an ivory paper arch edged in real gold leaf - the richness of a Baraat evening with the clean calm of a classic card.",
  css: H => {
    const outer = H.archD(150, 700, 560, 1300, .56, 7);
    const inner = H.archD(162, 676, 560, 1288, .56, 7);
    return `
    [data-d="b2-zumurrud"] { background: #06261d; color: #173f33; }
    [data-d="b2-zumurrud"] .vel { background: url(${H.img("emerald-velvet.webp")}) center/cover; filter: brightness(.95) saturate(1.05); transform: scaleX(-1); }
    [data-d="b2-zumurrud"] .lift { background: linear-gradient(160deg, #0d4a35, #08301f 60%, #0b3b2a); mix-blend-mode: screen; opacity: .55; }
    [data-d="b2-zumurrud"] .vig { background: radial-gradient(ellipse 45% 40% at 88% 30%, rgba(20,110,80,.28), transparent 70%), radial-gradient(ellipse 50% 40% at 15% 85%, rgba(20,110,80,.18), transparent 70%), radial-gradient(ellipse 75% 65% at 50% 50%, transparent 45%, rgba(0,10,6,.55) 100%); }
    [data-d="b2-zumurrud"] .sh { filter: drop-shadow(0 18px 26px rgba(0,0,0,.55)) drop-shadow(0 2px 3px rgba(0,0,0,.4)); }
    [data-d="b2-zumurrud"] .leaf { position: absolute; inset: 0; clip-path: path("${outer}");
        background: url(${H.img("gold-lattice-margin.webp")}) 30% 50%/auto 1400px; filter: brightness(1.1) saturate(.95) contrast(1.12) hue-rotate(2deg); }
    [data-d="b2-zumurrud"] .ivory { position: absolute; inset: 0; clip-path: path("${inner}");
        background: radial-gradient(ellipse 75% 60% at 50% 42%, #fbf6ea 0%, #f4ecda 60%, #ebdfc6 100%); }
    [data-d="b2-zumurrud"] .ivory::before { content: ""; position: absolute; inset: 0; opacity: .32; mix-blend-mode: multiply;
        background: url(${H.img("textured-ivory-paper.webp")}) center/700px auto; filter: contrast(.8); }
    [data-d="b2-zumurrud"] .tb { left: 230px; right: 230px; top: 318px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="b2-zumurrud"] .bism { font-size: calc(30px * var(--kt)); color: #7d5f24; }
    [data-d="b2-zumurrud"] .hosts { white-space: nowrap; font: 500 calc(21px * var(--kt)) 'Bodoni Moda', serif; letter-spacing: .2em; text-transform: uppercase; margin-top: 38px; color: #12382c; }
    [data-d="b2-zumurrud"] .inv { font: italic 400 calc(24px * var(--kt))/1.45 'Bodoni Moda', serif; margin-top: 12px; color: #2b4a3f; }
    [data-d="b2-zumurrud"] .nm { font: 400 calc(134px * var(--kn))/1.0 Corinthia, cursive; white-space: nowrap; color: #0f3b2e; }
    [data-d="b2-zumurrud"] .nm.foil { --foil: linear-gradient(100deg,#6a4a14 0%,#a9822f 22%,#cfac5a 36%,#7f5d1f 54%,#b8913f 72%,#5e420f 90%,#9a7530 100%); }
    [data-d="b2-zumurrud"] .nm.g { margin-top: 40px; }
    [data-d="b2-zumurrud"] .with { font: italic 400 calc(26px * var(--kt))/1 'Bodoni Moda', serif; color: #8a6a2f; margin: 6px 0 14px; }
    [data-d="b2-zumurrud"] .bp { font: italic 400 calc(20px * var(--kt)) 'Bodoni Moda', serif; color: #2b4a3f; margin-top: 4px; }
    [data-d="b2-zumurrud"] .rule { width: 150px; height: 18px; margin-top: 46px; }
    [data-d="b2-zumurrud"] .ev { font: 500 calc(21px * var(--kt)) Cinzel, serif; letter-spacing: .6em; padding-left: .6em; margin-top: 18px; color: #7d5f24; }
    [data-d="b2-zumurrud"] .dt { font: 400 calc(23px * var(--kt)) 'Bodoni Moda', serif; letter-spacing: .1em; text-transform: uppercase; margin-top: 18px; color: #12382c; }
    [data-d="b2-zumurrud"] .vn { font: 400 calc(23px * var(--kt))/1.5 'Bodoni Moda', serif; margin-top: 12px; color: #2b4a3f; }
    [data-d="b2-zumurrud"] .vn em { font-style: italic; }
    [data-d="b2-zumurrud"] .ur { font-size: calc(20px * var(--kt)); color: #4b6458; margin-top: 20px; }
    [data-d="b2-zumurrud"] .rs { font: italic 400 calc(19px * var(--kt)) 'Bodoni Moda', serif; color: #4b6458; margin-top: 4px; }
  `;
  },
  render: (H, D) => `
    <div class="layer vel"></div>
    <div class="layer lift"></div>
    <div class="layer vig"></div>
    <div class="layer sh"><div class="leaf"></div><div class="ivory"></div></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <path d="${H.archD(182, 636, 560, 1268, .56, 7)}" fill="none" stroke="url(#gold)" stroke-width="1.1" opacity=".9"/>
      <g fill="url(#goldBright)" stroke="url(#goldBright)">
        <line x1="500" y1="118" x2="500" y2="160" stroke-width="1"/>
        <circle cx="500" cy="112" r="3.2" stroke="none"/>
        <path d="M500,128 l7,12 l-7,12 l-7,-12z" stroke="none"/>
      </g>
    </svg></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts" data-fit="500"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-deep" data-fit="560"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-deep" data-fit="560"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <svg class="rule" viewBox="0 0 150 18"><g fill="none" stroke="#a5843f" stroke-width="1"><path d="M0,9 H60"/><path d="M90,9 H150"/></g><path d="M75,2 l7,7 l-7,7 l-7,-7z" fill="none" stroke="#a5843f"/><circle cx="75" cy="9" r="2" fill="#a5843f"/></svg>
      ${H.f("event", "div", 'class="ev"')}
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;&middot;&nbsp; ${H.f("venue")}<br><em>${H.f("place")}</em></div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`,
});
