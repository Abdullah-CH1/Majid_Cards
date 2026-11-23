/* B3 - Zardozi: oxblood velvet, a beaded gold-thread frame like a sherwani border, and one geometric zardozi star medallion.
   Round 2: no flowers - the embroidered floral rosette is replaced by an eight-point star medallion worked in "gold thread"
   (couched lines, bead rows and sequins). The goldwork is real metallic gold glitter seen through the geometry, so it reads
   as embroidery rather than flat vector. Bold frame, big ivory type. */
registerDesign({
  id: "b3-zardozi",
  name: "Zardozi",
  idea: "Oxblood velvet edged with a beaded gold-thread border and finished with a single eight-point star medallion in glinting zardozi goldwork - like the embroidery on the groom's sherwani - with big, clear ivory lettering.",
  css: H => {
    const P = '[data-d="b3-zardozi"]';
    const f = n => (+n).toFixed(2);
    const star = (R, k = .765, rot = 0) => { let d = ""; for (let i = 0; i < 16; i++) { const a = (i * 22.5 - 90 + rot) * Math.PI / 180, r = i % 2 ? R * k : R; d += (i ? "L" : "M") + f(r * Math.cos(a)) + "," + f(r * Math.sin(a)); } return d + "Z"; };
    const pts = (n, R, off = 0) => Array.from({ length: n }, (_, i) => { const a = (i * 360 / n - 90 + off) * Math.PI / 180; return [f(R * Math.cos(a)), f(R * Math.sin(a)), i * 360 / n + off]; });
    const MY = 1192, S = .9;
    // frame lines stop at the corner stars (stars sit centred on the bead row at 56,56)
    const C0 = 56, C1x = 944, C1y = 1344;
    const frame = (t, g, a) => { const tr = 1000 - t, br = 1400 - t;
      return `<path ${a} d="M${C0 + g},${t} H${C1x - g} M${C0 + g},${br} H${C1x - g} M${t},${C0 + g} V${C1y - g} M${tr},${C0 + g} V${C1y - g}"/>`; };
    // everything drawn in black: it is used as an alpha mask over the gold texture
    const corner = (x, y) => `<g transform="translate(${x},${y})"><path d="${star(28)}" stroke-width="3.2"/><path d="${star(13)}" fill="#000" stroke="none"/></g>`;
    const medal = `<g transform="translate(500,${MY}) scale(${S})">
        <circle r="124" stroke-width="7" stroke-dasharray="0 13.6" stroke-linecap="round"/>
        <circle r="111" stroke-width="3.5"/><circle r="104" stroke-width="1.6"/>
        <path d="${star(97, .765, 22.5)}" stroke-width="2.2"/>
        <path d="${star(97)}" stroke-width="4.5"/>
        ${pts(8, 111, 0).map(([x, y]) => `<circle cx="${x}" cy="${y}" r="6.5" fill="#000" stroke="none"/>`).join("")}
        ${pts(8, 80, 22.5).map(([x, y, a]) => `<path transform="translate(${x},${y}) rotate(${a})" d="M0,-9 L5,0 L0,9 L-5,0Z" fill="#000" stroke="none"/>`).join("")}
        <circle r="60" stroke-width="3"/>
        <circle r="50" stroke-width="5.5" stroke-dasharray="0 10.47" stroke-linecap="round"/>
        <path d="${star(37)}" fill="#000" stroke="none"/>
      </g>`;
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1400"><g fill="none" stroke="#000">
        ${frame(40, 23, 'stroke-width="5.5"')}
        ${frame(56, 39, 'stroke-width="6.5" stroke-dasharray="0 13" stroke-linecap="round"')}
        ${frame(72, 23, 'stroke-width="2.2"')}
        ${corner(56, 56)}${corner(944, 56)}${corner(56, 1344)}${corner(944, 1344)}
        ${medal}</g></svg>`;
    const mask = `url("data:image/svg+xml,${encodeURIComponent(svg.replace(/\s+/g, " "))}")`;
    return `
    ${P} { background: #3a0610; color: #f7efdc; font-variant-numeric: lining-nums; font-feature-settings: "lnum" 1; }
    ${P} .gr { background:
        radial-gradient(circle 210px at 50% ${MY}px, rgba(104,16,34,.95) 0%, rgba(83,10,23,.6) 55%, rgba(83,10,23,0) 100%),
        radial-gradient(ellipse 80% 60% at 50% 40%, #4f0915 0%, #3a0610 55%, #24030a 100%); }
    ${P} .tx { background: url(${H.img("crimson-satin.webp")}) center/cover; opacity: .10; mix-blend-mode: soft-light; filter: grayscale(1) blur(1px); }
    ${P} .gw { filter: drop-shadow(0 2px 1.5px rgba(10,0,2,.75)); }
    ${P} .gold { position: absolute; inset: 0;
        background: linear-gradient(120deg, rgba(214,174,92,.62) 0%, rgba(246,224,160,.62) 18%, rgba(196,156,76,.62) 36%, rgba(250,232,176,.62) 52%, rgba(190,150,70,.62) 70%, rgba(240,214,146,.62) 86%, rgba(184,142,62,.62) 100%),
            url(${H.img("gold-glitter-bokeh.webp")}) center/700px auto;
        filter: saturate(.78) contrast(1.06);
        -webkit-mask: ${mask} 0 0/100% 100% no-repeat; mask: ${mask} 0 0/100% 100% no-repeat; }
    ${P} .ctr { position: absolute; left: ${500 - 9}px; top: ${MY - 9}px; width: 18px; height: 18px; transform: rotate(45deg); background: #4a0915; }
    ${P} .ctr::after { content: ""; position: absolute; inset: 5px; background: #f1d98f; border-radius: 50%; }
    ${P} .tb { left: 110px; right: 110px; top: 110px; text-align: center; display: flex; flex-direction: column; align-items: center; }
    ${P} .bism { font-size: calc(48px * var(--kt)); line-height: 1.2; color: #f1d98f; }
    ${P} .hosts { white-space: nowrap; font: 400 calc(43px * var(--kt))/1.2 'Marcellus SC', serif; letter-spacing: .07em; margin-top: 18px; color: #f7efdc; }
    ${P} .inv { font: italic 400 calc(36px * var(--kt))/1.3 'Playfair Display', serif; margin-top: 8px; color: #f7efdc; }
    ${P} .nm { font: 400 calc(136px * var(--kn))/1.02 'Rouge Script', cursive; white-space: nowrap; }
    ${P} .nm.g { margin-top: 18px; }
    ${P} .with { font: italic 400 calc(44px * var(--kt))/1 'Playfair Display', serif; color: #f7efdc; margin: 0 0 4px; }
    ${P} .bp { font: italic 400 calc(34px * var(--kt))/1.25 'Playfair Display', serif; color: #f7efdc; margin-top: 2px; }
    ${P} .ev { display: flex; align-items: center; gap: 22px; margin-top: 20px; }
    ${P} .ev .f { font: 600 calc(50px * var(--kt))/1.15 Cinzel, serif; letter-spacing: .14em; margin-right: -.14em; }
    ${P} .ev i { display: block; width: 46px; height: 0; border-top: 5px dotted #e6c877; }
    ${P} .dt { font: 400 calc(42px * var(--kt))/1.25 Marcellus, serif; margin-top: 10px; color: #f7efdc; white-space: nowrap; }
    ${P} .vn { font: 400 calc(38px * var(--kt))/1.32 Marcellus, serif; margin-top: 4px; color: #f7efdc; }
    ${P} .vn .pl { font-size: calc(35px * var(--kt)); }
    ${P} .ur { font-size: calc(38px * var(--kt)); line-height: 1.85; color: #f7efdc; margin-top: 2px; }
    ${P} .rs { font: italic 400 calc(34px * var(--kt))/1.25 'Playfair Display', serif; color: #f7efdc; margin-top: 2px; }
  `;
  },
  render: (H, D) => `
    <div class="layer gr"></div>
    <div class="layer tx"></div>
    <div class="layer"><svg viewBox="0 0 1000 1400"><rect width="1000" height="1400" filter="url(#grain)" opacity=".22"/></svg></div>
    <div class="layer gw"><div class="gold"></div></div>
    <div class="ctr"></div>
    <div class="tb">
      ${H.bism()}
      ${H.f("hosts", "div", 'class="hosts" data-fit="760"')}
      <div class="inv">${H.f("invite1")}<br>${H.f("invite2")}</div>
      ${H.f("groom", "div", 'class="nm g foil foil-light" data-fit="740"')}
      ${H.f("joiner", "div", 'class="with"')}
      ${H.f("bride", "div", 'class="nm foil foil-light" data-fit="740"')}
      ${H.when("brideParents", H.f("brideParents", "div", 'class="bp"'))}
      <div class="ev"><i></i>${H.f("event", "span", 'class="foil foil-light"')}<i></i></div>
      <div class="dt" data-fit="760">${H.dateLine()}</div>
      <div class="vn">${H.f("time")} &nbsp;&middot;&nbsp; ${H.f("venue")}<br><span class="pl">${H.f("place")}</span></div>
      ${H.urdu()}
      ${H.when("rsvp", H.f("rsvp", "div", 'class="rs"'))}
    </div>`,
});
