WIS.ix['sheesh-mahal'] = { update: function (c) {
  var root = c.S.querySelector('.ix-sheesh-mahal'); if (!root) return;
  var R = 7, W = Math.sqrt(3) * R, H = 177.78, LX = 50, LY = 162, f = function (n) { return n.toFixed(2); };
  function hex(x, y, r) { var s = ''; for (var k = 0; k < 6; k++) { var a = Math.PI / 3 * k - Math.PI / 2; s += (k ? 'L' : 'M') + f(x + r * Math.cos(a)) + ' ' + f(y + r * Math.sin(a)); } return s + 'Z'; }
  function tri(x, y, r, o) { var s = ''; for (var k = 0; k < 3; k++) { var a = Math.PI * 2 / 3 * k + o; s += (k ? 'L' : 'M') + f(x + r * Math.cos(a)) + ' ' + f(y + r * Math.sin(a)); } return s + 'Z'; }
  var lp = '', ls = '', cells = [];
  for (var r = 0; r * 1.5 * R < H + R; r++) for (var q = -1; q < 10; q++) {
    var x = q * W + (r % 2 ? W / 2 : 0), y = r * 1.5 * R;
    if (x < -W || x > 100 + W) continue;
    lp += hex(x, y, R); ls += tri(x, y, R * .62, -Math.PI / 2) + tri(x, y, R * .62, Math.PI / 2);
    if (x > 2 && x < 98 && y > 3 && y < H - 3) cells.push({x: x, y: y});
  }
  root.querySelector('.sm-lp').setAttribute('d', lp);
  root.querySelector('.sm-ls').setAttribute('d', ls);
  /* arches */
  function arch(w, ys, ap, n) {
    var h = ys - ap, rr = (w * w + h * h) / (2 * w), cx = 50 + w - rr, a1 = Math.atan2(ap - ys, 50 - cx), pts = [], k, a;
    for (k = 0; k <= n; k++) { a = a1 * k / n; pts.push({x: 100 - (cx + rr * Math.cos(a)), y: ys + rr * Math.sin(a)}); }
    for (k = n - 1; k >= 0; k--) { a = a1 * k / n; pts.push({x: cx + rr * Math.cos(a), y: ys + rr * Math.sin(a)}); }
    return pts;
  }
  var inA = arch(32, 72, 32, 5), outA = arch(37, 72, 24, 24), base = 150;
  var d = 'M18 ' + base + 'L18 72', i;
  for (i = 1; i < inA.length; i++) { var p0 = inA[i - 1], p1 = inA[i], ch = Math.hypot(p1.x - p0.x, p1.y - p0.y); d += 'A' + f(ch * .58) + ' ' + f(ch * .58) + ' 0 0 1 ' + f(p1.x) + ' ' + f(p1.y); }
  d += 'L82 ' + base;
  var od = 'M13 ' + base + 'L13 72'; for (i = 1; i < outA.length; i++) od += 'L' + f(outA[i].x) + ' ' + f(outA[i].y); od += 'L87 ' + base;
  root.querySelector('.sm-ai').setAttribute('d', d);
  root.querySelector('.sm-ao').setAttribute('d', od);
  root.querySelector('.sm-af').setAttribute('d', d + 'Z');
  function poly(pts) { var L = [0]; for (var k = 1; k < pts.length; k++) L.push(L[k - 1] + Math.hypot(pts[k].x - pts[k - 1].x, pts[k].y - pts[k - 1].y)); return {p: pts, L: L}; }
  function at(P, t) { var T = t * P.L[P.L.length - 1], k = 1; while (k < P.L.length - 1 && P.L[k] < T) k++; var u = (T - P.L[k - 1]) / ((P.L[k] - P.L[k - 1]) || 1), a = P.p[k - 1], b = P.p[k]; return {x: a.x + (b.x - a.x) * u, y: a.y + (b.y - a.y) * u}; }
  var P1 = poly([{x: 18, y: base}].concat(inA, [{x: 82, y: base}])), P2 = poly([{x: 13, y: base}].concat(outA, [{x: 87, y: base}]));
  /* chips */
  var box = root.querySelector('.sm-chips'), chips = [], html = '';
  cells.forEach(function (e) { if (c.rand() < .86) chips.push(e); });
  chips.forEach(function (e) { e.ang = Math.atan2(e.x - 50, -(e.y - 105)); });
  var ord = chips.slice().sort(function (a, b) { return a.ang - b.ang; });
  var n1 = Math.ceil(ord.length * .55), n2 = ord.length - n1, i1 = 0, i2 = 0;
  ord.forEach(function (e, k) {
    var useIn = (k % 9) < 5 ? i1 < n1 : i2 >= n2, t;
    if (useIn) { t = at(P1, (i1 + .5) / n1); i1++; } else { t = at(P2, (i2 + .5) / n2); i2++; }
    e.tx = t.x - e.x; e.ty = t.y - e.y; e.inn = useIn;
  });
  chips.forEach(function (e) {
    var dist = Math.hypot(e.x - LX, e.y - LY), fl = 1.1 + dist * .026, tw = fl + 1.1 + c.rand() * 1.4, g = 5.5 + (1 - Math.min(dist, 160) / 160) * .4 + c.rand() * .5;
    html += '<span class="sm-c" style="left:' + f(e.x) + 'cqw;top:' + f(e.y) + 'cqw"><b></b><span class="sm-gd' + (e.inn ? '' : ' sm-o') + '" style="--tx:' + f(e.tx) + 'cqw;--ty:' + f(e.ty) + 'cqw;--g:' + f(g) + 's"><i style="--f:' + f(fl) + 's;--w:' + f(tw) + 's;--wd:' + f(1.6 + c.rand() * 1.6) + 's"></i></span></span>';
  });
  box.innerHTML = html;
  var mp = '';
  for (i = 0; i < 12; i++) { var a = Math.PI / 6 * i; mp += '<path d="' + hex(50 + 31 * Math.cos(a), 50 + 31 * Math.sin(a), 4.2) + '" style="--k:' + i + '"/>'; }
  mp += '<path class="sm-mc" d="' + tri(50, 50, 22, -Math.PI / 2) + tri(50, 50, 22, Math.PI / 2) + '"/>';
  root.querySelector('.sm-mp').innerHTML = mp;
} };
