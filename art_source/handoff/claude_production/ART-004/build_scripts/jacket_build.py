# ART-004 jacket candidate v003 (method A, accepted by Codex at 94cb54b): torso and sleeves, plus a soft front and
# cuff trim, on working copies of the frozen body's jacket and seam-binding faces. Hem at the original height, exact
# original weights, no side vents; cuff rolls back at the original ring radius with the sleeve seated into them.
# (v001 is in Git history at 43144e9, v002 at c1cd411.)
# blender -b <collar_packet_v002.blend> --python jacket_build.py -- <absolute out.blend>
# PROTECTED_BODY, SimmRig, the actions, the head and the collar are read, never written.
# Contract: no vertex is added, merged or re-weighted. Every candidate vertex is one original jacket vertex,
# moved. Its original index is stored in the integer attribute "orig_index".
import bpy, bmesh, sys, numpy as np
sys.dont_write_bytecode = True
out = sys.argv[sys.argv.index("--")+1]
JACKET_MAT = "Simm golden canvas jacket.001"
src = bpy.data.objects["PROTECTED_BODY"]; rig = bpy.data.objects["SimmRig"]

# ---- working copy: jacket-material faces only --------------------------------------------------------------
me = src.data.copy(); me.name = "SCULPT_JACKET"
ob = bpy.data.objects.new("SCULPT_JACKET", me)
col = bpy.data.collections.get("20_SCULPT_BODY_PARTS") or bpy.data.collections.new("20_SCULPT_BODY_PARTS")
if col.name not in [c.name for c in bpy.context.scene.collection.children]: bpy.context.scene.collection.children.link(col)
col.objects.link(ob)
# vertex group names live on the mesh datablock, so the copy already carries them in the original order
assert [g.name for g in ob.vertex_groups] == [g.name for g in src.vertex_groups]
oi = me.attributes.new("orig_index", 'INT', 'POINT')
oi.data.foreach_set("value", list(range(len(me.vertices))))
mi = [i for i, m in enumerate(me.materials) if m and m.name == JACKET_MAT][0]
bm = bmesh.new(); bm.from_mesh(me)
bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.material_index != mi], context='FACES')
bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
bm.verts.ensure_lookup_table(); bm.verts.index_update()

# ---- islands: torso, left sleeve, right sleeve --------------------------------------------------------------
seen = set(); islands = []
for v in bm.verts:
    if v.index in seen: continue
    st = [v]; comp = []; seen.add(v.index)
    while st:
        a = st.pop(); comp.append(a)
        for e in a.link_edges:
            b = e.other_vert(a)
            if b.index not in seen: seen.add(b.index); st.append(b)
    islands.append(comp)
islands.sort(key=lambda c: -len(c))
assert len(islands) == 3, [len(c) for c in islands]
torso = islands[0]; sleeves = islands[1:]
print("JACKET islands", [len(c) for c in islands])

def smooth1d(y, k=2):
    y = np.asarray(y, float)
    for _ in range(k): y = np.convolve(np.pad(y, 1, mode='edge'), [0.25, 0.5, 0.25], mode='valid')
    return y
def superscale(u, v, n):
    m = max(abs(u), abs(v)); e = (abs(u)**n + abs(v)**n) ** (1.0/n)
    return m / e if e > 1e-9 else 1.0
sstep = lambda t: 0.0 if t <= 0 else 1.0 if t >= 1 else t*t*(3-2*t)

# ---- torso: box cross-section to a soft rounded one, a belly, a tucked and slightly longer hem --------------
T_N, T_PUFF, HEM_DROP, HEM_FROM = 3.0, 0.085, 0.0, 0.690      # v003: hem not lowered (v002 dropped it 42 mm)
co = np.array([v.co[:] for v in torso]); z0, z1 = co[:, 2].min(), co[:, 2].max()
NB = 14; edges = np.linspace(z0, z1, NB+1); zc = 0.5*(edges[:-1]+edges[1:])
a = np.zeros(NB); b = np.zeros(NB); cy = np.zeros(NB)
for i in range(NB):
    m = (co[:, 2] >= edges[i]-0.012) & (co[:, 2] <= edges[i+1]+0.012)
    a[i] = np.abs(co[m, 0]).max(); cy[i] = 0.5*(co[m, 1].max()+co[m, 1].min()); b[i] = 0.5*(co[m, 1].max()-co[m, 1].min())
