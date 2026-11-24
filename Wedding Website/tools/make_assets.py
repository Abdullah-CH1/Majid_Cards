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

def _genv():
    sys.path.insert(0, str(HERE))
    import ginkgo_env
    return ginkgo_env

def ginkgo(cx, cy, R, ang, **kw):
    """one sculpted ginkgo leaf layer (alpha + height field); the engine lives in tools/ginkgo_env.py"""
    G = _genv(); kw.setdefault("bbox", (W, H))
    return G.leaf_fields(cx, cy, R, ang, **kw)

def relief_shade(hm, tint):
    """pearly satin lighting of a height field (tint 0 = silver-lilac, 1 = pink-mauve)"""
    return _genv().pearl_shade(hm, tint)

def envelope():
    """envelope front matching the reference video: big sculpted ginkgo leaves, pearly mauve, top flap from the
    sides (33.5%) to the tip under the seal (53.5%), envelope mouth under it, bottom flap rising to the seal."""
    print("envelope ... (about 2 minutes)")
    G = _genv()
    rgb, a, frgb, fa = G.build_envelope()
    save_rgba("envelope-body.webp", rgb, a, 90)
    save_rgba("envelope-flap.webp", frgb, fa, 90)
    # the same flap darkened (cross-faded in while it turns away from the light) -- no CSS masks: they fail on file://
    save_rgba("envelope-flap-dim.webp", frgb * np.array([0.40, 0.36, 0.40], np.float32), fa, 86)
    # soft shadow the closed flap casts on the envelope: contact + wide shadow, pre-blurred (900 x 1152)
    fh = frgb.shape[0]; pad = 60
    m = np.zeros((fh + pad, W), np.float32); m[:fh] = fa
    sh1 = cv2.GaussianBlur(cv2.warpAffine(m, np.float32([[1, 0, 0], [0, 1, 5]]), (W, fh + pad)), (0, 0), 2.5)
    sh2 = cv2.GaussianBlur(cv2.warpAffine(m, np.float32([[1, 0, 0], [0, 1, 21]]), (W, fh + pad)), (0, 0), 12)
    sa = 1 - (1 - 0.38 * sh1) * (1 - 0.62 * sh2)
    save_rgba("envelope-flap-shadow.webp", np.broadcast_to(np.array([25, 14, 22], np.float32), (fh + pad, W, 3)), sa, 86)
    # back of the flap (only seen edge-on while it lifts): plain paper of the same tone
    fh = frgb.shape[0]
    brgb = shade((noise(fh, W, 3, 2, 8) - 0.5) * 0.05, hexrgb("#a8959f"), depth=10, amb=0.74, kd=0.28, ks=0.03)
    save_rgba("envelope-flap-back.webp", brgb, fa, 86)

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
    """oval wax seal like the reference: thick irregular rounded rim, pressed oval with a double border,
    raised script monogram (CONFIG_MONO), little air pits; 600 x 660"""
    print("seal ...")
    rgb, blob = _genv().build_seal(CONFIG_MONO)
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
# colour statistics measured from the reference video (6 x 6 cells over the section, already corrected for the
# camera's exposure): the darkest and the brightest nacre tone found in each cell. Only these 72 colours come
# from the video; every streak, ring and cloud below is generated.
NACRE_LO = """7b6f79 7c727c 8a828c 8d808a 8e828e 827883
776e79 80747d 827984 8c818c 8c7e89 9d95a3
776e79 736a75 7c737e 847883 74666f 897986
6b6976 6a6573 716675 7d6d7b 857887 826f7f
6d636f 675f70 7b6a7a 786878 827080 806474
68606a 626070 646472 786a7a 896c80 836774"""
NACRE_HI = """97909a aaa3b0 e2dee8 cfc3d0 ffffff ffffff
9b909a aea5b0 f8f8ff dbd5e0 ffffff ffffff
9a929c 978a95 b8b1bd eeebf9 e1e0f0 ffffff
8d8993 7e7987 948694 c4b8c7 e4ddeb fff9ff
8f8993 887889 9d8794 a99cab c8b8cb f1dbe6
928c96 86828f 8f818f bba3b1 d5b8cb d3b4c4"""

