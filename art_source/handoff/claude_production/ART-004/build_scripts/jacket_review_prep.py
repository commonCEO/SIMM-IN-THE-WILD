# Review only, never saved. Run before render_views.py in the same Blender session:
#   blender -b jacket_candidate.blend --python jacket_review_prep.py --python render_views.py -- <render args> nobody ...
# JK_SHOW=after (default) shows SCULPT_JACKET on a temporary copy of the body without the original jacket and
# seam-binding faces. JK_SHOW=before shows the frozen body as it is. JK_ACT with JK_FRAME or JK_FRAC (0 to 1 of the clip) poses the rig for the frame.
import bpy, bmesh, os
show = os.environ.get("JK_SHOW", "after"); act = os.environ.get("JK_ACT", ""); frame = float(os.environ.get("JK_FRAME", "0"))
body = bpy.data.objects["PROTECTED_BODY"]; rig = bpy.data.objects["SimmRig"]; jk = bpy.data.objects.get("SCULPT_JACKET")
tmp = bpy.data.objects.new("REVIEW_BODY", body.data.copy()); bpy.context.scene.collection.objects.link(tmp)
tmp.modifiers.new("Armature", 'ARMATURE').object = rig
if show == "after":
    drop = [i for i, m in enumerate(tmp.data.materials) if m and m.name in ("Simm golden canvas jacket.001", "Simm golden seam binding.001")]
    bm = bmesh.new(); bm.from_mesh(tmp.data)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.material_index in drop], context='FACES')
    bm.to_mesh(tmp.data); bm.free()
if jk: jk.hide_render = show != "after"
for m in bpy.data.materials:                      # the body's texture files are not in Git: fall back to base values
    if m.use_nodes:
        for n in list(m.node_tree.nodes):
            if n.type == 'TEX_IMAGE' and (n.image is None or n.image.size[0] == 0):
                for l in list(n.outputs[0].links): m.node_tree.links.remove(l)
# carry the static head and collar on their bones for posed frames (object parenting of SCULPT roots only)
for root, bone in (("SCULPT_HEAD_ROOT", "head"), ("SCULPT_COLLAR_ROOT", "chest")):
    o = bpy.data.objects.get(root)
    if o:
        mw = o.matrix_world.copy(); o.parent = rig; o.parent_type = 'BONE'; o.parent_bone = bone; o.matrix_world = mw
if act:
    if rig.animation_data is None: rig.animation_data_create()
    rig.animation_data.action = bpy.data.actions[act]
    if os.environ.get("JK_FRAC"):                     # position in the clip as a fraction of its frame range
        f0, f1 = bpy.data.actions[act].frame_range; frame = f0 + (f1 - f0)*float(os.environ["JK_FRAC"])
    bpy.context.scene.frame_set(int(frame), subframe=frame - int(frame))
bpy.context.view_layer.update()
