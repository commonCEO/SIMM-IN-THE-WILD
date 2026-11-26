# ART-004 boot candidate v001: rigid two-part boots per leg (method accepted by Codex at 465ccf1).
# blender -b <file with PROTECTED_BODY and SimmRig, e.g. work/collar_packet_v004.blend> --python boot_build.py -- <absolute out.blend>
# Four static parts in actor space under SCULPT_BOOTS_ROOT. Each carries one vertex group at 1.0 naming the existing
# bone it follows (shaft: shin_l / shin_r, foot: foot_l / foot_r) and a custom property "bind_bone" with the same
# name. No armature modifier. PROTECTED_BODY, the rig, the actions and the socket are read, never written.
import bpy, bmesh, sys, math, numpy as np
from mathutils import Vector
sys.dont_write_bytecode = True
out = sys.argv[sys.argv.index("--")+1]
rig = bpy.data.objects["SimmRig"]; bd = bpy.data.objects["PROTECTED_BODY"]
coll = bpy.data.collections.get("20_SCULPT_BODY_PARTS") or bpy.data.collections.new("20_SCULPT_BODY_PARTS")
if coll.name not in [c.name for c in bpy.context.scene.collection.children]: bpy.context.scene.collection.children.link(coll)
root = bpy.data.objects.get("SCULPT_BOOTS_ROOT") or bpy.data.objects.new("SCULPT_BOOTS_ROOT", None)
if root.name not in coll.objects: coll.objects.link(root)
root.empty_display_size = 0.05
def srgb_of(m):
    b = m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value; return tuple(b[:3])
LEATHER = srgb_of(bpy.data.materials["Simm brown boot leather"]); SOLE = srgb_of(bpy.data.materials["Simm dark soles"])
def material(name, lin, rough):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (*lin, 1.0)
    b.inputs["Roughness"].default_value = rough; b.inputs["Specular"].default_value = 0.25; return m
M_LEATHER = material("SCULPT_MAT_BOOT_LEATHER", LEATHER, 0.72); M_SOLE = material("SCULPT_MAT_BOOT_SOLE", SOLE, 0.85)
sstep = lambda t: 0.0 if t <= 0 else 1.0 if t >= 1 else t*t*(3-2*t)
def loft(bm, rings_spec, n_around=40, expo=3.0):
    """rings_spec: list of (y, cx, w, zlo, zhi) cross-sections in the x-z plane; a rounded-box superellipse each."""
    rings = []
    for y, cx, w, zlo, zhi in rings_spec:
        zc = 0.5*(zlo + zhi); hz = 0.5*(zhi - zlo); ring = []
        for k in range(n_around):
            a = 2*math.pi*k/n_around; c, s = math.cos(a), math.sin(a)
            ring.append(bm.verts.new((cx + w*math.copysign(abs(c)**(2/expo), c), y, zc + hz*math.copysign(abs(s)**(2/expo), s))))
        rings.append(ring)
    for i in range(len(rings)-1):
        for k in range(n_around): bm.faces.new((rings[i][k], rings[i][(k+1) % n_around], rings[i+1][(k+1) % n_around], rings[i+1][k]))
    bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])
def tube_z(bm, cx, cy, zs, rx, ry, n_around=40):
    rings = []
    for z, sx, sy in zip(zs, rx, ry):
        rings.append([bm.verts.new((cx + sx*math.cos(2*math.pi*k/n_around), cy + sy*math.sin(2*math.pi*k/n_around), z)) for k in range(n_around)])
    for i in range(len(rings)-1):
        for k in range(n_around): bm.faces.new((rings[i][k], rings[i][(k+1) % n_around], rings[i+1][(k+1) % n_around], rings[i+1][k]))
    bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])
def shell(name, bm, voxel, tris):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    old = bpy.data.objects.get(name)
    if old: bpy.data.objects.remove(old)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob)
    for o in bpy.context.view_layer.objects: o.select_set(o is ob)
    bpy.context.view_layer.objects.active = ob
    md = ob.modifiers.new("fuse", 'REMESH'); md.mode = 'VOXEL'; md.voxel_size = voxel; bpy.ops.object.modifier_apply(modifier="fuse")
    md = ob.modifiers.new("relax", 'SMOOTH'); md.factor = 0.5; md.iterations = 6; bpy.ops.object.modifier_apply(modifier="relax")
    n = sum(len(p.vertices)-2 for p in ob.data.polygons)
    md = ob.modifiers.new("reduce", 'DECIMATE'); md.ratio = min(1.0, tris/max(n, 1)); bpy.ops.object.modifier_apply(modifier="reduce")
    for p in ob.data.polygons: p.use_smooth = True
    return ob
