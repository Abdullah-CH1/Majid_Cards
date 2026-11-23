/* Vintage Typewriter: per-line typing times (chars typed with steps()), carriage-return timing, keys and type-bar fan. */
WIS.ix['typewriter'] = { update: function (c) {
  var root = c.S.querySelector('.ix-typewriter'); if (!root) return;
  var q = function (s) { return root.querySelector(s); };
  var len = function (s) { return Math.max(1, Array.from(String(s || '')).length); };
  var L = ['Dear family & friends,', 'you are invited to the', c.ev || 'Walima', 'of ' + (c.b || '') + ' & ' + (c.g || ''),
           c.date || '', 'With love & duas,'];
  var n = L.map(len), tot = n.reduce(function (a, b) { return a + b; }, 0);
  var T0 = .75, R = .42, dt = Math.min(.07, 4.6 / tot), t = T0, ends = [];
  var set = function (el, o) { if (!el) return; for (var k in o) el.style.setProperty(k, o[k]); };
  for (var i = 0; i < 6; i++) {
    var s = t, e = s + n[i] * dt, j = i + 1, r = i ? (ends[i - 1] + .03).toFixed(3) + 's' : '0s';
    var v = {'--n': String(n[i]), '--s': s.toFixed(3) + 's', '--e': e.toFixed(3) + 's', '--dt': dt.toFixed(4) + 's', '--r': r};
    set(q('.tw-a.a' + j), v); set(q('.tw-b.b' + j), v); set(q('.tw-l.l' + j), v); set(q('.tw-h.h' + j), v);
    set(q('.tw-v.v' + j), {'--r': r});
    set(q('.tw-dg.d' + j), {'--t': e.toFixed(3) + 's'});
    ends.push(e); t = e + R;
  }
  var tEnd = ends[5];
  /* type-bar fan in the basket */
  var fan = q('.tw-fan');
  if (fan) {
    var f = [];
    for (var a = 10; a <= 170; a += 7.5) {
      var rd = a * Math.PI / 180, cx = Math.cos(rd), sy = Math.sin(rd);
      f.push('<line x1="' + (50 + cx * 3).toFixed(2) + '" y1="' + (112 + sy * 1.8).toFixed(2) + '" x2="' + (50 + cx * 16.6).toFixed(2) +
        '" y2="' + (112 + sy * 9.2).toFixed(2) + '"/>');
    }
    fan.innerHTML = f.join('');
  }
  /* keyboard: 4 rows of round keys, each pressing at its own rhythm while the letter is typed */
  var keys = q('.tw-keys');
  if (keys) {
    var rows = ['1234567890', 'QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM,'], ys = [141.2, 147.6, 154, 160.2], h = [];
    rows.forEach(function (row, ri) {
      var m = row.length, sp = 8.7, x0 = 50 - (m - 1) / 2 * sp + (ri === 3 ? -1.4 : ri * .9);
      for (var k = 0; k < m; k++) {
        var x = x0 + k * sp, y = ys[ri], P = dt * (5 + Math.floor(c.rand() * 9)), kd = T0 + c.rand() * P;
        var cnt = Math.max(1, Math.floor((tEnd - kd) / P));
        h.push('<g class="tw-k" style="--kp:' + P.toFixed(3) + 's;--kd:' + kd.toFixed(3) + 's;--kc:' + cnt + '">' +
          '<circle class="tw-ks" cx="' + x.toFixed(2) + '" cy="' + (y + .9).toFixed(2) + '" r="2.45"/>' +
          '<circle class="tw-kc" cx="' + x.toFixed(2) + '" cy="' + y.toFixed(2) + '" r="2.45"/>' +
          '<circle class="tw-kr" cx="' + x.toFixed(2) + '" cy="' + y.toFixed(2) + '" r="1.85"/>' +
          '<text class="tw-kt" x="' + x.toFixed(2) + '" y="' + (y + .78).toFixed(2) + '" text-anchor="middle">' + row.charAt(k).replace('&', '&amp;') + '</text></g>');
      }
    });
    keys.innerHTML = h.join('');
  }
} };
