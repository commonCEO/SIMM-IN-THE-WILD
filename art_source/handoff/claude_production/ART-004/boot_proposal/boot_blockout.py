# ART-004 boot method proposal: THROWAWAY clay blockout, not a production asset.
# blender -b collar_packet_v004.blend --python boot_blockout.py -- <absolute out.blend> [rigid|blend]
# Adds SCULPT_BOOT_SHAFT_L/R (on shin_l/r) and SCULPT_BOOT_FOOT_L/R (on foot_l/r) with an armature modifier so the
# clips can be evaluated. Nothing on PROTECTED_BODY, the rig, the actions or the socket is changed.
# "blend" is the candidate-only alternative: the lowest 40 mm of each shaft blends shin -> foot (up to 50 percent).
import bpy, bmesh, sys, math, numpy as np
from mathutils import Vector
sys.dont_write_bytecode = True
argv = sys.argv[sys.argv.index("--")+1:]; out = argv[0]; mode = argv[1] if len(argv) > 1 else "rigid"
rig = bpy.data.objects["SimmRig"]; bd = bpy.data.objects["PROTECTED_BODY"]
coll = bpy.data.collections.get("20_SCULPT_BODY_PARTS") or bpy.data.collections.new("20_SCULPT_BODY_PARTS")
SHAFT_TOP, SHAFT_BOT = 0.290, 0.130
def fuse(name, bm, voxel, smooth=8):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    old = bpy.data.objects.get(name)
    if old: bpy.data.objects.remove(old)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob)
    for o in bpy.context.view_layer.objects: o.select_set(o is ob)
    bpy.context.view_layer.objects.active = ob
    md = ob.modifiers.new("fuse", 'REMESH'); md.mode = 'VOXEL'; md.voxel_size = voxel; bpy.ops.object.modifier_apply(modifier="fuse")
    md = ob.modifiers.new("relax", 'SMOOTH'); md.factor = 0.5; md.iterations = smooth; bpy.ops.object.modifier_apply(modifier="relax")
    for p in ob.data.polygons: p.use_smooth = True
    return ob
def ellipsoid(bm, c, r, seg=24):
    res = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg//2, radius=1.0)
    for v in res["verts"]: v.co = Vector((c[0] + v.co.x*r[0], c[1] + v.co.y*r[1], c[2] + v.co.z*r[2]))
def rounded_box(bm, lo, hi):
    res = bmesh.ops.create_cube(bm, size=1.0)
    for v in res["verts"]:
        v.co = Vector(tuple(lo[i] + (v.co[i] + 0.5)*(hi[i] - lo[i]) for i in range(3)))
parts = []
for sd, tag in ((-1, "L"), (1, "R")):                      # thigh_l / shin_l / foot_l are on -X in this rig
    side = "l" if sd < 0 else "r"
    sh = rig.data.bones["shin_" + side]; ft = rig.data.bones["foot_" + side]
    a0, a1 = Vector(sh.tail_local), Vector(sh.head_local)  # ankle (z 0.16) up to knee (z 0.345)
    # ---- shaft: a soft leather tube round the trouser leg, slightly wider at the top, with a turned-over cuff
    bm = bmesh.new(); rings = []
    for i in range(14):
        t = i/13; z = SHAFT_BOT + t*(SHAFT_TOP - SHAFT_BOT)
        u = (z - a0.z)/(a1.z - a0.z); ax = a0.lerp(a1, u)
        rx = 0.062 + 0.004*t; ry = 0.066 + 0.002*t
        ring = [bm.verts.new((ax.x + rx*math.cos(2*math.pi*k/28), ax.y + ry*math.sin(2*math.pi*k/28), z)) for k in range(28)]
        rings.append(ring)
    for i in range(13):
        for k in range(28): bm.faces.new((rings[i][k], rings[i][(k+1) % 28], rings[i+1][(k+1) % 28], rings[i+1][k]))
    bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])      # closed solid: the trouser leg inside is hidden
    u = (SHAFT_TOP - a0.z)/(a1.z - a0.z); ax = a0.lerp(a1, u)
    cuff = bmesh.ops.create_cone(bm, cap_ends=False, segments=28, radius1=0.075, radius2=0.072, depth=0.024)
    for v in cuff["verts"]: v.co = Vector((ax.x + v.co.x, ax.y + v.co.y, SHAFT_TOP - 0.010 + v.co.z))
    bmesh.ops.contextual_create(bm, geom=[v for v in cuff["verts"] if v.co.z > SHAFT_TOP])
    bmesh.ops.contextual_create(bm, geom=[v for v in cuff["verts"] if v.co.z < SHAFT_TOP - 0.015])
    shaft = fuse("SCULPT_BOOT_SHAFT_" + tag, bm, 0.0035)
    # ---- foot: heel, ankle, toe box and a restrained sole, fused; narrower and flatter than the original shoe
    fx = a0.x; bm = bmesh.new()
    ellipsoid(bm, (fx, 0.030, 0.075), (0.056, 0.060, 0.070))          # heel and back of the ankle
    ellipsoid(bm, (fx, -0.006, 0.122), (0.074, 0.080, 0.058))         # ankle collar, wider than the shaft so it wraps the shaft bottom
    ellipsoid(bm, (fx, -0.090, 0.062), (0.062, 0.085, 0.054))         # instep
    ellipsoid(bm, (fx, -0.150, 0.046), (0.060, 0.056, 0.042))         # rounded toe box
    ellipsoid(bm, (fx, -0.058, 0.013), (0.064, 0.150, 0.013))         # sole: a flat rounded slab under the whole foot, 26 mm
    foot = fuse("SCULPT_BOOT_FOOT_" + tag, bm, 0.0035)
    # ---- binding for evaluation only: shaft on shin, foot on foot (or the blend variant on the shaft)
    for ob, bone in ((shaft, "shin_" + side), (foot, "foot_" + side)):
        g = ob.vertex_groups.new(name=bone); g.add([v.index for v in ob.data.vertices], 1.0, 'REPLACE')
        ob.modifiers.new("Armature", 'ARMATURE').object = rig
    if mode == "blend":
        gf = shaft.vertex_groups.new(name="foot_" + side); gs = shaft.vertex_groups["shin_" + side]
        for v in shaft.data.vertices:
            w = max(0.0, min(1.0, (SHAFT_BOT + 0.040 - v.co.z)/0.040))*0.5
            if w > 0: gs.add([v.index], 1.0 - w, 'REPLACE'); gf.add([v.index], w, 'REPLACE')
    parts += [shaft, foot]
for ob in parts:
    print("BOOT %-20s verts %5d tris %6d bounds z %.3f..%.3f" % (ob.name, len(ob.data.vertices), sum(len(p.vertices)-2 for p in ob.data.polygons), min(v.co.z for v in ob.data.vertices), max(v.co.z for v in ob.data.vertices)))
bpy.ops.wm.save_as_mainfile(filepath=out)
