# Review only, never saved. Close clay render aimed at a point, after jacket_review_prep.py and boot_review_prep.py:
#   blender -b f.blend --python jacket_review_prep.py --python boot_review_prep.py --python close_render.py -- \
#       <out.png> <x,y,z target> <azimuth deg> <elevation deg> <distance m> [size] [samples]
# Azimuth 0 looks from the front (-Y); positive turns toward -X (Simm's right), as in render_views.py. Lens 85 mm.
import bpy, sys, math
from mathutils import Vector
a = sys.argv[sys.argv.index("--")+1:]
out = a[0]; tgt = Vector([float(x) for x in a[1].split(",")]); az, el, dist = float(a[2]), float(a[3]), float(a[4])
size = int(a[5]) if len(a) > 5 else 520; samples = int(a[6]) if len(a) > 6 else 24
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = samples; sc.cycles.use_denoising = True
sc.render.resolution_x = sc.render.resolution_y = size; sc.render.resolution_percentage = 100; sc.view_settings.view_transform = 'Standard'
w = bpy.data.worlds.new("CloseWorld"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0.62, 0.62, 0.64, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 0.6
clay = bpy.data.materials.new("CLOSE_CLAY"); clay.use_nodes = True; clay.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.55, 0.55, 0.55, 1)
bpy.context.view_layer.material_override = clay
for o in bpy.data.objects:
    if o.name == "PROTECTED_BODY": o.hide_render = True
r, e = math.radians(az), math.radians(el); dv = Vector((-math.sin(r)*math.cos(e), -math.cos(r)*math.cos(e), math.sin(e)))
cd = bpy.data.cameras.new("CloseCam"); cd.lens = 85; cam = bpy.data.objects.new("CloseCam", cd); sc.collection.objects.link(cam); sc.camera = cam
cam.location = tgt + dv*dist; cam.rotation_euler = (tgt - cam.location).to_track_quat('-Z', 'Y').to_euler()
ld = bpy.data.lights.new("CloseKey", 'AREA'); ld.energy = 40; ld.size = 1.0; lo = bpy.data.objects.new("CloseKey", ld); sc.collection.objects.link(lo)
right = Vector((math.cos(r), -math.sin(r), 0)); lo.location = tgt + dv*1.2 + Vector((0, 0, 0.8)) - right*0.8; lo.rotation_euler = (tgt - lo.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = out; bpy.ops.render.render(write_still=True); print("CLOSE", out)
