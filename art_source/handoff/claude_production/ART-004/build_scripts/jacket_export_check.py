# Checks and exports the jacket candidate. Nothing is saved back to the .blend.
# blender -b jacket_candidate.blend --python jacket_export_check.py -- <absolute out.glb> <absolute out_vertex_map.json>
import bpy, sys, json, numpy as np
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode = True
out, out_json = sys.argv[sys.argv.index("--")+1:][:2]
jk = bpy.data.objects["SCULPT_JACKET"]; body = bpy.data.objects["PROTECTED_BODY"]; rig = bpy.data.objects["SimmRig"]
sc = bpy.context.scene

# ---- manifest and preservation contract ---------------------------------------------------------------------
assert [o.name for o in bpy.data.objects if o.name.startswith("SCULPT_JACKET")] == ["SCULPT_JACKET"], "missing or duplicate jacket"
assert [g.name for g in jk.vertex_groups] == [g.name for g in body.vertex_groups], "vertex group names or order differ"
oi = [d.value for d in jk.data.attributes["orig_index"].data]
assert len(set(oi)) == len(oi) == len(jk.data.vertices), "orig_index is not one-to-one"
jm = [i for i, m in enumerate(body.data.materials) if m and m.name == "Simm golden canvas jacket.001"][0]
orig_jacket = set()
for p in body.data.polygons:
    if p.material_index == jm: orig_jacket.update(p.vertices)
assert set(oi) == orig_jacket, "candidate is not exactly the original jacket vertex set"
maxinf = 0; moved = []
for v, k in zip(jk.data.vertices, oi):
    a = sorted((g.group, round(g.weight, 6)) for g in v.groups); b = sorted((g.group, round(g.weight, 6)) for g in body.data.vertices[k].groups)
    assert a == b, "weights differ at original vertex %d" % k
    maxinf = max(maxinf, sum(1 for g in v.groups if g.weight > 0)); moved.append((v.co - body.data.vertices[k].co).length)
ft = sorted(tuple(sorted(oi[i] for i in p.vertices)) for p in jk.data.polygons)
fo = sorted(tuple(sorted(p.vertices)) for p in body.data.polygons if p.material_index == jm)
assert ft == fo, "face connectivity differs from the original jacket faces"
uv_same = all(np.allclose([d.uv[:] for d in jk.data.uv_layers[n].data][:50], [d.uv[:] for d in jk.data.uv_layers[n].data][:50]) for n in ("UVMap", "SurfaceUV"))
co = np.array([v.co[:] for v in jk.data.vertices]); oc = np.array([body.data.vertices[k].co[:] for k in oi])
tris = sum(len(p.vertices)-2 for p in jk.data.polygons)
print("MANIFEST ok SCULPT_JACKET: %d verts, %d tris, 1 material %s, uv layers %s" % (len(oi), tris, [m.name for m in jk.data.materials], [u.name for u in jk.data.uv_layers]))
print("PRESERVED vertex set, face connectivity, group order and every weight identical to the original jacket; max influences per vertex %d" % maxinf)
print("MOVED max %.1f mm, mean %.1f mm, vertices moved more than 1 mm: %d of %d" % (max(moved)*1000, np.mean(moved)*1000, sum(1 for m in moved if m > 0.001), len(moved)))
print("BOUNDS original jacket min %s max %s" % (np.round(oc.min(0), 3), np.round(oc.max(0), 3)))
print("BOUNDS candidate       min %s max %s" % (np.round(co.min(0), 3), np.round(co.max(0), 3)))

# ---- frozen parts that sit on the jacket: do they now float or sink? -----------------------------------------
def tree_of(obj, verts=None): return BVHTree.FromPolygons(verts if verts is not None else [v.co.copy() for v in obj.data.vertices], [tuple(p.vertices) for p in obj.data.polygons])
new_t = tree_of(jk); old_t = BVHTree.FromPolygons([v.co.copy() for v in body.data.vertices], [tuple(p.vertices) for p in body.data.polygons if p.material_index == jm])
for names in (("Simm olive canvas", "Simm woven olive straps", "Simm canvas seams"), ("Simm brass fasteners",), ("Simm folded hood canvas",), ("Simm warm dark undershirt.001",)):
    ids = [i for i, m in enumerate(body.data.materials) if m and m.name in names]; vs = set()
    for p in body.data.polygons:
        if p.material_index in ids: vs.update(p.vertices)
    sunk = 0; fl = []; n = 0
    for k in vs:
        c = body.data.vertices[k].co; lo = old_t.find_nearest(c, 0.012)
        if lo[0] is None: continue
        n += 1; ln = new_t.find_nearest(c, 0.08)
        if ln[0] is None: continue
        sd = (c - ln[0]).dot(ln[1])
        if sd < -0.001: sunk += 1
        else: fl.append(sd)
    print("ONJACKET %-58s verts that lay within 12 mm of the old jacket: %4d; now under the new surface: %4d; floating above it: max %.1f mm, mean %.1f mm" % ("/".join(names), n, sunk, (max(fl) if fl else 0)*1000, (np.mean(fl) if fl else 0)*1000))