def _palette_map(txt, S):
    g = np.array([[hexrgb(c) for c in row.split()] for row in txt.strip().splitlines()], np.float32)
    n = g.shape[0]
    g = np.pad(g, ((1, 1), (1, 1), (0, 0)), mode="edge")
    big = cv2.resize(g, (S * (n + 2) // n, S * (n + 2) // n), interpolation=cv2.INTER_CUBIC)
    o = S // n
    big = big[o:o + S, o:o + S]
    return cv2.GaussianBlur(big, (0, 0), S / n * 0.45)

def _polar_noise(NA, NR, sa, sr, seed, octaves=3):
    """noise on an (angle, log-radius) grid, periodic in angle; sa/sr = feature size in samples"""
    K = NA // 6
    n = noise(NA + K, NR, 4, 1, seed)                       # white-ish
    out = np.zeros_like(n); amp = 1.0; tot = 0
    for o in range(octaves):
        out += cv2.GaussianBlur(n if o == 0 else noise(NA + K, NR, 4, 1, seed + 17 * o), (0, 0), sigmaX=sr / 2 ** o, sigmaY=sa / 2 ** o) * amp
        tot += amp; amp *= 0.55
    out /= tot
    w = np.linspace(0, 1, K, dtype=np.float32)[:, None]
    out[:K] = out[NA:NA + K] * (1 - w) + out[:K] * w         # cross-fade the seam
    out = out[:NA]
    return (out - out.mean()) / (out.std() + 1e-6)

def _rank01(f):
    """histogram-equalise to a uniform 0..1 field"""
    flat = f.ravel(); order = np.argsort(flat, kind="stable")
    r = np.empty_like(order, dtype=np.float32); r[order] = np.linspace(0, 1, flat.size, dtype=np.float32)
    return r.reshape(f.shape)

def nacre(S=1200, P=None):
    """mother-of-pearl as in the reference video: foggy grey-mauve shell, soft clouds, broad growth rings round the
    cameo, feathery streaks that zig-zag from ring to ring, silver-white flames towards the upper right, rose
    towards the lower right. Square; the cameo sits on the centre."""
    P = dict(swirl=0.12, zig=0.06, warp=0.8, cx=0.503, cy=0.503, w_iso=1.15, w_cloud=0.45, w_feather=0.3, w_fine=0.08, w_ring=0.26, flame=0.85,
             t0=0.29, t1=0.25, t2=0.05, emboss=0.03, blur=1.6, **(P or {}))
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    dx, dy = (xx / S - P["cx"]), (yy / S - P["cy"])
    warp1 = (noise(S, S, int(S / 1.6), 2, 61) - 0.5) * 1.6; warp2 = (noise(S, S, S // 3, 3, 62) - 0.5)
    r = np.hypot(dx, dy * 0.92) + 1e-4
    th = np.arctan2(dy, dx)
    rr = r + 0.085 * warp2 + 0.03 * warp1                                   # ring radius, gently wobbling
    lam = 0.066                                             # ring spacing (of the section width)
    band = rr / (2 * lam)                                   # one overlapping "scale" of nacre per two rings
    bi = np.floor(band); bf = band - bi
    tri = np.abs(((band * 0.5) % 1.0) * 2 - 1) * 2 - 1      # -1..1: the barbs lean one way, then the other (soft chevrons)
    NA, NR = 2880, 1024
    lr = np.log(r / 0.05) / np.log(1.0 / 0.05)
    a0 = th + P["swirl"] * np.log(r / 0.3) + warp1 * P["warp"]
    ri = np.clip((lr + warp2 * 0.05) * NR, 0, NR - 1).astype(np.float32)
    def samp(pn, a):
        ai = np.minimum((((a / (2 * np.pi)) % 1.0) * NA).astype(np.float32), NA - 1.001)
        return cv2.remap(np.vstack([pn, pn[:1]]), ri, ai, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    ab = a0 + P["zig"] * tri * 0.3 / np.maximum(r, 0.15)       # barbs lean one way, then the other
    cloud = samp(_polar_noise(NA, NR, 70, 45, 71, 2), a0)       # broad flames
    feather = samp(_polar_noise(NA, NR, 13, 22, 72, 2), ab)     # feather barbs
    fine = samp(_polar_noise(NA, NR, 5, 14, 73, 2), ab)       # hair-fine striation
    iso = noise(S, S, S // 4, 4, 74); iso = (iso - iso.mean()) / iso.std()
    mott = noise(S, S, S // 13, 3, 76); mott = (mott - mott.mean()) / mott.std()      # small mottling inside the flames
    ringp = rr / lam * 2 * np.pi
    rings = np.sin(ringp) * (0.6 + 0.4 * np.sin(ringp * 0.37 + 1.0))
    lo = _palette_map(NACRE_LO, S); hi = _palette_map(NACRE_HI, S)
    span = hi.mean(2) - lo.mean(2)
    calm = 1 - smooth01((span - 45) / 80)                   # 1 where the shell is quiet (left, bottom)
    lively = 1 - calm
    edge = 1 - 0.10 * np.exp(-bf / 0.22) * (0.3 + calm)     # each scale is a touch darker under the lip of the next one
    f = (P["w_iso"] * iso + P["w_cloud"] * cloud + (P["w_feather"] * feather + P["w_fine"] * fine) * (0.4 + 0.4 * lively)
         + P["w_ring"] * rings * (0.2 + 0.7 * calm))
    z = (f - f.mean()) / f.std()
    flame = smooth01((0.75 * iso + 0.5 * cloud + 0.3 * mott + 0.36 * feather + 0.1 * fine + 0.9) / 2.6)   # silver flames, feathered along the barbs
    t = P["t0"] + P["t1"] * z + P["t2"] * z * np.abs(z) + P["flame"] * lively * flame
    glint = smooth01((feather + 0.7 * fine + 0.5 * mott - 1.5) / 0.9)       # small wet highlights
    t = t + lively * (0.10 * mott + 0.12 * feather + 0.06 * fine)             # the flames are mottled and barbed, never flat
    t = np.clip(t * edge + 0.5 * glint * (0.15 + lively), -0.1, 1.4)
    col = lo + (hi - lo) * t[..., None]
    ice = (smooth01((col.mean(2) - 165) / 70) * 0.8)[..., None]              # the brightest nacre turns a cool blue-white
    col = col * (1 - ice) + np.minimum(col, 255) * np.array([0.945, 0.96, 1.02], np.float32) * ice
    # growth rings where the shell is calm: broad soft bands, a pale lip on each scale, a little fog
    lip = np.exp(-((bf - 0.06) / 0.05) ** 2) * (0.5 + 0.5 * np.sin(a0 * 3 + bi * 2.4))
    col += ((rings * 3.0 + lip * 5.0 + iso * 3.0 + cloud * 2.0 + feather * 1.0) * (0.2 + calm))[..., None]
    # keep the broad light/dark layout of the shell on the measured palette (clouds must not drift it)
    want = cv2.GaussianBlur(lo + (hi - lo) * 0.38, (0, 0), S / 7)
    have = cv2.GaussianBlur(col, (0, 0), S / 7)
    col *= (want / np.maximum(have, 1)) ** 0.75
    # gloss: light rakes across the relief from the upper left
    hm = cv2.GaussianBlur(z, (0, 0), 2.5)
    gy, gx = np.gradient(hm)
    emb = np.clip((-gx * 0.6 - gy * 0.8) * 10, -1, 1)
    col *= (1 + P["emboss"] * emb)[..., None]
    # slow iridescent drift: rose <-> sea-green
    hue = (noise(S, S, S // 5, 3, 75) - 0.5) * 1.6 - 0.4 * lively          # the lively nacre runs cooler (silver-blue)
    hue2 = (noise(S, S, S // 7, 2, 77) - 0.5) * 2.2 * calm                    # rose and blue-grey bloom in the calm shell
    col *= np.dstack([1 + 0.04 * hue + 0.05 * hue2, 1 - 0.025 * hue - 0.02 * hue2, 1 - 0.035 * hue - 0.045 * hue2])
    col = cv2.GaussianBlur(col, (0, 0), P["blur"])
    return np.clip(col, 0, 255)


def pearl():
    print("pearl ...")
    save_rgb("pearl.jpg", nacre(1200), 90)

# ---------------------------------------------------------------- venue sketch + photo placeholder
def venue_sketch():
    im = cv2.imread(str(STUDIO_ASSETS / "taj-mahal-elevation-painting.webp"))[100:1172, 280:1722]
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    bg = cv2.GaussianBlur(g, (0, 0), 30)
    paper = np.percentile(g, 92)
    tone = np.clip((np.minimum(paper, bg + 4) - g - 10) / 110, 0, 1)                         # broad pencil shading (washes, shadows)
    tone = cv2.GaussianBlur(tone, (0, 0), 1.0)
    line = np.clip((bg - g - 6) / 45, 0, 1) ** 0.8                  # crisp outlines / details
    a = np.clip(line * 1.6 + tone * 1.05, 0, 1)
    h, w = a.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    # soft irregular vignette at the bottom and sides, like a sketch fading into the page
    n = noise(h, w, 90, 3, 77)
    fade = smooth01((1 - np.abs(xx / w - 0.5) * 2) / 0.02) * smooth01(((h - yy) / h + (n - 0.5) * 0.12) / 0.06)
    a = a * fade
    a = cv2.resize(a, (1000, int(1000 * h / w)), interpolation=cv2.INTER_AREA)
    rgb = np.broadcast_to(hexrgb("#3d3843"), a.shape + (3,))
    return rgb, np.clip(a, 0, 1)


def venue():
    print("venue ...")
    rgb, a = venue_sketch()
    save_rgba("venue-sketch.webp", rgb, a, 90)

def photo():
    print("photo placeholder ...")
    PW, PHh = 600, 850
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
def _onoise(h, w, scale, octaves=4, seed=0):
    r = np.random.default_rng(seed); out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        s = max(2, int(scale / (2 ** o)))
        g = r.random((h // s + 3, w // s + 3)).astype(np.float32)
        out += amp * cv2.resize(g, (w, h), interpolation=cv2.INTER_CUBIC); tot += amp; amp *= 0.5
    return out / tot

WRINKLE = 0.0

def organza_rgba():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    def aniso(scale, ang, stretch, seed, octaves=2):
        S = int(max(W, H) * 1.5)
        n = _onoise(int(S / stretch) + 4, S, scale, octaves, seed)
        n = cv2.resize(n, (S, S), interpolation=cv2.INTER_CUBIC)
        M = cv2.getRotationMatrix2D((S / 2, S / 2), ang - 90, 1.0)
        n = cv2.warpAffine(n, M, (S, S), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        y0, x0 = (S - H) // 2, (S - W) // 2
        return n[y0:y0 + H, x0:x0 + W]
    # the sheet is drawn taut over the card but puckers everywhere: soft dimples a few cm wide, a little longer along the
    # drape (down-right), and two broad swells of the whole sheet
    h = 1.00 * aniso(230, 118, 2.0, 1, 2)
    h += 0.40 * aniso(120, 62, 1.6, 2, 2)
    h += 0.9 * _onoise(H, W, 620, 2, 5)
    h = cv2.GaussianBlur(h, (0, 0), 7)
    # wrinkles where the sheet is gathered and tucked round the card: folds fanning out of each corner, and
    # long wavy creases along the very top and bottom (the sheet is 1.28x the card, so the card's corners sit ~11-14% in)
    wr = np.zeros((H, W), np.float32)
    wob = _onoise(H, W, 260, 2, 61) - 0.5
    for k, (cx, cy) in enumerate(((0.06, 0.09), (0.94, 0.09), (0.06, 0.91), (0.94, 0.91))):
        px, py = cx * W, cy * H
        r = np.hypot(xx - px, (yy - py) * 0.62)
        th = np.arctan2(yy - py, xx - px)
        fan = np.sin(th * 34 + 11 * wob + k * 1.7) + 0.6 * np.sin(th * 71 - 8 * wob + k) + 0.5 * np.sin(th * 17 + 5 * wob)
        wr += 2.0 * fan * np.exp(-(r / (0.36 * W)) ** 2) * np.clip(r / (0.05 * W), 0, 1)
    for k, cy in enumerate((0.115, 0.885)):
        band = np.exp(-(((yy / H) - cy) / 0.075) ** 2)
        wave = np.sin((yy + 0.22 * (xx - W / 2) * (1 if k == 0 else -1)) / 15.0 + 10 * wob) + 0.6 * np.sin((yy - 0.1 * xx) / 7.5 + 7 * wob)
        wr += 0.8 * wave * band
    wr = cv2.GaussianBlur(wr, (0, 0), 2.2)
    h = h + WRINKLE * wr
    gy, gx = np.gradient(h * 380)
    # straight folds where the sheet is wrapped round the card: a thin bright crease, the doubled layer slightly denser on one side
    layer = np.zeros((H, W), np.float32); crease = np.zeros((H, W), np.float32)
    for (x0, y0, ang, side, la) in ((0, 330, -40, -1, .5), (0, 1180, 27, 1, .55), (900, 1500, 152, -1, .45), (560, 0, 60, -1, .3)):
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d = (xx - x0) * (-dy) + (yy - y0) * dx
        d += 10 * (_onoise(H, W, 340, 2, int(abs(ang)) + 20) - 0.5)
        layer += la * np.clip(side * d / 3.0, 0, 1)
        crease += (np.exp(-(d / 2.6) ** 2) + 0.3 * np.exp(-np.clip(side * d, 0, None) / 22) * (side * d > 0)) * (0.55 + 0.45 * _onoise(H, W, 90, 2, int(abs(ang)) + 40))
    # ---- the sheet's own borders, folded over at the edges (nothing of this lies over the middle of the card) ----
    def _to_sheet(px, py):                       # reference-frame px -> sheet px (frame is at ~0.9 zoom; sheet is 1.28x the card)
        uf = 0.5 + (px / 780 - 0.5) * 0.97; vf = 0.47 + (py / 1580 - 0.47) * 0.97
        return ((0.109 + 0.782 * uf) * W, (0.134 + 0.732 * vf) * H)
    FOLDS = [   # (polygon in reference px 780x1580, how dense the doubled cloth is). The top corners fold over as "/" and "\\"
        ([(-150, -300), (380, -300), (335, -20), (190, 150), (60, 300), (-20, 410), (-150, 470)], 0.9),        # top-left corner, edge runs like "/"
        ([(400, -300), (950, -300), (950, 470), (800, 410), (720, 300), (590, 150), (445, -20)], 0.9),          # top-right corner, edge runs like "\\"
        ([(-150, 1250), (0, 1268), (170, 1380), (300, 1490), (370, 1560), (430, 1800), (-150, 1800)], 0.7),   # bottom-left layer
        ([(470, 1470), (720, 1368), (950, 1310), (950, 1800), (400, 1800), (410, 1560)], 0.65),               # bottom-right layer
    ]
    fold_layer = np.zeros((H, W), np.float32); fold_edge = np.zeros((H, W), np.float32); fold_shadow = np.zeros((H, W), np.float32)
    for k, (poly, dens) in enumerate(FOLDS):
        pts = np.array([_to_sheet(x, y) for x, y in poly], np.float32)
        m = np.zeros((H, W), np.uint8); cv2.fillPoly(m, [np.round(pts).astype(np.int32)], 1)
        wobble = 14 * (_onoise(H, W, 300, 2, 70 + k) - 0.5)                       # the cut edge is soft and slightly wavy
        d_in = cv2.distanceTransform(m, cv2.DIST_L2, 5) + wobble * m
        d_out = cv2.distanceTransform(1 - m, cv2.DIST_L2, 5)
        inside = smooth01(d_in / 3.0) * m
        fold_layer = np.maximum(fold_layer, dens * inside * (0.30 + (1 - 0.30) * np.exp(-d_in / 80.0)))   # thin: the doubled cloth shows mostly near its edge
        fold_edge = np.maximum(fold_edge, np.exp(-((d_in - 3.0) / 3.2) ** 2) * m)                      # the rolled hem catches the light
        fold_edge = np.maximum(fold_edge, 0.25 * np.exp(-((d_in - 34) / 7.0) ** 2) * m * (0.5 + 0.5 * _onoise(H, W, 160, 2, 80 + k)))  # one soft crease just inside
        fold_shadow = np.maximum(fold_shadow, np.exp(-d_out / 12.0) * (1 - m))                         # and it shades the sheet beneath
    nrm = np.dstack([-gx, -gy, np.ones_like(h)]); nrm /= np.linalg.norm(nrm, axis=2, keepdims=True)
    l = np.array([-0.34, -0.60, 0.72]); l /= np.linalg.norm(l); hv = l + [0, 0, 1]; hv /= np.linalg.norm(hv)
    nh = np.clip((nrm * hv).sum(2), 0, 1); diff = np.clip((nrm * l).sum(2), 0, 1)
    # shine: a soft satin glow on every slope turned to the light + a small bright glint at its crest
    lo, mid, hi = np.percentile(nh, [40, 93, 99.7])
    glow = np.clip((nh - lo) / (mid - lo), 0, 1) ** 1.6
    glint = np.clip((nh - mid) / (hi - mid), 0, 1) ** 1.5
    weave = 0.5 + 0.5 * np.sin((xx * 0.86 + yy * 0.5) * 2 * math.pi / 3.1) * np.sin((xx * -0.5 + yy * 0.86) * 2 * math.pi / 3.1)   # fine organza weave
    hl = np.clip(0.40 * glow + 0.52 * glint + 0.18 * fold_layer + 0.25 * fold_edge, 0, 1) * (0.90 + 0.10 * weave)
    tint = _onoise(H, W, 200, 2, 8)[..., None]
    c_hl = np.array([250, 240, 248], np.float32) * (1 - tint) + np.array([236, 236, 255], np.float32) * tint
    c_veil = np.array([150, 122, 140], np.float32)                 # the film itself: a thin rosy-mauve veil
    shade = np.clip(1.0 - diff * 1.2, 0, 1)
    a_veil = np.clip(0.12 + 0.42 * shade + 0.21 * fold_layer + 0.15 * fold_shadow, 0, 0.72)
    a_hl = np.clip(0.86 * hl, 0, 0.86)
    a = a_veil + a_hl * (1 - a_veil)
    rgb = (c_veil * (a_veil * (1 - a_hl))[..., None] + c_hl * a_hl[..., None]) / np.maximum(a[..., None], 1e-4)
    return np.clip(rgb, 0, 255), np.clip(a, 0, 0.94)

def organza():
    """sheer organza sheet lying over the card (RGBA): a thin rosy veil with the soft satin shine of a puckered, taut sheet
    (broad dimples, a small glint on each crest) and a few straight folds where it is wrapped round the card"""
    print("organza ...")
    rgb, a = organza_rgba()
    save_rgba("organza.webp", rgb, a, 80)
    _fold_strip()

def _fold_strip():
    """the gathered, rolled edge of the fabric along one side of the opening diamond (RGBA strip, laid along each edge by app.js):
    x runs from the pinch point to the diamond's tip, y from just inside the opening (a soft shadow on the card) across the
    rolled edge (y = 16 %) into the bunched fabric with its taut folds running along the edge"""
    FW, FH = 640, 200
    x = np.linspace(0, 1, FW, dtype=np.float32)[None, :] * np.ones((FH, 1), np.float32)
    y = np.linspace(0, 1, FH, dtype=np.float32)[:, None] * np.ones((1, FW), np.float32)
    e = 0.16
    th = 1 - 0.55 * x                                             # the bunch thins toward the tip
    v = (y - e) / ((1 - e) * th)
    out_ = (v >= 0).astype(np.float32)
    wob = 0.5 * noise(FH, FW, 90, 2, 31) - 0.25
    sh = np.exp(-np.clip(e - y, 0, None) / 0.05) * (1 - out_) * 0.36
    bunch = np.clip(1 - v, 0, 1) ** 1.2 * out_
    roll = np.exp(-((v - 0.08) / 0.10) ** 2) * out_                # the soft bright rolled edge
    trough = np.exp(-((v - 0.32) / 0.10) ** 2) * out_               # the shadowed valley behind it
    st = np.exp(-((v - 0.50 - 0.25 * wob) / 0.05) ** 2) + 0.6 * np.exp(-((v - 0.76 + 0.2 * wob) / 0.04) ** 2)   # two fainter taut folds
    hl = np.clip(0.80 * roll + 0.40 * bunch * st, 0, 1)
    a_sh = sh
    a_veil = bunch * (0.40 + 0.30 * trough)
    a_hl = 0.68 * hl
    c_v = np.array([186, 158, 174], np.float32)[None, None, :] * (1 - 0.42 * trough)[..., None]   # gathered layers: denser, rosier
    a = a_veil + a_hl * (1 - a_veil)
    rgb = (c_v * (a_veil * (1 - a_hl))[..., None] + np.array([244, 236, 248], np.float32) * a_hl[..., None]) / np.maximum(a[..., None], 1e-4)
    A = a + a_sh * (1 - a)
    rgb = (rgb * a[..., None] + np.array([58, 38, 54], np.float32) * (a_sh * (1 - a))[..., None]) / np.maximum(A[..., None], 1e-4)
    fade = smooth01(x / 0.06) * smooth01((1 - x) / 0.10)
    save_rgba("fold.webp", np.clip(rgb, 0, 255), A * fade, 88)

def bow_frames(n=34):
    """3D organza bow on its band + the untie animation as numbered frames (same canvas, knot at ribbon3d.CX/CY),
    plus the two gathered band halves that stay once the knot has let go (ribbon.webp = the last frame's band rows)"""
    sys.path.insert(0, str(HERE))
    import ribbon3d as R
    fdir = OUT / "bow"; fdir.mkdir(exist_ok=True)
    for f in fdir.glob("bow-*.webp"):
        f.unlink()
    for i in range(n):
        u = i / (n - 1)
        rgb, a = R.render(u)
        if i == 0:                                              # the tied bow rests on screen: full size
            save_rgba("bow/bow-00.webp", rgb, a, 88)
        else:                                                   # frames in motion: 80 % size keeps the download small
            sz = (R.BW * 4 // 5, R.BH * 4 // 5)
            save_rgba(f"bow/bow-{i:02d}.webp", cv2.resize(rgb, sz, interpolation=cv2.INTER_AREA), cv2.resize(a, sz, interpolation=cv2.INTER_AREA), 68)
    print("band ...")
    y0, y1 = R.CY - R.BAND_HALF, R.CY + R.BAND_HALF
    save_rgba("ribbon.webp", rgb[y0:y1], a[y0:y1], 88)

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

# ---------------------------------------------------------------- embossed card v4 (sculpted relief traced from the reference)
class Relief:
    def __init__(self, w, h, s=2):
        self.s = s; self.W, self.H = w * s, h * s
        self.h = np.zeros((self.H, self.W), np.float32)

    def patch(self, cx, cy, rad):
        s = self.s; cx, cy, rad = cx * s, cy * s, rad * s
        x0, x1 = int(max(0, cx - rad)), int(min(self.W, cx + rad + 1))
        y0, y1 = int(max(0, cy - rad)), int(min(self.H, cy + rad + 1))
        if x0 >= x1 or y0 >= y1:
            return None
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        return (slice(y0, y1), slice(x0, x1)), (xx - cx) / s, (yy - cy) / s

    def put(self, sl, hgt, mask):
        """layer an element on top: it covers what is below (soft edge), sitting on the local surface"""
        reg = self.h[sl]
        reg[:] = reg * (1 - mask) + np.maximum(reg, hgt) * mask


def _tube(d, r):
    """round profile of a cord of radius r from the distance to its centre line"""
    return np.sqrt(np.clip(1 - (d / r) ** 2, 0, 1))


def _curve(pts, n=10):
    """smooth (Catmull-Rom) polyline through the given points"""
    P = np.asarray(pts, np.float32)
    if len(P) < 3:
        return np.array([P[0] + (P[-1] - P[0]) * t for t in np.linspace(0, 1, n + 1)], np.float32)
    Q = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    for i in range(len(P) - 1):
        p0, p1, p2, p3 = Q[i:i + 4]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P[-1])
    return np.array(out, np.float32)


def _along(P, t):
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    d = t * seg[-1]; k = int(np.clip(np.searchsorted(seg, d) - 1, 0, len(P) - 2))
    f = (d - seg[k]) / max(seg[k + 1] - seg[k], 1e-3)
    x, y = P[k] + (P[k + 1] - P[k]) * f
    return float(x), float(y), math.degrees(math.atan2(P[k + 1, 1] - P[k, 1], P[k + 1, 0] - P[k, 0]))


# petal kinds: outline pointedness, scalloped edge, beaded rim, radial flutes, rolled rim, puffiness
_PK = {"frill": dict(point=5.0, frill=0.075, nfr=6, bead=0.22, fl=4, fla=0.024, rim=0.085, puff=0.0),
       "cup": dict(point=4.5, frill=0.03, nfr=3, bead=0.0, fl=2, fla=0.02, rim=0.09, puff=0.0),
       "puff": dict(point=3.2, frill=0.04, nfr=2, bead=0.0, fl=1, fla=0.045, rim=0.035, puff=0.30),
       "flute": dict(point=2.4, frill=0.04, nfr=2, bead=0.0, fl=2, fla=0.085, rim=0.04, puff=0.13)}


def _petal(out, X, Y, R, th, dth, ri, ro, base, amp, kind, ph0=0.0):
    """one cupped petal in polar form about (0,0) of X,Y: centre angle th, half-width dth, from radius ri out to ro.
    painted into `out` (later petals lie on top)"""
    k = _PK[kind]
    r = np.hypot(X, Y); phi = np.arctan2(Y, X)
    d = (phi - th + math.pi) % (2 * math.pi) - math.pi
    u = d / dth; au = np.abs(u)
    prof = np.power(np.clip(1 - au ** k["point"], 0, 1), 0.5)
    e = ri + (ro - ri) * prof
    if k["nfr"]:
        e = e * (1 - k["frill"] * (1 - np.power(np.abs(np.cos(u * k["nfr"] * math.pi / 2 + ph0)), 0.6)) * prof)   # ruffled edge: round lobes, small notches
    ds = (1 - au) * np.maximum(r, 1) * dth
    dd = np.minimum(e - r, ds)                                         # ~distance to the petal's edge
    m = (au < 1) & (dd > 0) & (r > ri * 0.8)
    if not m.any():
        return
    t = np.clip((r - ri) / np.maximum(e - ri, 1), 0, 1)
    edge = smooth01(dd / (0.03 * R + 0.5))
    h = amp * t ** 1.3                                                 # cupped: rises to the rim
    if k["rim"]:
        rim = k["rim"] * np.exp(-((dd - 0.036 * R) / (0.021 * R)) ** 2)
        if k["bead"]:
            rim = rim * (1 + k["bead"] * np.cos(d * r * (2 * math.pi / (0.075 * R)) + ph0))
        h = h + rim
    if k["fl"]:
        fph = 0.0 if kind in ("flute", "puff") else ph0
        h = h - k["fla"] * (0.5 + 0.5 * np.cos(u * k["fl"] * 2 * math.pi + fph)) ** 5 * np.sqrt(t)
    if k["puff"]:
        h = h + k["puff"] * np.power(np.clip(1 - au ** 2, 0, 1), 0.5) * np.power(np.clip(np.sin(np.pi * np.clip(0.12 + 0.82 * t, 0, 1)), 0, 1), 0.6)
    hp = base + h * edge
    out[m] = hp[m]


def rose_head(R_, cx, cy, R, rot=0.0, seed=0, style="peony", guards=(), lift=1.0):
    """a full garden rose seen from the front, sculpted petal by petal (outer first, inner on top).
    style 'peony': frilled petal rings round a heart of tiny bead-like petals (top corners of the reference)
    style 'rose' : wrapped, cupped petals spiralling into a tight swirl (bottom corners)
    guards: the big outer petals [(angle deg, half-width deg, r_in, r_out, kind)] in units of R"""
    p = R_.patch(cx, cy, R * 1.5)
    if p is None:
        return
    sl, dx, dy = p
    rng = np.random.default_rng(seed)
    out = np.full(dx.shape, -1.0, np.float32)
    r = np.hypot(dx, dy)
    c = (math.cos(math.radians(rot)), math.sin(math.radians(rot)))

    def ring(n, ro, ri, base, amp, kind, jit=0.14, ov=1.3, ecc=0.0, rj=0.06):
        ph = rng.random() * 6.283
        for j in list(range(0, n, 2)) + list(range(1, n, 2)):
            th = ph + j * 2 * math.pi / n + rng.normal(0, jit * 2 * math.pi / n)
            _petal(out, dx - ecc * c[0] * R, dy - ecc * c[1] * R, R, th, math.pi / n * ov * (1 + rng.normal(0, 0.10)), ri * R,
                   ro * R * (1 + rng.normal(0, rj)), base + 0.035 * (j % 2), amp, kind, ph0=rng.random() * 6.283)

    for (ang, hwd, ri, ro, kind) in guards:
        _petal(out, dx, dy, R, math.radians(ang), math.radians(hwd), ri * R, ro * R, 0.05, 0.15, kind, ph0=rng.random() * 6.283)
    if style == "peony":
        ring(5, 0.90, 0.50, 0.14, 0.15, "frill", ov=1.28, rj=0.07)
        ring(5, 0.77, 0.46, 0.25, 0.14, "frill", ov=1.3, rj=0.06)
        ring(6, 0.64, 0.40, 0.35, 0.13, "frill", ov=1.3, rj=0.05)
        ring(6, 0.52, 0.34, 0.44, 0.12, "frill", ov=1.3, rj=0.05)
        ring(7, 0.42, 0.26, 0.52, 0.10, "cup", ov=1.25, rj=0.05)
        out[r < 0.33 * R] = 0.57                                       # heart: rings of tiny bead-like petals
        for kk, (rr, n) in enumerate([(0.30, 21), (0.225, 15), (0.15, 10), (0.075, 6), (0.0, 1)]):
            ph = rng.random() * 6.283
            for j in range(n):
                th = ph + j * 6.2832 / n + rng.normal(0, 0.05)
                rb = rr * R * (1 + rng.normal(0, 0.05)); br = 0.046 * R * (1 + rng.normal(0, 0.10))
                dd = np.hypot(dx - rb * math.cos(th), dy - rb * math.sin(th))
                hb = 0.57 + 0.02 * kk + 0.17 * _tube(dd, br)
                out[:] = np.where(dd < br, np.maximum(out, hb), out)
    else:
        if not guards:
            ring(6, 1.0, 0.56, 0.08, 0.17, "frill", ov=1.3)
        ring(5, 0.88, 0.50, 0.17, 0.16, "frill", ov=1.3, ecc=0.02)
        ring(5, 0.76, 0.44, 0.26, 0.15, "frill", ov=1.3, ecc=0.04)
        ring(5, 0.64, 0.36, 0.34, 0.14, "cup", ov=1.3, ecc=0.06)
        ring(4, 0.53, 0.28, 0.42, 0.13, "frill", ov=1.35, ecc=0.08)
        ring(4, 0.43, 0.20, 0.49, 0.12, "cup", ov=1.35, ecc=0.09)
        ring(3, 0.33, 0.13, 0.55, 0.11, "cup", ov=1.4, ecc=0.10, rj=0.03)
        ring(3, 0.24, 0.07, 0.61, 0.10, "cup", ov=1.4, ecc=0.108, rj=0.03)
        ring(2, 0.16, 0.02, 0.66, 0.09, "cup", ov=1.5, ecc=0.114, rj=0.02)
        ring(2, 0.09, 0.0, 0.70, 0.08, "cup", ov=1.5, ecc=0.118, rj=0.02)
    dome = 0.14 * np.sqrt(np.clip(1 - (r / (R * 1.45)) ** 2, 0, 1))
    m = cv2.GaussianBlur((out > -0.5).astype(np.float32), (0, 0), 0.55 * R_.s)
    R_.put(sl, (np.maximum(out, 0) + dome) * 0.9 * lift + 0.07, m)


def blossom(R_, x, y, r, rot=0.0, n=6, seed=0, lift=0.9):
    """small open flower of the side vines: n notched, cupped petals round a beaded eye"""
    p = R_.patch(x, y, r * 1.2 + 2)
    if p is None:
        return
    sl, dx, dy = p
    rng = np.random.default_rng(seed)
    out = np.full(dx.shape, -1.0, np.float32)
    RR = r * 1.7
    for j in list(range(0, n, 2)) + list(range(1, n, 2)):
        th = math.radians(rot) + j * 2 * math.pi / n + rng.normal(0, 0.06)
        _petal(out, dx, dy, RR, th, math.pi / n * 1.12, 0.2 * r, r * (1 + rng.normal(0, 0.05)), 0.10 + 0.03 * (j % 2), 0.12, "frill",
               ph0=math.pi)
    rr = np.hypot(dx, dy)
    out[rr < 0.3 * r] = 0.30
    for j in range(7):
        bx_, by_ = (0.19 * r * math.cos(j * 1.047 + 0.3), 0.19 * r * math.sin(j * 1.047 + 0.3)) if j < 6 else (0.0, 0.0)
        dd = np.hypot(dx - bx_, dy - by_)
        out[:] = np.where(dd < 0.11 * r, np.maximum(out, 0.30 + 0.16 * _tube(dd, 0.11 * r)), out)
    m = cv2.GaussianBlur((out > -0.5).astype(np.float32), (0, 0), 0.5 * R_.s)
    R_.put(sl, np.maximum(out, 0) * lift + 0.10, m)


def leaf(R_, bx, by, L, ang, Wd=None, nv=4, lift=1.0, bend=0.0):
    """engraved leaf from its base (bx,by) pointing at ang degrees: pointed, saw-toothed, with a carved midrib and
    nv plump vein segments a side (nv=0: a plain smooth leaflet)"""
    Wd = L * 0.54 if Wd is None else Wd
    a = math.radians(ang)
    cx, cy = bx + math.cos(a) * L / 2, by + math.sin(a) * L / 2
    p = R_.patch(cx, cy, L * 0.62 + 4)
    if p is None:
        return
    sl, dx, dy = p
    ux = dx * math.cos(a) + dy * math.sin(a); vy = -dx * math.sin(a) + dy * math.cos(a)
    u = ux / L + 0.5
    uc = np.clip(u, 0, 1)
    if bend:
        vy = vy - bend * L * uc * (1 - uc)
    hw = Wd / 2 * np.power(uc, 0.55) * np.power(1 - uc, 0.85) / 0.391
    if nv:
        ph = uc * nv * 1.12 + 0.2 - np.abs(vy) / (Wd / 2) * 0.62
        tooth = ph % 1.0
        hw = hw * (1 + 0.30 * (tooth - 0.62) * (uc > 0.08) * (uc < 0.93))
    vv = vy / np.maximum(hw, 0.5)
    m = smooth01((hw - np.abs(vy)) / 0.9) * (u > 0) * (u < 1)
    dome = 0.24 * np.power(np.clip(1 - vv ** 2, 0, 1), 0.5)
    hgt = 0.15 + dome - 0.11 * np.exp(-(vy / max(1.0, Wd * 0.035)) ** 2)        # carved midrib
    if nv:
        off = 1 - np.exp(-(vy / (Wd * 0.09 + 0.8)) ** 2)
        hgt = hgt + (0.17 * np.power(np.clip(np.sin(np.pi * tooth), 0, 1), 0.7) - 0.07) * off * np.clip(np.abs(vv) * 3, 0, 1)
    R_.put(sl, hgt * lift, m)


def stem(R_, pts, w0, w1=None, lift=0.6):
    """a stem along a polyline, tapering from w0 to w1 (radius, px)"""
    w1 = w0 if w1 is None else w1
    pts = np.asarray(pts, np.float32)
    s = R_.s
    xs, ys = pts[:, 0], pts[:, 1]
    x0, x1 = int(max(0, (xs.min() - w0 - 3) * s)), int(min(R_.W, (xs.max() + w0 + 3) * s))
    y0, y1 = int(max(0, (ys.min() - w0 - 3) * s)), int(min(R_.H, (ys.max() + w0 + 3) * s))
    if x0 >= x1 or y0 >= y1:
        return
    hgt = np.zeros((y1 - y0, x1 - x0), np.float32)
    n = len(pts)
    for i in range(n - 1):
        w = (w0 + (w1 - w0) * i / max(1, n - 2)) * s
        p0 = (int((pts[i, 0] * s - x0) * 4), int((pts[i, 1] * s - y0) * 4))
        p1 = (int((pts[i + 1, 0] * s - x0) * 4), int((pts[i + 1, 1] * s - y0) * 4))
        cv2.line(hgt, p0, p1, 1.0, max(1, int(round(w * 2))), cv2.LINE_AA, shift=2)
    dt = cv2.distanceTransform((hgt > 0.5).astype(np.uint8), cv2.DIST_L2, 5) / max(1.0, w0 * s)
    prof = np.sqrt(np.clip(dt * (2 - dt), 0, 1))
    m = cv2.GaussianBlur(hgt, (0, 0), 0.5)
    reg = R_.h[y0:y1, x0:x1]
    reg[:] = reg * (1 - m) + np.maximum(reg, 0.13 + prof * 0.32 * lift) * m


def berry(R_, x, y, r, lift=1.0):
    """little ring-shaped bud (a bead with a dimple), as on the reference's sprays"""
    p = R_.patch(x, y, r + 2)
    if p is None:
        return
    sl, dx, dy = p
    d = np.hypot(dx, dy)
    R_.put(sl, (0.16 + 0.44 * _tube(d - 0.50 * r, 0.52 * r)) * lift, smooth01((r - d) / 0.8))


def drop(R_, x, y, L, ang, lift=0.9):
    """tear-drop bud: plump, pointed, with a dimple"""
    leaf(R_, x, y, L, ang, Wd=L * 0.62, nv=0, lift=lift)
    a = math.radians(ang)
    p = R_.patch(x + math.cos(a) * L * 0.42, y + math.sin(a) * L * 0.42, L * 0.2 + 2)
    if p is not None:
        sl, dx, dy = p
        d = np.hypot(dx, dy)
        R_.h[sl] -= 0.16 * np.exp(-(d / (L * 0.09)) ** 2)


def spray(R_, pts, leaves=(), berries=(), w0=2.0, w1=1.2, L=28, lift=0.9):
    """a curling stem through pts with small leaflets [(t along stem, side +1/-1, length[, angle off the stem])]
    and ring buds [(x, y[, r])] on little stalks"""
    P = _curve(pts)
    stem(R_, P, w0, w1, lift=0.75)
    for b in berries:
        bx, by = b[0], b[1]; br = b[2] if len(b) > 2 else 6.6
        k = int(np.argmin(np.hypot(P[:, 0] - bx, P[:, 1] - by)))
        k = max(0, k - 3)
        mx, my = (P[k, 0] + bx) / 2, (P[k, 1] + by) / 2
        stem(R_, _curve([(P[k, 0], P[k, 1]), (mx + (by - P[k, 1]) * 0.12, my - (bx - P[k, 0]) * 0.12), (bx, by)], 6), 1.2, 0.9, lift=0.6)
        berry(R_, bx, by, br)
    for lf in leaves:
        t, side, ll = lf[0], lf[1], (lf[2] if len(lf) > 2 else L)
        da = lf[3] if len(lf) > 3 else 42
        x, y, tg = _along(P, t)
        leaf(R_, x, y, ll * 1.15, tg + side * da, Wd=ll * 0.58, nv=2 if ll < 40 else 3, lift=lift)
    return P


# ---------------------------------------------------------------- the cusped Mughal-arch frame
ARCH = dict(cx=450, ytop=238, ybot=1666, hw=338)
ARCH_SEGS = [((0, 0), (-4, 22), (-18, 44), (-46, 54)), ((-46, 54), (-80, 66), (-125, 60), (-152, 79)),      # ogee peak
             ((-152, 79), (-166, 88), (-172, 100), (-172, 115)),                                            # down to cusp 1
             ((-172, 115), (-200, 114), (-222, 138), (-224, 176)),                                          # lobe -> cusp 2
             ((-224, 176), (-262, 176), (-290, 215), (-294, 303)),                                          # lobe -> cusp 3
             ((-294, 303), (-318, 306), (-338, 335), (-338, 378))]                                          # shoulder -> straight side


def arch_path(cx=None, ytop=None, ybot=None):
    """closed outline (centre line of the outer moulding), traced from the reference: ogee peak, three cusps a side,
    straight sides; mirrored at the bottom. ARCH_SEGS are cubic beziers in px offsets from the peak (left half).
    (app.js draws the panel sheen with the same numbers)"""
    cx = ARCH["cx"] if cx is None else cx; ytop = ARCH["ytop"] if ytop is None else ytop; ybot = ARCH["ybot"] if ybot is None else ybot
    half = []
    for (p0, c1, c2, p3) in ARCH_SEGS:
        pts = _bez(*[(cx + x, ytop + y) for x, y in (p0, c1, c2, p3)], 40)
        half += pts if not half else pts[1:]
    top = half[::-1] + [(2 * cx - x, y) for x, y in half][1:]         # left side -> peak -> right side
    bot = [(x, ytop + ybot - y) for x, y in reversed(top)]
    return np.array(top + bot, np.float32)


def card_relief(W=900, H=1950, s=2):
    R_ = Relief(W, H, s)
    S = s
    # ---------- frame (built from a signed distance field so every offset line follows the cusps) ----------
    outl = arch_path()
    pm = np.zeros((R_.H, R_.W), np.uint8)
    cv2.fillPoly(pm, [np.round(outl * S * 16).astype(np.int32)], 1, cv2.LINE_AA, shift=4)
    din = cv2.distanceTransform(pm, cv2.DIST_L2, 5) / S
    dout = cv2.distanceTransform(1 - pm, cv2.DIST_L2, 5) / S
    sd = din - dout                                                    # >0 inside
    fr = np.zeros_like(sd)
    fr = np.maximum(fr, 0.56 * _tube(sd - 0.0, 5.2))                   # outer rounded moulding
    fr = np.maximum(fr, 0.34 * _tube(sd - 9.6, 2.3))                   # second, finer line
    # bead row
    cm = (sd >= 17.5).astype(np.uint8)
    cs, _ = cv2.findContours(cm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=len)[:, 0, :].astype(np.float32) / S
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(np.vstack([c, c[:1]]), axis=0).T))]
    beads = np.zeros_like(sd)
    nb = int(seg[-1] / 10.6)
    yy, xx = np.mgrid[0:R_.H, 0:R_.W].astype(np.float32)
    for i in range(nb):
        d = i * seg[-1] / nb
        k = int(np.clip(np.searchsorted(seg, d) - 1, 0, len(c) - 1))
        bx, by = c[k]
        x0, x1 = int((bx - 6) * S), int((bx + 6) * S) + 1; y0, y1 = int((by - 6) * S), int((by + 6) * S) + 1
        dd = np.hypot(xx[y0:y1, x0:x1] / S - bx, yy[y0:y1, x0:x1] / S - by)
        beads[y0:y1, x0:x1] = np.maximum(beads[y0:y1, x0:x1], 0.44 * _tube(dd, 3.7))
    fr = np.maximum(fr, beads)
    R_.h += fr
    panel = smooth01((sd - 22) / 3)                                   # the smooth glossy centre

    # ---------- florals (every position traced from the rectified reference video) ----------
    F = Relief(W, H, s)
    lf = lambda x, y, ang, L, Wd=None, nv=4, **kw: leaf(F, x, y, L, ang, Wd=Wd, nv=nv, **kw)

    def cluster(hub, pts, r=6.6):
        for (bx, by) in pts:
            stem(F, _curve([hub, ((hub[0] + bx) / 2 + (by - hub[1]) * 0.1, (hub[1] + by) / 2 - (bx - hub[0]) * 0.1), (bx, by)], 6), 1.2, 0.9, lift=0.6)
            berry(F, bx, by, r)

    def vine(pts, leaves, flowers=(), buds=(), shoots=(), tip=40):
        """side vine growing upwards through pts (bottom -> top): leaves [(y, side, L)], blossoms [(x, y, r)], ring buds,
        and curling side shoots [(y, side, length)] carrying small leaflets and a bud"""
        P = _curve(pts, 14)
        stem(F, P, 2.2, 1.3, lift=0.75)

        def at(y):
            k = min(int(np.argmin(np.abs(P[:, 1] - y))), len(P) - 2)
            return P[k, 0], P[k, 1], math.degrees(math.atan2(P[k + 1, 1] - P[k, 1], P[k + 1, 0] - P[k, 0]))
        for (y, side, L) in shoots:
            x0, y0, tg = at(y)
            a0 = math.radians(tg + side * 38); a1 = math.radians(tg + side * (62 + 10 * math.sin(y)))
            p1 = (x0 + math.cos(a0) * L * 0.55, y0 + math.sin(a0) * L * 0.55)
            p2 = (p1[0] + math.cos(a1) * L * 0.5, p1[1] + math.sin(a1) * L * 0.5)
            spray(F, [(x0, y0), p1, p2], leaves=[(0.38, side, L * 0.42, 48), (0.62, -side, L * 0.40, 44), (0.86, side, L * 0.34, 40)], w0=1.5, w1=1.0)
            berry(F, p2[0] + math.cos(a1) * 5, p2[1] + math.sin(a1) * 5, 5.8)
        for (y, side, L) in leaves:
            x0, y0, tg = at(y)
            leaf(F, x0, y0, L * 1.25, tg + side * (46 + 6 * math.sin(y)), Wd=L * 0.56, nv=3 if L >= 40 else 2, lift=0.95)
        x, y, tg = _along(P, 1.0)
        leaf(F, x, y + 4, tip, tg, Wd=tip * 0.42, nv=2)
        for (bx, by) in buds:
            k = int(np.argmin(np.hypot(P[:, 0] - bx, P[:, 1] - by - 14)))
            stem(F, [(P[k, 0], P[k, 1]), (bx, by)], 1.2, 0.9, lift=0.6); berry(F, bx, by, 6.8)
        for i, (x, y, r_) in enumerate(flowers):
            for q in range(3):                                         # little leaves peeping out from behind the flower
                leaf(F, x, y, r_ * 1.5, 30 + q * 120 + x, Wd=r_ * 0.7, nv=2, lift=0.85)
            blossom(F, x, y, r_, rot=x + y, n=7, seed=int(x + y))

    # ---- top-left: peony cut by the card edge, crown of leaves, two bud sprays, leaves trailing down the side
    for (x, y, a_, L) in [(45, 104, -106, 62), (92, 110, -94, 52), (150, 104, -96, 52), (174, 96, -78, 58), (210, 100, -84, 58), (24, 142, -152, 46)]:
        lf(x, y, a_, L, nv=3)
    spray(F, [(188, 120), (225, 93), (266, 78), (310, 70), (352, 72)], leaves=[(0.38, 1, 34, 50), (0.56, 1, 32, 55), (0.22, -1, 30, 60), (0.48, -1, 24, 70)],
          berries=[(268, 42), (300, 49), (323, 52), (343, 52), (360, 70), (348, 96), (322, 93), (298, 84)])
    spray(F, [(230, 201), (262, 186), (300, 170), (338, 160)], leaves=[(0.25, -1, 28, 55), (0.5, -1, 26, 60), (0.38, 1, 24, 50)],
          berries=[(320, 141), (347, 158), (328, 183), (297, 193), (300, 148)])
    lf(222, 243, 27, 80, 38, nv=5); lf(232, 222, 6, 46, nv=3)
    stem(F, _curve([(62, 368), (54, 430), (41, 500), (38, 570), (42, 628)]), 2.2, 1.3, lift=0.75)
    for (x, y, a_, L, w_) in [(60, 398, 36, 70, 34), (51, 452, 38, 72, 34), (40, 532, 52, 70, 32), (52, 420, 142, 56, 26), (43, 490, 146, 56, 26),
                              (38, 560, 140, 50, 24), (40, 592, 75, 40, 18)]:
        lf(x, y, a_, L, w_)
    cluster((42, 622), [(15, 632), (38, 654), (58, 640)])
    for (x, y, a_) in [(160, 352, 62), (128, 372, 100), (210, 326, 45)]:
        drop(F, x, y, 17, a_)
    rose_head(F, 115, 215, 122, seed=11, style="peony",
              guards=[(-128, 24, 0.5, 1.12, "puff"), (-92, 21, 0.5, 1.12, "puff"), (-58, 21, 0.5, 1.12, "puff"), (-22, 22, 0.5, 0.98, "frill"),
                      (8, 20, 0.5, 1.0, "frill"), (22, 14, 0.5, 1.14, "flute"), (40, 14, 0.5, 1.26, "flute"), (58, 14, 0.5, 1.2, "flute"),
                      (150, 22, 0.55, 1.12, "puff"), (120, 19, 0.55, 1.22, "puff"), (92, 18, 0.55, 1.2, "puff"), (180, 24, 0.5, 1.10, "puff"),
                      (215, 24, 0.5, 1.10, "puff")])
    # ---- left side vine
    vine([(50, 1425), (42, 1300), (36, 1200), (38, 1100), (45, 1000), (42, 900), (50, 820), (48, 752)],
         leaves=[(1385, 1, 44), (1372, -1, 40), (1335, 1, 46), (1330, -1, 42), (1180, -1, 40), (1150, 1, 42), (1100, -1, 40), (1065, 1, 50),
                 (1060, -1, 42), (1035, 1, 44), (850, 1, 38), (835, -1, 34), (805, -1, 32), (772, -1, 30)],
         flowers=[(42, 945, 35), (45, 1240, 35)], buds=[(68, 746), (72, 791)], shoots=[(1395, 1, 52), (1300, -1, 46), (1140, 1, 50), (1085, -1, 44), (880, 1, 50), (810, -1, 40), (790, 1, 40)], tip=38)
    # ---- top-right: the largest peony with its fan of fluted petals, crown, sprays and the leaves hanging below
    for (x, y, a_, L) in [(718, 104, -98, 64), (746, 98, -80, 42), (796, 104, -92, 50), (840, 108, -100, 60), (862, 102, -72, 56), (884, 132, -50, 46)]:
        lf(x, y, a_, L, nv=3)
    spray(F, [(704, 106), (665, 88), (622, 74), (578, 68), (540, 74)], leaves=[(0.2, 1, 36, 60), (0.46, 1, 30, 62), (0.68, 1, 26, 65), (0.4, -1, 28, 50), (0.58, -1, 26, 55)],
          berries=[(527, 76), (545, 98), (580, 103), (548, 50), (568, 42), (513, 96)])
    spray(F, [(668, 201), (630, 181), (590, 163), (555, 156)], leaves=[(0.3, 1, 30, 55), (0.6, 1, 26, 60), (0.45, -1, 22, 50)],
          berries=[(550, 157), (565, 184), (595, 195), (543, 181)])
    lf(655, 243, 150, 64, 40, nv=4)
    stem(F, _curve([(836, 368), (857, 440), (867, 520), (870, 600), (868, 652)]), 2.2, 1.3, lift=0.75)
    for (x, y, a_, L, w_) in [(842, 405, 160, 80, 40), (850, 468, 150, 70, 36), (863, 555, 125, 64, 34), (850, 398, 30, 56, 26), (861, 468, 40, 50, 24),
                              (867, 538, 46, 46, 22), (870, 598, 62, 40, 18)]:
        lf(x, y, a_, L, w_)
    cluster((868, 640), [(845, 641), (877, 648), (860, 669)])
    cluster((856, 520), [(831, 512)], r=5)
    for (x, y, a_) in [(716, 356, 115), (748, 384, 105), (656, 300, 140), (664, 332, 120)]:
        drop(F, x, y, 17, a_)
    rose_head(F, 765, 215, 126, seed=22, style="peony",
              guards=[(-128, 22, 0.5, 1.12, "puff"), (-95, 20, 0.5, 1.12, "puff"), (-62, 20, 0.5, 1.12, "puff"), (-28, 22, 0.5, 1.10, "puff"),
                      (5, 22, 0.5, 1.10, "puff"), (36, 20, 0.5, 1.05, "frill"), (205, 22, 0.5, 0.94, "frill"), (170, 22, 0.5, 0.94, "frill"),
                      (142, 16, 0.5, 1.05, "frill"), (122, 15, 0.5, 1.14, "flute"), (101, 15, 0.5, 1.27, "flute"), (80, 16, 0.5, 1.32, "flute"),
                      (59, 15, 0.5, 1.18, "flute")])
    # ---- right side vine (taller and leafier than the left one)
    stem(F, _curve([(850, 1185), (836, 1110), (814, 1052), (802, 1004)]), 1.8, 1.2, lift=0.7)
    for (x, y, a_, L) in [(838, 1115, -150, 44), (822, 1070, -40, 34), (812, 1050, -140, 46), (802, 1008, -100, 44)]:
        lf(x, y, a_, L, L * 0.4, nv=3)
    vine([(860, 1445), (852, 1300), (848, 1150), (846, 1000), (850, 860), (848, 752)],
         leaves=[(1410, -1, 44), (1395, 1, 40), (1345, -1, 56), (1330, 1, 46), (1165, -1, 60), (1120, 1, 44), (1010, 1, 46), (955, -1, 62),
                 (890, 1, 44), (855, -1, 54), (800, -1, 44), (790, 1, 34)],
         flowers=[(836, 1250, 37)], buds=[(873, 760), (818, 764)], shoots=[(1420, -1, 50), (1310, 1, 44), (1200, -1, 56), (1075, 1, 46), (985, -1, 52), (915, 1, 44), (825, -1, 46), (800, 1, 40)], tip=42)
    # ---- bottom-left: wrapped rose, compound leaf above, fern spray, big leaves and a bud cluster below
    stem(F, _curve([(75, 1555), (80, 1500), (92, 1440), (100, 1408)]), 2.2, 1.3, lift=0.75)
    for (x, y, a_, L, w_) in [(92, 1452, -78, 52, 22), (80, 1500, -135, 64, 28), (82, 1498, -42, 62, 28), (76, 1536, -160, 60, 28),
                              (78, 1538, -14, 68, 32), (88, 1468, -122, 50, 22), (90, 1466, -50, 50, 22)]:
        lf(x, y, a_, L, w_)
    cluster((172, 1592), [(186, 1565), (213, 1590)], r=6)
    stem(F, _curve([(205, 1748), (222, 1702), (236, 1652)]), 1.8, 1.2, lift=0.7)
    lf(233, 1684, -86, 64, 26); lf(216, 1724, -112, 42, 18, nv=3)
    spray(F, [(210, 1744), (250, 1719), (292, 1714), (330, 1738), (354, 1770)],
          leaves=[(0.16, -1, 30), (0.22, 1, 28), (0.36, -1, 32), (0.42, 1, 30), (0.56, -1, 32), (0.62, 1, 30), (0.76, -1, 28), (0.82, 1, 28), (0.93, -1, 24),
                  (0.95, 1, 24), (1.0, 0, 26)])
    lf(186, 1772, 12, 98, 54, nv=5)
    stem(F, _curve([(150, 1768), (172, 1830), (200, 1878), (228, 1906)]), 2.2, 1.4, lift=0.75)
    for (x, y, a_, L, w_) in [(140, 1758, 104, 100, 44), (212, 1812, 94, 86, 24), (84, 1742, 120, 92, 42), (40, 1732, 150, 72, 36), (60, 1800, 96, 80, 36)]:
        lf(x, y, a_, L, w_)
    stem(F, [(303, 1904), (304, 1846)], 1.4, 1.0, lift=0.6); lf(305, 1850, -90, 28, 12, nv=2)
    cluster((304, 1870), [(289, 1862), (322, 1859), (285, 1886), (313, 1891), (328, 1880)])
    rose_head(F, 120, 1645, 106, rot=200, seed=33, style="rose")
    # ---- bottom-right: the second large rose, leaves rising above it, fern spray and leaves below
    stem(F, _curve([(808, 1574), (790, 1520), (768, 1462), (752, 1424)]), 2.2, 1.3, lift=0.75)
    for (x, y, a_, L, w_) in [(772, 1474, -112, 62, 26), (790, 1520, -155, 82, 34), (792, 1518, -60, 56, 26), (800, 1552, -170, 76, 32),
                              (780, 1492, -135, 56, 24), (782, 1490, -75, 46, 20)]:
        lf(x, y, a_, L, w_)
    stem(F, _curve([(842, 1572), (862, 1500), (878, 1424)]), 2.0, 1.2, lift=0.75)
    for (x, y, a_, L) in [(848, 1548, -125, 48), (856, 1516, -30, 44), (862, 1492, -128, 46), (868, 1464, -32, 40), (874, 1440, -120, 40), (878, 1426, -78, 40)]:
        lf(x, y, a_, L, L * 0.42, nv=3)
    stem(F, [(714, 1614), (690, 1598)], 1.3, 1.0, lift=0.6); stem(F, [(714, 1614), (703, 1574)], 1.3, 1.0, lift=0.6)
    drop(F, 694, 1601, 18, 205); drop(F, 704, 1580, 18, 255)
    lf(657, 1706, -97, 76, 26)
    spray(F, [(700, 1794), (662, 1743), (605, 1720), (560, 1716), (522, 1741)],
          leaves=[(0.28, 1, 30), (0.34, -1, 28), (0.46, 1, 32), (0.52, -1, 30), (0.64, 1, 30), (0.70, -1, 30), (0.82, 1, 28), (0.86, -1, 26), (0.95, 1, 24),
                  (1.0, 0, 26)],
          berries=[(527, 1791), (549, 1796), (507, 1766)])
    lf(702, 1790, 176, 96, 54, nv=5)
    for (x, y, a_, L, w_) in [(700, 1782, 112, 108, 44), (748, 1776, 93, 104, 40), (800, 1770, 62, 96, 44), (848, 1748, 32, 76, 36), (838, 1832, 80, 66, 30)]:
        lf(x, y, a_, L, w_)
    cluster((806, 1848), [(800, 1867), (818, 1861)])
    cluster((584, 1864), [(575, 1836), (555, 1851), (568, 1874), (593, 1883), (566, 1898), (615, 1860)])
    rose_head(F, 765, 1655, 118, rot=170, seed=44, style="rose")
    floral = F.h * (1 - smooth01((sd + 20) / 8))                      # keep a clear margin round the frame
    R_.h = np.maximum(R_.h, floral)
    return R_, sd, panel


CARD_K, CARD_CY = 0.905, 0.467

def render_card(W=900, H=1950, s=2):
    R_, sd, panel = card_relief(W, H, s)
    hm = R_.h
    # the whole design sits at CARD_K of the canvas, about a point a little above the middle, with plain paper
    # around it: measured on the reference video, where the arch spans ~68% of the screen width (12% .. 82% down)
    _M = np.float32([[CARD_K, 0, (1 - CARD_K) * hm.shape[1] / 2], [0, CARD_K, (1 - CARD_K) * hm.shape[0] * CARD_CY]])
    _wp = lambda a_, mode=cv2.BORDER_CONSTANT: cv2.warpAffine(np.ascontiguousarray(a_, np.float32), _M, (hm.shape[1], hm.shape[0]), flags=cv2.INTER_AREA, borderMode=mode, borderValue=0)
    hm = _wp(hm, cv2.BORDER_REFLECT_101); panel = _wp(panel); sd = _wp(sd, cv2.BORDER_REPLICATE)   # mirrored relief completes the roses cut by the old edge
    HH, WW = hm.shape
    yy, xx = np.mgrid[0:HH, 0:WW].astype(np.float32)
    # fine brushed / linen grain on the paper (diagonal, like the reference)
    g = noise(HH, WW, 2, 1, 91)
    g = cv2.GaussianBlur(g, (0, 0), sigmaX=1.0)
    k = np.zeros((15, 15), np.float32); np.fill_diagonal(k, 1); k /= k.sum()
    brushed = cv2.filter2D(g, -1, k) - 0.5
    grain = brushed * 0.010 * (1 - 0.6 * panel) + (noise(HH, WW, 3, 2, 92) - 0.5) * 0.003
    hgt = cv2.GaussianBlur(hm, (0, 0), 0.75 * s) + grain
    # paper: matte satin; panel: smoother, glossier (the "mirror")
    sheen = 0.97 + 0.05 * np.sin((xx * 0.5 + yy * 0.3) / (420 * s)) + 0.03 * (noise(HH, WW, 500, 2, 22) - 0.5)
    col = hexrgb("#aea6b2") * sheen[..., None]
    rgb_p = shade(hgt, col, light=(-0.5, -0.7, 0.6), depth=36 * s / 2, amb=0.66, kd=0.42, ks=0.24, shin=12,
                  spec_rgb=(255, 248, 255))
    # ambient occlusion: crevices between petals/leaves go darker -> crisp engraved read
    blur = cv2.GaussianBlur(hm, (0, 0), 3.5 * s)
    occl = np.clip((blur - hm) * 3.0, 0, 1)
    rgb_p *= (1 - 0.40 * occl)[..., None]
    lift_l = np.clip(hm, 0, 1.2)
    rgb_p = rgb_p * (1 + 0.17 * lift_l)[..., None]
    # glossy panel: broad soft reflection, faint pearl tint
    u = (xx / WW); v = (yy / HH)
    refl = 0.5 + 0.5 * np.cos(((u - 0.35) * 1.6 + (v - 0.33) * 2.4) * math.pi)
    refl = np.clip(refl, 0, 1) ** 2
    tint = np.dstack([1 + 0.02 * np.sin(v * 9 + 1), 1 - 0.01 * np.sin(v * 7), 1 + 0.025 * np.sin(v * 8 + 2.5)])
    pcol = hexrgb("#c1b6bf") * tint * (0.98 + 0.07 * refl)[..., None]
    rgb_g = shade(hgt, pcol, light=(-0.5, -0.7, 0.6), depth=36 * s / 2, amb=0.70, kd=0.36, ks=0.30, shin=40,
                  spec_rgb=(255, 250, 255))
    rgb = rgb_p * (1 - panel[..., None]) + rgb_g * panel[..., None]
    light = 1.035 - 0.06 * v - 0.03 * u + 0.025 * np.exp(-(((u - 0.45) / 0.35) ** 2 + ((v - 0.35) / 0.3) ** 2))   # soft room light
    rgb = rgb * light[..., None]
    rgb = cv2.resize(rgb, (W, H), interpolation=cv2.INTER_AREA)
    pmask = cv2.resize(panel, (W, H), interpolation=cv2.INTER_AREA)
    return np.clip(rgb, 0, 255), pmask


def card():
    """the embossed card, traced element by element from the reference video: garden roses in the four corners (frilled
    peonies above, wrapped roses below) with their leaves, bud sprays and fern sprays, flowering vines down both sides,
    the three-cusped arch frame with its fine line and beaded row, and the smooth glossy centre panel"""
    print("card (v4) ...")
    rgb, pm = render_card(W, H, 2)
    save_rgb("card.jpg", rgb, 92)          # the glossy sheen over the centre panel is drawn by app.js (same arch)


if __name__ == "__main__":
    which = sys.argv[1:] or ["envelope", "seal", "satin", "bow", "card", "pearl", "venue", "photo"]
    for w in which:
        globals()[w]()
