# Read-only bending check for the boot blockout. blender -b <blockout.blend> --python boot_bend_check.py  (SAMPLES=97)
# Per clip: the ankle angle (shin against foot), shaft bottom poking out through the boot foot, the boot foot's
# collar opening away from the shaft (visible gap), and trouser leg poking out through the shaft.
import bpy, os, numpy as np, math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
NS = int(os.environ.get("SAMPLES", "97"))
rig = bpy.data.objects["SimmRig"]; bd = bpy.data.objects["PROTECTED_BODY"]; sc = bpy.context.scene
tm = [i for i, m in enumerate(bd.data.materials) if m and m.name == "Simm charcoal olive trousers"][0]
DIR = Vector((0.13, 0.27, 0.95)).normalized()
def inside(tree, c):
    n = 0; o = c.copy()
    for _ in range(16):
        h = tree.ray_cast(o, DIR, 1.0)
        if h[0] is None: break
        n += 1; o = h[0] + DIR*1e-5
    return n % 2 == 1
def evald(ob, dg):
    e = ob.evaluated_get(dg); m = e.to_mesh(); v = [x.co.copy() for x in m.vertices]; f = [tuple(p.vertices) for p in m.polygons]; e.to_mesh_clear(); return v, f
if rig.animation_data is None: rig.animation_data_create()
rest = {o.name: [v.co.copy() for v in o.data.vertices] for o in bpy.data.objects if o.name.startswith("SCULPT_BOOT_")}
tv_rest = [v.co.copy() for v in bd.data.vertices]
tro_ids = set(k for p in bd.data.polygons if p.material_index == tm for k in p.vertices)
for an in ("idle", "walk", "gather"):
    act = bpy.data.actions[an]; rig.animation_data.action = act; f0, f1 = act.frame_range
    worst = {"poke": (0, 0.0, None), "gap": (0.0, None), "trousers": (0, None), "angle": (0.0, None)}
    for fr in np.linspace(f0, f1, NS):
        sc.frame_set(int(fr), subframe=float(fr - int(fr))); dg = bpy.context.evaluated_depsgraph_get()
        pb = rig.evaluated_get(dg).pose.bones
        bv, bf = evald(bd, dg); tri_t = [f for p, f in zip(bd.data.polygons, bf) if p.material_index == tm]
        for sd, tag, side in ((-1, "L", "l"), (1, "R", "r")):
            sv, sf = evald(bpy.data.objects["SCULPT_BOOT_SHAFT_" + tag], dg); fv, ff = evald(bpy.data.objects["SCULPT_BOOT_FOOT_" + tag], dg)
            st = BVHTree.FromPolygons(sv, sf); ftree = BVHTree.FromPolygons(fv, ff)
            ang = math.degrees(pb["shin_" + side].y_axis.angle(pb["foot_" + side].y_axis))
            if ang > worst["angle"][0]: worst["angle"] = (ang, round(float(fr), 2))
            # shaft bottom band (rest Z under 0.17) that should stay inside the boot foot
            rs = rest["SCULPT_BOOT_SHAFT_" + tag]; n = 0; deep = 0.0
            for c0, c in zip(rs, sv):
                if c0.z < 0.165 and not inside(ftree, c):
                    loc, nrm, i, d = ftree.find_nearest(c, 0.05)
                    if loc is not None and d > 0.001: n += 1; deep = max(deep, d)
            if n > worst["poke"][0]: worst["poke"] = (n, deep, round(float(fr), 2))
            # boot foot collar rim (rest Z over 0.150) away from the shaft surface
            rf = rest["SCULPT_BOOT_FOOT_" + tag]; g = 0.0
            for c0, c in zip(rf, fv):
                if c0.z > 0.150:
                    loc, nrm, i, d = st.find_nearest(c, 0.05)
                    if loc is not None and not inside(st, c): g = max(g, d)
            if g > worst["gap"][0]: worst["gap"] = (g, round(float(fr), 2))
            # trouser vertices of this leg between Z 0.13 and 0.29 at rest that end up outside the shaft
            nt = 0
            for k, c0 in enumerate(tv_rest):
                if k in tro_ids and 0.135 < c0.z < 0.280 and np.sign(c0.x) == sd and not inside(st, bv[k]): nt += 1
            if nt > worst["trousers"][0]: worst["trousers"] = (nt, round(float(fr), 2))
    print("BEND %-6s %d samples: max ankle angle %.1f deg at frame %s | shaft bottom out of the boot foot: %d vertices up to %.1f mm at %s | foot collar off the shaft: up to %.1f mm at %s | trouser vertices out of the shaft: %d at %s" % (an, NS, worst["angle"][0], worst["angle"][1], worst["poke"][0], worst["poke"][1]*1000, worst["poke"][2], worst["gap"][0]*1000, worst["gap"][1], worst["trousers"][0], worst["trousers"][1]))
