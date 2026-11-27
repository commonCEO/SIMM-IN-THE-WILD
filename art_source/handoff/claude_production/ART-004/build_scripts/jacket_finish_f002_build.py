# ART-004 jacket + neck FINISH candidate f002: boundary and fold repair of f001 (Codex brief at 9de793b).
# blender -b <work/jacket_candidate_v004.blend> --python jacket_finish_f002_build.py -- <absolute out.blend>
# Held as in f001: the v004 envelope, hem length, hand-clear fit, strap paths, collar seating, head, boots, body, rig,
# rest pose, actions, socket; every original jacket and trim vertex keeps its v004 weights exactly. Kept from f001: the
# one-time subdivision, the hem-band waves, the two pockets (same separate part) and the brown neck colour.
# Changed from f001, after the diagnostic (f001's per-vertex "nearest jacket normal" trim flatten made the scalloped
# placket and the notched wrist; cuff widening made the wrist worse; subdivision and folds made neither):
#  - trim: the placket and cuff rolls (not the hem roll) are flattened about their OWN centre (mean of the roll within 10 mm) along a direction smoothed over
#    the roll, so neighbouring points move alike. Cuffs use the forearm's radial direction. No cuff widening.
#  - folds fade to zero within about 30 mm of the front plackets and the cuffs, so those boundary loops keep v004's shape.
#  - sleeves: the regular rings and the shoulder wave are gone. Three unequal compression folds sit at the inner elbow
#    only, blending out round the outer arm and ending well above the cuff.
import bpy, bmesh, sys, math, numpy as np
from mathutils import Vector, kdtree
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode = True
out = sys.argv[sys.argv.index("--")+1]
import os
STEPS = set(os.environ.get("FIN_STEPS", "sub,folds,flatten,cuff,pockets,neck").split(","))   # f002 diagnostic: run a subset
sstep = lambda x: np.clip(x, 0, 1)**2*(3 - 2*np.clip(x, 0, 1))
rig = bpy.data.objects["SimmRig"]; jk = bpy.data.objects["SCULPT_JACKET_LONG"]; tr = bpy.data.objects["SCULPT_JACKET_LONG_TRIM"]
def co_of(o): a = np.empty(len(o.data.vertices)*3); o.data.vertices.foreach_get("co", a); return a.reshape(-1, 3)
def set_co(o, c): o.data.vertices.foreach_set("co", c.ravel()); o.data.update()
B = {b: (np.array(rig.matrix_world @ rig.data.bones[b].head_local), np.array(rig.matrix_world @ rig.data.bones[b].tail_local)) for b in ("upper_arm_l", "forearm_l", "upper_arm_r", "forearm_r")}

def arm_frame(p, side):
    """nearest point on the arm (upper arm + forearm), distance along the arm from the elbow, radial unit vector"""
    best = None
    for b in ("upper_arm_" + side, "forearm_" + side):
        h, t = B[b]; d = t - h; s = np.clip(np.dot(p - h, d)/np.dot(d, d), 0, 1); q = h + s*d; r = np.linalg.norm(p - q)
        if best is None or r < best[0]: best = (r, q, b, s, d)
    r, q, b, s, d = best; elbow = B["forearm_" + side][0]
    along = np.dot(q - elbow, -d/np.linalg.norm(d)) if b.startswith("upper") else -np.dot(q - elbow, d/np.linalg.norm(d))
    rad = (p - q)/max(r, 1e-6)
    return along, rad, r

