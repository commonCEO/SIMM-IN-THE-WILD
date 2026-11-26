# Read-only measurements for the skirt prototype, 49 samples per clip (sampled, not continuous). Nothing is saved.
#  - poke: trouser vertices in the skirt's height band that are outside the skirt shell within 30 mm of it, found by a
#    ray outward from the hips axis that does not hit the skirt (front opening excluded by distance)
#  - hand: skirt vertices inside a hand (hand-only triangles, ray parity)
#  - stretch: largest ratio of a skirt edge's posed length to its rest length (tearing shows as stretch)
import bpy, math, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
rig = bpy.data.objects["SimmRig"]; bd = bpy.data.objects["PROTECTED_BODY"]; sk = bpy.data.objects["SCULPT_JACKET_SKIRT"]; sc = bpy.context.scene
mi = {m.name: i for i, m in enumerate(bd.data.materials) if m}; gn = [g.name for g in bd.vertex_groups]
def handv(k): return any(gn[g.group] in ("hand_l", "hand_r") and g.weight > 0.5 for g in bd.data.vertices[k].groups)
hand_f = [tuple(p.vertices) for p in bd.data.polygons if p.material_index == mi["Simm warm skin"] and all(handv(k) for k in p.vertices)]
tro = sorted(set(k for p in bd.data.polygons if p.material_index == mi["Simm charcoal olive trousers"] for k in p.vertices))
zlo = min(v.co.z for v in sk.data.vertices); tro = [k for k in tro if zlo + 0.010 < bd.data.vertices[k].co.z < 0.63]
edges = [tuple(e.vertices) for e in sk.data.edges]; rest = [v.co.copy() for v in sk.data.vertices]
rl = np.array([(rest[a] - rest[b]).length for a, b in edges])
DIR = Vector((0.13, 0.27, 0.95)).normalized()
def inside(t, c):
    n = 0; o = c.copy()
    for _ in range(16):
        h = t.ray_cast(o, DIR, 1.0)
        if h[0] is None: break
        n += 1; o = h[0] + DIR*1e-5
    return n % 2 == 1
if rig.animation_data is None: rig.animation_data_create()
import os
CLIPS = os.environ.get("CLIPS", "idle,walk,gather").split(",")
for an in CLIPS:
    act = bpy.data.actions[an]; rig.animation_data.action = act; f0, f1 = act.frame_range; W = {"poke": (0, 0.0, None), "hand": (0, None), "stretch": (0.0, None)}
    for fr in np.linspace(f0, f1, 49):
        sc.frame_set(int(fr), subframe=float(fr - int(fr))); dg = bpy.context.evaluated_depsgraph_get()
        eb = bd.evaluated_get(dg); mb = eb.to_mesh(); bv = [v.co.copy() for v in mb.vertices]; eb.to_mesh_clear()
        es = sk.evaluated_get(dg); ms = es.to_mesh(); sv = [v.co.copy() for v in ms.vertices]; sf = [tuple(p.vertices) for p in ms.polygons]; es.to_mesh_clear()
        st = BVHTree.FromPolygons(sv, sf); H = rig.evaluated_get(dg).pose.bones["hips"].matrix
        axis_o = H.translation; up = (H.to_3x3() @ Vector((0, 1, 0))).normalized()
        n = 0; far = 0.0
        for k in tro:
            p = bv[k]; rel = p - axis_o; rad = rel - up*rel.dot(up)
            if rad.length < 1e-4: continue
            d = rad.normalized(); h = st.ray_cast(p + d*0.0005, d, 0.25)
            if h[0] is None:
                near = st.find_nearest(p, 0.03)
                if near[0] is not None: n += 1; far = max(far, near[3])
        if n > W["poke"][0]: W["poke"] = (n, far, round(float(fr), 2))
        ht = BVHTree.FromPolygons(bv, hand_f); nh = sum(1 for c in sv if inside(ht, c) and (ht.find_nearest(c, 0.05)[3] or 0) > 0.001)
        if nh > W["hand"][0]: W["hand"] = (nh, round(float(fr), 2))
        pl = np.array([(sv[a] - sv[b]).length for a, b in edges]); st_ = float((pl/np.maximum(rl, 1e-6)).max())
        if st_ > W["stretch"][0]: W["stretch"] = (st_, round(float(fr), 2))
    print("MEASURE %-6s 49 samples: trouser points outside the skirt within 30 mm: worst %d (up to %.1f mm) at %s | skirt vertices in a hand: worst %d at %s | largest edge stretch %.2f at %s" % (an, W["poke"][0], W["poke"][1]*1000, W["poke"][2], W["hand"][0], W["hand"][1], W["stretch"][0], W["stretch"][1]))
