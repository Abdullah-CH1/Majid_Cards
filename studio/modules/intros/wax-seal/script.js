/* Wax seal letter: deterministic deckled (torn cotton paper) edge for the letter. */
WIS.ix['wax-seal'] = { update: function (c) {
  var root = c.S.querySelector('.ix-wax-seal'); if (!root) return;
  var el = root.querySelector('.ws-letter'); if (!el) return;
  var p = [], n = 22, i, j = function () { return (c.rand() * 0.9).toFixed(2); };
  for (i = 0; i <= n; i++) p.push((i * 100 / n).toFixed(2) + '% ' + j() + '%');
  for (i = 0; i <= n; i++) p.push((100 - j()).toFixed(2) + '% ' + (i * 100 / n).toFixed(2) + '%');
  for (i = n; i >= 0; i--) p.push((i * 100 / n).toFixed(2) + '% ' + (100 - j()).toFixed(2) + '%');
  for (i = n; i >= 0; i--) p.push(j() + '% ' + (i * 100 / n).toFixed(2) + '%');
  el.style.clipPath = 'polygon(' + p.join(',') + ')';
} };
