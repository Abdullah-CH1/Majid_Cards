"""Renders the bow-untie frames with the TEXTURED 3D bow (ribbon3d_tex: the real crinkled satin of the client's Gemini picture)
into assets/bow-tex3d/bow-NN.webp, exactly the way make_assets.bow_frames() does (frame 0 full size q88, others 80 % q68).
Same geometry, same untie timing; ribbon.webp is not touched."""
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np, cv2

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ribbon3d_tex as R

OUT = HERE.parent / "assets" / "bow-tex3d"

def save_rgba(path, rgb, a, q):
    bgra = np.dstack([cv2.cvtColor(rgb.astype(np.uint8), cv2.COLOR_RGB2BGR), (np.clip(a, 0, 1) * 255).astype(np.uint8)])   # as make_assets.save_rgba
    cv2.imwrite(str(path), bgra, [cv2.IMWRITE_WEBP_QUALITY, q])

def main(n=34):
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("bow-*.webp"):
        f.unlink()
    with ProcessPoolExecutor(max_workers=6) as ex:
        frames = list(ex.map(R.render, [i / (n - 1) for i in range(n)]))
    for i, (rgb, a) in enumerate(frames):
        if i == 0:
            save_rgba(OUT / "bow-00.webp", rgb, a, 88)
        else:
            sz = (R.BW * 4 // 5, R.BH * 4 // 5)
            save_rgba(OUT / f"bow-{i:02d}.webp", cv2.resize(rgb, sz, interpolation=cv2.INTER_AREA), cv2.resize(a, sz, interpolation=cv2.INTER_AREA), 68)
    print("wrote", n, "frames to", OUT)

if __name__ == "__main__":
    main()
