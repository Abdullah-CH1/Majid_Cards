/* Save the date: builds the month grid with the correct weekday alignment and marks the wedding day. */
(function () {
  function dow(y, m, d) { // 0 = Sunday (Sakamoto)
    var t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]; if (m < 3) y -= 1;
    return (y + Math.floor(y / 4) - Math.floor(y / 100) + Math.floor(y / 400) + t[m - 1] + d) % 7;
  }
  function dim(y, m) { return [31, (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0 ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]; }
  WIS.sc['save-date'] = { update: function (c) {
    var root = c.S.querySelector('.sc-save-date'); if (!root) return;
    var grid = root.querySelector('.svd-grid'); if (!grid) return;
    var dp = c.dp || {}, y = parseInt(dp.year, 10) || 2026, mi = dp.monIndex, m = (mi >= 0 ? mi : 11) + 1;
    var day = parseInt(dp.day, 10) || 1, n = dim(y, m); if (day > n) day = n;
    var first = dow(y, m, 1), h = [];
    for (var i = 0; i < first; i++) h.push('<span class="svd-c svd-e"></span>');
    for (var d = 1; d <= n; d++) {
      if (d === day) h.push('<span class="svd-c svd-on"><svg class="svd-ht" viewBox="0 0 100 100" aria-hidden="true"><path pathLength="1" d="M50 88C30 72 8 58 8 36C8 20 20 10 32 10C42 10 48 17 50 25C52 17 58 10 68 10C80 10 92 20 92 36C92 58 70 72 48 90"/></svg><em>' + d + '</em></span>');
      else h.push('<span class="svd-c" style="--i:' + d + '">' + d + '</span>');
    }
    grid.innerHTML = h.join('');
  } };
})();
