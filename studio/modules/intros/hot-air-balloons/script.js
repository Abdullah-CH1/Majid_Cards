/* Hot Air Balloons: builds the valley ridges with fairy-chimney rocks (fixed, deterministic shapes). */
(function () {
  function f(n) { return n.toFixed(2); }
  function layer(base, amp, ph, fr, rocks) {
    function y(x) { return base + amp * (Math.sin(x * fr + ph) * .6 + Math.sin(x * fr * 2.3 + ph * 1.7) * .3 + Math.sin(x * fr * 5.1 + ph * .6) * .1); }
    var d = 'M0 60L0 ' + f(y(0));
    for (var x = 2; x <= 100; x += 2) d += 'L' + x + ' ' + f(y(x));
    d += 'L100 60Z';
    rocks.forEach(function (r) {
      var cx = r[0], h = r[1], w = r[2], yb = y(cx) + 1.2, t = yb - h;
      d += 'M' + f(cx - w) + ' ' + f(yb) + 'C' + f(cx - w * .55) + ' ' + f(yb - h * .35) + ' ' + f(cx - w * .42) + ' ' + f(t + h * .2) + ' ' + f(cx - w * .36) + ' ' + f(t) +
        'Q' + f(cx - w * .5) + ' ' + f(t - w * .25) + ' ' + f(cx) + ' ' + f(t - w * .62) + 'Q' + f(cx + w * .5) + ' ' + f(t - w * .25) + ' ' + f(cx + w * .36) + ' ' + f(t) +
        'C' + f(cx + w * .42) + ' ' + f(t + h * .2) + ' ' + f(cx + w * .55) + ' ' + f(yb - h * .35) + ' ' + f(cx + w) + ' ' + f(yb) + 'Z';
    });
    return d;
  }
  var D = [
    layer(20, 2.2, .4, .07, [[14, 3, 1.4], [17, 2.2, 1.1], [61, 2.6, 1.3], [64, 3.6, 1.5], [88, 2.4, 1.2]]),
    layer(30, 2.6, 2.1, .09, [[6, 6, 2.2], [10.5, 4.2, 1.8], [36, 3.4, 1.6], [72, 5.5, 2.1], [76.5, 7.5, 2.4], [81, 4.4, 1.8], [95, 5, 2]]),
    layer(42, 2.4, 4.0, .08, [[-1, 13, 4.2], [5.5, 9, 3.4], [11, 5.5, 2.6], [87, 7, 3], [93, 12, 4], [100, 9, 3.4]])
  ];
  WIS.ix['hot-air-balloons'] = { update: function (c) {
    var root = c.S.querySelector('.ix-hot-air-balloons'); if (!root) return;
    for (var i = 0; i < 3; i++) { var p = root.querySelector('.hb-p' + (i + 1)); if (p) p.setAttribute('d', D[i]); }
  } };
})();
