# ART-004 first packet: hood roll and front scarf for Simm. Static meshes in the frozen actor's coordinates,
# intended to follow the existing `chest` bone at 100 percent. The frozen body, rig and actions are not edited.
# blender -b <head_candidate_v007.blend> --python collar_build.py -- <out.blend>
import bpy, bmesh, sys, math, numpy as np
sys.dont_write_bytecode = True
out = sys.argv[sys.argv.index("--")+1]

def catmull(P, n, closed=False):
    P = np.asarray(P, float)
    if closed: ext = np.vstack([P[-1], P, P[0], P[1]]); segs = len(P)
    else: ext = np.vstack([2*P[0]-P[1], P, 2*P[-1]-P[-2]]); segs = len(P)-1
    out_ = []
    m = n if closed else n+1
    for k in range(m):
        s = k/n*segs; i = min(int(s), segs-1); t = s - i
        p0, p1, p2, p3 = ext[i], ext[i+1], ext[i+2], ext[i+3]
        out_.append(0.5*((2*p1) + (-p0+p2)*t + (2*p0-5*p1+4*p2-p3)*t*t + (-p0+3*p1-3*p2+p3)*t**3))
    return np.array(out_)

def tube(bm, ctrl, n=48, around=24, closed=False, lump=()):
    """ctrl rows: x, y, z, lateral radius, vertical radius. A soft cloth roll swept along the path.
    lump = list of (position 0..1, width, scale) pinches or swells that become folds after fusing."""
    C = catmull(ctrl, n, closed)
    P = C[:, :3]; R = C[:, 3:5]
    m = len(P)
    T = np.roll(P, -1, 0) - np.roll(P, 1, 0) if closed else np.gradient(P, axis=0)
    T /= np.linalg.norm(T, axis=1)[:, None]
    Z = np.array([0, 0, 1.0]); B = np.cross(T, Z); B /= np.maximum(np.linalg.norm(B, axis=1), 1e-9)[:, None]
    U = np.cross(B, T)
    rings = []
    for i in range(m):
        s = i/(m-1) if not closed else i/m
        k = 1.0
        for pos, wid, sc in lump: k *= 1 + (sc-1)*math.exp(-((s-pos)/wid)**2)
        ring = []
        for j in range(around):
            a = 2*math.pi*j/around
            ring.append(bm.verts.new(P[i] + B[i]*math.cos(a)*R[i, 0]*k + U[i]*math.sin(a)*R[i, 1]*k))
        rings.append(ring)
    for i in range(m if closed else m-1):
        a_, b_ = rings[i], rings[(i+1) % m]
        for j in range(around):
            j2 = (j+1) % around
            bm.faces.new((a_[j], a_[j2], b_[j2], b_[j]))
    if not closed:
        for ring, p, t, flip in ((rings[0], P[0], T[0], True), (rings[-1], P[-1], T[-1], False)):
            c = bm.verts.new(p + t*(-0.006 if flip else 0.006))
            for j in range(around):
                j2 = (j+1) % around
                bm.faces.new((ring[j2], ring[j], c) if flip else (ring[j], ring[j2], c))

def finish(bm, name, voxel, tris, colour_srgb, rough):
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    old = bpy.data.objects.get(name)
    if old: bpy.data.objects.remove(old)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    for o in bpy.context.view_layer.objects: o.select_set(o is ob)
    md = ob.modifiers.new("fuse", 'REMESH'); md.mode = 'VOXEL'; md.voxel_size = voxel; md.use_smooth_shade = True
    bpy.ops.object.modifier_apply(modifier="fuse")
    md = ob.modifiers.new("relax", 'SMOOTH'); md.factor = 0.5; md.iterations = 10
    bpy.ops.object.modifier_apply(modifier="relax")
    n = sum(len(p.vertices)-2 for p in ob.data.polygons)
    md = ob.modifiers.new("reduce", 'DECIMATE'); md.ratio = min(1.0, tris/max(n, 1))
    bpy.ops.object.modifier_apply(modifier="reduce")
    for p in ob.data.polygons: p.use_smooth = True
    ob.data.use_auto_smooth = True; ob.data.auto_smooth_angle = math.radians(80)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.004); bpy.ops.object.mode_set(mode='OBJECT')
    c = np.array(colour_srgb, float)/255.0; lin = np.where(c <= 0.04045, c/12.92, ((c+0.055)/1.055)**2.4)
    mat = bpy.data.materials.get("SCULPT_MAT_"+name.split("_", 1)[1]) or bpy.data.materials.new("SCULPT_MAT_"+name.split("_", 1)[1])
    mat.use_nodes = True; b = mat.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Specular"].default_value = 0.25; b.inputs["Metallic"].default_value = 0
    ob.data.materials.clear(); ob.data.materials.append(mat)
    # intended binding, recorded in the source: every vertex 100 percent on `chest`. No armature modifier is added.
    g = ob.vertex_groups.new(name="chest"); g.add(list(range(len(ob.data.vertices))), 1.0, 'REPLACE')
    ob.parent = root
    return ob