a, b, cy = smooth1d(a), smooth1d(b), smooth1d(cy)
print("TORSO z %.3f..%.3f half-width %.3f..%.3f half-depth %.3f..%.3f" % (z0, z1, a.min(), a.max(), b.min(), b.max()))
for v in torso:
    x, y, z = v.co; t = (z - z0)/(z1 - z0)
    A, B, CY = np.interp(z, zc, a), np.interp(z, zc, b), np.interp(z, zc, cy)
    s = superscale(x/A, (y-CY)/B, T_N)
    k = 1.0 - 0.75*sstep((t-0.80)/0.20)                    # hold the neckline: the collar roots are buried there
    s = 1.0 + (s - 1.0)*k
    puff = 1.0 + T_PUFF*np.sin(np.pi*min(1.0, max(0.0, (t+0.10)/0.98)))**0.8 * k - 0.012*(1.0-t)**4
    x, y = x*s*puff, CY + (y-CY)*s*puff
    # shoulders slope a little instead of ending in a box corner
    w = sstep((t-0.66)/0.34)
    if abs(x) > 0.13:                                       # only outside the pack straps, which are frozen and stay put
        z -= 0.026*w*sstep((abs(x)-0.13)/0.07)
        x = np.sign(x)*(0.13 + (abs(x)-0.13)*(1.0 - 0.35*w*w))
    if z < HEM_FROM: z -= HEM_DROP*((HEM_FROM - z)/(HEM_FROM - z0))**1.5
    v.co = (x, y, z)

# ---- sleeves: box tube to a soft round tube, fuller upper arm, gathered cuff --------------------------------
S_PUFF = 1.13
for isl in sleeves:
    co = np.array([v.co[:] for v in isl]); c = co.mean(0)
    w_, vec = np.linalg.eigh(np.cov((co-c).T)); ax = vec[:, 2]
    if ax[2] > 0: ax = -ax                                   # axis runs shoulder to cuff, downward
    e1 = np.array([0.0, 1.0, 0.0]); e1 -= ax*e1.dot(ax); e1 /= np.linalg.norm(e1); e2 = np.cross(ax, e1)
    tt = (co-c) @ ax; t0, t1 = tt.min(), tt.max(); p1 = (co-c) @ e1; p2 = (co-c) @ e2
    NB = 10; ed = np.linspace(t0, t1, NB+1); tc = 0.5*(ed[:-1]+ed[1:]); c1 = np.zeros(NB); c2 = np.zeros(NB); a1 = np.zeros(NB); a2 = np.zeros(NB)
    for i in range(NB):
        m = (tt >= ed[i]-0.01) & (tt <= ed[i+1]+0.01)
        c1[i] = 0.5*(p1[m].max()+p1[m].min()); a1[i] = 0.5*(p1[m].max()-p1[m].min())
        c2[i] = 0.5*(p2[m].max()+p2[m].min()); a2[i] = 0.5*(p2[m].max()-p2[m].min())
    c1, c2, a1, a2 = smooth1d(c1), smooth1d(c2), smooth1d(a1), smooth1d(a2)
    print("SLEEVE side %+d length %.3f half-extents %.3f..%.3f / %.3f..%.3f" % (np.sign(c[0]), t1-t0, a1.min(), a1.max(), a2.min(), a2.max()))
    for v, T, q1, q2 in zip(isl, tt, p1, p2):
        t = (T - t0)/(t1 - t0)
        C1, C2, A1, A2 = np.interp(T, tc, c1), np.interp(T, tc, c2), np.interp(T, tc, a1), np.interp(T, tc, a2)
        s = superscale((q1-C1)/A1, (q2-C2)/A2, 2.0)
        k = sstep(t/0.22)                                    # the shoulder end stays put inside the torso
        f = 1.0 + (s*(S_PUFF + 0.07*np.sin(np.pi*t)) - 1.0)*k
        # v003: no flare and no gather at the end; the end is seated into the original cuff ring below
        n1, n2 = C1 + (q1-C1)*f, C2 + (q2-C2)*f
        v.co = c + ax*T + e1*n1 + e2*n2

