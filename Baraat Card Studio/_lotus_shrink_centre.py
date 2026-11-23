"""Shrink the bottom-centre lotus + half-mandala of the blank card, keep everything else.
usage: python shrink_centre.py <src> <out> <scale> [debugdir]
"""
import sys
from pathlib import Path
import numpy as np, cv2

src, out, SCALE = sys.argv[1], sys.argv[2], float(sys.argv[3])
dbg = Path(sys.argv[4]) if len(sys.argv) > 4 else None
img = cv2.imread(src).astype(np.float32)
H, W = img.shape[:2]
import os
if os.environ.get('NOPENDANT', '1') == '1':
    px0, px1, py0, py1 = 528, 594, 329, 486
    srcp = img[py0:py1, px0 + 82:px1 + 82].copy()          # clean paper just to the right
    # tone-match each row to the paper beside the pendant
    left = np.median(img[py0:py1, px0 - 14:px0], axis=1); right = np.median(img[py0:py1, px1:px1 + 14], axis=1)
    sref = np.median(srcp, axis=1)
    srcp += ((left + right) / 2 - sref)[:, None, :]
    fm = np.zeros((py1 - py0, px1 - px0), np.float32); fm[4:-4, 4:-4] = 1
    fm = cv2.GaussianBlur(fm, (0, 0), 2.2)[..., None]
    img[py0:py1, px0:px1] = srcp * fm + img[py0:py1, px0:px1] * (1 - fm)
lab = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
L, A, B = lab[..., 0] * 100 / 255, lab[..., 1] - 128, lab[..., 2] - 128

# ---- paper estimate (normalised convolution away from art) ----
def dE(x, y):
    d = x - y
    return np.sqrt((d[..., 0] * 100 / 255) ** 2 + d[..., 1] ** 2 + d[..., 2] ** 2)
den = cv2.bilateralFilter(img.astype(np.uint8), 5, 18, 5)
labd = cv2.cvtColor(den, cv2.COLOR_BGR2LAB).astype(np.float32)
pm = np.ones((H, W), bool)
FORCE = np.zeros((H, W), bool); FORCE[905:, 199:923] = True; FORCE[1080:, :300] = True; FORCE[1080:, 830:] = True
for _ in range(4):
    m = cv2.erode((pm & ~FORCE).astype(np.uint8), np.ones((9, 9), np.uint8)).astype(np.float32)
    wsum = cv2.GaussianBlur(m, (0, 0), 70)
    P = cv2.GaussianBlur(labd * m[..., None], (0, 0), 70) / (wsum[..., None] + 1e-6)
    bad = wsum < 0.08
    for x in range(W):                      # fill unsupported pixels from the nearest good row above
        col_bad = np.where(bad[:, x])[0]
        if len(col_bad):
            good = np.where(~bad[:, x])[0]
            for y in col_bad:
                gy = good[good < y]
                P[y, x] = P[gy[-1], x] if len(gy) else P[good[0], x]
    pm = dE(labd, P) < 5
