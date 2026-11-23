/* Marigold flowers (genda): small ruffled marigold pom-poms in orange and golden yellow, with a few loose
   petals, tumbling down. Colours are mixed from the palette gold (--acc) and flower colour (--bl). */
(function () {
  function shuffle(a, R) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(R() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function strat(n, R) { var a = []; for (var i = 0; i < n; i++) a.push((i + .15 + R() * .7) / n); return shuffle(a, R); }
  function edge(u, k) { var d = 2 * u - 1; return .5 + .5 * (d < 0 ? -1 : 1) * Math.pow(Math.abs(d), k); }
  function f(x) { return x.toFixed(2); }
  function xy(r, a) { return (r * Math.cos(a)).toFixed(2) + ' ' + (r * Math.sin(a)).toFixed(2); }

  // One row of ruffled petals: k frills bulging out to ~R from valleys at R-d, each frill a little different.
  function row(R, d, k, ph) {
    var st = 2 * Math.PI / k, rv = R - d, p = '';
    for (var i = 0; i < k; i++) {
      var a0 = ph + i * st, a1 = a0 + st;
      var Ri = R * (1 + .035 * Math.sin(i * 2.39 + ph * 7.3)) * (i % 2 ? .97 : 1);
      var rc = (Ri - .25 * rv * Math.cos(st / 2)) / (.75 * Math.cos(.3 * st));
      if (!i) p += 'M' + xy(rv, a0);
      p += 'C' + xy(rc, a0 + st * .22) + ' ' + xy(rc, a0 + st * .78) + ' ' + xy(rv, a1);
    }
    return p + 'Z';
  }
  // rows of ruffles from the outside in; alternating shades read as packed, crinkled petals
  var ROWS = [[19, 2.4, 21, 0, 4], [17, 2.3, 19, .17, 3], [14.9, 2.2, 17, .05, 2], [12.8, 2.1, 15, .29, 3],
              [10.6, 2, 13, .11, 1], [8.4, 1.9, 11, .37, 2], [6.2, 1.7, 9, .19, 0], [4, 1.4, 7, .43, 1], [2, 1, 5, .1, 3]];
  var BLOOM = '';
  ROWS.forEach(function (r) {
    BLOOM += '<path d="' + row(r[0], r[1], r[2], r[3]) + '" style="fill:var(--mg' + r[4] + ');stroke:var(--mg5)" stroke-width=".45" stroke-opacity=".32" stroke-linejoin="round"/>';
  });
  var PETAL = 'M0 5.5C-2.2 4-4.6.8-5-2.2C-4.4-3.2-3.6-3.4-3-2.8C-2.6-3.9-1.6-4.4-.8-3.8C-.2-4.6 1-4.6 1.4-3.8' +
              'C2.2-4.3 3.2-3.8 3.4-2.8C4-3.3 4.9-2.8 5-2C4.6 1 2.2 4 0 5.5Z';
  var LOOSE = '<path d="' + PETAL + '" style="fill:var(--mg2);stroke:var(--mg5)" stroke-width=".35" stroke-opacity=".4" stroke-linejoin="round"/>' +
              '<path d="' + PETAL + '" fill="url(#marigold-fx-lp)"/>' +
              '<path d="M0 4.6C-.1 1.6 0-1 .2-3.2M-.6 4C-1.6 1.8-2.4-.4-2.6-2M.6 4C1.6 1.8 2.4-.2 2.8-1.8" fill="none" style="stroke:var(--mg5)" stroke-width=".3" stroke-opacity=".35" stroke-linecap="round"/>';
  var DEFS = '<svg class="marigold-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>' +
    '<radialGradient id="marigold-fx-sph" cx=".38" cy=".32" r=".72">' +
      '<stop offset="0" stop-color="#fff" stop-opacity=".42"/><stop offset=".42" stop-color="#fff" stop-opacity="0"/>' +
      '<stop offset=".66" stop-color="#000" stop-opacity="0"/><stop offset=".9" stop-color="#000" stop-opacity=".26"/>' +
      '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>' +
    '<linearGradient id="marigold-fx-lp" x1="0" y1="0" x2="0" y2="1">' +
      '<stop offset="0" stop-color="#fff" stop-opacity=".28"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/>' +
      '<stop offset="1" stop-color="#000" stop-opacity=".22"/></linearGradient>' +
    '<symbol id="marigold-fx-b" viewBox="-20 -20 40 40">' + BLOOM + '</symbol>' +
    '<symbol id="marigold-fx-l" viewBox="-6 -6 12 12">' + LOOSE + '</symbol></defs></svg>';
  var SHADE = '<svg class="marigold-sh" viewBox="-20 -20 40 40" aria-hidden="true" focusable="false"><circle r="17.8" fill="url(#marigold-fx-sph)"/></svg>';

  WIS.fx['marigold'] = function (box, c) {
    var R = c.rand, N = 16, out = [DEFS];
    var xs = strat(N, R), ds = strat(N, R), zs = strat(N, R);
    var kinds = shuffle('oooooooyyyyyllll'.split(''), R);   // orange bloom, yellow bloom, loose petal
    for (var i = 0; i < N; i++) {
      var k = kinds[i], z = zs[i], loose = k === 'l';
      var s = loose ? 2 + z * 1 : 3.8 + z * 2.3;
      var dur = 12.4 - z * 2.8 + R() * 1.2, a = .8 + z * .18;
      var x = 5 + edge(xs[i], .85) * 90, del = c.t0 + .3 + ds[i] * 7;
      var inner = loose
        ? '<i class="marigold-r marigold-f" style="--ax:' + f(.4 + R() * .6) + ';--ay:' + f(R() * .8 - .4) + ';--r0:' + f(R() * 360) +
          'deg;animation-duration:' + f(2.2 + R() * 1.6) + 's;animation-delay:-' + f(R() * 3) + 's"><svg viewBox="0 0 12 12" aria-hidden="true" focusable="false"><use href="#marigold-fx-l"/></svg></i>'
        : '<i class="marigold-r" style="animation-duration:' + f(6 + R() * 5) + 's;animation-delay:-' + f(R() * 10) + 's' +
          (R() < .5 ? ';animation-direction:reverse' : '') + '"><svg viewBox="0 0 40 40" aria-hidden="true" focusable="false"><use href="#marigold-fx-b"/></svg></i>' + SHADE;
      out.push('<i class="marigold-p' + (k === 'y' ? ' marigold-y' : '') + '" style="left:' + f(x) + '%;--s:' + f(s) +
        'cqw;--a:' + f(a) + ';animation-duration:' + f(dur) + 's;animation-delay:' + f(del) + 's">' +
        '<i class="marigold-q" style="--sw:' + f(1.4 + R() * 2.6) + 'cqw;--tx:' + f(10 + R() * 18) + 'deg;--ty:' + f(8 + R() * 16) +
        'deg;animation-duration:' + f(2.6 + R() * 1.6) + 's;animation-delay:-' + f(R() * 3) + 's">' + inner + '</i></i>');
    }
    box.insertAdjacentHTML('beforeend', out.join(''));
  };
})();
