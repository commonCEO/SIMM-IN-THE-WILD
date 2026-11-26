# ART-004 jacket candidate v004: one longer jacket (Codex brief at 6532120).
# blender -b <work/boot_candidate_v002.blend> --python jacket_long_build.py -- <absolute out.blend>
# Input holds jacket v003 (SCULPT_JACKET, SCULPT_JACKET_TRIM), collar v004, boots v002 and head v009.
# Output replaces the two jacket parts with SCULPT_JACKET_LONG and SCULPT_JACKET_LONG_TRIM. Jacket v003 itself stays
# archived unchanged in jacket_candidate_v003.blend/.glb. PROTECTED_BODY, SimmRig, the rest pose, the actions and the
# socket are read, never written.
#
# Method. Jacket v003's torso is a closed shell with thickness, open at the front. It is cut once, at Z_CUT, and
# everything of the torso below that line is replaced: the cut loop (outer face, front edges, inner face) is carried
# straight down as new rows to Z_HEM, so the new lower band is the SAME surface continued, not a second layer under
# the old hem. Each row is pushed out by one radial offset per direction, shared by the outer and inner faces, so the
# cloth keeps v003's thickness. The offset is a gentle flare, raised where needed to keep CLR of air over the frozen
# trousers, lowered where the hanging hands need room, never below FLOOR over the trousers. Weights blend from the
# cut loop's own original weights at the top to hips plus a thigh share at the hem (the prototype's rule).
# Above Z_CUT nothing moves: sleeves, chest, neckline, straps, cuffs. The front plackets keep every ring above the
# cut and continue down the new front edges as a matching roll; a hem roll of the same section closes the bottom.
import bpy, bmesh, sys, math, numpy as np
from mathutils import Vector, kdtree
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode = True
out = sys.argv[sys.argv.index("--")+1]
Z_CUT, Z_HEM, NROW = 0.655, 0.480, 16
FLARE, CLR, FLOOR, HAND_AIR, WMAX = 0.016, 0.016, 0.012, 0.006, 0.6
RHO, HEM_RHO = 0.0075, 0.0065
sstep = lambda t: 0.0 if t <= 0 else 1.0 if t >= 1 else t*t*(3-2*t)
def smooth_c(y, k=2, wrap=False):
    y = np.asarray(y, float)
    for _ in range(k):
        p = np.concatenate([y[-1:], y, y[:1]]) if wrap else np.pad(y, 1, mode='edge')
        y = 0.25*p[:-2] + 0.5*p[1:-1] + 0.25*p[2:]
    return y

rig = bpy.data.objects["SimmRig"]; bd = bpy.data.objects["PROTECTED_BODY"]
jk3 = bpy.data.objects["SCULPT_JACKET"]; tr3 = bpy.data.objects["SCULPT_JACKET_TRIM"]
col = jk3.users_collection[0]
mi = {m.name: i for i, m in enumerate(bd.data.materials) if m}
tro = BVHTree.FromPolygons([v.co.copy() for v in bd.data.vertices], [tuple(p.vertices) for p in bd.data.polygons if p.material_index == mi["Simm charcoal olive trousers"]])
gnb = [g.name for g in bd.vertex_groups]
hand = [bd.data.vertices[k].co.copy() for k in range(len(bd.data.vertices)) if any(gnb[g.group] in ("hand_l", "hand_r") and g.weight > 0.5 for g in bd.data.vertices[k].groups)]
az_of = lambda x, y: math.atan2(x, -y)
def radial_hit(tree, a, z, rmax=0.40):
    d = Vector((math.sin(a), -math.cos(a), 0.0)); h = tree.ray_cast(Vector((0, 0, z)) + d*rmax, -d, rmax)
    return (rmax - h[3]) if h[0] is not None else None
def hand_cap(a, z):
    best = 9.0
    for c in hand:
        if abs(c.z - z) > 0.030: continue
        if abs((az_of(c.x, c.y) - a + math.pi) % (2*math.pi) - math.pi) > math.radians(9): continue
        best = min(best, math.hypot(c.x, c.y))
    return best

