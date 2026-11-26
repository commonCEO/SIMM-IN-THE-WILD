# ART-004 jacket candidate: torso and sleeves only, on a working copy of the frozen body's jacket faces.
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
T_N, T_PUFF, HEM_DROP, HEM_FROM = 3.0, 0.085, 0.042, 0.690
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
        f *= 1.0 - 0.10*sstep((t-0.86)/0.14)                 # gathered cuff
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
bpy.ops.wm.save_as_mainfile(filepath=out)
