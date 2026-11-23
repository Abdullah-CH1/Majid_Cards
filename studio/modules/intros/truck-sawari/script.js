WIS.ix['truck-sawari'] = { update: function (c) {
  var r = c.S.querySelector('.ix-truck-sawari .ts-rt'); if (!r) return;
  var w = /walima/i.test((c.evKey || '') + ' ' + (c.ev || ''));
  r.textContent = w ? 'Walima ki dawat hai!' : 'Baraat aa rahi hai!';
} };
