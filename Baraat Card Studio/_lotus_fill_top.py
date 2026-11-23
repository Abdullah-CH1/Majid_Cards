"""Fill the empty upper half / sides of the lotus-arch card (v3) with three decoration styles,
using elements cut from the card's own painting (lotus flowers, buds, leaves) + gold beads.
usage: python fill_top.py <orig_blank.jpg> <v3.png> <outdir>
"""
import sys, math
from pathlib import Path
import numpy as np, cv2

ORIG, BASE, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3])
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(11)

orig = cv2.imread(ORIG).astype(np.float32)
base = cv2.imread(BASE).astype(np.float32)
H, W = base.shape[:2]

def labsplit(img):
    lab = cv2.cvtColor(np.clip(img, 0, 255).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
    return lab, lab[..., 0] * 100 / 255, lab[..., 1] - 128, lab[..., 2] - 128

lab, L, A, B = labsplit(orig)
paper = np.array([196, 224, 243], np.float32)          # BGR of the cream paper
dEp = np.sqrt((L - 90.2) ** 2 + (A - 2.0) ** 2 + (B - 16.0) ** 2)

# ---------------- element cut-outs from the original painting ----------------
def cut(x0, y0, x1, y1, keep_stem=True, nolines=()):
    sl = (slice(y0, y1), slice(x0, x1))
    a, b, l, d = A[sl], B[sl], L[sl], dEp[sl]
    pink = (a > 7) & (d > 9)
    green = (a < 3.0) & (b > 18) & (d > 12)
    m = (pink | (green if keep_stem else np.zeros_like(pink))).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    # fill small holes
    inv = 1 - m
    n, lb, st, _ = cv2.connectedComponentsWithStats(inv, 4)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] < 1500:
            m[lb == i] = 1
    # keep the largest blob (+ anything big attached)
    n, lb, st, _ = cv2.connectedComponentsWithStats(m, 8)
    if n > 1:
        big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
        m = (lb == big).astype(np.uint8)
    for lx0, lx1 in nolines:                       # frame-line columns: keep only real petal pixels
        c0, c1 = max(0, lx0 - x0), min(x1 - x0, lx1 - x0)
        m[:, c0:c1] = (m[:, c0:c1] > 0) & (a[:, c0:c1] > 9)
    alpha = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.7)
    rgb = orig[sl].copy()
    return np.dstack([rgb, alpha])

EL = {
    "flowerL": cut(18, 826, 212, 982, keep_stem=False, nolines=((14, 37), (176, 201))),
    "flowerR": cut(924, 830, 1121, 984, keep_stem=False, nolines=((920, 945), (1084, 1108))),
    "budL": cut(98, 966, 172, 1054, keep_stem=False),
    "budR": cut(878, 1110, 962, 1232, keep_stem=False, nolines=((920, 945),)),
    "leafHalf": cut(880, 1018, 1046, 1186),
}
EL['leafR'] = np.concatenate([EL['leafHalf'], EL['leafHalf'][:, ::-1]], axis=1)
# stem colour sampled from a stem
stem_px = orig[965:1100, 55:112].reshape(-1, 3)
stem_px = stem_px[((A[965:1100, 55:112] < 0) & (L[965:1100, 55:112] < 66) & (B[965:1100, 55:112] > 15)).reshape(-1)]
STEM = np.array([70, 118, 112], np.float32)   # olive stem green (BGR), matched to the painted stems
# gold colour sampled from the crown mandala line work
gm = (A > 3) & (A < 10) & (B > 22) & (L < 68) & (dEp > 18)
gm[:, :380] = False; gm[:, 740:] = False; gm[350:, :] = False
GOLD = np.median(orig[gm], 0)
print("stem", STEM, "gold", GOLD)

