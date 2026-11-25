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
HOOD = [  # x, y, z, lateral radius, vertical radius      (front is -Y, Simm's right is -X)
    (-0.058, -0.127, 0.898, .026, .010),      # flat lapel end lying on the chest
    (-0.084, -0.104, 0.948, .032, .017),
    (-0.115, -0.046, 0.980, .040, .026),
    (-0.124,  0.030, 0.990, .047, .031),
    (-0.092,  0.104, 0.988, .056, .034),
    ( 0.004,  0.140, 0.980, .062, .036),      # fullest behind the neck, wider than tall: slumped cloth, not a ring
    ( 0.096,  0.098, 0.986, .050, .032),
    ( 0.119,  0.026, 0.986, .042, .028),
    ( 0.110, -0.048, 0.977, .036, .023),
    ( 0.081, -0.104, 0.946, .029, .015),
    ( 0.056, -0.126, 0.896, .023, .009)]
tube(bm, HOOD, n=80, around=26, lump=[(.18, .03, .82), (.33, .05, 1.12), (.52, .04, .90), (.68, .05, 1.10), (.84, .03, .84)])
# the hood's own bag, slumped over the top of the pack between the shoulders
DRAPE = [(0.000, 0.150, 0.984, .074, .030), (0.004, 0.188, 0.972, .062, .022), (0.008, 0.218, 0.950, .044, .015),
         (0.010, 0.238, 0.922, .024, .009), (0.011, 0.246, 0.902, .009, .004)]
tube(bm, DRAPE, n=28, around=22)
# two inner folds lying along the top of the roll, different lengths, so it reads as bunched cloth
FOLD = [(-0.124, 0.006, 0.998, .017, .011), (-0.108, 0.074, 1.000, .022, .012), (-0.056, 0.128, 0.998, .022, .012), (0.004, 0.144, 0.994, .014, .009)]
tube(bm, FOLD, n=28, around=16)
FOLD2 = [(0.120, -0.020, 0.996, .014, .010), (0.116, 0.042, 0.999, .019, .011), (0.082, 0.104, 0.998, .016, .010)]
tube(bm, FOLD2, n=20, around=16)
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
END = [(0.026, -0.078, 0.972, .022, .013), (0.038, -0.112, 0.944, .020, .011), (0.044, -0.127, 0.914, .016, .009), (0.046, -0.131, 0.896, .008, .005)]
tube(bm, END, n=22, around=18)
# the wrap-over: a second layer crossing the front, slightly higher on Simm's right, so the band is not a plain collar
WRAP = [(-0.062, -0.030, 0.992, .012, .014), (-0.046, -0.064, 0.990, .017, .017), (-0.006, -0.082, 0.983, .019, .018),
        (0.030, -0.074, 0.976, .017, .015), (0.050, -0.052, 0.973, .010, .010)]
tube(bm, WRAP, n=26, around=18)
scarf = finish(bm, "SCULPT_SCARF", 0.0022, 4000, (228, 210, 178), 0.90)

for o in (hood, scarf):
    print("PART", o.name, "verts", len(o.data.vertices), "tris", sum(len(p.vertices)-2 for p in o.data.polygons))
tx = bpy.data.texts.get("SCULPT_COLLAR_NOTES") or bpy.data.texts.new("SCULPT_COLLAR_NOTES")
tx.clear(); tx.write("ART-004 first packet. SCULPT_HOOD and SCULPT_SCARF are static meshes in actor coordinates. Each carries a single vertex group `chest` at weight 1.0 to record the intended binding. No armature modifier, no change to SimmRig, PROTECTED_BODY, actions or socket.\n")
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out)
