/* ============ Baraat Card Studio - core ============ */
"use strict";

/* ---------------- the wording (editable) ---------------- */
const DEFAULTS = {
  showBism: true,
  hosts: "Mr. & Mrs. Col Asim",
  invite1: "request the pleasure of your company",
  invite2: "at the Baraat of their beloved son",
  groom: "Abdul Aleem",
  joiner: "with",
  bride: "Laiba",
  brideParents: "",            // e.g. "d/o Mr. & Mrs. ..."  (empty = hidden)
  event: "Baraat",
  day: "Thursday",
  dateNum: "31", dateSup: "st",
  month: "December", year: "2026",
  time: "2:00 pm",
  venue: "Noor Mahal Marquee",
  place: "G.T Road, Islamabad",
  showUrdu: true,
  urdu: "آپ کی شرکت ہمارے لیے باعثِ مسرت ہوگی",
  rsvp: "",                    // empty = hidden
  monoG: "A", monoB: "L",
};
const FIELD_KEYS = Object.keys(DEFAULTS).filter(k => typeof DEFAULTS[k] === "string");
const STORE = "baraat-card-studio-v1";
let D = Object.assign({}, DEFAULTS);
let ADJ = {};                  // per design: { kn, kt, dy }
try { const s = JSON.parse(localStorage.getItem(STORE) || "null"); if (s) { Object.assign(D, s.D || {}); ADJ = s.ADJ || {}; } } catch (e) {}
function save() { try { localStorage.setItem(STORE, JSON.stringify({ D, ADJ })); } catch (e) {} }

/* ---------------- registry ---------------- */
const DESIGNS = [];
function registerDesign(d) { DESIGNS.push(d); }
const ENDCARDS = window.__ENDCARDS || [];   // [{name, idea, src, hash}]

