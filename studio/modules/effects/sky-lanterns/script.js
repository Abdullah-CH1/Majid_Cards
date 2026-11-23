/* Sky lanterns: tiny paper lanterns lit from inside, with a flickering halo, rising slowly from the bottom and
   shrinking and fading as they drift away into the distance. */
(function () {
  function shuffle(a, R) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(R() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function strat(n, R) { var a = []; for (var i = 0; i < n; i++) a.push((i + .15 + R() * .7) / n); return shuffle(a, R); }
  function edge(u, k) { var d = 2 * u - 1; return .5 + .5 * (d < 0 ? -1 : 1) * Math.pow(Math.abs(d), k); }
  function f(x) { return x.toFixed(2); }
  function stop(o, col) { return '<stop offset="' + o + '" style="stop-color:' + col + '"/>'; }
  function st(o, col, a) { return '<stop offset="' + o + '" stop-color="' + col + '" stop-opacity="' + a + '"/>'; }

  var BODY = 'M4.6 3.6C8.4 1.4 15.6 1.4 19.4 3.6L17.2 26.8C14.2 28.2 9.8 28.2 6.8 26.8Z';
  var DK = 'color-mix(in srgb,var(--acc) 60%,#000)';
  var ART =
    '<path d="' + BODY + '" fill="url(#sky-lanterns-fx-b)"/>' +
    '<path d="' + BODY + '" fill="url(#sky-lanterns-fx-s)"/>' +
    '<path d="' + BODY + '" fill="url(#sky-lanterns-fx-i)"/>' +
    '<path d="M9.4 2.4C9.1 10 9.4 19 10.1 27.7M14.6 2.4C14.9 10 14.6 19 13.9 27.7" fill="none" stroke="#000" stroke-opacity=".12" stroke-width=".4"/>' +
    '<path d="M4.6 3.6C8.4 1.4 15.6 1.4 19.4 3.6" fill="none" style="stroke:' + DK + '" stroke-opacity=".45" stroke-width=".5" stroke-linecap="round"/>' +
    '<path d="M6.8 26.8C9.8 28.2 14.2 28.2 17.2 26.8" fill="none" style="stroke:' + DK + '" stroke-width=".75" stroke-linecap="round"/>' +
    '<path d="M7.6 27.4L12 30.1L16.4 27.4" fill="none" style="stroke:' + DK + '" stroke-opacity=".55" stroke-width=".35"/>' +
    '<ellipse cx="12" cy="30.5" rx="1.25" ry="1.75" style="fill:color-mix(in srgb,var(--acc) 40%,#fff)"/>' +
    '<ellipse cx="12" cy="30.8" rx=".55" ry=".85" fill="#fff"/>';
  var DEFS = '<svg class="sky-lanterns-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>' +
    '<linearGradient id="sky-lanterns-fx-b" x1="0" y1="0" x2="0" y2="1">' +
      stop(0, 'color-mix(in srgb,var(--acc) 55%,var(--bl))') + stop(.5, 'color-mix(in srgb,var(--acc) 85%,var(--bl))') +
      stop(1, 'color-mix(in srgb,var(--acc) 45%,#fff)') + '</linearGradient>' +
    '<linearGradient id="sky-lanterns-fx-s" x1="0" y1="0" x2="1" y2="0">' + st(0, '#000', .22) + st(.32, '#000', 0) + st(.68, '#000', 0) + st(1, '#000', .22) + '</linearGradient>' +
    '<radialGradient id="sky-lanterns-fx-i" cx=".5" cy=".95" r=".75">' + st(0, '#fff', .6) + st(.55, '#fff', .12) + st(1, '#fff', 0) + '</radialGradient>' +
    '</defs></svg>';

  WIS.fx['sky-lanterns'] = function (box, c) {
    var R = c.rand, N = 13, out = [DEFS];
    var xs = strat(N, R), ds = strat(N, R), zs = strat(N, R);
    for (var i = 0; i < N; i++) {
      var z = zs[i], s = 3.1 + z * 2.4;
      var dur = 15 - z * 3 + R() * 1.5, a = .75 + z * .23;
      var x = 6 + edge(xs[i], .75) * 88, del = c.t0 + .3 + ds[i] * 7.5;
      out.push('<i class="sky-lanterns-p" style="left:' + f(x) + '%;--s:' + f(s) + 'cqw;--a:' + f(a) + ';--sc:' + f(.42 + R() * .16) +
        ';--y1:' + f(8 + R() * 36) + 'cqw;--dx:' + f((R() * 2 - 1) * 6) + 'cqw;animation-duration:' + f(dur) + 's;animation-delay:' + f(del) + 's">' +
        '<i class="sky-lanterns-q" style="--sw:' + f(.8 + R() * 1.4) + 'cqw;--rz:' + f(2 + R() * 4) + 'deg;animation-duration:' + f(3.2 + R() * 1.8) +
        's;animation-delay:-' + f(R() * 4) + 's">' +
        '<i class="sky-lanterns-h" style="animation-duration:' + f(1.6 + R() * 1.2) + 's;animation-delay:-' + f(R() * 2) + 's"></i>' +
        '<svg viewBox="0 0 24 34" aria-hidden="true" focusable="false">' + ART + '</svg></i></i>');
    }
    box.insertAdjacentHTML('beforeend', out.join(''));
  };
})();
