# Stage 1: primary head forms. START_HERE_v02.blend -> work/stage1.blend
import bpy, sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, sk; importlib.reload(sk)
from sk import *
out = sys.argv[sys.argv.index("--")+1]
face = bpy.data.objects["SCULPT_BASE_FACE"]
apply_world(face)
S = Sculpt(face)
print("twin maxdist", S.find_twins())
VF = vert_face_sets(face)
FS = {k: VF[k].astype(float) for k in VF}
ear = FS[29]; neck = np.maximum(FS[6], FS[359])
co = S.co

# ---- 1. macro proportions: toddler-big cranium, short lower face, slim short neck
zt = smooth_table([0.980, 1.030, 1.048, 1.103, 1.144, 1.187, 1.215, 1.338],
                  [0.950, 1.004, 1.040, 1.092, 1.126, 1.176, 1.216, 1.386], 0.008, 0.90, 1.42)
sx = smooth_table([0.980, 1.030, 1.048, 1.075, 1.103, 1.144, 1.187, 1.250, 1.338],
                  [0.80, 0.80, 1.12, 1.38, 1.52, 1.62, 1.64, 1.63, 1.60], 0.010, 0.90, 1.42)
sy = smooth_table([0.980, 1.030, 1.048, 1.103, 1.144, 1.187, 1.250, 1.338],
                  [0.85, 0.85, 1.10, 1.14, 1.18, 1.24, 1.30, 1.30], 0.010, 0.90, 1.42)
z0 = co[:, 2].copy()
co[:, 0] *= remap(z0, sx)
co[:, 1] = co[:, 1]*remap(z0, sy) + 0.008
co[:, 2] = remap(z0, zt)
S.co = co
# ears: the widening stretched them sideways; pull them back toward the skull and thin them
for s in (1, -1):
    m = ear*(np.sign(S.co[:, 0]) == s)
    x = S.co[:, 0]; piv = 0.158*s
    S.co[:, 0] = np.where(m > 0, piv + (x - piv)*0.50, x)

def soft(mask, it=3):
    m = mask.astype(float).copy(); E = S.E
    for _ in range(it):
        acc = np.zeros(S.n); np.add.at(acc, E[:, 0], m[E[:, 1]]); np.add.at(acc, E[:, 1], m[E[:, 0]])
        m = 0.5*m + 0.5*acc/np.maximum(S.deg, 1)
    return m
def mscale(mask, pivot, s):
    S.co += mask[:, None]*((S.co - np.asarray(pivot, float))*(np.asarray(s, float) - 1.0))

# ---- 2. nose: small, soft, integrated button; nostril cuts dissolved
mn = soft(FS[45], 4)
mscale(mn, (0, -0.124, 1.134), (0.50, 0.40, 0.60))
S.smooth(mask=soft(FS[45], 2), it=10, k=0.6)
S.grab((0, -0.134, 1.128), 0.022, (0, -0.003, 0.004))          # slightly upturned tip
# ---- 3. forehead and brow: child skull, no brow shelf, rounded forehead
S.grab((0, -0.135, 1.30), 0.10, (0, -0.004, 0.0))               # upper forehead roundness
S.grab((0, -0.140, 1.225), 0.085, (0, 0.011, 0.0))              # lower forehead back: no shelf over the eyes
S.smooth((0, -0.13, 1.215), 0.10, it=6, k=0.5)                  # melt the adult brow ridge
S.grab((0, 0.16, 1.26), 0.16, (0, 0.022, 0.0))                  # fuller occiput
S.grab((0, 0.0, 1.40), 0.15, (0, 0, 0.008))                     # crown dome
S.grab((0.135, -0.02, 1.365), 0.11, (-0.014, 0, -0.008), mirror=True)   # round off the boxy top corners
S.grab((0.16, 0.03, 1.25), 0.12, (0.004, 0, 0), mirror=True)    # parietal width
S.grab((0, -0.132, 1.190), 0.050, (0, 0.011, 0.0))               # glabella back: relaxed, no frown knot
S.grab((0, -0.128, 1.160), 0.032, (0, 0.006, 0.0))               # low soft child nose bridge
# ---- 4. mouth: designed as a closed quiet-smile line on the base's real lip loops
S.grab((0, -0.120, 1.088), 0.075, (0, -0.002, 0.0))             # slight muzzle fullness
S.scale((0, -0.125, 1.090), 0.060, (0.56, 1.0, 1.0), pivot=(0, -0.125, 1.090))
S.scale((0, -0.133, 1.090), 0.042, (1.0, 0.55, 0.85), pivot=(0, -0.122, 1.091))   # lips lose adult projection
UL = VF[44] & VF[47]; LL = VF[46] & VF[48]
from collections import deque
adj = [[] for _ in range(S.n)]
for a_, b_ in S.E: adj[a_].append(b_); adj[b_].append(a_)
skin_ = VF[44] | VF[46] | VF[45]
dl = np.full(S.n, 99); dq = deque()
for v in np.where(UL | LL)[0]: dl[v] = 0; dq.append(v)
while dq:
    v = dq.popleft()
    for w_ in adj[v]:
        if skin_[w_] and dl[w_] > dl[v]+1: dl[w_] = dl[v]+1; dq.append(w_)
