# Checks and exports the jacket finish candidate (SCULPT_JACKET_LONG, SCULPT_JACKET_LONG_TRIM, SCULPT_JACKET_POCKETS)
# against the held jacket v004. Nothing is saved back. A failed assert stops the run; its GLB is not delivered.
# blender -b <finish blend, with the gather_handclear study action added> --python jacket_finish_check.py -- \
#     <absolute out.glb> <absolute out_manifest.json> <absolute held v004 blend>
# SAMPLES env (default 97). Clips: idle, walk, gather (original, negative control), gather_handclear (study copy).
import bpy, bmesh, sys, os, json, math, hashlib, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
sys.dont_write_bytecode = True
out, out_json, held = sys.argv[sys.argv.index("--")+1:][:3]
NS = int(os.environ.get("SAMPLES", "97"))
body = bpy.data.objects["PROTECTED_BODY"]; rig = bpy.data.objects["SimmRig"]; sc = bpy.context.scene
PARTS = tuple(os.environ.get("FINISH_PARTS", "SCULPT_JACKET_LONG,SCULPT_JACKET_LONG_TRIM,SCULPT_JACKET_POCKETS").split(","))   # held baseline run: the two v004 parts
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
R = {"held_v004_blend_sha256": sha(held), "parts": {}, "clips": {}, "residuals": []}
for n in PARTS:
    assert [o.name for o in bpy.data.objects if o.name == n or o.name.startswith(n + ".")] == [n], "missing or duplicate part " + n
    ob = bpy.data.objects[n]
    assert [g.name for g in ob.vertex_groups] == [g.name for g in body.vertex_groups], n + ": vertex group names or order differ"
    assert len(ob.modifiers) == 1 and ob.modifiers[0].type == 'ARMATURE' and ob.modifiers[0].object == rig, n + ": modifier stack"
with bpy.data.libraries.load(held, link=False) as (src, dst):
    dst.meshes = [m for m in src.meshes if m in ("SCULPT_JACKET_LONG", "SCULPT_JACKET_LONG_TRIM")]
H = {m.name.split(".")[0]: m for m in dst.meshes}
for n in PARTS:
    me = bpy.data.objects[n].data; co = np.array([v.co[:] for v in me.vertices])
    inf = [sum(1 for g in v.groups if g.weight > 0) for v in me.vertices]; ws = [sum(g.weight for g in v.groups) for v in me.vertices]
    assert max(inf) <= 4 and min(ws) > 0.999 and max(ws) < 1.001, n + ": weights over 4 influences or not normalised"
    bm = bmesh.new(); bm.from_mesh(me); nm = sum(1 for e in bm.edges if len(e.link_faces) != 2); bm.free()
    rec = {"vertices": len(me.vertices), "triangles": sum(len(p.vertices) - 2 for p in me.polygons), "non_manifold_edges": nm,
           "bounds_min": np.round(co.min(0), 4).tolist(), "bounds_max": np.round(co.max(0), 4).tolist(), "material": [m.name for m in me.materials]}
    if n in H:
        hm = H[n]; k = len(hm.vertices); hco = np.array([v.co[:] for v in hm.vertices])
        same_w = all(sorted((g.group, round(g.weight, 6)) for g in me.vertices[i].groups) == sorted((g.group, round(g.weight, 6)) for g in hm.vertices[i].groups) for i in range(k))
        assert same_w, n + ": a held v004 vertex changed weight"
        d = np.linalg.norm(co[:k] - hco, axis=1)
        rec.update({"held_v004_vertices": k, "held_v004_triangles": sum(len(p.vertices) - 2 for p in hm.polygons), "held_vertices_weights_identical": True,
                    "held_vertices_moved_over_0_1mm": int((d > 1e-4).sum()), "held_vertices_max_move_mm": round(float(d.max())*1000, 2),
                    "new_vertices": len(me.vertices) - k})
    R["parts"][n] = rec
    print("PART %s: %s" % (n, rec))