# ---- light relax so old panel creases read as cloth, borders held -------------------------------------------
for _ in range(3):
    new = {}
    for v in bm.verts:
        if v.is_boundary or len(v.link_edges) < 3: continue
        avg = sum((e.other_vert(v).co for e in v.link_edges), v.co*0) / len(v.link_edges)
        new[v] = v.co.lerp(avg, 0.35)
    for v, p in new.items(): v.co = p
# ---- keep the cloth outside what it covers: trousers, shirt and skin of the frozen body (read only) ----------
from mathutils import Vector
from mathutils.bvhtree import BVHTree
UNDER = ("Simm charcoal olive trousers", "Simm warm dark undershirt.001", "Simm warm skin")
keep = [i for i, m in enumerate(src.data.materials) if m and m.name in UNDER]
under = BVHTree.FromPolygons([v.co.copy() for v in src.data.vertices], [tuple(p.vertices) for p in src.data.polygons if p.material_index in keep])
keep_t = [i for i, m in enumerate(src.data.materials) if m and m.name in UNDER[:2]]      # torso: trousers and shirt, not the hands
under_t = BVHTree.FromPolygons([v.co.copy() for v in src.data.vertices], [tuple(p.vertices) for p in src.data.polygons if p.material_index in keep_t])
# Torso: one smooth horizontal scale field, so the hem stays an even line instead of following every trouser detail.
CLEAR = 0.009; need = {}
for v in torso:
    x, y, z = v.co; CY = float(np.interp(min(max(z, zc[0]), zc[-1]), zc, cy)); d = Vector((x, y - CY, 0.0)); r = d.length
    if r < 1e-5: need[v] = 1.0; continue
    d /= r; hit = under_t.ray_cast(Vector((0.0, CY, z)) + d*0.6, -d, 0.6)
    rh = 0.6 - hit[3] if hit[0] is not None else 0.0
    need[v] = min(1.22, max(1.0, (rh + CLEAR)/r))
for _ in range(6):
    nxt = {}
    for v in torso:
        nb = [need[e.other_vert(v)] for e in v.link_edges]
        nxt[v] = max(need[v], 0.5*need[v] + 0.5*sum(nb)/len(nb)) if nb else need[v]
    need = nxt
for v in torso:
    CY = float(np.interp(min(max(v.co.z, zc[0]), zc[-1]), zc, cy)); f = need[v]
    v.co.x *= f; v.co.y = CY + (v.co.y - CY)*f
print("TORSO vertices scaled out to clear trousers and shirt: %d, largest factor %.3f" % (sum(1 for f in need.values() if f > 1.001), max(need.values())))
# The frozen pack straps lie on the old box-shaped chest. Bring the cloth back out under them so they do not hover.
ON = ("Simm olive canvas", "Simm woven olive straps", "Simm canvas seams")
on_i = [i for i, m in enumerate(src.data.materials) if m and m.name in ON]
straps = BVHTree.FromPolygons([v.co.copy() for v in src.data.vertices], [tuple(p.vertices) for p in src.data.polygons if p.material_index in on_i])
want = {}
for v in torso:
    x, y, z = v.co; CY = float(np.interp(min(max(z, zc[0]), zc[-1]), zc, cy)); d = Vector((x, y - CY, 0.0)); r = d.length; want[v] = 1.0
    if r < 1e-5: continue
    d /= r; loc, nrm, idx, dist = straps.find_nearest(v.co, 0.035)
    if loc is None: continue
    g = (loc - v.co).dot(d)
    if g > 0.003 and g > 0.6*dist: want[v] = min(1.15, (r + g - 0.002)/r)
