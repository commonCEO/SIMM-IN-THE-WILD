# ART-018 R2 Stage A export (Codex brief at 634c089). HAIR-ONLY static clay GLB + minimal source + manifest.
#   blender -b <stage A blend> --python r2a_export.py -- <abs empty out dir>
# GLB: SCULPT_HEAD_ROOT (identity, as v012) with SCULPT_HAIR only; metres, Y-up; one flat material R2A_CLAY; no rig,
# actions, textures, lights or cameras. Source: a .blend with only SCULPT_HEAD_ROOT and SCULPT_HAIR.
import bpy, sys, os, json, hashlib, numpy as np
out = sys.argv[sys.argv.index("--")+1]
assert os.path.isabs(out) and (not os.path.exists(out) or not os.listdir(out)), "output dir must be absolute and empty"
os.makedirs(out, exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
for n in ("SCULPT_HAIR", "SCULPT_HEAD_ROOT"):
    assert [o.name for o in bpy.data.objects if o.name == n or o.name.startswith(n + ".")] == [n], n
hair = bpy.data.objects["SCULPT_HAIR"]
m = bpy.data.materials.new("R2A_CLAY"); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
b.inputs["Base Color"].default_value = (0.55, 0.55, 0.55, 1); b.inputs["Roughness"].default_value = 0.6; b.inputs["Specular"].default_value = 0.3
hair.data.materials.clear(); hair.data.materials.append(m)
glb = os.path.join(out, "simm_hair_r2_stage_a_clay.glb")
for o in bpy.context.view_layer.objects: o.select_set(False)
for n in ("SCULPT_HEAD_ROOT", "SCULPT_HAIR"): bpy.data.objects[n].hide_set(False); bpy.data.objects[n].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects["SCULPT_HEAD_ROOT"]
bpy.ops.export_scene.gltf(filepath=glb, export_format='GLB', use_selection=True, export_apply=True, export_yup=True,
                          export_animations=False, export_skins=False, export_cameras=False, export_lights=False,
                          export_materials='EXPORT', export_texcoords=True, export_normals=True, export_morph=False, export_extras=False)
before = set(bpy.data.objects); n_act = len(bpy.data.actions); bpy.ops.import_scene.gltf(filepath=glb)
new = [o for o in bpy.data.objects if o not in before]
assert not [o for o in new if o.type == 'ARMATURE'] and len(bpy.data.actions) == n_act, "unexpected rig or actions"
ms = [o for o in new if o.type == 'MESH']; assert len(ms) == 1 and ms[0].name.startswith("SCULPT_HAIR"), [o.name for o in new]
P = np.array([ms[0].matrix_world @ v.co for v in ms[0].data.vertices])
import bmesh
bm = bmesh.new(); bm.from_mesh(hair.data); islands = 0; seen = set()
for v in bm.verts:
    if v.index in seen: continue
    islands += 1; st = [v]; seen.add(v.index)
    while st:
        x = st.pop()
        for e in x.link_edges:
            y = e.other_vert(x)
            if y.index not in seen: seen.add(y.index); st.append(y)
bm.free()
R = {"packet": "ART-018 R2 Stage A, hair-only CLAY diagnostic (Codex brief 634c089); not a production head",
     "glb": {"file": os.path.basename(glb), "sha256": sha(glb), "bytes": os.path.getsize(glb), "nodes": ["SCULPT_HEAD_ROOT", "SCULPT_HAIR"],
             "vertices": len(P), "triangles": sum(len(p.vertices) - 2 for p in ms[0].data.polygons), "bounds_min_blender_zup": P.min(0).round(4).tolist(),
             "bounds_max_blender_zup": P.max(0).round(4).tolist(), "materials": [x.name.split(".")[0] for x in ms[0].data.materials],
             "armatures": 0, "animations": 0, "cameras": 0, "lights": 0, "uv": "none (clay only)"},
     "source_islands": islands}
for o in new: bpy.data.objects.remove(o, do_unlink=True)
for o in list(bpy.data.objects):
    if o.name not in ("SCULPT_HEAD_ROOT", "SCULPT_HAIR"): bpy.data.objects.remove(o, do_unlink=True)
for a in list(bpy.data.actions): bpy.data.actions.remove(a)
bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
src = os.path.join(out, "hair_r2_stage_a_source.blend"); bpy.ops.wm.save_as_mainfile(filepath=src, compress=True, copy=True)
R["source_blend"] = {"file": os.path.basename(src), "sha256": sha(src), "objects": ["SCULPT_HEAD_ROOT", "SCULPT_HAIR"]}
json.dump(R, open(os.path.join(out, "hair_r2_stage_a_manifest.json"), "w"), indent=1)
print("R2A EXPORT", R["glb"]["sha256"], R["glb"]["triangles"], islands)
