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
    brgb = shade((noise(fh, W, 3, 2, 8) - 0.5) * 0.05, hexrgb("#8e7b88"), depth=10, amb=0.74, kd=0.28, ks=0.03)
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
    f = (P["w_iso"] * iso + P["w_cloud"] * cloud + (P["w_feather"] * feather + P["w_fine"] * fine) * (0.75 - 0.25 * lively)
         + P["w_ring"] * rings * (0.2 + 0.7 * calm))
    z = (f - f.mean()) / f.std()
    flame = smooth01((0.8 * iso + 0.45 * cloud + 0.5 * mott + 0.16 * feather + 0.05) / 1.25)   # silver flames, feathered along the barbs
    t = P["t0"] + P["t1"] * z + P["t2"] * z * np.abs(z) + P["flame"] * lively * flame
    glint = smooth01((feather + 0.7 * fine + 0.5 * mott - 1.5) / 0.9)       # small wet highlights
    t = t + lively * (0.08 * mott + 0.09 * feather + 0.05 * fine)             # the flames are mottled and barbed, never flat
    t = np.clip(t * edge + 0.5 * glint * (0.15 + lively), -0.25, 1.4)
    col = lo + (hi - lo) * t[..., None]
    ice = (smooth01((col.mean(2) - 165) / 70) * 0.8)[..., None]              # the brightest nacre turns a cool blue-white
    col = col * (1 - ice) + np.minimum(col, 255) * np.array([0.91, 0.945, 1.035], np.float32) * ice
    # growth rings where the shell is calm: broad soft bands, a pale lip on each scale, a little fog
    lip = np.exp(-((bf - 0.06) / 0.05) ** 2) * (0.5 + 0.5 * np.sin(a0 * 3 + bi * 2.4))
    col += ((rings * 3.0 + lip * 7.0 + iso * 3.0 + cloud * 2.0 + feather * 2.0) * (0.2 + calm))[..., None]
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
    hue = (noise(S, S, S // 5, 3, 75) - 0.5) * 1.6
    col *= np.dstack([1 + 0.06 * hue, 1 - 0.035 * hue, 1 - 0.05 * hue])
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
def organza():
    """sheer, glossy organza lying over the card (RGBA): soft irregular wrinkles stretched along the drape,
    satin highlights, slightly darker troughs, see-through on the flats -- like the fabric in the reference video"""
    print("organza ...")
    def streak(n, ang, length):                               # directional blur -> elongated wrinkles
        k = np.zeros((length, length), np.float32)
        c = length // 2; dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        cv2.line(k, (int(c - dx * c), int(c - dy * c)), (int(c + dx * c), int(c + dy * c)), 1.0, 1, cv2.LINE_AA)
        return cv2.filter2D(n, -1, k / k.sum(), borderType=cv2.BORDER_REFLECT)
    h = np.zeros((H, W), np.float32)
    for k, (sc, amp, ang, ln) in enumerate(((260, 1.0, 62, 221), (140, 0.55, 56, 151), (70, 0.26, 64, 101), (200, 0.40, -35, 121))):
        n = noise(H, W, sc, 2, 70 + k)
        n = streak(n, ang, ln)
        n = (n - n.min()) / (n.max() - n.min() + 1e-6)
        h += amp * (1 - np.abs(2 * n - 1)) ** 2.2              # ridged: soft troughs, crisp crests
    h += 0.8 * noise(H, W, 420, 2, 79)
    h = cv2.GaussianBlur(h, (0, 0), 2.0)
    gy, gx = np.gradient(h * 30)
    nrm = np.dstack([-gx, -gy, np.ones_like(h)]); nrm /= np.linalg.norm(nrm, axis=2, keepdims=True)
    l = np.array([-0.35, -0.7, 0.62]); l /= np.linalg.norm(l); hv = l + [0, 0, 1]; hv /= np.linalg.norm(hv)
    nl = (nrm * l).sum(2); nh = np.clip((nrm * hv).sum(2), 0, 1)
    diff = np.clip(nl, 0, 1); spec = nh ** 24; sheen = nh ** 6
    fres = 1 - nrm[..., 2]
    base = np.array([200, 168, 190], np.float32)
    rgb = base * (0.30 + 0.55 * diff)[..., None] + np.array([236, 230, 255], np.float32) * (0.80 * spec + 0.12 * sheen)[..., None]
    a = np.clip(0.08 + 1.0 * fres + 0.65 * spec + 0.08 * sheen + 0.18 * (1 - diff), 0, 0.85)
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

# ---------------------------------------------------------------- embossed card v3 (procedural engraving relief)
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


def rose_head(R_, cx, cy, R, rot=0.0, squash=0.9, seed=0, lift=1.0):
    """front-facing cabbage rose, sculpted: big puffy outer petals, rows of small cupped petals,
    and a large stippled heart of stamens (as in the reference emboss)"""
    p = R_.patch(cx, cy, R * 1.08)
    if p is None:
        return
    sl, dx, dy = p
    rng = np.random.default_rng(seed)
    a = math.radians(rot)
    xr = dx * math.cos(a) + dy * math.sin(a); yr = (-dx * math.sin(a) + dy * math.cos(a)) / squash
    r = np.hypot(xr, yr); phi = np.arctan2(yr, xr)
    out = np.full(r.shape, -1.0, np.float32)
    # (outer radius, inner radius, petals, base height, puff amplitude, angular overlap)
    rings = [(1.00, 0.58, 8, 0.10, 0.50, 1.45), (0.86, 0.50, 9, 0.23, 0.40, 1.42), (0.73, 0.45, 11, 0.36, 0.30, 1.40),
             (0.62, 0.41, 13, 0.47, 0.21, 1.36), (0.53, 0.38, 15, 0.56, 0.15, 1.32), (0.46, 0.36, 17, 0.63, 0.10, 1.30)]
    for k, (fo, fi, n, base, amp, ov) in enumerate(rings):
        Ro, Ri = R * fo, R * fi
        ph0 = rng.random() * 6.283
        order = list(range(0, n, 2)) + list(range(1, n, 2))
        for jj, j in enumerate(order):
            th = ph0 + j * 2 * math.pi / n + rng.normal(0, 0.06)
            d = (phi - th + math.pi) % (2 * math.pi) - math.pi
            u = d / (math.pi / n * ov)
            inside = np.abs(u) < 1
            if not inside.any():
                continue
            wob = 1 + 0.03 * np.cos(u * 3 * math.pi + j * 1.7) + rng.normal(0, 0.02)
            e = Ri + (Ro * wob - Ri) * np.power(np.clip(1 - np.abs(u) ** 2.6, 0, 1), 0.5)
            t = np.clip((r - Ri * 0.7) / np.maximum(e - Ri * 0.7, 1), 0, 1)
            m = (r < e) & inside
            puff = amp * np.power(np.clip(1 - u * u, 0, 1), 0.35) * np.power(np.clip(np.sin(np.pi * np.clip(0.18 + 0.82 * t, 0, 1)), 0, 1), 0.55)
            de = np.minimum(e - r, (1 - np.abs(u)) * np.maximum(r, 1) * (math.pi / n * ov))
            edge = smooth01(de / (0.07 * R))                                       # rounded-off petal edge
            vein = 0.03 * np.cos(u * math.pi * 5) * t
            lipr = 0.055 * np.exp(-((de - 0.045 * R) / (0.016 * R)) ** 2)            # rolled rim just inside the edge
            hp = base + 0.035 * (j % 2) - 0.07 + (puff + 0.07 + vein + lipr) * edge
            out = np.where(m, hp, out)                                             # painter: later petals lie on top
    # stippled heart
    rc = R * 0.37
    cmask = r < rc
    heart = 0.68 + 0.14 * np.sqrt(np.clip(1 - (r / rc) ** 2, 0, 1))
    cen = np.zeros(r.shape, np.float32)
    nd = int(64 * (R / 110) ** 2)
    for i in range(nd):
        rr_ = rc * 0.96 * math.sqrt((i + 0.5) / nd); th = i * 2.39996 + rng.normal(0, 0.02)
        px, py = rr_ * math.cos(th), rr_ * math.sin(th)
        br = R * 0.052 * (1.15 - 0.3 * rr_ / rc)
        x0, x1 = px - br, px + br
        dd = np.hypot(xr - px, yr - py)
        cen = np.maximum(cen, 0.17 * _tube(dd, br))
    ring_groove = -0.05 * np.exp(-((r - rc) / (0.02 * R)) ** 2)
    out = np.where(cmask, heart + cen, out) + ring_groove * (out > -0.5)
    dome = 0.18 * np.sqrt(np.clip(1 - (r / (R * 1.02)) ** 2, 0, 1))
    m = (out > -0.5).astype(np.float32)
    m = cv2.GaussianBlur(m, (0, 0), 0.7 * R_.s)
    hgt = (np.maximum(out, 0) + dome) * 0.85 * lift + 0.1
    R_.put(sl, hgt, m)


def leaf(R_, bx, by, L, Wd, ang, seed=0, fold=1, lift=1.0, serr=True):
    """serrated rose leaf from its base point (bx,by), pointing at ang degrees; midrib + chevron veins"""
    a = math.radians(ang)
    cx, cy = bx + math.cos(a) * L / 2, by + math.sin(a) * L / 2
    p = R_.patch(cx, cy, L * 0.55 + 4)
    if p is None:
        return
    sl, dx, dy = p
    ux = dx * math.cos(a) + dy * math.sin(a); vy = -dx * math.sin(a) + dy * math.cos(a)
    u = ux / L + 0.5
    rng = np.random.default_rng(seed)
    uc = np.clip(u, 0, 1)
    hw = Wd / 2 * np.power(np.clip(np.sin(math.pi * np.power(uc, 0.85)), 0, 1), 0.75)
    if serr:
        tooth = (u * L / max(6.0, L / 9)) % 1.0
        hw = hw * (1 + 0.075 * (tooth - 0.5) * 2 * (uc > 0.12))
    vv = vy / np.maximum(hw, 0.5)
    m = smooth01((hw - np.abs(vy)) / 1.0) * (u > 0) * (u < 1)
    dome = 0.36 * np.power(np.clip(1 - vv ** 2, 0, 1), 0.6)
    tilt = 0.10 * fold * np.clip(vv, -1, 1)                                  # folded along the midrib
    midrib = 0.10 * np.exp(-(vy / 1.6) ** 2) - 0.06 * np.exp(-((np.abs(vy) - 3.2) / 1.4) ** 2)
    ph = uc * L / max(7.0, L / 7) - np.abs(vv) * 1.1
    veins = -0.06 * np.maximum(0, np.cos(2 * math.pi * ph)) ** 8 * (np.abs(vv) > 0.12) * (np.abs(vv) < 0.9)
    rim = 0.02 * np.exp(-((hw - np.abs(vy)) / 1.3) ** 2)
    hgt = (0.18 + dome + tilt + midrib + veins + rim) * lift
    R_.put(sl, hgt, m * (u > 0.0))


def compound_leaf(R_, x, y, ang, L, seed=0, lift=1.0, pairs=2):
    """rose leaf: a petiole with a terminal leaflet and pairs of side leaflets"""
    a = math.radians(ang)
    ex, ey = x + math.cos(a) * L * 0.62, y + math.sin(a) * L * 0.62
    stem(R_, [(x, y), (ex, ey)], 1.8, 1.3, lift=0.7 * lift)
    rng = np.random.default_rng(seed)
    for q in range(pairs):
        t = 0.30 + q * 0.32 if pairs > 1 else 0.5
        px, py = x + math.cos(a) * L * 0.62 * t, y + math.sin(a) * L * 0.62 * t
        ll = L * (0.40 + 0.06 * q)
        for sgn in (-1, 1):
            leaf(R_, px, py, ll * (0.9 + 0.2 * rng.random()), ll * 0.52, ang + sgn * (52 - 6 * q) + rng.normal(0, 5),
                 seed=seed + q * 2 + (sgn > 0), fold=sgn, lift=lift)
    leaf(R_, ex - math.cos(a) * 2, ey - math.sin(a) * 2, L * 0.50, L * 0.27, ang + rng.normal(0, 6), seed=seed + 9, fold=1, lift=lift)


def leaflet_pair(R_, x, y, ang, L, Wd, seed=0, lift=0.9):
    leaf(R_, x, y, L, Wd, ang - 38, seed=seed, fold=1, lift=lift)
    leaf(R_, x, y, L, Wd, ang + 38, seed=seed + 1, fold=-1, lift=lift)


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
        layer = np.zeros_like(hgt)
        p0 = (int((pts[i, 0] * s - x0) * 4), int((pts[i, 1] * s - y0) * 4))
        p1 = (int((pts[i + 1, 0] * s - x0) * 4), int((pts[i + 1, 1] * s - y0) * 4))
        cv2.line(layer, p0, p1, 1.0, max(1, int(round(w * 2))), cv2.LINE_AA, shift=2)
        hgt = np.maximum(hgt, layer)
    dt = cv2.distanceTransform((hgt > 0.5).astype(np.uint8), cv2.DIST_L2, 5) / max(1.0, w0 * s)
    prof = np.sqrt(np.clip(dt * (2 - dt), 0, 1))
    m = cv2.GaussianBlur(hgt, (0, 0), 0.5)
    reg = R_.h[y0:y1, x0:x1]
    reg[:] = reg * (1 - m) + np.maximum(reg, 0.15 + prof * 0.35 * lift) * m


def berry(R_, x, y, r, lift=1.0):
    p = R_.patch(x, y, r + 2)
    if p is None:
        return
    sl, dx, dy = p
    d = np.hypot(dx, dy)
    R_.put(sl, (0.2 + 0.45 * _tube(d, r)) * lift, smooth01((r - d) / 0.8))


def sprig(R_, x, y, ang, L, nb=4, r=4.2, seed=0):
    """thin stalk ending in a little cluster of round buds (the '4 dots' sprays of the reference)"""
    rng = np.random.default_rng(seed)
    a = math.radians(ang)
    ex, ey = x + math.cos(a) * L, y + math.sin(a) * L
    bend = rng.normal(0, 0.18)
    pts = _bez((x, y), (x + math.cos(a + bend) * L * .4, y + math.sin(a + bend) * L * .4),
               (ex - math.cos(a - bend) * L * .3, ey - math.sin(a - bend) * L * .3), (ex, ey), 16)
    stem(R_, pts, 1.6, 1.1, lift=0.7)
    for k in range(nb):
        b = a + (k - (nb - 1) / 2) * 0.95 + rng.normal(0, 0.1)
        ll = r * (2.4 + rng.random() * 0.8)
        bx, by = ex + math.cos(b) * ll, ey + math.sin(b) * ll
        stem(R_, [(ex, ey), (bx, by)], 1.0, lift=0.6)
        berry(R_, bx, by, r * (0.85 + 0.3 * rng.random()))
    berry(R_, ex, ey, r * 0.8)


def blossom(R_, x, y, r, rot=0, n=5, lift=0.9):
    p = R_.patch(x, y, r * 1.1 + 2)
    if p is None:
        return
    sl, dx, dy = p
    rr = np.hypot(dx, dy); ph = np.arctan2(dy, dx) - math.radians(rot)
    lob = np.cos((ph * n) / 2) ** 2
    e = r * (0.55 + 0.45 * np.abs(np.cos(ph * n / 2)) ** 0.6)
    m = smooth01((e - rr) / 1.0)
    cup = 0.22 * (rr / np.maximum(e, 1)) ** 2 + 0.10 * np.exp(-((e - rr) / 1.6) ** 2)
    groove = -0.08 * np.exp(-((np.abs(np.sin(ph * n / 2))) / 0.08) ** 2) * (rr > r * 0.25)
    cen = np.where(rr < r * 0.28, 0.25 + 0.15 * _tube(rr, r * 0.28), 0)
    R_.put(sl, (0.25 + cup + groove + cen) * lift, m)


def bud(R_, x, y, L, ang, lift=0.9):
    """closed rose bud: teardrop with wrapped petals + two sepals"""
    a = math.radians(ang)
    cx, cy = x + math.cos(a) * L * 0.5, y + math.sin(a) * L * 0.5
    p = R_.patch(cx, cy, L * 0.6 + 3)
    if p is None:
        return
    sl, dx, dy = p
    ux = dx * math.cos(a) + dy * math.sin(a); vy = -dx * math.sin(a) + dy * math.cos(a)
    u = ux / L + 0.5
    uc = np.clip(u, 0, 1)
    hw = L * 0.36 * np.sqrt(np.clip(np.sin(math.pi * uc ** 0.7), 0, 1))
    m = smooth01((hw - np.abs(vy)) / 0.9) * (u > 0) * (u < 1)
    vv = vy / np.maximum(hw, 0.5)
    wrap = 0.06 * np.maximum(0, np.cos((vv * 1.2 + uc * 1.5) * math.pi * 1.3)) ** 4
    hgt = (0.28 + 0.36 * np.sqrt(np.clip(1 - vv ** 2, 0, 1)) - wrap) * lift
    R_.put(sl, hgt, m)
    leaf(R_, x, y, L * 0.75, L * 0.18, ang - 28, serr=False, lift=0.8)
    leaf(R_, x, y, L * 0.75, L * 0.18, ang + 28, serr=False, lift=0.8)


def spray(R_, pts, leaves, w0=2.6, w1=1.4, seed=0, lift=1.0, side0=1, leaf_ang=42, tip=None):
    """a stem (bezier points) with leaves along it; leaves=[(t, L, W)] t in 0..1 along the stem"""
    pts = np.asarray(pts, np.float32)
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    stem(R_, pts, w0, w1, lift=lift * 0.8)
    side = side0
    for i, (t, L, Wd) in enumerate(leaves):
        d = t * seg[-1]; k = int(np.clip(np.searchsorted(seg, d) - 1, 0, len(pts) - 2))
        f = (d - seg[k]) / max(seg[k + 1] - seg[k], 1e-3)
        x, y = pts[k] + (pts[k + 1] - pts[k]) * f
        tang = math.degrees(math.atan2(pts[k + 1, 1] - pts[k, 1], pts[k + 1, 0] - pts[k, 0]))
        if Wd < 0:                                                        # paired leaflets
            leaflet_pair(R_, x, y, tang, L, -Wd, seed=seed + i)
        else:
            leaf(R_, x, y, L, Wd, tang + side * leaf_ang, seed=seed + i, fold=side, lift=lift)
        side = -side
    return pts


# ---------------------------------------------------------------- the cusped Mughal-arch frame
def arch_path(cx, ytop, ybot, hw, oh):
    """closed outline: ogee peak, two lobes split by a cusp, straight sides; mirrored at the bottom.
    hw = half width, oh = height of the ornamental top (and bottom) in px"""
    ky = oh / 0.98
    segs = [((0, 0), (-0.05, 0.08), (-0.10, 0.17), (-0.18, 0.20)),
            ((-0.18, 0.20), (-0.26, 0.22), (-0.36, 0.22), (-0.43, 0.25)),
            ((-0.43, 0.25), (-0.53, 0.27), (-0.585, 0.37), (-0.585, 0.50)),
            ((-0.585, 0.50), (-0.60, 0.555), (-0.65, 0.585), (-0.71, 0.585)),
            ((-0.71, 0.585), (-0.90, 0.595), (-1.0, 0.76), (-1.0, 0.98))]
    half = []
    for (p0, c1, c2, p3) in segs:
        pts = _bez(*[(cx + x * hw, ytop + y * ky) for x, y in (p0, c1, c2, p3)], 40)
        half += pts if not half else pts[1:]
    top = half[::-1] + [(2 * cx - x, y) for x, y in half][1:]         # left side -> peak -> right side
    bot = [(x, ytop + ybot - y) for x, y in reversed(top)]
    return np.array(top + bot, np.float32)


def card_relief(W=900, H=1950, s=2):
    R_ = Relief(W, H, s)
    S = s
    # ---------- frame (built from a signed distance field so every offset line follows the cusps) ----------
    cx, ytop, ybot, hw, oh = 450, 243, 1580, 352, 360
    outl = arch_path(cx, ytop, ybot, hw, oh)
    pm = np.zeros((R_.H, R_.W), np.uint8)
    cv2.fillPoly(pm, [np.round(outl * S * 16).astype(np.int32)], 1, cv2.LINE_AA, shift=4)
    din = cv2.distanceTransform(pm, cv2.DIST_L2, 5) / S
    dout = cv2.distanceTransform(1 - pm, cv2.DIST_L2, 5) / S
    sd = din - dout                                                    # >0 inside
    fr = np.zeros_like(sd)
    fr = np.maximum(fr, 0.60 * _tube(sd - 0.0, 5.0))                   # outer rounded moulding
    fr = np.maximum(fr, 0.40 * _tube(sd - 9.8, 2.4))                   # second, finer line
    # bead row
    cm = (sd >= 19.5).astype(np.uint8)
    cs, _ = cv2.findContours(cm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=len)[:, 0, :].astype(np.float32) / S
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(np.vstack([c, c[:1]]), axis=0).T))]
    beads = np.zeros_like(sd)
    step = 12.0
    nb = int(seg[-1] / step)
    yy, xx = np.mgrid[0:R_.H, 0:R_.W].astype(np.float32)
    for i in range(nb):
        d = i * seg[-1] / nb
        k = int(np.clip(np.searchsorted(seg, d) - 1, 0, len(c) - 1))
        bx, by = c[k]
        x0, x1 = int((bx - 6) * S), int((bx + 6) * S) + 1; y0, y1 = int((by - 6) * S), int((by + 6) * S) + 1
        dd = np.hypot(xx[y0:y1, x0:x1] / S - bx, yy[y0:y1, x0:x1] / S - by)
        beads[y0:y1, x0:x1] = np.maximum(beads[y0:y1, x0:x1], 0.46 * _tube(dd, 3.9))
    fr = np.maximum(fr, beads)
    R_.h += fr
    panel = smooth01((sd - 24) / 3)                                   # the smooth glossy centre
    outside = smooth01((-sd - 4) / 6)                                  # where ornaments may go

    # ---------- florals ----------
    F = Relief(W, H, s)
    rng = np.random.default_rng(5)

    def along(P, t):
        seg_ = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
        d = t * seg_[-1]; k = int(np.clip(np.searchsorted(seg_, d) - 1, 0, len(P) - 2))
        f = (d - seg_[k]) / max(seg_[k + 1] - seg_[k], 1e-3)
        x, y = P[k] + (P[k + 1] - P[k]) * f
        return x, y, math.degrees(math.atan2(P[k + 1, 1] - P[k, 1], P[k + 1, 0] - P[k, 0]))

    def vine(pts, n, seed, L=92, flowers=(), sprigs=(), w=2.8):
        P = np.asarray(pts, np.float32)
        stem(F, P, w, w * 0.7, lift=0.8)
        side = 1
        for i, t in enumerate(np.linspace(0.03, 0.97, n)):
            x, y, tg = along(P, t)
            compound_leaf(F, x, y, tg + side * (55 + rng.normal(0, 8)), L * (0.85 + 0.3 * rng.random()), seed=seed + i * 11,
                          pairs=1 if i % 3 == 2 else 2)
            side = -side
        for (x, y, r_) in flowers:
            for q in range(5):
                a_ = q * 1.2566 + rng.random()
                leaf(F, x + math.cos(a_) * r_ * 0.7, y + math.sin(a_) * r_ * 0.7, r_ * 1.3, r_ * 0.62, math.degrees(a_) + 18,
                     seed=seed + q, lift=0.75)
            blossom(F, x, y, r_, rot=x + y)
        for (x, y, a_) in sprigs:
            sprig(F, x, y, a_, 22, nb=4, r=3.9, seed=int(x * 7 + y))
        return P

    def bspray(pts, nleaf, seed, tips=(), L=62):
        P = np.asarray(pts, np.float32)
        stem(F, P, 2.2, 1.3, lift=0.75)
        side = 1
        for i, t in enumerate(np.linspace(0.25, 0.8, nleaf)):
            x, y, tg = along(P, t)
            leaf(F, x, y, L * (0.9 - 0.25 * t), L * 0.42 * (0.9 - 0.25 * t), tg + side * 50, seed=seed + i, fold=side)
            side = -side
        x, y, tg = along(P, 1.0)
        sprig(F, x, y, tg, 22, nb=4, r=4.0, seed=seed + 50)
        for (t, da) in tips:
            x, y, tg = along(P, t)
            sprig(F, x, y, tg + da, 22, nb=4, r=3.8, seed=seed + int(t * 100))

    # ---- top-left
    vine(_bez((52, 300), (70, 640), (18, 980), (48, 1390), 80), 22, 300, L=84,
         flowers=[(70, 560, 17), (28, 850, 18), (50, 1120, 17)], sprigs=[(105, 700, -30), (12, 990, 210), (100, 1250, -20)])
    compound_leaf(F, 90, 250, 112, 160, seed=101)
    compound_leaf(F, 60, 190, 165, 140, seed=102)
    compound_leaf(F, 190, 245, 48, 135, seed=103)
    compound_leaf(F, 85, 120, -115, 120, seed=104)
    compound_leaf(F, 150, 280, 88, 120, seed=105, pairs=1)
    bspray(_bez((190, 120), (235, 95), (280, 80), (330, 70), 20), 3, 110, tips=[(0.55, -70), (0.3, -110)])
    bspray(_bez((222, 185), (262, 195), (305, 196), (350, 188), 20), 2, 120, tips=[(0.6, 70), (0.75, -60)])
    rose_head(F, 128, 182, 136, rot=10, squash=0.94, seed=1)
    # ---- top-right
    vine(_bez((800, 350), (815, 470), (840, 600), (858, 720), 30), 5, 220, L=90, flowers=[(842, 590, 16)])
    vine(_bez((862, 700), (836, 900), (888, 1100), (852, 1460), 70), 18, 400, L=84,
         flowers=[(840, 830, 17), (874, 1060, 18), (846, 1300, 17)], sprigs=[(805, 950, 210), (800, 1190, 200)])
    compound_leaf(F, 700, 320, 140, 150, seed=201)
    compound_leaf(F, 770, 360, 95, 150, seed=202)
    compound_leaf(F, 850, 320, 40, 140, seed=203)
    compound_leaf(F, 690, 220, 200, 130, seed=204)
    compound_leaf(F, 800, 150, -60, 120, seed=205)
    bspray(_bez((660, 190), (615, 168), (570, 152), (520, 142), 20), 3, 210, tips=[(0.5, -80), (0.75, 70)])
    bspray(_bez((650, 268), (612, 274), (578, 266), (540, 256), 16), 2, 220, tips=[(0.6, 80)])
    rose_head(F, 762, 262, 145, rot=-15, squash=0.91, seed=2)
    # ---- bottom-left
    compound_leaf(F, 110, 1390, -100, 140, seed=501)
    compound_leaf(F, 60, 1420, -150, 130, seed=502)
    compound_leaf(F, 200, 1530, 30, 150, seed=503)
    compound_leaf(F, 90, 1560, 110, 140, seed=504)
    compound_leaf(F, 175, 1420, -45, 120, seed=505, pairs=1)
    bspray(_bez((210, 1525), (260, 1560), (310, 1605), (362, 1652), 24), 4, 510, tips=[(0.55, -70)], L=70)
    bspray(_bez((180, 1575), (205, 1645), (230, 1702), (258, 1752), 16), 2, 520, tips=[(0.7, -60)])
    rose_head(F, 112, 1476, 136, rot=25, squash=0.94, seed=3)
    # ---- bottom-right
    compound_leaf(F, 760, 1560, -95, 150, seed=601)
    compound_leaf(F, 690, 1590, -150, 140, seed=602)
    compound_leaf(F, 840, 1570, -40, 140, seed=603)
    compound_leaf(F, 690, 1700, 160, 140, seed=604)
    compound_leaf(F, 780, 1760, 95, 130, seed=605)
    compound_leaf(F, 870, 1740, 40, 120, seed=606, pairs=1)
    bspray(_bez((665, 1632), (615, 1642), (562, 1642), (508, 1632), 20), 3, 610, tips=[(0.55, 80), (0.75, -75)], L=68)
    bspray(_bez((690, 1735), (645, 1772), (602, 1796), (556, 1806), 20), 2, 620, tips=[(0.6, 75)])
    rose_head(F, 772, 1660, 145, rot=-30, squash=0.91, seed=4)
    floral = F.h * (1 - smooth01((sd + 30) / 14))                     # keep a clear margin round the frame
    R_.h = np.maximum(R_.h, floral)
    return R_, sd, panel


