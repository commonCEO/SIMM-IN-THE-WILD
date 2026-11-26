# Measured clearance between the chest-bound collar parts and the head-bound head and hair, sampled through the
# three clips. Read-only: the file is never saved, and the rig is only evaluated, not edited.
# blender -b collar_packet.blend --python collar_pose_clearance.py
import bpy, sys, numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode = True
rig = bpy.data.objects["SimmRig"]; sc = bpy.context.scene
dg = bpy.context.evaluated_depsgraph_get()
def mesh_data(name):
    ev = bpy.data.objects[name].evaluated_get(dg); me = ev.to_mesh()
    v = [x.co.copy() for x in me.vertices]; f = [tuple(p.vertices) for p in me.polygons]; ev.to_mesh_clear(); return v, f
head_v, head_f = mesh_data("SCULPT_HEAD"); hair_v, hair_f = mesh_data("SCULPT_HAIR")
ZCUT = 1.035
visible_f = [f for f in head_f if min(head_v[i].z for i in f) >= ZCUT]
parts = {n: [v.co.copy() for v in bpy.data.objects[n].data.vertices] for n in ("SCULPT_HOOD", "SCULPT_SCARF")}
# The pack is skinned to chest like the collar parts, so collar against pack is one rigid measurement.
bo = bpy.data.objects["PROTECTED_BODY"]; bv = [bo.matrix_world @ v.co for v in bo.data.vertices]
body = BVHTree.FromPolygons(bv, [tuple(p.vertices) for p in bo.data.polygons])
# Behind Y 0.10 the only body surface near the collar is the pack. The inside test uses the whole body mesh,
# because a cut-out patch has open edges and gives false "inside" readings.
for pn, pts in parts.items():
    back = [c for c in pts if c.y > 0.10]; ins = 0; deep = 0.0; near = 9.0
    for c in back:
        loc, nrm, idx, d = body.find_nearest(c, 0.08)
        if loc is None: continue
        if (c - loc).dot(nrm) < 0: ins += 1; deep = max(deep, d)
        else: near = min(near, d)
    print("PACK %-12s verts behind Y 0.10: %d, inside the pack surface: %d, deepest %.1f mm, nearest outside %.1f mm" % (pn, len(back), ins, deep*1000, near*1000 if near < 9 else -1))
Rc = rig.data.bones["chest"].matrix_local.copy(); Rh = rig.data.bones["head"].matrix_local.copy()
if rig.animation_data is None: rig.animation_data_create()
worst = {}
for an in ("idle", "walk", "gather"):
    act = bpy.data.actions[an]; rig.animation_data.action = act
    f0, f1 = act.frame_range; frames = np.linspace(f0, f1, 13)
    for fr in frames:
        sc.frame_set(int(fr), subframe=float(fr - int(fr))); dg = bpy.context.evaluated_depsgraph_get()
        pb = rig.evaluated_get(dg).pose.bones
        # head-bound points expressed in the chest-bound collar's frame for this pose
        M = (pb["chest"].matrix @ Rc.inverted()).inverted() @ (pb["head"].matrix @ Rh.inverted())
        hv = [M @ v for v in head_v]; hrv = [M @ v for v in hair_v]
        # The neck column (head mesh below ZCUT at rest) is left out on purpose: a scarf and a hood roll rest
        # against the neck, so they are built in contact with it. What must stay clear is the visible head.
        trees = {"jaw and chin": (BVHTree.FromPolygons(hv, visible_f), lambda l, o: o.y < 0.03),
                 "skull base": (BVHTree.FromPolygons(hv, visible_f), lambda l, o: o.y >= 0.03),
                 "hair": (BVHTree.FromPolygons(hrv, hair_f), lambda l, o: True)}
        Minv = M.inverted()
        for pn, pts in parts.items():
            for zn, (tree, test) in trees.items():
                best = 9.0
                for c in pts:
                    loc, nrm, idx, d = tree.find_nearest(c, 0.09)
                    if loc is not None and d < best and test(loc, Minv @ loc): best = d
                key = (pn, zn)
                if key not in worst or best < worst[key][0]: worst[key] = (best, an, round(float(fr), 1))
        ang = M.to_euler()
        worst.setdefault(("head vs chest rotation deg", an), [0, 0, 0])
        w = worst[("head vs chest rotation deg", an)]
        for k in range(3): w[k] = max(w[k], abs(np.degrees(ang[k])))
for k, v in worst.items():
    if k[0].startswith("head vs"): print("ROT", k[1], "max |x,y,z| deg", [round(x, 1) for x in v])
    else: print("POSECLEAR %-12s to %-20s min %5.1f mm in %s at frame %s" % (k[0], k[1], v[0]*1000 if v[0] < 9 else -1, v[1], v[2]))
