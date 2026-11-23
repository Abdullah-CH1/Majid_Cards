/* Constellation: builds the chart ticks, background stars and the heart constellation (deterministic per update). */
(function () {
  function f(n) { return n.toFixed(2); }
  WIS.ix['constellation'] = { update: function (c) {
    var root = c.S.querySelector('.ix-constellation'); if (!root) return;
    var q = function (s) { return root.querySelector(s); };
    var g, h, i, a, r, x, y;
    g = q('.cn-ticks'); if (g) { h = [];
      for (i = 0; i < 72; i++) { a = i * 5 * Math.PI / 180; var big = i % 6 === 0, r1 = 91, r2 = big ? 97 : 94;
        h.push('<line class="' + (big ? 'cn-tk cn-tb' : 'cn-tk') + '" style="--i:' + i + '" x1="' + f(Math.cos(a) * r1) + '" y1="' + f(Math.sin(a) * r1) + '" x2="' + f(Math.cos(a) * r2) + '" y2="' + f(Math.sin(a) * r2) + '"/>'); }
      g.innerHTML = h.join(''); }
    g = q('.cn-rad'); if (g) { h = [];
      for (i = 0; i < 12; i++) { a = i * 30 * Math.PI / 180;
        h.push('<line pathLength="1" style="--i:' + i + '" x1="' + f(Math.cos(a) * 12) + '" y1="' + f(Math.sin(a) * 12) + '" x2="' + f(Math.cos(a) * 91) + '" y2="' + f(Math.sin(a) * 91) + '"/>'); }
      g.innerHTML = h.join(''); }
    g = q('.cn-bg'); if (g) { h = [];
      for (i = 0; i < 70; i++) { a = c.rand() * Math.PI * 2; r = 8 + Math.sqrt(c.rand()) * 80;
        x = Math.cos(a) * r; y = Math.sin(a) * r; var s = c.rand(), rad = s > .9 ? 1.1 : s > .6 ? .7 : .42;
        h.push('<circle class="cn-st" cx="' + f(x) + '" cy="' + f(y) + '" r="' + rad + '" style="--d:' + f(.2 + c.rand() * 2.4) + 's;--w:' + f(2 + c.rand() * 3) + 's"/>'); }
      g.innerHTML = h.join(''); }
    g = q('.cn-faint'); if (g) {
      var cons = [[[-70, -40], [-58, -52], [-46, -48], [-38, -58], [-24, -54]], [[48, 40], [60, 30], [72, 40], [64, 56], [50, 54], [48, 40]], [[-62, 42], [-52, 58], [-40, 50], [-30, 66]], [[30, -72], [42, -60], [56, -66], [66, -54]]];
      h = [];
      cons.forEach(function (p, k) { h.push('<polyline pathLength="1" style="--i:' + k + '" points="' + p.map(function (v) { return v.join(','); }).join(' ') + '"/>');
        p.forEach(function (v) { h.push('<circle class="cn-fs" cx="' + v[0] + '" cy="' + v[1] + '" r=".9" style="--i:' + k + '"/>'); }); });
      g.innerHTML = h.join(''); }
    g = q('.cn-heart'); if (g) {
      var N = 14, pts = [], sc = 3.1;
      for (i = 0; i < N; i++) { var t = i / N * Math.PI * 2;
        x = 16 * Math.pow(Math.sin(t), 3); y = -(13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t));
        pts.push([x * sc + (c.rand() - .5) * 3, y * sc - 6 + (c.rand() - .5) * 3]); }
      h = [];
      for (i = 0; i < N; i++) { var p = pts[i], n = pts[(i + 1) % N];
        h.push('<line class="cn-hl" pathLength="1" style="--i:' + i + '" x1="' + f(p[0]) + '" y1="' + f(p[1]) + '" x2="' + f(n[0]) + '" y2="' + f(n[1]) + '"/>'); }
      for (i = 0; i < N; i++) { var big2 = i === 0 || i === 4 || i === 10;
        h.push('<g class="cn-hs" style="--i:' + i + '" transform="translate(' + f(pts[i][0]) + ' ' + f(pts[i][1]) + ')"><circle class="cn-hg" r="' + (big2 ? 5 : 3.4) + '"/><circle class="cn-hd" r="' + (big2 ? 1.9 : 1.3) + '"/>' + (big2 ? '<path class="cn-hx" d="M-6 0H6M0-6V6"/>' : '') + '</g>'); }
      g.innerHTML = h.join(''); }
  } };
})();
