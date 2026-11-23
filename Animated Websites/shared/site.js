(() => {
  const W = window.WEDDING;
  const SITE = window.SITE || {};
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const stage = $('#st');
  const hero = $('#top');

  // ---------- toast ----------
  const toastEl = $('#siteToast');
  let toastTimer;
  function toast(msg) {
    clearTimeout(toastTimer);
    toastEl.textContent = msg;
    toastEl.classList.add('is-on');
    toastTimer = setTimeout(() => toastEl.classList.remove('is-on'), 3600);
  }

  // ---------- wording helpers ----------
  const title = () => `${W.groom} & ${W.bride} · ${W.event}`;
  const inviteText = () => `You're invited to the ${W.event} of ${W.groom} & ${W.bride} — ${W.dateDisplay} at ${W.timeDisplay}, ${W.venue}, ${W.address}.`;
  function shareUrl() {
    if (!/^https?:$/.test(location.protocol)) return '';
    const url = new URL(location.href);
    const guest = url.searchParams.get('guest');
    url.search = ''; url.hash = '';
    if (guest) url.searchParams.set('guest', guest);
    return url.href;
  }
  const fullShareText = () => { const u = shareUrl(); return inviteText() + (u ? `\n${u}` : ''); };

  // ---------- guest name from the link: ?guest=Saad%20%26%20Family ----------
  const guest = (new URLSearchParams(location.search).get('guest') || '').trim().slice(0, 80);
  if (guest) $('#guestName').textContent = `Dear ${guest}`;

  // ---------- music: uses shared/music.mp3 if you add one, otherwise a soft music-box tune ----------
  class MusicBox {
    constructor() { this.ctx = null; this.timer = null; this.step = 0; this.playing = false;
      this.seq = [293.66, 440, 369.99, 440, 329.63, 493.88, 392, 493.88, 349.23, 440, 392, 329.63, 293.66, 369.99, 440, 369.99]; }
    async start() {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) throw new Error('no audio');
      if (!this.ctx) { this.ctx = new AC(); this.master = this.ctx.createGain(); this.master.gain.value = .15; this.master.connect(this.ctx.destination); }
      await this.ctx.resume();
      if (this.playing) return;
      this.playing = true; this.note(); this.timer = setInterval(() => this.note(), 520);
    }
    stop() { this.playing = false; clearInterval(this.timer); if (this.ctx) this.ctx.suspend(); }
    note() {
      if (!this.playing || document.hidden) return;
      const t = this.ctx.currentTime, f = this.seq[this.step % this.seq.length];
      const tone = (type, freq, peak, len) => {
        const o = this.ctx.createOscillator(), g = this.ctx.createGain();
        o.type = type; o.frequency.setValueAtTime(freq, t);
        g.gain.setValueAtTime(.0001, t); g.gain.exponentialRampToValueAtTime(peak, t + .03); g.gain.exponentialRampToValueAtTime(.0001, t + len);
        o.connect(g); g.connect(this.master); o.start(t); o.stop(t + len + .05);
      };
      tone('sine', f, .16, 1.8);
      if (this.step % 4 === 0) tone('triangle', f / 2, .05, 2.1);
      this.step += 1;
    }
  }
  const musicBtn = $('#musicBtn');
  const song = new Audio('shared/music.mp3');
  song.loop = true; song.preload = 'none';
  const box = new MusicBox();
  let mode = null, playing = false;
  function setMusic(on) { playing = on; musicBtn.setAttribute('aria-pressed', String(on)); musicBtn.setAttribute('aria-label', on ? 'Pause music' : 'Play music'); }
  async function musicOn() {
    try {
      if (mode !== 'box') { await song.play(); mode = 'song'; setMusic(true); return; }
    } catch { mode = 'box'; }
    try { await box.start(); mode = 'box'; setMusic(true); } catch { setMusic(false); }
  }
  function musicOff() { if (mode === 'song') song.pause(); else box.stop(); setMusic(false); }
  musicBtn.addEventListener('click', () => (playing ? musicOff() : musicOn()));
  document.addEventListener('visibilitychange', () => { if (document.hidden && mode === 'song' && playing) song.pause(); else if (!document.hidden && mode === 'song' && playing) song.play().catch(() => {}); });

  // ---------- opening: tap the cover, then the animated invitation plays ----------
  const cover = $('#cover');
  let doneTimer;
  function animationLength() {
    const te = parseFloat(getComputedStyle(stage).getPropertyValue('--te')) || 13;
    return reduced ? 0.3 : Math.min(te, 30);
  }
  function playStage() {
    hero.classList.remove('is-done');
    clearTimeout(doneTimer);
    if (typeof window.WIS_PLAY === 'function') window.WIS_PLAY();
    doneTimer = setTimeout(() => hero.classList.add('is-done'), animationLength() * 1000);
  }
  function openInvitation() {
    if (cover.classList.contains('is-open')) return;
    cover.classList.add('is-open');
    document.body.classList.remove('is-locked');
    musicBtn.hidden = false;
    musicOn();
    window.scrollTo(0, 0);
    playStage();
    setTimeout(() => cover.remove(), reduced ? 50 : 1200);
  }
  $('#openBtn').addEventListener('click', openInvitation);
  $('#replay').addEventListener('click', () => { window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' }); playStage(); });

  // ---------- countdown ----------
  const start = new Date(W.start).getTime();
  const cells = { d: $('#cdD'), h: $('#cdH'), m: $('#cdM'), s: $('#cdS') };
  function tick() {
    const left = start - Date.now(), r = Math.max(0, left);
    cells.d.textContent = String(Math.floor(r / 864e5)).padStart(2, '0');
    cells.h.textContent = String(Math.floor(r / 36e5) % 24).padStart(2, '0');
    cells.m.textContent = String(Math.floor(r / 6e4) % 60).padStart(2, '0');
    cells.s.textContent = String(Math.floor(r / 1e3) % 60).padStart(2, '0');
    if (left <= 0) $('#cdMsg').textContent = left > -864e5 ? 'The celebration has begun!' : 'Thank you for celebrating with us.';
  }
  tick(); setInterval(tick, 1000);

  // ---------- calendar + directions ----------
  const calDate = d => d.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
  const place = `${W.venue}, ${W.address}`;
  $('#googleCal').href = 'https://calendar.google.com/calendar/render?' + new URLSearchParams({
    action: 'TEMPLATE', text: title(),
    dates: `${calDate(new Date(W.start))}/${calDate(new Date(W.end))}`,
    details: inviteText(), location: place
  });
  $('#directions').href = 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(W.mapsQuery || place);
  const icsEsc = v => v.replace(/\\/g, '\\\\').replace(/\n/g, '\\n').replace(/,/g, '\\,').replace(/;/g, '\\;');
  $('#icsBtn').addEventListener('click', () => {
    const u = shareUrl();
    const ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Aleem and Laiba//Invitation//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH',
      'BEGIN:VEVENT', 'UID:aleem-laiba-baraat-20261231@invitation', `DTSTAMP:${calDate(new Date())}`,
      `DTSTART:${calDate(new Date(W.start))}`, `DTEND:${calDate(new Date(W.end))}`,
      `SUMMARY:${icsEsc(title())}`, `DESCRIPTION:${icsEsc(inviteText() + (u ? `\n${u}` : ''))}`, `LOCATION:${icsEsc(place)}`,
      'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
    const href = URL.createObjectURL(new Blob([ics], { type: 'text/calendar;charset=utf-8' }));
    const a = Object.assign(document.createElement('a'), { href, download: 'Abdul-Aleem-Laiba-Baraat.ics' });
    document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(href), 1500);
    toast('Calendar file downloaded — open it to add the Baraat.');
  });

  // ---------- RSVP on WhatsApp ----------
  const form = $('#rsvpForm');
  const countField = $('#countField');
  const KEY = 'aleem-laiba-rsvp';
  const syncCount = () => { countField.hidden = $('input[name="attendance"]:checked', form).value === 'Regretfully declines'; };
  $$('input[name="attendance"]', form).forEach(i => i.addEventListener('change', syncCount));
  try {
    const saved = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (saved) {
      $('#rsvpName').value = saved.name || '';
      $('#rsvpCount').value = saved.guests || '1';
      $('#rsvpMsg').value = saved.message || '';
      const att = $$('input[name="attendance"]', form).find(i => i.value === saved.attendance);
      if (att) att.checked = true;
      syncCount();
      $('#savedNote').hidden = false;
    }
  } catch {}
  form.addEventListener('submit', e => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const d = new FormData(form);
    const r = { name: String(d.get('name')).trim(), attendance: String(d.get('attendance')), guests: String(d.get('guests')), message: String(d.get('message')).trim() };
    const lines = [`${W.event} RSVP — ${W.groom} & ${W.bride}`, `Name: ${r.name}`, `Response: ${r.attendance}`];
    if (r.attendance === 'Joyfully accepts') lines.push(`Number of guests: ${r.guests}`);
    if (r.message) lines.push(`Message: ${r.message}`);
    try { localStorage.setItem(KEY, JSON.stringify(r)); $('#savedNote').hidden = false; } catch {}
    const phone = String(W.hostWhatsApp || '').replace(/\D/g, '');
    const url = `https://wa.me/${phone}?text=${encodeURIComponent(lines.join('\n'))}`;
    const win = window.open(url, '_blank');
    if (win) win.opener = null; else location.href = url;
    toast('WhatsApp opened — tap Send to deliver your RSVP.');
  });

  // ---------- sharing ----------
  async function copy(text) {
    if (navigator.clipboard && window.isSecureContext) { await navigator.clipboard.writeText(text); return; }
    const t = Object.assign(document.createElement('textarea'), { value: text });
    t.style.cssText = 'position:fixed;opacity:0'; document.body.append(t); t.select();
    const ok = document.execCommand('copy'); t.remove(); if (!ok) throw new Error('copy failed');
  }
  $('#waShare').href = `https://wa.me/?text=${encodeURIComponent(fullShareText())}`;
  $('#shareBtn').addEventListener('click', async () => {
    const url = shareUrl();
    if (navigator.share && url) {
      try { await navigator.share({ title: title(), text: inviteText(), url }); return; }
      catch (err) { if (err.name === 'AbortError') return; }
    }
    try { await copy(fullShareText()); toast(url ? 'Invitation and link copied.' : 'Details copied. The live link works once the site is online.'); }
    catch { toast('Please use the WhatsApp button to share.'); }
  });
  $('#copyBtn').addEventListener('click', async () => {
    const url = shareUrl();
    try { await copy(url || fullShareText()); toast(url ? 'Link copied.' : 'Details copied. The live link works once the site is online.'); }
    catch { toast('Could not copy. Please copy the address from your browser.'); }
  });

  // ---------- reveal sections as they scroll in ----------
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } }), { threshold: .12 });
  $$('.reveal').forEach(el => io.observe(el));

  window.SITE_READY = true;
})();
