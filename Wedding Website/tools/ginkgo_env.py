"""Sculpted ginkgo-leaf envelope + oval wax seal (used by make_assets.py: envelope(), seal()).
The envelope is modelled as ONE height field per sheet (body, top flap): every leaf is a layer of plaster-like
relief (thick rounded edge, cupped blade, ruffled up-turned margin, fine veins that follow the flare of the fan,
petiole) draped over whatever lies below. The height field is then lit from the upper left like pearly satin, with
ray-marched soft cast shadows and ambient occlusion, and tone-matched to the reference video.
Leaf positions were traced from the rectified reference frames (900 x 1950 design px).
Run directly for a preview:  python tools/ginkgo_env.py <outdir>     (GENV_SS=0.5 for a quick half-size render)
"""
import math, sys, os
import numpy as np, cv2

W, H = 900, 1950                         # design px
SS = float(os.environ.get("GENV_SS", "1"))   # texture px per design px
TW, TH = int(round(W * SS)), int(round(H * SS))
HSCALE = 1.5
# luminance percentiles of the reference envelope (seal excluded): the textures are tone-matched to these
# (the raw video frames are under-exposed by the camera: the white page of the same video reads 184/180/194, so the
#  measured percentiles 69..209 are lifted by ~1.22 with a soft shoulder -> a lighter, pearly silver-mauve)
REF_P = ([1, 5, 10, 25, 50, 75, 90, 95, 99, 99.7], [84, 111, 124, 135, 152, 172, 193, 205, 224, 234])

def smooth01(x):
    x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)

