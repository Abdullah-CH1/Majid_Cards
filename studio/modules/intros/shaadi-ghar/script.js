/* Shaadi Wala Ghar: builds the fairy-light strings (wires + bulbs) on the wedding house, the neighbours'
   rooftops, the minaret and the ring around the initials. Every bulb gets its own switch-on time (--t)
   and chase phase (--c); CSS does all the animation. */
(function () {
  function f(x) { return (Math.round(x * 100) / 100).toString(); }
  WIS.ix['shaadi-ghar'] = {
    update: function (c) {
      var root = c.S.querySelector('.ix-shaadi-ghar'); if (!root) return;
      var g = root.querySelector('.sg-lights'); if (!g) return;
      var R = c.rand || Math.random, W = [], B = [], cols = ['', '', '', 'var(--sg-c2)', '', 'var(--sg-c3)'];
      var CH = 6.6;                                                   // when the chase begins
      function bulb(x, y, t, s, k) {
        var sz = 9 * (s || 1);
        B.push('<use class="sg-b" href="#shaadi-ghar-bulb" x="' + f(x - sz / 2) + '" y="' + f(y - sz / 2) + '" width="' + f(sz) +
          '" height="' + f(sz) + '" style="--t:' + f(t) + 's;--c:' + f(CH + (k % 6) * .15 + R() * .05) + 's' +
          (cols[k % 6] ? ';--bc:' + cols[k % 6] : '') + '"/>');
      }
      function wire(d, t, dur) {
        W.push('<path class="sg-wr" pathLength="1" d="' + d + '" style="--t:' + f(t) + 's;--w:' + f(dur) + 's"/>');
      }
      // catenary swag between two points, bulbs lit in order from 'from' end
      function swag(x1, y1, x2, y2, sag, n, t0, dt, rev, s) {
        wire('M' + x1 + ' ' + y1 + 'Q' + f((x1 + x2) / 2) + ' ' + f((y1 + y2) / 2 + 2 * sag) + ' ' + x2 + ' ' + y2, t0, n * dt + .1);
        for (var i = 0; i <= n; i++) {
          var u = i / n, x = x1 + (x2 - x1) * u, y = y1 + (y2 - y1) * u + 4 * sag * u * (1 - u);
          bulb(x, y, t0 + (rev ? n - i : i) * dt, s, i);
        }
      }
      function bez(p0, p1, p2, p3, u) { var v = 1 - u; return v * v * v * p0 + 3 * v * v * u * p1 + 3 * v * u * u * p2 + u * u * u * p3; }

      // 1. roofline swags of the wedding house - the moment the switch clicks
      swag(112, 384, 157, 384, 4, 6, 2.85, .03, false, 1);
      swag(157, 384, 203, 384, 4, 6, 3.0, .03, false, 1);
      swag(203, 384, 248, 384, 4, 6, 3.15, .03, false, 1);
      // 2. waterfall strands tumbling down the facade
      var xs = [116, 129, 142, 154, 166, 194, 206, 218, 231, 244];
      var ends = [624, 600, 610, 552, 552, 552, 552, 610, 600, 624];
      for (var s = 0; s < xs.length; s++) {
        var x0 = xs[s], y0 = 386, y3 = ends[s], a = (s % 2 ? 3 : -3), x3 = x0 + (s < 5 ? -2 : 2);
        var st = 3.25 + Math.abs(s - 4.5) * .11, n = Math.round((y3 - y0) / 15), dt = .075;
        wire('M' + x0 + ' ' + y0 + 'C' + (x0 + a) + ' ' + f(y0 + (y3 - y0) / 3) + ' ' + (x0 - a) + ' ' + f(y0 + 2 * (y3 - y0) / 3) + ' ' + x3 + ' ' + y3, st, n * dt + .15);
        for (var i = 1; i <= n; i++) {
          var u = i / n;
          bulb(bez(x0, x0 + a, x0 - a, x3, u), bez(y0, y0 + (y3 - y0) / 3, y0 + 2 * (y3 - y0) / 3, y3, u), st + i * dt, .9, i + s);
        }
      }
      // 3. neighbours light up, spreading outward along the street
      swag(112, 450, 58, 450, 4, 6, 4.95, .035, false, .9);
      swag(58, 450, -4, 450, 4, 7, 5.18, .035, false, .9);
      swag(248, 432, 304, 432, 4, 6, 5.05, .035, false, .9);
      swag(304, 432, 364, 432, 4, 7, 5.28, .035, false, .9);
      swag(222, 398, 292, 398, 3, 7, 5.5, .03, true, .75);
      swag(34, 407, 112, 384, 3, 7, 5.45, .03, true, .75);
      // minaret: lights climb up the shaft
      for (var m = 0; m < 9; m++) bulb(304, 396 - m * 17.5, 5.55 + m * .07, .7, m);
      bulb(304, 202, 6.25, 1.1, 3);
      // 4. ring of lights framing the initials, with drops to the roof corners
      var cx = 180, cy = 240, rx = 82, ry = 62, N = 34;
      W.push('<ellipse class="sg-wr" pathLength="1" cx="' + cx + '" cy="' + cy + '" rx="' + rx + '" ry="' + ry + '" style="--t:5.7s;--w:1.2s"/>');
      for (var k = 0; k < N; k++) {
        var th = Math.PI / 2 + k / N * Math.PI * 2;                  // start at the bottom, travel round
        bulb(cx + rx * Math.cos(th), cy + ry * Math.sin(th), 5.75 + k * .034, 1, k);
      }
      swag(cx - rx * .78, cy + ry * .63, 120, 352, 3, 5, 6.0, .05, true, .8);
      swag(cx + rx * .78, cy + ry * .63, 240, 352, 3, 5, 6.0, .05, true, .8);
      g.innerHTML = W.join('') + B.join('');
    }
  };
})();
