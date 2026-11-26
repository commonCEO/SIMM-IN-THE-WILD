# Review renders only, run after jacket_review_prep.py. BOOT_SHOW=after removes, on the temporary REVIEW_BODY copy only,
# the foot-owned faces of the three original shoe materials and the folded-hood piece, and shows the boots.
# Faces of those materials that are not foot-owned (the pack straps in "Simm brown boot leather") are kept.
import bpy, bmesh, os
rig = bpy.data.objects["SimmRig"]
for o in bpy.data.objects:
    if o.name.startswith("SCULPT_BOOT_") and not o.modifiers:
        o.modifiers.new("Armature", 'ARMATURE').object = rig; o.parent = None
tmp = bpy.data.objects["REVIEW_BODY"]
drop = {"Simm dark soles", "Simm brown boot leather", "Simm worn jacket edges", "Simm folded hood canvas"} if os.environ.get("BOOT_SHOW", "after") == "after" else {"Simm folded hood canvas"}
ids = [i for i, m in enumerate(tmp.data.materials) if m and m.name in drop]
gn = [g.name for g in tmp.vertex_groups]
def foot(k): return any(gn[g.group] in ("foot_l", "foot_r") and g.weight > 0.999 for g in tmp.data.vertices[k].groups)
hood = [i for i, m in enumerate(tmp.data.materials) if m and m.name == "Simm folded hood canvas"]
kill = [p.index for p in tmp.data.polygons if p.material_index in hood or (p.material_index in ids and all(foot(k) for k in p.vertices))]
bm = bmesh.new(); bm.from_mesh(tmp.data); bm.faces.ensure_lookup_table(); bmesh.ops.delete(bm, geom=[bm.faces[i] for i in kill], context='FACES'); bm.to_mesh(tmp.data); bm.free()
for o in bpy.data.objects:
    if o.name.startswith("SCULPT_BOOT_"): o.hide_render = os.environ.get("BOOT_SHOW", "after") != "after"
bpy.context.view_layer.update()
