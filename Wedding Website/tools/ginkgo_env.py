"""Sculpted ginkgo-leaf envelope + oval wax seal (used by make_assets.py: envelope(), seal()).
Every leaf is its own layer: a height field (soft swells, flared sides, ruffled up-turned margin, fine
dichotomous veins) lit like pearly satin, with a cast shadow on whatever lies below. Flaps are layers too.
Run directly for a preview:  python tools/ginkgo_env.py <outdir>
"""
import math, sys
import numpy as np, cv2

W, H = 900, 1950
HSCALE = 1.5
# luminance percentiles of the reference envelope (seal excluded): the textures are tone-matched to these
REF_P = ([1, 5, 10, 25, 50, 75, 90, 95, 99, 99.7], [69, 91, 101.5, 111, 125, 141, 160, 172, 195, 209])

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

# ------------------------------------------------------------------ lighting
LIGHT = np.array([-0.42, -0.72, 0.56], np.float32); LIGHT /= np.linalg.norm(LIGHT)
HALF = LIGHT + np.array([0, 0, 1.0], np.float32); HALF /= np.linalg.norm(HALF)

def pearl_shade(hgt, tint, ao=None):
    """height (px units) -> pearly lit colour. tint: (h,w) 0 = silver-lilac, 1 = pink-mauve"""
    gy, gx = np.gradient(hgt)
    n = np.dstack([-gx, -gy, np.ones_like(hgt)]); n /= np.linalg.norm(n, axis=2, keepdims=True)
    nl = (n * LIGHT).sum(2); nh = np.clip((n * HALF).sum(2), 0, 1)
    diff = np.clip(nl, 0, 1)
    wrap = np.clip((nl + 0.35) / 1.35, 0, 1)
    broad = nh ** 5; spec = nh ** 24
    lum = 0.16 + 0.40 * wrap + 0.40 * diff + 0.24 * broad
    if ao is not None:
        lum = lum * (1 - ao)
    silver = np.array([176, 175, 188], np.float32); mauve = np.array([178, 148, 164], np.float32)
    alb = silver[None, None] * (1 - tint[..., None]) + mauve[None, None] * tint[..., None]
    col = alb * lum[..., None] + np.array([255, 248, 255], np.float32) * (0.22 * spec)[..., None]
    return np.clip(col, 0, 255)

