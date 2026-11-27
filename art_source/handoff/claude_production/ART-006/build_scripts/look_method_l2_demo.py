# ART-006 look-method L2 demo (Codex brief at 4097e24). Review only, never saved. Same chain as look_method_demo.py:
#   SUPPORT_PALETTE=<p001 json> blender -b work/jacket_material_m002.blend --python .../jacket_review_prep.py \
#       --python .../boot_review_prep.py --python .../support_palette_apply.py --python look_method_l2_demo.py -- \
#       <out prefix> <step> <views> [size] [samples]
# Lighting model as in L1's demo (sun + constant world colour, no bounce light, Filmic, fixed exposure), but the key now
# uses the NATIVE study's direction, converted from Codex's Godot values instead of L1's approximation:
#   native key rotation (-40, -30, 0), Godot YXZ Euler -> light comes FROM Blender (-0.383, -0.663, 0.643):
#   30 deg from Simm's front toward Simm's right, 40 deg elevation (i.e. from the ref camera's side).
#   L1 side direction, Codex's source vector (-0.679, 0.707, 0.197) Godot -> Blender (-0.679, -0.197, 0.707):
#   73.8 deg toward Simm's right, 45 deg elevation.
# Steps:
#   base : native key (shadows on), cool ambient #b7c9d2
#   B    : L1's rejected side key (key moved to the side direction, x1.25), for reference
#   L2   : base + ONE added "form light": a directional light from the side direction, shadows OFF, no specular, warm
#          #ffe6c8, energy 0.3/0.8 of the key. Key, ambient, shadows and materials unchanged.
#   AL2  : L2 with L1's warm ambient #d9c7a8 (A stays a separate candidate; shown only as a control)
import bpy, sys, math
from mathutils import Vector
a = sys.argv[sys.argv.index("--")+1:]
pre, step, views = a[0], a[1], a[2].split(","); size = int(a[3]) if len(a) > 3 else 700; samples = int(a[4]) if len(a) > 4 else 48
KEY0, AMB0, FORM_RATIO = 5.0, 0.55, 0.3/0.8
def hexlin(h):
    c = [int(h[i:i+2], 16)/255 for i in (0, 2, 4)]
    return [x/12.92 if x <= 0.04045 else ((x + 0.055)/1.055)**2.4 for x in c]
def from_dir(az, el):
    r, e = math.radians(az), math.radians(el); return Vector((-math.sin(r)*math.cos(e), -math.cos(r)*math.cos(e), math.sin(e)))
NATIVE_KEY = Vector((-0.383, -0.663, 0.643)).normalized(); SIDE = Vector((-0.679067, -0.197149, 0.707107)).normalized()
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = samples; sc.cycles.use_denoising = True; sc.cycles.seed = 0
sc.cycles.max_bounces = 0; sc.cycles.diffuse_bounces = 0; sc.cycles.glossy_bounces = 0; sc.cycles.transmission_bounces = 0
sc.render.resolution_x = sc.render.resolution_y = size; sc.render.resolution_percentage = 100
sc.view_settings.view_transform = 'Filmic'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.0
for o in bpy.data.objects:
    if o.type == 'LIGHT': o.hide_render = True
    if o.name == "PROTECTED_BODY": o.hide_render = True
w = bpy.data.worlds.new("DemoWorld"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = hexlin("d9c7a8" if step == "AL2" else "b7c9d2") + [1]
w.node_tree.nodes["Background"].inputs[1].default_value = AMB0
def sun(name, src, energy, col, shadow=True, spec=True):
    d = bpy.data.lights.new(name, 'SUN'); d.color = hexlin(col); d.angle = math.radians(0.25); d.energy = energy
    d.cycles.cast_shadow = shadow
    o = bpy.data.objects.new(name, d); sc.collection.objects.link(o); o.rotation_euler = (-src).to_track_quat('-Z', 'Y').to_euler()
    o.visible_glossy = spec
    return o
if step == "B": sun("DemoKey", SIDE, KEY0*1.25, "fff0df")
else: sun("DemoKey", NATIVE_KEY, KEY0, "fff0df")
if step in ("L2", "AL2"): sun("DemoForm", SIDE, KEY0*FORM_RATIO, "ffe6c8", shadow=False, spec=False)
fl = bpy.data.materials.new("DemoFloor"); fl.use_nodes = True; fb = fl.node_tree.nodes["Principled BSDF"]
fb.inputs["Base Color"].default_value = hexlin("c8c0a5") + [1]; fb.inputs["Roughness"].default_value = 0.9; fb.inputs["Specular"].default_value = 0.2
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0)); bpy.context.active_object.data.materials.append(fl)
cd = bpy.data.cameras.new("DemoCam"); cd.sensor_width = 36; cam = bpy.data.objects.new("DemoCam", cd); sc.collection.objects.link(cam); sc.camera = cam
VIEWS = {"ref": (30, 15, 5.2, 0.72), "back": (180, 15, 5.2, 0.72), "face": (30, 15, 1.35, 1.17), "faceback": (180, 15, 2.4, 0.95)}
for v in views:
    az, el, dist, tz = VIEWS[v]; tgt = Vector((0, 0, tz))
    cd.lens = 84.7; cam.location = tgt + from_dir(az, el)*dist; cam.rotation_euler = (tgt - cam.location).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = "%s_%s_%s.png" % (pre, step, v); bpy.ops.render.render(write_still=True); print("DEMO", sc.render.filepath)
