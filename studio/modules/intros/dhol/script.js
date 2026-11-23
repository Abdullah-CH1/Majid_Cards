WIS.ix['dhol'] = {update: function (c) {
  var R = c.S.querySelector('.ix-dhol'); if (!R) return;
  function line(el, name, t0, span) {
    el.innerHTML = '';
    var s = (name || '').trim(), n = Array.from(s).length || 1;
    if (/[؀-ۿ]/.test(s)) {
      el.classList.add('dhol-ar'); el.style.fontSize = Math.min(17, 84 / (n * .42)).toFixed(2) + 'cqw';
      var w = document.createElement('span'); w.className = 'dhol-l'; w.textContent = s;
      w.style.setProperty('--t', t0.toFixed(2) + 's'); el.appendChild(w); return t0 + .4;
    }
    el.classList.remove('dhol-ar');
    el.style.fontSize = Math.min(20, 86 / (n * .5)).toFixed(2) + 'cqw';
    var st = Math.min(.09, span / n);
    Array.from(s).forEach(function (ch, i) {
      var l = document.createElement('span'); l.className = 'dhol-l';
      l.textContent = ch === ' ' ? ' ' : ch;
      l.style.setProperty('--t', (t0 + i * st).toFixed(2) + 's'); el.appendChild(l);
    });
    return t0 + n * st;
  }
  line(R.querySelector('.dhol-gn'), c.g, 3.0, 1.1);
  line(R.querySelector('.dhol-bn'), c.b, 4.55, 1.1);
  var P = R.querySelector('.dhol-puffs'); if (!P) return; P.innerHTML = '';
  var beats = [-0.1, .5, 1, 1.5, 2, 6.3, 6.8, 8.5];
  beats.forEach(function (t, bi) {
    var n = bi === beats.length - 1 ? 26 : 10, big = bi === beats.length - 1 ? 1.6 : 1;
    for (var i = 0; i < n; i++) {
      var e = document.createElement('i'), a = -Math.PI * (0.08 + c.rand() * 0.84), r = (14 + c.rand() * 26) * big;
      e.className = 'dhol-cf dhol-c' + (i % 4) + (c.rand() < .4 ? ' dhol-sq' : '');
      e.style.setProperty('--dx', (Math.cos(a) * r).toFixed(1) + 'cqw');
      e.style.setProperty('--dy', (Math.sin(a) * r * 1.2).toFixed(1) + 'cqw');
      e.style.setProperty('--rz', Math.round(c.rand() * 720 - 360) + 'deg');
      e.style.setProperty('--t', (t + c.rand() * .05).toFixed(2) + 's');
      P.appendChild(e);
    }
  });
}};
