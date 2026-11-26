# ART-004 boot candidate v002: rigid two-part boots per leg (method accepted by Codex at 465ccf1; v002 brief at f98e519).
# v002: smooth continuous sole perimeter that always contains the upper, a softer shaft-to-foot transition with two
# restrained folds, and a sole rocker fitted to the measured foot-bone motion in idle, walk and gather.
# (v001 is in Git history at fe5cd45.)
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
        so = shell(name + "_SOLE_TMP", sole_bm, 0.0016, 3000)
        so.data.materials.clear(); so.data.materials.append(M_LEATHER); so.data.materials.append(M_SOLE)
        for p in so.data.polygons: p.material_index = 1
        ob.data.materials.append(M_SOLE)
        for o in bpy.context.view_layer.objects: o.select_set(o in (ob, so))
        bpy.context.view_layer.objects.active = ob; bpy.ops.object.join()
    ob.data.use_auto_smooth = True; ob.data.auto_smooth_angle = math.radians(80)
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
    bm = bmesh.new(); zs = list(np.linspace(SHAFT_BOT, SHAFT_TOP - 0.010, 30))
    fold = lambda z: 0.0025*math.exp(-((z - 0.186)/0.007)**2) + 0.0018*math.exp(-((z - 0.228)/0.008)**2)
    flare = lambda z: 0.007*sstep((0.185 - z)/0.060)          # widens toward the ankle, meeting the boot foot softly
    rxs = [0.060 + flare(z) + fold(z) + 0.004*sstep((z - 0.235)/0.045) for z in zs]
    rys = [0.064 + flare(z) + fold(z) + 0.003*sstep((z - 0.235)/0.045) for z in zs]
    c0 = ax(0.20); tube_z(bm, c0.x, c0.y, zs, rxs, rys, n_around=48)
    ct = ax(SHAFT_TOP - 0.010); czs = list(np.linspace(SHAFT_TOP - 0.022, SHAFT_TOP, 7))
    tube_z(bm, ct.x, ct.y, czs, [0.068 + 0.0035*math.sin(math.pi*(z - czs[0])/0.022) for z in czs], [0.071 + 0.0035*math.sin(math.pi*(z - czs[0])/0.022) for z in czs], n_around=48)
    shaft = finish("SCULPT_BOOT_SHAFT_" + tag, bm, "shin_" + side, 0.0018, 6000)
    # ---- foot: one lofted boot from heel to toe. The ankle part rises round the shaft's lower edge, the instep
    #      slopes to a rounded toe; a 22 mm sole and a 30 mm heel, in a darker sole material below the welt line.
    fx = ax(0.16).x
    base = [  # y (front is -Y), half-width, top: control points, resampled below with rounded ends in plan
        (0.090, 0.040, 0.134), (0.075, 0.054, 0.152), (0.050, 0.064, 0.166), (0.020, 0.071, 0.172), (-0.010, 0.071, 0.170),
        (-0.040, 0.069, 0.158), (-0.070, 0.066, 0.132), (-0.100, 0.064, 0.100), (-0.130, 0.063, 0.080), (-0.155, 0.060, 0.068),
        (-0.172, 0.055, 0.061), (-0.186, 0.044, 0.054)]
    Y0, Y1 = 0.094, -0.194                              # heel back and toe tip
    ys = list(np.linspace(Y0, Y1, 46)); by = [p_[0] for p_ in base][::-1]
    W = lambda y: float(np.interp(y, by, [p_[1] for p_ in base][::-1])); T = lambda y: float(np.interp(y, by, [p_[2] for p_ in base][::-1]))
    def endround(y, w):                                 # quarter-ellipse in plan over the last 18 mm at each end
        d = min(y - Y1, Y0 - y)
        return w*math.sqrt(max(0.0, 1.0 - (max(0.0, 0.018 - d)/0.018)**2)) if d < 0.018 else w
    # rocker: fitted to how the foot bone actually moves, so that no sole point goes below the floor in the clips
    lift_y = np.zeros(len(ys)); fb = rig.data.bones["foot_" + side]; R0 = fb.matrix_local.copy()
    samples = []
    if rig.animation_data is None: rig.animation_data_create()
    for an in ("idle", "walk", "gather"):
        act = bpy.data.actions[an]; rig.animation_data.action = act; f0, f1 = act.frame_range
        for fr in np.linspace(f0, f1, 49):
            bpy.context.scene.frame_set(int(fr), subframe=float(fr - int(fr)))
            samples.append(rig.matrix_world @ rig.pose.bones["foot_" + side].matrix @ R0.inverted())
    rig.animation_data.action = None; bpy.context.scene.frame_set(0)
    for pb_ in rig.pose.bones: pb_.matrix_basis.identity()
    for it in range(6):
        pen = np.zeros(len(ys))
        for i, y in enumerate(ys):
            w = endround(y, W(y)) + 0.003
            for xx in (fx - w, fx - 0.5*w, fx, fx + 0.5*w, fx + w):
                P = Vector((xx, y, lift_y[i]))
                pen[i] = max(pen[i], max(-(M @ P).z for M in samples))
        if pen.max() < 0.0005: break
        lift_y = lift_y + np.clip(pen, 0, None)
        lift_y = np.maximum.reduce([np.roll(lift_y, k) for k in (-1, 0, 1)])     # widen, then smooth
        for _ in range(2): lift_y = np.maximum(lift_y, 0.25*np.roll(lift_y, 1) + 0.5*lift_y + 0.25*np.roll(lift_y, -1))
        lift_y[0] = lift_y[1]; lift_y[-1] = lift_y[-2]
    lift_y = lift_y - lift_y.min()                      # the lowest part of the sole stays on the floor at rest
    print("ROCKER side %s: fitted in %d passes; lift at heel %.1f mm, mid-foot %.1f mm, toe %.1f mm; residual %.1f mm" % (side, it + 1, lift_y[0]*1000, lift_y[len(ys)//2]*1000, lift_y[-1]*1000, pen.max()*1000))
    L = lambda i: float(lift_y[i])
    bm = bmesh.new()
    loft(bm, [(y, fx, endround(y, W(y)), 0.006 + L(i), T(y)) for i, y in enumerate(ys)], n_around=48)
    sb = bmesh.new()                                   # sole: one shell round the whole outline, 4 mm proud, 22 mm, heel 30 mm
    ys2 = [Y0 + 0.004] + ys + [Y1 - 0.005]; lift2 = [L(0)] + [L(i) for i in range(len(ys))] + [L(len(ys)-1)]
    def solew(y):
        d = min(y - (Y1 - 0.005), (Y0 + 0.004) - y); w = W(min(max(y, Y1), Y0)) + 0.004
        return max(0.004, w*math.sqrt(max(0.0, 1.0 - (max(0.0, 0.022 - d)/0.022)**2)))
    heel_h = lambda y: HEEL_T if y > 0.000 else SOLE_T + (HEEL_T - SOLE_T)*sstep((y + 0.020)/0.020)
    loft(sb, [(y, fx, solew(y), lz, lz + heel_h(y)) for y, lz in zip(ys2, lift2)], n_around=48, expo=3.6)
    foot = finish("SCULPT_BOOT_FOOT_" + tag, bm, "foot_" + side, 0.0018, 8000, sole_bm=sb)
    parts += [shaft, foot]
for ob in parts:
    co = np.array([v.co[:] for v in ob.data.vertices])
    print("BOOT %-20s bone %-7s verts %5d tris %5d bounds min %s max %s" % (ob.name, ob["bind_bone"], len(co), sum(len(p.vertices)-2 for p in ob.data.polygons), np.round(co.min(0), 3), np.round(co.max(0), 3)))
bpy.ops.wm.save_as_mainfile(filepath=out)
