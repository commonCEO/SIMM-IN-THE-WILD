# Review renders only, run after jacket_review_prep.py. BOOT_SHOW=after hides the original shoe materials and the
# folded-hood piece on the temporary REVIEW_BODY copy and shows the blockout; BOOT_SHOW=before hides the blockout.
import bpy, bmesh, os
show = os.environ.get("BOOT_SHOW", "after"); tmp = bpy.data.objects["REVIEW_BODY"]
drop = {"Simm dark soles", "Simm brown boot leather", "Simm worn jacket edges", "Simm folded hood canvas"} if show == "after" else {"Simm folded hood canvas"}
ids = [i for i, m in enumerate(tmp.data.materials) if m and m.name in drop]
bm = bmesh.new(); bm.from_mesh(tmp.data); bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.material_index in ids], context='FACES'); bm.to_mesh(tmp.data); bm.free()
for o in bpy.data.objects:
    if o.name.startswith("SCULPT_BOOT_"): o.hide_render = show != "after"
bpy.context.view_layer.update()
