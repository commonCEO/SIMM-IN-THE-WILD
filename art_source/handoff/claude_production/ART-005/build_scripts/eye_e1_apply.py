# Review only, never saved. Applies the E1 packet's albedo PNG (E1_PNG env) to SCULPT_MAT_EYE of the held head v012 in
# memory, exactly as eye_e1_build.py sets the material (no emission, roughness 0.55, Blender specular 0.25). Run before
# render_views.py:  E1_PNG=<abs png> blender -b inbox/head_candidate_v012.blend --python eye_e1_apply.py --python render_views.py -- ...
import bpy, os
tex = bpy.data.images.load(os.environ["E1_PNG"]); tex.colorspace_settings.name = 'sRGB'
m = bpy.data.materials["SCULPT_MAT_EYE"]; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
for l in list(nt.links):
    if l.to_socket == b.inputs["Base Color"]: l.from_node.image = tex
    elif l.to_socket == b.inputs["Emission"]: nt.links.remove(l)
b.inputs["Emission"].default_value = (0, 0, 0, 1); b.inputs["Emission Strength"].default_value = 0.0
b.inputs["Roughness"].default_value = 0.55; b.inputs["Specular"].default_value = 0.25
print("E1 PNG applied", os.environ["E1_PNG"])
