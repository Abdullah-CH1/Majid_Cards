"""Rebuild the lotus-arch card as pure SVG shapes (no embedded picture).
paper  -> smooth colour field (blurred grid of rects) + feTurbulence grain
art    -> colour-quantised layers traced to vector paths (stacked light -> dark)
usage: python trace_card.py <src.jpg> <out.svg> [K] [thresh]
"""
import sys, json
import numpy as np, cv2

src, out = sys.argv[1], sys.argv[2]
K = int(sys.argv[3]) if len(sys.argv) > 3 else 56
TH = float(sys.argv[4]) if len(sys.argv) > 4 else 5.0
MINA = int(sys.argv[5]) if len(sys.argv) > 5 else 14
import os
SC = int(os.environ.get('SC', '2'))
ORDER = os.environ.get('ORDER', 'light')
DIL = int(os.environ.get('DIL', '2'))

bgr = cv2.imread(src)
H, W = bgr.shape[:2]
big = cv2.resize(bgr, (W * SC, H * SC), interpolation=cv2.INTER_CUBIC)
lab = cv2.cvtColor(big, cv2.COLOR_BGR2LAB).astype(np.float32)
den = cv2.bilateralFilter(big, 7, 18, 7)
labd = cv2.cvtColor(den, cv2.COLOR_BGR2LAB).astype(np.float32)

# ---- paper estimate by normalised convolution, iterated ----
def smooth_paper(mask_paper, sigma=60):
    m = cv2.erode(mask_paper.astype(np.uint8), np.ones((15, 15), np.uint8)).astype(np.float32)
    num = cv2.GaussianBlur(labd * m[..., None], (0, 0), sigma)
    den_ = cv2.GaussianBlur(m, (0, 0), sigma)[..., None] + 1e-6
    return num / den_

# lab in OpenCV 8-bit scale: L*255/100, a+128, b+128 -> convert distances to dE-ish
def dE(a, b):
    d = a - b
    return np.sqrt((d[..., 0] * 100 / 255) ** 2 + d[..., 1] ** 2 + d[..., 2] ** 2)

paper_mask = np.ones(labd.shape[:2], bool)
for it in range(4):
    P = smooth_paper(paper_mask)
    diff = dE(labd, P)
    paper_mask = diff < TH
art = ~paper_mask
# clean: remove specks, close tiny gaps
art = art.astype(np.uint8)
art = cv2.morphologyEx(art, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
n, lbl, stats, _ = cv2.connectedComponentsWithStats(art, 8)
keep = np.zeros(n, bool); keep[1:] = stats[1:, cv2.CC_STAT_AREA] >= MINA * SC * SC
art = keep[lbl]

# ---- paper field as a coarse grid ----
GX, GY = 34, 42
Pbgr = cv2.cvtColor(np.clip(P, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
grid = np.clip(cv2.resize(Pbgr, (GX, GY), interpolation=cv2.INTER_AREA).astype(int) + 4, 0, 255).astype(np.uint8)

# ---- quantise art colours (k-means in Lab) ----
W_AB = np.array([1.0, 1.7, 1.7], np.float32)
pix = labd[art].reshape(-1, 3) * W_AB
crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 0.5)
sample = pix[np.random.default_rng(1).choice(len(pix), min(len(pix), 400000), replace=False)]
_, _, centers = cv2.kmeans(sample, K, None, crit, 3, cv2.KMEANS_PP_CENTERS)
# assign all art pixels
labels = np.empty(len(pix), np.int32)
for i in range(0, len(pix), 200000):
    ch_ = pix[i:i + 200000]
    labels[i:i + 200000] = np.argmin(((ch_[:, None, :] - centers[None, :, :]) ** 2).sum(-1), 1)
lab_img = np.full(art.shape, -1, np.int32); lab_img[art] = labels
# median-filter labels to kill salt noise
lab8 = (lab_img + 1).astype(np.uint8)
lab8 = cv2.medianBlur(lab8, 3)
lab_img = lab8.astype(np.int32) - 1
centers = centers / W_AB
order = np.argsort(-centers[:, 0]) if ORDER == 'light' else np.argsort(centers[:, 0])
rank = np.empty(K, int); rank[order] = np.arange(K)
rank_img = np.where(lab_img >= 0, rank[np.clip(lab_img, 0, None)], -1)
cbgr = cv2.cvtColor(np.clip(centers, 0, 255).astype(np.uint8)[None], cv2.COLOR_LAB2BGR)[0]

def hexc(c): return "#%02x%02x%02x" % (int(c[2]), int(c[1]), int(c[0]))

def contours_to_d(mask):
    cs, hier = cv2.findContours(mask.astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    parts = []
    for c in cs:
        if len(c) < 3: continue
        a = cv2.approxPolyDP(c, 1.0, True).reshape(-1, 2)
        if len(a) < 3: continue
        pts = a / SC
        parts.append("M" + " ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z")
    return "".join(parts)

art_d = cv2.dilate(art.astype(np.uint8), np.ones((2, 2), np.uint8)).astype(bool)
paths = []
for r in range(K):
    m = cv2.dilate((rank_img == r).astype(np.uint8), np.ones((DIL, DIL), np.uint8)).astype(bool) & art_d
    if not m.any(): continue
    d = contours_to_d(m)
    if d: paths.append((hexc(cbgr[order[r]]), d))

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" shape-rendering="geometricPrecision">',
       '<defs><filter id="pblur" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="22"/></filter>',
       '<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7" result="n"/>'
       '<feColorMatrix type="matrix" values="0 0 0 0 .52  0 0 0 0 .42  0 0 0 0 .28  3.2 0 0 0 -1.75"/></filter>',
       '<filter id="mott" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".012" numOctaves="3" seed="3"/>'
       '<feColorMatrix type="matrix" values="0 0 0 0 .55  0 0 0 0 .45  0 0 0 0 .3  0 0 0 -1.2 .62"/></filter></defs>',
       f'<rect width="{W}" height="{H}" fill="{hexc(grid.reshape(-1,3).mean(0))}"/>',
       '<g filter="url(#pblur)">']
cw, ch = W / GX, H / GY
for y in range(GY):
    for x in range(GX):
        svg.append(f'<rect x="{x*cw-1:.1f}" y="{y*ch-1:.1f}" width="{cw+2:.1f}" height="{ch+2:.1f}" fill="{hexc(grid[y,x])}"/>')
svg.append('</g>')
svg.append(f'<rect width="{W}" height="{H}" filter="url(#mott)" opacity=".22"/>')
svg.append(f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".55"/>')
svg.append('<g id="art" stroke-linejoin="round">')
for col, d in paths:
    svg.append(f'<path fill="{col}" fill-rule="evenodd" stroke="{col}" stroke-width=".25" d="{d}"/>')
svg.append('</g></svg>')
open(out, "w", encoding="utf-8").write("\n".join(svg))
print(json.dumps({"layers": len(paths), "art_px": int(art.sum()), "bytes": sum(len(s) for s in svg)}))
