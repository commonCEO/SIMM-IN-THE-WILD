# Export ONLY the new static head meshes to GLB (Y-up, metres, embedded textures, modifiers applied).
import bpy, sys
out = sys.argv[sys.argv.index("--")+1]
names = ["SCULPT_HEAD_ROOT", "SCULPT_HEAD", "SCULPT_EYE_L", "SCULPT_EYE_R", "SCULPT_HAIR", "SCULPT_BROWS", "SCULPT_LASHES"]
for o in bpy.context.view_layer.objects: o.select_set(False)
for n in names:
    o = bpy.data.objects[n]; o.hide_set(False); o.select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects["SCULPT_HEAD_ROOT"]
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=True, export_apply=True, export_yup=True,
                          export_animations=False, export_skins=False, export_cameras=False, export_lights=False,
                          export_materials='EXPORT', export_image_format='AUTO', export_texcoords=True, export_normals=True,
                          export_morph=False, export_extras=False)
print("EXPORTED", out)