def rot_scale(el, scale, angle, flip=False):
    e = el[:, :, ::-1] if False else el
    if flip:
        e = e[:, ::-1]
    h, w = e.shape[:2]
    nh, nw = max(2, int(h * scale)), max(2, int(w * scale))
    e = cv2.resize(e, (nw, nh), interpolation=cv2.INTER_AREA)
    # pad and rotate
    d = int(math.hypot(nw, nh)) + 4
    pad = np.zeros((d, d, 4), np.float32)
    oy, ox = (d - nh) // 2, (d - nw) // 2
    pad[oy:oy + nh, ox:ox + nw] = e
    M = cv2.getRotationMatrix2D((d / 2, d / 2), angle, 1.0)
    r = cv2.warpAffine(pad, M, (d, d), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
    return r

class Canvas:
    def __init__(self, img):
        self.img = img.copy()
        # paper grain modulation (keeps drawn marks from looking flat)
        g = cv2.cvtColor(np.clip(img, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
        self.grain = np.clip(g / (cv2.GaussianBlur(g, (0, 0), 6) + 1e-3), 0.85, 1.12)

    def paste(self, el, cx, cy, forbid=None):
        h, w = el.shape[:2]
        x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
        xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
        if xa >= xb or ya >= yb:
            return
        e = el[ya - y0:yb - y0, xa - x0:xb - x0]
        a = e[..., 3:4].copy()
        if forbid is not None:
            a *= (1 - forbid[ya:yb, xa:xb, None])
        self.img[ya:yb, xa:xb] = self.img[ya:yb, xa:xb] * (1 - a) + e[..., :3] * a

    def stroke(self, pts, color, width, opacity=1.0, forbid=None, taper=None):
        """antialiased polyline drawn at 4x then downsampled into an alpha mask"""
        S = 4
        x0 = int(max(0, min(p[0] for p in pts) - width * 3)); x1 = int(min(W, max(p[0] for p in pts) + width * 3 + 2))
        y0 = int(max(0, min(p[1] for p in pts) - width * 3)); y1 = int(min(H, max(p[1] for p in pts) + width * 3 + 2))
        m = np.zeros(((y1 - y0) * S, (x1 - x0) * S), np.uint8)
        n = len(pts)
        for i in range(n - 1):
            t = i / max(1, n - 2)
            wv = width if taper is None else width * (taper[0] + (taper[1] - taper[0]) * t)
            p, q = pts[i], pts[i + 1]
            cv2.line(m, (int((p[0] - x0) * S), int((p[1] - y0) * S)), (int((q[0] - x0) * S), int((q[1] - y0) * S)),
                     255, max(1, int(round(wv * S))), cv2.LINE_AA)
        a = cv2.resize(m.astype(np.float32) / 255, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA) * opacity
        if forbid is not None:
            a *= (1 - forbid[y0:y1, x0:x1])
        col = np.array(color, np.float32)[None, None, :] * self.grain[y0:y1, x0:x1, None]
        self.img[y0:y1, x0:x1] = self.img[y0:y1, x0:x1] * (1 - a[..., None]) + col * a[..., None]

    def dot(self, x, y, r, color, opacity=1.0, forbid=None):
        S = 4
        R = int(math.ceil(r + 2))
        x0, y0 = int(x) - R, int(y) - R
        m = np.zeros((2 * R * S, 2 * R * S), np.uint8)
        cv2.circle(m, (int((x - x0) * S), int((y - y0) * S)), int(r * S), 255, -1, cv2.LINE_AA)
        a = cv2.resize(m.astype(np.float32) / 255, (2 * R, 2 * R), interpolation=cv2.INTER_AREA) * opacity
        xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + 2 * R), min(H, y0 + 2 * R)
        a = a[ya - y0:yb - y0, xa - x0:xb - x0]
        if forbid is not None:
            a *= (1 - forbid[ya:yb, xa:xb])
        # light highlight to look like a bead
        col = np.array(color, np.float32)
        self.img[ya:yb, xa:xb] = self.img[ya:yb, xa:xb] * (1 - a[..., None]) + (col * self.grain[ya:yb, xa:xb, None]) * a[..., None]

# ---------------- forbidden area: arch interior + arch lines + crown mandala + frame ----------------
_, Lb, Ab, Bb = labsplit(base)
line = (Lb < np.median(Lb) - 9).astype(np.uint8)
line = cv2.dilate(line, np.ones((3, 3), np.uint8))
ff = line.copy(); mask = np.zeros((H + 2, W + 2), np.uint8)
cv2.floodFill(ff, mask, (560, 700), 2)
interior = (ff == 2)
forbid = cv2.dilate(interior.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))).astype(np.float32)
forbid[0:360, 375:747] = 1          # crown mandala + top ornament
forbid[:38, :] = 1; forbid[:, :35] = 1; forbid[:, W - 35:] = 1
forbid[835:, :] = 1                 # stay above the side lotus plants
forbid = cv2.GaussianBlur(forbid, (0, 0), 1.5)
cv2.imwrite(str(OUT / "_forbid.png"), (forbid * 255).astype(np.uint8))

def mirror_x(x):
    return 1121 - x

def both(fn):
    """run a left-side drawing function, then the same mirrored"""
    fn(lambda x: x, False)
    fn(mirror_x, True)

