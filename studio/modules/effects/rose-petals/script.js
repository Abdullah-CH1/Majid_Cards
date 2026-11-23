/* Rose petals: curled rose petals in three shapes (broad, rolled-edge, narrow) and three shades of --bl, shaded
   with neutral light/shadow gradients so the base colour can vary per petal. They fall with a lateral drift and
   flutter: some flip right over, others rock from side to side. */
(function () {
  function shuffle(a, R) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(R() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function strat(n, R) { var a = []; for (var i = 0; i < n; i++) a.push((i + .15 + R() * .7) / n); return shuffle(a, R); }
  function edge(u, k) { var d = 2 * u - 1; return .5 + .5 * (d < 0 ? -1 : 1) * Math.pow(Math.abs(d), k); }
  function f(x) { return x.toFixed(2); }
  function st(o, col, a) { return '<stop offset="' + o + '" stop-color="' + col + '" stop-opacity="' + a + '"/>'; }

  var SHAPES = [
    { d: 'M20 42.6C10.6 39 3.2 30.2 2.6 19.6C2.1 10.8 7.6 3.6 14.6 3C17.2 2.8 19 3.9 20.2 5.4C21.6 3.8 23.6 2.7 26.2 3C33 3.8 38.2 11 37.6 19.8C37 30.2 29.6 39 20 42.6Z',
      v: 'M20 40.6C19.3 31 19.5 18.5 20.3 7.4' },
    { d: 'M18.5 42.4C9.6 37.6 3.4 28.4 4.4 17.6C5.2 9 11.4 3.2 19.4 3.2C27.8 3.2 34.6 8.8 35.6 16.8C36.8 27.6 28.6 37.8 18.5 42.4Z',
      v: 'M18.6 40.4C17.8 30 18.4 17 19.8 5.6',
      lip: 'M35.6 16.8C34.6 8.8 27.8 3.2 19.4 3.2C26.4 5.4 31.6 10.4 32.6 17.6C33.2 22 32.2 26.4 30.2 29.8C33.8 26.6 36.2 21.8 35.6 16.8Z' },
    { d: 'M20 43C13.4 38.6 8.4 29.6 8.8 19.4C9.2 10.4 14 4.2 20 3.4C26 4.2 30.8 10.4 31.2 19.4C31.6 29.6 26.6 38.6 20 43Z',
      v: 'M20 41C19.6 31 19.8 18 20 6' }
  ];
  function art(sh) {
    return '<path d="' + sh.d + '" style="fill:var(--rp);stroke:color-mix(in srgb,var(--rp) 62%,#000)" stroke-width=".5" stroke-opacity=".5" stroke-linejoin="round"/>' +
      '<path d="' + sh.d + '" fill="url(#rose-petals-fx-s)"/>' +
      '<path d="' + sh.d + '" fill="url(#rose-petals-fx-h)"/>' +
      '<path d="' + sh.d + '" fill="url(#rose-petals-fx-c)"/>' +
      '<path d="' + sh.v + '" fill="none" stroke="#000" stroke-opacity=".13" stroke-width=".7" stroke-linecap="round"/>' +
      (sh.lip ? '<path d="' + sh.lip + '" fill="url(#rose-petals-fx-l)"/><path d="M32.6 17.6C33.2 22 32.2 26.4 30.2 29.8" fill="none" stroke="#000" stroke-opacity=".18" stroke-width=".6" stroke-linecap="round"/>' : '');
  }
  var DEFS = '<svg class="rose-petals-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>' +
    // deeper colour where the petal joined the flower
    '<radialGradient id="rose-petals-fx-s" cx=".5" cy="1" r=".9">' + st(0, '#000', .42) + st(.45, '#000', .12) + st(1, '#000', 0) + '</radialGradient>' +
    // light falling on the upper rim
    '<radialGradient id="rose-petals-fx-h" cx=".4" cy=".16" r=".62">' + st(0, '#fff', .4) + st(1, '#fff', 0) + '</radialGradient>' +
    // the petal is cupped: one side turns away from the light
    '<linearGradient id="rose-petals-fx-c" x1="0" y1="0" x2="1" y2="0">' + st(0, '#000', .2) + st(.34, '#000', 0) + st(.72, '#fff', 0) + st(1, '#fff', .14) + '</linearGradient>' +
    '<linearGradient id="rose-petals-fx-l" x1="0" y1="0" x2="1" y2="1">' + st(0, '#fff', .5) + st(1, '#fff', .06) + '</linearGradient>' +
    '</defs></svg>';
  var TONES = ['var(--bl)', 'color-mix(in srgb,var(--bl) 84%,#fff)', 'color-mix(in srgb,var(--bl) 80%,#000)'];

  WIS.fx['rose-petals'] = function (box, c) {
    var R = c.rand, N = 16, out = [DEFS];
    var xs = strat(N, R), ds = strat(N, R), zs = strat(N, R);
    var shapes = shuffle([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2], R);
    for (var i = 0; i < N; i++) {
      var z = zs[i], s = 2.9 + z * 2.4, flip = R() < .5;
      var dur = 12 - z * 2.8 + R() * 1.2, a = .84 + z * .14;
      var x = 5 + edge(xs[i], .85) * 90, del = c.t0 + .3 + ds[i] * 7;
      out.push('<i class="rose-petals-p" style="left:' + f(x) + '%;--s:' + f(s) + 'cqw;--a:' + f(a) + ';--rp:' + TONES[Math.floor(R() * 3)] +
        ';animation-duration:' + f(dur) + 's;animation-delay:' + f(del) + 's">' +
        '<i class="rose-petals-q" style="--sw:' + f(2 + R() * 3.2) + 'cqw;--rz:' + f(10 + R() * 18) + 'deg;animation-duration:' + f(2.8 + R() * 1.4) +
        's;animation-delay:-' + f(R() * 4) + 's">' +
        '<i class="rose-petals-r' + (flip ? '' : ' rose-petals-k') + '" style="--r0:' + f(R() * 360) + 'deg;--ax:' + f(.3 + R() * .7) + ';--ay:' + f(R() * 1.2 - .6) +
        ';--ry:' + f(45 + R() * 30) + 'deg;--rx:' + f(8 + R() * 14) + 'deg;animation-duration:' + f(flip ? 2.8 + R() * 2.2 : 1.6 + R() * .9) +
        's;animation-delay:-' + f(R() * 4) + 's"><svg viewBox="0 0 40 44" aria-hidden="true" focusable="false">' + art(SHAPES[shapes[i]]) + '</svg></i></i></i>');
    }
    box.insertAdjacentHTML('beforeend', out.join(''));
  };
})();
