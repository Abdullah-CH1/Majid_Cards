/* Fireflies: warm glowing points of light that blink on across the card, drift and rise slowly while their
   glow pulses, then fade away. Pure radial-gradient glows (no blur filters). */
(function () {
  function shuffle(a, R) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(R() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function strat(n, R) { var a = []; for (var i = 0; i < n; i++) a.push((i + .15 + R() * .7) / n); return shuffle(a, R); }
  function f(x) { return x.toFixed(2); }

  WIS.fx['fireflies'] = function (box, c) {
    var R = c.rand, N = 18, out = [];
    var xs = strat(N, R), ys = strat(N, R), ds = strat(N, R), zs = strat(N, R);
    for (var i = 0; i < N; i++) {
      var z = zs[i], g = 3.4 + z * 3.4;                          // glow diameter in cqw; bigger = nearer
      var dur = 8 + R() * 4.5, rise = 16 + R() * 30, dx = (R() * 2 - 1) * 7;
      out.push('<i class="fireflies-p' + (R() < .3 ? ' fireflies-w' : '') + '" style="left:' + f(4 + xs[i] * 92) + '%;top:' + f(24 + ys[i] * 74) +
        '%;--g:' + f(g) + 'cqw;--a:' + f(.6 + z * .38) + ';--rise:' + f(-rise) + 'cqw;--dx:' + f(dx) + 'cqw;animation-duration:' + f(dur) +
        's;animation-delay:' + f(c.t0 + .2 + ds[i] * 6) + 's">' +
        '<i class="fireflies-q" style="--wx:' + f(1 + R() * 2.4) + 'cqw;--wy:' + f(R() * 3 - 1.5) + 'cqw;animation-duration:' + f(2.4 + R() * 2.2) +
        's;animation-delay:-' + f(R() * 4) + 's">' +
        '<i class="fireflies-r" style="animation-duration:' + f(1.3 + R() * 1.7) + 's;animation-delay:-' + f(R() * 3) + 's"></i></i></i>');
    }
    box.insertAdjacentHTML('beforeend', out.join(''));
  };
})();
