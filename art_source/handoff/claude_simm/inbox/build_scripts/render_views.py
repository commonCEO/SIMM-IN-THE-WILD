# Review renderer (Cycles CPU, headless). Usage:
# blender -b file.blend --python render_views.py -- outprefix mode(clay|colour) size samples views(comma) [body]
import bpy, sys, math
from mathutils import Vector
argv = sys.argv[sys.argv.index("--")+1:]
outprefix, mode, size, samples = argv[0], argv[1], int(argv[2]), int(argv[3])
views = argv[4].split(",")
show_body = len(argv) > 5 and argv[5] == "body"
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = samples
sc.cycles.use_denoising = True
sc.render.resolution_x = size; sc.render.resolution_y = size; sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.view_settings.view_transform = 'Standard'
sc.view_settings.look = 'None'
sc.render.threads_mode = 'AUTO'
# world: soft neutral ambient
w = bpy.data.worlds.new("ReviewWorld"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.62, 0.62, 0.64, 1) if mode == "clay" else (0.70, 0.66, 0.60, 1)
bg.inputs[1].default_value = 0.55
def add_light(name, kind, loc, energy, size_, color=(1,1,1)):
    d = bpy.data.lights.new(name, kind); d.energy = energy; d.color = color
    if kind == 'AREA': d.size = size_
    if kind == 'SUN': d.angle = size_
    o = bpy.data.objects.new(name, d); sc.collection.objects.link(o); o.location = loc
    return o
target = Vector((0, 0.0, 1.20))
def aim(o, tgt):
    d = (tgt - o.location); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
cam_d = bpy.data.cameras.new("ReviewCam"); cam_d.lens = 110; cam_d.sensor_width = 36
cam = bpy.data.objects.new("ReviewCam", cam_d); sc.collection.objects.link(cam); sc.camera = cam
key = add_light("Key", 'AREA', (0,0,0), 55, 1.2, (1.0, 0.97, 0.92)); 
fill = add_light("Fill", 'AREA', (0,0,0), 12, 2.0, (0.9, 0.95, 1.0))
# body visibility
for o in bpy.data.objects:
    if o.name == "PROTECTED_BODY": o.hide_render = not show_body
if mode == "clay":
    clay = bpy.data.materials.new("REVIEW_CLAY"); clay.use_nodes = True
    b = clay.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (0.55, 0.55, 0.55, 1); b.inputs["Roughness"].default_value = 0.6
    b.inputs["Specular"].default_value = 0.3
    bpy.context.view_layer.material_override = clay
VIEWS = {  # azimuth degrees from front (-Y) toward -X (character right), elevation degrees, distance
    "front": (0, 0, 2.6), "side": (90, 0, 2.6), "back": (180, 0, 2.6), "ref": (-30+60, 28, 2.6),
    "sideL": (-90, 0, 2.6), "top": (0, 80, 2.6), "q2": (-40, 10, 2.6), "low": (20, -20, 2.6), "bq": (140, 15, 2.6), "bq2": (-140, 15, 2.6),
}
# ref angle: face pointing to screen-right => camera rotated toward character's right (-X)
VIEWS["ref"] = (30, 15, 2.6)
VIEWS["alt"] = (72.3, 15, 2.6)      # Codex's exact alternate camera: Godot position (-1.576, 1.659, 0.502), target (0, 1.215, 0)
tz = float(argv[6]) if len(argv) > 6 else 1.21
dist_scale = float(argv[7]) if len(argv) > 7 else 1.0
target.z = tz
for v in views:
    az, el, dist = VIEWS[v]; dist *= dist_scale
    a = math.radians(az); e = math.radians(el)
    dirv = Vector((-math.sin(a)*math.cos(e), -math.cos(a)*math.cos(e), math.sin(e)))
    cam_d.lens = 84.7 if v in ("ref", "alt") else 110        # ref view matches Codex's Godot study: 24 degree FOV
    cam.location = target + dirv*dist; aim(cam, target)
    # key light: upper-left of camera, soft; fill from right
    right = Vector((math.cos(a), -math.sin(a), 0))
    key.location = target + dirv*1.6 + Vector((0,0,1.1)) - right*1.1; aim(key, target)
    fill.location = target + dirv*1.5 + right*1.6 + Vector((0,0,0.2)); aim(fill, target)
    sc.render.filepath = f"{outprefix}_{mode}_{v}.png"
    bpy.ops.render.render(write_still=True)
    print("RENDERED", sc.render.filepath)