def fold_field(P, sleeve_side=None):
    """displacement (m) for each rest position; sleeve_side: per-point 'l', 'r' or '' (torso or not a sleeve)"""
    D = np.zeros_like(P)
    # torso lower band: waves round the body, growing toward the hem, none where the hands hang, none above the waist
    az = np.degrees(np.arctan2(P[:, 0], -P[:, 1])); rxy = np.hypot(P[:, 0], P[:, 1])
    radial = np.c_[P[:, 0]/np.maximum(rxy, 1e-6), P[:, 1]/np.maximum(rxy, 1e-6), np.zeros(len(P))]
    amp = 0.0038*sstep((0.615 - P[:, 2])/0.11)
    amp *= 1.0 - np.exp(-((np.abs(az) - 82.0)/16.0)**2)                   # hands hang at about +-82 degrees
    if sleeve_side is not None: amp *= np.array([s_ == "" for s_ in sleeve_side])   # torso only
    wave = np.sin(np.radians(az)*7.0 + 2.2*(0.60 - P[:, 2])/0.12)
    D += radial*(amp*wave)[:, None]
    # sleeves: three unequal compression folds at the inner elbow (along = distance above the elbow, m), tilted a
    # little, strongest on the inner side and gone round the outer arm; the nearest one to the wrist ends 50 mm above it
    RIDGES = [(0.016, 0.0045, 0.0070), (-0.002, 0.0032, 0.0060), (-0.019, 0.0020, 0.0055)]   # centre, height, half-width
    for side, sx in (("l", -1), ("r", 1)):
        m = np.array([s_ == side for s_ in sleeve_side]) if sleeve_side is not None else (P[:, 0]*sx > 0.17)
        for i in np.where(m)[0]:
            along, rad, r = arm_frame(P[i], side)
            if r > 0.09: continue
            inner = max(-rad[1], 0.0)**1.3                                 # 1 on the inner (front) side, 0 round the outer arm
            tilt = 0.007*rad[0]*sx
            e = sum(h*math.exp(-((along - c - tilt)/w)**2) for c, h, w in RIDGES)*inner
            D[i] += rad*e
    return D

# 1-2: jacket and trim, positions only -------------------------------------------------------------------------
w_before = {o.name: [sorted((g.group, round(g.weight, 7)) for g in v.groups) for v in o.data.vertices] for o in (jk, tr)}
# the v003/v004 sleeves and upper torso are too coarse (408 vertices per sleeve) to carry folds a few cm apart: the
# jacket is subdivided once. Original vertices keep their positions and weights (asserted below); new vertices get
# weights interpolated by the subdivision and orig_index -1.
n_old = len(jk.data.vertices)
bmj = bmesh.new(); bmj.from_mesh(jk.data)
if "sub" not in STEPS: bmj.free(); bmj = None
# edges of many-sided faces (the closed sleeve ends) are not cut: cutting them puts a new vertex at the cap's centre,
# on the arm axis, inside the wrist
if bmj is not None:
    ngon_e = {e for f in bmj.faces if len(f.verts) > 4 for e in f.edges}
    bmesh.ops.subdivide_edges(bmj, edges=[e for e in bmj.edges if e not in ngon_e], cuts=1, use_grid_fill=True, smooth=0.0)
    oil_ = bmj.verts.layers.int["orig_index"]; bmj.verts.ensure_lookup_table()
    for v in bmj.verts[n_old:]: v[oil_] = -1
    bmj.to_mesh(jk.data); bmj.free(); jk.data.update()
for p_ in jk.data.polygons: p_.use_smooth = True
# new vertices only: drop interpolated weights under 0.01, keep at most 4, renormalise (clean export)
for v in jk.data.vertices[n_old:]:
    ws_ = sorted(((g.group, g.weight) for g in v.groups if g.weight >= 0.01), key=lambda gw: -gw[1])[:4]; t_ = sum(w for _, w in ws_)
    for g in [g.group for g in v.groups]: jk.vertex_groups[g].remove([v.index])
    for g, w in ws_: jk.vertex_groups[g].add([v.index], w/t_, 'REPLACE')
w_now = [sorted((g.group, round(g.weight, 7)) for g in v.groups) for v in jk.data.vertices]
assert w_now[:n_old] == w_before[jk.name], "subdivision changed original weights"
assert all(len(w) > 0 for w in w_now[n_old:]), "a new vertex has no weights"
w_before[jk.name] = w_now
print("SUBDIVIDE jacket %d -> %d vertices; original weights identical" % (n_old, len(jk.data.vertices)))
J0 = co_of(jk); T0 = co_of(tr)
# which jacket vertices are sleeves: the connected pieces other than the torso (the largest)
ed = np.empty(len(jk.data.edges)*2, dtype=np.int64); jk.data.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
par = list(range(len(J0)))
def fnd(a):
    while par[a] != a: par[a] = par[par[a]]; a = par[a]
    return a
