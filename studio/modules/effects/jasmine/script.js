/* Jasmine flowers (motia): tiny white five-petal flowers and a few closed buds, as in a gajra, drifting down
   softly with a falling-leaf pendulum sway while they slowly turn. */
(function () {
  function shuffle(a, R) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(R() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function strat(n, R) { var a = []; for (var i = 0; i < n; i++) a.push((i + .15 + R() * .7) / n); return shuffle(a, R); }
  function edge(u, k) { var d = 2 * u - 1; return .5 + .5 * (d < 0 ? -1 : 1) * Math.pow(Math.abs(d), k); }
  function f(x) { return x.toFixed(2); }
  function stop(o, col) { return '<stop offset="' + o + '" style="stop-color:' + col + '"/>'; }
  function five(inner) { var g = ''; for (var i = 0; i < 5; i++) g += '<g transform="rotate(' + i * 72 + ')">' + inner + '</g>'; return g; }

  var PETAL = 'M0-.6C-2.5-2-3.9-5.9-2.4-9.3C-1.6-10.9.1-11.5 1.2-10.7C3.3-8.8 2.9-3.5 0-.6Z';
  var VEIN = 'M0-1.8C-.3-4.3-.3-6.8.2-9.2';
  var EDGE = 'stroke:color-mix(in srgb,var(--acc) 45%,var(--cd))';
  var FLOWER =
    '<g transform="translate(.5 .75)" fill="#000" fill-opacity=".11">' + five('<path d="' + PETAL + '"/>') + '</g>' +
    five('<path d="' + PETAL + '" fill="url(#jasmine-fx-w)" style="' + EDGE + '" stroke-width=".42" stroke-linejoin="round"/>') +
    five('<path d="' + VEIN + '" fill="none" style="stroke:color-mix(in srgb,var(--lv) 40%,#fff)" stroke-opacity=".55" stroke-width=".35" stroke-linecap="round"/>') +
    '<circle r="1.4" style="fill:color-mix(in srgb,var(--acc) 55%,var(--lv))"/><circle cx="-.4" cy="-.4" r=".5" fill="#fff" fill-opacity=".6"/>';
  var BUD = 'M0-10.2C2.4-8.6 2.9-3.4 1.9 1.4C1.5 3.4 1 4.6.7 5.4H-.7C-1 4.6-1.5 3.4-1.9 1.4C-2.9-3.4-2.4-8.6 0-10.2Z';
  var BUDART =
    '<path d="' + BUD + '" transform="translate(.4 .6)" fill="#000" fill-opacity=".11"/>' +
    '<path d="' + BUD + '" fill="url(#jasmine-fx-u)" style="' + EDGE + '" stroke-width=".4"/>' +
    '<path d="M-.5-9.4C1.2-6.2 1.5-1.6.5 4.6" fill="none" style="stroke:color-mix(in srgb,var(--lv) 40%,#fff)" stroke-opacity=".5" stroke-width=".35" stroke-linecap="round"/>' +
    '<path d="M-1.8 4.4C-1.4 7 1.4 7 1.8 4.4C.9 5.4-.9 5.4-1.8 4.4Z" style="fill:var(--lv)"/>' +
    '<path d="M0 6.6C.2 7.6.1 8.3-.3 8.9" fill="none" style="stroke:var(--lv)" stroke-width=".5" stroke-linecap="round"/>';
  var DEFS = '<svg class="jasmine-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>' +
    '<radialGradient id="jasmine-fx-w" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="11">' +
      stop(0, 'color-mix(in srgb,var(--lv) 28%,#fff)') + stop(.3, 'color-mix(in srgb,var(--lt) 45%,#fff)') + stop(1, '#fff') + '</radialGradient>' +
    '<linearGradient id="jasmine-fx-u" x1="0" y1="0" x2="0" y2="1">' +
      stop(0, '#fff') + stop(.62, 'color-mix(in srgb,var(--lt) 45%,#fff)') + stop(1, 'color-mix(in srgb,var(--lv) 35%,#fff)') + '</linearGradient>' +
    '<symbol id="jasmine-fx-f" viewBox="-12 -12 24 24">' + FLOWER + '</symbol>' +
    '<symbol id="jasmine-fx-b" viewBox="-4 -11 8 20">' + BUDART + '</symbol></defs></svg>';

  WIS.fx['jasmine'] = function (box, c) {
    var R = c.rand, N = 16, out = [DEFS];
    var xs = strat(N, R), ds = strat(N, R), zs = strat(N, R);
    var kinds = shuffle('ffffffffffffbbbb'.split(''), R);
    for (var i = 0; i < N; i++) {
      var bud = kinds[i] === 'b', z = zs[i];
      var s = bud ? 1.3 + z * .4 : 2.8 + z * 1.7;
      var dur = 15.5 - z * 3 + R() * 1.2, a = .86 + z * .12;
      var x = 5 + edge(xs[i], .85) * 90, del = c.t0 + .3 + ds[i] * 7.5;
      var art = bud ? '<svg viewBox="0 0 8 20" aria-hidden="true" focusable="false"><use href="#jasmine-fx-b"/></svg>'
                    : '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#jasmine-fx-f"/></svg>';
      out.push('<i class="jasmine-p" style="left:' + f(x) + '%;--s:' + f(s) + 'cqw;--h:' + f(bud ? s * 2.5 : s) + 'cqw;--a:' + f(a) +
        ';animation-duration:' + f(dur) + 's;animation-delay:' + f(del) + 's">' +
        '<i class="jasmine-q" style="--sw:' + f(.8 + R() * 1.8) + 'cqw;--rz:' + f(12 + R() * 14) + 'deg;animation-duration:' + f(2.8 + R() * 1.4) +
        's;animation-delay:-' + f(R() * 4) + 's">' +
        '<i class="jasmine-r" style="--tx:' + f(bud ? R() * 20 : 15 + R() * 40) + 'deg;animation-duration:' + f(9 + R() * 7) + 's;animation-delay:-' + f(R() * 12) + 's' +
        (R() < .5 ? ';animation-direction:reverse' : '') + '">' + art + '</i></i></i>');
    }
    box.insertAdjacentHTML('beforeend', out.join(''));
  };
})();
