/* B3 - Zardozi: oxblood velvet, a slim beaded gold frame, and one real gold-thread embroidered medallion. */
registerDesign({
  id: "b3-zardozi",
  name: "Zardozi",
  idea: "Oxblood velvet with a slim beaded gold frame and a single antique zardozi medallion, hand-embroidered in gold thread - like the groom's sherwani itself.",
  css: H => {
    /* crop of the centre rosette of the embroidered canopy (source 2000 x 1961, rosette centre 970,1028) */
    const S = 344, cx = 968, cy = 1029, r = 268, k = S / (2 * r);
    return `
    [data-d="b3-zardozi"] { background: #3a0610; color: #f6ead6; }
    [data-d="b3-zardozi"] .gr { background:
        radial-gradient(circle 260px at 50% 1088px, #530a17 0%, #530a17 45%, rgba(83,10,23,.0) 100%),
        radial-gradient(ellipse 80% 60% at 50% 40%, #4f0915 0%, #3a0610 55%, #24030a 100%); }
    [data-d="b3-zardozi"] .tx { background: url(${H.img("crimson-satin.webp")}) center/cover; opacity: .10; mix-blend-mode: soft-light; filter: grayscale(1) blur(1px); }
    [data-d="b3-zardozi"] .med { position: absolute; left: 50%; top: ${1088 - S / 2}px; width: ${S}px; height: ${S}px; translate: -50% 0;
        background: url(${H.img("maroon-velvet-gold-embroidery.webp")}) ${-(cx - r) * k}px ${-(cy - r) * k}px/${2000 * k}px auto no-repeat;
        filter: brightness(.74) saturate(.9) contrast(1.1);
        -webkit-mask-image: radial-gradient(circle closest-side, #000 90%, transparent 99%);
                mask-image: radial-gradient(circle closest-side, #000 90%, transparent 99%); }
    [data-d="b3-zardozi"] .tb { left: 110px; right: 110px; top: 118px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    [data-d="b3-zardozi"] .bism { font-size: calc(34px * var(--kt)); color: #e8c97c; }
    [data-d="b3-zardozi"] .hosts { white-space: nowrap; font: 400 calc(25px * var(--kt)) 'Marcellus SC', serif; letter-spacing: .18em; margin-top: 36px; color: #fbf1e0; }
    [data-d="b3-zardozi"] .inv { font: italic 400 calc(24px * var(--kt))/1.45 'Playfair Display', serif; margin-top: 12px; color: #ecd9c0; }
    [data-d="b3-zardozi"] .nm { font: 400 calc(112px * var(--kn))/1.08 'Rouge Script', cursive; white-space: nowrap; }
    [data-d="b3-zardozi"] .nm.g { margin-top: 36px; }
    [data-d="b3-zardozi"] .with { font: italic 400 calc(26px * var(--kt))/1 'Playfair Display', serif; color: #e8c97c; margin: 2px 0 6px; }
    [data-d="b3-zardozi"] .bp { font: italic 400 calc(21px * var(--kt)) 'Playfair Display', serif; color: #ecd9c0; margin-top: 2px; }
    [data-d="b3-zardozi"] .ev { font: 400 calc(22px * var(--kt)) Cinzel, serif; letter-spacing: .6em; padding-left: .6em; margin-top: 42px; color: #e8c97c; }
    [data-d="b3-zardozi"] .dt { font: 400 calc(24px * var(--kt)) 'Marcellus', serif; letter-spacing: .12em; text-transform: uppercase; margin-top: 20px; color: #fbf1e0; }
    [data-d="b3-zardozi"] .vn { font: 500 calc(25px * var(--kt))/1.45 'Cormorant Garamond', serif; margin-top: 12px; color: #f0e1ca; }
    [data-d="b3-zardozi"] .ur { font-size: calc(21px * var(--kt)); color: #dcc6a6; margin-top: 16px; }
    [data-d="b3-zardozi"] .rs { font: italic 400 calc(19px * var(--kt)) 'Playfair Display', serif; color: #dcc6a6; margin-top: 4px; }
  `;
  },
  render: (H, D) => {
    const knot = (x, y) => `<g transform="translate(${x},${y})"><rect x="-6" y="-6" width="12" height="12" transform="rotate(45)" fill="none" stroke="url(#goldBright)" stroke-width="1"/><circle r="2.2" fill="url(#goldBright)"/></g>`;
    return `
    <div class="layer gr"></div>
    <div class="layer tx"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400"><rect width="1000" height="1400" filter="url(#grain)" opacity=".22"/></svg></div>
    <div class="layer"><svg viewBox="0 0 1000 1400">
      <g fill="none" stroke="url(#gold)">
        <rect x="48" y="48" width="904" height="1304" stroke-width="1.5"/>
        <rect x="60" y="60" width="880" height="1280" stroke-width="2.4" stroke-dasharray="0 8" stroke-linecap="round"/>
        <rect x="72" y="72" width="856" height="1256" stroke-width=".8"/>
      </g>
      ${knot(60, 60)}${knot(940, 60)}${knot(60, 1340)}${knot(940, 1340)}
      <circle cx="500" cy="1088" r="184" fill="none" stroke="url(#gold)" stroke-width=".8" opacity=".7"/>
      <circle cx="500" cy="1088" r="193" fill="none" stroke="url(#gold)" stroke-width="2" stroke-dasharray="0 7" stroke-linecap="round" opacity=".75"/>
    </svg></div>
    <div class="med"></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts" data-fit="720"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-light" data-fit="720"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-light" data-fit="720"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      ${H.f("event", "div", 'class="ev"')}
      <div class="dt">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;&middot;&nbsp; ${H.f("venue")}, ${H.f("place")}</div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`;
  },
});