# ---- clips: does the cloth get crossed by thighs or hands? before against after -----------------------------
tm = [i for i, m in enumerate(body.data.materials) if m and m.name == "Simm charcoal olive trousers"][0]
sm = [i for i, m in enumerate(body.data.materials) if m and m.name == "Simm warm skin"][0]
if rig.animation_data is None: rig.animation_data_create()
for an in ("idle", "walk", "gather"):
    act = bpy.data.actions[an]; rig.animation_data.action = act; f0, f1 = act.frame_range; res = {}
    for fr in np.linspace(f0, f1, 9):
        sc.frame_set(int(fr), subframe=float(fr - int(fr))); dg = bpy.context.evaluated_depsgraph_get()
        eb = body.evaluated_get(dg); mb = eb.to_mesh(); bv = [v.co.copy() for v in mb.vertices]
        ej = jk.evaluated_get(dg); mj = ej.to_mesh(); jv = [v.co.copy() for v in mj.vertices]
        for label, mi_ in (("thighs", tm), ("hands", sm)):
            t = BVHTree.FromPolygons(bv, [tuple(p.vertices) for p in mb.polygons if p.material_index == mi_])
            for state, pts in (("before", [bv[k] for k in oi]), ("after", jv)):
                cnt = 0; deep = 0.0
                for c in pts:
                    loc, nrm, idx, d = t.find_nearest(c, 0.04)
                    if loc is not None and (c - loc).dot(nrm) < -0.0005: cnt += 1; deep = max(deep, d)
                key = (label, state); w = res.get(key, (0, 0.0)); res[key] = (max(w[0], cnt), max(w[1], deep))
        eb.to_mesh_clear(); ej.to_mesh_clear()
    for label in ("thighs", "hands"):
        b_, a_ = res[(label, "before")], res[(label, "after")]
        print("CLIP %-6s jacket vertices inside the %-6s surface, worst of 9 samples: before %3d (deepest %4.1f mm), after %3d (deepest %4.1f mm)" % (an, label, b_[0], b_[1]*1000, a_[0], a_[1]*1000))
rig.animation_data.action = None; sc.frame_set(0)
for pb in rig.pose.bones: pb.matrix_basis.identity()        # in memory only: back to rest before export

# ---- sidecar: original index, original rest position, candidate position -------------------------------------
json.dump({"object": "SCULPT_JACKET", "source_object": "PROTECTED_BODY", "source_material": "Simm golden canvas jacket.001",
           "axes": "Blender Z-up, metres, front -Y", "vertices": [[k, [round(x, 6) for x in body.data.vertices[k].co], [round(x, 6) for x in v.co]] for v, k in zip(jk.data.vertices, oi)]},
          open(out_json, "w"), separators=(",", ":"))

# ---- export: the candidate skinned to a copy of the rest skeleton, no animation ------------------------------
for o in bpy.data.objects: o.select_set(False)
# The frozen rig is not selectable in this file and is left that way. The export uses a throwaway copy of the
# armature at rest and a throwaway copy of the jacket bound to it. Neither copy is saved.
rc = rig.copy(); rc.data = rig.data.copy(); rc.name = "SimmRigRestCopy"; rc.animation_data_clear()
sc.collection.objects.link(rc); rc.hide_select = False; rc.hide_viewport = False
jc = jk.copy(); jc.data = jk.data.copy(); sc.collection.objects.link(jc); jk.name = "SCULPT_JACKET_SRC"; jc.name = "SCULPT_JACKET"
jc.modifiers["Armature"].object = rc; jc.parent = rc
for pb in rc.pose.bones: pb.matrix_basis.identity()
bpy.context.view_layer.update()
for o in (jc, rc):
    o.hide_set(False); o.select_set(True)
assert rc.select_get() and jc.select_get()
bpy.context.view_layer.objects.active = jc
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=True, export_animations=False, export_skins=True, export_yup=True, export_apply=False, export_def_bones=False)
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=out)
new = [o for o in bpy.data.objects if o not in before]
arm = [o for o in new if o.type == 'ARMATURE']; meshes = [o for o in new if o.type == 'MESH']
assert len(arm) == 1 and len(meshes) == 1, [o.name for o in new]
ib = sorted(b.name for b in arm[0].data.bones); rb = sorted(b.name for b in rig.data.bones)
jk.name = "SCULPT_JACKET_SRC"
m = meshes[0]; gi = {g.index: g.name for g in m.vertex_groups}; gj = {g.index: g.name for g in jk.vertex_groups}
kd = {tuple(np.round(v.co, 5)): v for v in jk.data.vertices}; worst = 0.0; miss = 0
for v in m.data.vertices:
    w = m.matrix_world @ v.co; s_ = kd.get(tuple(np.round(w, 5)))
    if s_ is None: miss += 1; continue
    a = {gi[g.group]: g.weight for g in v.groups if g.weight > 1e-4}; b = {gj[g.group]: g.weight for g in s_.groups if g.weight > 1e-4}
    worst = max(worst, max(abs(a.get(k, 0) - b.get(k, 0)) for k in set(a) | set(b)))
mc = np.array([m.matrix_world @ v.co for v in m.data.vertices])
print("GLB mesh %s verts %d tris %d materials %s; armature bones %d, names match rig: %s; actions in file: %d" % (m.name, len(m.data.vertices), sum(len(p.vertices)-2 for p in m.data.polygons), [x.name for x in m.data.materials], len(ib), ib == rb, len([a for a in bpy.data.actions if a.name not in ("idle", "walk", "gather")])))
print("GLB re-import bounds min %s max %s; weight difference against the candidate: max %.5f; vertices not matched by position: %d" % (np.round(mc.min(0), 3), np.round(mc.max(0), 3), worst, miss))
print("EXPORTED", out)