def noise(h, w, scale, octaves=4, seed=0):
    r = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        s = max(1, int(scale / (2 ** o)))
        g = r.random((h // s + 3, w // s + 3)).astype(np.float32)
        g = cv2.resize(g, (w + 3 * s, h + 3 * s), interpolation=cv2.INTER_CUBIC)[:h, :w]
        out += g * amp; tot += amp; amp *= 0.5
    return out / tot

def dgrid(x0, y0, x1, y1):
    """design-px coordinates of the texture pixels x0..x1, y0..y1"""
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    return (yy + 0.5) / SS, (xx + 0.5) / SS

# ------------------------------------------------------------------ lighting
LIGHT = np.array([-0.42, -0.72, 0.56], np.float32); LIGHT /= np.linalg.norm(LIGHT)
HALF = LIGHT + np.array([0, 0, 1.0], np.float32); HALF /= np.linalg.norm(HALF)

def cast_shadow(hgt, reach=100.0, rise=0.33, soft=5.0):
    """soft shadow (0..1) a height field (design px) casts on itself; the light comes from the upper left"""
    u = LIGHT[:2] / np.linalg.norm(LIGHT[:2])
    over = np.full(hgt.shape, -1e3, np.float32)
    hh, ww = hgt.shape
    k = 1.5
    while k <= reach:
        M = np.float32([[1, 0, -k * u[0] * SS], [0, 1, -k * u[1] * SS]])
        sh = cv2.warpAffine(hgt, M, (ww, hh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        over = np.maximum(over, sh - k * rise - hgt - 0.02 * k)
        k += 1.5 if k < 30 else 3.0
    s = smooth01(over / soft)
    return cv2.GaussianBlur(s, (0, 0), 3.5 * SS)

def pearl_shade(hgt, tint, ao=None, shadow=None):
    """height (design px) -> pearly lit colour. tint: (h,w) 0 = silver-lilac, 1 = pink-mauve"""
    gy, gx = np.gradient(hgt); gx = gx * SS; gy = gy * SS
    n = np.dstack([-gx, -gy, np.ones_like(hgt)]); n /= np.linalg.norm(n, axis=2, keepdims=True)
    nl = (n * LIGHT).sum(2); nh = np.clip((n * HALF).sum(2), 0, 1)
    diff = np.clip(nl, 0, 1)
    wrap = np.clip((nl + 0.35) / 1.35, 0, 1)
    broad = nh ** 5; spec = nh ** 24
    lit = 1.0 if shadow is None else 1 - shadow
    lum = 0.15 + 0.40 * wrap * (0.42 + 0.58 * lit) + (0.52 * diff + 0.07 * broad) * lit
    if ao is not None:
        lum = lum * (1 - ao)
    silver = np.array([176, 175, 188], np.float32); mauve = np.array([178, 151, 165], np.float32)
    alb = silver[None, None] * (1 - tint[..., None]) + mauve[None, None] * tint[..., None]
    col = alb * lum[..., None] + np.array([255, 248, 255], np.float32) * (0.12 * spec * lit)[..., None]
    return np.clip(col, 0, 255)

def shade_sheet(hgt, tint):
    """full lighting of a composited height field: normals + cast shadows + ambient occlusion"""
    hs = cv2.GaussianBlur(hgt, (0, 0), max(0.55, 0.7 * SS))
    sh = cast_shadow(hs)
    ao = (0.14 * np.clip((cv2.GaussianBlur(hs, (0, 0), 9 * SS) - hs) / 12.0, 0, 1)
          + 0.40 * np.clip((cv2.GaussianBlur(hs, (0, 0), 34 * SS) - hs) / 30.0, 0, 1))
    return pearl_shade(hs, tint, ao=ao, shadow=sh)

# ------------------------------------------------------------------ ginkgo leaf
def _wave(s, lam, rr, n=3):
    """irregular 1-D wave of the arc position s (px) around wavelength lam, about -1..1"""
    out = 0
    for _ in range(n):
        out = out + np.sin(s * (2 * math.pi / (lam * rr.uniform(0.6, 1.6))) + rr.uniform(0, 6.283))
    return out / (0.62 * n)

def leaf_fields(cx, cy, R, ang, spread=55, seed=0, f0=0.15, flare=0.8, bend=0.0, droop=0.12, lobes=1.0, ruffle=1.0,
                notch=0.0, notch_t=0.0, veins=1.0, thick=10.0, curl=1.0, cup=1.0, fold=1.0, stem=0.0, stem_bend=0.0,
                bbox=None, **_):
    """one sculpted ginkgo leaf: returns (x0, y0, alpha, height, vein) on the texture grid.
    Petiole end at (cx, cy) design px, blade pointing ang (deg), length R, half-angle `spread` at the margin.
    The sides are concave (the fan flares out with distance) and the veins follow that flare."""
    rr = np.random.default_rng(seed)
    bw, bh = bbox if bbox else (W, H)
    pad = R * 1.16 + stem + 14
    x0, x1 = int(max(0, cx - pad) * SS), int(min(bw, cx + pad) * SS)
    y0, y1 = int(max(0, cy - pad) * SS), int(min(bh, cy + pad) * SS)
    if x0 >= x1 or y0 >= y1:
        return None
    yy, xx = dgrid(x0, y0, x1, y1)
    dx, dy = xx - cx, yy - cy
    r = np.hypot(dx, dy) + 1e-3
    sp = math.radians(spread)
    a = np.radians((np.degrees(np.arctan2(dy, dx)) - ang + 180) % 360 - 180)
    q = r / R
    a = a - math.radians(bend) * q + 0.03 * np.sin(q * 3.1 + rr.uniform(0, 6.283))
    A = sp * (f0 + (1 - f0) * np.sin(np.clip(q / flare, 0, 1) * math.pi / 2) ** 1.2)     # half-angle grows with r
    t = a / A
    tcl = np.clip(t, -1.25, 1.25)
    s = tcl * sp * R                                                        # arc position along the margin
    ph = rr.random(8) * 6.283
    # margin: broad lobes, scallops, crinkles and little torn nicks
    w1 = _wave(s, 125, rr); w2 = _wave(s, 50, rr); w3 = _wave(s, 20, rr)
    edge = R * (1 - droop * np.abs(tcl) ** 2.5 + lobes * 0.065 * _wave(s, 0.8 * sp * R, rr, 2))
    edge = edge + ruffle * (12.0 * w1 + 3.2 * w2 + 0.5 * w3)
    for _c in range(int(rr.integers(1, 3))):                                 # one or two little tears
        tn = rr.uniform(-0.8, 0.8)
        edge = edge - ruffle * rr.uniform(0.03, 0.07) * R * np.exp(-((tcl - tn) / rr.uniform(0.02, 0.035)) ** 2)
    if notch:
        edge = edge - notch * R * (np.exp(-((tcl - notch_t) / 0.04) ** 2) + 0.35 * np.exp(-((tcl - notch_t) / 0.16) ** 2))
    dist_m = edge - r
    swl = 5.0 * _wave(r, 115, rr) + 2.0 * _wave(r, 42, rr); swr = 5.0 * _wave(r, 115, rr) + 2.0 * _wave(r, 42, rr)
    sw = np.where(t < 0, swl, swr) * smooth01((q - 0.3) / 0.3) * ruffle
    dist_s = (1 - np.abs(t)) * A * r + sw
    k = 14.0
    dmin = -k * np.log(np.exp(-np.clip(dist_s, -40, 400) / k) + np.exp(-np.clip(dist_m, -40, 400) / k))
    ew = max(1.4, 1.3 / SS)
    alpha = smooth01((dmin + ew / 2) / ew)
    rn = r / np.maximum(edge, 1); rc = np.clip(rn, 0, 1)
    ds = np.clip(dist_s, 0, None); dm = np.clip(dmin, 0, None)
    # ---- height (design px)
    h = thick * (1 - (1 - np.clip(dm / 9.0, 0, 1)) ** 2)                                 # thick rounded edge
    h = h + cup * 6.0 * np.sin(math.pi * rc ** 0.85) * (0.7 + 0.3 * np.cos(1.7 * tcl + ph[0])) * smooth01(rc / 0.2)
    h = h - fold * 4.0 * np.exp(-(tcl / 0.16) ** 2) * smooth01((rc - 0.05) / 0.4)        # shallow valley on the axis
    for _i in range(int(rr.integers(2, 4))):                                              # broad soft radial folds
        tc = rr.uniform(-0.85, 0.85); wd = rr.uniform(0.10, 0.25); amp = rr.choice([-1, 1]) * rr.uniform(1.0, 2.6)
        h = h + amp * np.exp(-((tcl - tc) / wd) ** 2) * smooth01((rc - 0.12) / 0.4)
    nearm = smooth01((rc - 0.70) / 0.30) ** 1.3
    h = h + curl * (10.0 * smooth01((rc - 0.66) / 0.34) ** 2 + nearm * (3.2 * w1 + 1.5 * w2))   # margin curls up, fluted
    h = h + curl * 7.0 * np.exp(-ds / 18.0) * smooth01((rc - 0.2) / 0.3) * (1 + 0.08 * sw)   # sides roll up
    # veins: fine ridges of constant t (so they bend with the flare); sparse, most of them faint
    arc = A * r
    vein = np.zeros_like(h)
    vw = max(1.8, 1.0 / SS)
    for f, amp in ((12, 1.0), (24, 0.9), (48, 0.8), (96, 0.7), (192, 0.6), (384, 0.5), (768, 0.4)):
        tj = t + (0.40 / f) * np.sin(t * f * 0.61 + ph[f % 7]) + (0.22 / f) * np.sin(t * f * 1.37 + ph[(f + 2) % 7])
        u = (tj + 1) * f * 0.5
        idx = np.round(u)
        dpx = np.abs(u - idx) / (f * 0.5) * arc
        rnd = (np.sin(idx * 12.9898 + f * 78.233 + seed) * 43758.5453) % 1.0
        rnd2 = (np.sin(idx * 39.3468 + f * 11.135 + seed) * 24634.6345) % 1.0
        if f <= 24:                                                      # primary veins: long, strongest by the petiole
            along = 0.15 + 0.85 * (1 - smooth01((rc - 0.2) / 0.55))
        else:                                                            # hair-fine streaks: short soft dashes
            along = smooth01(1.6 * np.sin(rc * (9.0 + 16.0 * rnd2) + rnd * 6.283) - 0.35)
        on = smooth01((arc * 2 / f - 3.2) / 3.5)
        vein += amp * rnd ** 1.25 * along * on * np.exp(-(dpx / vw) ** 2)
    vis = 0.30 + 0.70 * np.sin(2.3 * tcl + 3.1 * rc + ph[1]) ** 2
    vein = np.clip(veins * vis * vein * smooth01((rn - 0.02) / 0.10) * (1 - 0.7 * smooth01((rn - 0.9) / 0.1)), 0, 1.4)
    h = h + 0.9 * vein
    # hand-modelled surface: soft lumps and a fine tooth
    hh_, ww_ = h.shape
    h = h + 9.0 * (noise(hh_, ww_, max(2, int(150 * SS)), 2, seed + 7) - 0.5) * smooth01(rc / 0.3)
    # silky radial striation (like brushed plaster): random stripes of constant t, in bands that keep ~3-8 px spacing
    stri = np.zeros_like(h)
    um = ((np.clip(t, -1.3, 1.3) + 1.3) / 2.6).astype(np.float32); vm = np.clip(rc, 0, 1).astype(np.float32)
    for nu in (80, 160, 320, 640):
        tex = rr.random((26, nu)).astype(np.float32) - 0.5
        smp = cv2.remap(tex, um * (nu - 1), vm * 25, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        spc = 2.6 * arc / nu
        stri += smp * smooth01((spc - 2.2) / 2.0) * (1 - smooth01((spc - 4.6) / 3.5))
    h = h + 1.05 * veins * stri * (0.35 + 0.65 * vis) * smooth01((rn - 0.04) / 0.12)
    # petiole: a round stalk behind the base, running on into the blade as a ridge
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    u = dx * ca + dy * sa; v = -dx * sa + dy * ca
    h = h + 3.5 * np.exp(-(v / 4.5) ** 2) * np.exp(-np.clip(u, 0, None) / (0.14 * R)) * (u > 0)
    if stem > 0:
        vc = v - stem_bend * (np.clip(-u, 0, None) / stem) ** 2 * stem
        wd = 4.4
        a_st = smooth01((wd - np.abs(vc)) / ew + 0.5) * smooth01((u + stem) / 4.0) * smooth01((10.0 - u) / 6.0)
        h_st = 2.5 + 5.0 * np.sqrt(np.clip(1 - (vc / wd) ** 2, 0, 1))
        h = np.where(a_st > alpha, h_st, np.maximum(h, h_st * a_st))
        alpha = np.maximum(alpha, a_st)
    return x0, y0, alpha.astype(np.float32), (h * HSCALE).astype(np.float32), vein.astype(np.float32)

def stem_fields(pts, width, bbox=None):
    """thin raised twig along a polyline (design px), tapering towards its last point"""
    bw, bh = bbox if bbox else (W, H)
    tw, th = int(round(bw * SS)), int(round(bh * SS))
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, x1 = int(max(0, min(xs) - 12) * SS), int(min(bw, max(xs) + 12) * SS)
    y0, y1 = int(max(0, min(ys) - 12) * SS), int(min(bh, max(ys) + 12) * SS)
    yy, xx = dgrid(x0, y0, x1, y1)
    d = np.full(yy.shape, 1e3, np.float32); along = np.zeros_like(d); L = 0.0
    for (ax_, ay_), (bx_, by_) in zip(pts[:-1], pts[1:]):
        vx, vy = bx_ - ax_, by_ - ay_; ln = math.hypot(vx, vy)
        u = np.clip(((xx - ax_) * vx + (yy - ay_) * vy) / (ln * ln), 0, 1)
        dd = np.hypot(xx - (ax_ + u * vx), yy - (ay_ + u * vy))
        along = np.where(dd < d, L + u * ln, along); d = np.minimum(d, dd); L += ln
    hw = width / 2 * (1.0 - 0.45 * along / L)
    ew = max(1.4, 1.3 / SS)
    alpha = smooth01((hw - d) / ew + 0.5)
    prof = np.sqrt(np.clip(1 - (d / hw) ** 2, 0, 1))
    return x0, y0, alpha.astype(np.float32), ((prof * width * 0.7 + 1.5) * HSCALE).astype(np.float32)

# ------------------------------------------------------------------ compositing (one height field per sheet)
class Canvas:
    def __init__(self, w, h, tint, paper):
        self.w, self.h = w, h
        self.hg = paper.astype(np.float32).copy()
        self.tint = tint.astype(np.float32).copy()
        self.alb = np.ones((h, w), np.float32)

    def layer(self, f, clip=None, tint=0.0, lift=0.0, tone=1.0):
        """drape a leaf over what is already there"""
        if f is None: return
        x0, y0, a, hgt = f[:4]
        hh, ww = a.shape
        if clip is not None: a = a * clip[y0:y0 + hh, x0:x0 + ww]
        reg = self.hg[y0:y0 + hh, x0:x0 + ww]
        base = cv2.GaussianBlur(reg, (0, 0), 38 * SS)
        reg[:] = reg * (1 - a) + (base + hgt + lift) * a
        if tint:
            tr = self.tint[y0:y0 + hh, x0:x0 + ww]; tr[:] = np.clip(tr + tint * a, 0, 1)
        ar = self.alb[y0:y0 + hh, x0:x0 + ww]; ar[:] = ar * (1 - a) + tone * a

    def render(self):
        return shade_sheet(self.hg, self.tint) * self.alb[..., None]

def luma(rgb):
    return rgb[..., 0] * 0.30 + rgb[..., 1] * 0.59 + rgb[..., 2] * 0.11

def tone_curve(rgb):
    """piecewise-linear luminance map that gives rgb the reference's tonal distribution"""
    g = luma(rgb)
    src = [float(np.percentile(g, p)) for p in REF_P[0]]
    return [0.0] + src + [255.0], [0.0] + list(REF_P[1]) + [240.0]

def tone_apply(rgb, tm):
    g = luma(rgb)
    g2 = np.interp(g, tm[0], tm[1])
    return np.clip(rgb * (g2 / np.maximum(g, 1))[..., None], 0, 255)

def flat_paper(h, w, seed):
    return (noise(h, w, max(2, int(260 * SS)), 3, seed + 1) - 0.5) * 10.0 + (noise(h, w, max(2, int(60 * SS)), 2, seed + 2) - 0.5) * 1.2

def tint_map(th, tw, seed=3):
    yy, xx = dgrid(0, 0, tw, th)
    t = -0.52 + 0.95 * (xx / W) ** 1.5 + 0.62 * (yy / H)
    t += (noise(th, tw, max(2, int(420 * SS)), 3, seed) - 0.5) * 0.6
    return np.clip(t, 0, 1)

# ------------------------------------------------------------------ envelope geometry (fractions of W/H)
FLAP_SIDE_Y, FLAP_TIP_Y = 0.335, 0.535        # top flap: sides -> tip (hidden under the seal)
POCKET_SIDE_Y, POCKET_TIP_Y = 0.300, 0.478    # top edge of the side flaps (the envelope mouth)
BOT_SIDE_Y, BOT_TIP_Y = 0.700, 0.505          # bottom flap: sides -> apex (under the seal)

# leaves, bottom layer first (design px, traced from the reference video)
BODY_LEAVES = [
    dict(cx=340, cy=1040, R=450, ang=-152, spread=44, seed=100, tone=0.88),               # L1 left of the seal
    dict(cx=600, cy=1010, R=430, ang=-28, spread=40, seed=110, tint=0.08),                # R0 right of the seal
    dict(cx=215, cy=1425, R=420, ang=-98, spread=56, seed=102, tone=0.95),                # L2 rising on the left
    dict(cx=745, cy=1350, R=430, ang=-80, spread=54, seed=112, tint=0.12),                # R1 rising on the right
    dict(cx=478, cy=1905, R=720, ang=-170, spread=40, seed=130, ruffle=0.6, curl=0.5, tone=0.88, veins=0.6),    # B6 broad, lower left
    dict(cx=300, cy=2165, R=315, ang=-88, spread=55, seed=131, tone=0.92, ruffle=0.5, curl=0.6, veins=0.6),                # B5 very bottom
    dict(cx=495, cy=1925, R=430, ang=-30, spread=44, seed=132, tint=0.10, tone=0.9, veins=0.6, ruffle=0.7),     # B4 lower right
    dict(cx=474, cy=1790, R=620, ang=-128, spread=32, seed=133, f0=0.2),                          # B2 big left
    dict(cx=572, cy=1228, R=515, ang=60, spread=57, seed=134, tint=0.22, f0=0.5, flare=0.6),         # B3 big pink, hangs from the seal
    dict(cx=452, cy=1562, R=385, ang=-121, spread=32, seed=135, tone=1.05, bend=-8),               # B1 upper left
]
BODY_TWIG = [(456, 1240), (453, 1400), (450, 1500), (457, 1650), (472, 1790), (486, 1900), (493, 1965)]
FLAP_LEAVES = [
    dict(cx=-150, cy=250, R=340, ang=-50, spread=45, seed=205),                           # top-left corner
    dict(cx=462, cy=735, R=680, ang=-150, spread=44, seed=202, ruffle=0.7, tone=0.93, f0=0.45),    # F2 lower left
    dict(cx=492, cy=745, R=560, ang=-34, spread=42, seed=201, tint=0.06, f0=0.45),                 # F3 lower right
    dict(cx=445, cy=950, R=262, ang=-110, spread=60, seed=204, f0=0.35, ruffle=0.5, curl=0.7, tone=1.07, veins=0.6),   # F4 small, over the tip
    dict(cx=474, cy=712, R=735, ang=-86, spread=60, seed=203, f0=0.13, flare=0.85, droop=0.22,
         notch=0.13, notch_t=0.25, stem=42, stem_bend=0.1),                               # F1 the big fan
]

def _lay(cv, specs, clip, bb):
    for p in specs:
        p = dict(p); tint = p.pop("tint", 0.0); tone = p.pop("tone", 1.0)
        cv.layer(leaf_fields(**p, bbox=bb), clip, tint=tint, tone=tone)

def build_body():
    yy, xx = dgrid(0, 0, TW, TH)
    ax = np.abs(xx - W / 2) / (W / 2)
    mouth = H * (POCKET_TIP_Y - (POCKET_TIP_Y - POCKET_SIDE_Y) * ax)
    sides = smooth01((yy - mouth) * SS / 1.6)
    paper = flat_paper(TH, TW, 11) + 3.0 * np.exp(-(np.clip(yy - mouth, 0, None) / 4.0) ** 2)    # bevel on the mouth edge
    cv = Canvas(TW, TH, tint_map(TH, TW), paper)
    bb = (W, H)
    _lay(cv, BODY_LEAVES, None, bb)
    cv.layer(stem_fields(BODY_TWIG, 8.5, bb))
    # bottom flap: the art runs across the seams (as in the video); the flap is a low step with a creased edge
    bline = H * (BOT_TIP_Y + (BOT_SIDE_Y - BOT_TIP_Y) * ax)
    bd = (yy - bline) * 0.76
    bot = smooth01(bd / 2.2 + 0.5)
    cv.hg += HSCALE * (4.2 * bot + 1.6 * np.exp(-((bd - 1.5) / 2.6) ** 2) - 2.2 * np.exp(-((bd + 3.0) / 2.4) ** 2))
    rgb = cv.render()
    return rgb, np.clip(np.maximum(sides, smooth01((yy - bline) * SS / 1.6)), 0, 1)

def build_flap():
    FH = int(TH * 0.56)
    yy, xx = dgrid(0, 0, TW, FH)
    ax = np.abs(xx - W / 2) / (W / 2)
    lim = H * (FLAP_TIP_Y - (FLAP_TIP_Y - FLAP_SIDE_Y) * ax)
    dist = lim - yy
    mask = smooth01((dist * SS + 0.6) / 1.6)
    paper = flat_paper(FH, TW, 31) + 3.5 * (1 - smooth01(dist / 9.0))      # rounded bevel along the flap edge
    cv = Canvas(TW, FH, tint_map(TH, TW, 5)[:FH], paper)
    _lay(cv, FLAP_LEAVES, None, (W, FH / SS))
    rgb = cv.render()
    # the folded edge of the flap catches a little light
    edge = np.exp(-(np.clip(dist, 0, None) / 2.6) ** 2) * mask
    rgb = np.clip(rgb * (1 + 0.08 * (1 - smooth01(dist / 22.0)) * mask)[..., None] + 40 * edge[..., None], 0, 255)
    return rgb, mask

# ------------------------------------------------------------------ wax seal (oval, thick irregular rim, A & L)
from PIL import Image, ImageDraw, ImageFont
MONO_FONT = r"C:\Windows\Fonts\FRSCRIPT.TTF"

def _txt(text, size, cw, ch, off, font=MONO_FONT):
    im = Image.new("L", (cw, ch), 0); d = ImageDraw.Draw(im); f = ImageFont.truetype(font, size)
    bb = d.textbbox((0, 0), text, font=f)
    d.text(((cw - (bb[2] - bb[0])) / 2 - bb[0] + off[0], (ch - (bb[3] - bb[1])) / 2 - bb[1] + off[1]), text, font=f, fill=255)
    return np.array(im, np.float32) / 255

def build_seal(mono=("A", "L")):
    SW, SH = 600, 660
    yy, xx = np.mgrid[0:SH, 0:SW].astype(np.float32)
    cx, cy = SW / 2, SH / 2
    ang = np.arctan2(yy - cy, xx - cx)
    rr = np.random.default_rng(5)
    # irregular outer wax outline (an ellipse with soft lumps and one flattened side)
    wob = (0.014 * np.sin(ang * 3 + 0.7) + 0.010 * np.sin(ang * 5 + 2.1) + 0.012 * np.sin(ang * 6 + 0.3)
           + 0.004 * np.sin(ang * 13 + 1.9) + 0.030 * np.exp(-((ang - 0.25) / 0.22) ** 2) + 0.018 * np.exp(-((ang + 2.6) / 0.3) ** 2))
    ax_, ay_ = 288 * (1 + wob), 318 * (1 + wob)
    rho = np.sqrt(((xx - cx) / ax_) ** 2 + ((yy - cy) / ay_) ** 2)
    d_o = (1 - rho) * 260                                            # ~px inside the wax outline
    blob = smooth01((d_o + 0.8) / 2.0)
    # stamp (pressed oval)
    sa, sb = 172, 276
    rs = np.sqrt(((xx - cx) / sa) ** 2 + ((yy - cy) / sb) ** 2)
    dist_s = (1 - rs) * 200                                          # ~px inside the stamp edge
    u = np.clip(np.clip(d_o, 0, None) / (np.clip(d_o, 0, None) + np.clip(-dist_s, 0, None) + 1e-3), 0, 1)
    rim = np.where(u < 0.5, 36 * np.sin(np.clip(u, 0, 0.5) * math.pi) ** 0.55, 20 + 16 * np.cos((u - 0.5) * math.pi))   # rounded roll of wax
    press = smooth01((dist_s + 3) / 12.0)
    h = rim * (1 - press) + 12.0 * press                             # steep inner wall, flat pressed field
    h += 3.0 * (noise(SH, SW, 90, 3, 41) - 0.5) * (1 - press) + 0.25 * (noise(SH, SW, 25, 2, 42) - 0.5)
    # double oval border inside the stamp
    def ring(off, w, amp):
        return amp * np.exp(-((dist_s - off) / w) ** 2)
    h += ring(9, 3.0, 4.0) + ring(22, 2.2, 3.0)
    # monogram: A (upper left) & L (lower right), raised
    cw, ch = SW, SH
    m = np.maximum(np.maximum(_txt(mono[0], 268, cw, ch, (-26, -86)), _txt(mono[1], 268, cw, ch, (28, 92))),
                   _txt("&", 126, cw, ch, (4, 6)))
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))
    mh = cv2.GaussianBlur(m, (0, 0), 1.6)
    h += 6.0 * mh * press
    # little air pits on the rim and a lump on the right
    for (px, py, pr) in [(92, 250, 4.5), (88, 285, 4), (94, 322, 3.5), (100, 352, 3), (505, 410, 8)]:
        d2 = ((xx - px) ** 2 + (yy - py) ** 2) / pr ** 2
        h += (-4.0 if pr < 6 else 5.0) * np.exp(-d2)
    h = cv2.GaussianBlur(h, (0, 0), 0.8)
    gy, gx = np.gradient(h)
    n = np.dstack([-gx, -gy, np.ones_like(h)]); n /= np.linalg.norm(n, axis=2, keepdims=True)
    nl = (n * LIGHT).sum(2); nh = np.clip((n * HALF).sum(2), 0, 1)
    diff = np.clip(nl, 0, 1); wrap = np.clip((nl + 0.4) / 1.4, 0, 1)
    base = np.array([102, 90, 96], np.float32) * (0.96 + 0.08 * noise(SH, SW, 120, 3, 43))[..., None]
    lum = 0.20 + 0.42 * wrap + 0.36 * diff
    col = base * lum[..., None] + np.array([230, 222, 228], np.float32) * (0.55 * nh ** 22 + 0.14 * nh ** 5)[..., None]
    return np.clip(col, 0, 255), blob

def build_envelope():
    """-> body_rgb, body_alpha, flap_rgb, flap_alpha (tone-matched to the reference video)"""
    rgb, a = build_body()
    frgb, fa = build_flap()
    comp = rgb * a[..., None] + np.array([60, 48, 58], np.float32) * (1 - a[..., None])
    FH = frgb.shape[0]
    fs = np.zeros((TH, TW), np.float32); fs[:FH] = fa
    fs1 = cv2.GaussianBlur(cv2.warpAffine(fs, np.float32([[1, 0, 0], [0, 1, 5 * SS]]), (TW, TH)), (0, 0), 2.5 * SS)
    fs = cv2.GaussianBlur(cv2.warpAffine(fs, np.float32([[1, 0, 0], [0, 1, 21 * SS]]), (TW, TH)), (0, 0), 12 * SS)
    comp *= ((1 - 0.38 * fs1) * (1 - 0.62 * fs))[..., None]      # = the CSS drop-shadows of the flap                      # (the site draws this shadow with CSS)
    comp[:FH] = comp[:FH] * (1 - fa[..., None]) + frgb * fa[..., None]
    tm = tone_curve(comp)
    def grade(c, y0=0):                                          # warm the silver a touch; rosier toward the lower right, as in the video
        hh, ww = c.shape[:2]
        yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
        t = np.clip(0.75 * (xx / ww) + 0.55 * ((yy + y0) / TH) - 0.45, 0, 1)[..., None]
        return np.clip(c * (np.array([1.02, 0.995, 1.0], np.float32) * (1 - t) + np.array([1.04, 0.985, 0.985], np.float32) * t), 0, 255)
    return grade(tone_apply(rgb, tm)), a, grade(tone_apply(frgb, tm)), fa

def preview(out):
    rgb, a, frgb, fa = build_envelope()
    comp = rgb * a[..., None] + np.array([60, 48, 58], np.float32) * (1 - a[..., None])
    FH = frgb.shape[0]
    fs = np.zeros((TH, TW), np.float32); fs[:FH] = fa
    fs1 = cv2.GaussianBlur(cv2.warpAffine(fs, np.float32([[1, 0, 0], [0, 1, 5 * SS]]), (TW, TH)), (0, 0), 2.5 * SS)
    fs = cv2.GaussianBlur(cv2.warpAffine(fs, np.float32([[1, 0, 0], [0, 1, 21 * SS]]), (TW, TH)), (0, 0), 12 * SS)
    comp *= ((1 - 0.38 * fs1) * (1 - 0.62 * fs))[..., None]      # = the CSS drop-shadows of the flap
    comp[:FH] = comp[:FH] * (1 - fa[..., None]) + frgb * fa[..., None]
    srgb, sa = build_seal()
    sw = int(TW * 0.40); sh = int(sw * 660 / 600)
    srgb = cv2.resize(srgb, (sw, sh), interpolation=cv2.INTER_AREA); sa = cv2.resize(sa, (sw, sh), interpolation=cv2.INTER_AREA)
    x0 = TW // 2 - sw // 2; y0 = int(TH * 0.513) - sh // 2
    sh_m = np.zeros((TH, TW), np.float32); sh_m[y0:y0 + sh, x0:x0 + sw] = sa
    sh_m = cv2.GaussianBlur(cv2.warpAffine(sh_m, np.float32([[1, 0, 4 * SS], [0, 1, 9 * SS]]), (TW, TH)), (0, 0), 7 * SS)
    comp *= (1 - 0.5 * sh_m)[..., None]
    reg = comp[y0:y0 + sh, x0:x0 + sw]; reg[:] = reg * (1 - sa[..., None]) + srgb * sa[..., None]
    cv2.imwrite(str(out) + "/env_proto.png", cv2.cvtColor(comp.astype(np.uint8), cv2.COLOR_RGB2BGR))

if __name__ == "__main__":
    import time; t0 = time.time()
    preview(sys.argv[1] if len(sys.argv) > 1 else ".")
    print("done", round(time.time() - t0, 1), "s")