mi = {m.name: i for i, m in enumerate(body.data.materials) if m}; gn = [g.name for g in body.vertex_groups]
def handv(k): return any(gn[g.group] in ("hand_l", "hand_r") and g.weight > 0.5 for g in body.data.vertices[k].groups)
hand_f = [tuple(p.vertices) for p in body.data.polygons if p.material_index == mi["Simm warm skin"] and all(handv(k) for k in p.vertices)]
tro = sorted(set(k for p in body.data.polygons if p.material_index == mi["Simm charcoal olive trousers"] for k in p.vertices))
tro = [k for k in tro if 0.483 < body.data.vertices[k].co.z < 0.70]
strap = sorted(set(k for p in body.data.polygons if p.material_index in [mi[x] for x in ("Simm woven olive straps",) if x in mi] for k in p.vertices))
DIR = Vector((0.13, 0.27, 0.95)).normalized()
def parity(t, c):
    n = 0; o = c.copy()
    for _ in range(24):
        h = t.ray_cast(o, DIR, 2.0)
        if h[0] is None: break
        n += 1; o = h[0] + DIR*1e-6
    return n % 2 == 1
def inside_hand(t, c):
    loc, nrm, idx, d = t.find_nearest(c, 0.03)
    if loc is None or (c - loc).dot(nrm) > -0.001: return 0.0
    return d if parity(t, c) else 0.0
objs = [bpy.data.objects[n] for n in PARTS]
if rig.animation_data is None: rig.animation_data_create()
for tr_ in rig.animation_data.nla_tracks: tr_.mute = True
for an in [c for c in ("idle", "walk", "gather", "gather_handclear") if c in bpy.data.actions]:
    act = bpy.data.actions[an]; rig.animation_data.action = act; f0, f1 = act.frame_range
    W = {"tro": (0, 0.0, None), "hand": (0, 0.0, None), "strap": (0, None), "gap": (9.0, None)}
    for fr in np.linspace(f0, f1, NS):
        sc.frame_set(int(fr), subframe=float(fr - int(fr))); dg = bpy.context.evaluated_depsgraph_get()
        eb = body.evaluated_get(dg); mb = eb.to_mesh(); bv = [v.co.copy() for v in mb.vertices]; eb.to_mesh_clear()
        M = {}
        for o in objs:
            e = o.evaluated_get(dg); m = e.to_mesh(); M[o.name] = ([v.co.copy() for v in m.vertices], [tuple(p.vertices) for p in m.polygons]); e.to_mesh_clear()
        gv, gf = M["SCULPT_JACKET_LONG"]; gt = BVHTree.FromPolygons(gv, gf)
        Hm = rig.evaluated_get(dg).pose.bones["hips"].matrix; ax = Hm.translation; up = (Hm.to_3x3() @ Vector((0, 1, 0))).normalized()
        bad = []
        for k in tro:
            p = bv[k]; rel = p - ax; rad = rel - up*rel.dot(up); rl = rad.length
            if rl < 1e-4: continue
            d = rad/rl; near = gt.find_nearest(p, 0.05)
            if parity(gt, p) or (gt.ray_cast(p + d*1e-4, d, 0.25)[0] is None and gt.ray_cast(p - d*1e-4, -d, rl)[0] is not None):
                bad.append((k, near[3] if near[0] is not None else 0.0))
        if len(bad) > W["tro"][0]: W["tro"] = (len(bad), max(b[1] for b in bad), round(float(fr), 2))
        for b in bad: R["residuals"].append({"clip": an, "frame": round(float(fr), 2), "kind": "trousers through the jacket", "body_vertex": b[0], "depth_mm": round(b[1]*1000, 2)})
        ht = BVHTree.FromPolygons(bv, hand_f); hb = 0; deep = 0.0
        for n_, (vs, fs) in M.items():
            for i, c in enumerate(vs):
                dd = inside_hand(ht, c)
                if dd > 0:
                    hb += 1; deep = max(deep, dd); R["residuals"].append({"clip": an, "frame": round(float(fr), 2), "kind": "cloth inside a hand", "part": n_, "vertex": i, "depth_mm": round(dd*1000, 2)})
                else:
                    nr = ht.find_nearest(c, 0.03)
                    if nr[0] is not None and nr[3] < W["gap"][0]: W["gap"] = (nr[3], round(float(fr), 2))
        if hb > W["hand"][0]: W["hand"] = (hb, deep, round(float(fr), 2))
        # frozen pack straps that end up inside the jacket shell (the straps lie on the jacket's chest)
        ns = sum(1 for k in strap if parity(gt, bv[k]))
        if ns > W["strap"][0]: W["strap"] = (ns, round(float(fr), 2))
    R["clips"][an] = {"trouser_points_through_jacket_worst": W["tro"][0], "deepest_mm": round(W["tro"][1]*1000, 2), "at": W["tro"][2],
                      "cloth_vertices_in_hand_worst": W["hand"][0], "hand_deepest_mm": round(W["hand"][1]*1000, 2), "hand_at": W["hand"][2],
                      "smallest_hand_gap_mm": round(W["gap"][0]*1000, 2), "gap_at": W["gap"][1],
                      "strap_vertices_inside_jacket_worst": W["strap"][0], "strap_at": W["strap"][1]}
    print("CLIP %-16s %d samples: %s" % (an, NS, R["clips"][an]))