# ------------------------------------------------------------------ ginkgo leaf
def leaf_fields(cx, cy, R, ang, spread=55, seed=0, notch=0.06, veins=1.0, folds=1.0, ruffle=1.0, side_bulge=0.22, fold=1.0, swell=1.0,
                bbox=None):
    """returns (x0, y0, alpha, height) for one sculpted ginkgo leaf; base (petiole) at (cx, cy), pointing ang (deg)."""
    rr = np.random.default_rng(seed)
    pad = int(R * 1.08) + 12
    x0, x1 = int(max(0, cx - pad)), int(min(bbox[0], cx + pad))
    y0, y1 = int(max(0, cy - pad)), int(min(bbox[1], cy + pad))
    if x0 >= x1 or y0 >= y1:
        return None
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    dx, dy = xx - cx, yy - cy
    r = np.hypot(dx, dy) + 1e-3
    sp = math.radians(spread)
    a = np.radians((np.degrees(np.arctan2(dy, dx)) - ang + 180) % 360 - 180)
    # gentle s-bend of the whole fan so it is not a perfect wedge
    a = a + 0.05 * np.sin(r / R * 2.2 + rr.random() * 6)
    t = a / sp
    ph = rr.random(6) * 6.283
    # margin: broad lobes + ruffles + soft central notch
    edge = (R * (1 - 0.10 * t ** 2
                + ruffle * (0.028 * np.sin(t * 3.6 + ph[0]) + 0.012 * np.sin(t * 9 + ph[1])))                 + ruffle * (8.0 * np.sin(t * sp * R / 42.0 + ph[2]) + 3.0 * np.sin(t * sp * R / 15.0 + ph[3]) + 1.0 * np.sin(t * sp * R / 6.0 + ph[1])))
    edge -= notch * R * np.exp(-(t / 0.07) ** 2)
    tm = 0.38 + 0.62 * smooth01(r / (0.80 * R)) ** 0.75                    # narrow at the petiole, sides flare out
    # corner rounding where side meets margin
    dist_side = (tm - np.abs(t)) * sp * r                                  # px inside the side edge
    dist_side += ruffle * smooth01((r / R - 0.35) / 0.4) * (7.0 * np.sin(r / 40.0 + ph[4] + 3 * np.sign(t)) + 2.5 * np.sin(r / 14.0 + ph[5]) + 0.9 * np.sin(r / 6.0 + ph[2]))
    dist_marg = edge - r                                                   # px inside the margin
    k = 18.0
    dmin = -k * np.log(np.exp(-np.clip(dist_side, -40, 400) / k) + np.exp(-np.clip(dist_marg, -40, 400) / k))
    alpha = smooth01((dmin + 0.8) / 1.8)
    alpha *= smooth01((r - 3) / 6)
    rn = np.clip(r / np.maximum(edge, 1), 0, 1.2)
    rc = np.clip(rn, 0, 1)
    ds = np.clip(dist_side, 0, None)
    # ---- height (px): soft sculpted swells, a ridge along the axis, edges curling up
    h = 4.0 * smooth01(rc / 0.30)
    h += fold * 9.0 * np.cos(np.clip(t, -1, 1) * math.pi / 2) ** 2 * smooth01(rc / 0.45)
    h += 14.0 * np.sin(rc * math.pi * 0.9) * (0.6 + 0.4 * np.cos(t * 2.1 + ph[3]))          # blade bulges between base and margin
    for i in range(5):
        k = rr.uniform(1.0, 3.5); m = rr.uniform(2.0, 6.0); amp = rr.uniform(2.5, 6.0) * swell
        h += amp * np.sin(k * t + m * rc + rr.random() * 6.283) * smooth01(rc / 0.25)
    h += 9.0 * smooth01((rc - 0.55) / 0.45) ** 2                        # margin cups upward
    h += 4.0 * np.exp(-ds / 14.0) * smooth01((rc - 0.15) / 0.3)        # sides roll up
    # a few soft radial creases
    for _ in range(int(2 + rr.integers(0, 3))):
        tc = rr.uniform(-0.8, 0.8); s = rr.choice([-1, 1]) * rr.uniform(0.8, 2.0) * folds
        wpx = rr.uniform(4, 9)
        h += s * np.exp(-(((t - tc) * sp * r) / wpx) ** 2) * smooth01((rn - 0.1) / 0.3)
    # veins: fine glossy ridges converging on the petiole; a few bright ones, most faint, fading in and out
    arc = sp * r
    tv = t + 0.003 * np.sin(r / 23.0 + ph[0])
    vein = np.zeros_like(h)
    for f, amp in ((18, 1.0), (36, 0.9), (72, 0.8), (144, 0.65), (288, 0.45)):
        tj = tv + (0.45 / f) * np.sin(tv * f * 0.61 + ph[f % 6]) + (0.25 / f) * np.sin(tv * f * 1.37 + ph[(f + 2) % 6])
        u = (tj + 1) * f * 0.5
        dpx = np.abs(u - np.round(u)) / (f * 0.5) * arc
        idx = np.round(u).astype(np.float32)
        rnd = (np.sin(idx * 12.9898 + f * 78.233) * 43758.5453) % 1.0           # per-line random number
        rnd2 = (np.sin(idx * 39.3468 + f * 11.135) * 24634.6345) % 1.0
        strength = rnd ** 1.8                                                     # most faint, a few strong
        along = smooth01(0.5 + 0.9 * np.sin(rc * (2.0 + 3.0 * rnd2) + rnd * 6.283))   # lines fade in and out
        spacing = arc * 2 / f
        on = smooth01((spacing - 5.0) / 4.0)
        vein += amp * strength * along * on * np.exp(-(dpx / 1.25) ** 2)
    vis = 0.35 + 0.65 * np.sin(2.3 * t + 3.1 * rc + ph[1]) ** 2
    vein = veins * vis * vein * smooth01((rn - 0.03) / 0.10) * (1 - 0.8 * smooth01((rn - 0.92) / 0.08))
    h += 0.9 * vein
    # thin ruffled edge
    nearm = smooth01((rc - 0.78) / 0.22)
    h += ruffle * nearm * (6.0 * np.sin(t * sp * R / 42.0 + ph[2] + 0.8) + 2.0 * np.sin(t * sp * R / 15.0 + ph[3] + 0.5))
    h += ruffle * 4.0 * np.exp(-ds / 16.0) * smooth01((rc - 0.4) / 0.3) * np.sin(r / 40.0 + ph[4] + 3 * np.sign(t) + 0.8)   # wavy sides
    lipw = smooth01((rn - 0.18) / 0.25)
    h += 3.2 * np.exp(-(np.clip(dmin, 0, None) / 4.5) ** 2) * lipw          # rolled, up-turned edge
    h += 4.0
    return x0, y0, alpha.astype(np.float32), (h * HSCALE).astype(np.float32), np.clip(vein, 0, 1.5).astype(np.float32)

