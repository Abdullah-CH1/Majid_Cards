WIS.ix['phulkari'] = { update: function (c) {
  var R = c.S.querySelector('.ix-phulkari'); if (!R) return;
  var mg = R.querySelector('.phk-mg'), sg = R.querySelector('.phk-sg'), fl = R.querySelector('.phk-fl');
  if (!mg || mg.getAttribute('data-done')) return;
  var CX = 50, CY = 32, m = '', s = '', f = '';
  function p(x, y) { return x.toFixed(2) + ' ' + y.toFixed(2); }
  function dia(cx, cy, a, D, h, w) { var ux = Math.cos(a), uy = Math.sin(a), vx = -uy, vy = ux, x = cx + ux * D, y = cy + uy * D;
    return 'M' + p(x + ux * h, y + uy * h) + 'L' + p(x + vx * w, y + vy * w) + 'L' + p(x - ux * h, y - uy * h) + 'L' + p(x - vx * w, y - vy * w) + 'Z'; }
  function st(d, t, l) { var j = (c.rand() * 0.06).toFixed(2);
    m += '<path d="' + d + '" pathLength="1" class="phk-mk" style="--d:' + (t + +j).toFixed(2) + 's;--l:' + l + 's"/>';
    s += '<path d="' + d + '" class="phk-sp"/>'; }
  function fi(d, t, k) { f += '<path d="' + d + '" class="phk-f' + k + '" style="--d:' + t.toFixed(2) + 's"/>'; }
  var i, a;
  st(dia(CX, CY, -Math.PI / 2, 0, 5, 5), 0.2, 2.2);
  fi(dia(CX, CY, -Math.PI / 2, 0, 2.6, 2.6), 2.3, 1);
  for (i = 0; i < 8; i++) { a = -Math.PI / 2 + i * Math.PI / 4;
    st(dia(CX, CY, a, 12.5, 6.5, 3), 2.9 + i * 0.16, 0.5);
    fi(dia(CX, CY, a, 12.5, 3.6, 1.6), 3.5 + i * 0.12, i % 2 ? 2 : 1);
    st(dia(CX, CY, a + Math.PI / 8, 15, 2, 2), 4.8 + i * 0.08, 0.35);
    st(dia(CX, CY, a + Math.PI / 4 * 0.5 + Math.PI / 8, 25, 2.5, 2.5), 5.0 + i * 0.07, 0.35); }
  st('M28 10H72V54H28Z', 4.8, 1.0);
  st('M7 7H93V170.8H7Z', 5.9, 1.2);
  var z = 'M14 144'; for (i = 0; i < 18; i++) z += 'L' + (16 + i * 4) + ' ' + (i % 2 ? 144 : 138);
  st(z, 6.0, 0.9);
  for (i = 0; i < 9; i++) { st(dia(18 + i * 8, 154, -Math.PI / 2, 0, 4, 3), 6.1 + i * 0.07, 0.3); fi(dia(18 + i * 8, 154, -Math.PI / 2, 0, 2, 1.4), 6.5 + i * 0.05, i % 2 ? 1 : 2); }
  [[15, 15], [85, 15], [15, 163], [85, 163]].forEach(function (q, k) {
    for (i = 0; i < 4; i++) st(dia(q[0], q[1], i * Math.PI / 2, 3, 3, 1.6), 5.6 + k * 0.1 + i * 0.05, 0.3);
    fi(dia(q[0], q[1], 0, 0, 1.2, 1.2), 6.2 + k * 0.1, 2); });
  mg.innerHTML = m; sg.innerHTML = s; fl.innerHTML = f; mg.setAttribute('data-done', '1');
} };
