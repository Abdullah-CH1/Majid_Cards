"""Turn a cut-out picture of a real bow into the untie frames the page plays.
    python tools/bow_from_image.py                 (reads tools/src/gemini_bow_cut.png, writes assets/gemini/bow/bow-NN.webp)
    python tools/bow_from_image.py --src tools/src/other.png --knot 370,180 --loops 500 --out assets/bow2 --frames 78
        --knot   where the knot centre is in the source picture (pixels)
        --knot-size  half width,height of the knot in source pixels (default 87,122)
        --loops  how wide the two loops are together in the source picture (pixels); they are drawn SPAN wide on the card

The movement follows the reference video frame by frame (its frames 162 to 198, 30 per second;
our frame i stands for video frame V0 + (V1 - V0) * i / (N - 1)):
  163-172  the left loop is pulled into the knot: it slides in, flattening, and disappears behind the knot (no fade)
  166-178  the right loop and the right tail are whisked off up and to the right together, accelerating,
           stretched and motion-blurred along their path, until they leave the card
  163-178  the flat band is drawn tight: it gathers into the knot from both sides
  178-182  the left tail hangs on its own at full length
  181-196  the left tail swings up towards the band and slips up through the knot, getting shorter
  190-198  the knot shrinks and lets go; what is left is exactly the two gathered band halves (assets/ribbon.webp)
Nothing moves more than about 25 px from one frame to the next unless it is blurred along its motion.
"""
from pathlib import Path
import numpy as np, cv2

HERE = Path(__file__).resolve().parent
SRC = HERE / "src" / "gemini_bow_cut.png"
RIBBON = HERE.parent / "assets" / "ribbon.webp"
OUT = HERE.parent / "assets" / "gemini" / "bow"
BW, BH, CX, CY = 900, 720, 450, 235          # frame canvas and where the knot sits (same as the rendered bow)
BAND_Y, BAND_H = 105, 260                    # rows of the canvas the band picture covers (the page puts the band halves exactly there)
KX, KY, LOOPS = 880, 730, 1360               # knot and loop span in the source picture
SPAN = 520                                   # loop span on the canvas (the card is 900 wide)
N = 78                                       # frames; the page plays them in 1.3 s (60 per second)
import argparse as _ap
_a = _ap.ArgumentParser(); _a.add_argument("--src"); _a.add_argument("--knot"); _a.add_argument("--loops", type=float)
_a.add_argument("--span", type=float); _a.add_argument("--out"); _a.add_argument("--frames", type=int)
_a.add_argument("--knot-size", dest="ksize")   # half width,height of the knot in source pixels
_o, _ = _a.parse_known_args()
if _o.src: SRC = Path(_o.src).resolve()
if _o.knot: KX, KY = (float(v) for v in _o.knot.split(","))
if _o.loops: LOOPS = _o.loops
if _o.span: SPAN = _o.span
if _o.out: OUT = (HERE.parent / _o.out).resolve()
if _o.frames: N = _o.frames
KRX, KRY = (float(v) for v in _o.ksize.split(",")) if _o.ksize else (87.0, 122.0)
V0, V1 = 162.0, 198.0                        # the video frames the sequence covers

def sm(x):
    x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)

def ss(x):                                   # slower start and settle
    x = np.clip(x, 0, 1); return x * x * x * (x * (6 * x - 15) + 10)

def about(M):                                # 3x3 transform applied about the knot
    T = np.array([[1, 0, CX], [0, 1, CY], [0, 0, 1.0]]); Ti = np.array([[1, 0, -CX], [0, 1, -CY], [0, 0, 1.0]])
    return T @ M @ Ti

def rot(deg):
    a = np.radians(deg); return np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1.0]])

def scl(sx, sy): return np.diag([sx, sy, 1.0])
def shift(dx, dy): return np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1.0]])

