# ART-016 B1 export (Codex brief at faa8749). Static CLAY-only diagnostic GLB + head-only editable source + manifest.
#   blender -b <scratch>/head_b1.blend --python b1_export.py -- <abs empty out dir> <abs held head_candidate_v012.blend>
# GLB: SCULPT_HEAD_ROOT with SCULPT_HEAD, SCULPT_EYE_L/R, SCULPT_BROWS, SCULPT_LASHES, SCULPT_HAIR; options as
# stage4_export.py (metres, Y-up, modifiers applied). Two flat materials only: B1_CLAY (everything) and B1_EYE_DARK
# (non-emissive dark eyes). No body, skeleton, actions, lights, cameras or textures.
import bpy, sys, os, json, hashlib, tempfile, shutil, numpy as np
out, held = sys.argv[sys.argv.index("--")+1:][:2]
assert os.path.isabs(out) and (not os.path.exists(out) or not os.listdir(out)), "output dir must be absolute and empty"
os.makedirs(out, exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
PARTS = ["SCULPT_HEAD", "SCULPT_EYE_L", "SCULPT_EYE_R", "SCULPT_BROWS", "SCULPT_LASHES", "SCULPT_HAIR"]
for n in PARTS + ["SCULPT_HEAD_ROOT"]:
    assert [o.name for o in bpy.data.objects if o.name == n or o.name.startswith(n + ".")] == [n], "missing or duplicate " + n
def flat(name, rgb, rough):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = list(rgb) + [1]; b.inputs["Roughness"].default_value = rough; b.inputs["Specular"].default_value = 0.3
    b.inputs["Emission Strength"].default_value = 0.0; return m
clay = flat("B1_CLAY", (0.55, 0.55, 0.55), 0.6); eye = flat("B1_EYE_DARK", (0.035, 0.020, 0.014), 0.6)
for n in PARTS:
    me = bpy.data.objects[n].data; me.materials.clear(); me.materials.append(eye if n.startswith("SCULPT_EYE") else clay)
glb = os.path.join(out, "simm_head_b1_clay.glb")
for o in bpy.context.view_layer.objects: o.select_set(False)
for n in ["SCULPT_HEAD_ROOT"] + PARTS:
    o = bpy.data.objects[n]; o.hide_set(False); o.select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects["SCULPT_HEAD_ROOT"]
bpy.ops.export_scene.gltf(filepath=glb, export_format='GLB', use_selection=True, export_apply=True, export_yup=True,
                          export_animations=False, export_skins=False, export_cameras=False, export_lights=False,
                          export_materials='EXPORT', export_image_format='AUTO', export_texcoords=True, export_normals=True,
                          export_morph=False, export_extras=False)
R = {"packet": "ART-016 head blockout B1, CLAY diagnostic (Codex brief faa8749); not a production head", "glb": {"file": os.path.basename(glb), "sha256": sha(glb), "bytes": os.path.getsize(glb)}, "parts": {}}
# held v012 head-part base meshes, for the change list and the neck seam check (read from a temporary copy)
tmpd = tempfile.mkdtemp(); hc = os.path.join(tmpd, "held.blend"); shutil.copy(held, hc)
with bpy.data.libraries.load(hc) as (s_, d_): d_.meshes = [m for m in s_.meshes if m in PARTS]
HELD = {m.name.split(".")[0]: np.array([v.co[:] for v in m.vertices]) for m in d_.meshes}
for n in PARTS:
    cur = np.array([v.co[:] for v in bpy.data.objects[n].data.vertices]); h = HELD.get(n)
    rec = {"base_vertices": len(cur), "held_base_vertices": None if h is None else len(h)}
    if h is not None and h.shape == cur.shape:
        dd = np.linalg.norm(cur - h, axis=1); rec.update({"base_moved_over_0.05mm": int((dd > 5e-5).sum()), "base_max_move_mm": round(float(dd.max()*1000), 2)})
        if n == "SCULPT_HEAD":
            neck = h[:, 2] < 1.02; face_low = (h[:, 2] < 1.10) & (h[:, 1] < -0.05)
            rec.update({"neck_vertices_z_below_1.02": int(neck.sum()), "neck_max_move_mm": round(float(dd[neck].max()*1000), 4),
                        "lower_face_below_z_1.10_max_move_mm": round(float(dd[face_low].max()*1000), 4),
                        "moved_region_min": h[dd > 5e-5].min(0).round(3).tolist() if (dd > 5e-5).any() else None,
                        "moved_region_max": h[dd > 5e-5].max(0).round(3).tolist() if (dd > 5e-5).any() else None})
    else:
        rec["note"] = "rebuilt from scratch (different vertex count)" if h is not None else "no held counterpart"
    R["parts"][n] = rec
# re-import: counts, bounds, materials
before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=glb)
new = [o for o in bpy.data.objects if o not in before]
assert not [o for o in new if o.type == 'ARMATURE'] and not bpy.data.actions[:0], "unexpected rig/actions"
meshes = {o.name.split(".")[0]: o for o in new if o.type == 'MESH'}; assert sorted(meshes) == sorted(PARTS), sorted(meshes)
allp = []
for n, o in meshes.items():
    P = np.array([o.matrix_world @ v.co for v in o.data.vertices]); allp.append(P)
    R["parts"][n].update({"glb_vertices": len(P), "glb_triangles": sum(len(p.vertices) - 2 for p in o.data.polygons), "glb_bounds_min": P.min(0).round(4).tolist(),
                          "glb_bounds_max": P.max(0).round(4).tolist(), "glb_materials": [m.name.split(".")[0] for m in o.data.materials]})
A = np.concatenate(allp); R["glb"].update({"total_triangles": sum(p["glb_triangles"] for p in R["parts"].values()), "bounds_min_blender_zup": A.min(0).round(4).tolist(),
                                          "bounds_max_blender_zup": A.max(0).round(4).tolist(), "root": "SCULPT_HEAD_ROOT at the origin, identity (as v012)",
                                          "armatures": 0, "animations": len(bpy.data.actions) - len([a for a in bpy.data.actions if a.users]), "cameras": 0, "lights": 0})
for o in new: bpy.data.objects.remove(o, do_unlink=True)
# head-only editable source: keep the SCULPT_ head objects, drop the starter's body, rig, old head and socket
keep = set(PARTS + ["SCULPT_HEAD_ROOT"])
for o in list(bpy.data.objects):
    if o.name not in keep: bpy.data.objects.remove(o, do_unlink=True)
for a in list(bpy.data.actions): bpy.data.actions.remove(a)
bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
src = os.path.join(out, "head_b1_source.blend"); bpy.ops.wm.save_as_mainfile(filepath=src, compress=True, copy=True)
R["source_blend"] = {"file": "head_b1_source.blend", "sha256": sha(src), "objects": sorted(keep)}
json.dump(R, open(os.path.join(out, "head_b1_manifest.json"), "w"), indent=1)
print("B1 EXPORT", R["glb"]["sha256"], R["glb"]["total_triangles"], json.dumps(R["parts"]["SCULPT_HEAD"]))
