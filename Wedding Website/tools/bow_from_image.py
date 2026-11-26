"""Turn a cut-out picture of a real bow into the 34 untie frames the page plays.
    python tools/bow_from_image.py                 (reads tools/src/gemini_bow_cut.png, writes assets/gemini/bow/bow-NN.webp)
The loops are drawn into the knot, the tails swing out along the band and slip away, the knot lets go.
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
N = 34

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
    for i in range(N):
        t = i / (N - 1)
        p1 = sm(t / 0.62)                       # loops slip into the knot
        p2 = sm((t - 0.12) / 0.66)              # tails swing up to the band
        p3 = sm((t - 0.58) / 0.42)              # tails slide out, knot lets go
        fr = np.zeros((BH, BW, 4), np.float32)
        for name, sgn in (("tl", -1), ("tr", 1)):
            phi = 58 * sgn                       # tail direction, degrees from straight down
            M = shift(sgn * 330 * p3, -6 * p2) @ about(rot(-sgn * 55 * p2) @ rot(-phi) @ scl(1 - 0.30 * p2 - 0.25 * p3, 1 + 0.30 * p1) @ rot(phi))
            over(fr, warp(L[name], M), 1 - p3 ** 1.6)
        for name, sgn in (("ll", -1), ("lr", 1)):
            M = about(rot(sgn * 10 * p1) @ scl(1 - 0.90 * p1, 1 - 0.82 * p1))
            over(fr, warp(L[name], M), 1 - sm((t - 0.50) / 0.14))
        over(fr, warp(L["k"], about(scl(1 - 0.45 * p3, 1 - 0.55 * p3))), 1 - sm((t - 0.52) / 0.18))
        cv2.imwrite(str(OUT / ("bow-%02d.webp" % i)), finish(fr), [cv2.IMWRITE_WEBP_QUALITY, 90])
    print("wrote", N, "frames to", OUT)

if __name__ == "__main__":
    main()