def catenary(xa, ya, xb, yb, sag, n):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = xa + (xb - xa) * t
        y = ya + (yb - ya) * t + sag * 4 * t * (1 - t)
        pts.append((x, y))
    return pts

BEAD = tuple(GOLD)
BEAD_D = tuple(np.clip(GOLD * 0.82, 0, 255))
STEM_C = tuple(STEM)

def corner_cluster(c, mx, flip, scale=1.0):
    s = scale
    P = lambda el, sc, ang, x, y, f=False: c.paste(rot_scale(EL[el], sc * s, ang if not flip else -ang, flip ^ f), mx(x), y, forbid)
    P("leafR", 0.36, 30, 96, 118, True)
    P("leafR", 0.30, -28, 236, 76)
    P("leafR", 0.27, 72, 70, 236, True)
    P("leafR", 0.22, -60, 330, 60)
    P("budR", 0.62, 34, 50, 176)
    P("budR", 0.52, -42, 318, 96)
    P("flowerR", 0.48, -14, 246, 116)
    P("flowerL", 0.64, 8, 132, 132)
    P("budR", 0.46, 8, 186, 66)

# ======================= A: Lotus corners + gold festoons down the sides =======================
def design_A():
    c = Canvas(base)
    def draw(mx, flip):
        # festoon of beaded gold swags zig-zagging down the side strip
        anchors = [(46, 250), (166, 330), (46, 420), (166, 500), (46, 590), (166, 670), (60, 760)]
        for (xa, ya), (xb, yb) in zip(anchors[:-1], anchors[1:]):
            for sag, n, rb, rs in ((24, 12, 4.0, 2.6), (40, 15, 3.0, 2.0)):          # double strand
                c.stroke(catenary(mx(xa), ya, mx(xb), yb, sag, 40), BEAD_D, 1.3, 0.9, forbid)
                for k, (x, y) in enumerate(catenary(mx(xa), ya, mx(xb), yb, sag, n)):
                    c.dot(x, y, rb if k % 3 == 0 else rs, BEAD, 1.0, forbid)
        for i, (x, y) in enumerate(anchors[:-1]):
            c.paste(rot_scale(EL["leafR"], 0.17, 40 if i % 2 == 0 else -40, flip ^ (i % 2 == 1)), mx(x + (14 if i % 2 == 0 else -14)), y + 4, forbid)
            if i % 2 == 0:
                c.paste(rot_scale(EL["flowerL"], 0.42, 0, flip), mx(x + 10), y - 8, forbid)
            else:
                c.paste(rot_scale(EL["budR"], 0.50, 0, flip), mx(x - 8), y - 14, forbid)
        # tassel at the end
        x, y = anchors[-1]
        for j in range(4):
            c.dot(mx(x), y + 8 + j * 8, 2.0 if j != 2 else 3.0, BEAD, 1.0, forbid)
        c.paste(rot_scale(EL["budR"], 0.50, 0, flip), mx(x), y + 62, forbid)
        corner_cluster(c, mx, flip, 0.95)
    both(draw)
    return c.img

# ======================= B: Lotus vines =======================
def bez(p0, p1, p2, p3, n=60):
    out = []
    for i in range(n + 1):
        t_ = i / n
        x = (1 - t_) ** 3 * p0[0] + 3 * (1 - t_) ** 2 * t_ * p1[0] + 3 * (1 - t_) * t_ ** 2 * p2[0] + t_ ** 3 * p3[0]
        y = (1 - t_) ** 3 * p0[1] + 3 * (1 - t_) ** 2 * t_ * p1[1] + 3 * (1 - t_) * t_ ** 2 * p2[1] + t_ ** 3 * p3[1]
        out.append((x, y))
    return out