def stem_fields(pts, width, bbox):
    """thin raised twig / petiole along a polyline"""
    m = np.zeros((bbox[1], bbox[0]), np.float32)
    cv2.polylines(m, [np.int32(np.round(np.array(pts) * 4))], False, 1.0, int(width * 4), cv2.LINE_AA, shift=2)
    d = cv2.distanceTransform((m < 0.5).astype(np.uint8), cv2.DIST_L2, 5)
    inside = cv2.distanceTransform((m >= 0.5).astype(np.uint8), cv2.DIST_L2, 5)
    hw = width / 2
    prof = np.sqrt(np.clip(1 - ((hw - inside) / hw) ** 2, 0, 1)) * (m >= 0.5)
    alpha = cv2.GaussianBlur(m, (0, 0), 0.6)
    return 0, 0, alpha, (prof * width * 0.7 + 3.0).astype(np.float32)

# ------------------------------------------------------------------ compositing
class Canvas:
    def __init__(self, w, h, tint):
        self.w, self.h = w, h
        self.rgb = np.zeros((h, w, 3), np.float32)
        self.alpha = np.zeros((h, w), np.float32)
        self.tint = tint

    def panel(self, mask, hgt, shadow=(0.30, 5, (3, 6))):
        col = pearl_shade(hgt, self.tint)
        self.shadow(mask, *shadow)
        self.rgb = self.rgb * (1 - mask[..., None]) + col * mask[..., None]
        self.alpha = np.maximum(self.alpha, mask)

    def shadow(self, mask, strength, blur, off):
        M = np.float32([[1, 0, off[0]], [0, 1, off[1]]])
        s = cv2.warpAffine(mask, M, (self.w, self.h))
        s = cv2.GaussianBlur(s, (0, 0), blur)
        self.rgb *= (1 - strength * s * (1 - mask))[..., None]

    def layer(self, f, clip=None):
        if f is None: return
        x0, y0, a, hgt = f[:4]
        gloss = f[4] if len(f) > 4 else None
        hh, ww = a.shape
        full = np.zeros((self.h, self.w), np.float32); full[y0:y0 + hh, x0:x0 + ww] = a
        if clip is not None: full *= clip
        # cast + contact shadow on what is below
        self.shadow(full, 0.50, 13, (7, 13))
        self.shadow(full, 0.30, 3.5, (2.0, 4.0))
        # shade the leaf itself (ambient occlusion near its base)
        col = pearl_shade(hgt, self.tint[y0:y0 + hh, x0:x0 + ww])
        rim = np.clip((a - cv2.GaussianBlur(a, (0, 0), 3.4)) * 2.4, 0, 1)      # glossy up-turned edge catches the light
        col = col + 88 * rim[..., None]
        if gloss is not None:                                                     # veins read as fine bright lines
            col = col + 95 * gloss[..., None]
        col = np.clip(col, 0, 255)
        a2 = full[y0:y0 + hh, x0:x0 + ww][..., None]
        reg = self.rgb[y0:y0 + hh, x0:x0 + ww]
        reg[:] = reg * (1 - a2) + col * a2

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
    return (noise(h, w, 260, 3, seed + 1) - 0.5) * 14.0 + (noise(h, w, 60, 2, seed + 2) - 0.5) * 1.2

def tint_map(h, w, seed=3):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    t = -0.25 + 1.05 * (xx / w) ** 1.4 + 0.35 * (yy / h)
    t += (noise(h, w, 420, 3, seed) - 0.5) * 0.7
    return np.clip(t, 0, 1)

# ------------------------------------------------------------------ envelope geometry (fractions of W/H)
FLAP_SIDE_Y, FLAP_TIP_Y = 0.335, 0.535        # top flap: sides -> tip (hidden under the seal)
POCKET_SIDE_Y, POCKET_TIP_Y = 0.300, 0.478    # side flaps' top edge (the envelope mouth)
BOT_SIDE_Y, BOT_TIP_Y = 0.700, 0.505          # bottom flap: sides -> rounded apex