rig.animation_data.action = None; sc.frame_set(0)
for pb in rig.pose.bones: pb.matrix_basis.identity()

# export: the three parts on a rest copy of the skeleton, no animation; re-import and account for every vertex
rc = rig.copy(); rc.data = rig.data.copy(); rc.name = "SimmRigRestCopy"; rc.animation_data_clear()
sc.collection.objects.link(rc); rc.hide_select = False; rc.hide_viewport = False
for pb in rc.pose.bones: pb.matrix_basis.identity()
copies = []
for n in PARTS:
    ob = bpy.data.objects[n]; c = ob.copy(); c.data = ob.data.copy(); sc.collection.objects.link(c); ob.name = n + "_SRC"; c.name = n
    c.modifiers["Armature"].object = rc; c.parent = rc; copies.append(c)
bpy.context.view_layer.update()
for o in bpy.data.objects: o.select_set(False)
for o in copies + [rc]: o.hide_set(False); o.select_set(True)
bpy.context.view_layer.objects.active = copies[0]
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=True, export_animations=False, export_skins=True, export_yup=True, export_apply=False, export_def_bones=False)
before = set(bpy.data.objects); n_act = len(bpy.data.actions)
bpy.ops.import_scene.gltf(filepath=out)
newo = [o for o in bpy.data.objects if o not in before]
arm = [o for o in newo if o.type == 'ARMATURE']; meshes = [o for o in newo if o.type == 'MESH']
assert len(arm) == 1 and len(meshes) == len(PARTS) and len(bpy.data.actions) == n_act, [o.name for o in newo]
ib = {b.name: b for b in arm[0].data.bones}; rb = {b.name: b for b in rig.data.bones}; assert sorted(ib) == sorted(rb)
wh = max(((arm[0].matrix_world @ ib[n].head_local) - (rig.matrix_world @ b.head_local)).length for n, b in rb.items()); assert wh < 1e-5, wh
R["glb"] = {"file": os.path.basename(out), "sha256": sha(out), "bytes": os.path.getsize(out), "bones": len(ib), "animations": 0, "parts": {}}
for n in PARTS:
    src = bpy.data.objects[n + "_SRC"]; m = [x for x in meshes if x.name.split(".")[0] == n]; assert len(m) == 1, n; m = m[0]
    gi = {g.index: g.name for g in m.vertex_groups}; gs = {g.index: g.name for g in src.vertex_groups}
    kd = KDTree(len(src.data.vertices))
    for i, v in enumerate(src.data.vertices): kd.insert(v.co, i)
    kd.balance(); hit = set(); un = 0; wbad = 0
    for v in m.data.vertices:
        w_ = m.matrix_world @ v.co; cands = kd.find_range(w_, 2e-5)
        if not cands: un += 1; continue
        a = {gi[g.group]: g.weight for g in v.groups if g.weight > 1e-6}; best = 9.0; bi = None
        for _, i, _ in cands:
            b = {gs[g.group]: g.weight for g in src.data.vertices[i].groups if g.weight > 1e-6}
            dd = max(abs(a.get(k, 0) - b.get(k, 0)) for k in set(a) | set(b))
            if dd < best: best = dd; bi = i
        hit.add(bi); wbad += best > 1e-5
    co = np.array([m.matrix_world @ v.co for v in m.data.vertices])
    R["glb"]["parts"][n] = {"vertices_in_file": len(m.data.vertices), "triangles": sum(len(p.vertices) - 2 for p in m.data.polygons), "materials": [x.name.split(".")[0] for x in m.data.materials],
                            "bounds_min": np.round(co.min(0), 4).tolist(), "bounds_max": np.round(co.max(0), 4).tolist(), "unmatched": un, "covered": len(hit), "source_vertices": len(src.data.vertices), "weight_mismatches": wbad}
    print("GLBACC", n, "unmatched", un, "covered", len(hit), "of", len(src.data.vertices), "weight mismatches", wbad)
    assert un == 0 and len(hit) == len(src.data.vertices) and wbad == 0, n + ": GLB accounting failed"
json.dump(R, open(out_json, "w"), indent=1)
print("EXPORTED", out, R["glb"]["sha256"])
