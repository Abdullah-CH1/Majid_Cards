"""Generate every texture/image the wedding website uses (run once; outputs into ../assets).
All surfaces are built from height maps lit like real paper / wax / satin / nacre.
    python tools/make_assets.py            (all)
    python tools/make_assets.py envelope   (just one group: envelope, seal, satin, card, pearl, venue, photo)
"""
import sys, math
from pathlib import Path
import numpy as np, cv2

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "assets"
OUT.mkdir(exist_ok=True)
STUDIO_ASSETS = Path(r"F:\Wedding Card\Baraat Card Studio\assets")
rng = np.random.default_rng(7)
W, H = 900, 1950                      # 2x of a ~450 x 975 phone viewport

def hexrgb(h):
    h = h.lstrip("#"); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)

def noise(h, w, scale, octaves=4, seed=0):
    r = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        s = max(1, int(scale / (2 ** o)))
        g = r.random((h // s + 3, w // s + 3)).astype(np.float32)
        g = cv2.resize(g, (w + 3 * s, h + 3 * s), interpolation=cv2.INTER_CUBIC)[:h, :w]
        out += g * amp; tot += amp; amp *= 0.5
    return out / tot

def shade(hgt, base_rgb, light=(-0.55, -0.75, 0.65), depth=6.0, amb=0.55, kd=0.55, ks=0.25, shin=24,
          spec_rgb=(255, 255, 255)):
    """Lambert + Blinn specular on a height field. base_rgb: (h,w,3) or (3,)"""
    gy, gx = np.gradient(hgt * depth)
    n = np.dstack([-gx, -gy, np.ones_like(hgt)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    l = np.array(light, np.float32); l /= np.linalg.norm(l)
    v = np.array([0, 0, 1.0], np.float32)
    hv = (l + v); hv /= np.linalg.norm(hv)
    diff = np.clip((n * l).sum(2), 0, 1)
    spec = np.clip((n * hv).sum(2), 0, 1) ** shin
    base = np.broadcast_to(np.asarray(base_rgb, np.float32), hgt.shape + (3,))
    col = base * (amb + kd * diff)[..., None] + np.asarray(spec_rgb, np.float32) * (ks * spec)[..., None]
    return np.clip(col, 0, 255)

def save_rgb(name, rgb, q=90):
    p = OUT / name
    bgr = cv2.cvtColor(rgb.astype(np.uint8), cv2.COLOR_RGB2BGR)
    if name.endswith(".jpg"):
        cv2.imwrite(str(p), bgr, [cv2.IMWRITE_JPEG_QUALITY, q])
    else:
        cv2.imwrite(str(p), bgr, [cv2.IMWRITE_WEBP_QUALITY, q] if name.endswith(".webp") else [])
    print("wrote", p.name, rgb.shape[1], "x", rgb.shape[0])

def save_rgba(name, rgb, alpha, q=90):
    p = OUT / name
    bgra = np.dstack([cv2.cvtColor(rgb.astype(np.uint8), cv2.COLOR_RGB2BGR), (np.clip(alpha, 0, 1) * 255).astype(np.uint8)])
    cv2.imwrite(str(p), bgra, [cv2.IMWRITE_WEBP_QUALITY, q] if name.endswith(".webp") else [])
    print("wrote", p.name, rgb.shape[1], "x", rgb.shape[0])

def paper_grain(h, w, seed=1, amt=1.0):
    return (noise(h, w, 3, 2, seed) - 0.5) * 0.35 * amt + (noise(h, w, 60, 3, seed + 1) - 0.5) * 0.6 * amt

# ---------------------------------------------------------------- ginkgo relief
def smooth01(x):
    x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)

def ginkgo(hmap, cx, cy, R, ang, spread=62, lift=1.0, seed=0):
    """sculpt one ginkgo (fan) leaf on top of hmap (in place): soft rounded edges, pleats, a stem."""
    hh, ww = hmap.shape
    pad = int(R * 1.25) + 10
    x0, x1 = int(max(0, cx - pad)), int(min(ww, cx + pad))
    y0, y1 = int(max(0, cy - pad)), int(min(hh, cy + pad))
    if x0 >= x1 or y0 >= y1:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    dx, dy = xx - cx, yy - cy
    r = np.hypot(dx, dy)
    a = (np.degrees(np.arctan2(dy, dx)) - ang + 180) % 360 - 180
    t = a / spread
    rr = np.random.default_rng(seed); ph = rr.random() * 6.28
    edge = R * (1 - 0.06 * t ** 2 + 0.035 * np.sin(t * 7 + ph) + 0.02 * np.sin(t * 17 + 2 * ph))
    edge -= 0.16 * R * np.exp(-(t / 0.06) ** 2)                       # notch
    side = 1 - smooth01((np.abs(t) - 0.92) / 0.10)                     # soft fan sides
    rim = smooth01((edge - r) / 7.0)                                   # soft outer edge
    base_fade = smooth01((r - R * 0.05) / (R * 0.10))
    a_leaf = rim * side * base_fade
    rn = np.clip(r / np.maximum(edge, 1), 0, 1)
    dome = np.sin(rn * math.pi * 0.55) * (1 - 0.5 * t ** 2)
    pleat = 0.12 * np.cos(t * 7 * math.pi) * rn                      # broad folds
    fine = 0.035 * np.cos(t * 38 * math.pi) * (0.2 + rn)               # fine veins
    curl = 0.25 * smooth01((rn - 0.80) / 0.2)
    leaf = lift * (0.55 * dome + pleat + fine + curl)
    region = hmap[y0:y1, x0:x1]
    under = cv2.GaussianBlur(region, (0, 0), 6)
    region[:] = region * (1 - a_leaf) + (under * 0.6 + 0.12 + leaf) * a_leaf
    # stem from the leaf base
    sx = int(cx - math.cos(math.radians(ang)) * R * 0.45); sy = int(cy - math.sin(math.radians(ang)) * R * 0.45)
    stem = np.zeros_like(hmap); cv2.line(stem, (int(cx), int(cy)), (sx, sy), 1.0, max(3, int(R * 0.025)), cv2.LINE_AA)
    stem = cv2.GaussianBlur(stem, (0, 0), 2.0)
    hmap[:] = np.maximum(hmap, stem * (hmap.max() * 0 + 0.55))

def relief_shade(hm, col, depth=30, ao=0.55):
    """shade with ambient occlusion so overlapping leaves cast soft shadows"""
    blur = cv2.GaussianBlur(hm, (0, 0), 18)
    occl = np.clip((blur - hm) * 2.2, 0, 1)
    rgb = shade(hm, col, depth=depth, amb=0.66, kd=0.42, ks=0.16, shin=10, spec_rgb=(250, 242, 250))
    return np.clip(rgb * (1 - ao * occl)[..., None], 0, 255)

def envelope():
    print("envelope ...")
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    apex_y = H * 0.56; side_y = H * 0.80          # bottom flap: from the sides at 80% up to the centre
    # ---------- body ----------
    hm = np.zeros((H, W), np.float32)
    leaves = [
        (-30, 430, 400, 15), (930, 430, 400, 165), (110, 800, 360, -15), (790, 800, 360, -165),
        (290, 1020, 290, -60), (610, 1020, 290, -120),
        (60, 1180, 360, -35), (860, 1150, 360, -145), (150, 1480, 380, -60), (760, 1500, 380, -120),
        (450, 1300, 300, -90), (40, 1820, 420, -50), (880, 1840, 420, -130), (450, 1700, 360, -90),
        (300, 1960, 360, -80), (620, 1990, 360, -100),
    ]
    for i, (cx, cy, R, ang) in enumerate(leaves):
        ginkgo(hm, cx, cy, R, ang, seed=i)
    # bottom flap plateau + raised seam (the flap edges run from the bottom corners to the apex)
    tb = np.clip((yy - apex_y) / (side_y - apex_y), 0, 1)
    halfw = (W / 2) * tb * 1.02
    flap = smooth01((halfw - np.abs(xx - W / 2)) / 6.0) * (yy > apex_y)
    hm = hm * 0.85 + flap * 0.18
    seam = np.zeros_like(hm)
    pts = [(int(W / 2 + s * (W / 2) * (k / 40) ** 0.92), int(apex_y + (H - apex_y) * k / 40)) for s in (-1, 1) for k in range(41)]
    for s in (-1, 1):
        ps = [(int(W / 2 + s * (W / 2) * (k / 60)), int(apex_y + (side_y - apex_y) * k / 60)) for k in range(61)]
        cv2.polylines(seam, [np.array(ps, np.int32)], False, 1.0, 4, cv2.LINE_AA)
    hm += cv2.GaussianBlur(seam, (0, 0), 2.5) * 0.35
    hm = cv2.GaussianBlur(hm, (0, 0), 1.2) + (noise(H, W, 2, 2, 3) - 0.5) * 0.006
    col = hexrgb("#bba5b3") * (0.97 + 0.06 * noise(H, W, 400, 3, 9)[..., None])
    rgb = relief_shade(hm, col)
    vcut = yy < H * (0.31 + 0.19 * (1 - np.abs(xx - W / 2) / (W / 2)))     # top flap: from the sides at 31% down to the centre
    alpha = cv2.GaussianBlur(np.where(vcut, 0.0, 1.0).astype(np.float32), (0, 0), 0.8)
    save_rgba("envelope-body.webp", rgb, alpha, 88)
    # ---------- inside liner ----------
    liner = shade((noise(H, W, 2, 2, 5) - 0.5) * 0.05, hexrgb("#8e7987"), depth=10, amb=0.72, kd=0.28, ks=0.03)
    shadow = 1 - 0.35 * np.clip(1 - yy / (H * 0.5), 0, 1)
    save_rgb("envelope-inside.jpg", liner * shadow[..., None], 86)
    # ---------- top flap ----------
    FH = int(H * 0.50); fh = FH
    fm = np.zeros((fh, W), np.float32)
    fl = [(450, -120, 560, 90), (120, 60, 440, 62), (780, 60, 440, 118), (450, 250, 380, 90), (200, 470, 330, 60), (700, 470, 330, 120), (450, 560, 340, 90)]
    for i, (cx, cy, R, ang) in enumerate(fl):
        ginkgo(fm, cx, cy, R, ang, seed=30 + i)
    fy, fx = np.mgrid[0:fh, 0:W].astype(np.float32)
    lim = H * (0.31 + 0.19 * (1 - np.abs(fx - W / 2) / (W / 2)))
    fmask = smooth01((lim - fy) / 2.0)
    bevel = smooth01((lim - fy) / 14.0)
    fm = cv2.GaussianBlur(fm, (0, 0), 1.2) * bevel + bevel * 0.2 + (noise(fh, W, 2, 2, 7) - 0.5) * 0.006
    frgb = relief_shade(fm, hexrgb("#c2acba") * (0.97 + 0.06 * noise(fh, W, 300, 3, 4)[..., None]))
    save_rgba("envelope-flap.webp", frgb, fmask, 88)
    brgb = shade((noise(fh, W, 2, 2, 8) - 0.5) * 0.05, hexrgb("#a6909d"), depth=10, amb=0.74, kd=0.28, ks=0.03)
    save_rgba("envelope-flap-back.webp", brgb, fmask, 86)

# ---------------------------------------------------------------- wax seal
from PIL import Image, ImageDraw, ImageFont
SCRIPT_FONT = r"C:\Windows\Fonts\ITCEDSCR.TTF"
CONFIG_MONO = ("A", "L")

def text_mask(text, size, font=SCRIPT_FONT, canvas=(600, 600), offset=(0, 0)):
    im = Image.new("L", canvas, 0); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(font, size)
    bb = d.textbbox((0, 0), text, font=f)
    x = (canvas[0] - (bb[2] - bb[0])) / 2 - bb[0] + offset[0]
    y = (canvas[1] - (bb[3] - bb[1])) / 2 - bb[1] + offset[1]
    d.text((x, y), text, font=f, fill=255)
    return np.array(im, np.float32) / 255

def seal():
    print("seal ...")
    S = 560
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    c = S / 2
    ang = np.arctan2(yy - c, xx - c); r = np.hypot(xx - c, yy - c)
    R = 230 + 10 * np.sin(ang * 5 + 1) + 6 * np.sin(ang * 11 + 2) + 4 * np.sin(ang * 23)   # irregular wax edge
    blob = smooth01((R - r) / 5)
    dome = np.sqrt(np.clip(1 - (r / (R + 1)) ** 2, 0, 1))
    hm = dome * 0.9
    ring_r = 168
    ring = np.exp(-((r - ring_r) / 13) ** 2)                 # raised rim of the stamp
    recess = smooth01((ring_r - 12 - r) / 6)                 # pressed centre
    hm = hm + ring * 0.45 - recess * 0.35
    m1 = text_mask(CONFIG_MONO[0], 250, canvas=(S, S), offset=(-34, -18))
    m2 = text_mask(CONFIG_MONO[1], 250, canvas=(S, S), offset=(38, 22))
    mono = cv2.GaussianBlur(np.maximum(m1, m2), (0, 0), 2.2)
    hm = hm + mono * 0.42 * recess
    dots = np.zeros_like(hm)
    for k in range(48):
        a = k / 48 * 2 * math.pi
        cv2.circle(dots, (int(c + (ring_r - 26) * math.cos(a)), int(c + (ring_r - 26) * math.sin(a))), 3, 1.0, -1, cv2.LINE_AA)
    hm = hm + cv2.GaussianBlur(dots, (0, 0), 1.2) * 0.18 * recess
    hm = cv2.GaussianBlur(hm, (0, 0), 1.0)
    col = hexrgb("#9d8b98") * (0.95 + 0.1 * noise(S, S, 60, 3, 2)[..., None])
    rgb = shade(hm, col, depth=55, amb=0.48, kd=0.55, ks=0.55, shin=22, spec_rgb=(255, 246, 255))
    save_rgba("seal.webp", rgb, blob, 92)

# ---------------------------------------------------------------- satin
def satin():
    print("satin ...")
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    warp = (noise(H, W, 700, 3, 11) - 0.5) * 180
    u = (xx * 0.55 + yy * 0.45 + warp) / 120
    hm = 0.6 * np.sin(u) + 0.3 * np.sin(u * 0.53 + 1.3)                       # long diagonal folds
    hm += 0.35 * np.sin((xx * -0.75 + yy * 0.66 + warp * 0.8) / 170)          # crossing folds
    hm += 0.55 * (noise(H, W, 420, 3, 12) - 0.5)
    hm = cv2.GaussianBlur(hm.astype(np.float32), (0, 0), 9)
    col = hexrgb("#cbb6c4") * (0.97 + 0.05 * noise(H, W, 600, 2, 13)[..., None])
    rgb = shade(hm, col, light=(-0.35, -0.6, 0.72), depth=55, amb=0.64, kd=0.40, ks=0.20, shin=22, spec_rgb=(255, 248, 255))
    save_rgb("satin.jpg", rgb, 88)

# ---------------------------------------------------------------- organza bow + ribbon band
def _poly_mask(shape, pts, blur=1.2):
    m = np.zeros(shape, np.uint8)
    cv2.fillPoly(m, [np.array(pts, np.int32)], 255, cv2.LINE_AA)
    return cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), blur)

def _bez(p0, p1, p2, p3, n=50):
    return [((1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0],
             (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]) for t in np.linspace(0, 1, n)]

def _organza(mask, hm, base="#efe3ec", alpha_body=0.55, edge_alpha=0.9):
    """translucent sheer fabric: brighter hem at the edges, sheen from the folds"""
    dist = cv2.distanceTransform((mask > 0.5).astype(np.uint8), cv2.DIST_L2, 5)
    hem = np.exp(-dist / 3.0) * (mask > 0.02)
    rgb = shade(hm, hexrgb(base), light=(-0.3, -0.7, 0.65), depth=60, amb=0.75, kd=0.3, ks=0.6, shin=10)
    sheen = np.clip((rgb.mean(2) - 200) / 55, 0, 1)
    a = mask * (alpha_body + 0.35 * sheen) + hem * (edge_alpha - alpha_body)
    return rgb, np.clip(a, 0, 0.97)

def bow():
    print("bow ...")
    BW, BH = 900, 760
    cx, cy = 450, 330
    shape = (BH, BW)
    loops, tails = [], []
    for s in (-1, 1):
        loops.append(_bez((cx, cy), (cx + s * 120, cy - 230), (cx + s * 400, cy - 190), (cx + s * 330, cy + 10)) +
                     _bez((cx + s * 330, cy + 10), (cx + s * 290, cy + 120), (cx + s * 130, cy + 70), (cx, cy)))
        tails.append(_bez((cx - s * 10, cy + 10), (cx + s * 60, cy + 160), (cx + s * 130, cy + 300), (cx + s * 240, cy + 410)) +
                     _bez((cx + s * 300, cy + 360), (cx + s * 190, cy + 250), (cx + s * 90, cy + 140), (cx + s * 30, cy + 15)))
    rgb_all = np.zeros(shape + (3,), np.float32); a_all = np.zeros(shape, np.float32)
    yy, xx = np.mgrid[0:BH, 0:BW].astype(np.float32)
    for i, pts in enumerate(tails + loops):
        m = _poly_mask(shape, pts)
        hm = cv2.GaussianBlur(m, (0, 0), 18) * 1.4 + 0.07 * np.sin((xx * 0.8 + yy * (0.6 if i % 2 else -0.6)) / 34) * m
        hm += 0.12 * (noise(BH, BW, 120, 2, 40 + i) - 0.5) * m
        rgb, a = _organza(m, hm, alpha_body=0.42)
        rgb_all = rgb_all * (1 - a[..., None]) + rgb * a[..., None]
        a_all = a_all + a * (1 - a_all)
    km = np.zeros(shape, np.float32); cv2.ellipse(km, (cx, cy + 4), (46, 40), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
    km = cv2.GaussianBlur(km, (0, 0), 1.5)
    khm = cv2.GaussianBlur(km, (0, 0), 10) * 2 + 0.2 * np.sin(yy / 6) * km
    krgb, ka = _organza(km, khm, base="#e9dbe6", alpha_body=0.85)
    rgb_all = rgb_all * (1 - ka[..., None]) + krgb * ka[..., None]
    a_all = a_all + ka * (1 - a_all)
    save_rgba("bow.webp", rgb_all, a_all, 92)
    RH = 150
    yy2, xx2 = np.mgrid[0:RH, 0:W].astype(np.float32)
    gather = 1 - 0.45 * np.exp(-((xx2 - W / 2) / 140) ** 2)
    half = 52 * gather
    m = smooth01((half - np.abs(yy2 - RH / 2)) / 1.5)
    hm = 0.6 * np.cos((yy2 - RH / 2) / np.maximum(half, 1) * 1.4) + 0.15 * np.sin(xx2 / 37) \
         + 0.5 * np.exp(-((xx2 - W / 2) / 150) ** 2) * np.sin((yy2 - RH / 2) / 5)
    rgb, a = _organza(m, hm.astype(np.float32), alpha_body=0.5)
    save_rgba("ribbon.webp", rgb, a, 92)

# ---------------------------------------------------------------- embossed card
def _wreath_piece(box, size, rot=0):
    im = cv2.imread(str(STUDIO_ASSETS / "engraved-flower-wreath-cut.png"), cv2.IMREAD_UNCHANGED).astype(np.float32)
    x0, y0, x1, y1 = box
    crop = im[y0:y1, x0:x1]
    ink = np.clip((crop[..., 3] / 255) * (1 - crop[..., :3].mean(2) / 255) * 1.6, 0, 1)
    # merge the engraving's stipple dots into smooth sculpted petals, keep a little of the fine detail
    body = cv2.GaussianBlur(ink, (0, 0), 3.5)
    body = smooth01((body - 0.10) / 0.25)
    body = cv2.GaussianBlur(body, (0, 0), 4)
    ink = body * 0.85 + cv2.GaussianBlur(ink, (0, 0), 1.2) * 0.25
    h, w = ink.shape; sc = size / max(h, w)
    ink = cv2.resize(ink, (int(w * sc), int(h * sc)), interpolation=cv2.INTER_AREA)
    if rot:
        hh, ww = ink.shape; d = int(math.hypot(hh, ww)) + 4
        pad = np.zeros((d, d), np.float32); pad[(d - hh) // 2:(d - hh) // 2 + hh, (d - ww) // 2:(d - ww) // 2 + ww] = ink
        ink = cv2.warpAffine(pad, cv2.getRotationMatrix2D((d / 2, d / 2), rot, 1), (d, d))
    return ink

def _stamp(hm, piece, cx, cy, amt=1.0):
    h, w = piece.shape; x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(hm.shape[1], x0 + w), min(hm.shape[0], y0 + h)
    if xa < xb and ya < yb:
        hm[ya:yb, xa:xb] = np.maximum(hm[ya:yb, xa:xb], piece[ya - y0:yb - y0, xa - x0:xb - x0] * amt)

def frame_path(x0, y0, x1, y1, peak=70, notch=34):
    """scalloped cartouche: concave corner notches, ogee peak at top and bottom"""
    cxm = (x0 + x1) / 2
    top = [(x0, y0 + notch)]
    top += [(x0 + notch - notch * math.cos(a), y0 + notch - notch * math.sin(a)) for a in np.linspace(0, math.pi / 2, 12)][1:]
    top += _bez((x0 + notch, y0), (cxm - 120, y0), (cxm - 70, y0), (cxm - 55, y0 - peak * 0.45), 20)
    top += _bez((cxm - 55, y0 - peak * 0.45), (cxm - 40, y0 - peak), (cxm - 10, y0 - peak), (cxm, y0 - peak), 16)
    right = [(2 * cxm - x, y) for x, y in reversed(top)]
    upper = top + right[1:]
    lower = [(x, y0 + y1 - y) for x, y in reversed(upper)]
    return upper + lower[1:]

# ---------------------------------------------------------------- mother of pearl
def pearl():
    print("pearl ...")
    PH = 1500
    yy, xx = np.mgrid[0:PH, 0:W].astype(np.float32)
    w1 = noise(PH, W, 520, 3, 31); w2 = noise(PH, W, 520, 3, 32)
    u = noise(PH, W, 260, 3, 33)
    mapx = np.clip(xx + (w1 - 0.5) * 300, 0, W - 1).astype(np.float32); mapy = np.clip(yy + (w2 - 0.5) * 300, 0, PH - 1).astype(np.float32)
    v = cv2.remap(u, mapx, mapy, cv2.INTER_LINEAR)
    v = cv2.GaussianBlur((v - v.min()) / (v.max() - v.min()), (0, 0), 3)
    bands = np.sin(v * 13) * 0.5 + 0.5
    pal = np.array([hexrgb(c) for c in ("#837a90", "#b2a9bf", "#e3dbe6", "#f6f2f6", "#d6c6d4", "#c0c8d8", "#ead9e1", "#9d94ad")])
    idx = (v * 0.65 + bands * 0.35) * (len(pal) - 1)
    i0 = np.floor(idx).astype(int).clip(0, len(pal) - 2); f = (idx - i0)[..., None]
    col = pal[i0] * (1 - f) + pal[i0 + 1] * f
    hm = cv2.GaussianBlur((v * 0.6 + bands * 0.12).astype(np.float32), (0, 0), 3)
    rgb = shade(hm, col, light=(-0.4, -0.6, 0.7), depth=45, amb=0.74, kd=0.32, ks=0.3, shin=20, spec_rgb=(255, 252, 255))
    vig = 1 - 0.25 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - PH / 2) / (PH / 2)) ** 2)
    save_rgb("pearl.jpg", rgb * vig[..., None], 88)