def build_body():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ax = np.abs(xx - W / 2) / (W / 2)
    tint = tint_map(H, W)
    cv = Canvas(W, H, tint)
    # side flaps (one sheet below the mouth line)
    mouth = H * (POCKET_TIP_Y - (POCKET_TIP_Y - POCKET_SIDE_Y) * ax)
    sides = smooth01((yy - mouth) / 1.6)
    hp = flat_paper(H, W, 11) + 3.0 * np.exp(-(np.clip(yy - mouth, 0, None) / 4.0) ** 2)    # bevel on the mouth edge
    cv.panel(sides, hp)
    bb = (W, H)
    left_clip = sides * smooth01((W / 2 + 4 - xx) / 2) ; right_clip = sides * smooth01((xx - W / 2 + 4) / 2)
    # leaves on the side flaps (they run on under the bottom flap)
    for p in [dict(cx=330, cy=1180, R=560, ang=-128, spread=50, seed=100),
              dict(cx=300, cy=1290, R=440, ang=-174, spread=44, seed=102, fold=-0.6),
              dict(cx=300, cy=1075, R=420, ang=-160, spread=42, seed=101)]:
        cv.layer(leaf_fields(**p, bbox=bb), left_clip)
    for p in [dict(cx=600, cy=1180, R=560, ang=-52, spread=50, seed=110),
              dict(cx=594, cy=1345, R=400, ang=-4, spread=42, seed=112),
              dict(cx=560, cy=1131, R=460, ang=-16, spread=46, seed=111)]:
        cv.layer(leaf_fields(**p, bbox=bb), right_clip)
    # bottom flap
    bline = H * (BOT_TIP_Y + (BOT_SIDE_Y - BOT_TIP_Y) * ax)
    bline = bline + 18 * np.exp(-((xx - W / 2) / 26) ** 2) * 0    # (apex rounding handled by blur below)
    bot = smooth01((yy - bline) / 1.6)
    bot = np.minimum(bot, 1)
    hb = flat_paper(H, W, 21) + 3.0 * np.exp(-(np.clip(yy - bline, 0, None) / 4.0) ** 2)
    hb += 2.0 * np.exp(-((xx - W / 2) / 3.0) ** 2) * (yy > H * 0.56)     # faint centre crease
    cv.panel(bot, hb, shadow=(0.55, 7, (2, 8)))
    # ginkgo sprig on the bottom flap: twig up the middle, leaves alternating, upper leaves on top
    twig = [(452 + 5 * math.sin(k / 9), H * 0.62 + k * (H * 0.40 / 40)) for k in range(41)]
    cv.layer(stem_fields(twig, 7, bb), bot)
    sprig = [dict(cx=450, cy=2080, R=560, ang=-92, spread=62, seed=130),     # fills the very bottom
             dict(cx=478, cy=1890, R=520, ang=-34, spread=50, seed=131),    # lower right
             dict(cx=455, cy=1770, R=660, ang=-146, spread=50, seed=132),   # lower left
             dict(cx=462, cy=1600, R=540, ang=-38, spread=50, seed=133),    # big right
             dict(cx=452, cy=1445, R=360, ang=-124, spread=46, seed=134)]   # upper left
    for p in sprig:
        cv.layer(leaf_fields(**p, bbox=bb), bot)
    bd = np.clip(yy - bline, 0, None)
    bedge = np.exp(-(bd / 3.0) ** 2) * bot
    cv.rgb = np.clip(cv.rgb * (1 + 0.10 * (1 - smooth01(bd / 26.0)) * bot)[..., None] + 52 * bedge[..., None], 0, 255)
    return cv.rgb, np.clip(np.maximum(sides, bot), 0, 1)

