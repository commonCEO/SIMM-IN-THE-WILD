# ART-020 (Codex dispatch 33b35d4): build the HEAD-ONLY interactive hair starter from held v012. Preparation only:
# no new hair shape is made here. Run on the held source; it is never saved over.
#   blender -b art_source/handoff/claude_simm/inbox/head_candidate_v012.blend --python build_starter.py -- <abs out.blend> [<abs reference png>]
# The optional reference png (read from Codex's branch with git cat-file) is linked by a RELATIVE path to
# art_source/handoff/claude_simm/APPROVED_REFERENCE.png and never packed, so no reference pixels are stored in the file.
import bpy, sys, os, json, math, hashlib
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from starter_common import PROTECTED, obj_record
args = sys.argv[sys.argv.index("--")+1:]; out = args[0]; ref = args[1] if len(args) > 1 else None
assert os.path.isabs(out) and out.endswith(".blend") and not os.path.exists(out), "out must be a new absolute .blend path"
src = bpy.data.filepath
SOURCE = {n: obj_record(bpy.data.objects[n]) for n in PROTECTED + ["SCULPT_HAIR"]}
# 1) keep only the head: drop body, rig, socket, old head, guides, actions (in this NEW file only)
keep = set(PROTECTED + ["SCULPT_HEAD_ROOT", "SCULPT_HAIR"])
for o in list(bpy.data.objects):
    if o.name not in keep: bpy.data.objects.remove(o, do_unlink=True)
for a in list(bpy.data.actions): bpy.data.actions.remove(a)
# 2) collections
sc = bpy.context.scene; root_coll = sc.collection
def coll(name):
    c = bpy.data.collections.new(name); root_coll.children.link(c); return c
cP, cH, cW, cR = coll("00_PROTECTED_FACE_DO_NOT_EDIT"), coll("01_HELD_HAIR_CONTROL"), coll("10_WORK_HAIR"), coll("20_REVIEW")
def move(o, c):
    for x in list(o.users_collection): x.objects.unlink(o)
    c.objects.link(o)
for n in PROTECTED + ["SCULPT_HEAD_ROOT"]:
    o = bpy.data.objects[n]; move(o, cP); o.hide_select = True
for c in list(bpy.data.collections):
    if c not in (cP, cH, cW, cR) and not c.objects and not c.children: bpy.data.collections.remove(c)
