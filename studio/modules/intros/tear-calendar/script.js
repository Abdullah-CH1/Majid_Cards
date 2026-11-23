/* Countdown Calendar: builds ~12 tear-off pages counting down to the wedding day (correct months & weekdays). */
(function () {
  var MN = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  var WD = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  function dow(y, m, d) { var t = [0,3,2,5,0,3,5,1,4,6,2,4]; if (m < 3) y -= 1;
    return (y + Math.floor(y / 4) - Math.floor(y / 100) + Math.floor(y / 400) + t[m - 1] + d) % 7; }
  function dim(y, m) { return [31, (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0 ? 29 : 28, 31,30,31,30,31,31,30,31,30,31][m - 1]; }
  WIS.ix['tear-calendar'] = { update: function (c) {
    var root = c.S.querySelector('.ix-tear-calendar'); if (!root) return;
    var box = root.querySelector('.tc-pages'); if (!box) return;
    var dp = c.dp || {}, y = parseInt(dp.year, 10) || 2026, mi = dp.monIndex, m = (mi >= 0 ? mi : 11) + 1;
    var d = parseInt(dp.day, 10) || 12; if (d > dim(y, m)) d = dim(y, m);
    var N = 12, list = [];
    for (var k = 0; k < N; k++) { d -= 1; if (d < 1) { m -= 1; if (m < 1) { m = 12; y -= 1; } d = dim(y, m); } list.push([y, m, d]); }
    /* list[0] = the day before the wedding ... list[N-1] = earliest (top of the pad, torn first) */
    var t = 1.0, gap = .78, times = [];
    for (var j = 0; j < N; j++) { times.push(t); t += gap; gap = Math.max(.14, gap * .8); }
    var h = [];
    for (var i = 0; i < N; i++) {           /* DOM order: last torn first, so the earliest page sits on top */
      var p = list[i], tt = times[N - 1 - i], w = dow(p[0], p[1], p[2]);
      var dir = c.rand() < .5 ? -1 : 1, dx = (dir * (18 + c.rand() * 26)).toFixed(1), rz = (dir * (14 + c.rand() * 22)).toFixed(1);
      var dur = Math.max(.55, 1.05 - (N - 1 - i) * .045).toFixed(2);
      h.push('<div class="tc-pg' + (w === 5 ? ' tc-fri' : '') + '" style="--t:' + tt.toFixed(2) + 's;--dx:' + dx + 'cqw;--rz:' + rz + 'deg;--du:' + dur + 's">' +
        '<div class="tc-mo">' + MN[p[1] - 1] + ' ' + p[0] + '</div><div class="tc-num"><span>' + p[2] + '</span></div><div class="tc-wd">' + WD[w] + '</div></div>');
    }
    box.innerHTML = h.join('');
  } };
})();