/* Gold Foil Press: fine gold flecks that settle on the card after the foil peels (deterministic per update). */
WIS.ix['foil-press'] = { update: function (c) {
  var root = c.S.querySelector('.ix-foil-press'); if (!root) return;
  var box = root.querySelector('.fp-fx'); if (!box) return;
  var h = [], i, x, y, f = function (n) { return n.toFixed(2); };
  for (i = 0; i < 30; i++) {
    /* keep most flecks to the margins of the card so they never sit on the text */
    var side = c.rand();
    if (side < .35) { x = 2 + c.rand() * 14; y = 3 + c.rand() * 94; }
    else if (side < .7) { x = 84 + c.rand() * 13; y = 3 + c.rand() * 94; }
    else if (side < .85) { x = 10 + c.rand() * 80; y = 1.5 + c.rand() * 5; }
    else { x = 10 + c.rand() * 80; y = 93 + c.rand() * 5; }
    h.push('<i class="fp-fk" style="--x:' + f(x) + '%;--y:' + f(y) + '%;--s:' + f(.45 + c.rand() * .8) + 'cqw;--r:' + Math.round(c.rand() * 360 - 180) + 'deg;--dx:' + f((c.rand() - .5) * 6) + 'cqw;--a:' + f(.55 + c.rand() * .4) + ';--d:' + f(c.rand() * 1.1) + 's"></i>');
  }
  box.innerHTML = h.join('');
} };