for _ in range(4):
    want = {v: max(want[v], 0.5*want[v] + 0.5*sum(want[e.other_vert(v)] for e in v.link_edges)/max(1, len(v.link_edges))) for v in torso}
for v in torso:
    CY = float(np.interp(min(max(v.co.z, zc[0]), zc[-1]), zc, cy)); f = want[v]
    v.co.x *= f; v.co.y = CY + (v.co.y - CY)*f
print("TORSO vertices brought out under the frozen straps and pack: %d, largest factor %.3f" % (sum(1 for f in want.values() if f > 1.002), max(want.values())))
# ======================= v002 corrections, after Codex's native review of v001 =================================
import math
from mathutils.kdtree import KDTree
lay = bm.verts.layers.int["orig_index"]
orig = lambda v: src.data.vertices[v[lay]].co
cyz = lambda z: float(np.interp(min(max(z, zc[0]), zc[-1]), zc, cy))

# A. Strap contact in 3D. Each frozen strap or pack vertex that lay within 12 mm of the old jacket should sit at
#    the same height above the new cloth. The cloth is lifted under it with a smooth falloff; the strap is not moved.
old_jacket = BVHTree.FromPolygons([v.co.copy() for v in src.data.vertices], [tuple(p.vertices) for p in src.data.polygons if p.material_index == mi])
sv = set()
for p in src.data.polygons:
    if p.material_index in on_i: sv.update(p.vertices)
rest_gap = []
for k in sv:
    c = src.data.vertices[k].co; lo = old_jacket.find_nearest(c, 0.012)
    if lo[0] is not None: rest_gap.append((c.copy(), lo[3]))
for it in range(5):
    cur = BVHTree.FromBMesh(bm); recs = []
    for c, d_old in rest_gap:
        loc, nrm, idx, d = cur.find_nearest(c, 0.06)
        if loc is None: continue
        ex = (d if (c - loc).dot(nrm) >= 0 else -d) - d_old
        if ex > 0.0015: recs.append((loc.copy(), (c - loc).normalized(), ex))
    if not recs: break
    kd = KDTree(len(recs))
    for i, r in enumerate(recs): kd.insert(r[0], i)
    kd.balance()
    for v in torso:
        bw = 0.0; best = None
        for co_, i, dist in kd.find_range(v.co, 0.04):
            w = recs[i][2]*(1.0 - dist/0.04)**2
            if w > bw: bw = w; best = recs[i][1]
        if best is not None: v.co += best*bw*0.9
print("TORSO strap contact passes: %d, strap and pack vertices tracked: %d, still more than 1.5 mm high after the last pass: %d" % (it + 1, len(rest_gap), len(recs)))

# B. Gathered, sewn hem. In v001 the hem flared 2 to 3 cm past the old line at the hips, the right hand went into
#    it in the gather clip, and its outline followed every trouser detail. Here the bottom band is drawn to one
#    smooth outline: the trousers' outer envelope by angle, widened and low-passed, plus 11 mm of air. The hem is
#    not lowered.
NBIN = 72; SIDE_LIFT = 0.010; req = np.zeros(NBIN); band = []   # v003: at most a 10 mm rise, a curve, not a vent (v002: up to 80 mm)
for v in torso:
    if v.co.z > 0.645: continue
    CY = cyz(v.co.z); d = Vector((v.co.x, v.co.y - CY, 0.0)); r = d.length
    if r < 1e-5: continue
    d /= r; th = math.atan2(d.y, d.x); k = int((th + math.pi)/(2*math.pi)*NBIN) % NBIN
    hit = under_t.ray_cast(Vector((0.0, CY, v.co.z)) + d*0.6, -d, 0.6)
    if hit[0] is not None: req[k] = max(req[k], 0.6 - hit[3] + 0.011)
    band.append((v, CY, r, th))
import json, os
sweep = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "jacket_hand_sweep.json")))
# v002 widened the outline for the thighs' swing here. v003 keeps the measurement for the log but does not widen.
zb0 = min(v.co.z for v, CY, r, th in band) - 0.004; swr = np.zeros(NBIN)
for x, y, z in sweep["hips_trousers"]:
    if z < zb0 or z > 0.645: continue
    k = int((math.atan2(y - cyz(z), x) + math.pi)/(2*math.pi)*NBIN) % NBIN
    swr[k] = max(swr[k], math.hypot(x, y - cyz(z)))