def build_flap():
    FH = int(H * 0.56)
    yy, xx = np.mgrid[0:FH, 0:W].astype(np.float32)
    ax = np.abs(xx - W / 2) / (W / 2)
    lim = H * (FLAP_TIP_Y - (FLAP_TIP_Y - FLAP_SIDE_Y) * ax)
    dist = lim - yy
    mask = smooth01((dist + 0.6) / 1.6)
    tint = tint_map(H, W, 5)[:FH]
    cv = Canvas(W, FH, tint)
    hp = flat_paper(FH, W, 31) + 3.5 * (1 - smooth01(dist / 9.0))      # rounded bevel along the flap edge
    cv.panel(mask, hp)
    bb = (W, FH)
    # all three spring from one point above the seal; the flap paper by the tip is left bare (as in the video)
    leaves = [dict(cx=468, cy=748, R=740, ang=-141, spread=30, seed=202),                 # left, its lower edge runs out to the side
              dict(cx=472, cy=751, R=830, ang=-86, spread=55, seed=203),                    # big central fan
              dict(cx=490, cy=800, R=700, ang=-47, spread=27, seed=201)]                    # right, lying over the fan
    for p in leaves:
        cv.layer(leaf_fields(**p, bbox=bb), mask)
    # re-light the bevel on top of the leaves so the flap edge reads as a clean folded edge
    edge = np.exp(-(np.clip(dist, 0, None) / 3.0) ** 2) * mask
    cv.rgb = np.clip(cv.rgb * (1 + 0.10 * (1 - smooth01(dist / 26.0)) * mask)[..., None] + 58 * edge[..., None], 0, 255)
    return cv.rgb, mask

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
    base = np.array([116, 104, 109], np.float32) * (0.96 + 0.08 * noise(SH, SW, 120, 3, 43))[..., None]
    lum = 0.20 + 0.42 * wrap + 0.36 * diff
    col = base * lum[..., None] + np.array([230, 222, 228], np.float32) * (0.55 * nh ** 22 + 0.14 * nh ** 5)[..., None]
    return np.clip(col, 0, 255), blob

def build_envelope():
    """-> body_rgb, body_alpha, flap_rgb, flap_alpha (tone-matched to the reference video)"""
    rgb, a = build_body()
    frgb, fa = build_flap()
    comp = rgb * a[..., None] + np.array([60, 48, 58], np.float32) * (1 - a[..., None])
    FH = frgb.shape[0]
    fs = np.zeros((H, W), np.float32); fs[:FH] = fa
    fs1 = cv2.GaussianBlur(cv2.warpAffine(fs, np.float32([[1, 0, 0], [0, 1, 5]]), (W, H)), (0, 0), 2.5)
    fs = cv2.GaussianBlur(cv2.warpAffine(fs, np.float32([[1, 0, 0], [0, 1, 21]]), (W, H)), (0, 0), 12)
    comp *= ((1 - 0.38 * fs1) * (1 - 0.62 * fs))[..., None]      # = the CSS drop-shadows of the flap                      # (the site draws this shadow with CSS)
    comp[:FH] = comp[:FH] * (1 - fa[..., None]) + frgb * fa[..., None]
    tm = tone_curve(comp)
    return tone_apply(rgb, tm), a, tone_apply(frgb, tm), fa

def preview(out):
    rgb, a, frgb, fa = build_envelope()
    comp = rgb * a[..., None] + np.array([60, 48, 58], np.float32) * (1 - a[..., None])
    FH = frgb.shape[0]
    fs = np.zeros((H, W), np.float32); fs[:FH] = fa
    fs1 = cv2.GaussianBlur(cv2.warpAffine(fs, np.float32([[1, 0, 0], [0, 1, 5]]), (W, H)), (0, 0), 2.5)
    fs = cv2.GaussianBlur(cv2.warpAffine(fs, np.float32([[1, 0, 0], [0, 1, 21]]), (W, H)), (0, 0), 12)
    comp *= ((1 - 0.38 * fs1) * (1 - 0.62 * fs))[..., None]      # = the CSS drop-shadows of the flap
    comp[:FH] = comp[:FH] * (1 - fa[..., None]) + frgb * fa[..., None]
    srgb, sa = build_seal()
    sw = int(W * 0.40); sh = int(sw * 660 / 600)
    srgb = cv2.resize(srgb, (sw, sh), interpolation=cv2.INTER_AREA); sa = cv2.resize(sa, (sw, sh), interpolation=cv2.INTER_AREA)
    x0 = W // 2 - sw // 2; y0 = int(H * 0.513) - sh // 2
    sh_m = np.zeros((H, W), np.float32); sh_m[y0:y0 + sh, x0:x0 + sw] = sa
    sh_m = cv2.GaussianBlur(cv2.warpAffine(sh_m, np.float32([[1, 0, 4], [0, 1, 9]]), (W, H)), (0, 0), 7)
    comp *= (1 - 0.5 * sh_m)[..., None]
    reg = comp[y0:y0 + sh, x0:x0 + sw]; reg[:] = reg * (1 - sa[..., None]) + srgb * sa[..., None]
    cv2.imwrite(str(out) + "/env_proto.png", cv2.cvtColor(comp.astype(np.uint8), cv2.COLOR_RGB2BGR))

if __name__ == "__main__":
    import time; t0 = time.time()
    preview(sys.argv[1] if len(sys.argv) > 1 else ".")
    print("done", round(time.time() - t0, 1), "s")
