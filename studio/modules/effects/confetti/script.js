/* Gold confetti: metallic gold foil strips, sequins and squares with a few palette-coloured pieces, tumbling
   down with a real 3D flip (rotate3d about a random axis) and a glint each time a face turns to the light. */
(function () {
  function shuffle(a, R) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(R() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function strat(n, R) { var a = []; for (var i = 0; i < n; i++) a.push((i + .15 + R() * .7) / n); return shuffle(a, R); }
  function f(x) { return x.toFixed(2); }

  WIS.fx['confetti'] = function (box, c) {
    var R = c.rand, N = 20, out = [];
    var xs = strat(N, R), ds = strat(N, R), zs = strat(N, R);
    var shapes = shuffle('ssssssssssooooottttt'.split(''), R);           // strip, round sequin, square
    var cols = shuffle(['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'bl', 'bl', 'bl', 'p2', 'p2', 'lv', 'lv', 'ink2'], R);
    for (var i = 0; i < N; i++) {
      var sh = shapes[i], z = zs[i], k = 1 + z * .45, w, h;
      if (sh === 's') { w = (.8 + R() * .3) * k; h = w * (2.2 + R() * .5); }
      else if (sh === 'o') { w = h = (1.15 + R() * .3) * k; }
      else { w = h = (1 + R() * .3) * k; }
      var gold = cols[i] === 'g';
      var dur = 10.5 - z * 2.5 + R() * 1.2, del = c.t0 + .2 + ds[i] * 6.5, a = .78 + z * .2;
      var ax = R() * 2 - 1, ay = R() * 2 - 1, az = R() * .5 - .25;
      if (Math.abs(ax) + Math.abs(ay) < .5) ax = ax < 0 ? -.8 : .8;
      out.push('<i class="confetti-p" style="left:' + f(3 + xs[i] * 94) + '%;--w:' + f(w) + 'cqw;--h:' + f(h) + 'cqw;--a:' + f(a) +
        ';--rot:' + f((R() < .5 ? -1 : 1) * (90 + R() * 200)) + 'deg;animation-duration:' + f(dur) + 's;animation-delay:' + f(del) + 's">' +
        '<i class="confetti-q" style="--sw:' + f(1.2 + R() * 2.6) + 'cqw;--rz:' + f(8 + R() * 22) + 'deg;animation-duration:' + f(1.7 + R() * 1.3) +
        's;animation-delay:-' + f(R() * 3) + 's">' +
        '<i class="confetti-r confetti-' + sh + (gold ? ' confetti-g' : ' confetti-k') + '" style="' + (gold ? '' : '--k:var(--' + cols[i] + ');') +
        '--ax:' + f(ax) + ';--ay:' + f(ay) + ';--az:' + f(az) + ';--f:' + f(1.4 + R() * 1.4) + 's;--fp:-' + f(R() * 3) + 's"></i></i></i>');
    }
    box.insertAdjacentHTML('beforeend', out.join(''));
  };
})();