rest_req = req.copy()          # v003: no widening for the thigh swing; at the original hem height it is not needed
print("TORSO hem outline widened for the thighs' swing in %d of %d directions, by up to %.1f mm" % (int((req > rest_req + 1e-6).sum()), NBIN, (req - rest_req).max()*1000))
if (req == 0).any():                                       # empty bins take their neighbours' value
    idx = np.arange(NBIN); good = req > 0; req = np.interp(idx, idx[good], req[good], period=NBIN)
env = np.maximum.reduce([np.roll(req, sft) for sft in (-2, -1, 0, 1, 2)])
for _ in range(4): env = 0.25*np.roll(env, 1) + 0.5*env + 0.25*np.roll(env, -1)
env = np.maximum(env, req)
# The hands' measured travel (jacket_hand_sweep.json, hips rest space) caps the outline: 6 mm of air to the hand
# where that is possible, never closer than 2 mm to the trousers.
zlo = min(v.co.z for v, CY, r, th in band) - 0.012; hmin = np.full(NBIN, 9.0)
for x, y, z in sweep["hips"]:
    if z < zlo or z > 0.660: continue
    th = math.atan2(y - cyz(z), x); k = int((th + math.pi)/(2*math.pi)*NBIN) % NBIN
    hmin[k] = min(hmin[k], math.hypot(x, y - cyz(z)))
hmin = np.minimum.reduce([np.roll(hmin, sft) for sft in (-1, 0, 1)])
# Where the swinging thigh and the hand leave less than 6 mm for cloth, there is no outline that clears both.
# There the thigh wins (a trouser corner through the hem shows in every walk cycle) and the hem is lifted,
# out of the hand's way, as a side vent. The lift is computed further down from how high the hand reaches.
room = (hmin - 0.006) - (req - 0.011 + 0.004)
cap = np.maximum(hmin - 0.006, req - 0.011 + 0.004); capped = int((cap < env).sum()); env = np.minimum(env, cap)
for _ in range(2): env = np.minimum(0.25*np.roll(env, 1) + 0.5*env + 0.25*np.roll(env, -1), cap)
# How high the hand reaches inside the cloth's radius, per direction: the hem is lifted to just above that.
hz = np.zeros(NBIN)
for x, y, z in sweep["hips"]:
    if z < zlo or z > 0.660: continue
    k = int((math.atan2(y - cyz(z), x) + math.pi)/(2*math.pi)*NBIN) % NBIN
    if math.hypot(x, y - cyz(z)) < env[k] + 0.006: hz[k] = max(hz[k], z)
need_lift = np.where(hz > 0, np.clip(hz + 0.006 - zb0, 0.0, SIDE_LIFT), 0.0)
lift = np.maximum.reduce([np.roll(need_lift, sft) for sft in (-1, 0, 1)])
for _ in range(2): lift = np.maximum(0.25*np.roll(lift, 1) + 0.5*lift + 0.25*np.roll(lift, -1), need_lift)
print("TORSO hem outline capped by the hand sweep in %d of %d directions; directions with under 6 mm of room between swinging thigh and hand: %d; hem lifted in %d directions, by up to %.0f mm" % (capped, NBIN, int((room < 0.006).sum()), int((lift > 0.001).sum()), lift.max()*1000))
for v, CY, r, th in band:
    u = (th + math.pi)/(2*math.pi)*NBIN - 0.5; k0 = int(math.floor(u)) % NBIN; fr_ = u - math.floor(u)
    target = env[k0]*(1-fr_) + env[(k0+1) % NBIN]*fr_
    w = sstep((0.645 - v.co.z)/0.055); f = (r + (target - r)*w)/r
    v.co.x *= f; v.co.y = CY + (v.co.y - CY)*f
    lw = lift[k0]*(1-fr_) + lift[(k0+1) % NBIN]*fr_
    if lw > 0.0: v.co.z += lw*max(0.0, (0.660 - v.co.z)/(0.660 - zb0))