/* ---------------- assets -> blob URLs ---------------- */
const ASSET_URL = {};
(function () {
  const src = window.__ASSETS || {};
  for (const [name, uri] of Object.entries(src)) {
    try {
      const [head, b64] = uri.split(",");
      const mime = head.slice(5, head.indexOf(";"));
      const bin = atob(b64), u8 = new Uint8Array(bin.length);
      for (let i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
      ASSET_URL[name] = URL.createObjectURL(new Blob([u8], { type: mime }));
    } catch (e) { ASSET_URL[name] = uri; }
  }
})();

/* ---------------- helpers for designs ---------------- */
const esc = s => String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const r2 = n => +(+n).toFixed(2);

const H = {
  esc,
  /** editable text: H.f("groom", "div", 'class="name"') */
  f(key, tag = "span", attrs = "") {
    let cls = "f";
    attrs = String(attrs).replace(/\bclass\s*=\s*(["'])(.*?)\1/i, (m, q, c) => { cls += " " + c; return ""; });
    return `<${tag} class="${cls}" data-f="${key}" ${attrs}>${esc(D[key])}</${tag}>`;
  },
  /** returns html only when field is non-empty */
  has(key) { return String(D[key] || "").trim() !== ""; },
  when(key, html) { return H.has(key) ? html : ""; },
  /** URL of an asset file in assets/ e.g. H.img("ivory-satin.webp") */
  img(name) {
    if (!ASSET_URL[name]) console.warn("missing asset", name);
    return ASSET_URL[name] || "";
  },
  /** Bismillah calligraphy glyph (respects the Bismillah checkbox) */
  bism(attrs = 'class="bism"') { return D.showBism ? `<div ${attrs}>&#xFDFD;</div>` : ""; },
  /** Urdu closing line (respects the Urdu checkbox) */
  urdu(attrs = 'class="ur"') { return D.showUrdu && H.has("urdu") ? H.f("urdu", "div", attrs) : ""; },
  /** "Thursday, 31st December 2026" built from editable parts */
  dateLine(o = {}) {
    const sep = o.sep == null ? ", " : o.sep;
    return `${H.f("day")}${esc(sep)}${H.f("dateNum")}<sup>${H.f("dateSup")}</sup> ${H.f("month")} ${H.f("year")}`;
  },
  monoG() { return H.f("monoG"); }, monoB() { return H.f("monoB"); },

  /* ---- geometry ---- */
  /** cusped (multifoil) Mughal arch path. x,w = left & width; ySpring = where the curve starts; yBase = bottom */
  archD(x, w, ySpring, yBase, k = .62, lobes = 7, open = false) {
    const s = w / 2, R = k * w, cxL = x + R, cxR = x + w - R, ta = Math.acos((s - R) / R), L = [], Rr = [];
    for (let i = 0; i <= lobes; i++) { const t = Math.PI - (Math.PI - ta) * i / lobes; L.push([cxL + R * Math.cos(t), ySpring - R * Math.sin(t)]); }
    for (let i = lobes; i >= 0; i--) { const t = Math.PI - (Math.PI - ta) * i / lobes; Rr.push([cxR - R * Math.cos(t), ySpring - R * Math.sin(t)]); }
    let d = `M${r2(x)},${r2(yBase)} L${r2(x)},${r2(ySpring)}`;
    const p = L.concat(Rr.slice(1));
    for (let i = 1; i < p.length; i++) { const r = Math.hypot(p[i][0] - p[i - 1][0], p[i][1] - p[i - 1][1]) * .62; d += ` A${r2(r)},${r2(r)} 0 0 1 ${r2(p[i][0])},${r2(p[i][1])}`; }
    d += ` L${r2(x + w)},${r2(yBase)}`; if (!open) d += " Z"; return d;
  },
  archApex(w, ySpring, k = .62) { const s = w / 2, R = k * w; return ySpring - Math.sqrt(R * R - (R - s) * (R - s)); },
  /** plain pointed arch (two-centred) */
  pointedD(x, w, ySpring, yBase, k = .62, open = false) {
    const s = w / 2, R = k * w, h = Math.sqrt(R * R - (R - s) * (R - s));
    let d = `M${r2(x)},${r2(yBase)} L${r2(x)},${r2(ySpring)} A${r2(R)},${r2(R)} 0 0 1 ${r2(x + s)},${r2(ySpring - h)} A${r2(R)},${r2(R)} 0 0 1 ${r2(x + w)},${r2(ySpring)} L${r2(x + w)},${r2(yBase)}`;
    if (!open) d += " Z"; return d;
  },
  /** ogee / onion arch with shoulders */
  ogeeD(x, w, ySpring, yBase, h, open = false) {
    const X = t => r2(x + w * t), Y = t => r2(ySpring - h * t);
    let d = `M${X(0)},${r2(yBase)} L${X(0)},${Y(0)} C${X(0)},${Y(.1)} ${X(.035)},${Y(.15)} ${X(.075)},${Y(.15)} C${X(.035)},${Y(.25)} ${X(.06)},${Y(.42)} ${X(.2)},${Y(.55)} C${X(.34)},${Y(.68)} ${X(.46)},${Y(.78)} ${X(.5)},${Y(1)} C${X(.54)},${Y(.78)} ${X(.66)},${Y(.68)} ${X(.8)},${Y(.55)} C${X(.94)},${Y(.42)} ${X(.965)},${Y(.25)} ${X(.925)},${Y(.15)} C${X(.965)},${Y(.15)} ${X(1)},${Y(.1)} ${X(1)},${Y(0)} L${X(1)},${r2(yBase)}`;
    if (!open) d += " Z"; return d;
  },
  /** fine gold line-art mandala centred at 0,0 (wrap in <g transform="translate(x,y)">) */
  mandala(R, o = {}) {
    const sw = o.sw || 1.4, st = o.stroke || "url(#gold)", out = [];
    const petal = (r1, r2_, w, pinch = .7) => { const L = r2_ - r1; return `M0,${r2(-r1)} C${r2(w)},${r2(-r1 - L * .2)} ${r2(w * pinch)},${r2(-r2_ + L * .28)} 0,${r2(-r2_)} C${r2(-w * pinch)},${r2(-r2_ + L * .28)} ${r2(-w)},${r2(-r1 - L * .2)} 0,${r2(-r1)}Z`; };
    const rot = (n, fn, off = 0) => { let s = ""; for (let i = 0; i < n; i++) s += `<g transform="rotate(${r2(off + i * 360 / n)})">${fn(i)}</g>`; return s; };
    out.push(`<circle r="${r2(R * .1)}"/><circle r="${r2(R * .045)}" fill="${st}"/>`);
    out.push(rot(8, () => `<path d="${petal(R * .1, R * .24, R * .055)}"/>`));
    out.push(`<circle r="${r2(R * .27)}" stroke-dasharray="1 ${r2(R * .018)}" stroke-linecap="round" stroke-width="${sw * 2}"/>`);
    out.push(rot(16, () => `<path d="${petal(R * .29, R * .48, R * .06)}"/><path d="${petal(R * .32, R * .44, R * .028)}"/>`));
    out.push(rot(16, () => `<circle cy="${r2(-R * .515)}" r="${r2(R * .012)}" fill="${st}" stroke="none"/>`, 11.25));
    out.push(`<circle r="${r2(R * .54)}"/><circle r="${r2(R * .565)}"/>`);
    out.push(rot(24, () => `<path d="${petal(R * .565, R * .78, R * .055, .62)}"/><path d="${petal(R * .6, R * .74, R * .022)}"/><circle cy="${r2(-R * .82)}" r="${r2(R * .011)}" fill="${st}" stroke="none"/>`));
    out.push(rot(48, () => `<path d="M0,${r2(-R * .86)} q${r2(R * .035)},${r2(-R * .06)} 0,${r2(-R * .12)} q${r2(-R * .035)},${r2(R * .06)} 0,${r2(R * .12)}Z"/>`));
    out.push(`<circle r="${r2(R * .85)}" stroke-width="${sw * .8}"/>`);
    out.push(rot(48, () => `<circle cy="${r2(-R * .995)}" r="${r2(R * .009)}" fill="${st}" stroke="none"/>`, 3.75));
    return `<g fill="none" stroke="${st}" stroke-width="${sw}" stroke-linejoin="round">${out.join("")}</g>`;
  },
  /** small flourish divider as inline svg (colour = currentColor) */
  flourish(w = 120, flip = false) {
    return `<svg viewBox="0 0 120 24" width="${w}" height="${w / 5}" style="overflow:visible;${flip ? "transform:scaleX(-1)" : ""}"><g fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"><path d="M2,12 H70"/><path d="M70,12 C82,12 86,4 96,4 C106,4 110,12 104,16 C98,20 90,14 96,9"/></g><circle cx="112" cy="12" r="3.2" fill="currentColor"/></svg>`;
  },
};

/* shared svg defs placed inside every card (so exports keep them) */
const SHARED_DEFS = `<svg class="defs" aria-hidden="true"><defs>
  <linearGradient id="gold" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1000" y2="1400"><stop offset="0" stop-color="#9c7630"/><stop offset=".16" stop-color="#e6c877"/><stop offset=".3" stop-color="#b38a3c"/><stop offset=".46" stop-color="#f1d98f"/><stop offset=".62" stop-color="#a98134"/><stop offset=".8" stop-color="#e0bf6c"/><stop offset="1" stop-color="#8e6a2a"/></linearGradient>
  <linearGradient id="goldBright" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1000" y2="1400"><stop offset="0" stop-color="#c9a24e"/><stop offset=".18" stop-color="#f6e2a2"/><stop offset=".34" stop-color="#d2ad5a"/><stop offset=".5" stop-color="#fff0c0"/><stop offset=".66" stop-color="#c79d48"/><stop offset=".84" stop-color="#f2d88e"/><stop offset="1" stop-color="#b08636"/></linearGradient>
  <linearGradient id="goldB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6e2a2"/><stop offset=".35" stop-color="#c9a24e"/><stop offset=".6" stop-color="#f0d68e"/><stop offset="1" stop-color="#9a742d"/></linearGradient>
  <linearGradient id="roseGold" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1000" y2="1400"><stop offset="0" stop-color="#a86f5a"/><stop offset=".3" stop-color="#f0c4ae"/><stop offset=".55" stop-color="#b9806a"/><stop offset=".8" stop-color="#ecc0a9"/><stop offset="1" stop-color="#94604c"/></linearGradient>
  <linearGradient id="silver" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1000" y2="1400"><stop offset="0" stop-color="#9ea2a6"/><stop offset=".3" stop-color="#f2f3f4"/><stop offset=".55" stop-color="#b3b7bb"/><stop offset=".8" stop-color="#e9ebed"/><stop offset="1" stop-color="#8d9195"/></linearGradient>
  <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="4"/><feColorMatrix type="matrix" values="0 0 0 0 .35  0 0 0 0 .27  0 0 0 0 .18  0 0 0 -1.1 .62"/></filter>
  <filter id="mottle" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".006" numOctaves="4" seed="11"/><feColorMatrix type="matrix" values="0 0 0 0 .55  0 0 0 0 .42  0 0 0 0 .25  0 0 0 -1.6 .9"/></filter>
  <filter id="softshadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000" flood-opacity=".28"/></filter>
</defs></svg>`;

/* ---------------- rendering ---------------- */
function adjOf(id) { return Object.assign({ kn: 1, kt: 1, dy: 0 }, ADJ[id] || {}); }
function cardHTML(d, editing = false) {
  const a = adjOf(d.id);
  let inner = "";
  try { inner = d.render(H, D); } catch (e) { inner = `<div style="padding:60px;color:#c00;font:24px monospace">Design error: ${esc(e.message)}</div>`; console.error(e); }
  return `<div class="card${editing ? " editing" : ""}" data-d="${d.id}" style="--kn:${a.kn};--kt:${a.kt};--dy:${a.dy}px">${SHARED_DEFS}${inner}</div>`;
}
/** shrink text with data-fit="maxWidthPx" until it fits */
function fitAll(root) {
  root.querySelectorAll("[data-fit]").forEach(el => {
    el.style.fontSize = "";
    const max = +el.dataset.fit; let fs = parseFloat(getComputedStyle(el).fontSize), n = 0;
    while (el.scrollWidth > max && fs > 8 && n++ < 60) { fs *= .96; el.style.fontSize = fs + "px"; }
  });
}
function injectStyles() {
  let css = "";
  for (const d of DESIGNS) css += `\n/* ${d.id} */\n` + (typeof d.css === "function" ? d.css(H) : (d.css || ""));
  const st = document.createElement("style"); st.id = "design-css"; st.textContent = css; document.head.appendChild(st);
}

/* ---------------- app ---------------- */
let CUR = 0;                // index into ITEMS
let ITEMS = [];             // [{type:'design', d} | {type:'end', e}]
let editing = true;
const $ = s => document.querySelector(s);

function buildGallery() {
  const g = $("#thumbs-new"), e = $("#thumbs-end");
  g.innerHTML = ""; e.innerHTML = "";
  ITEMS.forEach((it, i) => {
    const t = document.createElement("div");
    t.className = "thumb" + (it.type === "end" ? " tall" : "");
    t.dataset.i = i;
    if (it.type === "design") t.innerHTML = `<div class="mini">${cardHTML(it.d)}</div><span class="num">${i + 1}</span><div class="lbl">${esc(it.d.name)}</div>`;
    else t.innerHTML = `<img src="${H.img(it.e.src)}" alt=""><span class="num">${i + 1}</span><div class="lbl">${esc(it.e.name)}</div>`;
    t.onclick = () => select(i);
    (it.type === "design" ? g : e).appendChild(t);
  });
  if (!ENDCARDS.length) $("#end-h").style.display = "none";
  scaleThumbs();
  fitAll(g);
}
function scaleThumbs() {
  document.querySelectorAll(".thumb .mini").forEach(m => { const w = m.parentElement.clientWidth; m.style.transform = `scale(${w / 1000})`; });
}
function refreshThumb(i) {
  const t = document.querySelector(`.thumb[data-i="${i}"] .mini`);
  if (t && ITEMS[i].type === "design") { t.innerHTML = cardHTML(ITEMS[i].d); fitAll(t); }
}
function refreshAllThumbs() { ITEMS.forEach((it, i) => it.type === "design" && refreshThumb(i)); }

function layoutStage() {
  const st = $(".stage"), h = $(".stage .holder"), c = h.firstElementChild; if (!c) return;
  const W = c.dataset.w ? +c.dataset.w : 1000, Hh = c.dataset.h ? +c.dataset.h : 1400;
  const s = Math.min((st.clientWidth - 36) / W, (st.clientHeight - 36) / Hh);
  h.style.width = W * s + "px"; h.style.height = Hh * s + "px"; c.style.transform = `scale(${s})`;
}
function renderMain() {
  const it = ITEMS[CUR], h = $(".stage .holder");
  if (it.type === "design") {
    h.innerHTML = cardHTML(it.d, editing);
    fitAll(h); bindEditable(h.firstElementChild);
    $(".title").innerHTML = `${esc(it.d.name)}<small>Design ${CUR + 1} of ${ITEMS.length}</small>`;
    $(".idea").innerHTML = `<b>Idea:</b> ${esc(it.d.idea || "")}`;
    $("#adj").style.display = ""; $("#endnote").style.display = "none"; $("#btn-edit").style.display = ""; $(".panel").classList.remove("endmode");
    const a = adjOf(it.d.id); $("#kn").value = a.kn; $("#kt").value = a.kt; $("#dy").value = a.dy; showAdj();
  } else {
    h.innerHTML = `<img src="${H.img(it.e.src)}" data-w="1080" data-h="1920" width="1080" height="1920" alt="">`;
    $(".title").innerHTML = `${esc(it.e.name)}<small>Design ${CUR + 1} of ${ITEMS.length} · from the video studio</small>`;
    $(".idea").innerHTML = `<b>Idea:</b> ${esc(it.e.idea || "")}`;
    $("#adj").style.display = "none"; $("#endnote").style.display = ""; $("#btn-edit").style.display = "none"; $(".panel").classList.add("endmode");
    const a = $("#studio-link"); a.href = "../wedding_invite_studio_fully_customizable.html" + (it.e.hash || "");
  }
  document.querySelectorAll(".thumb").forEach(t => t.classList.toggle("sel", +t.dataset.i === CUR));
  layoutStage();
  try { history.replaceState(null, "", "#" + (it.type === "design" ? it.d.id : "end-" + CUR)); } catch (e) {}
}
function select(i) { CUR = (i + ITEMS.length) % ITEMS.length; renderMain(); const t = document.querySelector(`.thumb[data-i="${CUR}"]`); t && t.scrollIntoView({ block: "nearest" }); }

/* --- editing: on the card --- */
function bindEditable(card) {
  card.querySelectorAll(".f").forEach(el => {
    if (editing) el.setAttribute("contenteditable", "plaintext-only");
    el.addEventListener("keydown", ev => { if (ev.key === "Enter") { ev.preventDefault(); el.blur(); } });
    el.addEventListener("input", () => {
      const k = el.dataset.f; D[k] = el.textContent;
      card.querySelectorAll(`.f[data-f="${k}"]`).forEach(o => { if (o !== el) o.textContent = D[k]; });
      const inp = document.querySelector(`[data-k="${k}"]`); if (inp) inp.value = D[k];
      save();
    });
    el.addEventListener("blur", () => { fitAll(card); clearTimeout(window.__rt); window.__rt = setTimeout(refreshAllThumbs, 50); });
  });
}
/* --- editing: side panel --- */
function buildPanel() {
  document.querySelectorAll("[data-k]").forEach(inp => {
    const k = inp.dataset.k;
    if (inp.type === "checkbox") { inp.checked = !!D[k]; inp.onchange = () => { D[k] = inp.checked; save(); renderMain(); refreshAllThumbs(); }; }
    else { inp.value = D[k] == null ? "" : D[k]; inp.oninput = () => { D[k] = inp.value; save(); liveUpdate(k); }; inp.onchange = () => { renderMain(); refreshAllThumbs(); }; }
  });
  ["kn", "kt", "dy"].forEach(k => {
    $("#" + k).oninput = () => {
      const it = ITEMS[CUR]; if (it.type !== "design") return;
      ADJ[it.d.id] = Object.assign(adjOf(it.d.id), { [k]: +$("#" + k).value }); save();
      const c = $(".stage .card"); c.style.setProperty("--" + k, k === "dy" ? $("#dy").value + "px" : $("#" + k).value); showAdj();
      fitAll(c); refreshThumb(CUR);
    };
  });
  $("#adj-reset").onclick = () => { const it = ITEMS[CUR]; if (it.type !== "design") return; delete ADJ[it.d.id]; save(); renderMain(); refreshThumb(CUR); };
  $("#all-reset").onclick = () => { if (!confirm("Put back the original wording on all designs?")) return; D = Object.assign({}, DEFAULTS); ADJ = {}; save(); buildPanel(); renderMain(); refreshAllThumbs(); };
}
function showAdj() { $("#kn-v").textContent = Math.round($("#kn").value * 100) + "%"; $("#kt-v").textContent = Math.round($("#kt").value * 100) + "%"; $("#dy-v").textContent = $("#dy").value; }
function liveUpdate(k) {
  const c = $(".stage .card"); if (!c) return;
  const els = c.querySelectorAll(`.f[data-f="${k}"]`);
  if (!els.length) { clearTimeout(window.__lu); window.__lu = setTimeout(renderMain, 250); return; }
  els.forEach(o => o.textContent = D[k]); fitAll(c);
  clearTimeout(window.__rt); window.__rt = setTimeout(refreshAllThumbs, 400);
}

/* --- download --- */
function toast(msg) { const t = $(".toast"); t.textContent = msg; t.classList.add("show"); clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove("show"), 2600); }
async function download(px) {
  const it = ITEMS[CUR];
  const name = `${CUR + 1} ${it.type === "design" ? it.d.name : it.e.name}`.replace(/[\\/:*?"<>|]/g, "");
  if (it.type === "end") {
    const a = document.createElement("a"); a.href = H.img(it.e.src); a.download = name + ".png"; a.click(); return;
  }
  if (!window.htmlToImage) { toast("Download needs internet (image tool not loaded)."); return; }
  toast("Making image…");
  const box = $("#exporter"); box.innerHTML = cardHTML(it.d, false); fitAll(box);
  try {
    await document.fonts.ready;
    // wait until every <img> and CSS background image in the card is decoded
    const urls = new Set();
    box.querySelectorAll("*").forEach(el => {
      const bg = getComputedStyle(el).backgroundImage || "";
      for (const m of bg.matchAll(/url\(["']?([^"')]+)["']?\)/g)) urls.add(m[1]);
      const mk = getComputedStyle(el).webkitMaskImage || "";
      for (const m of mk.matchAll(/url\(["']?([^"')]+)["']?\)/g)) urls.add(m[1]);
    });
    const waits = [...box.querySelectorAll("img")].map(im => (im.complete ? Promise.resolve() : new Promise(r => { im.onload = im.onerror = r; })).then(() => im.decode && im.decode().catch(() => {})));
    urls.forEach(u => waits.push(new Promise(r => { const im = new Image(); im.onload = im.onerror = r; im.src = u; })));
    await Promise.all(waits);
    await new Promise(r => setTimeout(r, 200));
    const url = await htmlToImage.toPng(box.firstElementChild, { pixelRatio: px / 1000, width: 1000, height: 1400, cacheBust: false });
    const a = document.createElement("a"); a.href = url; a.download = `${name} (${px}px).png`; a.click();
    toast("Saved to your Downloads folder.");
  } catch (e) { console.error(e); toast("Could not make the image - use Make Images.bat instead."); }
  box.innerHTML = "";
}

/* --- boot --- */
function boot() {
  injectStyles();
  ITEMS = DESIGNS.map(d => ({ type: "design", d })).concat(ENDCARDS.map(e => ({ type: "end", e })));
  if (new URLSearchParams(location.search).has("render")) return renderMode();
  buildGallery(); buildPanel();
  const h = decodeURIComponent(location.hash.slice(1));
  const i = ITEMS.findIndex(it => it.type === "design" && it.d.id === h);
  CUR = i >= 0 ? i : 0;
  renderMain();
  $("#btn-prev").onclick = () => select(CUR - 1);
  $("#btn-next").onclick = () => select(CUR + 1);
  $("#btn-edit").onclick = () => { editing = !editing; $("#btn-edit").classList.toggle("on", editing); $("#btn-edit").textContent = editing ? "Edit on card: ON" : "Edit on card: OFF"; renderMain(); };
  $("#btn-dl1").onclick = () => download(1080);
  $("#btn-dl2").onclick = () => download(2000);
  window.addEventListener("resize", () => { layoutStage(); scaleThumbs(); });
  document.addEventListener("keydown", ev => {
    if (ev.target.closest("input,textarea,[contenteditable]")) return;
    if (ev.key === "ArrowRight") select(CUR + 1);
    if (ev.key === "ArrowLeft") select(CUR - 1);
  });
  document.fonts.ready.then(() => { fitAll(document); layoutStage(); });
}
function renderMode() {
  document.body.classList.add("render");
  const only = (new URLSearchParams(location.search).get("only") || "").split(",").filter(Boolean);
  const root = document.getElementById("renderroot");
  root.innerHTML = DESIGNS.filter(d => !only.length || only.includes(d.id)).map(d => cardHTML(d)).join("");
  document.fonts.ready.then(() => {
    fitAll(root);
    const imgs = [...root.querySelectorAll("img")].map(im => im.complete ? 0 : new Promise(r => { im.onload = im.onerror = r; }));
    Promise.all(imgs).then(() => setTimeout(() => { document.body.dataset.ready = "1"; }, 300));
  });
}
document.addEventListener("DOMContentLoaded", boot);
