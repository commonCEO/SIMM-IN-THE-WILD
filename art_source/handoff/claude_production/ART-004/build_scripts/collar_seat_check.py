# Read-only: is the collar's lower edge still seated on the jacket (and pack) through the clips? Nothing is saved.
# blender -b collar_packet_v004.blend --python collar_seat_check.py      (SAMPLES=25 by default)
# For each 8-degree direction round the neck, the gap is the smallest distance from the hood's lower band to the
# seat surface (jacket v003, or the frozen pack/straps where higher). 0 means touching or overlapping; anything
# above 1 mm is reported as an air gap. The hood is carried by `chest`, the jacket by its own weights.
import bpy, os, math, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
NS = int(os.environ.get("SAMPLES", "25"))
rig = bpy.data.objects["SimmRig"]; jk = bpy.data.objects["SCULPT_JACKET"]; bd = bpy.data.objects["PROTECTED_BODY"]; hood = bpy.data.objects["SCULPT_HOOD"]
sc = bpy.context.scene; CX, CY = 0.0, 0.040
keep = [i for i, m in enumerate(bd.data.materials) if m and m.name in ("Simm olive canvas", "Simm woven olive straps", "Simm canvas seams", "Simm folded hood canvas")]
hv = [hood.matrix_world @ v.co for v in hood.data.vertices]
def trees(jv, jp, bv):
    return [BVHTree.FromPolygons(jv, jp), BVHTree.FromPolygons(bv, [tuple(p.vertices) for p in bd.data.polygons if p.material_index in keep])]
def nearest(ts, c):
    return min((t.find_nearest(c, 0.1)[3] or 9.0) for t in ts)
dg = bpy.context.evaluated_depsgraph_get()
rig.animation_data_create() if rig.animation_data is None else None
rig.animation_data.action = None
for pb in rig.pose.bones: pb.matrix_basis.identity()
sc.frame_set(0); dg = bpy.context.evaluated_depsgraph_get()
ts0 = trees([v.co.copy() for v in jk.data.vertices], [tuple(p.vertices) for p in jk.data.polygons], [v.co.copy() for v in bd.data.vertices])
d0 = np.array([nearest(ts0, c) for c in hv])
az = np.degrees(np.arctan2(np.array([c.x for c in hv]) - CX, -(np.array([c.y for c in hv]) - CY)))
band = (d0 < 0.012) & (np.abs(az) > 40)                     # the hood's lower band, on the stand, not the lapels
bins = np.round(az/8).astype(int)
ub = sorted(set(bins[band]))
def gaps(dist):
    return {b: float(dist[band & (bins == b)].min()) for b in ub}
g0 = gaps(d0)
print("SEAT rest: %d directions round the neck; largest gap %.1f mm; directions with a gap over 1 mm: %d; band vertices %d" % (len(ub), max(g0.values())*1000, sum(1 for v in g0.values() if v > 0.001), int(band.sum())))
Rc = rig.data.bones["chest"].matrix_local.copy()
for an in ("idle", "walk", "gather"):
    act = bpy.data.actions[an]; rig.animation_data.action = act; f0, f1 = act.frame_range; worst = (0.0, None, None); over = 0
    for fr in np.linspace(f0, f1, NS):
        sc.frame_set(int(fr), subframe=float(fr - int(fr))); dg = bpy.context.evaluated_depsgraph_get()
        M = rig.evaluated_get(dg).pose.bones["chest"].matrix @ Rc.inverted()
        ej = jk.evaluated_get(dg); mj = ej.to_mesh(); eb = bd.evaluated_get(dg); mb = eb.to_mesh()
        ts = trees([v.co.copy() for v in mj.vertices], [tuple(p.vertices) for p in mj.polygons], [v.co.copy() for v in mb.vertices])
        ej.to_mesh_clear(); eb.to_mesh_clear()
        dist = np.full(len(hv), 9.0); idx = np.where(band)[0]
        for i in idx: dist[i] = nearest(ts, M @ hv[i])
        g = gaps(dist); b = max(g, key=g.get)
        over = max(over, sum(1 for v in g.values() if v > 0.001))
        if g[b] > worst[0]: worst = (g[b], round(float(fr), 2), b*8)
    print("SEAT %-6s %d samples: largest gap %.1f mm at frame %s, direction %s degrees; most directions with a gap over 1 mm in one sample: %d of %d" % (an, NS, worst[0]*1000, worst[1], worst[2], over, len(ub)))
