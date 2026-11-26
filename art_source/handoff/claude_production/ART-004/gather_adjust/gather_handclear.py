# ART-004: adjusted copy of the `gather` clip, chosen by the user ("1 adjust", 26 Nov 2026).
# blender -b <file with SimmRig> --python gather_handclear.py -- <absolute out.blend> <absolute out_keys.json> [<absolute out.glb>]
# Makes a NEW action `gather_handclear`: a copy of `gather` in which only the upper_arm_l Z rotation channel gets an
# extra outward rotation, A * sin^2(pi * t), t = 0 at the first frame and 1 at the last, so the clip still starts and
# ends exactly as before and still loops. In this rig *_l is Simm's right side (-X). The original `gather` action,
# the rest pose, every other bone and channel, and the socket are untouched.
import bpy, sys, json, math
sys.dont_write_bytecode = True
argv = sys.argv[sys.argv.index("--")+1:]; out, out_json = argv[0], argv[1]; out_glb = argv[2] if len(argv) > 2 else None
A = math.radians(4.5)
rig = bpy.data.objects["SimmRig"]; src = bpy.data.actions["gather"]
old = bpy.data.actions.get("gather_handclear")
if old: bpy.data.actions.remove(old)
act = src.copy(); act.name = "gather_handclear"; act.use_fake_user = True
f0, f1 = src.frame_range
fc = [c for c in act.fcurves if c.data_path == 'pose.bones["upper_arm_l"].rotation_euler' and c.array_index == 2]
assert len(fc) == 1, "upper_arm_l Z rotation channel not found once"
fc = fc[0]; rows = []
for k in fc.keyframe_points:
    t = (k.co.x - f0)/(f1 - f0); d = A*math.sin(math.pi*t)**2
    rows.append({"frame": k.co.x, "original_rad": k.co.y, "offset_rad": d, "new_rad": k.co.y + d})
    k.co.y += d; k.handle_left.y += d; k.handle_right.y += d
fc.update()
# proof that nothing else differs from the source action
for c in act.fcurves:
    s = src.fcurves.find(c.data_path, index=c.array_index)
    same = [abs(a.co.y - b.co.y) < 1e-9 and abs(a.co.x - b.co.x) < 1e-9 for a, b in zip(c.keyframe_points, s.keyframe_points)]
    if not (c.data_path == fc.data_path and c.array_index == fc.array_index): assert all(same) and len(c.keyframe_points) == len(s.keyframe_points), "unexpected change in " + c.data_path
print("ACTION gather_handclear: %d channels copied from gather, 1 changed (upper_arm_l rotation_euler Z), peak offset %.1f deg at mid-clip, 0 at frames %.0f and %.0f" % (len(act.fcurves), math.degrees(A), f0, f1))
json.dump({"action": "gather_handclear", "source_action": "gather", "bone": "upper_arm_l", "channel": "rotation_euler", "index": 2, "rotation_mode": rig.pose.bones["upper_arm_l"].rotation_mode,
           "formula": "new = original + 4.5 deg * sin^2(pi * (frame - first) / (last - first))", "frame_range": [f0, f1], "keys": rows}, open(out_json, "w"), indent=1)
bpy.ops.wm.save_as_mainfile(filepath=out)
if out_glb:   # DISABLED 26 Nov: this export used export_nla_strips=False, which in Blender 3.5 merges all actions and
              # wrote the ORIGINAL gather curve under the new name. gather_handclear_rig_only.glb is therefore defective.
    raise SystemExit("GLB export removed: use calibration_export.py, which exports each clip separately and re-imports to check")
if False:
    for o in bpy.data.objects: o.select_set(False)
    rig.hide_set(False); rig.hide_select = False
    if not rig.visible_get(): bpy.context.scene.collection.objects.link(rig)
    rig.select_set(True); bpy.context.view_layer.objects.active = rig
    rig.animation_data.action = act
    for t in list(rig.animation_data.nla_tracks): rig.animation_data.nla_tracks.remove(t)
    bpy.ops.export_scene.gltf(filepath=out_glb, export_format='GLB', use_selection=True, export_animations=True, export_nla_strips=False,
                              export_force_sampling=True, export_frame_range=False, export_skins=True, export_def_bones=False, export_yup=True)
    import json as _j, struct as _s                    # name the clip in the file; the exporter calls it "Animation"
    d = open(out_glb, 'rb').read(); m_, v_, t_ = _s.unpack('<III', d[:12]); n_ = _s.unpack('<I', d[12:16])[0]; g_ = _j.loads(d[20:20+n_])
    g_['animations'][0]['name'] = 'gather_handclear'; js = _j.dumps(g_, separators=(',', ':')).encode(); js += b' '*((4 - len(js) % 4) % 4)
    open(out_glb, 'wb').write(_s.pack('<III', m_, v_, 20 + len(js) + len(d) - 20 - n_) + _s.pack('<II', len(js), 0x4E4F534A) + js + d[20+n_:])
    print("EXPORTED", out_glb)