inside = 0; nearest = 9.0
for v, CY, r, th in band:
    loc, nrm, idx_, dd = under_t.find_nearest(v.co, 0.05)
    if loc is None: continue
    sd_ = dd if (v.co - loc).dot(nrm) >= 0 else -dd
    nearest = min(nearest, sd_); inside += sd_ < 0
print("TORSO hem band: %d vertices on one smooth outline, radius %.3f to %.3f m; closest to the trousers %.1f mm; inside the trousers: %d" % (len(band), env.min(), env.max(), nearest*1000, inside))
# v003, local hand tuck. In `gather` the clip presses the right hand into the hip (the frozen trousers already take
# up to 4.4 mm there), while the original jacket never met the hand. The rounded hem bulges 1 to 2 cm further out at
# that spot. Hem-band vertices are 100 percent on `hips`, so their rest position is also their position in hips
# space, where the hands' measured travel is stored. Each one within 8 mm of that path is blended back to its
# original, contact-free position; the blend fades out over 30 mm and nowhere else is touched.
hp = np.array(sweep["hips"]); kd_h = KDTree(len(hp))
for i, p_ in enumerate(hp): kd_h.insert(Vector(p_), i)
kd_h.balance(); seeds = [v for v in torso if v.co.z < 0.66 and kd_h.find(v.co)[2] < 0.008]
moved = 0
if seeds:
    kd_s = KDTree(len(seeds))
    for i, v in enumerate(seeds): kd_s.insert(v.co.copy(), i)
    kd_s.balance(); blend = {}
    for v in torso:
        if v.co.z > 0.70: continue
        c_, i, dist = kd_s.find(v.co)
        if dist < 0.030: blend[v] = sstep(1.0 - dist/0.030)
    for v, w in blend.items(): v.co = v.co.lerp(orig(v), w)
    moved = len(blend)
print("TORSO hand tuck: %d hem vertices within 8 mm of the hands' measured path; %d vertices blended back toward their original positions" % (len(seeds), moved))
cuff_fit = {}
for isl in sleeves:
    co_ = np.array([v.co[:] for v in isl]); zmin = co_[:, 2].min(); end = co_[co_[:, 2] < zmin + 0.012]
    cxy = end[:, :2].mean(0); cuff_fit[int(np.sign(cxy[0]))] = (float(cxy[0]), float(cxy[1]), float(zmin), float(np.hypot(end[:, 0]-cxy[0], end[:, 1]-cxy[1]).mean()))
# ======================= end of v002 torso corrections ==========================================================
# v003: seat each sleeve end into the original cuff ring. The ring stays at its original radius and height
# (mean radius about 47 mm, inner about 41 mm, Z 0.644 to 0.655). The last few centimetres of the sleeve are drawn
# to a radius 2.5 mm larger than the ring's inner radius, so the sleeve edge runs into the roll and the roll reads
# as the turned-back edge of the same cloth.
bind_i = [i for i, m in enumerate(src.data.materials) if m and m.name == "Simm golden seam binding.001"][0]
ring_v = {}
for p in src.data.polygons:
    if p.material_index == bind_i:
        for k in p.vertices:
            c = src.data.vertices[k].co
            if abs(c.x) > 0.19 and c.z < 0.66: ring_v[k] = c.copy()
seat = {}
for sd in (-1, 1):
    rc = np.array([c[:] for k, c in ring_v.items() if np.sign(c.x) == sd]); ctr = rc.mean(0)
    rr = np.hypot(rc[:, 0]-ctr[0], rc[:, 1]-ctr[1]); seat[sd] = (ctr, float(rr.min()), float(rr.max()), float(rc[:, 2].min()), float(rc[:, 2].max()))
    print("CUFF ring side %+d: centre (%.4f, %.4f, %.4f), radius %.1f to %.1f mm, Z %.3f to %.3f" % (sd, ctr[0], ctr[1], ctr[2], rr.min()*1000, rr.max()*1000, rc[:, 2].min(), rc[:, 2].max()))
