"""Use a ready-made picture as the envelope artwork instead of the generated leaves.
    python tools/envelope_from_image.py <picture>        (any size; it is cropped to 900:1950 from its centre)
Writes the same files the page already uses (assets/envelope-*.webp), cut along the page's flap geometry:
top flap edges from 33.5 % at the sides to the tip at 53.5 %, envelope mouth from 30 % to 47.8 %.
The previous files are copied to assets/_envelope_generated/ the first time, so it can be undone.
"""
import sys, shutil
from pathlib import Path
import numpy as np, cv2

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "assets"
W, H = 900, 1950
FH, SH = 1092, 1152                          # flap image height, flap-shadow image height
NAMES = ["envelope-body.webp", "envelope-flap.webp", "envelope-flap-dim.webp", "envelope-flap-back.webp", "envelope-flap-shadow.webp"]

def smooth01(x):
    x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)

def save(name, bgr, alpha, q=90):
    bgra = np.dstack([np.clip(bgr, 0, 255).astype(np.uint8), (np.clip(alpha, 0, 1) * 255).astype(np.uint8)])
    cv2.imwrite(str(OUT / name), bgra, [cv2.IMWRITE_WEBP_QUALITY, q]); print("wrote", name, bgra.shape[1], "x", bgra.shape[0])

def main(src):
    global OUT
    if len(sys.argv) > 2:
        OUT = HERE.parent / sys.argv[2]; OUT.mkdir(parents=True, exist_ok=True)
    bak = OUT / "_envelope_generated"
    if len(sys.argv) <= 2 and not bak.exists():
        bak.mkdir()
        for n in NAMES: shutil.copy(OUT / n, bak / n)
    im = cv2.imread(src)
    h, w = im.shape[:2]
    TIP = float(sys.argv[3]) if len(sys.argv) > 3 else None      # where the flap's point is in the picture (0..1 of its height)
    ZOOM = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0      # 1 = the picture's full width is shown
    if TIP is None:                                              # simple centre crop
        if w / h > W / H:
            nw = int(round(h * W / H)); x0 = (w - nw) // 2; im = im[:, x0:x0 + nw]
        else:
            nh = int(round(w * H / W)); y0 = (h - nh) // 2; im = im[y0:y0 + nh]
        art = cv2.resize(im, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32)
    else:
        # show (almost) the whole picture: full width, and its height gently re-spaced so that the picture's own flap
        # point lands exactly where the animation lifts the flap (53.5 % down). Above and below the point are scaled separately.
        sc = W * ZOOM / w; xs = (np.arange(W, dtype=np.float32) + (w * sc - W) / 2) / sc
        tip_src, tip_dst = TIP * h, 0.535 * H
        yd = np.arange(H, dtype=np.float32)
        ys = np.where(yd <= tip_dst, yd * tip_src / tip_dst, tip_src + (yd - tip_dst) * (h - tip_src) / (H - tip_dst))
        print("vertical scale above / below the flap point: %.2f / %.2f" % (tip_dst / (tip_src * sc), (H - tip_dst) / ((h - tip_src) * sc)))
        mx, my = np.meshgrid(xs, ys)
        art = cv2.remap(cv2.GaussianBlur(im, (0, 0), 0.6), mx.astype(np.float32), my.astype(np.float32), cv2.INTER_AREA if sc < 1 else cv2.INTER_CUBIC).astype(np.float32)
    # gentle grade toward the site's dusty mauve (target mean about R152 G140 B152), keeping the picture's own light and shade
    mean = art.reshape(-1, 3).mean(0); target = np.array([152, 140, 152], np.float32)      # BGR order happens to be symmetric here
    art = np.clip(art * (1 + 0.8 * (target / mean - 1)), 0, 255)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    t = 1 - np.abs(xx - W / 2) / (W / 2)                       # 0 at the sides, 1 at the centre
    flap_edge = H * (0.335 + (0.535 - 0.335) * t)              # lower edge of the top flap
    mouth_edge = H * (0.30 + (0.478 - 0.30) * t)               # opening of the envelope under it
    # ---- top flap (its own sheet) ----
    fa = smooth01((flap_edge - yy) / 2.0 + 0.5)[:FH]
    near = np.clip((flap_edge - yy) / 7.0, 0, 1)[:FH]          # a thin lit paper edge along the cut
    flap = art[:FH] * (1 + 0.02 * (1 - near))[..., None]
    save("envelope-flap.webp", flap, fa)
    save("envelope-flap-dim.webp", flap * np.array([0.50, 0.44, 0.50], np.float32), fa)
    back = cv2.GaussianBlur(art[:FH], (0, 0), 28) * 0.93
    save("envelope-flap-back.webp", back, fa)
    # ---- soft shadow the closed flap casts on the envelope ----
    d = (yy - flap_edge)[:SH]
    sh = np.exp(-np.clip(d, 0, None) / 16.0) * (d > -2) * 0.12
    save("envelope-flap-shadow.webp", np.zeros((SH, W, 3), np.float32) + np.array([40, 26, 40], np.float32), sh)
    # ---- body: everything below the mouth ----
    ba = smooth01((yy - mouth_edge) / 2.0 + 0.5)
    hem = np.clip((yy - mouth_edge) / 9.0, 0, 1)
    body = art * (1 - 0.03 * (1 - hem))[..., None]
    save("envelope-body.webp", body, ba)

if __name__ == "__main__":
    main(sys.argv[1])
