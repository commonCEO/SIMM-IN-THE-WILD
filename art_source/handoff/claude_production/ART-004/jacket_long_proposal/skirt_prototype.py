# ART-004 longer-jacket METHOD PROTOTYPE (Codex brief at 6a7da65). Throwaway clay; no export.
# blender -b <file with jacket v003, e.g. work/boot_candidate_v002.blend> --python skirt_prototype.py -- <absolute out.blend> [W]
# Adds SCULPT_JACKET_SKIRT: a new lower jacket panel on its own topology (open at the front), tucked up inside the jacket
# v003 hem and carried down to Z 0.48. Its rows blend from 100 percent `hips` at the top to a share of the same-side
# thigh at the hem (W, default 0.6), so the lower panel follows the legs. Jacket v003 itself, PROTECTED_BODY, the rig,
# the rest pose, the actions and the socket are not changed.
import bpy, bmesh, sys, math, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode = True
argv = sys.argv[sys.argv.index("--")+1:]; out = argv[0]; WMAX = float(argv[1]) if len(argv) > 1 else 0.6
rig = bpy.data.objects["SimmRig"]; bd = bpy.data.objects["PROTECTED_BODY"]; jk = bpy.data.objects["SCULPT_JACKET"]
sstep = lambda t: 0.0 if t <= 0 else 1.0 if t >= 1 else t*t*(3-2*t)
Z_TOP, Z_JOIN, Z_HEM = 0.665, 0.655, 0.480        # hidden top inside the jacket, start of thigh blend, new hem
CY = 0.0
jt = BVHTree.FromPolygons([v.co.copy() for v in jk.data.vertices], [tuple(p.vertices) for p in jk.data.polygons])
mi = {m.name: i for i, m in enumerate(bd.data.materials) if m}
tro = BVHTree.FromPolygons([v.co.copy() for v in bd.data.vertices], [tuple(p.vertices) for p in bd.data.polygons if p.material_index == mi["Simm charcoal olive trousers"]])
def radial_hit(tree, az, z, rmax=0.40):
    d = Vector((math.sin(az), -math.cos(az), 0.0)); o = Vector((0.0, CY, z)) + d*rmax
    h = tree.ray_cast(o, -d, rmax)
    return (rmax - h[3]) if h[0] is not None else None
NA = 96; OPEN = math.radians(19)                   # front opening half-angle, matching jacket v003's front edges
azs = [a for a in np.linspace(-math.pi, math.pi, NA, endpoint=False) if abs(a) > OPEN]
azs = sorted(azs, key=lambda a: (a if a > 0 else a + 2*math.pi))   # from the left front edge round the back to the right
zs = list(np.linspace(Z_TOP, Z_HEM, 15))
rj = np.array([radial_hit(jt, a, 0.600) or 0.17 for a in azs])          # jacket v003 radius at its lower band
rt = {z: np.array([radial_hit(tro, a, z) or 0.10 for a in azs]) for z in zs}
for _ in range(3): rj = 0.25*np.roll(rj, 1) + 0.5*rj + 0.25*np.roll(rj, -1)
# v2: keep the panel's sides clear of the hands where they hang at rest (5 mm), never closer than 10 mm to the trousers
gn = [g.name for g in bd.vertex_groups]
hand = [bd.data.vertices[k].co for k in range(len(bd.data.vertices)) if any(gn[g.group] in ("hand_l", "hand_r") and g.weight > 0.5 for g in bd.data.vertices[k].groups)]
def hand_cap(a, z):
    best = 9.0
    for c in hand:
        if abs(c.z - z) > 0.030: continue
        aa = math.atan2(c.x, -(c.y - CY))
        if abs((aa - a + math.pi) % (2*math.pi) - math.pi) > math.radians(9): continue
        best = min(best, math.hypot(c.x, c.y - CY))
    return best - 0.005
bm = bmesh.new(); rows = []
for z in zs:
    t = sstep((Z_JOIN - z)/(Z_JOIN - Z_HEM))
    r = np.maximum(rj - 0.004 + 0.016*t, rt[z] + 0.020)   # inside the jacket at the top, flaring, 20 mm clear of the trousers
    for _ in range(2): r = 0.25*np.roll(r, 1) + 0.5*r + 0.25*np.roll(r, -1)
    r = np.maximum(np.minimum(r, np.array([hand_cap(a, z) for a in azs])), rt[z] + 0.010)
    rows.append([bm.verts.new((math.sin(a)*ri, CY - math.cos(a)*ri, z)) for a, ri in zip(azs, r)])
for i in range(len(rows)-1):
    for k in range(len(azs)-1): bm.faces.new((rows[i][k], rows[i][k+1], rows[i+1][k+1], rows[i+1][k]))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
for f in bm.faces: f.normal_flip() if f.normal.dot(f.calc_center_median() - Vector((0, CY, f.calc_center_median().z))) < 0 else None
me = bpy.data.meshes.new("SCULPT_JACKET_SKIRT"); bm.to_mesh(me); bm.free()
ob = bpy.data.objects.new("SCULPT_JACKET_SKIRT", me); bpy.context.scene.collection.objects.link(ob)
md = ob.modifiers.new("thick", 'SOLIDIFY'); md.thickness = 0.007; md.offset = -1.0
md = ob.modifiers.new("sub", 'SUBSURF'); md.levels = 1; md.render_levels = 1
for o in bpy.context.view_layer.objects: o.select_set(o is ob)
bpy.context.view_layer.objects.active = ob
bpy.ops.object.modifier_apply(modifier="thick"); bpy.ops.object.modifier_apply(modifier="sub")
for p in ob.data.polygons: p.use_smooth = True
ob.data.materials.append(jk.data.materials[0])
# weights: rows above Z_JOIN 100 percent hips; below, the thigh share rises to WMAX at the hem. Same-side thigh takes
# most of it at the sides and front; at the back centre the two thighs share it.
g = {n: ob.vertex_groups.new(name=n) for n in ("hips", "thigh_l", "thigh_r")}
for v in ob.data.vertices:
    t = (Z_JOIN - v.co.z)/(Z_JOIN - Z_HEM); w = WMAX*min(1.0, max(0.0, t))**0.7      # rises early, so the mid band follows too
    s = sstep(abs(v.co.x)/0.10); back = sstep(v.co.y/0.08)                          # 0 at the front, 1 at the back
    w *= 1.0 - 0.45*back*(1 - s)                                                    # softer at the back centre, where both thighs pull
    same, other = ("thigh_l", "thigh_r") if v.co.x < 0 else ("thigh_r", "thigh_l")
    ws, wo = w*(0.5 + 0.5*s), w*0.5*(1 - s)
    g["hips"].add([v.index], 1.0 - ws - wo, 'REPLACE')
    if ws > 0: g[same].add([v.index], ws, 'REPLACE')
    if wo > 0: g[other].add([v.index], wo, 'REPLACE')
ob.modifiers.new("Armature", 'ARMATURE').object = rig
co = np.array([v.co[:] for v in ob.data.vertices])
print("SKIRT verts %d tris %d Z %.3f..%.3f; rows %d; front opening +-%.0f deg; thigh share at the hem %.2f" % (len(co), sum(len(p.vertices)-2 for p in ob.data.polygons), co[:,2].min(), co[:,2].max(), len(zs), math.degrees(OPEN), WMAX))
bpy.ops.wm.save_as_mainfile(filepath=out)