def warp(layer, M):
    return cv2.warpAffine(layer, M[:2].astype(np.float32), (BW, BH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)

def over(dst, src, op=1.0):                  # premultiplied "over"
    a = src[..., 3:4] * op
    dst[..., :3] = src[..., :3] * op + dst[..., :3] * (1 - a); dst[..., 3:4] = a + dst[..., 3:4] * (1 - a)

def mblur(layer, vx, vy):                    # motion blur along (vx, vy): the distance the piece travels in one frame
    n = float(np.hypot(vx, vy))
    if n < 3: return layer
    s = int(np.ceil(n)) | 1; c = s // 2; k = np.zeros((s * 4, s * 4), np.float32)
    ux, uy = vx / n * n / 2 * 4, vy / n * n / 2 * 4
    cv2.line(k, (int(c * 4 + 2 - ux), int(c * 4 + 2 - uy)), (int(c * 4 + 2 + ux), int(c * 4 + 2 + uy)), 1.0, 4)
    k = cv2.resize(k, (s, s), interpolation=cv2.INTER_AREA); k /= k.sum()
    return cv2.filter2D(layer, -1, k, borderType=cv2.BORDER_CONSTANT)

def with_shadow(pm):                         # the bow's soft contact shadow (premultiplied in, premultiplied out)
    a = pm[..., 3]
    def cast(sig, dy_, dx_):
        s = cv2.GaussianBlur(a, (0, 0), sig); return cv2.warpAffine(s, np.float32([[1, 0, dx_], [0, 1, dy_]]), (BW, BH))
    sh = np.clip(0.26 * cast(5, 6, 3) + 0.20 * cast(14, 13, 6), 0, 0.5) * (1 - a)
    out = pm.copy(); out[..., :3] += np.array([64, 48, 72], np.float32) * sh[..., None]; out[..., 3] += sh
    return out

def band_layers():
    """the band at any gather g: 0 = flat across the card, 1 = the two gathered halves of assets/ribbon.webp (exactly)"""
    r = cv2.imread(str(RIBBON), cv2.IMREAD_UNCHANGED).astype(np.float32)
    assert r.shape[:2] == (BAND_H, BW), r.shape
    a = r[..., 3] / 255; pm = np.dstack([r[..., :3] * a[..., None], a])
    cols = np.arange(BW); ys = np.arange(BAND_H, dtype=np.float32)
    top = np.array([ys[a[:, x] > 0.5].min() if (a[:, x] > 0.5).any() else BAND_H / 2 for x in cols], np.float32)
    bot = np.array([ys[a[:, x] > 0.5].max() if (a[:, x] > 0.5).any() else BAND_H / 2 for x in cols], np.float32)
    top = cv2.GaussianBlur(top[None], (0, 0), 3)[0]; bot = cv2.GaussianBlur(bot[None], (0, 0), 3)[0]
    # flat band: the fabric near each side edge, drawn across to the centre (its streaks run along the band, so this reads as one flat ribbon)
    half = BW // 2; src_x = np.empty(BW, np.float32)
    src_x[:half] = np.linspace(0, half * 0.30, half); src_x[half:] = np.linspace(BW - 1 - half * 0.30, BW - 1, BW - half)
    wc = sm((cols - (half - 70)) / 140.0).astype(np.float32)                    # the two sides are blended across the middle so the flat band has no seam
    ft = float(top[:8].mean()) * (1 - wc) + float(top[-8:].mean()) * wc; fb = float(bot[:8].mean()) * (1 - wc) + float(bot[-8:].mean()) * wc
    bump = np.exp(-((cols - half) / 60.0) ** 2).astype(np.float32)[None, :, None]
    my0, mx0 = np.mgrid[0:BAND_H, 0:BW].astype(np.float32)
    def band(g):
        t_, b_ = ft + (top - ft) * g, fb + (bot - fb) * g                       # this column's band edges at gather g
        v = (my0 - t_[None]) / np.maximum(b_ - t_, 1e-3)[None]                    # 0..1 across the band
        flat = cv2.remap(pm, np.repeat(src_x[None], BAND_H, 0), (ft[None] + v * (fb - ft)[None]).astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        flat = flat * (1 - bump) + cv2.blur(flat, (121, 1)) * bump
        real = cv2.remap(pm, mx0, (top[None] + v * (bot - top)[None]).astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        inside = (sm((v + 0.02) / 0.04) * sm((1.02 - v) / 0.04) * ((b_ - t_) > 1.5)[None])[..., None]
        mix = sm((g - 0.35) / 0.65)                                               # the gathered pleats come in as it tightens
        out = (flat * (1 - mix) + real * mix) * inside
        if g >= 0.999: out = pm
        full = np.zeros((BH, BW, 4), np.float32); full[BAND_Y:BAND_Y + BAND_H] = out
        return full
    return band

def main():
    c = cv2.imread(str(SRC), cv2.IMREAD_UNCHANGED).astype(np.float32)
    k = SPAN / LOOPS
    b = cv2.warpAffine(c, np.float32([[k, 0, CX - KX * k], [0, k, CY - KY * k]]), (BW, BH), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    rgb, a = b[..., :3], b[..., 3] / 255 * 0.96
    rgb = rgb * 0.90 + np.array([178, 160, 176], np.float32) * 0.10            # a breath of the card's mauve so the bow belongs to the scene
    rgb = np.where(rgb > 232, 232 + (rgb - 232) * 0.5, rgb)
    pm = np.dstack([rgb * a[..., None], a]).astype(np.float32)                # premultiplied
    yy, xx = np.mgrid[0:BH, 0:BW].astype(np.float32); dx, dy = xx - CX, yy - CY
    ang = np.degrees(np.arctan2(dy, np.abs(dx) + 1e-3))                        # 0 = along the band, 90 = straight down
    tail = sm((ang - 26) / 10); r = np.hypot(dx / (KRX * k), dy / (KRY * k))
    knot = 1 - sm((r - 0.9) / 0.25); left = sm((-dx + 4) / 8); right = 1 - left
    L = {n: pm * m[..., None] for n, m in {"tl": tail * left * (1 - knot), "tr": tail * right * (1 - knot),
                                              "ll": (1 - tail) * left * (1 - knot), "lr": (1 - tail) * right * (1 - knot), "k": knot}.items()}
    dirs = {}                                                                  # each tail's own direction and length from the knot
    for name in ("tl", "tr"):
        w = L[name][..., 3] * (np.hypot(dx, dy) > 60); mx, my = (w * dx).sum() / w.sum(), (w * dy).sum() / w.sum()
        n = np.hypot(mx, my); dirs[name] = (mx / n, my / n, float(((dx * mx + dy * my) / n)[w > 0.5].max()))
    band = band_layers()
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("bow-*.webp"): f.unlink()

    def through_knot(name, p, sway):                                           # a tail drawn back through the knot along itself, gathering as it nears it
        ux0, uy0, ln = dirs[name]; ca, sa = np.cos(np.radians(sway)), np.sin(np.radians(sway))
        ux, uy = ca * ux0 - sa * uy0, sa * ux0 + ca * uy0                          # its direction once swung by `sway` about the knot
        lay = warp(L[name], shift(-ux * (ln + 24) * p, -uy * (ln + 24) * p) @ about(rot(sway)))
        proj = dx * ux + dy * uy; perp = -dx * uy + dy * ux
        f = 1 - sm(p * 2.5) * (1 - (0.25 + 0.75 * sm(proj / 150)))               # it narrows where it goes into the knot
        lay = cv2.remap(lay, (CX + proj * ux - perp / f * uy).astype(np.float32), (CY + proj * uy + perp / f * ux).astype(np.float32),
                        cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        return lay * sm((proj - 2) / 10)[..., None]                            # what has gone through is behind the knot

    def centroid(name):
        w = L[name][..., 3]; return np.array([(w * xx).sum() / w.sum(), (w * yy).sum() / w.sum(), 1.0])
    c_lr, c_tr, HS = centroid("lr"), centroid("tr"), SPAN / 2
    D = BW - CX + 0.25 * HS                                                    # far enough that the right side has left the card

    def pose(v):                                                               # every piece's state at video frame v
        pv = lambda a_, b_: float(np.clip((v - a_) / (b_ - a_), 0, 1))
        P = {}
        P["ll"] = ss(pv(163, 172.5))                                           # left loop pulled into the knot
        q = pv(166, 178.5) ** 1.6                                              # right loop + tail whisked off up-right (accelerating)
        P["q"] = q
        P["Mr"] = shift(D * q, -0.30 * D * q) @ about(rot(-8 * q) @ scl(1 + 0.45 * q, 1 - 0.2 * q))
        P["Mtr"] = P["Mr"] @ about(rot(-30 * sm(q * 1.4)))                     # the tail swings up towards the band as it goes
        P["tl"] = sm(pv(181, 196))                                             # left tail, last, slips up through the knot
        P["sway"] = -3.5 * np.sin(np.pi * pv(165, 178)) + 24 * sm(pv(182, 193))  # tugged, then swings up towards the band
        P["k"] = pv(190, 198)
        P["g"] = 0.22 + 0.78 * sm(pv(163, 178))                                # band drawn tight
        return P

    dv = (V1 - V0) / (N - 1)
    for i in range(N):
        v = V0 + (V1 - V0) * i / (N - 1)                                       # the video frame this picture stands for
        P, Pp = pose(v), pose(v - dv)
        g = P["g"]
        bow = np.zeros((BH, BW, 4), np.float32)
        # right tail and right loop: whisked away together, blurred by how far they went since the last frame
        for nm, M, Mp, c in (("tr", P["Mtr"], Pp["Mtr"], c_tr), ("lr", P["Mr"], Pp["Mr"], c_lr)):
            d = (M @ c - Mp @ c)[:2]; d = d * min(1.0, 70 / max(1e-3, float(np.hypot(*d)) * 1.3))
            over(bow, mblur(warp(L[nm], M), d[0] * 1.3, d[1] * 1.3), 1 - 0.8 * sm((P["q"] - 0.55) / 0.45))
        # left tail
        over(bow, through_knot("tl", P["tl"], P["sway"]))
        # left loop: slides into the knot, flattening, and is hidden where it has gone in
        p = P["ll"]
        ll = warp(L["ll"], shift(0.55 * HS * p, 0) @ about(rot(6 * np.sin(np.pi * p)) @ scl(1 - 0.5 * p, 1 - 0.6 * p)))
        over(bow, ll * (1 - sm(p * 6) * sm((dx + 0.12 * HS) / 16))[..., None])
        # knot: shrinks and lets go
        p_k = P["k"]; kk = 1 - 0.7 * sm(p_k)
        over(bow, warp(L["k"], about(scl(kk, kk))), 1 - sm((p_k - 0.3) / 0.7))
        fr = band(g); over(fr, with_shadow(bow))
        al = fr[..., 3]; out = np.dstack([np.clip(fr[..., :3] / np.maximum(al[..., None], 1e-4), 0, 255), al * 255]).astype(np.uint8)
        cv2.imwrite(str(OUT / ("bow-%02d.webp" % i)), out, [cv2.IMWRITE_WEBP_QUALITY, 90])
    print("wrote", N, "frames to", OUT)

if __name__ == "__main__":
    main()
