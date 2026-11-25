# Compare the frozen reference data in a candidate .blend against the untouched starter, and inspect the GLB.
# blender -b --python verify_candidate.py -- START.blend CANDIDATE.blend CANDIDATE.glb
import bpy, sys, hashlib, json, numpy as np
start, cand, glb = sys.argv[sys.argv.index("--")+1:][:3]
def digest(path):
    bpy.ops.wm.open_mainfile(filepath=path)
    d = {}
    for n in ("PROTECTED_BODY", "REFERENCE_FAILED_OLD_HEAD"):
        o = bpy.data.objects[n]; me = o.data
        a = np.empty(len(me.vertices)*3, dtype=np.float32); me.vertices.foreach_get('co', a)
        d[n] = dict(verts=len(me.vertices), polys=len(me.polygons), co=hashlib.sha1(a.tobytes()).hexdigest(),
                    matrix=[round(x, 6) for r in o.matrix_world for x in r], parent=o.parent.name if o.parent else None,
                    hide_render=o.hide_render, hide_viewport=o.hide_viewport, mats=[s.material.name if s.material else None for s in o.material_slots],
                    groups=sorted(g.name for g in o.vertex_groups), mods=[(m.name, m.type) for m in o.modifiers])
    rig = bpy.data.objects["SimmRig"]
    d["SimmRig"] = dict(matrix=[round(x, 6) for r in rig.matrix_world for x in r], parent=rig.parent.name if rig.parent else None,
                        bones={b.name: [round(x, 6) for r in b.matrix_local for x in r] + [b.parent.name if b.parent else None] for b in rig.data.bones})
    s = bpy.data.objects["hand_r_socket"]
    d["hand_r_socket"] = dict(matrix_basis=[round(x, 6) for r in s.matrix_basis for x in r], parent=s.parent.name, parent_type=s.parent_type, parent_bone=s.parent_bone)
    acts = {}
    for a in bpy.data.actions:
        h = hashlib.sha1()
        for fc in a.fcurves:
            h.update(fc.data_path.encode()); h.update(bytes([fc.array_index]))
            k = np.empty(len(fc.keyframe_points)*2, dtype=np.float32); fc.keyframe_points.foreach_get('co', k); h.update(k.tobytes())
        acts[a.name] = dict(fcurves=len(a.fcurves), range=[round(x, 3) for x in a.frame_range], hash=h.hexdigest())
    d["actions"] = acts
    return d
A = digest(start); B = digest(cand)
ok = True
for k in A:
    same = json.dumps(A[k], sort_keys=True) == json.dumps(B[k], sort_keys=True)
    ok &= same; print("FROZEN", k, "UNCHANGED" if same else "CHANGED !!!")
print("bones", len(A["SimmRig"]["bones"]), "actions", sorted(A["actions"]))
new = [(o.name, o.type) for o in bpy.data.collections["10_SCULPT_NEW_HEAD"].objects]
print("NEW OBJECTS", new)
print("FROZEN_ALL_UNCHANGED", ok)
# ---- GLB contents
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
tot = 0; lo = np.array([9e9]*3); hi = -lo
for o in bpy.data.objects:
    if o.type == 'MESH':
        me = o.data; t = sum(len(p.vertices)-2 for p in me.polygons); tot += t
        co = np.array([o.matrix_world @ v.co for v in me.vertices]); lo = np.minimum(lo, co.min(0)); hi = np.maximum(hi, co.max(0))
        print("GLB MESH", o.name, "verts", len(me.vertices), "tris", t, "mats", [m.name for m in me.materials], "uv", len(me.uv_layers), "parent", o.parent.name if o.parent else None)
    else:
        print("GLB NODE", o.name, o.type, "loc", tuple(round(x, 5) for x in o.location), "rot", tuple(round(x, 5) for x in o.rotation_euler), "scale", tuple(round(x, 5) for x in o.scale))
print("GLB total tris", tot, "bbox(Blender Z-up after import) min", lo.round(3), "max", hi.round(3))
print("GLB materials", [m.name for m in bpy.data.materials], "images", [(i.name, tuple(i.size)) for i in bpy.data.images])
print("GLB armatures", len(bpy.data.armatures), "actions", len(bpy.data.actions), "cameras", len(bpy.data.cameras), "lights", len(bpy.data.lights))
