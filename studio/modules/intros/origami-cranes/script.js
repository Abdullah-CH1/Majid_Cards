/* Origami cranes: builds the flock (positions, sizes, palette tones, wing beat offsets) deterministically. */
(function () {
  var SVG = '<polygon class="oc-w2" points="42 56 60 20 70 6 58 58"/><polygon class="oc-tl" points="42 60 8 34 8 36 34 66"/>' +
    '<polygon class="oc-bd" points="70 60 50 52 28 60 50 70"/><polygon class="oc-nk" points="58 68 62 58 82 34 93 42 84 41"/>' +
    '<polygon class="oc-w1" points="26 4 34 22 56 56 40 58"/>';
  var POS = [[13, 22], [27, 44], [66, 13], [86, 24], [16, 66], [62, 56], [89, 60], [37, 9], [76, 76], [5, 44], [48, 74]];
  var TONES = ['var(--ef)', 'var(--acc)', 'var(--bl)', 'var(--lv)', 'color-mix(in srgb,var(--acc) 50%,var(--ef))',
    'var(--p2)', 'color-mix(in srgb,var(--bl) 55%,var(--ef))'];
  WIS.ix['origami-cranes'] = { update: function (c) {
    var root = c.S.querySelector('.ix-origami-cranes'); if (!root) return;
    var box = root.querySelector('.oc-flock'); if (!box) return;
    var h = [], i, p, s, a1;
    for (i = 0; i < POS.length; i++) {
      p = POS[i]; s = 6.5 + c.rand() * 5.5; a1 = -2 + c.rand() * 4;
      h.push('<div class="oc-fw" style="left:' + (p[0] - s / 2).toFixed(2) + 'cqw;top:' + (p[1] - s / 2).toFixed(2) + 'cqw;width:' +
        s.toFixed(2) + 'cqw;height:' + s.toFixed(2) + 'cqw;--a0:' + (-36 - c.rand() * 6).toFixed(1) + 'deg;--a1:' + a1.toFixed(1) +
        'deg;--a2:' + (a1 + 3).toFixed(1) + 'deg;--a3:' + (34 + c.rand() * 6).toFixed(1) + 'deg;--dl:' + (i * 0.06 + c.rand() * 0.25).toFixed(2) +
        's"><svg class="oc-cr" viewBox="0 0 100 100" style="--c:' + TONES[i % TONES.length] + ';--fd:' + (-c.rand() * 0.9).toFixed(2) +
        's" aria-hidden="true">' + SVG + '</svg></div>');
    }
    box.innerHTML = h.join('');
  } };
})();
