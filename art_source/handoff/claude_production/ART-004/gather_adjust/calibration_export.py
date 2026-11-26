# ART-004 gather calibration packet (Codex request at d3f3a94).
# blender -b <blend with SimmRig, gather, gather_handclear and SCULPT_JACKET_SKIRT> --python calibration_export.py -- <absolute out.glb> <absolute manifest.json>
# Exports ONE diagnostic GLB: the 17 original rest bones, the ORIGINAL `gather` and `gather_handclear` as two separately
# named clips, and only the prototype lower panel skinned to the existing bones. Nothing is saved back to the .blend.
#
# Root cause of the first delivery (17d5036): it was exported with export_nla_strips=False. In Blender 3.5 that MERGES
# every action the armature uses into one clip ("Animation"); the exporter warns "Some strips have same channel
# animation" and keeps the original gather's upper_arm_l curve. So that GLB carried the ORIGINAL gather under the new
# name, with no Z offset at all. Here each clip is its own NLA track and export_nla_strips=True, and the result is
# re-imported and checked below, so the same mistake cannot pass silently.
import bpy, sys, json, math, hashlib
from mathutils import Vector
sys.dont_write_bytecode = True
argv = sys.argv[sys.argv.index("--")+1:]; out_glb, out_json = argv[0], argv[1]
CLIPS = ("gather", "gather_handclear"); FPS = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
TIMES = (0.2, 0.4, 0.6)

def fingerprint(act):
    rows = []
    for c in sorted(act.fcurves, key=lambda c: (c.data_path, c.array_index)):
        rows.append("%s[%d]:" % (c.data_path, c.array_index) + ";".join("%.6f,%.9f,%s" % (k.co.x, k.co.y, k.interpolation) for k in c.keyframe_points))
    return hashlib.sha256("\n".join(rows).encode()).hexdigest()

rig = bpy.data.objects["SimmRig"]; sk = bpy.data.objects["SCULPT_JACKET_SKIRT"]
acts = {n: bpy.data.actions[n] for n in CLIPS}
src = {"fingerprint_sha256": {n: fingerprint(a) for n, a in acts.items()}, "frame_range": {n: list(a.frame_range) for n, a in acts.items()}}

# authoring-side expectation: Blender world position of hand_l head at each time, for both clips
def hand_world(act, t):
    rig.animation_data.action = act; bpy.context.scene.frame_set(int(round(t*FPS)))
    return list(rig.matrix_world @ rig.pose.bones["hand_l"].head)
if rig.animation_data is None: rig.animation_data_create()
for tr in list(rig.animation_data.nla_tracks): rig.animation_data.nla_tracks.remove(tr)
expect = {n: {str(t): hand_world(a, t) for t in TIMES} for n, a in acts.items()}
rig.animation_data.action = None; bpy.context.scene.frame_set(0)

# scene for export: rig + panel only, one NLA track per clip
for o in list(bpy.data.objects):
    if o not in (rig, sk): bpy.data.objects.remove(o, do_unlink=True)
for n in list(bpy.data.actions):
    if n.name not in CLIPS: bpy.data.actions.remove(n)
for n in CLIPS:
    tr = rig.animation_data.nla_tracks.new(); tr.name = n
    tr.strips.new(n, int(acts[n].frame_range[0]), acts[n])
for o in (rig, sk):
    if o.name not in bpy.context.scene.collection.objects: bpy.context.scene.collection.objects.link(o)
    o.hide_set(False); o.hide_viewport = False; o.hide_select = False
sk.parent = rig
for o in bpy.data.objects: o.select_set(o in (rig, sk))
bpy.context.view_layer.objects.active = rig
bpy.ops.export_scene.gltf(filepath=out_glb, export_format='GLB', use_selection=True, export_animations=True, export_nla_strips=True,
                          export_force_sampling=True, export_frame_range=False, export_skins=True, export_def_bones=False,
                          export_yup=True, export_apply=False, export_materials='NONE', export_extras=True)

# panel weights/transform manifest (authoring side)
gnames = [g.name for g in sk.vertex_groups]
wsum = {}; nz = {}
for v in sk.data.vertices:
    for g in v.groups:
        if g.weight > 0: wsum[gnames[g.group]] = wsum.get(gnames[g.group], 0.0) + g.weight; nz[gnames[g.group]] = nz.get(gnames[g.group], 0) + 1
panel = {"object": sk.name, "vertices": len(sk.data.vertices), "triangles": sum(len(p.vertices)-2 for p in sk.data.polygons),
         "bones_used": sorted(wsum), "vertices_per_bone": nz, "weight_sum_per_bone": {k: round(v, 4) for k, v in wsum.items()},
         "max_influences_per_vertex": max(len([g for g in v.groups if g.weight > 0]) for v in sk.data.vertices),
         "object_matrix_world_is_identity": all(abs(sk.matrix_world[i][j] - (1.0 if i == j else 0.0)) < 1e-6 for i in range(4) for j in range(4)),
         "z_range_blender": [min(v.co.z for v in sk.data.vertices), max(v.co.z for v in sk.data.vertices)],
         "unfinished": ["join with jacket v003 hem is visible", "3 trouser points up to 1.3 mm at rest (frame 0)", "largest edge stretch 1.37 in walk frame 6"]}

