# ART-020 check and (optional) export for the interactive hair starter. Works headless or from Blender's Text Editor.
#   check only:  blender -b <edited starter>.blend --python check_and_export.py
#   check+export: blender -b <edited starter>.blend --python check_and_export.py -- <abs new .glb path>
#   In the GUI: open this file in the Text Editor and press Run Script; it checks and, if OUT below is set, exports.
# REFUSES to export when any protected face part changed, when SCULPT_HAIR_WORK is missing or duplicated, or when the
# output exists. Exports ONLY SCULPT_HEAD_ROOT > SCULPT_HAIR (renamed from SCULPT_HAIR_WORK for the file), metres,
# Y up, modifiers applied, placeholder material, no rig, actions, cameras, lights or textures. The .blend is not saved.
import bpy, sys, os, json, hashlib
OUT = None                                    # GUI use: set to an absolute path such as r"C:\...\hair_candidate_01.glb"
here = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() and os.path.exists(__file__) else bpy.path.abspath("//")
sys.path.insert(0, here)
from starter_common import PROTECTED, obj_record
if "--" in sys.argv and len(sys.argv) > sys.argv.index("--") + 1: OUT = sys.argv[sys.argv.index("--") + 1]
man_path = os.path.join(here, "simm_hair_starter_manifest.json"); M = json.load(open(man_path))
problems = []
for n in PROTECTED:
    o = bpy.data.objects.get(n)
    if o is None: problems.append(n + " missing"); continue
    r = obj_record(o); b = M["objects"][n]
    if r["fingerprint"] != b["fingerprint"]: problems.append(n + " geometry changed")
    if r["modifiers"] != b["modifiers"]: problems.append(n + " modifiers changed")
    if r["parent"] != "SCULPT_HEAD_ROOT": problems.append(n + " re-parented")
root = bpy.data.objects.get("SCULPT_HEAD_ROOT")
if root is None or not obj_record.__globals__["np"].allclose(root.matrix_world, obj_record.__globals__["np"].eye(4), atol=1e-7): problems.append("SCULPT_HEAD_ROOT missing or moved")
works = [o for o in bpy.data.objects if o.name == "SCULPT_HAIR_WORK" or o.name.startswith("SCULPT_HAIR_WORK.")]
if len(works) != 1 or works[0].name != "SCULPT_HAIR_WORK": problems.append("need exactly one SCULPT_HAIR_WORK, found %s" % [o.name for o in works])
held = bpy.data.objects.get("SCULPT_HAIR_HELD_CONTROL")
if held is None or obj_record(held)["fingerprint"] != M["objects"]["SCULPT_HAIR_HELD_CONTROL"]["fingerprint"]: problems.append("held hair control missing or changed")
rep = {"protected_unchanged": not problems, "problems": problems}
if works: 
    w = obj_record(works[0]); rep["work_hair"] = {k: w[k] for k in ("vertices", "polygons", "bounds_min", "bounds_max", "modifiers", "parent")}
    rep["work_hair"]["changed_from_held"] = w["fingerprint"] != M["objects"]["SCULPT_HAIR_HELD_CONTROL"]["fingerprint"]
print("STARTER CHECK", json.dumps(rep))
if OUT:
    assert not problems, "refusing to export: " + "; ".join(problems)
    assert os.path.isabs(OUT) and OUT.endswith(".glb") and not os.path.exists(OUT), "OUT must be a new absolute .glb path"
    w = works[0]; old = w.name; w.name = "SCULPT_HAIR"; lock = root.hide_select; root.hide_select = False   # locked objects cannot be selected
    try:
        for o in bpy.context.view_layer.objects: o.select_set(False)
        for o in (root, w): o.hide_set(False); o.select_set(True)
        bpy.context.view_layer.objects.active = root
        bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_apply=True, export_yup=True,
                                  export_animations=False, export_skins=False, export_cameras=False, export_lights=False,
                                  export_materials='PLACEHOLDER', export_texcoords=True, export_normals=True, export_morph=False, export_extras=False)
    finally:
        w.name = old; root.hide_select = lock
    rep["export"] = {"file": OUT, "sha256": hashlib.sha256(open(OUT, "rb").read()).hexdigest(), "bytes": os.path.getsize(OUT)}
    json.dump(rep, open(OUT[:-4] + "_check.json", "w"), indent=1); print("EXPORTED", json.dumps(rep["export"]))