for isl in sleeves:
    sd = 1 if sum(v.co.x for v in isl) > 0 else -1; ctr, rin, rout, zlo, zhi = seat[sd]
    target = rin + 0.0025
    for v in isl:
        oz = src.data.vertices[v[lay]].co.z                    # original height: the sleeve end is the lowest original row
        w = sstep((zhi + 0.035 - oz)/0.035)
        if w <= 0.0: continue
        dx, dy = v.co.x - ctr[0], v.co.y - ctr[1]; r = math.hypot(dx, dy)
        if r < 1e-6: continue
        f = (r + (target - r)*w)/r
        v.co.x = ctr[0] + dx*f; v.co.y = ctr[1] + dy*f
        if oz < zhi + 0.004: v.co.z = min(v.co.z, ctr[2] + 0.001)   # the end row sits in the middle of the roll
pushed = 0
for isl, clear in ((sleeves[0], 0.004), (sleeves[1], 0.004)):
    for v in isl:
        loc, nrm, idx, d = under.find_nearest(v.co, 0.05)
        if loc is None: continue
        if (v.co - loc).dot(nrm) < clear: v.co = loc + nrm*clear; pushed += 1
print("SLEEVE vertices pushed clear of skin:", pushed)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
for f in bm.faces: f.smooth = True
bm.to_mesh(me); bm.free(); me.update()

# ---- one flat material in the held jacket colour; original UV layers are kept --------------------------------
mat = bpy.data.materials.get("SCULPT_MAT_JACKET") or bpy.data.materials.new("SCULPT_MAT_JACKET")
mat.use_nodes = True; bs = mat.node_tree.nodes["Principled BSDF"]
bs.inputs["Base Color"].default_value = (0.723, 0.381, 0.027, 1.0)       # the frozen jacket material's own base value
bs.inputs["Roughness"].default_value = 0.86; bs.inputs["Specular"].default_value = 0.2
me.materials.clear(); me.materials.append(mat)
for p in me.polygons: p.material_index = 0
md = ob.modifiers.new("Armature", 'ARMATURE'); md.object = rig        # reads the rig, does not edit it
print("JACKET verts %d tris %d" % (len(me.vertices), sum(len(p.vertices)-2 for p in me.polygons)))

# ---- v002 trim: the original front placket strips and cuff rings, reshaped into soft rolled edges -------------
# Same contract as the jacket: original vertices moved, original groups and weights (plackets 100 percent spine,
# cuffs 100 percent forearm). The pocket strips and the two-triangle end fragments are left out.
import math
BIND_MAT = "Simm golden seam binding.001"
tme = src.data.copy(); tme.name = "SCULPT_JACKET_TRIM"; tob = bpy.data.objects.new("SCULPT_JACKET_TRIM", tme); col.objects.link(tob)
ta = tme.attributes.new("orig_index", 'INT', 'POINT'); ta.data.foreach_set("value", list(range(len(tme.vertices))))
bi = [i for i, m in enumerate(tme.materials) if m and m.name == BIND_MAT][0]
tb = bmesh.new(); tb.from_mesh(tme)
bmesh.ops.delete(tb, geom=[f for f in tb.faces if f.material_index != bi], context='FACES')
bmesh.ops.delete(tb, geom=[v for v in tb.verts if not v.link_faces], context='VERTS')
tb.verts.ensure_lookup_table(); tb.verts.index_update()
seen = set(); tis = []
for v in tb.verts:
    if v.index in seen: continue
    st = [v]; comp = []; seen.add(v.index)
    while st:
        a_ = st.pop(); comp.append(a_)
        for e in a_.link_edges:
            b_ = e.other_vert(a_)
            if b_.index not in seen: seen.add(b_.index); st.append(b_)
    tis.append(comp)
