"""Turn a cut-out picture of a real bow into the untie frames the page plays.
    python tools/bow_from_image.py                 (reads tools/src/gemini_bow_cut.png, writes assets/gemini/bow/bow-NN.webp)
One loop after the other is drawn into the knot, then each tail slips up through it, and the knot lets go.
"""
import sys
from pathlib import Path
import numpy as np, cv2

HERE = Path(__file__).resolve().parent
SRC = HERE / "src" / "gemini_bow_cut.png"
OUT = HERE.parent / "assets" / "gemini" / "bow"
BW, BH, CX, CY = 900, 720, 450, 235          # frame canvas and where the knot sits (same as the rendered bow)
KX, KY, LOOPS = 880, 730, 1360               # knot and loop span in the source picture
SPAN = 470                                   # loop span on the canvas (the card is 900 wide)
N = 48

def sm(x):
    x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)

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

def finish(pm):                              # un-premultiply, add the soft contact shadow, write
    a = pm[..., 3]; rgb = pm[..., :3] / np.maximum(a[..., None], 1e-4)
    s1 = np.roll(np.roll(cv2.GaussianBlur(a, (0, 0), 5), 6, 0), 3, 1); s2 = np.roll(np.roll(cv2.GaussianBlur(a, (0, 0), 14), 13, 0), 6, 1)
    sh = np.clip(0.26 * s1 + 0.20 * s2, 0, 0.5); A = a + sh * (1 - a)
    out = (rgb * a[..., None] + np.array([64, 48, 72], np.float32) * (sh * (1 - a))[..., None]) / np.maximum(A[..., None], 1e-4)
    return np.dstack([np.clip(out, 0, 255), A * 255]).astype(np.uint8)

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
    tail = sm((ang - 26) / 10); r = np.hypot(dx / 30.0, dy / 42.0)
    knot = 1 - sm((r - 0.9) / 0.25); left = sm((-dx + 4) / 8); right = 1 - left
    L = {n: pm * m[..., None] for n, m in {"tl": tail * left * (1 - knot), "tr": tail * right * (1 - knot),
                                              "ll": (1 - tail) * left * (1 - knot), "lr": (1 - tail) * right * (1 - knot), "k": knot}.items()}
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("bow-*.webp"): f.unlink()
    # each tail's own direction (from the knot to the middle of the tail), so it can be drawn back through the knot along itself
    dirs = {}
    for name in ("tl", "tr"):
        w = L[name][..., 3] * (np.hypot(dx, dy) > 60); mx, my = (w * dx).sum() / w.sum(), (w * dy).sum() / w.sum()
        n = np.hypot(mx, my); dirs[name] = (mx / n, my / n, float(((dx * mx + dy * my) / n)[w > 0.5].max()))
    # the pull happens one piece after another, as it does by hand: right loop, left loop, then each tail slips up through the knot
    seq = {"lr": (0.00, 0.40), "ll": (0.14, 0.56), "tr": (0.30, 0.74), "tl": (0.44, 0.90), "k": (0.84, 1.00)}
    def prog(name, t):
        a, b = seq[name]; x = np.clip((t - a) / (b - a), 0, 1); return x * x * x * (x * (6 * x - 15) + 10)      # slow start, slow settle
    for i in range(N):
        t = i / (N - 1)
        fr = np.zeros((BH, BW, 4), np.float32)
        for name, sgn in (("tl", -1), ("tr", 1)):
            ux, uy, ln = dirs[name]; p = prog(name, t)
            lead = prog("lr" if name == "tr" else "ll", t)                     # while its loop is drawn in, the tail is tugged and sways a little
            sway = sgn * (3.0 * np.sin(np.pi * lead) - 5.0 * np.sin(np.pi * p) * (1 - p))
            M = shift(-ux * (ln + 24) * p, -uy * (ln + 24) * p) @ about(rot(sway))
            lay = warp(L[name], M)
            proj = dx * ux + dy * uy; perp = -dx * uy + dy * ux                # the ribbon gathers as it nears the knot, so it funnels into it
            f = 1 - min(1.0, p * 5) * (1 - (0.20 + 0.80 * sm(proj / 150)))
            lay = cv2.remap(lay, (CX + proj * ux - perp / f * uy).astype(np.float32), (CY + proj * uy + perp / f * ux).astype(np.float32),
                            cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
            lay = lay * sm((proj - 2) / 10)[..., None]                         # whatever has passed the knot is gone
            over(fr, lay)
        for name, sgn in (("ll", -1), ("lr", 1)):
            p = prog(name, t)
            M = about(rot(-sgn * 7 * np.sin(np.pi * p)) @ scl(1 - 0.97 * p, 1 - 0.90 * p ** 1.25))
            over(fr, warp(L[name], M), 1 - sm((p - 0.93) / 0.07))
        pk = prog("k", t); tug = 1 + 0.05 * np.sin(np.pi * prog("tl", t))
        over(fr, warp(L["k"], about(scl((1 - 0.75 * pk) * (2 - tug), (1 - 0.75 * pk) * tug))), 1 - sm((pk - 0.45) / 0.55))
        cv2.imwrite(str(OUT / ("bow-%02d.webp" % i)), finish(fr), [cv2.IMWRITE_WEBP_QUALITY, 90])
    print("wrote", N, "frames to", OUT)

if __name__ == "__main__":
    main()