Pbgr = cv2.cvtColor(np.clip(P, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)
D = dE(labd, P)

# ---- region that holds the centre art (between the arch's inner verticals, lower part) ----
X0, X1, Y0 = 199, 923, 905
region = np.zeros((H, W), bool); region[Y0:, X0:X1] = True

# ---- side plants inside that region (leaves, stems, buds): keep them ----
chroma = np.sqrt(A ** 2 + B ** 2)
green = ((A < 2.6) & (B > 19) & (D > 14))
dark = (L < 58) & (D > 10)
side_zone = np.zeros((H, W), bool); side_zone[:, :385] = True; side_zone[:, 742:] = True
narrow = np.zeros((H, W), bool); narrow[:, :335] = True; narrow[:, 790:] = True
pinkside = (A > 7) & (D > 10) & narrow
seed = ((green & side_zone) | pinkside) & region
seed = cv2.morphologyEx(seed.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
seed = cv2.morphologyEx(seed, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
# fill each plant blob solid (holes inside leaves)
ff = seed.astype(bool)
holes = ~ff
nh, lh, sh, _ = cv2.connectedComponentsWithStats(holes.astype(np.uint8), 4)
small = np.zeros(nh, bool); small[1:] = sh[1:, cv2.CC_STAT_AREA] < 250
plants = ff | small[lh]
n, lbl, st, _ = cv2.connectedComponentsWithStats(plants.astype(np.uint8), 8)
gcount = np.bincount(lbl.ravel(), weights=(green | pinkside).ravel().astype(np.float64), minlength=n)
keep = np.zeros(n, bool); scount = np.bincount(lbl.ravel(), weights=seed.ravel().astype(np.float64), minlength=n)
keep[1:] = (st[1:, cv2.CC_STAT_AREA] > 400) & (gcount[1:] / np.maximum(scount[1:], 1) > 0.3)
plants = keep[lbl] & side_zone
plants = cv2.dilate(plants.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))).astype(bool)

# ---- bottom double frame line (runs behind the lotus) ----
LY0, LY1 = 1348, 1394
band = slice(LY0, LY1)
ref = np.median(np.concatenate([img[LY0 - 8:LY0, 268:372], img[LY1:LY1 + 6, 268:372]], 0).reshape(-1, 3), axis=0)
delta = np.median(img[band, 268:372], axis=1) - ref                       # (rows, 3), relative to nearby paper
delta = np.minimum(delta, 0)                                               # the line only darkens
delta[np.abs(delta).max(1) < 5] = 0
lotus = cv2.morphologyEx(((A > 10) & (D > 12)).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
lotus = cv2.dilate(lotus, np.ones((3, 3), np.uint8)).astype(bool)
img_ex = img.copy()
sub = region[band] & ~lotus[band] & ~plants[band]
img_ex[band] -= delta[:, None, :] * sub[..., None]
D = dE(cv2.cvtColor(np.clip(cv2.bilateralFilter(np.clip(img_ex,0,255).astype(np.uint8), 5, 18, 5),0,255), cv2.COLOR_BGR2LAB).astype(np.float32), P)

# ---- centre art as colour + alpha (colour-to-alpha against the local paper) ----
t0, t1 = 6.0, 18.0
alpha = np.clip((D - t0) / (t1 - t0), 0, 1)
marks = (D > 8).astype(np.uint8)
n2, l2, s2, _ = cv2.connectedComponentsWithStats(marks, 8)
k2 = np.zeros(n2, bool); k2[1:] = s2[1:, cv2.CC_STAT_AREA] >= 25
support = cv2.dilate(k2[l2].astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
alpha[~support] = 0
alpha[~region] = 0; alpha[plants] = 0
alpha[LY0:] *= lotus[LY0:]
alpha[:, :X0 + 10] = 0; alpha[:, X1 - 10:] = 0      # nothing from the arch's own lines at the edges
alpha = cv2.GaussianBlur(alpha, (0, 0), 0.5)
MX = 559.75
occl = cv2.dilate(plants.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool) & region
ys, xs = np.where(occl)
xm = np.round(2 * MX - xs).astype(int)
ok = (xm >= X0) & (xm < X1)
ys, xs, xm = ys[ok], xs[ok], xm[ok]
good = ~occl[ys, xm]
ys, xs, xm = ys[good], xs[good], xm[good]
alpha[ys, xs] = alpha[ys, xm]
img_ex[ys, xs] = img_ex[ys, xm]
a3 = alpha[..., None]
col = np.where(a3 > 0.02, Pbgr + (img_ex - Pbgr) / np.maximum(a3, 0.02), Pbgr)
col = np.clip(col, 0, 255)

# ---- clean plate: centre region replaced by paper texture from the empty arch interior ----
clean = img.copy()
src_y0, src_y1 = 478, Y0 - 2                 # plain paper rows inside the arch
rows = np.linspace(src_y0, src_y1, H - Y0).astype(np.float32)
mapx, mapy = np.meshgrid(np.arange(X0, X1, dtype=np.float32), rows)
patch = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
# match the local paper tone: patch - its paper + destination paper
ppatch = cv2.remap(Pbgr, mapx, mapy, cv2.INTER_LINEAR)
patch = patch - ppatch + Pbgr[Y0:, X0:X1]
replace = region.copy(); replace[plants] = False
r = replace[Y0:, X0:X1]
# soft blend at the plant boundaries and region top
soft = cv2.GaussianBlur(r.astype(np.float32), (0, 0), 1.5)
soft[: 6] *= np.linspace(0, 1, 6)[:, None]
clean[Y0:, X0:X1] = patch * soft[..., None] + img[Y0:, X0:X1] * (1 - soft[..., None])
# redraw the frame line across the cleaned area
clean[band, X0:X1] += delta[:, None, :] * soft[LY0 - Y0:LY1 - Y0, :, None]

# ---- scale the centre art and composite it back, bottom-centre anchored ----
cx = 560
pre = np.dstack([col * a3, alpha])            # premultiplied
cw, ch = int(W * SCALE), int(H * SCALE)
small = cv2.resize(pre, (cw, ch), interpolation=cv2.INTER_AREA)
ox, oy = int(round(cx - cx * SCALE)), H - ch   # keep x=cx fixed, bottom fixed
canvas = np.zeros((H, W, 4), np.float32)
canvas[oy:oy + ch, ox:ox + cw] = small
sa = canvas[..., 3:4]
# don't paint over the kept side plants
sa = sa * (1 - plants[..., None].astype(np.float32))
outimg = clean * (1 - sa) + canvas[..., :3] * (sa > 0) * (sa / np.maximum(canvas[..., 3:4], 1e-6))
outimg = np.where(sa > 0, clean * (1 - sa) + canvas[..., :3] / np.maximum(canvas[..., 3:4], 1e-6) * sa, clean)
cv2.imwrite(out, np.clip(outimg, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 97] if out.lower().endswith(".jpg") else [])
if dbg:
    dbg.mkdir(exist_ok=True)
    cv2.imwrite(str(dbg / "plants.png"), plants.astype(np.uint8) * 255)
    cv2.imwrite(str(dbg / "alpha.png"), (alpha * 255).astype(np.uint8))
    cv2.imwrite(str(dbg / "clean.jpg"), np.clip(clean, 0, 255).astype(np.uint8))
print("done", out)
