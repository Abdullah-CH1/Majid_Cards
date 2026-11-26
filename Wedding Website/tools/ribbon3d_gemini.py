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
BASE = np.array([206, 184, 197], np.float32)        # dusty rose-grey organza (RGB), like the ribbon in the video

GLARE = 0.72

def norm(v):
    return v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-9)

def _smooth_rand(rr, n, k):
    g = rr.standard_normal(max(4, n // k + 3)); return np.interp(np.linspace(0, len(g) - 1, n), np.arange(len(g)), g)

def _pleats(s, seed, nf=3.0):
    """irregular gathered pleats across the ribbon (-1..1): a few folds of uneven width and depth"""
    r = np.random.default_rng(1000 + int(seed))
    ph = r.uniform(0, 6.28, 3); f = nf * r.uniform(0.75, 1.3, 3)
    wob = 0.5 * np.sin(s * r.uniform(1.5, 3.0) + ph[2])
    p = np.cos((s + 0.18 * wob) * math.pi * f[0] + ph[0]) + 0.55 * np.cos(s * math.pi * f[1] * 1.7 + ph[1]) * (0.6 + 0.4 * wob)
    return (p / 1.3).astype(np.float32)

def _svals(ns, h=0.05):
    """cross positions -1..1: a narrow hem cell at each edge, a narrow stitch cell next to it, even cells between"""
    return np.concatenate([[-1.0, -1 + h, -1 + 1.9 * h], np.linspace(-1 + 1.9 * h, 1 - 1.9 * h, ns - 4)[1:-1], [1 - 1.9 * h, 1 - h, 1.0]]).astype(np.float32)

def sheet(P, w, B, ns=44, disp=None, seed=0, opa=0.0, micro=1.0, tcut=None, lum=1.0, gloss=1.0, hem=1.0, fan=None, run=1.0, rnd=0.0, crk=1.0, off=None, shine=0.0, look=False, rope=0.0):
    if look:
        return _sheet_gemini(P, w, B, ns, disp, seed, opa, micro, tcut, lum, gloss, hem, fan, run, rnd, crk, off, shine, rope)
    return _sheet_orig(P, w, B, ns, disp, seed, opa, micro, tcut, lum, gloss, hem, fan, run, rnd, crk, off, shine)

# ---- the client's Gemini bow: silvery-white crushed satin, nearly opaque, crinkled metallic glints, bright frayed edge
G_BASE = 0.90 * np.array([216, 212, 217], np.float32) + 0.10 * BASE   # silver-white, warmed ~10% toward the band's rose-grey
G_HI = np.array([255, 255, 255], np.float32)
G_CRK = 1.0                                          # extra crushed-crinkle strength (x the piece's own crk)
KNOT_LUM = 1.42
G_GRAIN = 0.018; G_SPARK = 7.0; G_KNEE = 232.0; G_TONE = 0.10; G_BLUR = 0.55   # bow post-processing

def _sheet_gemini(P, w, B, ns, disp, seed, opa, micro, tcut, lum, gloss, hem, fan, run, rnd, crk, off, shine, rope):
    P = np.asarray(P, np.float32); w = np.asarray(w, np.float32); B = norm(np.asarray(B, np.float32))
    N = len(P); rr = np.random.default_rng(seed)
    T = norm(np.gradient(P, axis=0))
    B = norm(B - (B * T).sum(1, keepdims=True) * T)
    Nn = norm(np.cross(T, B))
    s = _svals(ns)
    V = P[:, None, :] + (s[None, :, None] * (w[:, None, None] / 2)) * B[:, None, :]
    d = np.zeros((N, ns), np.float32) if disp is None else np.asarray(disp, np.float32).copy()
    # (same random draws as the original, in the same order, so the cloth keeps its folds)
    g = rr.standard_normal((max(3, N // 45 + 2), 10)).astype(np.float32)
    m = cv2.resize(g, (ns, N), interpolation=cv2.INTER_CUBIC)
    d += micro * 0.9 * m * np.clip(w / 150.0, 0.15, 1.2)[:, None]
    d += micro * 2.0 * _smooth_rand(rr, N, 26)[:, None] * (0.6 + 0.4 * np.sin(s * 2.1 + 1.0))[None, :]
    wk = np.clip(w / 170.0, 0.12, 1.0)[:, None]
    if crk:
        c1 = cv2.resize(rr.standard_normal((max(4, N // 15), max(4, ns // 4))).astype(np.float32), (ns, N), interpolation=cv2.INTER_CUBIC)
        c2 = cv2.resize(rr.standard_normal((max(3, N // 24), 5)).astype(np.float32), (ns, N), interpolation=cv2.INTER_CUBIC)
        c3 = cv2.resize(rr.standard_normal((max(4, N // 4), max(4, ns // 2))).astype(np.float32), (ns, N), interpolation=cv2.INTER_CUBIC)
        d += crk * (1.1 * c1 + 2.6 * c2 + 0.25 * c3) * wk
    # crushed satin: faceted dents (linear interpolation -> crisp creases between little flat planes)
    rc = np.random.default_rng(7000 + int(seed))
    cc = max(crk, 0.35) * G_CRK
    # long soft ridges running ALONG the ribbon (~8x longer than across) + only a faint fine crinkle on top
    f1 = cv2.resize(rc.standard_normal((max(3, N // 40), max(6, ns // 3))).astype(np.float32), (ns, N), interpolation=cv2.INTER_CUBIC)
    f2 = cv2.resize(rc.standard_normal((max(4, N // 5), max(4, ns // 2))).astype(np.float32), (ns, N), interpolation=cv2.INTER_CUBIC)
    d += cc * (2.6 * f1 + 0.30 * f2) * wk
    V = V + d[..., None] * Nn[:, None, :]
    if off is not None:
        V = V + np.asarray(off, np.float32)
    lum = np.asarray(lum, np.float32)
    if lum.ndim == 1:
        lum = lum[:, None]
    if tcut is not None:
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
    diff = np.clip(nl, 0, 1) * 0.8 + 0.2 * np.abs(nl)
    alng = lambda x: cv2.GaussianBlur(np.ascontiguousarray(x, np.float32), (0, 0), sigmaX=0.6, sigmaY=3.5)   # smear along the length only
    nh = np.clip(alng(n @ HALF), 0, 1)
    spec = nh ** 40; sheen = nh ** 6
    glz = _sm((nh ** 10 - 0.22) / 0.55)                      # liquid satin glare on the lengthwise folds that face the light
    shade = _sm((0.55 - nl) / 0.70)
    fres = (1 - nv) ** 1.5
    kt = max(4, int(N / (30 * run)) + 2)
    g1 = cv2.resize(rr.standard_normal((kt, ns)).astype(np.float32), (ns, N), interpolation=cv2.INTER_CUBIC)
    g1 = 0.7 * g1 + 0.15 * (np.roll(g1, 1, 1) + np.roll(g1, -1, 1))
    g2 = cv2.resize(rr.standard_normal((max(3, N // 60 + 2), 7)).astype(np.float32), (ns, N), interpolation=cv2.INTER_CUBIC)
    fn = np.zeros(N, np.float32) if fan is None else np.asarray(fan, np.float32)
    thin = np.clip(g1 - (0.80 - 0.70 * fn[:, None]), 0, None); thin = thin / (thin + 0.22)
    broad = np.clip(g2 - 0.05, 0, None); broad = broad / (broad + 0.6)
    env = 0.35 + 0.65 * sheen
    hl = np.clip(gloss * (0.42 * thin * env + 0.08 * broad * env) + 0.5 * spec + 0.16 * sheen + 0.80 * glz, 0, 1)
    if shine:
        g3 = cv2.resize(rr.standard_normal((max(3, N // 70 + 2), 6)).astype(np.float32), (ns, N), interpolation=cv2.INTER_CUBIC)
        nhh = alng(n @ HALF)                                # the big bright bands come from the folds themselves
        g3 = np.tanh((nhh - float(np.median(nhh))) / max(float(nhh.std()), 0.03)) + 0.12 * g3 + 0.10 * g1
        g3 = alng(g3); g3 = g3 - float(np.percentile(g3, 72))
        band = _sm(g3 / 0.55 + 0.35)
        hl = np.clip(np.maximum(hl, 0.62 * shine * band * (0.45 + 0.55 * _sm((nl - 0.05) / 0.6))), 0, 1)
        shade = np.clip(shade + 0.35 * shine * _sm((-g3 - 0.6) / 1.2), 0, 1.6)
    hl = _sm(hl * 1.15) * 0.68 + 0.32 * hl                          # soft transitions, no hard-edged patches
    dark = np.clip(-g1 - 0.9 + 0.7 * fn[:, None], 0, 1) * 0.7
    if rope:                                               # a twisted cord: diagonal wraps catching the light one after the other
        ii = np.arange(N, dtype=np.float32)[:, None]
        tw = np.sin(ii * 1.25 + s[None, :] * 3.4 + seed)
        hl = np.clip(hl * (0.55 + 0.45 * _sm(tw + 0.5)) + 0.45 * rope * _sm((tw - 0.35) / 0.5), 0, 1)
        dark = np.clip(dark + 0.85 * rope * _sm((-tw - 0.1) / 0.6), 0, 1)
    body = G_BASE[None, None, :] * ((0.64 + 0.42 * diff - 0.22 * dark - 0.28 * shade) * lum)[..., None] + 10 * fres[..., None]
    if rnd:
        body = body * (1 - rnd * np.abs(s) ** 2.5)[None, :, None]; hl = hl * (1 - 0.7 * np.abs(s) ** 2)[None, :]
    col = body * (1 - hl[..., None]) + G_HI * hl[..., None]
    a = 0.80 + 0.6 * opa + 0.14 * fres + 0.15 * hl + 0.06 * dark
    a = np.clip(a, 0, 0.975)
    cq = (col[:-1, :-1] + col[1:, :-1] + col[:-1, 1:] + col[1:, 1:]) / 4
    aq = (a[:-1, :-1] + a[1:, :-1] + a[:-1, 1:] + a[1:, 1:]) / 4
    if hem > 0:                                             # the frayed edge: a fine, broken, glittering silver thread
        lit = (0.86 + 0.20 * (diff[:-1] + diff[1:]) / 2) * (lum if lum.ndim < 2 else lum[:-1])
        for j, jj in ((0, 1), (ns - 2, ns - 3)):
            fr = rc.random(N - 1).astype(np.float32)
            spark = (0.70 + 0.30 * fr + 0.35 * (fr > 0.82)) * lit[:, min(j, ns - 2)]
            cq[:, j] = np.array([250, 249, 254], np.float32) * np.clip(spark, 0, 1.15)[:, None]
            aq[:, j] = np.clip(0.55 + 0.45 * rc.random(N - 1), 0, 1) * hem
            cq[:, jj] = cq[:, jj] * 0.92 + 18
    cq = np.clip(cq, 0, 255)
    zq = (V[:-1, :-1, 2] + V[1:, 1:, 2]) / 2
    quads = []
    for i in range(N - 1):
        for j in range(ns - 1):
            pts = np.array([V[i, j, :2], V[i, j + 1, :2], V[i + 1, j + 1, :2], V[i + 1, j, :2]], np.float32)
            quads.append((float(zq[i, j]), pts, cq[i, j], float(aq[i, j])))
    return quads

def _sheet_orig(P, w, B, ns=44, disp=None, seed=0, opa=0.0, micro=1.0, tcut=None, lum=1.0, gloss=1.0, hem=1.0, fan=None, run=1.0, rnd=0.0, crk=1.0, off=None, shine=0.0):
    """quads for one piece of sheer organza ribbon.
    P: (N,3) centre path, w: (N,) width, B: (N,3) cross direction, disp: (N,ns) offset along the normal (pleats, bulges).
    tcut: (ns,) fraction of the length kept per cross position (slanted cut end).
    fan: (N,) 0..1 how tightly the ribbon is gathered there (crisper, denser pleat lines).  -> list of (z, pts2d(4,2), rgb, alpha)
    The cloth itself is a thin veil; what you see of it are the glossy streaks running along its length, the woven hems
    and the places where it turns away from the eye or lies double."""
    P = np.asarray(P, np.float32); w = np.asarray(w, np.float32); B = norm(np.asarray(B, np.float32))
    N = len(P); rr = np.random.default_rng(seed)
    T = norm(np.gradient(P, axis=0))
    B = norm(B - (B * T).sum(1, keepdims=True) * T)
    Nn = norm(np.cross(T, B))
    s = _svals(ns)
    V = P[:, None, :] + (s[None, :, None] * (w[:, None, None] / 2)) * B[:, None, :]
    d = np.zeros((N, ns), np.float32) if disp is None else np.asarray(disp, np.float32).copy()
    # soft lengthwise folds + a slow billow along the length
    g = rr.standard_normal((max(3, N // 45 + 2), 10)).astype(np.float32)
    m = cv2.resize(g, (ns, N), interpolation=cv2.INTER_CUBIC)
    d += micro * 0.9 * m * np.clip(w / 150.0, 0.15, 1.2)[:, None]
    d += micro * 2.0 * _smooth_rand(rr, N, 26)[:, None] * (0.6 + 0.4 * np.sin(s * 2.1 + 1.0))[None, :]
    if crk:                                                 # crinkled satin: small soft dents, longer along the ribbon than across it
        c1 = cv2.resize(rr.standard_normal((max(4, N // 15), max(4, ns // 4))).astype(np.float32), (ns, N), interpolation=cv2.INTER_CUBIC)
        c2 = cv2.resize(rr.standard_normal((max(3, N // 24), 5)).astype(np.float32), (ns, N), interpolation=cv2.INTER_CUBIC)
        c3 = cv2.resize(rr.standard_normal((max(4, N // 4), max(4, ns // 2))).astype(np.float32), (ns, N), interpolation=cv2.INTER_CUBIC)
        d += crk * (1.1 * c1 + 2.6 * c2 + 0.25 * c3) * np.clip(w / 170.0, 0.12, 1.0)[:, None]
    V = V + d[..., None] * Nn[:, None, :]
    if off is not None:
        V = V + np.asarray(off, np.float32)
    lum = np.asarray(lum, np.float32)
    if lum.ndim == 1:
        lum = lum[:, None]
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
    spec = nh ** 34; sheen = nh ** 5
    glz = _sm((nh ** 15 - 0.36) / 0.38)                      # the wet-looking satin glare where a dent faces the light
    shade = _sm((0.62 - nl) / 0.75)                         # folds turned away from it
    fres = (1 - nv) ** 1.5
    # glossy streaks: thin bright threads running along the ribbon (they converge where it is gathered) + broader satin bands
    kt = max(4, int(N / (30 * run)) + 2)
    g1 = cv2.resize(rr.standard_normal((kt, ns)).astype(np.float32), (ns, N), interpolation=cv2.INTER_CUBIC)
    g1 = 0.7 * g1 + 0.15 * (np.roll(g1, 1, 1) + np.roll(g1, -1, 1))
    g2 = cv2.resize(rr.standard_normal((max(3, N // 60 + 2), 7)).astype(np.float32), (ns, N), interpolation=cv2.INTER_CUBIC)
    fn = np.zeros(N, np.float32) if fan is None else np.asarray(fan, np.float32)
    thin = np.clip(g1 - (0.80 - 0.70 * fn[:, None]), 0, None); thin = thin / (thin + 0.22)
    broad = np.clip(g2 - 0.05, 0, None); broad = broad / (broad + 0.6)
    env = 0.42 + 0.58 * sheen                               # streaks flare where the cloth faces the light
    hl = np.clip(gloss * (0.62 * thin * env + 0.60 * broad * env * (0.55 + 0.45 * thin)) + 0.5 * spec + 0.10 * sheen + GLARE * glz * (0.72 + 0.28 * thin), 0, 1)
    if shine:                                               # broad mirror-like bands of light running along the ribbon, crisp at one side
        g3 = cv2.resize(rr.standard_normal((max(3, N // 70 + 2), 6)).astype(np.float32), (ns, N), interpolation=cv2.INTER_CUBIC)
        nhh = n @ HALF
        g3 = 0.75 * g3 + 0.80 * np.tanh((nhh - float(np.median(nhh))) / max(float(nhh.std()), 0.03)) + 0.15 * g1
        g3 = cv2.GaussianBlur(g3, (0, 0), 1.2); g3 = g3 - float(np.percentile(g3, 80))           # about a fifth of the cloth mirrors the light
        band = _sm(g3 / 0.22 + 0.15) * (0.88 + 0.12 * thin)       # crisp-edged mirror patches
        hl = np.clip(hl * (1 - 0.55 * min(shine, 1.0)) + shine * 1.0 * band * (0.30 + 0.70 * _sm((nl - 0.15) / 0.5)), 0, 1)
        shade = np.clip(shade + 0.8 * shine * _sm((-g3 - 0.9) / 0.9), 0, 1.6)
    dark = np.clip(-g1 - 0.9 + 0.7 * fn[:, None], 0, 1) * 0.7       # shadow lines between pleats
    body = BASE[None, None, :] * ((0.70 + 0.36 * diff - 0.20 * dark - 0.13 * shade) * lum)[..., None] + 14 * fres[..., None]
    if rnd:                                                 # a plump strand: its flanks fall into shadow
        body = body * (1 - rnd * np.abs(s) ** 2.5)[None, :, None]; hl = hl * (1 - 0.8 * np.abs(s) ** 2)[None, :]
    col = body * (1 - hl[..., None]) + np.array([252, 247, 253], np.float32) * hl[..., None]
    a = 0.31 + opa + 0.34 * fres + 0.52 * hl + 0.22 * dark + 0.10 * shade + 0.20 * fn[:, None]
    a = np.clip(a, 0, 0.93)
    cq = (col[:-1, :-1] + col[1:, :-1] + col[:-1, 1:] + col[1:, 1:]) / 4
    aq = (a[:-1, :-1] + a[1:, :-1] + a[:-1, 1:] + a[1:, 1:]) / 4
    hem = hem * HEM_K
    if hem > 0:                                             # woven hems: a bright thread right at the edge, a darker stitch line inside it
        lit = (0.80 + 0.22 * (diff[:-1] + diff[1:]) / 2) * (lum if lum.ndim < 2 else lum[:-1])
        hv = 0.72 + 0.28 * np.clip(1 + 0.8 * _smooth_rand(rr, N - 1, 14), 0, 2) / 2          # the hem catches the light unevenly
        for j, jj in ((0, 1), (ns - 2, ns - 3)):
            cq[:, j] = np.array([246, 238, 244], np.float32) * lit[:, min(j, ns - 2), None]
            aq[:, j] = np.maximum(aq[:, j], (0.34 + 0.36 * lit[:, min(j, ns - 2)].clip(0.8, 1.02) / 1.02 * (0.6 + 0.4 * np.sin(np.arange(N - 1) / 9.0 + j) ** 2)) * hem * hv)
            cq[:, jj] = cq[:, jj] * 0.80; aq[:, jj] = np.minimum(aq[:, jj] + 0.22 * hem, 0.93)
    cq = np.clip(cq, 0, 255)
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
HEM_K = 0.28          # how strong the woven hem line is (1 = bright outline; the reference shows almost none)
BOW_K = 0.84          # size of the bow (loops, tails, knot) about the knot; the band is not scaled
BW, BH, CX, CY = 900, 720, 450, 235            # canvas of every bow frame and of the band; the knot sits at (CX, CY)
BAND_W = 236; BAND_HALF = 130

def _sm(x):
    x = np.clip(x, 0.0, 1.0); return x * x * (3 - 2 * x)

def _key(f, *kv):
    return float(np.interp(f, [k for k, _ in kv], [v for _, v in kv]))

def loop_piece(sgn, k, tilt, seed):
    """one bow loop: a flat band of ribbon that leaves the knot, runs out, folds softly back over itself and returns underneath.
    The band is turned a little towards the eye, so the two layers lie offset: the upper face on top, the open inside and the
    under layer showing along the lower edge and round the fold. k: size 1..0, tilt: degrees above the horizontal"""
    n = 190; ns = 46
    phi = np.linspace(0.0, 2 * math.pi, n)
    rs = np.random.default_rng(40 + seed)
    big, flat, fat = (1.10, 1.0, 1.0) if sgn < 0 else (0.98, 0.85, 0.92)   # no two loops of a hand-tied bow are alike
    L = 14 + 335 * k ** 0.8 * big; Rz = 3 + 84 * k ** 1.5 * flat          # untying: it flattens first, then slides through the knot
    hs = np.sin(phi / 2)
    a = 18 + ((L - 18) / 2) * (1 - np.cos(phi))                            # distance out from the knot
    back = _sm((phi - 0.85 * math.pi) / (0.3 * math.pi))                    # 0 upper layer ... 1 under layer
    sp = np.sin(phi); h = Rz * np.sign(sp) * np.abs(sp) ** 0.62 * (1 - 0.30 * back)     # height of the layer over the loop's mid plane
    h = h + 7 * k * _smooth_rand(rs, n, 36) * hs ** 2
    al0 = 0.86 if sgn < 0 else 0.76                                         # how far the band is turned towards the eye
    th = math.radians(tilt)
    ax = np.array([sgn * math.cos(th), -math.sin(th), 0.0]); pp = np.array([sgn * math.sin(th), math.cos(th), 0.0])   # axis / lateral (down)
    up = -pp * math.sin(al0) + np.array([0, 0, math.cos(al0)])              # thickness direction of the loop
    Bd = pp * math.cos(al0) + np.array([0, 0, math.sin(al0)])
    lat = 44 * k * (a / max(L, 1)) ** 2 + 5 * k * _smooth_rand(rs, n, 40) * hs ** 2    # the loop droops a little under its own weight
    P = np.array([CX, CY, 16.0])[None, :] + a[:, None] * ax[None, :] + h[:, None] * up[None, :] + lat[:, None] * pp[None, :]
    kk = k ** 0.4                                                           # the cloth keeps its width while the loop is pulled out
    Wf = 40 + kk * 195 * fat
    wv = (40 + (Wf - 40) * np.clip((a - 18) / (0.74 * max(L - 18, 1)), 0, 1) ** 0.85) * (1 + 0.04 * k * _smooth_rand(rs, n, 30))
    wv = wv * (1 - 0.10 * back * hs ** 2)
    Bv = np.repeat(Bd[None, :], n, 0)
    s = _svals(ns)
    near = np.exp(-(a - 18) / 55.0)                                        # pinched into the knot
    soft = np.exp(-(a - 18) / 170.0)                                       # the pleats fan out and soften along the loop
    dent = cv2.resize(rs.standard_normal((4, 4)).astype(np.float32), (ns, n), interpolation=cv2.INTER_CUBIC)      # a slightly crushed, hand-tied loop
    disp = (10.0 * near + 6.5 * k * soft + 0.3)[:, None] * _pleats(s, seed, 2.6)[None, :] + 5.0 * k * dent * (hs ** 2)[:, None]         + 7 * k * (hs ** 2)[:, None] * np.sin(s[None, :] * 1.9 + 0.8 * sgn + phi[:, None] * 0.5)
    rnd_ = 40 * k * hs ** 12                                                # the fold is soft and round, not a straight crease
    off = -(rnd_[:, None] * (np.abs(s[None, :]) ** 2.4 - 0.12 * s[None, :]))[..., None] * ax[None, None, :]
    lum = 1 - (0.26 * back + 0.10 * np.exp(-((phi - math.pi) / 0.5) ** 2)) * hs ** 2
    return sheet(P, wv, Bv, ns=ns, disp=disp, seed=seed, fan=(0.3 + 0.7 * k) * np.exp(-(a - 18) / 45.0), gloss=0.6, micro=0.5, opa=-0.10, lum=lum, crk=0.7 * k ** 0.5, off=off, shine=1.0, run=1.8, look=True)

TAIL_L = 585

def tail_piece(sgn, ln, ang, wf, seed):
    """a tail hanging from the knot. ln: length 1..0 (it slides up into the knot), ang: degrees below horizontal"""
    n = 130; ns = 44
    Lt = TAIL_L * ln * (1.0 if sgn < 0 else 0.93)                              # never cut to quite the same length
    t_ = np.linspace(0, 1, n); d = Lt * t_
    a0 = math.radians(ang)
    bend = (0.20 * np.sin(math.pi * t_) + 0.07 * np.sin(2.3 * math.pi * t_ + seed)) * ln                                 # gentle curve
    x = CX + sgn * 6 + sgn * np.cumsum(np.cos(a0 + bend) * np.gradient(d))
    y = CY + 14 + np.cumsum(np.sin(a0 + bend) * np.gradient(d))
    z = 4 - 16 * _sm(d / 200) + 5 * np.sin(d / 55 + seed)
    P = np.stack([x, y, z], 1)
    g = np.gradient(P[:, :2], axis=0); g /= np.maximum(np.linalg.norm(g, axis=1, keepdims=True), 1e-6)
    perp = np.stack([-g[:, 1], g[:, 0], np.zeros(n)], 1) * sgn
    tw = 0.40 * np.sin(d / 120 + (0.4 if sgn > 0 else 1.9)) * min(1.0, ln * 1.5) + 0.20
    Bv = perp * np.cos(tw)[:, None] + np.array([0, 0, 1.0]) * np.sin(tw)[:, None]
    wv = (36 + (168 * wf - 36) * _sm(d / 210) ** 0.8) * (1 - 0.30 * t_ ** 2.2)          # slimmer tails that narrow gently toward the end
    s = _svals(ns)
    amp = 8.0 * np.exp(-d / 90.0) + 0.5
    disp = amp[:, None] * _pleats(s, 20 + seed, 3.0)[None, :] + 6 * np.sin(d / 90 + 2 * seed)[:, None] * s[None, :] \
        + 15 * np.sin(s[None, :] * 2.3 + seed + d[:, None] / 230) * _sm(d / 150)[:, None]      # one long soft fold down the tail
    cut = 1 - (0.5 + 0.5 * s) ** 1.6 * min(0.99, 95 / max(Lt, 1.0))  # a softer, shallower slant at the end (no sharp corner)
    return sheet(P, wv, Bv, ns=ns, disp=disp, seed=seed, tcut=cut, micro=1.6, fan=np.exp(-d / 110.0), gloss=0.85, run=2.2, crk=0.8, shine=1.0, opa=-0.03, look=True)

def knot_pieces(ks):
    """the small tight knot: a plump bead of gathered ribbon, three strands twisting across it like a rope"""
    out = []
    n = 30; ns = 14
    s = _svals(ns, 0.04)
    phi = np.linspace(-math.pi * 0.58, math.pi * 0.58, n)
    r = 45 * ks                                                              # the bead under the strands
    P = np.stack([CX - 2 + 5 * ks * np.sin(phi), CY + 3 + r * np.sin(phi), 20 * ks + 8 + r * 0.6 * np.cos(phi)], 1)
    Bv = np.stack([np.ones(n), np.zeros(n), np.zeros(n)], 1)
    wv = 72.0 * ks * (0.34 + 0.66 * np.clip(np.cos(phi / 1.16), 0, 1) ** 0.7)
    disp = (16 * ks * (1 - s ** 2))[None, :] * np.cos(phi / 1.2)[:, None]
    sh = np.array([5.0, 9.0, -14.0], np.float32) * ks                         # its shadow on the loops
    out.append(sheet(P + sh, wv * 1.22, Bv, ns=ns, seed=96, opa=-0.05, micro=0.0, hem=0.0, gloss=0.0, crk=0.0, lum=0.36, rnd=0.5))
    out.append(sheet(P, wv, Bv, ns=ns, disp=disp, seed=95, opa=0.55, micro=0.3, hem=0.0, fan=np.full(n, 0.3), gloss=0.9, rnd=0.14, crk=0.5, look=True, rope=0.6, lum=KNOT_LUM))
    ns = 10; s = _svals(ns, 0.05)
    for k, (off, rr_, zz, sl, wd, lean) in enumerate(((-25, 36, 0, -0.62, 20, 10), (19, 45, 1, 0.24, 31, 19), (-3, 51, 5, -0.38, 19, 14), (12, 33, 8, -0.95, 14, -13), (-14, 27, 10, 0.50, 10, 7))):
        r = rr_ * ks
        P = np.stack([CX - 2 + off * ks + lean * ks * np.sin(phi + 0.25 * k), CY + 3 + 0.2 * off * ks + r * np.sin(phi), (30 + zz) * ks + 10 + r * 0.6 * np.cos(phi)], 1)
        Bv = np.stack([np.ones(n), sl * np.ones(n), np.zeros(n)], 1)
        wv = wd * ks * (0.5 + 0.5 * np.cos(phi / 1.2 + 0.12 * (k - 1)))
        disp = (8 * ks * (1 - s ** 2))[None, :] * np.cos(phi / 1.2)[:, None]
        out.append(sheet(P, wv, Bv, ns=ns, disp=disp, seed=90 + k, opa=0.30, micro=0.3, lum=1.04 * KNOT_LUM, hem=0.0, fan=np.full(n, 0.3), gloss=1.6, rnd=0.16, crk=0.6, look=True, rope=1.2))
    return out

def band_piece(sgn, g, gap, seed):
    """one half of the band. g: 0 lying relaxed ... 1 drawn tight (a fan of pleats from the knot); gap: tip distance from the centre"""
    n = 150; ns = 48
    d = np.linspace(0, 500, n)                                              # distance from the knot/tip
    x = CX + sgn * (gap + d)
    y = CY + 3 * np.sin(d / 120 + seed) * (1 - g) + 3.0 * _sm(d / 260) * np.sin(d / 170 + 1.3 * seed) + sgn * 2.5 * _sm(d / 400)   # it never lies dead straight
    z = -34 + 4 * np.sin(d / 70 + seed)
    P = np.stack([x, y, z], 1)
    wk = 36 * (1 - 0.8 * _sm(gap / 12))
    w_rest = wk + (BAND_W - wk) * _sm(d / 170) ** 0.8
    w_taut = wk + (BAND_W - wk) * (d / 450) ** 0.9
    wv = np.minimum(w_rest * (1 - g) + w_taut * g, BAND_W) * (1 - 0.022 * (1 + np.sin(d / 95 + 2 * seed)) * _sm(d / 200))
    tw = 0.10 * np.sin(d / 90 + seed)
    Bv = np.stack([np.zeros(n), np.cos(tw), np.sin(tw)], 1)
    s = _svals(ns, 0.04)
    amp = (9 - 3 * g) * np.exp(-d / (110 + 90 * g)) + 0.15 + 0.30 * g
    disp = amp[:, None] * (0.55 * np.cos(s[None, :] * math.pi * 4.5 + seed + 1.6 * np.sin(s[None, :] * 3 + seed)) + 0.6 * _pleats(s, 50 + seed, 4.0)[None, :])
    fan = np.clip((0.55 + 0.45 * g) * np.exp(-d / (190 + 260 * g)) + 0.25 * g, 0, 1)
    return sheet(P, wv, Bv, ns=ns, disp=disp, seed=seed, opa=0.17, lum=0.97, micro=0.6, fan=fan, gloss=1.0, run=2.6, crk=0.45)

def bow_state(u):
    """what every piece is doing at untie progress u (0 tied ... 1 the knot has let go); keyed on the reference video, frames 150-198"""
    f = 150 + 48 * u
    return dict(
        kL=_key(f, (150, 1), (158, .86), (162, .72), (166, .46), (170, .16), (172, 0)),
        kR=_key(f, (150, 1), (158, .88), (162, .78), (166, .62), (170, .44), (174, .12), (176, 0)),
        tL=_key(f, (150, 15), (160, 11), (166, 6)), tR=_key(f, (150, 4), (158, 6), (162, 14), (166, 34), (170, 56), (174, 70)),
        lnR=_key(f, (160, 1), (166, .62), (170, .22), (173, 0)), angR=_key(f, (150, 41), (160, 43), (170, 26)),
        lnL=_key(f, (174, 1), (178, .86), (182, .66), (186, .5), (190, .26), (194, .07), (196, 0)),
        angL=_key(f, (150, 46), (166, 50), (172, 56), (178, 60), (186, 53), (192, 42)), wfL=_key(f, (160, 1), (174, 1.25), (182, 1.0), (190, .62)),
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
        c = np.float32([CX, CY]); nb = 2 if band else 0
        q = q[:nb] + [[(z, c + (pts - c) * BOW_K, col, a) for (z, pts, col, a) in piece] for piece in q[nb:]]
    return q

def render(u, band=True, bow=True):
    """RGBA frame (rgb float 0..255, alpha 0..1) with a soft contact shadow baked in"""
    q = bow_quads(u, band, bow)
    nb = 2 if band else 0
    r = np.random.default_rng(5)                            # fine crinkle shimmer of the weave
    gr = cv2.GaussianBlur(r.standard_normal((BH, BW)).astype(np.float32), (0, 0), 0.9)
    gr = gr / gr.std()
    # the band: exactly the original look (ribbon.webp shows it after the untie)
    rgb, a = rasterize(q[:nb], BW, BH) if nb else (np.zeros((BH, BW, 3), np.float32), np.zeros((BH, BW), np.float32))
    lum = rgb.mean(2, keepdims=True) / 255.0
    rgb = np.clip(rgb * (1 + 0.024 * gr[..., None]) + 9 * np.clip(gr[..., None] - 1.2, 0, 2) * lum, 0, 255)
    knee = 196.0; rgb = np.where(rgb > knee, knee + (rgb - knee) * 0.45, rgb)          # compress the highlights
    rgb = rgb * 0.90 + np.array([176, 158, 170], np.float32) * 0.10                   # a little of the fabric's own tone
    rgb = cv2.GaussianBlur(rgb, (0, 0), 0.8); a = cv2.GaussianBlur(a, (0, 0), 0.9)      # soft cloth edges, not cut-outs
    if len(q) > nb:                                         # the bow (always in front of the band): the Gemini silver satin
        brgb, ba = rasterize(q[nb:], BW, BH)
        r2 = np.random.default_rng(11)
        sp = cv2.GaussianBlur(r2.standard_normal((BH, BW)).astype(np.float32), (0, 0), 0.6); sp = sp / sp.std()
        bl = brgb.mean(2, keepdims=True) / 255.0
        brgb = np.clip(brgb * (1 + G_GRAIN * gr[..., None]) + G_SPARK * np.clip(sp[..., None] - 1.6, 0, 2) * bl ** 2, 0, 255)   # metallic glitter
        kn = G_KNEE; brgb = np.where(brgb > kn, kn + (brgb - kn) * 0.6, brgb)
        tt = G_TONE * (1 - _sm((brgb.mean(2, keepdims=True) - 150) / 90))          # rose-grey into the shadows, highlights stay white
        brgb = brgb * (1 - tt) + np.array([176, 158, 170], np.float32) * tt
        bb = cv2.GaussianBlur(brgb, (0, 0), 2.2); brgb = np.clip(brgb + 0.35 * (brgb - bb), 0, 255)   # crisp like the photo
        brgb = cv2.GaussianBlur(brgb, (0, 0), G_BLUR); ba = cv2.GaussianBlur(ba, (0, 0), 0.7)
        A2 = ba + a * (1 - ba)
        rgb = (brgb * ba[..., None] + rgb * (a * (1 - ba))[..., None]) / np.maximum(A2[..., None], 1e-4)
        a = A2
    s1 = np.roll(np.roll(cv2.GaussianBlur(a, (0, 0), 4), 5, 0), 2, 1); s1[:5] = 0; s1[:, :2] = 0      # (no wrap-around from the roll)
    s2 = np.roll(np.roll(cv2.GaussianBlur(a, (0, 0), 13), 12, 0), 5, 1); s2[:12] = 0; s2[:, :5] = 0
    sh = np.clip(0.24 * s1 + 0.20 * s2, 0, 0.5)
    A = a + sh * (1 - a)
    out = (rgb * a[..., None] + np.array([72, 48, 64], np.float32) * (sh * (1 - a))[..., None]) / np.maximum(A[..., None], 1e-4)
    return out, A