for a, b in ed: par[fnd(a)] = fnd(b)
root = np.array([fnd(i) for i in range(len(J0))]); ids, cnt = np.unique(root, return_counts=True); torso_id = ids[cnt.argmax()]
side = np.array(["" if r == torso_id else ("l" if J0[root == r][:, 0].mean() < 0 else "r") for r in root])
print("PIECES jacket: torso %d vertices, sleeves %d (l) and %d (r)" % ((side == "").sum(), (side == "l").sum(), (side == "r").sum()))
# fade the folds to zero near the plackets and cuffs (the trim islands other than the hem roll)
_tb = bmesh.new(); _tb.from_mesh(tr.data); _tb.verts.ensure_lookup_table(); _seen = set(); _comps = []
for v in _tb.verts:
    if v.index in _seen: continue
    st = [v]; c = []; _seen.add(v.index)
    while st:
        a_ = st.pop(); c.append(a_.index)
        for e in a_.link_edges:
            b2 = e.other_vert(a_)
            if b2.index not in _seen: _seen.add(b2.index); st.append(b2)
    _comps.append(c)
_tb.free()
_hem = max(_comps, key=lambda c: (np.array([tr.data.vertices[i].co.z for i in c]).max() < 0.50, len(c)))   # the roll that stays below Z 0.50
_bound = np.array([tr.data.vertices[i].co[:] for c in _comps if c is not _hem for i in c])
_bkd = kdtree.KDTree(len(_bound))
for i, p in enumerate(_bound): _bkd.insert(Vector(p), i)
_bkd.balance()
def boundary_fade(P): return np.array([float(sstep((_bkd.find(Vector(p))[2] - 0.006)/0.024)) for p in P])
print("BOUNDARY trim islands %s; hem roll %d vertices (not faded)" % ([len(c) for c in _comps], len(_hem)))
# inward hem waves may not take the cloth closer than 3 mm to the frozen trousers (f002 contact check: inward waves
# pushed the hem edge into the trousers at about +-64 degrees)
_bd = bpy.data.objects["PROTECTED_BODY"]; _mi = {m.name: i for i, m in enumerate(_bd.data.materials) if m}
_tro = BVHTree.FromPolygons([v.co.copy() for v in _bd.data.vertices], [tuple(p.vertices) for p in _bd.data.polygons if p.material_index == _mi["Simm charcoal olive trousers"]])
def limit_inward(P, D):
    for i in np.where(np.linalg.norm(D, axis=1) > 1e-6)[0]:
        rxy = math.hypot(P[i, 0], P[i, 1]); radial = np.array([P[i, 0]/rxy, P[i, 1]/rxy, 0.0]); inw = -float(D[i] @ radial)
        if inw <= 0: continue
        near = _tro.find_nearest(Vector(P[i]), 0.05); clear = near[3] if near[0] is not None else 0.05
        cap = max(0.0, clear - 0.003)
        if inw > cap: D[i] += radial*(inw - cap)
    return D
