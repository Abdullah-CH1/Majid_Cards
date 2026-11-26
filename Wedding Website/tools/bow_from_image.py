"""Turn a cut-out picture of a real bow into the untie frames the page plays.
    python tools/bow_from_image.py                 (reads tools/src/gemini_bow_cut.png, writes assets/gemini/bow/bow-NN.webp)

The movement follows the reference video frame by frame (its frames 162 to 198, 30 per second):
  162-171  the left loop is drawn into the knot
  166-177  the right loop and the right tail are pulled away to the right along the band (fast, blurred)
  162-176  the flat band is drawn tight: it gathers into the knot from both sides
  177-191  the left tail, the last piece, slips up through the knot
  189-198  the knot lets go; what is left is exactly the two gathered band halves (assets/ribbon.webp)
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
N = 40                                       # frames; the page plays them in 1.3 s
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

def smear(layer, px):                        # motion blur along the band for a piece that is whisked away
    px = int(px)
    return layer if px < 3 else cv2.blur(layer, (px, max(1, px // 6)))

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
    tail = sm((ang - 26) / 10); r = np.hypot(dx / (87 * k), dy / (122 * k))
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

    def through_knot(name, p, sway, blur=0):                                   # a tail drawn back through the knot along itself, gathering as it nears it
        ux, uy, ln = dirs[name]
        lay = warp(L[name], shift(-ux * (ln + 24) * p, -uy * (ln + 24) * p) @ about(rot(sway)))
        proj = dx * ux + dy * uy; perp = -dx * uy + dy * ux
        f = 1 - min(1.0, p * 5) * (1 - (0.20 + 0.80 * sm(proj / 150)))
        lay = cv2.remap(lay, (CX + proj * ux - perp / f * uy).astype(np.float32), (CY + proj * uy + perp / f * ux).astype(np.float32),
                        cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        return smear(lay * sm((proj - 2) / 10)[..., None], blur)

    for i in range(N):
        v = V0 + (V1 - V0) * i / (N - 1)                                       # the video frame this picture stands for
        pv = lambda a_, b_: np.clip((v - a_) / (b_ - a_), 0, 1)
        p_ll = ss(pv(162, 171.5))                                              # left loop into the knot
        p_lr = pv(166, 177) ** 1.8                                             # right loop whisked off to the right (it accelerates away)
        p_tr = pv(168, 176.5) ** 1.5                                           # right tail follows it through the knot
        p_tl = ss(pv(177, 191.5))                                              # left tail, last, slips up through the knot
        p_k = sm(pv(189, 197.5))
        g = 0.22 + 0.78 * sm(pv(162, 177))                                     # band drawn tight
        bow = np.zeros((BH, BW, 4), np.float32)
        # tails (under the loops)
        over(bow, through_knot("tr", p_tr, 6 * np.sin(np.pi * p_tr), blur=70 * np.sin(np.pi * min(1, p_tr * 1.15))), 1 - sm((p_tr - 0.75) / 0.25))
        tug = np.sin(np.pi * pv(164, 177))                                     # while the right side is pulled the left tail is tugged, then it goes
        over(bow, through_knot("tl", p_tl, -3.5 * tug - 14 * sm(p_tl / 0.6) * (1 - 0.3 * p_tl)))
        # loops
        over(bow, warp(L["ll"], about(rot(7 * np.sin(np.pi * p_ll)) @ scl(1 - 0.97 * p_ll, 1 - 0.90 * p_ll ** 1.25))), 1 - sm((p_ll - 0.93) / 0.07))
        lr = warp(L["lr"], shift(300 * p_lr, 0) @ about(rot(-10 * sm(p_lr * 2)) @ scl(1 + 0.55 * p_lr, 1 - 0.72 * sm(p_lr * 1.3))))
        over(bow, smear(lr, 90 * np.sin(np.pi * min(1, p_lr * 1.1))), 1 - sm((p_lr - 0.45) / 0.5))
        # knot
        kk = 1 - 0.78 * p_k
        over(bow, warp(L["k"], about(scl(kk, kk))), 1 - sm((p_k - 0.55) / 0.45))
        fr = band(g); over(fr, with_shadow(bow))
        al = fr[..., 3]; out = np.dstack([np.clip(fr[..., :3] / np.maximum(al[..., None], 1e-4), 0, 255), al * 255]).astype(np.uint8)
        cv2.imwrite(str(OUT / ("bow-%02d.webp" % i)), out, [cv2.IMWRITE_WEBP_QUALITY, 90])
    print("wrote", N, "frames to", OUT)

if __name__ == "__main__":
    main()
