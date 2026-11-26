# ART-004 collar: hood and front scarf for Simm (v003; v001 and v002 are in Git history). Static meshes in the frozen actor's coordinates,
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

# ---------------- hood v003: a standing, bunched hood around the neck, after the user's review of the native side view
# v002 lay on the shoulders and left up to 9 cm of bare neck at the sides and 6 cm at the back. In the reference
# the head sits down in the hood. v003 stands up around the neck to just under the jaw and the hair line, fitted to
# the head mesh in this file: inner surface 11 mm off the neck skin, top below the jaw and the hair tips.
bm = bmesh.new()
CX, CY = 0.0, 0.040                                  # neck centre in plan view
hv = np.array([v.co[:] for v in bpy.data.objects["SCULPT_HEAD"].data.vertices]) @ np.array(bpy.data.objects["SCULPT_HEAD"].matrix_world)[:3, :3].T + np.array(bpy.data.objects["SCULPT_HEAD"].matrix_world)[:3, 3]
h_az = np.degrees(np.arctan2(hv[:, 0]-CX, -(hv[:, 1]-CY))); h_r = np.hypot(hv[:, 0]-CX, hv[:, 1]-CY)
#        |az|  base   top    thickness (radial)
PROF = [( 38, 0.976, 1.004, 0.026), ( 50, 0.978, 1.020, 0.028), ( 65, 0.980, 1.036, 0.030), ( 80, 0.982, 1.050, 0.032),
        (100, 0.983, 1.060, 0.034), (125, 0.986, 1.062, 0.036), (150, 0.990, 1.054, 0.039), (180, 0.994, 1.045, 0.042)]
P_az = np.array([p_[0] for p_ in PROF], float)
def prof(a, i): return float(np.interp(abs(a), P_az, [p_[i] for p_ in PROF]))
def r_inner(a, zb, zt):
    m = (np.abs(((h_az - a + 180) % 360) - 180) < 9) & (hv[:, 2] > zb) & (hv[:, 2] < zt + 0.008) & (h_r < 0.095)
    return (h_r[m].max() if m.any() else 0.06) + 0.011
rows = []
for a in list(range(-38, -181, -8)) + [-180] + list(range(172, 37, -8)) + [38]:
    if a == -180: a = 180.0
    zb, zt, t = prof(a, 1), prof(a, 2), prof(a, 3)
    rc = r_inner(a, zb, zt) + t/2
    ar = math.radians(a)
    rows.append((CX + rc*math.sin(ar), CY - rc*math.cos(ar), 0.5*(zb + zt), t/2, 0.5*(zt - zb)))
rows = sorted(rows, key=lambda r_: math.atan2(r_[0], -(r_[1]-CY)) % (2*math.pi))   # from Simm's left front, round the back
# the stand turns down into short lapels on the chest at each front edge (v002 lapel ends kept)
# short, flat turn-downs: the stand folds over onto the chest and ends, it does not hang as a separate roll
LAP_R = [(-0.074, -0.100, 0.962, .010, .005), (-0.082, -0.088, 0.970, .019, .009), (-0.090, -0.068, 0.978, .022, .012)]
LAP_L = [(0.089, -0.068, 0.978, .021, .012), (0.080, -0.088, 0.970, .018, .009), (0.072, -0.100, 0.962, .009, .005)]
left = [r_ for r_ in rows if r_[0] > 0]; right = [r_ for r_ in rows if r_[0] <= 0]
left.sort(key=lambda r_: -r_[1]); right.sort(key=lambda r_: r_[1])         # left side from back to front, right from front to back
HOOD = LAP_R + right + left + LAP_L
tube(bm, HOOD, n=150, around=28, lump=[(.12, .03, .88), (.25, .04, 1.10), (.36, .03, .92), (.46, .05, 1.12), (.56, .03, .90), (.66, .04, 1.10), (.78, .03, .93), (.90, .03, .88)])
# gathered hood cloth bunched behind the neck, sitting on the stand and on top of the pack, not over the flap
BUNCH = [(-0.060, 0.128, 1.012, .022, .020), (-0.020, 0.146, 1.020, .026, .024), (0.024, 0.144, 1.016, .025, .022), (0.062, 0.124, 1.010, .020, .018)]
tube(bm, BUNCH, n=30, around=20, lump=[(.30, .10, 1.10), (.70, .10, .92)])
# a soft rolled top lip on the stand, uneven in thickness, longer on Simm's right
LIP_R = [r_ for r_ in right if 70 < abs(math.degrees(math.atan2(r_[0], -(r_[1]-CY)))) < 175]
FOLD = [(x_*1.02, CY + (y_-CY)*1.02, z_ + v_*0.85, 0.011, 0.009) for x_, y_, z_, l_, v_ in LIP_R]
if len(FOLD) > 2: tube(bm, FOLD, n=3*len(FOLD), around=14)
hood = finish(bm, "SCULPT_HOOD", 0.0024, 9000, (228, 172, 44), 0.86)

# ---------------- scarf: a pale soft band round the neck inside the collar, lower in front, one short end tucked forward
bm = bmesh.new()
RING = []
for k in range(12):
    a = 2*math.pi*k/12                      # a = 0 is the front
    x = 0.071*math.sin(a); y = -0.006 - 0.067*math.cos(a)
    z = 0.990 - 0.008*max(0.0, math.cos(a))**3 + 0.003*math.sin(2*a)   # v003: raised; dips in a soft V at the throat
    RING.append((x, y, z, .015 + .002*math.cos(a), .017 - .003*math.cos(a)))   # thinner than v002, cloth not a pillow
tube(bm, RING, n=72, around=22, closed=True, lump=[(.04, .03, .80), (.12, .03, 1.12), (.33, .04, 1.07), (.70, .04, .92), (.93, .03, 1.10)])
# v002: no hanging end. The end is tucked straight down into the shirt opening and is almost entirely hidden.
END = [(0.020, -0.066, 0.982, .014, .010), (0.021, -0.072, 0.966, .010, .007), (0.021, -0.074, 0.952, .005, .004)]
tube(bm, END, n=14, around=14)
# the wrap-over is lower and thinner than in v001: an asymmetric fold, not a raised loop
WRAP = [(-0.058, -0.032, 0.997, .010, .011), (-0.040, -0.060, 0.996, .013, .013), (-0.004, -0.074, 0.992, .014, .013),
        (0.028, -0.068, 0.987, .011, .010), (0.044, -0.050, 0.984, .007, .007)]
tube(bm, WRAP, n=24, around=16)
scarf = finish(bm, "SCULPT_SCARF", 0.0022, 4000, (228, 210, 178), 0.90)

for o in (hood, scarf):
    print("PART", o.name, "verts", len(o.data.vertices), "tris", sum(len(p.vertices)-2 for p in o.data.polygons))
tx = bpy.data.texts.get("SCULPT_COLLAR_NOTES") or bpy.data.texts.new("SCULPT_COLLAR_NOTES")
tx.clear(); tx.write("ART-004 first packet. SCULPT_HOOD and SCULPT_SCARF are static meshes in actor coordinates. Each carries a single vertex group `chest` at weight 1.0 to record the intended binding. No armature modifier, no change to SimmRig, PROTECTED_BODY, actions or socket.\n")
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out)
