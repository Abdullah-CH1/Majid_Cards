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

  // ---------- countdown ticket shape (scalloped ends) ----------
  (function ticketShape() {
    const w = 400, h = 100, r = 8, n = 5;           // n scallops on each end
    let d = `M ${r} 0 H ${w - r}`;
    for (let i = 0; i < n; i++) {                    // right end: bumps
      const y0 = (i / n) * h, y1 = ((i + 1) / n) * h;
      d += ` Q ${w + 2} ${(y0 + y1) / 2} ${w - r} ${y1}`;
    }
    d += ` H ${r}`;
    for (let i = n; i > 0; i--) {                    // left end
      const y0 = (i / n) * h, y1 = ((i - 1) / n) * h;
      d += ` Q ${-2} ${(y0 + y1) / 2} ${r} ${y1}`;
    }
    d += " Z";
    const svg = `<svg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -2 ${w + 8} ${h + 4}' preserveAspectRatio='none'>` +
      `<path d='${d}' fill='#f6f3f7'/><path d='${d}' fill='none' stroke='#cfc6d3' stroke-width='1' transform='translate(${w * 0.03} ${h * 0.09}) scale(.94 .82)'/></svg>`;
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
  const BOW_FRAMES = 24;
  const bowImg = $("#bowImg");
  const bowSrc = i => `assets/bow/bow-${String(i).padStart(2, "0")}.webp`;
  const bowCache = [];
  for (let i = 0; i < BOW_FRAMES; i++) { const im = new Image(); im.src = bowSrc(i); bowCache.push(im); }   // preload while the envelope is shown
  const halfL = $(".wrap.half.left"), halfR = $(".wrap.half.right"), wrapBox = $("#wrapBox");
  const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;    // easeInOutCubic
  const clamp01 = t => Math.max(0, Math.min(1, t));
  const wait = ms => new Promise(r => setTimeout(r, ms));
  function animate(ms, step) {                 // runs step(0..1) every frame for ms milliseconds
    return new Promise(res => {
      const t0 = performance.now();
      const f = now => { const t = clamp01((now - t0) / ms); step(t); t < 1 ? requestAnimationFrame(f) : res(); };
      requestAnimationFrame(f);
    });
  }
  const bandL = $(".band-half.left"), bandR = $(".band-half.right");
  const easeIn = t => t * t * t, easeOut = t => 1 - Math.pow(1 - t, 3);
  function setDiamond(p) {                     // the knot lets go: the fabric opens from the centre as a diamond,
    const e = easeOut(p) * 0.35 + ease(p) * 0.65;   // pinched left and right where the ribbon gathers pull it aside
    const A = 96 * e, B = 66 * e;             // half-height / half-width of the diamond, % of the screen
    halfL.style.clipPath = `polygon(0 0, 50.1% 0, 50.1% ${50 - A}%, ${50 - B}% 50%, 50.1% ${50 + A}%, 50.1% 100%, 0 100%)`;
    halfR.style.clipPath = `polygon(100% 0, 49.9% 0, 49.9% ${50 - A}%, ${50 + B}% 50%, 49.9% ${50 + A}%, 49.9% 100%, 100% 100%)`;
    wrapBox.style.setProperty("--B", `${B}%`);
    wrapBox.style.setProperty("--g", String(Math.sin(Math.min(1, p * 1.15) * Math.PI) * 0.9));
    const k = Math.max(0.02, 1 - B / 50);      // each band half stays gathered at its pinch point
    bandL.style.transform = `scaleX(${k})`; bandR.style.transform = `scaleX(${k})`;
    bandL.style.opacity = bandR.style.opacity = String(clamp01(k * 2.2));
    halfL.style.opacity = halfR.style.opacity = String(1 - clamp01((p - 0.86) / 0.14));
  }
  let started = false;
  async function openInvitation() {
    if (started) return; started = true;
    if (audio.src) audio.play().then(() => setMuted(false)).catch(() => {});
    op.classList.add("open");                  // flap folds back, the seal goes with it
    await wait(1150);
    op.classList.add("drop");                  // envelope slides away: sheer organza + bow over the card
    await wait(1650);
    await animate(1650, t => {                 // the bow is pulled undone: loops slip into the knot, tails draw out to the sides
      const i = Math.round(ease(t) * (BOW_FRAMES - 1));
      const src = bowSrc(i);
      if (!bowImg.src.endsWith(src)) bowImg.src = src;
    });
    animate(260, t => { bowImg.style.opacity = String(1 - t); });
    setTimeout(() => body.classList.add("revealed"), 1250);   // wording fades in once the card is clear
    await animate(1500, setDiamond);
    body.classList.remove("locked");
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

  // ---------- pearl frame (row of pearls around the section) ----------
  const pf = $("#pearlFrame");
  function drawPearls() {
    const r = pf.getBoundingClientRect(); const W = r.width, H = r.height;
    if (!W) return;
    const m = W * 0.07, rad = W * 0.09, step = W * 0.034;
    const x0 = m, y0 = m, x1 = W - m, y1 = H - m;
    const pts = [];
    const seg = (ax, ay, bx, by) => { const L = Math.hypot(bx - ax, by - ay); return { L, f: t => [ax + (bx - ax) * t, ay + (by - ay) * t] }; };
    const arc = (cx, cy, a0, a1) => ({ L: Math.abs(a1 - a0) * rad, f: t => [cx + rad * Math.cos(a0 + (a1 - a0) * t), cy + rad * Math.sin(a0 + (a1 - a0) * t)] });
    const parts = [
      seg(x0 + rad, y0, x1 - rad, y0), arc(x1 - rad, y0 + rad, -Math.PI / 2, 0),
      seg(x1, y0 + rad, x1, y1 - rad), arc(x1 - rad, y1 - rad, 0, Math.PI / 2),
      seg(x1 - rad, y1, x0 + rad, y1), arc(x0 + rad, y1 - rad, Math.PI / 2, Math.PI),
      seg(x0, y1 - rad, x0, y0 + rad), arc(x0 + rad, y0 + rad, Math.PI, Math.PI * 1.5)];
    const total = parts.reduce((a, p) => a + p.L, 0);
    const n = Math.round(total / step);
    for (let i = 0; i < n; i++) {
      let d = (i / n) * total, k = 0;
      while (d > parts[k].L) { d -= parts[k].L; k++; }
      pts.push(parts[k].f(d / parts[k].L));
    }
    const pr = W * 0.0105;
    let s = `<defs><radialGradient id="pg" cx="35%" cy="32%" r="70%"><stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="#f3eef4"/><stop offset=".75" stop-color="#c9bfcd"/><stop offset="1" stop-color="#8e8296"/></radialGradient></defs>`;
    s += `<path d="M ${x0 + rad} ${y0 + W * .022} H ${x1 - rad}" stroke="none"/>`;
    pts.forEach(([x, y], i) => {
      const big = i % 4 === 0;
      s += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${(big ? pr * 1.35 : pr).toFixed(2)}" fill="url(#pg)" style="filter:drop-shadow(0 1px 1.5px rgba(40,25,45,.45))"/>`;
    });
    pf.setAttribute("viewBox", `0 0 ${W} ${H}`);
    pf.innerHTML = s;
  }

  // ---------- scratch to reveal ----------
  const cv = $("#scratch"), ctx = cv.getContext("2d");
  let scratched = false, moves = 0, coverW = 0, fontsDone = false;
  function drawCover() {
    const r = cv.getBoundingClientRect(); const dpr = Math.min(2, window.devicePixelRatio || 1);
    if (!r.width || scratched) return;
    if (Math.abs(r.width - coverW) < 2 && moves > 0) return;      // keep scratch progress on small resizes (phone URL bar)
    coverW = r.width;
    cv.width = Math.round(r.width * dpr); cv.height = Math.round(r.height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const w = r.width, h = r.height;
    const g = ctx.createRadialGradient(w * .4, h * .35, 4, w * .5, h * .5, w * .75);
    g.addColorStop(0, "#fbf8fb"); g.addColorStop(.6, "#ece4ee"); g.addColorStop(1, "#cdc1d1");
    ctx.globalCompositeOperation = "source-over";
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = "rgba(140,120,145,.55)"; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.ellipse(w / 2, h / 2, w / 2 - 9, h / 2 - 9, 0, 0, Math.PI * 2); ctx.stroke();
    ctx.fillStyle = "#7d6c7c"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    const words = (C.scratchText || "Scratch to reveal").split(" ");
    const l1 = words.slice(0, 1).join(" "), l2 = words.slice(1).join(" ");
    ctx.font = `${Math.round(w * 0.16)}px "Pinyon Script", cursive`;
    ctx.fillText(l1, w / 2, h * 0.44);
    ctx.font = `${Math.round(w * 0.12)}px "Pinyon Script", cursive`;
    ctx.fillText(l2, w / 2, h * 0.58);
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