# ---------------------------------------------------------------- venue sketch + photo placeholder
def venue():
    print("venue ...")
    im = cv2.imread(str(STUDIO_ASSETS / "taj-mahal-elevation-painting.webp"))[100:1172, 280:1722]
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    bg = cv2.GaussianBlur(g, (0, 0), 25)
    ink = np.clip((bg - g - 9) / 55, 0, 1) ** 0.85             # threshold drops the paper fibres
    ink = cv2.resize(ink, (1200, int(1200 * ink.shape[0] / ink.shape[1])), interpolation=cv2.INTER_AREA)
    rgb = np.broadcast_to(hexrgb("#4a4452"), ink.shape + (3,))
    save_rgba("venue-sketch.webp", rgb, np.clip(ink * 1.6, 0, 1), 90)

def photo():
    print("photo placeholder ...")
    PW, PHh = 600, 760
    yy, xx = np.mgrid[0:PHh, 0:PW].astype(np.float32)
    g = 1 - 0.7 * (((xx - PW / 2) / PW) ** 2 + ((yy - PHh / 2) / PHh) ** 2)
    base = hexrgb("#7d6a7a")[None, None, :] * g[..., None]
    m = cv2.GaussianBlur(text_mask("A & L", 190, canvas=(PW, PHh), offset=(0, -40)), (0, 0), 0.8)
    rgb = base * (1 - m[..., None]) + hexrgb("#f5ecf2") * m[..., None]
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 26)
    msg = "replace with your photo"; bb = d.textbbox((0, 0), msg, font=f)
    d.text(((PW - bb[2]) / 2, PHh * 0.68), msg, font=f, fill=(240, 228, 236))
    im.save(OUT / "photo.jpg", quality=90); print("wrote photo.jpg")