# ---- copy v003, cut the torso ---------------------------------------------------------------------------------
me = jk3.data.copy(); me.name = "SCULPT_JACKET_LONG"; ob = bpy.data.objects.new("SCULPT_JACKET_LONG", me); col.objects.link(ob)
gidx = {g.name: g.index for g in jk3.vertex_groups}
bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
dl = bm.verts.layers.deform.active; oil = bm.verts.layers.int["orig_index"]
seen = set(); isl = []
for v in bm.verts:
    if v in seen: continue
    st = [v]; c = []; seen.add(v)
    while st:
        a_ = st.pop(); c.append(a_)
        for e in a_.link_edges:
            b_ = e.other_vert(a_)
            if b_ not in seen: seen.add(b_); st.append(b_)
    isl.append(c)
isl.sort(key=lambda c: -len(c)); assert [len(c) for c in isl] == [1258, 408, 408], [len(c) for c in isl]
torso = set(isl[0]); old_verts = set(bm.verts)
tf = [f for f in bm.faces if all(v in torso for v in f.verts)]
te = list({e for f in tf for e in f.edges})
res = bmesh.ops.bisect_plane(bm, geom=list(torso) + te + tf, plane_co=(0, 0, Z_CUT), plane_no=(0, 0, 1), clear_inner=True)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
cut = [e for e in bm.edges if e.is_boundary]
assert cut and all(abs(v.co.z - Z_CUT) < 1e-6 for e in cut for v in e.verts), "boundary outside the cut"
# order the cut into one loop
adj = {}
for e in cut:
    a_, b_ = e.verts; adj.setdefault(a_, []).append(b_); adj.setdefault(b_, []).append(a_)
assert all(len(n) == 2 for n in adj.values()), "cut is not a simple loop"
loop = [cut[0].verts[0]]; prev = None
while True:
    nx = [n for n in adj[loop[-1]] if n is not prev][0]
    if nx is loop[0]: break
    prev = loop[-1]; loop.append(nx)
assert len(loop) == len(adj), "cut has more than one loop: %d of %d vertices" % (len(loop), len(adj))
for v in loop:
    if v not in old_verts: v[oil] = -1
    assert len(v[dl]) > 0, "cut vertex without weights"
print("CUT at Z %.3f: one loop of %d vertices (%d new on the cut, %d original)" % (Z_CUT, len(loop), sum(1 for v in loop if v not in old_verts), sum(1 for v in loop if v in old_verts)))

