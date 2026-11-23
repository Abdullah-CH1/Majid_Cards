WIS.ix['miniature'] = { update: function (c) {
  var r = c.S.querySelector('.ix-miniature .mn-fw'); if (!r) return;
  r.innerHTML = '';
  var B = [[24, 22, 0], [76, 18, .45], [50, 12, .9], [30, 34, 1.35], [72, 31, 1.7]];
  for (var k = 0; k < B.length; k++) {
    var b = document.createElement('div'); b.className = 'mn-bu' + (k % 2 ? ' mn-b2' : '');
    b.style.left = B[k][0] + '%'; b.style.top = B[k][1] + '%';
    b.style.setProperty('--s', (B[k][2] + c.rand() * .15).toFixed(2) + 's');
    var n = 12, rot = c.rand() * 30;
    for (var i = 0; i < n; i++) for (var j = 1; j <= 3; j++) {
      var d = document.createElement('i');
      d.style.setProperty('--a', (rot + i * 360 / n).toFixed(1) + 'deg');
      d.style.setProperty('--r', (j * (k == 2 ? 4.6 : 3.6)).toFixed(1) + 'cqw');
      if (j == 3) d.className = 'mn-t';
      b.appendChild(d);
    }
    r.appendChild(b);
  }
} };
