# Review only, never saved. Unlit view of the m002 jacket parts: each material is replaced by an emission of its albedo
# map (strength 1, Standard view transform, no look, exposure 0), so an on-screen pixel equals the texture's sRGB value.
# The same view in an engine with an unshaded material should give the same numbers; a lighter, washed-out result means
# the albedo was read as linear, a darker one means it was converted twice.
#   blender -b work/jacket_material_m002.blend --python build_scripts/jacket_m002_neutral_preview.py -- <out prefix> [size]
import bpy, sys, math
a = sys.argv[sys.argv.index("--")+1:]; pre = a[0]; size = int(a[1]) if len(a) > 1 else 512
PARTS = ("SCULPT_JACKET_LONG", "SCULPT_JACKET_LONG_TRIM", "SCULPT_JACKET_POCKETS")
sc = bpy.context.scene; rig = bpy.data.objects["SimmRig"]; rig.data.pose_position = 'REST'
for o in bpy.data.objects:
    if o.type in ('MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'GPENCIL') and o.name not in PARTS: o.hide_render = True
for n in PARTS:
    o = bpy.data.objects[n]; o.hide_render = False
    for s in o.material_slots:
        src = s.material; m = bpy.data.materials.new("UNLIT_" + src.name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
        tex = [x for x in src.node_tree.nodes if x.type == 'TEX_IMAGE' and x.image.colorspace_settings.name == 'sRGB'][0]
        uv = nt.nodes.new("ShaderNodeUVMap"); uv.uv_map = "M002_UV"; t = nt.nodes.new("ShaderNodeTexImage"); t.image = tex.image
        em = nt.nodes.new("ShaderNodeEmission"); ou = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(uv.outputs["UV"], t.inputs["Vector"]); nt.links.new(t.outputs["Color"], em.inputs["Color"]); nt.links.new(em.outputs[0], ou.inputs["Surface"])
        s.material = m
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 16; sc.cycles.use_denoising = False; sc.cycles.seed = 0
sc.render.resolution_x = sc.render.resolution_y = size; sc.render.resolution_percentage = 100
sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0; sc.view_settings.gamma = 1
w = bpy.data.worlds.new("NeutralWorld"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.214, 0.214, 0.214, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 1.0   # sRGB 128 grey
cd = bpy.data.cameras.new("NeutralCam"); cd.type = 'ORTHO'; cd.ortho_scale = 0.62
cam = bpy.data.objects.new("NeutralCam", cd); sc.collection.objects.link(cam); sc.camera = cam
for tag, ang in (("front", 0.0), ("back", 180.0)):
    r = math.radians(ang); cam.location = (2.0*math.sin(r), -2.0*math.cos(r), 0.73)
    cam.rotation_euler = (math.radians(90), 0, r)
    sc.render.filepath = "%s_%s.png" % (pre, tag); bpy.ops.render.render(write_still=True); print("NEUTRAL", sc.render.filepath)