lipline = (dl <= 2)                                   # the three tight loops that make the closed lip seam
inner = (VF[47] | VF[48] | VF[49]) & ~lipline
upper_ = VF[44] & ~VF[46]; lower_ = VF[46] & ~VF[44]
xm = np.abs(S.co[lipline, 0]).max()
MW = 0.0225; MZ = 1.0900; MY = S.co[lipline, 1].min() + 0.0030
def mouth_line(u):
    au = np.abs(u)
    z = MZ - 0.0018 + 0.0062*au**2.0           # corners sit ~6 mm above the centre: one smooth upturned arc
    y = MY + 0.0070*au**2.0                     # line wraps round the muzzle
    return u*MW, y, z
idx = np.where(lipline)[0]; u = np.clip(S.co[idx, 0]/xm, -1, 1)
x, y, z = mouth_line(u)
ring = dl[idx]
y = y + (2 - ring)*0.0013                        # inner loops step back into the mouth
z = z + np.where(ring == 2, 0.0003*(upper_[idx].astype(float) - lower_[idx].astype(float))*(1-np.abs(u)), 0.0)
S.co[idx] = np.stack([x, y, z], 1)
idx = np.where(inner)[0]; u = np.clip(S.co[idx, 0]/xm, -1, 1)
x, y, z = mouth_line(u)
zc = S.co[idx, 2].mean()
S.co[idx, 0] = x*0.9
S.co[idx, 2] = z + (S.co[idx, 2] - zc)*0.08
S.co[idx, 1] = np.maximum(S.co[idx, 1], y + 0.007)
# relax the lip skin into one soft mound, then re-seat the seam on it as a short, shallow crease
free_ = (~inner).astype(float)
tgt = S.co[lipline].copy(); ringl = dl[lipline]
for _pass in range(3):
    zone = S.w((0, -0.122, 1.090), 0.062)*free_
    S.smooth(mask=zone, it=25, k=0.5)                       # seam floats with the surface
    cur = S.co[lipline]
    cur[:, 0] = tgt[:, 0]; cur[:, 2] = tgt[:, 2]
    cur[:, 1] = cur[:, 1] + 0.0004 + (2 - ringl)*0.0012   # crease depth
    S.co[lipline] = cur
    S.smooth(mask=zone*(~lipline).astype(float), it=10, k=0.5)   # skin settles around the pinned seam
ii = np.where(inner)[0]
S.co[ii, 1] = np.maximum(S.co[ii, 1], S.co[lipline, 1].max() + 0.004)
S.inflate((0, -0.130, 1.0815), 0.014, 0.0022, mask=(~(lipline | inner)).astype(float))       # small lower lip pad
S.inflate((0, -0.130, 1.0965), 0.016, 0.0012, mask=(~(lipline | inner)).astype(float))       # upper lip, barely there
S.grab((MW+0.004, -0.118, 1.096), 0.014, (0.0, 0.0015, 0.0), mask=(~(lipline | inner)).astype(float), mirror=True)  # corner dimples
# ---- 5. jaw, chin, cheeks
S.inflate((0.080, -0.075, 1.072), 0.060, 0.012, mirror=True)                 # soft jowl: round lower face, not a wedge
S.grab((0.150, -0.045, 1.185), 0.075, (-0.009, 0.0, 0.0), mirror=True)       # temples in: widest point drops to the cheeks
S.grab((0, -0.112, 1.046), 0.045, (0, -0.007, 0.003))                        # chin: small, soft, under the lip
S.scale((0, -0.110, 1.050), 0.050, (0.90, 1.0, 1.0), pivot=(0, -0.110, 1.050))
S.inflate((0.098, -0.092, 1.104), 0.075, 0.010, mirror=True)                 # full low cheeks
S.grab((0.060, -0.118, 1.116), 0.040, (0.0, -0.004, 0.002), mirror=True)     # cheek front (apple)
S.smooth((0, -0.10, 1.07), 0.09, it=3, k=0.4, mask=(~(lipline | inner)).astype(float))
# ---- 6. ears: smaller, simpler, set lower (child ear sits between eye and nose base)
me_ = soft(ear, 2)
for s_ in (1, -1):
    m = me_*(np.sign(S.co[:, 0]) == s_)
    mscale(m, (0.160*s_, 0.035, 1.150), (1.0, 0.80, 0.78))