coll = bpy.data.collections.get("20_SCULPT_BODY_PARTS") or bpy.data.collections.new("20_SCULPT_BODY_PARTS")
if coll.name not in bpy.context.scene.collection.children: bpy.context.scene.collection.children.link(coll)
root = bpy.data.objects.get("SCULPT_COLLAR_ROOT") or bpy.data.objects.new("SCULPT_COLLAR_ROOT", None)
if root.name not in coll.objects: coll.objects.link(root)
root.empty_display_size = 0.05

# ---------------- hood: a soft horseshoe resting on the shoulders, fullest behind the neck, lapel ends on the chest
bm = bmesh.new()
# v002 (after Codex's native review of v001): the roll is narrower and slumps inward and back into the valley
# between the neck and the pack, instead of lying on the shoulders as a shelf. The lapel ends are short with
# rounded tips. The hood bag no longer runs over the pack flap: nothing of the hood lies behind Y 0.118.
HOOD = [  # x, y, z, lateral radius, vertical radius      (front is -Y, Simm's right is -X)
    (-0.064, -0.122, 0.939, .009, .005),      # tapered tip
    (-0.071, -0.112, 0.948, .020, .012),      # short rounded lapel end
    (-0.092, -0.084, 0.967, .027, .019),
    (-0.107, -0.036, 0.984, .030, .026),
    (-0.105,  0.026, 0.992, .032, .030),
    (-0.070,  0.068, 0.991, .033, .031),
    ( 0.002,  0.083, 0.987, .030, .031),      # back centre sits in the valley in front of the pack dome
    ( 0.074,  0.066, 0.989, .031, .029),
    ( 0.103,  0.024, 0.988, .031, .027),
    ( 0.103, -0.038, 0.981, .029, .024),
    ( 0.087, -0.086, 0.964, .025, .018),
    ( 0.067, -0.111, 0.946, .018, .011),
    ( 0.061, -0.120, 0.938, .008, .005)]
tube(bm, HOOD, n=80, around=26, lump=[(.14, .03, .84), (.30, .05, 1.14), (.50, .04, .90), (.66, .05, 1.12), (.86, .03, .86)])
# what is left of the hood bag: a soft bunch along the back of the roll, leaning back but stopping short of the pack
BAG = [(-0.060, 0.082, 1.000, .019, .012), (-0.004, 0.094, 1.003, .022, .014), (0.052, 0.086, 0.999, .017, .011)]
tube(bm, BAG, n=22, around=18)
# one inner fold along the top on Simm's right, and a shorter one on his left, of different thickness
FOLD = [(-0.110, -0.004, 1.000, .014, .010), (-0.103, 0.040, 1.006, .019, .012), (-0.074, 0.072, 1.005, .016, .010)]
tube(bm, FOLD, n=22, around=16)
FOLD2 = [(0.106, 0.002, 0.998, .012, .008), (0.094, 0.044, 1.002, .014, .009)]
tube(bm, FOLD2, n=14, around=14)
hood = finish(bm, "SCULPT_HOOD", 0.0024, 7000, (228, 172, 44), 0.86)

# ---------------- scarf: a pale soft band round the neck inside the collar, lower in front, one short end tucked forward
bm = bmesh.new()
RING = []
for k in range(12):
    a = 2*math.pi*k/12                      # a = 0 is the front
    x = 0.071*math.sin(a); y = -0.006 - 0.067*math.cos(a)
    z = 0.981 - 0.011*math.cos(a) + 0.003*math.sin(2*a)
    RING.append((x, y, z, .019 + .003*math.cos(a), .022 - .003*math.cos(a)))
tube(bm, RING, n=72, around=22, closed=True, lump=[(.06, .03, .88), (.33, .04, 1.07), (.70, .04, .92)])
# v002: no hanging end. The end is tucked straight down into the shirt opening and is almost entirely hidden.
END = [(0.020, -0.066, 0.970, .014, .010), (0.021, -0.072, 0.958, .010, .007), (0.021, -0.074, 0.949, .005, .004)]
tube(bm, END, n=14, around=14)
# the wrap-over is lower and thinner than in v001: an asymmetric fold, not a raised loop
WRAP = [(-0.058, -0.032, 0.984, .010, .011), (-0.040, -0.061, 0.982, .013, .013), (-0.004, -0.076, 0.977, .014, .013),
        (0.028, -0.069, 0.972, .011, .010), (0.044, -0.050, 0.969, .007, .007)]
tube(bm, WRAP, n=24, around=16)
scarf = finish(bm, "SCULPT_SCARF", 0.0022, 4000, (228, 210, 178), 0.90)

for o in (hood, scarf):
    print("PART", o.name, "verts", len(o.data.vertices), "tris", sum(len(p.vertices)-2 for p in o.data.polygons))
tx = bpy.data.texts.get("SCULPT_COLLAR_NOTES") or bpy.data.texts.new("SCULPT_COLLAR_NOTES")
tx.clear(); tx.write("ART-004 first packet. SCULPT_HOOD and SCULPT_SCARF are static meshes in actor coordinates. Each carries a single vertex group `chest` at weight 1.0 to record the intended binding. No armature modifier, no change to SimmRig, PROTECTED_BODY, actions or socket.\n")
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out)
