(() => {
  const C = window.INVITE || {};
  const $ = s => document.querySelector(s);
  const body = document.body;

  // ---------- fill in the wording ----------
  document.querySelectorAll("[data-k]").forEach(el => { el.textContent = C[el.dataset.k] ?? ""; });
  $("#locText").innerHTML = (C.locationText || []).map(p => `<p>${p.replace(/[<>&]/g, c => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;" }[c]))}</p>`).join("");
  const dir = $("#dirBtn");
  dir.textContent = C.directionsLabel || "Get directions";
  dir.href = "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(C.mapsQuery || C.venue || "");
  $("#photo").src = C.photo || "assets/photo.jpg";

  // ---------- card: glossy "mirror" centre panel (same arch as the embossed frame in assets/card.jpg) ----------
  (function cardSheen() {
    const host = $(".card-sheen"); if (!host) return;
    const cx = 450, ytop = 238, ybot = 1666;                                      // keep in step with ARCH / ARCH_SEGS in tools/make_assets.py
    const segs = [[[0, 0], [-4, 22], [-18, 44], [-46, 54]], [[-46, 54], [-80, 66], [-125, 60], [-152, 79]], [[-152, 79], [-166, 88], [-172, 100], [-172, 115]],
      [[-172, 115], [-200, 114], [-222, 138], [-224, 176]], [[-224, 176], [-262, 176], [-290, 215], [-294, 303]], [[-294, 303], [-318, 306], [-338, 335], [-338, 378]]];
    const P = (x, y, sx, top) => [cx + sx * x, top ? ytop + y : ybot - y];
    const f = p => p[0].toFixed(1) + " " + p[1].toFixed(1);
    let d = "M " + f(P(-338, 378, 1, true));
    for (let i = segs.length - 1; i >= 0; i--) { const [a, b, c, e] = segs[i]; d += ` C ${f(P(...c, 1, true))} ${f(P(...b, 1, true))} ${f(P(...a, 1, true))}`; }
    for (const [a, b, c, e] of segs) d += ` C ${f(P(...b, -1, true))} ${f(P(...c, -1, true))} ${f(P(...e, -1, true))}`;
    d += " L " + f(P(-338, 378, -1, false));
    for (let i = segs.length - 1; i >= 0; i--) { const [a, b, c, e] = segs[i]; d += ` C ${f(P(...c, -1, false))} ${f(P(...b, -1, false))} ${f(P(...a, -1, false))}`; }
    for (const [a, b, c, e] of segs) d += ` C ${f(P(...b, 1, false))} ${f(P(...c, 1, false))} ${f(P(...e, 1, false))}`;
    d += " Z";
    host.innerHTML = `<svg viewBox="0 0 900 1950" preserveAspectRatio="none" aria-hidden="true">
      <defs>
        <mask id="panelMask"><path d="${d}" fill="#fff" stroke="#000" stroke-width="50"/></mask>
        <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0.3">
          <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".22" stop-color="#fff" stop-opacity="0"/>
          <stop offset=".36" stop-color="#fdf6ff" stop-opacity=".045"/><stop offset=".5" stop-color="#fdf6ff" stop-opacity=".10"/>
          <stop offset=".64" stop-color="#fdf6ff" stop-opacity=".045"/><stop offset=".78" stop-color="#fff" stop-opacity="0"/>
          <stop offset="1" stop-color="#fff" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="glow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffaff" stop-opacity=".05"/><stop offset=".45" stop-color="#fffaff" stop-opacity=".10"/><stop offset="1" stop-color="#fffaff" stop-opacity=".16"/></linearGradient>
      </defs>
      <g mask="url(#panelMask)"><rect width="900" height="1950" fill="url(#glow)"/><rect class="sheen-band" x="-450" width="1800" height="1950" fill="url(#sweep)"/></g></svg>`;
  })();

  // ---------- countdown ticket shape (ivory label with scrolled ends and a small crest, as in the reference) ----------
  (function ticketShape() {
    const body = "M40 30 L232 30 C252 30 258 22 268 16 C279 10 290 8 300 8 C310 8 321 10 332 16 C342 22 348 30 368 30 L560 30 " +
      "C571 30 581 27 585 36 C589 46 569 52 567 64 C565 76 581 84 589 90 C581 96 565 104 567 116 C569 128 589 134 585 144 C581 153 571 150 560 150 " +
      "L368 150 C348 150 342 158 332 163 C321 169 310 171 300 171 C290 171 279 169 268 163 C258 158 252 150 232 150 L40 150 " +
      "C29 150 19 153 15 144 C11 134 31 128 33 116 C35 104 19 96 11 90 C19 84 35 76 33 64 C31 52 11 46 15 36 C19 27 29 30 40 30 Z";
    const curls = "M268 16 C262 10 252 12 254 19 C256 24 263 23 262 18 M332 16 C338 10 348 12 346 19 C344 24 337 23 338 18 " +
      "M268 163 C262 169 252 167 254 160 C256 155 263 156 262 161 M332 163 C338 169 348 167 346 160 C344 155 337 156 338 161 " +
      "M15 36 C9 30 2 36 7 41 C11 45 16 41 13 38 M585 36 C591 30 598 36 593 41 C589 45 584 41 587 38 " +
      "M15 144 C9 150 2 144 7 139 C11 135 16 139 13 142 M585 144 C591 150 598 144 593 139 C589 135 584 139 587 142 " +
      "M11 90 C5 86 3 94 8 95 M589 90 C595 86 597 94 592 95 M292 14 C296 10 304 10 308 14 M292 166 C296 170 304 170 308 166";
    // stretch the body taller (the reference label is a deep panel with only a small crest)
    const ty = y => y < 30 ? 17 - (30 - y) * 0.6 : y > 150 ? 183 + (y - 150) * 0.6 : 17 + (y - 30) * 1.383;
    const tall = p => p.replace(/(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)/g, (m, x, y) => `${x} ${ty(+y).toFixed(1)}`);
    const B = tall(body), K = tall(curls);
    const crest = "M276 19 C268 7 252 9 250 16 C248 23 257 25 259 19 M324 19 C332 7 348 9 350 16 C352 23 343 25 341 19 " +
      "M286 14 C290 5 310 5 314 14 M296 9 C298 4 302 4 304 9 M244 23 C236 23 230 20 226 16 M356 23 C364 23 370 20 374 16";
    const crestB = crest.replace(/(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)/g, (m, x, y) => `${x} ${200 - +y}`);
    const svg = `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 200' preserveAspectRatio='none'>` +
      `<defs><linearGradient id='p' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#f8f6f8'/><stop offset='.55' stop-color='#f0edf0'/><stop offset='1' stop-color='#e2dde3'/></linearGradient>` +
      `<linearGradient id='m' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#8d8591'/><stop offset='.5' stop-color='#4f4854'/><stop offset='1' stop-color='#7a727e'/></linearGradient></defs>` +
      `<path d='${B}' fill='url(#p)' stroke='url(#m)' stroke-width='10' stroke-linejoin='round'/>` +
      `<path d='${B}' fill='none' stroke='#d9d3dc' stroke-width='1.4' transform='translate(300 100) scale(.985 .955) translate(-300 -100)'/>` +
      `<path d='${B}' fill='none' stroke='#8a828e' stroke-width='1.2' transform='translate(300 100) scale(.955 .87) translate(-300 -100)'/>` +
      `<g fill='none' stroke='#4f4854' stroke-width='4.2' stroke-linecap='round'><path d='${K}'/><path d='${tall(crest)}'/><path d='${tall(crestB)}'/></g>` +
      `<g fill='none' stroke='#cfc8d2' stroke-width='1' stroke-linecap='round' transform='translate(-.8 -1)'><path d='${K}'/><path d='${tall(crest)}'/><path d='${tall(crestB)}'/></g></svg>`;
    $(".ticket").style.backgroundImage = `url("data:image/svg+xml,${encodeURIComponent(svg)}")`;
  })();

  // ---------- music ----------
  const audio = $("#music"), mBtn = $("#musicBtn");
  if (C.music) {
    audio.src = C.music;
    audio.addEventListener("canplay", () => { mBtn.hidden = false; }, { once: true });
    audio.addEventListener("error", () => { mBtn.hidden = true; });
  }
  const setMuted = m => { mBtn.classList.toggle("muted", m); };
  setMuted(true);
  mBtn.addEventListener("click", () => {
    if (audio.paused) { audio.play().then(() => setMuted(false)).catch(() => {}); }
    else { audio.pause(); setMuted(true); }
  });

  // ---------- opening sequence ----------
  const op = $("#opening");
  const BOW_FRAMES = 34;
  const bowImg = $("#bowImg");
  const bowSrc = i => `assets/bow/bow-${String(i).padStart(2, "0")}.webp?v=20261126c`;
  const bowCache = [];
  for (let i = 0; i < BOW_FRAMES; i++) { const im = new Image(); im.src = bowSrc(i); bowCache.push(im); }   // preload while the envelope is shown
  const halfL = $(".wrap.half.left"), wrapBox = $("#wrapBox"), envStage = $("#envStage");
  const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;    // easeInOutCubic
  const clamp01 = t => Math.max(0, Math.min(1, t));
  const wait = ms => new Promise(r => setTimeout(r, ms));
  function animate(ms, step) {                 // runs step(0..1) every frame for ms milliseconds
    return new Promise(res => {
      const t0 = performance.now();
      const f = () => { const t = clamp01((performance.now() - t0) / ms); step(t); t < 1 ? requestAnimationFrame(f) : res(); };
      requestAnimationFrame(f);
    });
  }
  const bandL = $(".band-half.left"), bandR = $(".band-half.right");
  // the four rolled fabric edges of the diamond: upper-left, lower-left, upper-right, lower-right
  const foldClips = ["left", "right"].map(side => { const c = document.createElement("div"); c.className = "fold-clip " + side; wrapBox.insertBefore(c, bandL); return c; });
  const foldEdges = [0, 1, 2, 3].map(i => { const d = document.createElement("div"); d.className = "fold-edge"; foldClips[i >> 1].appendChild(d); return d; });
  function keyCurve(xs, ys) {                  // smooth curve through measured keys (cubic Hermite, finite-difference tangents)
    const n = xs.length, m = xs.map((_, i) => i === 0 ? (ys[1] - ys[0]) / (xs[1] - xs[0]) : i === n - 1 ? (ys[i] - ys[i - 1]) / (xs[i] - xs[i - 1]) : (ys[i + 1] - ys[i - 1]) / (xs[i + 1] - xs[i - 1]));
    return x => {
      if (x <= xs[0]) return ys[0];
      if (x >= xs[n - 1]) return ys[n - 1];
      let i = 0; while (x > xs[i + 1]) i++;
      const h = xs[i + 1] - xs[i], t = (x - xs[i]) / h, t2 = t * t, t3 = t2 * t;
      return (2 * t3 - 3 * t2 + 1) * ys[i] + (t3 - 2 * t2 + t) * h * m[i] + (-2 * t3 + 3 * t2) * ys[i + 1] + (t3 - t2) * h * m[i + 1];
    };
  }
  // the diamond measured from the video (frames after the knot lets go, 30 fps): half-width B and half-height A, % of the screen.
  // A slit opens first (tall and thin), both grow steadily, then the fabric slips off past the sides and corners.
  const DIA_FRAMES = 43.5;
  const DIA_KEYS = [0, 2, 7, 14, 22, 27, 32, 37, 41.5, 43.5];
  const diaB = keyCurve(DIA_KEYS, [0, 1.5, 11, 27, 46, 58, 69, 81, 97, 108]);
  const diaA = keyCurve(DIA_KEYS, [0, 8, 17.5, 27, 41, 56, 74, 96, 122, 138]);
  function setDiamond(p) {                     // the knot lets go: the fabric opens from the centre as a diamond,
    const t = p * DIA_FRAMES;                  // pinched left and right where the ribbon gathers pull it aside
    const B = Math.max(0, diaB(t)), A = Math.max(0, diaA(t));
    const a2 = A / 1.28, b2 = B / 1.28;         // the sheet is 1.28x the card (inset -14%), the diamond is measured on the card
    halfL.style.clipPath = t <= 0 ? "none" : `polygon(evenodd, 0 0, 100% 0, 100% 100%, 0 100%, 0 0, 50% ${50 - a2}%, ${50 + b2}% 50%, 50% ${50 + a2}%, ${50 - b2}% 50%, 50% ${50 - a2}%)`;
    // rolled edges: each strip runs from its pinch point to the diamond's tip, the bunched fabric on the outside
    const bw = wrapBox.clientWidth, bh = wrapBox.clientHeight;
    const px = B / 100 * bw, py = A / 100 * bh, len = Math.hypot(px, py), ang = Math.atan2(py, px);
    const thick = Math.min(1, 0.06 + len / (0.6 * bw));
    const eo = (clamp01(t / 2.5) * (1 - clamp01((t - 38) / 5))).toFixed(3);
    const place = (el, sx, th, flip) => {
      el.style.transform = `translate(${(bw / 2 + sx * px).toFixed(1)}px, ${(bh / 2).toFixed(1)}px) rotate(${th.toFixed(4)}rad) scale(${(len / 100).toFixed(4)}, ${(flip * thick).toFixed(3)}) translateY(-16%)`;
      el.style.opacity = eo;
    };
    place(foldEdges[0], -1, -ang, -1); place(foldEdges[1], -1, ang, 1);
    place(foldEdges[2], 1, ang - Math.PI, 1); place(foldEdges[3], 1, Math.PI - ang, -1);
    // each band half stays gathered at its pinch point and is drawn off to its side
    const k = Math.max(0.02, (50 - Math.max(B, 2.22)) / 47.78), ky = 0.3 + 0.7 * Math.pow(k, 0.6);
    bandL.style.transform = bandR.style.transform = `scale(${k.toFixed(4)}, ${ky.toFixed(4)})`;
    bandL.style.opacity = bandR.style.opacity = clamp01(k * 5).toFixed(3);
    halfL.style.opacity = (1 - clamp01((t - 40) / 3.5)).toFixed(3);
  }
  // ---- the envelope opening, timed frame by frame against the reference video (30 fps) ----
  const flap = $("#flap"), flapDim = $("#flapDim"), flapShadow = $("#flapShadow"), seal = $("#seal"), pocket = $(".env-shadow");
  function smoothCurve(pts) {                 // monotone cubic through [x, y] keys (no overshoot)
    const n = pts.length, xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
    const d = [], m = new Array(n).fill(0);
    for (let i = 0; i < n - 1; i++) d.push((ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]));
    m[0] = d[0]; m[n - 1] = d[n - 2];
    for (let i = 1; i < n - 1; i++) m[i] = d[i - 1] * d[i] <= 0 ? 0 : 3 * (xs[i + 1] - xs[i - 1]) / ((2 * xs[i + 1] - xs[i] - xs[i - 1]) / d[i - 1] + (xs[i + 1] + xs[i] - 2 * xs[i - 1]) / d[i]);
    return x => {
      if (x <= xs[0]) return ys[0];
      if (x >= xs[n - 1]) return ys[n - 1];
      let i = 0; while (x > xs[i + 1]) i++;
      const h = xs[i + 1] - xs[i], t = (x - xs[i]) / h, t2 = t * t, t3 = t2 * t;
      return (2 * t3 - 3 * t2 + 1) * ys[i] + (t3 - 2 * t2 + t) * h * m[i] + (-2 * t3 + 3 * t2) * ys[i + 1] + (t3 - t2) * h * m[i + 1];
    };
  }
  const lerpTab = (tab, x) => {
    if (x <= tab[0][0]) return tab[0][1];
    for (let i = 1; i < tab.length; i++) if (x <= tab[i][0]) { const [x0, y0] = tab[i - 1], [x1, y1] = tab[i]; return y0 + (y1 - y0) * (x - x0) / (x1 - x0); }
    return tab[tab.length - 1][1];
  };
  // height of the flap tip on screen (1 = closed, 0 = edge-on at the top), measured from the video:
  // a quick first lift that eases into a short hover about half way up, then it folds on over the top
  const tipHeight = smoothCurve([[0, 1], [.13, .94], [.23, .865], [.33, .785], [.43, .73], [.53, .69], [.63, .65], [.73, .605],
    [.83, .57], [.93, .548], [1.03, .528], [1.13, .5], [1.23, .43], [1.33, .355], [1.43, .29], [1.53, .225], [1.63, .15],
    [1.73, .09], [1.83, .04], [1.93, 0], [2.05, -.09]]);
  const SEAL_SQUASH = [[0, 1], [40, .95], [62, .77], [70, .56], [76, .4], [84, .27], [90, .16], [100, .06]];   // the seal reads thicker than the flat flap
  const SEAL_LIGHT = [[0, 1], [30, 1.3], [55, 1.5], [70, 1.3], [82, 1.0], [95, .85]];                        // catches the light as it tilts up
  const FLAP_DIM = [[0, 0], [45, 0], [65, .12], [80, .34], [95, .6]];                                         // flap turns away from the light
  const POCKET = [[0, 0], [.2, 1]];                                                                                                 // shadow inside the envelope
  function flapAngle(r, L, P) {               // solve  cos(a) * P / (P - L sin a) = r   (perspective rotation about the top edge)
    let lo = 0, hi = 1.95;
    for (let k = 0; k < 28; k++) {
      const a = (lo + hi) / 2, v = Math.cos(a) * P / (P - L * Math.sin(a));
      if (v > r) lo = a; else hi = a;
    }
    return (lo + hi) / 2;
  }
  let pocketOut = 1;                          // the flap's shadow clears from the card as the envelope slips away
  function liftFlap() {
    const Hs = envStage.clientHeight, P = 3.55 * Hs;               // = the CSS perspective (3.55 x the artwork height)
    const Lf = 0.535 * Hs, Ls = 0.513 * Hs;                         // flap tip / seal centre below the top edge
    const DUR = 2.05;
    return animate(DUR * 1000, t => {
      const T = t * DUR;
      const a = flapAngle(tipHeight(T), Lf, P), deg = a * 180 / Math.PI;
      flap.style.transform = `rotateX(${deg.toFixed(3)}deg)`;
      flapDim.style.opacity = lerpTab(FLAP_DIM, deg).toFixed(3);
      flapShadow.style.opacity = (1 - clamp01(deg / 65)).toFixed(3);
      const Z = Ls * Math.sin(a), m = P / (P - Z), dy = Ls * Math.cos(a) * m - Ls;
      const sq = lerpTab(SEAL_SQUASH, deg);
      seal.style.transform = `translate(-50%, -50%) translateY(${dy.toFixed(2)}px) scale(${m.toFixed(4)}, ${(m * sq).toFixed(4)})`;
      seal.style.filter = `brightness(${lerpTab(SEAL_LIGHT, deg).toFixed(3)}) drop-shadow(0 1px 1.5px rgba(30,16,26,.5)) drop-shadow(3px ${(7 + deg / 14).toFixed(1)}px 8px rgba(34,18,30,.62)) drop-shadow(6px ${(14 + deg / 7).toFixed(1)}px ${(18 + deg / 9).toFixed(1)}px rgba(34,18,30,.44))`;
      seal.style.opacity = String(1 - clamp01((deg - 92) / 6));
      flap.style.opacity = deg > 94 ? "0" : "1";              // past vertical it would only show as a sliver
      pocket.style.opacity = (lerpTab(POCKET, T) * pocketOut).toFixed(3);
    });
  }
  document.documentElement.classList.add("locked");
  (function firstPaint() {
    const urls = ["assets/envelope-body.webp?v=20261126c", "assets/envelope-flap.webp?v=20261126c", "assets/seal.webp?v=20261126c"];
    const done = () => body.classList.add("ready");
    Promise.all(urls.map(u => new Promise(r => { const im = new Image(); im.onload = im.onerror = r; im.src = u; }))).then(done);
    setTimeout(done, 3000);
  })();
  op.addEventListener("touchmove", e => e.preventDefault(), { passive: false });   // no rubber-band scrolling under the envelope (iOS)
  let started = false;
  async function openInvitation() {
    if (started) return; started = true;
    if (audio.src) audio.play().then(() => setMuted(false)).catch(() => {});
    op.classList.add("open"); body.classList.add("opened");
    await wait(220);                           // (in the video the flap starts a beat after the tap)
    const lift = liftFlap().then(() => { flap.style.visibility = seal.style.visibility = "hidden"; });
    await wait(930);                           // while the flap is still folding back, the lower envelope starts to slip down:
    // slowly at first, then faster, until it is off the screen (measured from the video, frames 91-140; seconds -> screen heights)
    const envBody = $(".env-body"), SLIDE_S = 1.72;
    const slide = smoothCurve([[0, 0], [.13, .03], [.27, .065], [.4, .10], [.53, .135], [.67, .175], [.8, .22], [.93, .275],
      [1.07, .34], [1.2, .43], [1.33, .54], [1.47, .67], [1.6, .82], [1.72, 1]]);
    await animate(SLIDE_S * 1000, t => {
      envBody.style.transform = flapShadow.style.transform = `translateY(${(slide(t * SLIDE_S) * 104).toFixed(2)}%)`;
      pocketOut = lerpTab([[0, 1], [.55, 1], [.95, .5], [1.3, 0]], t * SLIDE_S);
      pocket.style.opacity = Math.min(+pocket.style.opacity, pocketOut).toFixed(3);
    });
    await lift;
    op.classList.add("drop");
    $("#envBox").style.visibility = "hidden";
    await wait(260);                           // the wrapped card rests a moment (video: frames 140-150)
    await animate(1600, t => {                 // the bow is pulled undone (frames follow the video): loops slip into the knot,
      const src = bowSrc(Math.round(t * (BOW_FRAMES - 1)));   // the band is drawn tight, the last tail slides out, the knot lets go
      if (!bowImg.src.endsWith(src)) bowImg.src = src;
    });
    bandL.style.opacity = bandR.style.opacity = "1";   // the last frame is exactly the two gathered band halves: swap to them
    bowImg.style.opacity = "0";
    setTimeout(() => body.classList.add("revealed"), 1650);   // wording fades in once the card is clear
    await animate(1450, setDiamond);
    body.classList.remove("locked"); document.documentElement.classList.remove("locked");
    window.scrollTo(0, 0);
    op.classList.add("gone");
  }
  $("#seal").addEventListener("click", openInvitation);
  $("#envBox").addEventListener("click", openInvitation);

  // ---------- countdown ----------
  const target = new Date(C.countdownTo || "2026-12-31T14:00:00+05:00").getTime();
  const cd = { d: $("#cd-d"), h: $("#cd-h"), m: $("#cd-m"), s: $("#cd-s") };
  function tick() {
    let t = Math.max(0, Math.floor((target - Date.now()) / 1000));
    const d = Math.floor(t / 86400); t -= d * 86400;
    const h = Math.floor(t / 3600); t -= h * 3600;
    const m = Math.floor(t / 60); const s = t - m * 60;
    cd.d.textContent = d; cd.h.textContent = h; cd.m.textContent = String(m).padStart(2, "0"); cd.s.textContent = String(s).padStart(2, "0");
  }
  tick(); setInterval(tick, 1000);

  // ---------- pearl frame: a square string of glass-clear seed pearls on the shell; a large pearl at each corner, and along
  //            each side three larger pieces (cut crystals and six-petal flowers) with four seed pearls between them ----------
  const pf = $("#pearlFrame");
  function drawPearls() {
    const r = pf.getBoundingClientRect(); const W = r.width, H = r.height;
    if (!W) return;
    const x0 = W * 0.101, x1 = W * 0.899, y0 = H * 0.105, y1 = H * 0.907;
    const rs = W * 0.0076, rb = W * 0.0185, rg = W * 0.0175, rf = W * 0.017;
    const n = v => v.toFixed(2);
    let s = `<defs>
      <radialGradient id="pgBody" cx="36%" cy="28%" r="82%"><stop offset="0" stop-color="#fff" stop-opacity=".42"/><stop offset=".42" stop-color="#ece6ee" stop-opacity=".2"/><stop offset=".8" stop-color="#9a8a9c" stop-opacity=".14"/><stop offset="1" stop-color="#3f2e42" stop-opacity=".42"/></radialGradient>
      <radialGradient id="pgSpec"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".5" stop-color="#fff" stop-opacity=".4"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
      <linearGradient id="pgRim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset=".45" stop-color="#7d6c7e" stop-opacity=".25"/><stop offset="1" stop-color="#33243a" stop-opacity=".62"/></linearGradient>
      <linearGradient id="pgPetal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".62"/><stop offset="1" stop-color="#e3dbe6" stop-opacity=".32"/></linearGradient>
      <filter id="ps" x="-50%" y="-50%" width="200%" height="200%"><feDropShadow dx="${n(W * .0022)}" dy="${n(W * .004)}" stdDeviation="${n(W * .003)}" flood-color="#281b2c" flood-opacity=".55"/></filter></defs><g filter="url(#ps)">`;
    const bead = (x, y, R, big) => {
      let g = `<circle cx="${n(x)}" cy="${n(y)}" r="${n(R)}" fill="url(#pgBody)" stroke="url(#pgRim)" stroke-width="${n(Math.max(.6, R * .15))}"/>`
        + `<ellipse cx="${n(x - R * .2)}" cy="${n(y - R * .34)}" rx="${n(R * .42)}" ry="${n(R * .3)}" fill="url(#pgSpec)"/>`;
      if (big) {                                       // light pooling low inside the dome, as in a drop of glass
        const a0 = .25, a1 = 1.9, q = R * .62;
        g += `<path d="M${n(x + Math.cos(a0) * q)} ${n(y + Math.sin(a0) * q)}A${n(q)} ${n(q)} 0 0 1 ${n(x + Math.cos(a1) * q)} ${n(y + Math.sin(a1) * q)}" fill="none" stroke="#fff" stroke-opacity=".45" stroke-width="${n(R * .18)}" stroke-linecap="round"/>`;
      }
      return g;
    };
    const gem = (x, y, R) => {                         // round cut crystal: dark girdle, bright table, a few facet lines
      let g = bead(x, y, R, false) + `<circle cx="${n(x)}" cy="${n(y)}" r="${n(R * .9)}" fill="none" stroke="#3a2a40" stroke-opacity=".5" stroke-width="${n(R * .13)}"/>`;
      for (let k = 0; k < 4; k++) {
        const a = k * Math.PI / 4 + .3, c = Math.cos(a) * R * .74, d = Math.sin(a) * R * .74;
        g += `<path d="M${n(x - c)} ${n(y - d)}L${n(x + c)} ${n(y + d)}" stroke="#fff" stroke-opacity=".38" stroke-width="${n(R * .12)}"/>`;
      }
      return g + `<circle cx="${n(x)}" cy="${n(y)}" r="${n(R * .34)}" fill="#fff" fill-opacity=".5"/>`;
    };
    const flower = (x, y, R) => {                      // six narrow white petals round a tiny pearl
      let g = "";
      for (let k = 0; k < 6; k++) {
        const a = k * 60 + 30, px = x + Math.cos(a * Math.PI / 180) * R * .56, py = y + Math.sin(a * Math.PI / 180) * R * .56;
        g += `<ellipse cx="${n(px)}" cy="${n(py)}" rx="${n(R * .46)}" ry="${n(R * .22)}" transform="rotate(${a} ${n(px)} ${n(py)})" fill="url(#pgPetal)" stroke="#4a3a50" stroke-opacity=".4" stroke-width=".5"/>`;
      }
      return g + bead(x, y, R * .26, false);
    };
    const between = [.26, .42, .58, .74];              // the four seed pearls of each quarter
    const side = (ax, ay, bx, by, mids) => {
      for (let q = 0; q < 4; q++) {
        const fx = t => ax + (bx - ax) * (q + t) / 4, fy = t => ay + (by - ay) * (q + t) / 4;
        if (q === 0) s += bead(ax, ay, rb, true);
        else s += mids[q - 1] === "f" ? flower(fx(0), fy(0), rf) : gem(fx(0), fy(0), rg);
        between.forEach(t => { s += bead(fx(t), fy(t), rs, false); });
      }
    };
    side(x0, y0, x1, y0, "fgf"); side(x1, y0, x1, y1, "gfg"); side(x1, y1, x0, y1, "fgf"); side(x0, y1, x0, y0, "gfg");
    s += "</g>";
    pf.setAttribute("viewBox", `0 0 ${W} ${H}`);
    pf.innerHTML = s;
  }

  // ---------- scratch to reveal ----------
  const cv = $("#scratch"), ctx = cv.getContext("2d");
  let scratched = false, moves = 0, coverW = 0;
  function drawCover() {
    const r = cv.getBoundingClientRect(); const dpr = Math.min(2, window.devicePixelRatio || 1);
    if (!r.width || scratched) return;
    if (Math.abs(r.width - coverW) < 2 && moves > 0) return;      // keep scratch progress on small resizes (phone URL bar)
    coverW = r.width;
    cv.width = Math.round(r.width * dpr); cv.height = Math.round(r.height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const w = r.width, h = r.height;
    ctx.globalCompositeOperation = "source-over";
    const g = ctx.createLinearGradient(0, 0, w * .5, h);              // flat, matt lilac-grey, a breath lighter at the top
    g.addColorStop(0, "#d3ccde"); g.addColorStop(.5, "#cec7da"); g.addColorStop(1, "#c6bfd3");
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    const sh = ctx.createRadialGradient(w * .4, h * .3, 2, w * .45, h * .4, w * .9);
    sh.addColorStop(0, "rgba(255,255,255,.14)"); sh.addColorStop(1, "rgba(255,255,255,0)");
    ctx.fillStyle = sh; ctx.fillRect(0, 0, w, h);
    [[.3, .2, .5, "255,255,255", .10], [.72, .36, .42, "196,188,214", .16], [.34, .68, .5, "224,214,230", .12], [.66, .82, .4, "190,184,208", .14], [.5, .5, .3, "236,228,240", .08]]
      .forEach(([x, y, rr, c, a]) => {                               // faint cloudiness, like brushed foil
        const m = ctx.createRadialGradient(w * x, h * y, 0, w * x, h * y, w * rr);
        m.addColorStop(0, `rgba(${c},${a})`); m.addColorStop(1, `rgba(${c},0)`);
        ctx.fillStyle = m; ctx.fillRect(0, 0, w, h);
      });
    ctx.fillStyle = ctx.strokeStyle = "#2f2936"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    const words = (C.scratchText || "Scratch to reveal").split(" ");
    const l1 = words.slice(0, 1).join(" "), l2 = words.slice(1).join(" ");
    const font = '"Monsieur La Doulaise", "Pinyon Script", cursive';
    ctx.font = `100px ${font}`;                                       // both lines one size; the first word spans ~half the oval
    const fs = Math.min(w * 0.26, 100 * (w * 0.45) / Math.max(1, ctx.measureText(l1).width));
    ctx.font = `${fs.toFixed(1)}px ${font}`;
    ctx.lineWidth = Math.max(.4, fs * 0.012);                          // the hairline script reads a little firmer, as in print
    [[l1, 0.448], [l2, 0.568]].forEach(([t, y]) => { ctx.fillText(t, w / 2, h * y); ctx.strokeText(t, w / 2, h * y); });
  }
  function scratchAt(e) {
    const r = cv.getBoundingClientRect();
    const x = e.clientX - r.left, y = e.clientY - r.top;
    ctx.globalCompositeOperation = "destination-out";
    ctx.beginPath(); ctx.arc(x, y, r.width * 0.09, 0, Math.PI * 2); ctx.fill();
    if (++moves % 12 === 0) checkCleared();
  }
  function checkCleared() {
    const { width: w, height: h } = cv;
    const data = ctx.getImageData(0, 0, w, h).data;
    let clear = 0, tot = 0;
    for (let i = 3; i < data.length; i += 4 * 37) { tot++; if (data[i] < 40) clear++; }
    if (clear / tot > 0.42) { scratched = true; cv.classList.add("done"); }
  }
  let down = false;
  cv.addEventListener("pointerdown", e => { down = true; cv.setPointerCapture(e.pointerId); scratchAt(e); });
  cv.addEventListener("pointermove", e => { if (down) scratchAt(e); });
  ["pointerup", "pointercancel", "pointerleave"].forEach(ev => cv.addEventListener(ev, () => { down = false; }));

  // ---------- scroll reveals ----------
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { threshold: 0.15 });
  document.querySelectorAll(".reveal").forEach(el => io.observe(el));

  const layout = () => { drawPearls(); drawCover(); };
  window.addEventListener("resize", layout);
  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(layout);
  layout();
})();
