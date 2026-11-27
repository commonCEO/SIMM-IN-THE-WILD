# Surface-based contact check that does not depend on the garment's vertex density (ART-004 f002, Codex 9de793b).
# blender -b <garment blend with the gather_handclear study action> --python jacket_contact_check.py -- <out.json>
# GARMENT env: comma list of garment parts (default the f002 three). SAMPLES env (default 97).
# For every sampled pose, each garment surface is intersected (BVH overlap, triangle against triangle) with the
# UNCHANGED partner surfaces: the hands (warm-skin triangles whose vertices are all over 50 percent hand), the pack
# straps, the trousers, and the collar's hood and scarf carried by the chest bone. The result is the set of PARTNER
# triangles crossed. Partner meshes are identical in every file, so these sets compare directly between garments of any
# density. A crossing means the surfaces intersect at that triangle; it does not measure depth.
import bpy, sys, os, json, numpy as np
from mathutils import Matrix
from mathutils.bvhtree import BVHTree
out = sys.argv[sys.argv.index("--")+1]
G = os.environ.get("GARMENT", "SCULPT_JACKET_LONG,SCULPT_JACKET_LONG_TRIM,SCULPT_JACKET_POCKETS").split(",")
NS = int(os.environ.get("SAMPLES", "97"))
body = bpy.data.objects["PROTECTED_BODY"]; rig = bpy.data.objects["SimmRig"]; sc = bpy.context.scene
mi = {m.name: i for i, m in enumerate(body.data.materials) if m}; gn = [g.name for g in body.vertex_groups]
def handv(k): return any(gn[g.group] in ("hand_l", "hand_r") and g.weight > 0.5 for g in body.data.vertices[k].groups)
P_ = list(body.data.polygons)
groups = {"hand": [p.index for p in P_ if p.material_index == mi["Simm warm skin"] and all(handv(k) for k in p.vertices)],
          "strap": [p.index for p in P_ if p.material_index == mi["Simm woven olive straps"]],
          "trousers": [p.index for p in P_ if p.material_index == mi["Simm charcoal olive trousers"] and min(body.data.vertices[k].co.z for k in p.vertices) < 0.70]}
collar = [bpy.data.objects[n] for n in ("SCULPT_HOOD", "SCULPT_SCARF")]
chest = rig.data.bones["chest"]
if rig.animation_data is None: rig.animation_data_create()
for t in rig.animation_data.nla_tracks: t.mute = True
R = {"garment": G, "samples": NS, "partner_triangles": {k: len(v) for k, v in groups.items()}, "clips": {}}
for an in [c for c in ("idle", "walk", "gather", "gather_handclear") if c in bpy.data.actions]:
    act = bpy.data.actions[an]; rig.animation_data.action = act; f0, f1 = act.frame_range
    union = {k: set() for k in list(groups) + ["collar"]}; worst = {k: (0, None) for k in union}
    for fr in np.linspace(f0, f1, NS):
        sc.frame_set(int(fr), subframe=float(fr - int(fr))); dg = bpy.context.evaluated_depsgraph_get()
        eb = body.evaluated_get(dg); mb = eb.to_mesh(); bv = [v.co.copy() for v in mb.vertices]; eb.to_mesh_clear()
        gv = []; gf = []
        for n in G:
            e = bpy.data.objects[n].evaluated_get(dg); m = e.to_mesh(); off = len(gv)
            gv += [e.matrix_world @ v.co for v in m.vertices]; gf += [tuple(off + i for i in p.vertices) for p in m.polygons]; e.to_mesh_clear()
        gt = BVHTree.FromPolygons(gv, gf)
        hit = {}
        for k, idx in groups.items():
            t = BVHTree.FromPolygons(bv, [tuple(P_[i].vertices) for i in idx])
            hit[k] = {idx[j] for _, j in gt.overlap(t)}
        pb = rig.evaluated_get(dg).pose.bones["chest"]
        M = rig.matrix_world @ pb.matrix @ chest.matrix_local.inverted() @ rig.matrix_world.inverted()
        cv = []; cf = []; tag = []
        for o in collar:
            off = len(cv); cv += [M @ (o.matrix_world @ v.co) for v in o.data.vertices]
            for p in o.data.polygons: cf.append(tuple(off + i for i in p.vertices)); tag.append("%s:%d" % (o.name, p.index))
        ct = BVHTree.FromPolygons(cv, cf); hit["collar"] = {tag[j] for _, j in gt.overlap(ct)}
        for k, s in hit.items():
            union[k] |= s
            if len(s) > worst[k][0]: worst[k] = (len(s), round(float(fr), 2))
    R["clips"][an] = {k: {"worst_frame_count": worst[k][0], "at": worst[k][1], "union": sorted(union[k], key=str)} for k in union}
    print("CONTACT %-16s " % an + "  ".join("%s worst %d at %s, union %d" % (k, worst[k][0], worst[k][1], len(union[k])) for k in union))
json.dump(R, open(out, "w"))