cuffs = [c for c in tis if len(c) == 726]; plackets = [c for c in tis if len(c) == 96]
assert len(cuffs) == 2 and len(plackets) == 2, [len(c) for c in tis]
dropped = [c for c in tis if len(c) not in (726, 96)]
print("TRIM kept: 2 cuff rings, 2 placket strips. Left out: %d islands, %d vertices (pocket strips and end fragments)" % (len(dropped), sum(len(c) for c in dropped)))
jt = BVHTree.FromPolygons([v.co.copy() for v in me.vertices], [tuple(p.vertices) for p in me.polygons])
hem_z = min(v.co.z for v in me.vertices if abs(v.co.x) < 0.12 and v.co.y < 0)
def front_edge(sd, z):                                    # innermost point of the jacket front at this height
    for k in range(70):
        x = sd*(0.016 + 0.002*k); h = jt.ray_cast(Vector((x, -0.5, z)), Vector((0, 1, 0)), 0.9)
        if h[0] is not None and h[0].y < -0.02: return x, h[0].y
    return None
RHO = 0.0075; BTN_Z, BTN_X, BTN_BACK = 0.876, 0.047, -0.1378      # frozen brass button: centre height, centre X, back face Y
for comp in plackets:
    sd = 1.0 if sum(v.co.x for v in comp) > 0 else -1.0
    zs = np.linspace(hem_z + 0.006, 0.966, 28); ex = []; ey = []
    for z in zs:
        e = front_edge(sd, z)
        if e is None: e = (ex[-1], ey[-1]) if ex else (sd*0.05, -0.12)
        ex.append(e[0]); ey.append(e[1])
    ex, ey = smooth1d(ex, 3), smooth1d(ey, 3)
    levels = []; srt = sorted(comp, key=lambda v: v.co.z)
    for v in srt:
        if levels and v.co.z - levels[-1][-1].co.z < 0.004: levels[-1].append(v)
        else: levels.append([v])
    for li, lv in enumerate(levels):
        zo = sum(v.co.z for v in lv)/len(lv); z = zo
        z = max(z, hem_z + 0.006)                         # the strip keeps its original height: it ends above the gathered hem band
        xc = float(np.interp(z, zs, ex)) - sd*0.003; yc = float(np.interp(z, zs, ey)) + 0.002
        b = math.exp(-((z - BTN_Z)/0.038)**2)             # the roll comes forward to seat the button, both sides alike
        xc += (sd*BTN_X - xc)*b; yc += ((BTN_BACK + RHO) - yc)*b
        rho = RHO*(0.55 if li in (0, len(levels)-1) or len(lv) < 6 else 1.0)
        cx_ = sum(v.co.x for v in lv)/len(lv); cy_ = sum(v.co.y for v in lv)/len(lv)
        for v in lv:
            dx, dy = v.co.x - cx_, v.co.y - cy_; n = math.hypot(dx, dy) or 1.0
            v.co = (xc + rho*dx/n, yc + rho*dy/n, z)
# v003: the cuff rings keep their original positions exactly (v002 moved them out to about 51 mm and they floated)
bmesh.ops.delete(tb, geom=[v for c in dropped for v in c], context='VERTS')
bmesh.ops.recalc_face_normals(tb, faces=tb.faces)
for f in tb.faces: f.smooth = True
tb.to_mesh(tme); tb.free(); tme.update()
tmat = bpy.data.materials.get("SCULPT_MAT_JACKET_TRIM") or bpy.data.materials.new("SCULPT_MAT_JACKET_TRIM")
tmat.use_nodes = True; tbs = tmat.node_tree.nodes["Principled BSDF"]
tbs.inputs["Base Color"].default_value = (0.468, 0.22, 0.019, 1.0)        # the frozen seam-binding material's own base value
tbs.inputs["Roughness"].default_value = 0.86; tbs.inputs["Specular"].default_value = 0.2
tme.materials.clear(); tme.materials.append(tmat)
for p in tme.polygons: p.material_index = 0
tob.modifiers.new("Armature", 'ARMATURE').object = rig
print("TRIM verts %d tris %d" % (len(tme.vertices), sum(len(p.vertices)-2 for p in tme.polygons)))
bpy.ops.wm.save_as_mainfile(filepath=out)
