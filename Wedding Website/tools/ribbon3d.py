"""Tiny 3D ribbon renderer for sheer organza (bow, tails, knot, band) + bow-untie animation frames.
Each ribbon = centre path P(t) in 3D, width w(t), cross direction B(t). Rendered as quads, back to front,
with two-sided lighting, a fresnel-like opacity (sheer fabric is more opaque where it turns away),
bright hems along both edges and a fine woven sheen.
"""
import math
import numpy as np, cv2

LIGHT = np.array([-0.45, -0.75, 0.55]); LIGHT /= np.linalg.norm(LIGHT)
VIEW = np.array([0, 0, 1.0])
HALF = (LIGHT + VIEW); HALF /= np.linalg.norm(HALF)
BASE = np.array([226, 206, 219], np.float32)        # dusty mauve-pink organza (RGB), same family as the wrap

def norm(v):
    return v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-9)

def strip(P, w, B, ns=15, weave=0.0, pleat=0.0):
    """make quads for one ribbon piece. P: (N,3), w: (N,), B: (N,3)  -> list of (z, pts2d(4,2), rgb, alpha)"""
    P = np.asarray(P, np.float32).copy(); B = norm(np.asarray(B, np.float32)); w = np.asarray(w, np.float32)
    rr = np.random.default_rng(len(P) + int(abs(P[0, 0])) + int(abs(P[0, 1])))
    def smooth_noise(n, k):
        g = rr.standard_normal(max(4, n // k + 3)); return np.interp(np.linspace(0, len(g) - 1, n), np.arange(len(g)), g)
    P[:, 2] += 3.0 * smooth_noise(len(P), 30)
    B = norm(B + np.stack([np.zeros(len(P)), np.zeros(len(P)), 0.12 * smooth_noise(len(P), 28)], 1))
    T = norm(np.gradient(P, axis=0))
    # make B perpendicular to T
    B = norm(B - (B * T).sum(1, keepdims=True) * T)
    N = norm(np.cross(T, B))
    s = np.linspace(-1, 1, ns)
    V = P[:, None, :] + (s[None, :, None] * (w[:, None, None] / 2)) * B[:, None, :]
    quads = []
    seglen = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
    for i in range(len(P) - 1):
        n = N[i]
        nv = n @ VIEW
        if nv < 0:
            n = -n; nv = -nv
        diff = max(0.0, float(n @ LIGHT)) * 0.55 + 0.45 * abs(float(n @ LIGHT))
        spec = max(0.0, float(n @ HALF)) ** 14
        fres = (1 - nv) ** 1.4
        stripes = 1 + weave * math.sin(seglen[i] * 0.9)
        pl = pleat[i] if hasattr(pleat, "__len__") else pleat
        for j in range(ns - 1):
            hem = 1.0 if (j == 0 or j == ns - 2) else 0.0
            sj = (s[j] + s[j + 1]) / 2
            nj = n + B[i] * (pl * math.cos(sj * math.pi * 3.0))
            nj = nj / np.linalg.norm(nj)
            diff = max(0.0, float(nj @ LIGHT)) * 0.55 + 0.45 * abs(float(nj @ LIGHT))
            spec = max(0.0, float(nj @ HALF)) ** 14
            col = BASE * (0.80 + 0.30 * diff) * stripes + 255 * (0.65 * spec) + 20 * fres
            col = col * (1 + 0.05 * hem)
            a = 0.30 + 0.50 * fres + 0.30 * spec + 0.30 * hem
            pts = np.array([V[i, j, :2], V[i, j + 1, :2], V[i + 1, j + 1, :2], V[i + 1, j, :2]], np.float32)
            z = float((V[i, j, 2] + V[i + 1, j + 1, 2]) / 2)
            quads.append((z, pts, np.clip(col, 0, 255), min(0.93, a)))
    return quads

def _peel(quads, W, H, ss, gap=6.0):
    """two-layer depth peeling inside one ribbon piece: neighbouring quads never double-blend,
    but a fold lying over another part of the same ribbon is still seen through."""
    Wp, Hp = W * ss, H * ss
    z1 = np.full((Hp, Wp), -1e9, np.float32); z2 = np.full((Hp, Wp), -1e9, np.float32)
    c1 = np.zeros((Hp, Wp, 3), np.float32); c2 = np.zeros((Hp, Wp, 3), np.float32)
    a1 = np.zeros((Hp, Wp), np.float32); a2 = np.zeros((Hp, Wp), np.float32)
    for z, pts, col, a in quads:
        p = pts * ss
        x0, y0 = np.floor(p.min(0)).astype(int) - 1; x1, y1 = np.ceil(p.max(0)).astype(int) + 2
        x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(Wp, x1), min(Hp, y1)
        if x0 >= x1 or y0 >= y1:
            continue
        m = np.zeros((y1 - y0, x1 - x0), np.uint8)
        cv2.fillConvexPoly(m, np.round(p - [x0, y0]).astype(np.int32), 1)
        mm = m.astype(bool)
        if not mm.any():
            continue
        Z1 = z1[y0:y1, x0:x1]; Z2 = z2[y0:y1, x0:x1]
        C1 = c1[y0:y1, x0:x1]; C2 = c2[y0:y1, x0:x1]; A1 = a1[y0:y1, x0:x1]; A2 = a2[y0:y1, x0:x1]
        front = mm & (z > Z1 + gap)                 # new nearest layer: old nearest becomes 2nd
        C2[front] = C1[front]; A2[front] = A1[front]; Z2[front] = Z1[front]
        same = mm & (np.abs(z - Z1) <= gap)         # same layer (neighbour quad): just overwrite
        top = front | same
        C1[top] = col; A1[top] = a; Z1[top] = np.maximum(Z1[top], z) if False else z
        behind = mm & (z < Z1 - gap) & (z > Z2 + gap)
        C2[behind] = col; A2[behind] = a; Z2[behind] = z
    # composite 2nd layer, then nearest layer over it
    rgb = c2 * a2[..., None]
    A = a2.copy()
    rgb = rgb * (1 - a1[..., None]) + c1 * a1[..., None]
    A = A + a1 * (1 - A)
    zmean = float(np.mean([q[0] for q in quads])) if quads else 0
    return rgb, A, zmean

def rasterize(groups, W, H, ss=2):
    """groups: list of quad lists (one per ribbon piece); pieces are blended back to front."""
    if groups and isinstance(groups[0], tuple):
        groups = [groups]
    layers = [_peel(g, W, H, ss) for g in groups if g]
    layers.sort(key=lambda L: L[2])
    rgbP = np.zeros((H * ss, W * ss, 3), np.float32); A = np.zeros((H * ss, W * ss), np.float32)
    for lrgb, la, _ in layers:                       # lrgb is premultiplied
        rgbP = rgbP * (1 - la[..., None]) + lrgb
        A = A + la * (1 - A)
    rgbP = cv2.resize(rgbP, (W, H), interpolation=cv2.INTER_AREA)
    A = cv2.resize(A, (W, H), interpolation=cv2.INTER_AREA)
    rgb = rgbP / np.maximum(A[..., None], 1e-4)
    rgb = cv2.GaussianBlur(rgb, (0, 0), 1.1)
    A = cv2.GaussianBlur(A, (0, 0), 0.5)
    return np.clip(rgb, 0, 255), np.clip(A, 0, 1)

# ------------------------------------------------------------------ bow geometry
def rot_z(v, cx, cy, ang):
    c, s = math.cos(ang), math.sin(ang)
    x, y = v[..., 0] - cx, v[..., 1] - cy
    out = v.copy(); out[..., 0] = cx + c * x - s * y; out[..., 1] = cy + s * x + c * y
    return out

def _sm(x):
    x = np.clip(x, 0.0, 1.0); return x * x * (3 - 2 * x)

def bow_quads(u=0.0, cx=450, cy=330):
    """u = 0 tied bow ... 1 untied: tails pulled out sideways into a straight band, loops slid out, knot open.
    Returns one quad list per piece."""
    q = []
    lk = (1 - u) ** 1.35                      # loop size
    # ---- loops (broad, puffy, gathered at the knot)
    if lk > 0.04:
        for sgn in (-1, 1):
            n = 200
            phi = np.linspace(0.02, 2 * math.pi - 0.02, n)
            L = 12 + 330 * lk
            Rz = 14 + 72 * lk
            lift = 105 * lk
            x = cx + sgn * (16 + (L / 2) * (1 - np.cos(phi)))
            z = 16 + Rz * np.sin(phi)
            y = cy - lift * ((1 - np.cos(phi)) / 2) ** 1.3 + 40 * np.sin(phi) * lk - 34 * lk * np.sin(phi / 2) ** 2
            P = np.stack([x, y, z], 1)
            P = rot_z(P, cx, cy, -sgn * math.radians(8 * lk))
            wmax = 60 + 190 * lk
            wv = 48 + (wmax - 48) * ((1 - np.cos(phi)) / 2) ** 0.55 * (1 - 0.2 * np.exp(-((phi - math.pi) / 0.35) ** 2))
            alpha = (0.45 * np.sin(phi) + 0.5 * np.sin(phi / 2) ** 6) * lk
            Bv = np.stack([np.zeros(n), np.cos(alpha), np.sin(alpha)], 1)
            pleat = 0.55 * np.exp(-((phi - 0) / 0.9) ** 2) + 0.55 * np.exp(-((phi - 2 * math.pi) / 0.9) ** 2) + 0.18
            q.append(strip(P, wv, Bv, weave=0.05, pleat=pleat))
    # ---- tails: hang down at first, then swing out sideways and straighten as they are pulled
    sw = _sm(u * 1.15)
    for sgn in (-1, 1):
        n = 150
        t_ = np.linspace(0, 1, n)
        ang = math.radians(62 * (1 - sw) + 2 * sw)               # below horizontal
        Lt = 400 + 160 * sw
        sag = 40 * (1 - sw)
        x = cx + sgn * (18 + Lt * t_ * math.cos(ang))
        y = cy + 14 * (1 - sw) + Lt * t_ * math.sin(ang) + sag * np.sin(math.pi * t_)
        z = 6 - 14 * t_ * (1 - sw) + 8 * np.sin(t_ * 5) * (1 - sw) - 30 * sw
        P = np.stack([x, y, z], 1)
        d = np.gradient(P[:, :2], axis=0); d /= np.linalg.norm(d, axis=1, keepdims=True)
        perp = np.stack([-d[:, 1], d[:, 0], np.zeros(n)], 1) * sgn
        tw = (1.0 * np.sin(math.pi * t_ * 1.2 + (0.6 if sgn > 0 else 1.4))) * (1 - sw)
        Bv = norm(perp * np.cos(tw)[:, None] + np.array([0, 0, 1.0]) * np.sin(tw)[:, None])
        wv = (150 * (1 - sw) + 180 * sw) * (0.9 + 0.1 * np.cos(t_ * 7)) * (0.55 + 0.45 * _sm(t_ * 4))
        q.append(strip(P, wv, Bv, weave=0.05, pleat=0.35 * (1 - t_) + 0.12))
    # ---- knot: loosens, then opens
    kw = (56 + 10 * u) * (1 - _sm((u - 0.62) / 0.33))
    if kw > 3:
        n = 70
        phi = np.linspace(-math.pi * 0.95, math.pi * 0.95, n)
        r = 24 + 12 * u
        P = np.stack([cx + 5 * np.sin(phi * 2), cy + r * np.sin(phi), 34 + r * np.cos(phi)], 1)
        Bv = np.stack([np.ones(n), np.zeros(n), 0.3 * np.sin(phi * 3)], 1)
        q.append(strip(P, np.full(n, kw), Bv, weave=0.08, pleat=0.6))
    return q

def band_quads(W=900, cy=110, gather=0.32):
    n = 320
    x = np.linspace(-30, W + 30, n)
    y = cy + 5 * np.sin(x / 85)
    z = -40 + 6 * np.sin(x / 60)
    P = np.stack([x, y, z], 1)
    wv = 185 * (1 - gather * np.exp(-((x - W / 2) / 110) ** 2))
    a = 0.22 * np.sin(x / 47) + 0.6 * np.exp(-((x - W / 2) / 70) ** 2) * np.sin(x / 9)
    Bv = np.stack([np.zeros(n), np.cos(a), np.sin(a)], 1)
    return strip(P, wv, Bv, weave=0.05, pleat=0.18 + 0.5 * np.exp(-((x - W / 2) / 110) ** 2))