def design_B():
    c = Canvas(base)
    def draw(mx, flip):
        M = lambda pts: [(mx(x), y) for x, y in pts]
        side = bez((70, 120), (150, 260), (40, 400), (118, 540), 90) + bez((118, 540), (170, 640), (60, 700), (92, 805), 70)[1:]
        side2 = bez((120, 160), (60, 260), (160, 330), (140, 430), 60)
        top = bez((150, 60), (230, 40), (300, 90), (362, 64), 60)
        for path, w in ((side, 3.0), (side2, 2.0), (top, 2.4)):
            c.stroke(M(path), STEM_C, w, 0.95, forbid, taper=(1.15, 0.45))
        # hanging shoots from the top vine
        for (x, y, L_, bend) in [(205, 52, 110, 10), (262, 62, 140, -12), (318, 72, 80, 8)]:
            shoot = bez((x, y), (x + bend, y + L_ * .35), (x - bend, y + L_ * .7), (x + bend * .5, y + L_), 30)
            c.stroke(M(shoot), STEM_C, 1.6, 0.9, forbid, taper=(1.0, 0.4))
            ex, ey = shoot[-1]
            if L_ >= 100:
                c.paste(rot_scale(EL["budR"], 0.44, 180 + 8 * np.sign(bend), flip), mx(ex), ey + 18, forbid)
            else:
                c.paste(rot_scale(EL["flowerL"], 0.30, 0, flip), mx(ex), ey + 6, forbid)
        # leaves along the vines
        spots = [(side, i) for i in (6, 26, 48, 70, 92, 114, 136, 156)] + [(side2, i) for i in (18, 44)] + [(top, i) for i in (20, 44)]
        for k, (path, i) in enumerate(spots):
            i = min(i, len(path) - 2)
            x, y = path[i]; dx, dy = path[i + 1][0] - x, path[i + 1][1] - y
            side_ = 1 if k % 2 else -1
            ang = math.degrees(math.atan2(-dy, dx)) + 70 * side_
            lf = rot_scale(EL["leafR"], 0.21 + 0.04 * (k % 3), ang, flip ^ (k % 2 == 1))
            c.paste(lf, mx(x + 22 * side_), y + 6, forbid)
        # blossoms and buds on the side vines
        for k, i in enumerate((36, 82, 128, 158)):
            i = min(i, len(side) - 1)
            x, y = side[i]
            if k % 2 == 0:
                c.paste(rot_scale(EL["flowerL"], 0.42, 0, flip), mx(x + 6), y - 4, forbid)
            else:
                c.paste(rot_scale(EL["budR"], 0.50, -14, flip), mx(x - 4), y - 8, forbid)
        c.paste(rot_scale(EL["budR"], 0.40, 20, flip), mx(side2[-1][0]), side2[-1][1] + 14, forbid)
        corner_cluster(c, mx, flip, 0.82)
    both(draw)
    return c.img

# ======================= C: Phool Ladi (hanging flower strings) =======================
def design_C():
    c = Canvas(base)
    strings = [(50, 790), (88, 700), (126, 610), (162, 520), (212, 300), (254, 252), (296, 212), (338, 176)]
    def draw(mx, flip):
        # gold valance of small swags along the top
        xs = [40 + 40 * i for i in range(9)]
        for xa, xb in zip(xs[:-1], xs[1:]):
            c.stroke(catenary(mx(xa), 46, mx(xb), 46, 9, 16), BEAD_D, 1.3, 0.9, forbid)
            for k, (x, y) in enumerate(catenary(mx(xa), 46, mx(xb), 46, 9, 5)):
                c.dot(x, y, 2.0, BEAD, 1.0, forbid)
        for si, (sx, y_end) in enumerate(strings):
            x = mx(sx)
            c.stroke([(x, 47), (x, y_end - 14)], BEAD_D, 1.0, 0.75, forbid)
            y = 62; k = si % 2
            while y < y_end - 40:
                if k % 4 == 1:
                    c.paste(rot_scale(EL["budR"], 0.30, 0, flip ^ (k % 8 == 1)), x, y + 14, forbid); y += 38
                elif k % 4 == 3:
                    c.paste(rot_scale(EL["flowerL"], 0.20, 0, flip), x, y + 8, forbid); y += 26
                else:
                    c.dot(x, y, 2.6, BEAD, 1.0, forbid); c.dot(x, y + 8, 1.7, BEAD, 1.0, forbid); y += 18
                k += 1
            if y_end > 400:
                c.paste(rot_scale(EL["flowerL"], 0.30, 0, flip), x, y_end - 6, forbid)
            else:
                c.paste(rot_scale(EL["budR"], 0.32, 0, flip), x, y_end - 6, forbid)
        for sx, _ in strings:
            c.dot(mx(sx), 47, 3.6, BEAD_D, 1.0, forbid); c.dot(mx(sx), 47, 1.8, BEAD, 1.0, forbid)
    both(draw)
    return c.img

for name, fn in [("A", design_A), ("B", design_B), ("C", design_C)]:
    img = fn()
    cv2.imwrite(str(OUT / f"v4{name}.png"), np.clip(img, 0, 255).astype(np.uint8))
    print("made", name)
for k, e in EL.items():
    cv2.imwrite(str(OUT / f"_el_{k}.png"), np.clip(np.dstack([e[..., :3], e[..., 3] * 255]), 0, 255).astype(np.uint8))
