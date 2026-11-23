(() => {
  'use strict';

  const $ = selector => document.querySelector(selector);
  const $$ = selector => [...document.querySelectorAll(selector)];
  const details = {
    groom: 'Abdul Aleem',
    bride: 'Laiba',
    date: 'Thursday, 31 December 2026',
    start: '2026-12-31T14:00:00+05:00',
    end: '2026-12-31T17:00:00+05:00',
    venue: 'Noor Mahal Marquee',
    address: 'G.T. Road, Islamabad, Pakistan',
    hostWhatsApp: ''
  };
  let toastTimer;

  function notify(message) {
    const toast = $('#toast');
    if (!toast) return;
    clearTimeout(toastTimer);
    toast.textContent = message;
    toast.classList.add('on');
    toastTimer = setTimeout(() => toast.classList.remove('on'), 3400);
  }

  function currentEvent() {
    return ($('#ev')?.textContent || 'Baraat').trim();
  }

  function currentDesign() {
    return ($('#snName')?.textContent.split(' · ')[0] || 'Animated invitation').trim();
  }

  function eventTitle() {
    return `${details.groom} & ${details.bride} — ${currentEvent()}`;
  }

  function invitationText() {
    return `You’re invited to the ${currentEvent()} of ${details.groom} & ${details.bride}. ${details.date} at 2:00 PM, ${details.venue}, ${details.address}.`;
  }

  function shareUrl() {
    if (!/^https?:$/.test(location.protocol)) return '';
    return location.href;
  }

  function fullShareText() {
    const url = shareUrl();
    return `${invitationText()}\nAnimated design: ${currentDesign()}${url ? `\n${url}` : ''}`;
  }

  function calendarDate(date) {
    return date.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
  }

  function calendarUrl() {
    const params = new URLSearchParams({
      action: 'TEMPLATE',
      text: eventTitle(),
      dates: `${calendarDate(new Date(details.start))}/${calendarDate(new Date(details.end))}`,
      details: invitationText(),
      location: `${details.venue}, ${details.address}`
    });
    return `https://calendar.google.com/calendar/render?${params}`;
  }

  function icsEscape(value) {
    return value.replace(/\\/g, '\\\\').replace(/\n/g, '\\n').replace(/,/g, '\\,').replace(/;/g, '\\;');
  }

  function downloadCalendar() {
    const url = shareUrl();
    const lines = [
      'BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Aleem and Laiba//Animated Wedding Invitation//EN',
      'CALSCALE:GREGORIAN', 'METHOD:PUBLISH', 'BEGIN:VEVENT',
      'UID:aleem-laiba-20261231@wedding-invitation',
      `DTSTAMP:${calendarDate(new Date())}`,
      `DTSTART:${calendarDate(new Date(details.start))}`,
      `DTEND:${calendarDate(new Date(details.end))}`,
      `SUMMARY:${icsEscape(eventTitle())}`,
      `DESCRIPTION:${icsEscape(`${invitationText()}${url ? `\n${url}` : ''}`)}`,
      `LOCATION:${icsEscape(`${details.venue}, ${details.address}`)}`,
      'END:VEVENT', 'END:VCALENDAR'
    ];
    const blob = new Blob([lines.join('\r\n')], {type:'text/calendar;charset=utf-8'});
    const objectUrl = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = objectUrl;
    link.download = `Abdul-Aleem-Laiba-${currentEvent()}.ics`;
    document.body.append(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(objectUrl), 1500);
    notify('Calendar file downloaded.');
  }

  function updateCountdown() {
    const distance = new Date(details.start).getTime() - Date.now();
    const remaining = Math.max(0, distance);
    const values = {
      days: Math.floor(remaining / 86400000),
      hours: Math.floor(remaining / 3600000) % 24,
      minutes: Math.floor(remaining / 60000) % 60,
      seconds: Math.floor(remaining / 1000) % 60
    };
    Object.entries(values).forEach(([key, value]) => {
      const element = $(`#animated${key[0].toUpperCase()}${key.slice(1)}`);
      if (element) element.textContent = String(value).padStart(2, '0');
    });
    const message = $('#animatedCountdownMessage');
    if (message && distance <= 0) message.textContent = distance > -86400000 ? 'The celebration has begun!' : 'Thank you for celebrating with us.';
  }

  class MusicBox {
    constructor(button) {
      this.button = button;
      this.context = null;
      this.timer = null;
      this.step = 0;
      this.playing = false;
      this.sequence = [293.66,440,369.99,440,329.63,493.88,392,493.88,349.23,440,392,329.63,293.66,369.99,440,369.99];
    }
    async start() {
      try {
        if (!this.context) {
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          if (!AudioContext) throw new Error('Audio unavailable');
          this.context = new AudioContext();
          this.master = this.context.createGain();
          this.master.gain.value = .16;
          this.master.connect(this.context.destination);
        }
        await this.context.resume();
        if (this.playing) return;
        this.playing = true;
        this.playNote();
        this.timer = setInterval(() => this.playNote(), 520);
        this.updateButton();
      } catch {
        notify('Music is not available in this browser.');
      }
    }
    stop() {
      this.playing = false;
      clearInterval(this.timer);
      this.timer = null;
      if (this.context) this.context.suspend();
      this.updateButton();
    }
    toggle() { this.playing ? this.stop() : this.start(); }
    updateButton() {
      this.button.setAttribute('aria-pressed', String(this.playing));
      this.button.setAttribute('aria-label', this.playing ? 'Pause music' : 'Play music');
      this.button.textContent = this.playing ? 'Music on' : 'Music off';
    }
    playNote() {
      if (!this.playing || document.hidden) return;
      const now = this.context.currentTime;
      const frequency = this.sequence[this.step % this.sequence.length];
      const oscillator = this.context.createOscillator();
      const gain = this.context.createGain();
      oscillator.type = 'sine';
      oscillator.frequency.setValueAtTime(frequency, now);
      gain.gain.setValueAtTime(.0001, now);
      gain.gain.exponentialRampToValueAtTime(.16, now + .025);
      gain.gain.exponentialRampToValueAtTime(.0001, now + 1.8);
      oscillator.connect(gain);
      gain.connect(this.master);
      oscillator.start(now);
      oscillator.stop(now + 1.85);
      if (this.step % 4 === 0) {
        const bass = this.context.createOscillator();
        const bassGain = this.context.createGain();
        bass.type = 'triangle';
        bass.frequency.value = frequency / 2;
        bassGain.gain.setValueAtTime(.0001, now);
        bassGain.gain.exponentialRampToValueAtTime(.05, now + .04);
        bassGain.gain.exponentialRampToValueAtTime(.0001, now + 2.1);
        bass.connect(bassGain);
        bassGain.connect(this.master);
        bass.start(now);
        bass.stop(now + 2.15);
      }
      this.step += 1;
    }
  }

  async function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.append(textarea);
    textarea.select();
    const copied = document.execCommand('copy');
    textarea.remove();
    if (!copied) throw new Error('Copy failed');
  }

  function updateSelection() {
    const name = currentDesign();
    if ($('#toolsDesignName')) $('#toolsDesignName').textContent = name;
    if ($('#animatedGoogle')) $('#animatedGoogle').href = calendarUrl();
    if ($('#animatedWaShare')) $('#animatedWaShare').href = `https://wa.me/?text=${encodeURIComponent(fullShareText())}`;
    document.title = `${name} | ${details.groom} & ${details.bride}`;
  }

  function initialiseTools() {
    if (!$('#inviteTools')) return;
    const galleryHeading = $('.galh b');
    if (galleryHeading) galleryHeading.textContent = 'Animated designs';
    const hint = $('#kbdHint');
    if (hint) hint.textContent = 'Tap the card to replay · use the arrows to browse animations';
    $('#animatedDirections').href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${details.venue}, ${details.address}`)}`;
    $('#animatedIcs').addEventListener('click', downloadCalendar);
    $('#animatedShare').addEventListener('click', async () => {
      const url = shareUrl();
      if (navigator.share && url) {
        try {
          await navigator.share({title:eventTitle(), text:`${invitationText()}\nAnimated design: ${currentDesign()}`, url});
          return;
        } catch (error) {
          if (error.name === 'AbortError') return;
        }
      }
      try {
        await copyText(fullShareText());
        notify(url ? 'Invitation and animated design link copied.' : 'Invitation details copied. Your live design link will work after hosting.');
      } catch {
        notify('Please use the WhatsApp link to share this design.');
      }
    });

    const music = new MusicBox($('#animatedMusic'));
    $('#animatedMusic').addEventListener('click', () => music.toggle());
    const form = $('#animatedRsvpForm');
    $('#animatedRsvpToggle').addEventListener('click', () => {
      form.hidden = !form.hidden;
      $('#animatedRsvpToggle').setAttribute('aria-expanded', String(!form.hidden));
      if (!form.hidden) form.scrollIntoView({behavior:'smooth', block:'nearest'});
    });
    $$('input[name="animatedAttendance"]').forEach(input => input.addEventListener('change', () => {
      $('#animatedCountField').hidden = $('input[name="animatedAttendance"]:checked').value === 'Regretfully declines';
    }));

    try {
      const saved = JSON.parse(localStorage.getItem('aleem-laiba-rsvp') || 'null');
      if (saved) {
        $('#animatedName').value = saved.name || '';
        $('#animatedGuests').value = saved.guests || '1';
        $('#animatedMessage').value = saved.message || '';
        const attendance = $$('input[name="animatedAttendance"]').find(input => input.value === saved.attendance);
        if (attendance) attendance.checked = true;
        $('#animatedCountField').hidden = saved.attendance === 'Regretfully declines';
        $('#animatedSaved').hidden = false;
      }
    } catch {}

    form.addEventListener('submit', event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const data = new FormData(form);
      const response = {
        name: String(data.get('name')).trim(),
        attendance: String(data.get('animatedAttendance')),
        guests: String(data.get('guests')),
        message: String(data.get('message')).trim()
      };
      const lines = [`Wedding RSVP — ${details.groom} & ${details.bride}`, `Event: ${currentEvent()}`, `Name: ${response.name}`, `Response: ${response.attendance}`];
      if (response.attendance === 'Joyfully accepts') lines.push(`Number of guests: ${response.guests}`);
      if (response.message) lines.push(`Message: ${response.message}`);
      try {
        localStorage.setItem('aleem-laiba-rsvp', JSON.stringify(response));
        $('#animatedSaved').hidden = false;
      } catch {}
      const phone = details.hostWhatsApp.replace(/\D/g, '');
      const popup = window.open(`https://wa.me/${phone}?text=${encodeURIComponent(lines.join('\n'))}`, '_blank');
      if (popup) popup.opener = null;
      else location.href = `https://wa.me/${phone}?text=${encodeURIComponent(lines.join('\n'))}`;
      notify('WhatsApp opened — tap Send to deliver your RSVP.');
    });

    updateSelection();
    updateCountdown();
    setInterval(updateCountdown, 1000);
    ['#snName', '#ev'].forEach(selector => {
      const element = $(selector);
      if (element) new MutationObserver(updateSelection).observe(element, {childList:true, subtree:true, characterData:true});
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialiseTools);
  else initialiseTools();
})();