_tmask = np.array([s_ == "" for s_ in side])
_DJ = fold_field(J0, side)*boundary_fade(J0)[:, None]; _DJ[_tmask] = limit_inward(J0[_tmask], _DJ[_tmask])
if "folds" in STEPS: set_co(jk, J0 + _DJ)
J1 = co_of(jk)
jt = BVHTree.FromPolygons([tuple(p) for p in J1], [tuple(p.vertices) for p in jk.data.polygons])
tkd = kdtree.KDTree(len(J0))
for i, p in enumerate(J0): tkd.insert(Vector(p), i)
tkd.balance()
tside = np.array([side[tkd.find(Vector(p))[1]] for p in T0])             # trim follows the piece it sits on
_DT = fold_field(T0, tside)*boundary_fade(T0)[:, None]; _ttm = np.array([s_ == "" for s_ in tside]); _DT[_ttm] = limit_inward(T0[_ttm], _DT[_ttm])
T1 = T0 + _DT if "folds" in STEPS else T0.copy()
FLAT = 0.45
if "flatten" in STEPS:
    # direction: nearest jacket normal, smoothed over the trim's own edges; cuffs: the forearm's radial direction
    N_ = np.array([np.array(jt.find_nearest(Vector(p), 0.05)[1] or (0, 0, 1)) for p in T1])
    ted = np.empty(len(tr.data.edges)*2, dtype=np.int64); tr.data.edges.foreach_get("vertices", ted); ted = ted.reshape(-1, 2)
    tdeg = np.bincount(ted.ravel(), minlength=len(T1)).astype(float)
    for _ in range(60):
        acc = np.zeros_like(N_); np.add.at(acc, ted[:, 0], N_[ted[:, 1]]); np.add.at(acc, ted[:, 1], N_[ted[:, 0]])
        N_ = 0.5*N_ + 0.5*acc/np.maximum(tdeg, 1)[:, None]; N_ /= np.maximum(np.linalg.norm(N_, axis=1), 1e-9)[:, None]
    cuff_idx = set(i for c in _comps if len(c) == 726 for i in c)
    for c in [c for c in _comps if c is not _hem]:                          # the hem roll is not flattened: it already
        ckd = kdtree.KDTree(len(c))                                        # crosses the trousers in v004; flattening moved that
        for k, i in enumerate(c): ckd.insert(Vector(T1[i]), k)
        ckd.balance()
        for i in c:
            p = T1[i]; near = [c[k] for _, k, _ in ckd.find_range(Vector(p), 0.010)]; cen = T1[near].mean(0)
            if i in cuff_idx:
                sd = "l" if p[0] < 0 else "r"; h, t = B["forearm_" + sd]; ax = (t - h)/np.linalg.norm(t - h)
                q = h + ax*np.dot(cen - h, ax); n = cen - q; n -= ax*np.dot(n, ax); n /= max(np.linalg.norm(n), 1e-9)
            else:
                n = N_[i]
            dn = float((p - cen) @ n)
            T1[i] = p - (1 - FLAT)*dn*n
# cuffs: the two v003 cuff rings become flat bands, twice as long along the arm (about 11 to 22 mm), growing only toward
# the elbow so the wrist edge (and the hand's clearance) stays where it was
tb_ = bmesh.new(); tb_.from_mesh(tr.data); tb_.verts.ensure_lookup_table()
seen = set(); comps = []
for v in tb_.verts:
    if v.index in seen: continue
    st = [v]; c = []; seen.add(v.index)
    while st:
        a_ = st.pop(); c.append(a_.index)
        for e in a_.link_edges:
            b2 = e.other_vert(a_)
            if b2.index not in seen: seen.add(b2.index); st.append(b2)
    comps.append(c)
tb_.free()
cuffs = [c for c in comps if len(c) == 726]; assert len(cuffs) == 2, [len(c) for c in comps]
for c in []:                                                                   # f002: no cuff widening
    P_ = T1[c]; cen = P_.mean(0); sd = "l" if cen[0] < 0 else "r"; h, t = B["forearm_" + sd]; ax = (t - h)/np.linalg.norm(t - h)
    along = (P_ - cen) @ ax; lo = along.max()                                       # ax points toward the wrist
    T1[c] = P_ + np.outer((along - lo)*1.0, ax)                                    # wrist edge fixed, band doubles toward the elbow
set_co(tr, T1)
for o in (jk, tr):
    assert [sorted((g.group, round(g.weight, 7)) for g in v.groups) for v in o.data.vertices] == w_before[o.name], o.name + ": weights changed"
print("FOLDS jacket: %d of %d vertices moved over 0.1 mm, max %.1f mm; trim: max move %.1f mm" % (int((np.linalg.norm(J1 - J0, axis=1) > 1e-4).sum()), len(J0), np.linalg.norm(J1 - J0, axis=1).max()*1000, np.linalg.norm(T1 - T0, axis=1).max()*1000))

