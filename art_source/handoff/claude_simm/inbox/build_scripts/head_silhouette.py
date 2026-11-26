# Silhouette heights for the crown study. Renders an alpha mask of the head and hair (Cycles, 4 samples, transparent film)
# at one of the agreed cameras of render_views.py ("ref", "alt", "front"), 672 px, target Z 1.20, distance scale 0.55,
# then reports, in pixels: the highest hair point (full top, tufts included) and the top of the MAIN mass, found by a
# morphological opening that removes features narrower than OPEN px (thin tufts and spikes). Also writes the masks.
# blender -b head.blend --python head_silhouette.py -- <view> <out prefix>     (then analyse with Pillow outside Blender)
import bpy, sys, math
from mathutils import Vector
view, pre = sys.argv[sys.argv.index("--")+1:][:2]
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 4   # headless: no GPU
sc.cycles.use_denoising = False; sc.render.film_transparent = True                                         # only alpha is used
sc.render.resolution_x = sc.render.resolution_y = 672; sc.render.resolution_percentage = 100
for o in bpy.data.objects: o.hide_render = not o.name.startswith(("SCULPT_HEAD", "SCULPT_HAIR", "SCULPT_EYE", "SCULPT_BROWS", "SCULPT_LASHES")) or o.type != 'MESH'
cd = bpy.data.cameras.new("SilCam"); cam = bpy.data.objects.new("SilCam", cd); sc.collection.objects.link(cam); sc.camera = cam
az, el, dist = {"ref": (30, 15, 2.6), "alt": (72.3, 15, 2.6), "front": (0, 0, 2.6)}[view]; dist *= 0.55
cd.lens = 84.7 if view in ("ref", "alt") else 110; cd.sensor_width = 36
a = math.radians(az); e = math.radians(el); t = Vector((0, 0, 1.20))
cam.location = t + Vector((-math.sin(a)*math.cos(e), -math.cos(a)*math.cos(e), math.sin(e)))*dist
cam.rotation_euler = (t - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = pre + "_mask_" + view + ".png"; bpy.ops.render.render(write_still=True); print("MASK", sc.render.filepath)