def render_card(W=900, H=1950, s=2):
    R_, sd, panel = card_relief(W, H, s)
    hm = R_.h
    HH, WW = hm.shape
    yy, xx = np.mgrid[0:HH, 0:WW].astype(np.float32)
    # fine brushed / linen grain on the paper (diagonal, like the reference)
    g = noise(HH, WW, 2, 1, 91)
    g = cv2.GaussianBlur(g, (0, 0), sigmaX=1.0)
    k = np.zeros((15, 15), np.float32); np.fill_diagonal(k, 1); k /= k.sum()
    brushed = cv2.filter2D(g, -1, k) - 0.5
    grain = brushed * 0.010 * (1 - 0.6 * panel) + (noise(HH, WW, 3, 2, 92) - 0.5) * 0.003
    hgt = cv2.GaussianBlur(hm, (0, 0), 1.1 * s) + grain
    # paper: matte satin; panel: smoother, glossier (the "mirror")
    sheen = 0.97 + 0.05 * np.sin((xx * 0.5 + yy * 0.3) / (420 * s)) + 0.03 * (noise(HH, WW, 500, 2, 22) - 0.5)
    col = hexrgb("#aea6b2") * sheen[..., None]
    rgb_p = shade(hgt, col, light=(-0.5, -0.7, 0.6), depth=34 * s / 2, amb=0.66, kd=0.42, ks=0.24, shin=12,
                  spec_rgb=(255, 248, 255))
    # ambient occlusion: crevices between petals/leaves go darker -> crisp engraved read
    blur = cv2.GaussianBlur(hm, (0, 0), 5 * s)
    occl = np.clip((blur - hm) * 2.4, 0, 1)
    rgb_p *= (1 - 0.32 * occl)[..., None]
    lift_l = np.clip(hm, 0, 1.2)
    rgb_p = rgb_p * (1 + 0.13 * lift_l)[..., None]
    # glossy panel: broad soft reflection, faint pearl tint
    u = (xx / WW); v = (yy / HH)
    refl = 0.5 + 0.5 * np.cos(((u - 0.35) * 1.6 + (v - 0.33) * 2.4) * math.pi)
    refl = np.clip(refl, 0, 1) ** 2
    tint = np.dstack([1 + 0.02 * np.sin(v * 9 + 1), 1 - 0.01 * np.sin(v * 7), 1 + 0.025 * np.sin(v * 8 + 2.5)])
    pcol = hexrgb("#c1b6bf") * tint * (0.98 + 0.07 * refl)[..., None]
    rgb_g = shade(hgt, pcol, light=(-0.5, -0.7, 0.6), depth=34 * s / 2, amb=0.70, kd=0.36, ks=0.30, shin=40,
                  spec_rgb=(255, 250, 255))
    rgb = rgb_p * (1 - panel[..., None]) + rgb_g * panel[..., None]
    light = 1.035 - 0.06 * v - 0.03 * u + 0.025 * np.exp(-(((u - 0.45) / 0.35) ** 2 + ((v - 0.35) / 0.3) ** 2))   # soft room light
    rgb = rgb * light[..., None]
    rgb = cv2.resize(rgb, (W, H), interpolation=cv2.INTER_AREA)
    pmask = cv2.resize(panel, (W, H), interpolation=cv2.INTER_AREA)
    return np.clip(rgb, 0, 255), pmask


def card():
    """the embossed card: sculpted cabbage roses + leaves in the corners, rose vines down both sides,
    the cusped arch frame with its beaded line, and the smooth glossy centre panel"""
    print("card (v3) ...")
    rgb, pm = render_card(W, H, 2)
    save_rgb("card.jpg", rgb, 92)          # the glossy sheen over the centre panel is drawn by app.js (same arch)


if __name__ == "__main__":
    which = sys.argv[1:] or ["envelope", "seal", "satin", "bow", "card", "pearl", "venue", "photo"]
    for w in which:
        globals()[w]()
