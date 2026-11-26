# Review only, never saved. Run before render_views.py (or an export) in the same Blender session on head v011:
#   HAIR_ALBEDO=<png> HAIR_ROUGH=0.5 blender -b head_candidate_v011.blend --python hair_material_apply.py --python render_views.py -- ...
# Swaps ONLY the image and roughness of SCULPT_MAT_HAIR. Unset HAIR_ALBEDO keeps v011's image; unset HAIR_ROUGH keeps
# 0.70. Metallic 0 and specular 0.25 are asserted unchanged; nothing else in the scene is touched.
import bpy, os
m = bpy.data.materials["SCULPT_MAT_HAIR"]; nt = m.node_tree
b = [n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'][0]; t = [n for n in nt.nodes if n.type == 'TEX_IMAGE'][0]
assert abs(b.inputs["Metallic"].default_value) < 1e-9 and abs(b.inputs["Specular"].default_value - 0.25) < 1e-6
if os.environ.get("HAIR_ALBEDO"):
    t.image = bpy.data.images.load(os.environ["HAIR_ALBEDO"], check_existing=False); t.image.colorspace_settings.name = 'sRGB'
if os.environ.get("HAIR_ROUGH"): b.inputs["Roughness"].default_value = float(os.environ["HAIR_ROUGH"])
print("HAIR_MATERIAL image %s roughness %.2f metallic %.2f specular %.2f" % (t.image.name, b.inputs["Roughness"].default_value, b.inputs["Metallic"].default_value, b.inputs["Specular"].default_value))