held = bpy.data.objects["SCULPT_HAIR"]; held.name = "SCULPT_HAIR_HELD_CONTROL"; held.data.name = "SCULPT_HAIR_HELD_CONTROL"
move(held, cH); held.hide_select = True; held.hide_set(True); held.hide_render = True
work = held.copy(); work.data = held.data.copy(); work.name = "SCULPT_HAIR_WORK"; work.data.name = "SCULPT_HAIR_WORK"
cW.objects.link(work); work.hide_select = False; work.hide_set(False); work.hide_render = False; work.parent = held.parent; work.matrix_world = held.matrix_world.copy()
# 3) review: clay material, two view layers, agreed cameras (render_views.py ref/alt), key and fill for the ref view
clay = bpy.data.materials.new("REVIEW_CLAY"); clay.use_nodes = True; b = clay.node_tree.nodes["Principled BSDF"]
b.inputs["Base Color"].default_value = (0.55, 0.55, 0.55, 1); b.inputs["Roughness"].default_value = 0.6; b.inputs["Specular"].default_value = 0.3
vl = sc.view_layers[0]; vl.name = "WORK"
vc = sc.view_layers.new("CLAY_REVIEW"); vc.material_override = clay
w = bpy.data.worlds.new("REVIEW_WORLD"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.62, 0.62, 0.64, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 0.55
T = Vector((0, 0, 1.215)); CAMS = {}
def cam(name, az, el, dist):
    d = bpy.data.cameras.new(name); d.lens = 84.7; d.sensor_width = 36; o = bpy.data.objects.new(name, d); cR.objects.link(o)
    a, e = math.radians(az), math.radians(el); dv = Vector((-math.sin(a)*math.cos(e), -math.cos(a)*math.cos(e), math.sin(e)))
    o.location = T + dv*dist; o.rotation_euler = (T - o.location).to_track_quat('-Z', 'Y').to_euler(); o.hide_select = True
    CAMS[name] = {"azimuth_deg": az, "elevation_deg": el, "distance_m": dist, "lens_mm": 84.7, "target": list(T), "location": [round(x, 4) for x in o.location]}; return o, dv
cref, dref = cam("CAM_REF", 30, 15, 2.6); cam("CAM_ALT", 72.3, 15, 2.6)
cam("CAM_REF_HEAD", 30, 15, 1.43); cam("CAM_ALT_HEAD", 72.3, 15, 1.43)
a = math.radians(30); right = Vector((math.cos(a), -math.sin(a), 0))
def light(name, loc, energy, size, col):
    d = bpy.data.lights.new(name, 'AREA'); d.energy = energy; d.size = size; d.color = col; o = bpy.data.objects.new(name, d); cR.objects.link(o)
    o.location = loc; o.rotation_euler = (T - o.location).to_track_quat('-Z', 'Y').to_euler(); o.hide_select = True
light("KEY_REF", T + dref*1.6 + Vector((0, 0, 1.1)) - right*1.1, 55, 1.2, (1.0, 0.97, 0.92))
light("FILL_REF", T + dref*1.5 + right*1.6 + Vector((0, 0, 0.2)), 12, 2.0, (0.9, 0.95, 1.0))
sc.camera = bpy.data.objects["CAM_REF_HEAD"]; sc.render.engine = 'BLENDER_EEVEE'; sc.render.resolution_x = sc.render.resolution_y = 900
sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'
# 4) reference: external, relative, NOT packed
REF = None
if ref:
    img = bpy.data.images.load(ref, check_existing=False); img.name = "APPROVED_REFERENCE (external, not packed)"
    # path relative to the STARTER's folder; saved with relative_remap off so Blender keeps it exactly
    img.filepath = "//../../../claude_simm/APPROVED_REFERENCE.png"; img.use_fake_user = True
    REF = {"image": img.name, "relative_path": img.filepath, "packed": img.packed_file is not None,
           "sha256_of_file_read": hashlib.sha256(open(ref, "rb").read()).hexdigest()}
    assert not REF["packed"]
bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
if ref: assert any(i.name.startswith("APPROVED_REFERENCE") for i in bpy.data.images)
# 5) records: every protected mesh and the held hair must match the source exactly
ST = {n: obj_record(bpy.data.objects[n]) for n in PROTECTED}
ST["SCULPT_HAIR_HELD_CONTROL"] = obj_record(held); ST["SCULPT_HAIR_WORK"] = obj_record(work)
for n in PROTECTED: assert ST[n]["fingerprint"] == SOURCE[n]["fingerprint"], n
assert ST["SCULPT_HAIR_HELD_CONTROL"]["fingerprint"] == ST["SCULPT_HAIR_WORK"]["fingerprint"] == SOURCE["SCULPT_HAIR"]["fingerprint"]
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True, relative_remap=False)
if REF: REF["relative_path"] = bpy.data.images[REF["image"]].filepath; assert REF["relative_path"] == "//../../../claude_simm/APPROVED_REFERENCE.png", REF
M = {"ticket": "ART-020 head-only interactive hair starter (Codex 33b35d4); preparation only, no new hair shape",
     "source_blend": os.path.basename(src), "source_blend_sha256": hashlib.sha256(open(src, "rb").read()).hexdigest(),
     "starter_blend": os.path.basename(out), "units": "metres, Blender Z up, front -Y, Simm's right -X; glTF export is Y up",
     "attachment_root": "SCULPT_HEAD_ROOT (empty, identity world matrix, as v012); all head parts are its children",
     "collections": {"00_PROTECTED_FACE_DO_NOT_EDIT": PROTECTED + ["SCULPT_HEAD_ROOT"], "01_HELD_HAIR_CONTROL": ["SCULPT_HAIR_HELD_CONTROL (hidden)"],
                     "10_WORK_HAIR": ["SCULPT_HAIR_WORK (the only editable object)"], "20_REVIEW": sorted(CAMS) + ["KEY_REF", "FILL_REF"]},
     "view_layers": {"WORK": "own materials", "CLAY_REVIEW": "material override REVIEW_CLAY (grey 0.55, roughness 0.6)"},
     "cameras": CAMS, "removed_from_this_file_only": ["PROTECTED_BODY", "REFERENCE_FAILED_OLD_HEAD", "SimmRig", "simm", "hand_r_socket", "SCULPT_HAIR_GUIDES", "all actions"],
     "objects": ST, "reference": REF}
json.dump(M, open(out[:-6] + "_manifest.json", "w"), indent=1)
print("STARTER", out, {n: ST[n]["vertices"] for n in ST})