# ---- 7. neck: slim child neck
mk = soft(neck, 3)
S.co[:, 0] *= (1 - 0.10*mk)
S.symmetrize()

# ---- 8. eyes: fit the base's real lid rings onto eyeballs as upright ovals
from collections import deque
EYE_R = 0.043; EYE_X = 0.064; EYE_Z = 1.171; OVAL_A = 0.0225; OVAL_B = 0.0300; OVAL_N = 2.35
adj = [[] for _ in range(S.n)]
for a_, b_ in S.E: adj[a_].append(b_); adj[b_].append(a_)
def bfs(src, allowed):
    d = np.full(S.n, 10**6); dq = deque()
    for v in src: d[v] = 0; dq.append(v)
    while dq:
        v = dq.popleft()
        for w_ in adj[v]:
            if allowed[w_] and d[w_] > d[v]+1: d[w_] = d[v]+1; dq.append(w_)
    return d
skin_rest = VF[44] | VF[45] | VF[46] | VF[29]
def oval(phi, grow=0.0):
    c, s_ = np.cos(phi), np.sin(phi)
    e = 2.0/OVAL_N
    p = (OVAL_A+grow)*np.sign(c)*np.abs(c)**e
    # egg: a touch wider in the upper half, lower lid slightly flatter
    q = (OVAL_B+grow)*np.sign(s_)*np.abs(s_)**e
    q = np.where(q < 0, q*0.94, q)
    return p, q
eye_info = {}
for sgn in (1, -1):
    side = (S.co[:, 0]*sgn) > 0
    A = VF[37] & side; Bm = VF[28] & side; Cm = VF[27] & side
    L0 = A & Bm; L1 = Bm & Cm; L2 = Cm & skin_rest
    region = A | Bm | Cm
    d0 = bfs(np.where(L0)[0], region); d1 = bfs(np.where(L1)[0], region); d2 = bfs(np.where(L2)[0], region)
    # order the inner lid loop
    l0 = np.where(L0)[0]; l0set = set(l0.tolist())
    start = l0[np.argmax(S.co[l0, 0]*sgn)]           # outer corner
    loop = [start]; prev = None; cur = start
    while True:
        nxt = [w_ for w_ in adj[cur] if w_ in l0set and w_ != prev and (w_ not in loop or (w_ == start and len(loop) > 2))]
        if not nxt or nxt[0] == start: break
        prev, cur = cur, nxt[0]; loop.append(cur)
    assert len(loop) == len(l0), (len(loop), len(l0))
    P = S.co[loop]
    inner_i = int(np.argmin(P[:, 0]*sgn))
    seg = np.linalg.norm(np.roll(P, -1, 0) - P, axis=1)
    arcA = list(range(0, inner_i+1)); arcB = list(range(inner_i, len(loop))) + [0]
    upA = P[arcA, 2].mean() > P[arcB, 2].mean()
    phi = np.zeros(S.n)
    def assign(arc, a0, a1):
        L = np.concatenate([[0], np.cumsum([seg[i] for i in arc[:-1]])]); L /= L[-1]
        for i, t_ in zip(arc, L): phi[loop[i]] = a0 + (a1-a0)*t_
    if upA: assign(arcA, 0.0, np.pi); assign(arcB, np.pi, 2*np.pi)
    else:   assign(arcA, 2*np.pi, np.pi); assign(arcB, np.pi, 0.0)
    # propagate the ring parameter outward (and inward into the socket) along the radial edge flow
    known = L0.copy()
    order = sorted(np.where(region & ~L0)[0], key=lambda v: d0[v])
    for v in order:
        nb = [w_ for w_ in adj[v] if known[w_] and d0[w_] < d0[v]]
        if not nb: nb = [w_ for w_ in adj[v] if known[w_]]
        if not nb: continue
        phi[v] = np.arctan2(np.mean(np.sin(phi[nb])), np.mean(np.cos(phi[nb]))); known[v] = True
    # eyeball centre: front pole sits a little behind the surrounding skin so the eye is set in, not bulging
    l2 = np.where(L2)[0]
    skin_y = np.percentile(S.co[l2, 1], 35)
    C = np.array([EYE_X*sgn, skin_y + 0.0035 + EYE_R, EYE_Z])
    eye_info[sgn] = C
    def on_sphere(p, q, R):
        return np.stack([C[0] + p*sgn, C[1] - np.sqrt(np.maximum(R*R - p*p - q*q, 1e-8)), C[2] + q], 1)
    idx = np.where(region)[0]
    new = S.co.copy()
    for v in idx:
        ph = phi[v]; up = max(np.sin(ph), 0.0)
        th = 0.0016 + 0.0034*up                         # upper lid carries the thickness; lower lid stays flush
        if A[v] and not L0[v]:
            p, q = oval(np.array([ph]), -0.002*min(d0[v], 6))
            new[v] = on_sphere(p, q, EYE_R - 0.003 - 0.002*min(d0[v], 6))[0]
        elif Bm[v]:
            t_ = d0[v]/max(d0[v]+d1[v], 1)
            p, q = oval(np.array([ph]), (0.0012 + 0.0020*up)*t_)
            new[v] = on_sphere(p, q, EYE_R - 0.0010 + (th+0.0010)*(t_**0.7))[0]
        elif Cm[v]:
            tau = d1[v]/max(d1[v]+d2[v], 1)
            p, q = oval(np.array([ph]), (0.0012 + 0.0020*up) + 0.020*tau)
            lid = on_sphere(p, q, EYE_R + th)[0]
            h = tau*tau*(3-2*tau)
            new[v] = lid*(1-h) + S.co[v]*h
    S.co = new
    # relax the orbital skin between lid and face so the transition is a soft sculpted slope
    m = (Cm & ~L1 & ~L2).astype(float)
    S.smooth(mask=m, it=12, k=0.5)
    S.smooth(mask=(L2 & ~Bm).astype(float), it=3, k=0.4)