# re-import the EXPORTED file into an empty scene and measure there
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.scene.render.fps, bpy.context.scene.render.fps_base = int(round(FPS)), 1.0   # factory scene is 24 fps; the importer maps glTF seconds to frames with it
bpy.ops.import_scene.gltf(filepath=out_glb)
arm = [o for o in bpy.data.objects if o.type == 'ARMATURE'][0]; mesh = [o for o in bpy.data.objects if o.type == 'MESH']
clips = {}
for a in bpy.data.actions:
    for n in CLIPS:
        if a.name == n or a.name.startswith(n + "_") and not (n == "gather" and a.name.startswith("gather_handclear")): clips[n] = a
assert set(clips) == set(CLIPS), "re-import: expected clips %s, got %s" % (CLIPS, [a.name for a in bpy.data.actions])
if arm.animation_data is None: arm.animation_data_create()
for tr in list(arm.animation_data.nla_tracks): tr.mute = True
bones = [b.name for b in arm.data.bones]
def sample(act, t):
    arm.animation_data.action = act; bpy.context.scene.frame_set(int(round(t*FPS)))
    return {b: (arm.pose.bones[b].matrix_basis.copy(), arm.pose.bones[b].rotation_quaternion.copy()) for b in bones}, arm.matrix_world @ arm.pose.bones["hand_l"].head
report = {"glb": out_glb, "sha256": hashlib.sha256(open(out_glb, "rb").read()).hexdigest(), "fps": FPS,
          "frame_to_time": "time_s = frame / %g; frame 0 = 0.0 s, frame 6 = 0.2 s, frame 12 = 0.4 s, frame 18 = 0.6 s, frame 24 = 0.8 s" % FPS,
          "reimport": {"bones": len(bones), "bone_names": bones, "meshes": [m.name for m in mesh], "clips": {n: a.name for n, a in clips.items()},
                       "clip_frame_range": {n: list(a.frame_range) for n, a in clips.items()},
                       "keys_upper_arm_l_rotation": {n: max((len(c.keyframe_points) for c in a.fcurves if 'upper_arm_l' in c.data_path and 'rotation' in c.data_path), default=0) for n, a in clips.items()}},
          "source_actions": src, "panel": panel, "samples": {}}
worst_other = 0.0
for t in TIMES:
    po, ho = sample(clips["gather"], t); pc, hc = sample(clips["gather_handclear"], t)
    qo, qc = po["upper_arm_l"][1], pc["upper_arm_l"][1]
    d = qo.rotation_difference(qc); ang = math.degrees(d.angle)
    for b in bones:
        if b == "upper_arm_l": continue
        mo, mc = po[b][0], pc[b][0]
        worst_other = max(worst_other, max(abs(mo[i][j] - mc[i][j]) for i in range(4) for j in range(4)))
    report["samples"][str(t)] = {
        "upper_arm_l_local_quat_wxyz": {"gather": [round(x, 6) for x in qo], "gather_handclear": [round(x, 6) for x in qc]},
        "upper_arm_l_delta_deg": round(ang, 3), "delta_axis_local": [round(x, 4) for x in d.axis],
        "expected_delta_deg": round(4.5*math.sin(math.pi*t/0.8)**2, 3),
        "hand_l_world_blender_zup_m": {"gather": [round(x, 5) for x in ho], "gather_handclear": [round(x, 5) for x in hc]},
        "hand_l_delta_mm_blender_zup": [round(1000*(hc[i]-ho[i]), 2) for i in range(3)],
        "hand_l_delta_mm_gltf_yup": [round(1000*(hc[0]-ho[0]), 2), round(1000*(hc[2]-ho[2]), 2), round(-1000*(hc[1]-ho[1]), 2)],
        "authoring_hand_l_delta_mm_blender_zup": [round(1000*(expect["gather_handclear"][str(t)][i]-expect["gather"][str(t)][i]), 2) for i in range(3)]}
report["other_16_bones_max_local_matrix_difference"] = worst_other
json.dump(report, open(out_json, "w"), indent=1)   # written before the checks, so a failure can be read
for t in TIMES:
    s = report["samples"][str(t)]
    assert abs(s["upper_arm_l_delta_deg"] - s["expected_delta_deg"]) < 0.05, "exported delta %.3f deg at %.1f s, expected %.3f" % (s["upper_arm_l_delta_deg"], t, s["expected_delta_deg"])
    assert max(abs(s["hand_l_delta_mm_blender_zup"][i] - s["authoring_hand_l_delta_mm_blender_zup"][i]) for i in range(3)) < 0.5, "re-imported hand delta differs from authoring at %.1f s" % t
assert worst_other < 1e-5, "another bone differs between the two exported clips: %g" % worst_other
assert len(bones) == 17 and len(mesh) == 1, "expected 17 bones and only the panel mesh"
json.dump(report, open(out_json, "w"), indent=1)
print("CALIBRATION OK", report["sha256"]); print(json.dumps(report["samples"], indent=1))
