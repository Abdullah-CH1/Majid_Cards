/* Departure Board: builds split-flap rows from the couple's details. */
(function () {
  var AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }
  function up(s, n) { return String(s || '').toUpperCase().replace(/\s+/g, ' ').trim().slice(0, n); }
  WIS.ix['departure-board'] = { update: function (c) {
    var root = c.S.querySelector('.ix-departure-board'); if (!root) return;
    var box = root.querySelector('.db-rows'); if (!box) return;
    var rnd = c.rand || Math.random, dp = c.dp || {};
    var ev = String(c.ev || 'Walima').toUpperCase();
    var dd = ('0' + (parseInt(dp.day, 10) || 1)).slice(-2);
    var mm = ('0' + (((dp.monIndex >= 0) ? dp.monIndex : 11) + 1)).slice(-2);
    var date = (dd + ' ' + up(dp.mon3 || dp.mon || 'DEC', 3) + ' ' + (dp.year || '')).trim();
    var rows = [
      [{ l: 'Flight', t: ev.replace(/[^A-Z]/g, '').slice(0, 2) + ' ' + dd + mm }],
      [{ l: 'Destination', t: up(ev, 14) }],
      [{ l: 'Passengers', t: up(c.g || 'Hamza', 14) }],
      [{ l: '', t: '& ' + up(c.b || 'Ayesha', 12) }],
      [{ l: 'Date', t: up(date, 14) }],
      [{ l: 'Gate', t: 'OPEN', w: 5 }, { l: 'Status', t: 'ON TIME', w: 8, k: 'db-st' }]
    ];
    var h = [], r, s, i, k, t0;
    for (r = 0; r < rows.length; r++) {
      t0 = 0.7 + r * 0.55;
      h.push('<div class="db-row">');
      for (s = 0; s < rows[r].length; s++) {
        var seg = rows[r][s], w = seg.w || 14, txt = seg.t.slice(0, w);
        h.push('<div class="db-seg ' + (seg.k || '') + '" style="--w:' + w + '">');
        h.push('<div class="db-lb">' + esc(seg.l) + '</div><div class="db-tl">');
        for (i = 0; i < w; i++) {
          var ch = txt.charAt(i);
          if (!ch || ch === ' ') { h.push('<i class="db-t"></i>'); continue; }
          var n = 2 + Math.floor(rnd() * 3), strip = ['<span></span>'];
          for (k = 0; k < n - 1; k++) strip.push('<span>' + AZ.charAt(Math.floor(rnd() * AZ.length)) + '</span>');
          strip.push('<span class="db-f">' + esc(ch) + '</span>');
          var d = t0 + (s ? 0.3 : 0) + i * 0.045;
          h.push('<i class="db-t db-a" style="--d:' + d.toFixed(2) + 's;--n:' + n + '"><b>' + strip.join('') + '</b></i>');
        }
        h.push('</div></div>');
      }
      h.push('</div>');
    }
    box.innerHTML = h.join('');
  } };
})();