# brow: melt everything between upper lid and forehead into one calm slope (lids stay pinned)
zc_ = S.co[:, 2]; fr = np.clip((-S.co[:, 1] - 0.05)/0.04, 0, 1)
band = np.clip((zc_ - 1.175)/0.02, 0, 1)*np.clip((1.30 - zc_)/0.04, 0, 1)*fr
nb = np.clip((zc_ - 1.135)/0.02, 0, 1)*np.clip((0.036 - np.abs(S.co[:, 0]))/0.012, 0, 1)*fr   # between the eyes, down the bridge
pin = VF[28] | VF[37]
browmask = np.maximum(band, nb)*(~pin).astype(float)
S.smooth(mask=browmask, it=40, k=0.5)
S.grab((0.064, -0.118, 1.150), 0.030, (0, -0.002, 0.0015), mirror=True)  # hint of lower-lid/cheek lift for the smile
S.symmetrize()
print("EYE centres", eye_info)
S.commit()
for p_ in face.data.polygons: p_.use_smooth = True
md = face.modifiers.new("Subdivision", 'SUBSURF'); md.levels = 1; md.render_levels = 1

# ---- eyeballs: keep the base eye's outer shell, make it a true sphere of the fitted radius
import bmesh
for nm, sgn in (("SCULPT_BASE_EYE_L", 1), ("SCULPT_BASE_EYE_R", -1)):
    eo = bpy.data.objects[nm]; apply_world(eo)
    bm = bmesh.new(); bm.from_mesh(eo.data); bm.verts.ensure_lookup_table()
    # islands
    seen = set(); isl = []
    for v in bm.verts:
        if v.index in seen: continue
        st = [v]; comp = []; seen.add(v.index)
        while st:
            x = st.pop(); comp.append(x)
            for e in x.link_edges:
                y = e.other_vert(x)
                if y.index not in seen: seen.add(y.index); st.append(y)
        isl.append(comp)
    def ext(comp):
        c = np.array([v.co for v in comp]); return np.prod(c.max(0)-c.min(0))
    isl.sort(key=ext)
    bmesh.ops.delete(bm, geom=isl[0], context='VERTS')       # inner iris bowl shell
    cs = np.array([v.co for v in bm.verts]); cen = 0.5*(cs.max(0)+cs.min(0))
    C = eye_info[sgn]
    for v in bm.verts:
        d = np.array(v.co) - cen; d /= np.linalg.norm(d)
        v.co = C + d*EYE_R
    for f in bm.faces: f.smooth = True
    bm.to_mesh(eo.data); bm.free(); eo.data.update()
bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out)