# ---- radial offset per direction and row ----------------------------------------------------------------------
NB = 144; bw = 2*math.pi/NB
bins = lambda a: int(((a + math.pi) % (2*math.pi)) // bw) % NB
bc = np.array([-math.pi + (i + 0.5)*bw for i in range(NB)])
la = np.array([az_of(v.co.x, v.co.y) for v in loop]); lr = np.array([math.hypot(v.co.x, v.co.y) for v in loop])
rin = np.full(NB, np.nan); rout = np.full(NB, np.nan)
for a_, r_ in zip(la, lr):
    i = bins(a_); rin[i] = np.nanmin([rin[i], r_]); rout[i] = np.nanmax([rout[i], r_])
valid = ~np.isnan(rin); vi = np.where(valid)[0]
for i in range(NB):
    if not valid[i]:
        j = vi[np.argmin(np.minimum(abs(vi - i), NB - abs(vi - i)))]; rin[i] = rin[j]; rout[i] = rout[j]
zs = np.linspace(Z_CUT, Z_HEM, NROW + 1)
# Outer and inner faces get their own offsets (Do, Di). Normally both equal the target (flare, CLR over the trousers,
# FLOOR minimum), so the cloth keeps v003's thickness. Where a hanging hand leaves less room, the outer face stops
# HAND_AIR short of the hand and the inner face gives way down to FLOOR_MIN over the trousers, thinning the cloth to
# no less than TH_MIN. Only if even that does not fit does the outer face go past the cap (reported).
FLOOR_MIN, TH_MIN = 0.0085, 0.002
Do = np.zeros((NROW + 1, NB)); Di = np.zeros((NROW + 1, NB)); Fmin = np.zeros((NROW + 1, NB)); short = 0
th0 = rout - rin
for k, z in enumerate(zs):
    if k == 0: continue
    t = sstep((Z_CUT - z)/(Z_CUT - Z_HEM))
    for i, a_ in enumerate(bc):
        rt = radial_hit(tro, a_, z) or 0.10
        target = max(FLARE*t, rt + CLR - rin[i], rt + FLOOR - rin[i])
        cap_ = hand_cap(a_, z) - HAND_AIR - rout[i]
        do = min(target, cap_); di = target
        if do < target:
            di = max(rt + FLOOR_MIN - rin[i], min(target, do + th0[i] - TH_MIN))
            if do < di - th0[i] + TH_MIN: do = di - th0[i] + TH_MIN; short += 1
        Do[k, i] = do; Di[k, i] = di; Fmin[k, i] = rt + FLOOR_MIN - rin[i]
for A_ in (Do, Di):
    for k in range(1, NROW + 1): A_[k] = smooth_c(A_[k], 3, wrap=True)
    for i in range(NB): A_[1:, i] = smooth_c(A_[1:, i], 2)
Di = np.maximum(Di, Fmin); Do = np.maximum(Do, Di - th0 + TH_MIN); Do[0] = 0.0; Di[0] = 0.0
def interp(A_, k, a_):
    x = (a_ + math.pi)/bw - 0.5; i0 = int(math.floor(x)) % NB; i1 = (i0 + 1) % NB; f = x - math.floor(x)
    return A_[k, i0]*(1 - f) + A_[k, i1]*f
def offset(k, a_, r0):
    i = bins(a_); s_ = 0.0 if th0[i] < 1e-4 else min(1.0, max(0.0, (r0 - rin[i])/th0[i]))
    return interp(Di, k, a_)*(1 - s_) + interp(Do, k, a_)*s_
thin = (Do - Di)[1:] + th0[None, :]
print("OFFSET rows %d, Z %.3f to %.3f; flare %.0f mm at the hem; outer offset %.1f to %.1f mm, inner %.1f to %.1f mm; cloth thickness %.1f to %.1f mm (v003 at the cut %.1f to %.1f); bins where the hand cap could not be met: %d" % (NROW, Z_CUT, Z_HEM, FLARE*1000, Do[1:].min()*1000, Do[1:].max()*1000, Di[1:].min()*1000, Di[1:].max()*1000, thin.min()*1000, thin.max()*1000, th0.min()*1000, th0.max()*1000, short))

# ---- weights: cut-loop weights at the top, hips plus a thigh share at the hem ---------------------------------
H, TL, TR = gidx["hips"], gidx["thigh_l"], gidx["thigh_r"]
def skirt_w(x, y, z):
    side = sstep((abs(x) - 0.08)/0.08)                      # sides follow the thighs sooner: their swing has no room here
    t = (Z_CUT - z)/(Z_CUT - Z_HEM); w = WMAX*min(1.0, max(0.0, t))**(0.7 - 0.35*side)
    s = sstep(abs(x)/0.10); back = sstep(y/0.08); w *= 1.0 - 0.45*back*(1 - s)
    same, other = (TL, TR) if x < 0 else (TR, TL)
    ws, wo = w*(0.5 + 0.5*s), w*0.5*(1 - s)
    return {H: 1.0 - ws - wo, same: ws, other: wo}
def mix(w0, w1, b):
    w = {g: (1 - b)*w0.get(g, 0.0) + b*w1.get(g, 0.0) for g in set(w0) | set(w1)}
    w = dict(sorted(((g, x) for g, x in w.items() if x > 1e-4), key=lambda gx: -gx[1])[:4])
    s = sum(w.values()); return {g: x/s for g, x in w.items()}

# ---- new rows ------------------------------------------------------------------------------------------------
rows = [loop]
for k in range(1, NROW + 1):
    z = zs[k]; b = sstep(min(1.0, 2.5*k/NROW)); row = []
    for v in loop:
        a_ = az_of(v.co.x, v.co.y); r0 = math.hypot(v.co.x, v.co.y); r = r0 + offset(k, a_, r0)
        nv = bm.verts.new((math.sin(a_)*r, -math.cos(a_)*r, z)); nv[oil] = -1
        w0 = dict(v[dl].items()); w = mix(w0, skirt_w(nv.co.x, nv.co.y, z), b)
        for g, x in w.items(): nv[dl][g] = x
        row.append(nv)
    rows.append(row)
newf = []
for k in range(NROW):
    A, B = rows[k], rows[k+1]; n = len(A)
    for i in range(n):
        j = (i + 1) % n; newf.append(bm.faces.new((A[i], A[j], B[j], B[i])))
cap = bmesh.ops.triangle_fill(bm, use_beauty=True, use_dissolve=False, edges=[e for e in bm.edges if e.is_boundary and all(v in set(rows[-1]) for v in e.verts)], normal=(0, 0, -1))
newf += [f for f in cap["geom"] if isinstance(f, bmesh.types.BMFace)]
for f in newf: f.smooth = True; f.material_index = 0
bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
nm = sum(1 for e in bm.edges if len(e.link_faces) != 2)
assert nm == 0, "non-manifold edges after the band: %d" % nm
bm.to_mesh(me); bm.free(); me.update()
ob.modifiers.clear(); ob.modifiers.new("Armature", 'ARMATURE').object = rig
nvn = sum(1 for v in me.attributes["orig_index"].data if v.value < 0)
print("JACKET_LONG verts %d (new %d) tris %d; cap triangles %d; non-manifold edges 0" % (len(me.vertices), nvn, sum(len(p.vertices)-2 for p in me.polygons), len([f for f in cap["geom"] if isinstance(f, bmesh.types.BMFace)])))

# ---- trim: plackets kept above the cut and continued down the new front edges, plus a hem roll -----------------
jt = BVHTree.FromPolygons([v.co.copy() for v in me.vertices], [tuple(p.vertices) for p in me.polygons])
kd = kdtree.KDTree(len(me.vertices))
for v in me.vertices: kd.insert(v.co, v.index)
kd.balance()
def weights_at(p):                                      # inverse-distance mean of the 8 nearest jacket vertices
    acc = {}; tot = 0.0
    for _, i, d in kd.find_n(p, 8):
        w_ = 1.0/max(d, 1e-4); tot += w_
        for g in me.vertices[i].groups: acc[g.group] = acc.get(g.group, 0.0) + w_*g.weight
    return {g: x/tot for g, x in acc.items()}
def path_weights(path, passes=6):                      # weights along a roll, smoothed ring to ring, max 4, normalised
    W = [weights_at(p) for p in path]; gs = sorted({g for w in W for g in w})
    M = np.array([[w.get(g, 0.0) for g in gs] for w in W])
    for j in range(M.shape[1]): M[:, j] = smooth_c(M[:, j], passes)
    out = []
    for row in M:
        top = sorted(((gs[j], x) for j, x in enumerate(row) if x > 1e-4), key=lambda gx: -gx[1])[:4]; t_ = sum(x for _, x in top)
        out.append({g: x/t_ for g, x in top})
    return out
def front_edge(sd, z):
    for k in range(90):
        x = sd*(0.016 + 0.002*k); h = jt.ray_cast(Vector((x, -0.5, z)), Vector((0, 1, 0)), 0.9)
        if h[0] is not None and h[0].y < -0.02: return x, h[0].y
    return None
tme = tr3.data.copy(); tme.name = "SCULPT_JACKET_LONG_TRIM"; tob = bpy.data.objects.new("SCULPT_JACKET_LONG_TRIM", tme); col.objects.link(tob)
tb = bmesh.new(); tb.from_mesh(tme); tb.verts.ensure_lookup_table(); tdl = tb.verts.layers.deform.active; toi = tb.verts.layers.int["orig_index"]
seen = set(); tis = []
for v in tb.verts:
    if v in seen: continue
    st = [v]; c = []; seen.add(v)
    while st:
        a_ = st.pop(); c.append(a_)
        for e in a_.link_edges:
            b_ = e.other_vert(a_)
            if b_ not in seen: seen.add(b_); st.append(b_)
    tis.append(c)
plackets = [c for c in tis if len(c) == 96]; assert len(plackets) == 2 and len(tis) == 4, [len(c) for c in tis]
Z_KEEP = Z_CUT + 0.010                                     # placket rings at or above this stay exactly as in v003
def tube(path, rho, wlist, cap_ends=True, rho_ends=None):
    n_s = 10; rings = []; u = None
    for i, p in enumerate(path):
        tg = (path[min(i+1, len(path)-1)] - path[max(i-1, 0)]).normalized()
        u = tg.orthogonal().normalized() if u is None else (u - tg*u.dot(tg)).normalized()   # parallel transport: no twist
        w_ = tg.cross(u).normalized()
        r = rho if rho_ends is None or 0 < i < len(path)-1 else rho_ends
        ring = []
        for s in range(n_s):
            ang = 2*math.pi*s/n_s; nv = tb.verts.new(p + (u*math.cos(ang) + w_*math.sin(ang))*r); nv[toi] = -1
            for g, x in wlist[i].items(): nv[tdl][g] = x
            ring.append(nv)
        rings.append(ring)
    fs = []
    for i in range(len(rings)-1):
        for s in range(n_s):
            t_ = (s + 1) % n_s; fs.append(tb.faces.new((rings[i][s], rings[i][t_], rings[i+1][t_], rings[i+1][s])))
    if cap_ends:
        for ring in (rings[0], rings[-1]): fs.append(tb.faces.new(ring))
    return fs
newtf = []; ends = {}
for comp in plackets:
    sd = 1.0 if sum(v.co.x for v in comp) > 0 else -1.0
    low = [v for v in comp if v.co.z < Z_KEEP]; keep = [v for v in comp if v.co.z >= Z_KEEP]
    kz = min(v.co.z for v in keep); last = [v for v in keep if v.co.z - kz < 0.004]
    c0 = sum((v.co for v in last), Vector())/len(last); r0 = sum((v.co - c0).length for v in last)/len(last)
    bmesh.ops.delete(tb, geom=low, context='VERTS')
    # the cut ring of the kept strip is open now; close it
    hole = [e for e in tb.edges if e.is_boundary and all(v in set(last) for v in e.verts)]
    if hole: bmesh.ops.holes_fill(tb, edges=hole, sides=0)
    zz = list(np.arange(kz, Z_HEM + 0.006, -0.008)) + [Z_HEM + 0.006]; ex = []; ey = []
    for z in zz:
        e = front_edge(sd, z); e = e if e is not None else (ex[-1], ey[-1])
        ex.append(e[0]); ey.append(e[1])
    ex, ey = smooth_c(ex, 3), smooth_c(ey, 3)
    path = [Vector((float(x) - sd*0.003, float(y) + 0.002, float(z))) for x, y, z in zip(ex, ey, zz)]
    sh = c0 - path[0]
    for i, p in enumerate(path): p += sh*max(0.0, 1.0 - i/4.0)       # start exactly on the kept ring, ease onto the new edge
    newtf += tube(path, max(r0, RHO*0.9), path_weights(path))
    ends[sd] = path[-1]
    print("PLACKET %s: %d v003 rings kept (Z >= %.3f), %d vertices removed below; new roll %d rings from Z %.3f to %.3f" % ("+X" if sd > 0 else "-X", len({round(v.co.z, 3) for v in keep}), Z_KEEP, len(low), len(path), path[0].z, path[-1].z))
# hem roll from one front corner round the back to the other
zh = Z_HEM + 0.005; a_p, a_m = az_of(ends[1.0].x, ends[1.0].y), az_of(ends[-1.0].x, ends[-1.0].y)
aa = np.linspace(a_p, a_m + 2*math.pi, 140); path = []
for a_ in aa:
    r = radial_hit(jt, a_, zh) or 0.2
    path.append(Vector((math.sin(a_)*(r - 0.002), -math.cos(a_)*(r - 0.002), zh)))
path[0] = Vector((ends[1.0].x, ends[1.0].y, zh)); path[-1] = Vector((ends[-1.0].x, ends[-1.0].y, zh))
newtf += tube(path, HEM_RHO, path_weights(path))
for f in newtf: f.smooth = True; f.material_index = 0
bmesh.ops.recalc_face_normals(tb, faces=tb.faces[:])
tb.to_mesh(tme); tb.free(); tme.update()
tob.modifiers.clear(); tob.modifiers.new("Armature", 'ARMATURE').object = rig
print("TRIM_LONG verts %d (new %d) tris %d" % (len(tme.vertices), sum(1 for v in tme.attributes["orig_index"].data if v.value < 0), sum(len(p.vertices)-2 for p in tme.polygons)))

# ---- swap in the new parts; v003 stays archived in its own files ----------------------------------------------
for o in (jk3, tr3): bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=out)
