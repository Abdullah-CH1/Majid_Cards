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
BASE = np.array([198, 168, 181], np.float32)        # dusty rose-grey organza (RGB), like the ribbon in the video

def norm(v):
    return v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-9)

def _smooth_rand(rr, n, k):
    g = rr.standard_normal(max(4, n // k + 3)); return np.interp(np.linspace(0, len(g) - 1, n), np.arange(len(g)), g)

def sheet(P, w, B, ns=24, disp=None, seed=0, opa=0.0, micro=1.0, tcut=None, lum=1.0):
    """quads for one piece of sheer satin-organza ribbon.
    P: (N,3) centre path, w: (N,) width, B: (N,3) cross direction, disp: (N,ns) offset along the normal (pleats, bulges).
    tcut: (ns,) fraction of the length kept per cross position (slanted cut end).  -> list of (z, pts2d(4,2), rgb, alpha)"""
    P = np.asarray(P, np.float32); w = np.asarray(w, np.float32); B = norm(np.asarray(B, np.float32))
    N = len(P); rr = np.random.default_rng(seed)
    T = norm(np.gradient(P, axis=0))
    B = norm(B - (B * T).sum(1, keepdims=True) * T)
    Nn = norm(np.cross(T, B))
    s = np.linspace(-1, 1, ns)
    V = P[:, None, :] + (s[None, :, None] * (w[:, None, None] / 2)) * B[:, None, :]
    d = np.zeros((N, ns), np.float32) if disp is None else np.asarray(disp, np.float32).copy()
    # fine lengthwise folds (the glossy streaks of the fabric) + a slow billow along the length
    g = rr.standard_normal((max(3, N // 45 + 2), max(4, ns // 3 + 2))).astype(np.float32)
    m = cv2.resize(g, (ns, N), interpolation=cv2.INTER_CUBIC)
    d += micro * 0.55 * m * np.clip(w / 150.0, 0.15, 1.2)[:, None]
    d += micro * 2.0 * _smooth_rand(rr, N, 26)[:, None] * (0.6 + 0.4 * np.sin(s * 2.1 + 1.0))[None, :]
    V = V + d[..., None] * Nn[:, None, :]
    if tcut is not None:                                   # slide each column back along the ribbon
        ti = np.linspace(0, 1, N)
        for j in range(ns):
            tj = np.minimum(ti, tcut[j])
            for c in range(3):
                V[:, j, c] = np.interp(tj, ti, V[:, j, c])
    dT = np.gradient(V, axis=0); dS = np.gradient(V, axis=1)
    n = norm(np.cross(dT, dS))
    n = np.where(n[..., 2:3] < 0, -n, n)
    nv = n[..., 2]
    nl = n @ LIGHT
    diff = np.clip(nl, 0, 1) * 0.75 + 0.25 * np.abs(nl)
    nh = np.clip(n @ HALF, 0, 1)
    spec = nh ** 24; sheen = nh ** 6
    fres = (1 - nv) ** 1.5
    col = BASE[None, None, :] * ((0.60 + 0.44 * diff) * lum)[..., None] + np.array([252, 247, 255], np.float32) * (0.58 * spec + 0.10 * sheen)[..., None] + 26 * fres[..., None]
    a = 0.27 + opa + 0.50 * fres + 0.42 * spec + 0.08 * sheen
    a[:, 0] += 0.30; a[:, -1] += 0.30                      # hems: a denser woven edge
    col[:, 0] = col[:, 0] * 0.84 + 8; col[:, -1] = col[:, -1] * 0.84 + 8
    a = np.clip(a, 0, 0.95)
    cq = np.clip((col[:-1, :-1] + col[1:, :-1] + col[:-1, 1:] + col[1:, 1:]) / 4, 0, 255)
    aq = (a[:-1, :-1] + a[1:, :-1] + a[:-1, 1:] + a[1:, 1:]) / 4
    zq = (V[:-1, :-1, 2] + V[1:, 1:, 2]) / 2
    quads = []
    for i in range(N - 1):
        for j in range(ns - 1):
            pts = np.array([V[i, j, :2], V[i, j + 1, :2], V[i + 1, j + 1, :2], V[i + 1, j, :2]], np.float32)
            quads.append((float(zq[i, j]), pts, cq[i, j], float(aq[i, j])))
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
    rgb = cv2.GaussianBlur(rgb, (0, 0), 0.7)
    A = cv2.GaussianBlur(A, (0, 0), 0.5)
    return np.clip(rgb, 0, 255), np.clip(A, 0, 1)

# ------------------------------------------------------------------ bow geometry
BW, BH, CX, CY = 900, 720, 450, 235            # canvas of every bow frame and of the band; the knot sits at (CX, CY)
BAND_W = 236; BAND_HALF = 130

def _sm(x):
    x = np.clip(x, 0.0, 1.0); return x * x * (3 - 2 * x)

def _key(f, *kv):
    return float(np.interp(f, [k for k, _ in kv], [v for _, v in kv]))

def loop_piece(sgn, k, tilt, seed):
    """one bow loop. k: size 1..0, tilt: degrees above the horizontal"""
    n = 150; ns = 26
    phi = np.linspace(0.0, 2 * math.pi, n)
    L = 14 + 312 * k; Rz = 6 + 40 * k
    a = 20 + (L / 2) * (1 - np.cos(phi))                                  # distance out from the knot
    z = 14 + Rz * np.sin(phi) + 10 * k * np.sin(phi / 2) ** 2
    lat = (28 - 74 * phi / (2 * math.pi)) * np.sin(phi / 2) ** 0.7 * k     # front layer sits lower, the back layer peeps out above
    th = math.radians(tilt)
    ax = np.array([sgn * math.cos(th), -math.sin(th)]); pp = np.array([sgn * math.sin(th), math.cos(th)])   # axis / lateral (down)
    P = np.stack([CX + ax[0] * a + pp[0] * lat, CY + ax[1] * a + pp[1] * lat, z], 1)
    wmax = 56 + 204 * k ** 0.75
    wv = 44 + (wmax - 44) * np.sin(phi / 2) ** 0.5 * (1 - 0.34 * np.exp(-((phi - math.pi) / 0.55) ** 2))
    al = 0.30 * np.sin(phi) * k + 0.04 * k                                  # the face leans back a little: catches the light
    Bv = np.stack([np.full(n, pp[0]) * np.cos(al), np.full(n, pp[1]) * np.cos(al), np.sin(al)], 1)
    s = np.linspace(-1, 1, ns)
    amp = 9.0 * np.exp(-(a - 20) / 70.0) + 0.3
    disp = amp[:, None] * np.cos(s[None, :] * math.pi * 3.2 + 0.7 * seed) + 15 * k * (1 - s[None, :] ** 2) * (np.sin(phi / 2) ** 2)[:, None]
    return sheet(P, wv, Bv, ns=ns, disp=disp, seed=seed)

def tail_piece(sgn, ln, ang, wf, seed):
    """a tail hanging from the knot. ln: length 1..0 (it slides up into the knot), ang: degrees below horizontal"""
    n = 120; ns = 24
    Lt = 600 * ln
    t_ = np.linspace(0, 1, n); d = Lt * t_
    a0 = math.radians(ang)
    bend = 0.20 * np.sin(math.pi * t_) * ln                                 # gentle curve
    x = CX + sgn * 10 + sgn * np.cumsum(np.cos(a0 + bend) * np.gradient(d))
    y = CY + 12 + np.cumsum(np.sin(a0 + bend) * np.gradient(d))
    z = 4 - 16 * _sm(d / 200) + 5 * np.sin(d / 55 + seed)
    P = np.stack([x, y, z], 1)
    g = np.gradient(P[:, :2], axis=0); g /= np.maximum(np.linalg.norm(g, axis=1, keepdims=True), 1e-6)
    perp = np.stack([-g[:, 1], g[:, 0], np.zeros(n)], 1) * sgn
    tw = 0.42 * np.sin(d / 130 + (0.4 if sgn > 0 else 1.9)) * min(1.0, ln * 1.5) + 0.30
    Bv = perp * np.cos(tw)[:, None] + np.array([0, 0, 1.0]) * np.sin(tw)[:, None]
    wv = (42 + (212 * wf - 42) * _sm(d / 190) ** 0.8)
    s = np.linspace(-1, 1, ns)
    amp = 8.0 * np.exp(-d / 90.0) + 0.4
    disp = amp[:, None] * np.cos(s[None, :] * math.pi * 3.0 + seed) + 5 * np.sin(d / 90 + 2 * seed)[:, None] * s[None, :]
    cut = 1 - (0.5 + 0.5 * s * sgn) * min(0.99, 110 / max(Lt, 1.0))         # slanted cut end
    return sheet(P, wv, Bv, ns=ns, disp=disp, seed=seed, tcut=cut, micro=1.7, opa=0.05)

def knot_pieces(ks):
    """the tight little knot: three plump wraps side by side, slightly slanted"""
    out = []
    n = 26; ns = 9
    phi = np.linspace(-math.pi * 0.62, math.pi * 0.62, n)
    r = 43 * ks
    for k, off in enumerate((-23, 0, 23)):
        P = np.stack([CX + off * ks + 15 * ks * np.sin(phi), CY + 2 + r * np.sin(phi), 34 * ks + 8 + r * 0.55 * np.cos(phi)], 1)
        Bv = np.stack([np.ones(n), np.zeros(n), np.zeros(n)], 1)
        s = np.linspace(-1, 1, ns)
        disp = (9 * ks * (1 - s ** 2))[None, :] * np.ones((n, 1))
        out.append(sheet(P, np.full(n, 27.0 * ks), Bv, ns=ns, disp=disp, seed=90 + k, opa=0.5, micro=0.5, lum=0.97))
    return out

def band_piece(sgn, g, gap, seed):
    """one half of the band. g: 0 lying relaxed ... 1 drawn tight (a fan of pleats from the knot); gap: tip distance from the centre"""
    n = 150; ns = 30
    d = np.linspace(0, 500, n)                                              # distance from the knot/tip
    x = CX + sgn * (gap + d)
    y = CY + 3 * np.sin(d / 120 + seed) * (1 - g) + np.zeros(n)
    z = -34 + 4 * np.sin(d / 70 + seed)
    P = np.stack([x, y, z], 1)
    wk = 40 * (1 - 0.8 * _sm(gap / 12))
    w_rest = wk + (BAND_W - wk) * _sm(d / 170) ** 0.8
    w_taut = wk + (BAND_W - wk) * (d / 450) ** 0.9
    wv = np.minimum(w_rest * (1 - g) + w_taut * g, BAND_W)
    tw = 0.10 * np.sin(d / 90 + seed)
    Bv = np.stack([np.zeros(n), np.cos(tw), np.sin(tw)], 1)
    s = np.linspace(-1, 1, ns)
    amp = (9 - 3 * g) * np.exp(-d / (110 + 90 * g)) + 0.15 + 0.30 * g
    disp = amp[:, None] * np.cos(s[None, :] * math.pi * 4.5 + seed + 1.6 * np.sin(s[None, :] * 3 + seed))
    return sheet(P, wv, Bv, ns=ns, disp=disp, seed=seed, opa=0.07, lum=0.97, micro=0.5)

def bow_state(u):
    """what every piece is doing at untie progress u (0 tied ... 1 the knot has let go); keyed on the reference video, frames 150-198"""
    f = 150 + 48 * u
    return dict(
        kL=_key(f, (150, 1), (158, .86), (162, .72), (166, .46), (170, .16), (172, 0)),
        kR=_key(f, (150, 1), (158, .88), (162, .78), (166, .62), (170, .44), (174, .12), (176, 0)),
        tL=_key(f, (150, 14), (166, 6)), tR=_key(f, (150, 14), (162, 17), (166, 34), (170, 56), (174, 70)),
        lnR=_key(f, (160, 1), (166, .62), (170, .22), (173, 0)), angR=_key(f, (160, 51), (170, 26)),
        lnL=_key(f, (174, 1), (178, .86), (182, .66), (186, .5), (190, .26), (194, .07), (196, 0)),
        angL=_key(f, (150, 51), (170, 55), (178, 60), (186, 53), (192, 42)), wfL=_key(f, (174, 1), (182, .74), (190, .6)),
        ks=_key(f, (190, 1), (194, .6), (197, 0)),
        g=_key(f, (150, 0), (160, .2), (170, .7), (177, 1)),
        gap=_key(f, (193, 0), (198, 20)))

def bow_quads(u=0.0, band=True, bow=True):
    """every piece of the bow (+ band) at untie progress u, one quad list per piece"""
    S = bow_state(u); q = []
    if band:
        q.append(band_piece(-1, S["g"], S["gap"], 3)); q.append(band_piece(1, S["g"], S["gap"], 8))
    if bow:
        if S["lnL"] > 0.02: q.append(tail_piece(-1, S["lnL"], S["angL"], S["wfL"], 1))
        if S["lnR"] > 0.02: q.append(tail_piece(1, S["lnR"], S["angR"], 1.0, 2))
        if S["kL"] > 0.03: q.append(loop_piece(-1, S["kL"], S["tL"], 5))
        if S["kR"] > 0.03: q.append(loop_piece(1, S["kR"], S["tR"], 6))
        if S["ks"] > 0.05: q += knot_pieces(S["ks"])
    return q

def render(u, band=True, bow=True):
    """RGBA frame (rgb float 0..255, alpha 0..1) with a soft contact shadow baked in"""
    rgb, a = rasterize(bow_quads(u, band, bow), BW, BH)
    r = np.random.default_rng(5)                            # fine crinkle shimmer of the weave
    gr = cv2.GaussianBlur(r.standard_normal((BH, BW)).astype(np.float32), (0, 0), 0.9)
    gr = gr / gr.std()
    lum = rgb.mean(2, keepdims=True) / 255.0
    rgb = np.clip(rgb * (1 + 0.024 * gr[..., None]) + 16 * np.clip(gr[..., None] - 1.2, 0, 2) * lum, 0, 255)
    sh = cv2.GaussianBlur(a, (0, 0), 7)
    sh = np.roll(np.roll(sh, 7, 0), 3, 1) * 0.30
    sh[:7] = 0; sh[:, :3] = 0                               # (no wrap-around from the roll)
    A = a + sh * (1 - a)
    out = (rgb * a[..., None] + np.array([72, 48, 64], np.float32) * (sh * (1 - a))[..., None]) / np.maximum(A[..., None], 1e-4)
    return out, A
