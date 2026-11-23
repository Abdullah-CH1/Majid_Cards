/* Floating hearts: rose (--bl) and gold (--acc) hearts, plus a few hairline gold outlines, rising from the
   bottom. Size = depth: small hearts are far away, so they rise slower and are fainter. */
(function () {
  function shuffle(a, R) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(R() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  // n values spread evenly over 0..1 (one per slot, jittered) in random order: even coverage, no clumps
  function strat(n, R) { var a = []; for (var i = 0; i < n; i++) a.push((i + .15 + R() * .7) / n); return shuffle(a, R); }
  // fewer particles in the middle of the card, where the names are
  function edge(u, k) { var d = 2 * u - 1; return .5 + .5 * (d < 0 ? -1 : 1) * Math.pow(Math.abs(d), k); }
  function f(x) { return x.toFixed(2); }
  function stop(o, col) { return '<stop offset="' + o + '" style="stop-color:' + col + '"/>'; }

  var H = 'M16 28.6C10.4 24.6 1.6 18.3 1.6 10.1C1.6 5.3 5.2 1.6 9.6 1.6C12.3 1.6 14.6 3 16 5.2' +
          'C17.4 3 19.7 1.6 22.4 1.6C26.8 1.6 30.4 5.3 30.4 10.1C30.4 18.3 21.6 24.6 16 28.6Z';
  var GLOSS = '<path d="M6.3 7.6C7.1 5.5 9.4 4.4 11.5 5.1" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="1.5" stroke-linecap="round"/>';
  var ART = {
    b: '<path d="' + H + '" fill="url(#hearts-fx-b)"/>' + GLOSS,
    g: '<path d="' + H + '" fill="url(#hearts-fx-g)"/>' + GLOSS,
    o: '<path d="' + H + '" style="fill:color-mix(in srgb,var(--acc) 16%,transparent);stroke:var(--acc)" stroke-width="1.5" stroke-linejoin="round"/>'
  };
  var DEFS = '<svg class="hearts-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>' +
    '<radialGradient id="hearts-fx-b" cx=".34" cy=".3" r=".8">' +
      stop(0, 'color-mix(in srgb,var(--bl) 50%,#fff)') + stop(.48, 'var(--bl)') + stop(1, 'color-mix(in srgb,var(--bl) 68%,#000)') +
    '</radialGradient>' +
    '<linearGradient id="hearts-fx-g" x1="0" y1="0" x2="1" y2="1">' +
      stop(0, 'color-mix(in srgb,var(--acc) 40%,#fff)') + stop(.32, 'var(--acc)') + stop(.52, 'color-mix(in srgb,var(--acc) 55%,#fff)') +
      stop(.72, 'var(--acc)') + stop(1, 'color-mix(in srgb,var(--acc) 62%,#000)') +
    '</linearGradient></defs></svg>';

  WIS.fx['hearts'] = function (box, c) {
    var R = c.rand, N = 16, out = [DEFS];
    var xs = strat(N, R), ds = strat(N, R), zs = strat(N, R);
    var kinds = shuffle('bbbbbbbggggggooo'.split(''), R);
    for (var i = 0; i < N; i++) {
      var z = zs[i], s = 2.4 + z * 2.7;
      var dur = 13.6 - z * 3.6 + R() * 1.2, a = .52 + z * .4;
      var x = 5 + edge(xs[i], .8) * 90, del = c.t0 + .3 + ds[i] * 7;
      out.push('<i class="hearts-p" style="left:' + f(x) + '%;--s:' + f(s) + 'cqw;--a:' + f(a) +
        ';animation-duration:' + f(dur) + 's;animation-delay:' + f(del) + 's">' +
        '<i class="hearts-q" style="--sw:' + f(1.2 + R() * 2.2) + 'cqw;--rz:' + f(5 + R() * 9) + 'deg;--ry:' + f(14 + R() * 26) +
        'deg;animation-duration:' + f(2.3 + R() * 1.5) + 's;animation-delay:-' + f(R() * 3) + 's">' +
        '<svg viewBox="0 0 32 30" aria-hidden="true" focusable="false">' + ART[kinds[i]] + '</svg></i></i>');
    }
    box.insertAdjacentHTML('beforeend', out.join(''));
  };
})();