if "pockets" not in STEPS:
    bpy.ops.wm.save_as_mainfile(filepath=out); raise SystemExit(0)
# 3: pockets ----------------------------------------------------------------------------------------------------
kd = kdtree.KDTree(len(J1))
for i, p in enumerate(J1): kd.insert(Vector(p), i)
kd.balance()
def surf(az, z):
    d = Vector((math.sin(math.radians(az)), -math.cos(math.radians(az)), 0)); h = jt.ray_cast(Vector((0, 0, z)) + d*0.4, -d, 0.4)
    return (np.array(h[0]), np.array(h[1])) if h[0] is not None else (None, None)
bm = bmesh.new()
POCKETS = [(-45.0, 0.548), (45.0, 0.548)]                                    # azimuth (deg), centre height (m)
PW, PH, NU, NV = 26.0, 0.070, 14, 12                                         # width in degrees, height, grid
for az0, z0 in POCKETS:
    for layer, lift in (("patch", 0.0026), ("flap", 0.0042)):
        zt = z0 + PH/2; zb = (z0 + PH/2 - 0.020) if layer == "flap" else (z0 - PH/2)
        grid = []
        for j in range(NV + 1):
            z = zb + (zt - zb)*j/NV; row = []
            for k in range(NU + 1):
                u = -1 + 2*k/NU; az = az0 + 0.5*PW*u*(1.04 if layer == "flap" else 1.0)
                p, n = surf(az, z)
                v_ = (j/NV)*2 - 1
                round_ = (1 - abs(u)**6)*(1 - abs(v_)**6) if layer == "patch" else (1 - abs(u)**6)
                row.append(bm.verts.new(tuple(p + n*lift*(0.35 + 0.65*round_))))
            grid.append(row)
        for j in range(NV):
            for k in range(NU): bm.faces.new((grid[j][k], grid[j][k+1], grid[j+1][k+1], grid[j+1][k]))
pm = bpy.data.meshes.new("SCULPT_JACKET_POCKETS"); bm.to_mesh(pm); bm.free()
po = bpy.data.objects.new("SCULPT_JACKET_POCKETS", pm); jk.users_collection[0].objects.link(po)
md = po.modifiers.new("thick", 'SOLIDIFY'); md.thickness = 0.0022; md.offset = -1.0; md.use_rim = True
for o in bpy.context.view_layer.objects: o.select_set(o is po)
bpy.context.view_layer.objects.active = po; bpy.ops.object.modifier_apply(modifier="thick")
for p_ in pm.polygons: p_.use_smooth = True
pm.materials.append(jk.data.materials[0])
for g in jk.vertex_groups: po.vertex_groups.new(name=g.name)
for v in pm.vertices:
    acc = {}; tot = 0.0
    for _, i, d in kd.find_n(v.co, 6):
        w_ = 1.0/max(d, 1e-4); tot += w_
        for g in jk.data.vertices[i].groups: acc[g.group] = acc.get(g.group, 0.0) + w_*g.weight
    top = [gw for gw in sorted(acc.items(), key=lambda gw: -gw[1])[:4] if gw[1]/tot >= 0.01]; s_ = sum(x for _, x in top)
    for g, x in top: po.vertex_groups[g].add([v.index], x/s_, 'REPLACE')
po.modifiers.new("Armature", 'ARMATURE').object = rig
print("POCKETS verts %d tris %d" % (len(pm.vertices), sum(len(p.vertices) - 2 for p in pm.polygons)))

# 4: neck ---------------------------------------------------------------------------------------------------------
sm = bpy.data.materials["SCULPT_MAT_SCARF"]; b_ = [n for n in sm.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'][0]
old = tuple(round(x, 3) for x in b_.inputs["Base Color"].default_value[:3])
b_.inputs["Base Color"].default_value = (0.200, 0.112, 0.058, 1.0)         # warm shirt-like brown (sRGB about 124, 93, 67)
print("NECK scarf base colour %s -> %s" % (old, (0.200, 0.112, 0.058)))
bpy.ops.wm.save_as_mainfile(filepath=out)