def finish(name, bm, bone, voxel, tris, sole_bm=None):
    ob = shell(name, bm, voxel, tris)
    ob.data.materials.clear(); ob.data.materials.append(M_LEATHER)
    if sole_bm is not None:                         # a separate clean sole shell, joined into the same part
        so = shell(name + "_SOLE_TMP", sole_bm, 0.0020, 1200)
        so.data.materials.clear(); so.data.materials.append(M_LEATHER); so.data.materials.append(M_SOLE)
        for p in so.data.polygons: p.material_index = 1
        ob.data.materials.append(M_SOLE)
        for o in bpy.context.view_layer.objects: o.select_set(o in (ob, so))
        bpy.context.view_layer.objects.active = ob; bpy.ops.object.join()
    ob.data.use_auto_smooth = True; ob.data.auto_smooth_angle = math.radians(60)
    for o in bpy.context.view_layer.objects: o.select_set(o is ob)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.004); bpy.ops.object.mode_set(mode='OBJECT')
    g = ob.vertex_groups.new(name=bone); g.add(list(range(len(ob.data.vertices))), 1.0, 'REPLACE')
    ob["bind_bone"] = bone; ob.parent = root
    return ob
SHAFT_BOT, SHAFT_TOP, SOLE_T, HEEL_T = 0.100, 0.290, 0.022, 0.030   # shaft bottom sunk 28 mm deeper into the boot foot
parts = []
for sd, tag, side in ((-1, "L", "l"), (1, "R", "r")):         # *_l bones are on -X in this rig
    sh = rig.data.bones["shin_" + side]; a0, a1 = Vector(sh.tail_local), Vector(sh.head_local)
    ax = lambda z: a0.lerp(a1, (z - a0.z)/(a1.z - a0.z))
    # ---- shaft: one smooth leather tube, slightly wider at the top, ending in a soft turned-down cuff
    bm = bmesh.new(); zs = list(np.linspace(SHAFT_BOT, SHAFT_TOP - 0.012, 12))
    c0 = ax(0.20); tube_z(bm, c0.x, c0.y, zs, [0.060 + 0.006*sstep((z - 0.18)/0.11) for z in zs], [0.064 + 0.004*sstep((z - 0.18)/0.11) for z in zs])
    ct = ax(SHAFT_TOP - 0.010); czs = list(np.linspace(SHAFT_TOP - 0.030, SHAFT_TOP, 7))
    tube_z(bm, ct.x, ct.y, czs, [0.071 + 0.004*math.sin(math.pi*(z - czs[0])/0.030) for z in czs], [0.075 + 0.004*math.sin(math.pi*(z - czs[0])/0.030) for z in czs])
    shaft = finish("SCULPT_BOOT_SHAFT_" + tag, bm, "shin_" + side, 0.0022, 5000)
    # ---- foot: one lofted boot from heel to toe. The ankle part rises round the shaft's lower edge, the instep
    #      slopes to a rounded toe; a 22 mm sole and a 30 mm heel, in a darker sole material below the welt line.
    fx = ax(0.16).x
    prof = [  # y (front is -Y), half-width, top
        (0.090, 0.030, 0.105), (0.080, 0.046, 0.140), (0.060, 0.058, 0.160), (0.030, 0.068, 0.168), (0.000, 0.071, 0.168),
        (-0.030, 0.069, 0.160), (-0.060, 0.066, 0.140), (-0.090, 0.064, 0.105), (-0.120, 0.063, 0.082), (-0.150, 0.061, 0.068),
        (-0.170, 0.056, 0.060), (-0.182, 0.046, 0.054), (-0.190, 0.028, 0.046)]   # toe tip at the original's length
    bm = bmesh.new()
    # a rocker sole: toe spring over the front 70 mm and a rounded heel edge, so the boot rolls with the foot
    # bone in the walk instead of digging its toe or heel corner into the floor
    lift = lambda y: 0.022*sstep((-0.105 - y)/0.085)**1.4 + 0.018*sstep((y - 0.040)/0.050)**1.6
    loft(bm, [(y, fx, w, 0.004 + lift(y), top) for y, w, top in prof])
    sb = bmesh.new()                                   # sole: 3 mm proud of the upper all round, 22 mm, heel 30 mm
    loft(sb, [(y, fx, w + 0.003, lift(y), lift(y) + SOLE_T) for y, w, top in prof[1:-1]], expo=5.0)
    loft(sb, [(y, fx, w, lift(y), max(HEEL_T, lift(y) + SOLE_T)) for y, w in ((0.084, 0.044), (0.070, 0.058), (0.020, 0.063), (-0.012, 0.061))], expo=5.0)
    foot = finish("SCULPT_BOOT_FOOT_" + tag, bm, "foot_" + side, 0.0022, 6000, sole_bm=sb)
    parts += [shaft, foot]
for ob in parts:
    co = np.array([v.co[:] for v in ob.data.vertices])
    print("BOOT %-20s bone %-7s verts %5d tris %5d bounds min %s max %s" % (ob.name, ob["bind_bone"], len(co), sum(len(p.vertices)-2 for p in ob.data.polygons), np.round(co.min(0), 3), np.round(co.max(0), 3)))
bpy.ops.wm.save_as_mainfile(filepath=out)
