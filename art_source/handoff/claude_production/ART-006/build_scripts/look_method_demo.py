# ART-006 look-method demo (Codex brief at e91d3bd). Review only, never saved. Run after jacket_review_prep.py,
# boot_review_prep.py and support_palette_apply.py (SUPPORT_PALETTE=p001) on the held work/jacket_material_m002.blend:
#   blender -b f.blend --python .../jacket_review_prep.py --python .../boot_review_prep.py \
#       --python .../support_palette_apply.py --python look_method_demo.py -- <out prefix> <step> <views> [size] [samples]
# Approximates the native study's lighting model, not its renderer: one sun (key) + a constant world colour (ambient),
# diffuse/glossy bounces off so there is no bounce light (Godot's study has none beyond SSAO), Filmic, fixed exposure.
# Steps change ONE variable at a time on top of "base":
#   base : key warm #fff0df, energy KEY0, from the native-like direction; ambient #b7c9d2 at AMB0
#   A    : ambient colour #b7c9d2 -> #d9c7a8 (warm), same energy
#   C    : ambient energy x 0.25/0.35 (key:fill ratio up), colour unchanged
#   B    : key turned to about 45 deg off the ref camera axis toward Simm's right, elevation 45 deg, energy x 1.25
#   ABC  : all three
# Absolute values are calibrated to Blender only (KEY0, AMB0); the RATIOS are what map to the Godot proposal.
import bpy, sys, math
from mathutils import Vector, Euler
a = sys.argv[sys.argv.index("--")+1:]
pre, step, views = a[0], a[1], a[2].split(","); size = int(a[3]) if len(a) > 3 else 700; samples = int(a[4]) if len(a) > 4 else 48
KEY0, AMB0 = 5.0, 0.55
def hexlin(h):
    c = [int(h[i:i+2], 16)/255 for i in (0, 2, 4)]
    return [x/12.92 if x <= 0.04045 else ((x + 0.055)/1.055)**2.4 for x in c]
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = samples; sc.cycles.use_denoising = True; sc.cycles.seed = 0
sc.cycles.max_bounces = 0; sc.cycles.diffuse_bounces = 0; sc.cycles.glossy_bounces = 0; sc.cycles.transmission_bounces = 0
sc.render.resolution_x = sc.render.resolution_y = size; sc.render.resolution_percentage = 100
sc.view_settings.view_transform = 'Filmic'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.0
for o in bpy.data.objects:
    if o.type == 'LIGHT': o.hide_render = True
    if o.name == "PROTECTED_BODY": o.hide_render = True
amb_col, amb_e = hexlin("b7c9d2"), AMB0
if "A" in step: amb_col = hexlin("d9c7a8")
if "C" in step: amb_e = AMB0 * 0.25/0.35
w = bpy.data.worlds.new("DemoWorld"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = amb_col + [1]; w.node_tree.nodes["Background"].inputs[1].default_value = amb_e
kd = bpy.data.lights.new("DemoKey", 'SUN'); kd.color = hexlin("fff0df"); kd.angle = math.radians(0.25); kd.energy = KEY0
key = bpy.data.objects.new("DemoKey", kd); sc.collection.objects.link(key)
# sun direction given as where the light comes FROM: azimuth from Simm's front (-Y) toward -X (Simm's right), elevation
def aim_from(az, el):
    r, e = math.radians(az), math.radians(el); d = Vector((-math.sin(r)*math.cos(e), -math.cos(r)*math.cos(e), math.sin(e)))
    key.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
if "B" in step: aim_from(30 + 45, 45); kd.energy = KEY0 * 1.25      # ref camera sits at azimuth 30
else: aim_from(-35, 50)                                               # near-frontal, from the camera's right (native-like)
fl = bpy.data.materials.new("DemoFloor"); fl.use_nodes = True; fb = fl.node_tree.nodes["Principled BSDF"]
fb.inputs["Base Color"].default_value = hexlin("c8c0a5") + [1]; fb.inputs["Roughness"].default_value = 0.9; fb.inputs["Specular"].default_value = 0.2
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0)); bpy.context.active_object.data.materials.append(fl)
cd = bpy.data.cameras.new("DemoCam"); cd.sensor_width = 36; cam = bpy.data.objects.new("DemoCam", cd); sc.collection.objects.link(cam); sc.camera = cam
VIEWS = {"ref": (30, 15, 2.6*2.0), "alt": (72.3, 15, 2.6*2.0), "back": (180, 15, 2.6*2.0)}
tgt = Vector((0, 0, 0.72))
for v in views:
    az, el, dist = VIEWS[v]; r, e = math.radians(az), math.radians(el)
    dv = Vector((-math.sin(r)*math.cos(e), -math.cos(r)*math.cos(e), math.sin(e)))
    cd.lens = 84.7; cam.location = tgt + dv*dist; cam.rotation_euler = (tgt - cam.location).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = "%s_%s_%s.png" % (pre, step, v); bpy.ops.render.render(write_still=True); print("DEMO", sc.render.filepath)