# ================================================================ v2: sheer organza, 3D bow, rose card
def organza():
    """crinkled sheer organza sheet (RGBA) that lies over the card"""
    print("organza ...")
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    h = np.zeros((H, W), np.float32)
    for k, (sc, amp) in enumerate(((260, 0.9), (120, 0.45), (56, 0.18))):
        n = noise(H, W, sc, 2, 50 + k)
        h += amp * (1 - np.abs(2 * n - 1)) ** 3                    # ridged noise = crisp crinkles
    warp = (noise(H, W, 600, 2, 60) - 0.5) * 200
    h += 0.35 * np.sin((xx * 0.5 + yy * 0.55 + warp) / 140)         # soft drape
    h = cv2.GaussianBlur(h, (0, 0), 2.0)
    gy, gx = np.gradient(h * 18)
    nrm = np.dstack([-gx, -gy, np.ones_like(h)]); nrm /= np.linalg.norm(nrm, axis=2, keepdims=True)
    l = np.array([-0.4, -0.7, 0.6]); l /= np.linalg.norm(l); hv = l + [0, 0, 1]; hv /= np.linalg.norm(hv)
    diff = np.clip((nrm * l).sum(2), 0, 1); spec = np.clip((nrm * hv).sum(2), 0, 1) ** 40
    fres = 1 - nrm[..., 2]
    base = hexrgb("#f1e6ef")
    rgb = base * (0.80 + 0.25 * diff)[..., None] + 255 * (0.9 * spec)[..., None]
    a = np.clip(0.24 + 1.7 * fres + 0.65 * spec, 0, 0.85)
    save_rgba("organza.webp", np.clip(rgb, 0, 255), a, 86)

def bow_frames(n=24):
    """3D organza bow + its untie animation as numbered frames, plus the band"""
    sys.path.insert(0, str(HERE))
    import ribbon3d as R
    print("band ...")
    rgb, a = R.rasterize(R.band_quads(), 900, 220)
    save_rgba("ribbon.webp", rgb, a, 92)
    fdir = OUT / "bow"; fdir.mkdir(exist_ok=True)
    for i in range(n):
        u = i / (n - 1)
        rgb, a = R.rasterize(R.bow_quads(u), 900, 760)
        save_rgba(f"bow/bow-{i:02d}.webp", rgb, a, 88)

def _rose_relief(name, size, rot=0, flip=False, detail=1.0):
    im = cv2.imread(str(STUDIO_ASSETS / name), cv2.IMREAD_UNCHANGED).astype(np.float32)
    a = im[..., 3] / 255; g = cv2.cvtColor(im[..., :3].astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    # relief: soft silhouette dome + carved detail from the painting's light/dark
    sil = cv2.GaussianBlur(a, (0, 0), 6)
    hp = g - cv2.GaussianBlur(g, (0, 0), 5)
    hgt = sil * 0.55 + a * (0.35 * (1 - g)) + a * hp * 1.6 * detail
    if flip:
        hgt = hgt[:, ::-1]
    h, w = hgt.shape; sc = size / max(h, w)
    hgt = cv2.resize(hgt, (int(w * sc), int(h * sc)), interpolation=cv2.INTER_AREA)
    if rot:
        hh, ww = hgt.shape; d = int(math.hypot(hh, ww)) + 4
        pad = np.zeros((d, d), np.float32); pad[(d - hh) // 2:(d - hh) // 2 + hh, (d - ww) // 2:(d - ww) // 2 + ww] = hgt
        hgt = cv2.warpAffine(pad, cv2.getRotationMatrix2D((d / 2, d / 2), rot, 1), (d, d))
    return hgt

def arch_path(x0, x1, ytop, ybot, shoulder=60, peak=95, cusp=26):
    """tall Mughal-arch cartouche: straight sides, cusped shoulders, ogee peak (mirrored at the bottom)"""
    cx = (x0 + x1) / 2
    half = []
    half += [(x0, ytop + shoulder + cusp)]
    # concave cusp at the shoulder
    for a in np.linspace(math.pi, math.pi * 1.5, 14):
        half.append((x0 + cusp + cusp * math.cos(a), ytop + shoulder + cusp + cusp * math.sin(a)))
    sx = x0 + cusp
    half += _bez((sx, ytop + shoulder), (sx + 70, ytop + shoulder), (sx + 95, ytop + shoulder - 30), (sx + 120, ytop + shoulder - 34), 18)[1:]
    half += _bez((sx + 120, ytop + shoulder - 34), (cx - 120, ytop + shoulder - 40), (cx - 40, ytop + 20), (cx, ytop - peak + shoulder - 20), 30)[1:]
    right = [(2 * cx - x, y) for x, y in reversed(half)]
    top = half + right[1:]
    bottom = [(x, ytop + ybot - y) for x, y in reversed(top)]
    return top + bottom[1:]

def card():
    print("card (v2) ...")
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    frame = np.array(arch_path(112, 788, 300, 1650), np.float32)
    inner = np.array(arch_path(134, 766, 322, 1628), np.float32)
    panel = np.zeros((H, W), np.float32); cv2.fillPoly(panel, [frame.astype(np.int32)], 1.0, cv2.LINE_AA)
    keep_out = cv2.GaussianBlur(cv2.dilate(panel, np.ones((41, 41), np.uint8)), (0, 0), 6)
    roses = np.zeros((H, W), np.float32)
    def put(hgt, cx, cy, amt=1.0):
        h, w = hgt.shape; x0, y0 = int(cx - w / 2), int(cy - h / 2)
        xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
        if xa < xb and ya < yb:
            roses[ya:yb, xa:xb] = np.maximum(roses[ya:yb, xa:xb], hgt[ya - y0:yb - y0, xa - x0:xb - x0] * amt)
    put(_rose_relief("rose-redoute-pink-cabbage-cut.png", 520, rot=-38), 150, 210)
    put(_rose_relief("rose-redoute-pink-single-cut.png", 520, rot=40, flip=True), 755, 210)
    put(_rose_relief("rose-redoute-pink-single-cut.png", 520, rot=-150), 150, 1745)
    put(_rose_relief("rose-redoute-pink-cabbage-cut.png", 520, rot=148, flip=True), 755, 1745)
    for i, y in enumerate((620, 990, 1360)):                       # climbing briar vines up both sides
        put(_rose_relief("rose-redoute-blush-briar-cut.png", 380, rot=(8 if i % 2 else -8)), 54, y, 0.85)
        put(_rose_relief("rose-redoute-blush-briar-cut.png", 380, rot=(-8 if i % 2 else 8), flip=True), 846, y, 0.85)
    put(_rose_relief("rose-redoute-blush-briar-cut.png", 300, rot=90), 450, 120, 0.7)  # small spray above the peak
    put(_rose_relief("rose-redoute-blush-briar-cut.png", 300, rot=-90), 450, 1830, 0.7)
    roses *= (1 - keep_out)                                         # nothing touches the frame
    fr = np.zeros((H, W), np.float32)
    cv2.polylines(fr, [frame.astype(np.int32)], True, 1.0, 4, cv2.LINE_AA)
    cv2.polylines(fr, [inner.astype(np.int32)], True, 0.6, 2, cv2.LINE_AA)
    mid = np.array(arch_path(123, 777, 311, 1639), np.float32)
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(np.vstack([mid, mid[:1]]), axis=0).T))]
    for dd in np.arange(0, seg[-1], 10):
        i = int(np.clip(np.searchsorted(seg, dd) - 1, 0, len(mid) - 1)); j = (i + 1) % len(mid)
        f = (dd - seg[i]) / max(seg[i + 1] - seg[i], 1e-3)
        x, y = mid[i] + (mid[j] - mid[i]) * f
        cv2.circle(fr, (int(round(x)), int(round(y))), 2, 0.9, -1, cv2.LINE_AA)
    fr = cv2.GaussianBlur(fr, (0, 0), 1.1)
    hgt = roses * 0.9 + fr * 0.75 + cv2.GaussianBlur(panel, (0, 0), 2) * 0.06 + (noise(H, W, 2, 2, 21) - 0.5) * 0.002
    sheen = 0.96 + 0.07 * np.sin((xx * 0.6 + yy * 0.4) / 380) + 0.03 * noise(H, W, 500, 2, 22)
    col = hexrgb("#c6b5c1") * sheen[..., None]
    rgb = shade(hgt, col, light=(-0.5, -0.7, 0.62), depth=42, amb=0.62, kd=0.44, ks=0.26, shin=16, spec_rgb=(255, 246, 252))
    save_rgb("card.jpg", rgb, 92)

if __name__ == "__main__":
    which = sys.argv[1:] or ["envelope", "seal", "satin", "bow", "card", "pearl", "venue", "photo"]
    for w in which:
        globals()[w]()
