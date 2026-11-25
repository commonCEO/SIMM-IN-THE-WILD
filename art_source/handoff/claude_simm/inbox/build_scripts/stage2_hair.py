# Stage 2: hair. work/stage1.blend -> work/stage2.blend
# Built like a clay sculpt: (1) one thick hair mass over the scalp, (2) hand-placed clumps merged into it at the
# roots, (3) thin accent strands, then everything fused into a single surface and relaxed.
# Each clump is an individually authored guide path: (azimuth, elevation, offset from the hair-mass surface in m).
# azimuth 0 = face front, + = Simm's left (+X), - = Simm's right (-X), 180 = back. elevation 90 = crown.
import bpy, bmesh, sys, os, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, hairkit; importlib.reload(hairkit)
from hairkit import *
argv = sys.argv[sys.argv.index("--")+1:]
out = argv[0]; VOX = float(argv[1]) if len(argv) > 1 else 0.0024; TRIS = int(argv[2]) if len(argv) > 2 else 36000
face = bpy.data.objects["SCULPT_BASE_FACE"]
coll = bpy.data.collections["10_SCULPT_NEW_HEAD"]
scalp = Scalp(face)
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)

# ---------------- hairline: elevation above which the scalp carries hair, by |azimuth|
HL_AZ = [0, 25, 50, 68, 80, 92, 106, 120, 150, 180]
HL_EL = [29, 28, 19, 5, 1, 0, -3, -26, -30, -31]      # stays above the ear so the mass never cuts through it
def wrap(az): return ((az + 180) % 360) - 180
def hairline(az): return float(np.interp(abs(wrap(az)), HL_AZ, HL_EL))
def mass(az, el):
    """thickness of the primary hair mass above the skin (v002: a big airy volume, heavier on Simm's right)"""
    hl = hairline(az); a = wrap(az); back = sstep((abs(a) - 90)/70)
    heavy = sstep((a + 160)/50)*sstep((-15 - a)/50)*sstep((el - hl)/30)
    crown = sstep((el - 60)/22)
    side = sstep((abs(a) - 55)/30)*sstep((150 - abs(a))/40)*sstep((el - hl)/26)*sstep((78 - el)/30)
    front = sstep((70 - abs(a))/20)
    return 0.004 + (0.008 - 0.004*front)*sstep((el - (hl-10))/10) + (0.037 + 0.006*back)*sstep((el - hl)/32) + 0.010*heavy + 0.010*crown + 0.014*side

bm = bmesh.new()
# ---------------- 1. primary mass: a clean shell on the real skull, rim rolled under at the hairline
NA, NE = 120, 26
grid = []
for i in range(NA):
    az = -180 + 360*i/NA; hl = hairline(az); col = []
    for j in range(NE+1):
        t = j/NE; el = hl + (89.2 - hl)*t
        col.append(bm.verts.new(scalp.point(az, el, mass(az, el))))
    col.insert(0, bm.verts.new(scalp.point(az, hl - 6, 0.0015)))     # thin feathered rim
    col.insert(0, bm.verts.new(scalp.point(az, hl - 5, -0.006)))     # tucked under the skin
    col.append(None); grid.append(col)
topv = bm.verts.new(scalp.point(0, 90, mass(0, 90)))
innerc = bm.verts.new(tuple(HC + np.array([0, 0, 0.05])))
for i in range(NA):
    a, b = grid[i], grid[(i+1) % NA]
    for j in range(NE+2):
        bm.faces.new((a[j], b[j], b[j+1], a[j+1]))
    bm.faces.new((a[NE+2], b[NE+2], topv))
    bm.faces.new((b[0], a[0], innerc))                                 # close the volume inside the head

# ---------------- 2/3. clumps and strands
GUIDES = []
def L(name, pts, w, t=0.016, n=16, **kw):
    P = [scalp.point(a, e, mass(a, e) + r) for a, e, r in pts]
    kw.setdefault('under', 0.9)      # undersides sink into the mass: no hollow gaps beneath a clump
    GUIDES.append((name, P)); sweep(bm, catmull(P, n), w, thick=t, **kw)

# v002 layout, read from the full-resolution reference: a few bold windswept clumps radiating from the crown,
# fringe swept across the forehead toward Simm's left, heavy mass over his right temple and ear, flicks kicking
# out on his left, one tall tuft at the top.
BIG = dict(t=.026)
# ===== fringe: parted above Simm's right eye, swept diagonally toward his left
L("fringe_1", [(-30, 66, -.010), (-18, 42, .002), (-6, 16, .006), (7, -11, .009)], .100, t=.022, grooves=[(-.3, .4), (.3, .35)], ridge_at=.15, tip_pow=2.6)
L("fringe_2", [(-22, 70, -.010), (-4, 48, .002), (14, 22, .006), (30, -10, .009)], .098, t=.022, grooves=[(.25, .4)], ridge_at=-.2, tip_pow=2.6)
L("fringe_3", [(-12, 73, -.010), (10, 52, .003), (33, 25, .007), (50, -9, .012)], .098, t=.022, grooves=[(-.2, .4), (.35, .3)], ridge_at=.2, tip_pow=2.6)
L("fringe_4", [(0, 75, -.010), (26, 57, .004), (51, 31, .010), (71, -3, .026)], .092, t=.022, grooves=[(.2, .4)], ridge_at=-.2, tip_pow=2.6)
L("fringe_short", [(-37, 62, -.008), (-35, 45, .003), (-33, 24, .005), (-29, 0, .006)], .076, t=.018, grooves=[(0, .35)], tip_pow=2.4)
L("fringe_5", [(8, 76, -.010), (38, 64, .004), (62, 46, .010), (80, 26, .020)], .090, t=.022, grooves=[(.1, .4)], ridge_at=.2, tip_pow=2.2)
# ===== Simm's right (screen-left): heavy mass over temple and ear, tips kicking out
L("right_temple", [(-41, 66, -.010), (-53, 44, .003), (-63, 18, .009), (-68, -14, .014)], .114, grooves=[(-.25, .4), (.3, .35)], ridge_at=.2, tip_pow=2.4, **BIG)
L("right_ear",    [(-53, 69, -.010), (-69, 48, .005), (-83, 28, .016), (-94, 8, .046)], .104, grooves=[(.2, .4)], ridge_at=-.2, **BIG)
L("right_flick",  [(-65, 71, -.010), (-87, 54, .008), (-103, 36, .028), (-114, 20, .066)], .098, grooves=[(-.2, .4), (.3, .3)], ridge_at=.2, tip_pow=1.7, **BIG)
L("right_upper",  [(-81, 73, -.008), (-105, 60, .010), (-121, 46, .026), (-131, 35, .052)], .084, grooves=[(.1, .35)], ridge_at=-.3, tip_pow=1.6, **BIG)
L("right_spike",  [(-70, 81, -.006), (-86, 75, .018), (-97, 69, .052)], .048, t=.018, n=12, grooves=[(0, .3)], tip_pow=1.4)
L("right_burn",   [(-84, 40, -.006), (-86, 16, .003), (-84, -4, .007), (-78, -21, .013)], .072, t=.018, grooves=[(.15, .35)], ridge_at=-.2)
L("right_behind", [(-104, 36, -.006), (-106, 10, .005), (-106, -12, .011), (-102, -31, .026)], .084, t=.022, grooves=[(-.2, .35)], ridge_at=.2)
# ===== Simm's left (screen-right): lighter, three flicks pointing out and up
L("left_flick_hi",  [(30, 77, -.010), (62, 63, .005), (84, 47, .020), (99, 33, .054)], .092, grooves=[(.2, .4)], ridge_at=-.2, tip_pow=1.6, **BIG)
L("left_flick_mid", [(50, 71, -.010), (76, 53, .005), (92, 33, .018), (105, 15, .048)], .092, grooves=[(-.2, .4), (.3, .3)], ridge_at=.2, tip_pow=1.6, **BIG)
L("left_flick_low", [(72, 58, -.008), (86, 36, .003), (94, 12, .012), (99, -10, .032)], .084, t=.022, grooves=[(.1, .35)], ridge_at=-.3, tip_pow=1.6)
L("left_burn",      [(80, 36, -.006), (80, 14, .003), (78, -4, .007), (74, -19, .011)], .062, t=.016, grooves=[(-.15, .35)], ridge_at=.2)
L("left_behind",    [(106, 40, -.006), (108, 14, .005), (108, -10, .011), (104, -29, .028)], .084, t=.022, grooves=[(.2, .35)], ridge_at=-.2)
# ===== top: broad masses rolling off the crown into the parting, the fringe roots and the left flicks
L("top_to_part",  [(172, 80, -.012), (-120, 85, .004), (-70, 79, .008), (-50, 69, .010)], .112, root=.35, belly=.3, grooves=[(-.3, .4), (.3, .35)], ridge_at=.1, **BIG)
L("top_to_left",  [(160, 79, -.012), (92, 85, .004), (52, 81, .008), (32, 77, .009)], .112, root=.35, belly=.3, grooves=[(.25, .4)], ridge_at=-.2, **BIG)
L("top_to_front", [(-176, 78, -.012), (-20, 89, .006), (-16, 79, .009), (-18, 71, .009)], .104, root=.35, belly=.3, grooves=[(-.2, .4)], ridge_at=.2, **BIG)
L("top_right_bk", [(-166, 74, -.012), (-134, 68, .004), (-108, 66, .010), (-94, 60, .016)], .100, root=.35, belly=.3, grooves=[(.1, .35)], ridge_at=-.3, **BIG)
L("top_left_bk",  [(166, 74, -.012), (134, 68, .004), (108, 66, .010), (94, 60, .016)], .096, root=.35, belly=.3, grooves=[(-.1, .35)], ridge_at=.3, **BIG)
# ===== tufts: the tall one at the top leaning toward Simm's left, a second spike beyond it
L("tuft_main", [(-14, 84, -.012), (8, 88, .018), (32, 84, .044), (52, 76, .072)], .082, t=.028, grooves=[(.25, .45), (-.3, .3)], ridge_at=-.2, tip_pow=1.5, root=.55, belly=.3)
L("tuft_main_b", [(-30, 80, -.012), (-6, 86, .012), (24, 84, .030), (46, 78, .050)], .066, t=.022, grooves=[(0, .4)], tip_pow=1.6, root=.55, belly=.3)
L("tuft_second", [(40, 80, -.010), (70, 74, .016), (92, 66, .042), (107, 58, .074)], .062, t=.022, grooves=[(.1, .35)], tip_pow=1.5, root=.55, belly=.3)
L("tuft_back", [(150, 83, -.008), (174, 75, .016), (-172, 64, .048)], .054, t=.018, n=12, grooves=[(.1, .35)], tip_pow=1.4)
# ===== back, lower tier: down to the nape, tips kicking out                   [not visible in reference: invented]
L("back_c",   [(180, 54, -.010), (180, 10, .000), (180, -32, .004), (180, -60, .026)], .122, grooves=[(-.35, .4), (.3, .35)], ridge_at=.1, **BIG)
L("back_l1",  [(148, 54, -.010), (146, 10, .000), (148, -30, .004), (156, -56, .032)], .118, grooves=[(.25, .4), (-.4, .3)], ridge_at=-.2, **BIG)
L("back_r1",  [(-148, 54, -.010), (-146, 10, .000), (-147, -29, .004), (-153, -54, .030)], .118, grooves=[(-.25, .4), (.4, .3)], ridge_at=.2, **BIG)
L("back_l2",  [(120, 52, -.010), (117, 12, .000), (115, -20, .006), (121, -45, .038)], .106, grooves=[(.1, .4)], ridge_at=-.3, **BIG)
L("back_r2",  [(-120, 52, -.010), (-118, 12, .000), (-117, -20, .006), (-124, -43, .036)], .106, grooves=[(-.1, .4)], ridge_at=.3, **BIG)
# ===== back, upper tier: shorter, staggered over the lower tier, tips lifting  [invented]
L("back_u1",  [(165, 72, -.008), (166, 36, .006), (168, 0, .012), (173, -22, .036)], .108, grooves=[(.3, .4), (-.2, .3)], ridge_at=-.2, **BIG)
L("back_u2",  [(-165, 72, -.008), (-165, 36, .006), (-164, 2, .012), (-158, -19, .034)], .110, grooves=[(-.3, .4), (.2, .3)], ridge_at=.2, **BIG)
L("back_u3",  [(134, 70, -.008), (131, 36, .006), (128, 4, .012), (133, -16, .040)], .100, grooves=[(0, .4)], ridge_at=.3, **BIG)
L("back_u4",  [(-134, 70, -.008), (-132, 36, .006), (-131, 4, .012), (-138, -14, .038)], .100, grooves=[(.1, .4)], ridge_at=-.3, **BIG)
# ===== nape: short under-clumps that feather the lower edge                    [invented]
NP = dict(t=.012, n=10, tip_pow=1.8, root=.3, belly=.35)
L("nape_a", [(168, -8, -.012), (167, -36, .003), (165, -50, .012)], .074, **NP)
L("nape_b", [(-168, -8, -.012), (-167, -35, .003), (-164, -48, .012)], .074, **NP)
L("nape_c", [(138, -4, -.012), (136, -32, .003), (133, -46, .014)], .070, **NP)
L("nape_d", [(-138, -4, -.012), (-136, -31, .003), (-134, -44, .014)], .070, **NP)
L("nape_e", [(114, 8, -.012), (112, -18, .003), (110, -32, .014)], .060, **NP)
L("nape_f", [(-114, 8, -.012), (-112, -18, .003), (-110, -31, .014)], .060, **NP)
# ===== under-fringe: short clumps following the sweep, so the hairline never reads as a band
U = dict(t=.014, n=10, tip_pow=2.4)
L("under_a", [(-24, 42, -.002), (-16, 20, .003), (-9, -4, .004)], .076, **U)
L("under_b", [(-6, 44, -.002), (6, 21, .003), (17, -4, .004)], .078, **U)
L("under_c", [(14, 44, -.002), (28, 21, .003), (40, -4, .004)], .078, **U)
L("under_d", [(34, 40, -.002), (48, 18, .003), (60, -3, .004)], .074, **U)
L("under_e", [(-46, 36, -.002), (-54, 20, .003), (-61, 2, .004)], .074, **U)
L("under_f", [(56, 32, -.002), (64, 18, .003), (71, 2, .004)], .068, **U)
# ===== accent strands: thin, lifted, following the big shapes
A = dict(t=.009, n=12, tip_pow=1.3)
L("acc_fr_a", [(-26, 68, .002), (-10, 50, .010), (6, 34, .013), (18, 22, .013)], .028, **A)
L("acc_fr_b", [(-6, 74, .002), (18, 58, .010), (40, 42, .014), (56, 28, .018)], .028, **A)
L("acc_rt_a", [(-47, 68, .002), (-61, 48, .010), (-74, 30, .014), (-83, 14, .022)], .030, **A)
L("acc_rt_b", [(-74, 72, .002), (-96, 58, .012), (-112, 42, .026), (-122, 30, .044)], .028, **A)
L("acc_lf_a", [(40, 74, .002), (70, 58, .010), (88, 40, .020), (101, 24, .044)], .028, **A)
L("acc_bk_a", [(174, 62, .002), (176, 30, .010), (178, 2, .014), (-178, -16, .024)], .030, **A)
L("acc_bk_b", [(-146, 62, .002), (-145, 32, .010), (-144, 8, .014), (-148, -10, .028)], .030, **A)
L("acc_bk_c", [(146, 62, .002), (144, 32, .010), (142, 8, .014), (146, -10, .028)], .030, **A)

bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
me = bpy.data.meshes.new("SCULPT_HAIR"); bm.to_mesh(me); bm.free()
for nm in ("SCULPT_HAIR", "SCULPT_HAIR_GUIDES"):
    o_ = bpy.data.objects.get(nm)
    if o_: bpy.data.objects.remove(o_)
hair = bpy.data.objects.new("SCULPT_HAIR", me); coll.objects.link(hair)
bpy.context.view_layer.objects.active = hair
for o_ in bpy.context.view_layer.objects: o_.select_set(o_ is hair)
print("SOURCE verts", len(me.vertices), "clumps", len(GUIDES))
# ---------------- fuse into one sculpted surface, relax the joins, reduce
m = hair.modifiers.new("fuse", 'REMESH'); m.mode = 'VOXEL'; m.voxel_size = VOX; m.adaptivity = 0.0; m.use_smooth_shade = True
bpy.ops.object.modifier_apply(modifier="fuse")
m = hair.modifiers.new("relax", 'SMOOTH'); m.factor = 0.5; m.iterations = 4
bpy.ops.object.modifier_apply(modifier="relax")
print("FUSED verts", len(hair.data.vertices))
# drop everything that ended up buried inside the head
bm = bmesh.new(); bm.from_mesh(hair.data)
dead = []
for v in bm.verts:
    d = np.array(v.co) - HC; r = np.linalg.norm(d)
    az = math.degrees(math.atan2(d[0], -d[1])); el = math.degrees(math.asin(d[2]/r))
    if r < scalp.radius(az, el) - 0.0015: dead.append(v)
bmesh.ops.delete(bm, geom=dead, context='VERTS')
bm.to_mesh(hair.data); bm.free()
tris = sum(len(p.vertices)-2 for p in hair.data.polygons)
m = hair.modifiers.new("reduce", 'DECIMATE'); m.ratio = min(1.0, TRIS/max(tris, 1))
bpy.ops.object.modifier_apply(modifier="reduce")
# drop loose crumbs left by fusing and reduction (tiny disconnected shells read as specks)
bm = bmesh.new(); bm.from_mesh(hair.data); bm.verts.ensure_lookup_table()
seen = set(); crumbs = []
for v in bm.verts:
    if v.index in seen: continue
    st = [v]; comp = [v]; seen.add(v.index)
    while st:
        x_ = st.pop()
        for e in x_.link_edges:
            y_ = e.other_vert(x_)
            if y_.index not in seen: seen.add(y_.index); st.append(y_); comp.append(y_)
    if len(comp) < 400: crumbs += comp
print("crumb verts removed", len(crumbs))
bmesh.ops.delete(bm, geom=crumbs, context='VERTS'); bm.to_mesh(hair.data); bm.free()
for p in hair.data.polygons: p.use_smooth = True
hair.data.use_auto_smooth = True; hair.data.auto_smooth_angle = math.radians(75)
mat = bpy.data.materials.get("SCULPT_MAT_HAIR") or bpy.data.materials.new("SCULPT_MAT_HAIR")
mat.use_nodes = True; mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.19, 0.085, 0.04, 1)
mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.55
hair.data.materials.append(mat)
# editable guide curves (authoring record; not exported)
cu = bpy.data.curves.new("SCULPT_HAIR_GUIDES", 'CURVE'); cu.dimensions = '3D'
for name, P in GUIDES:
    sp = cu.splines.new('NURBS'); sp.points.add(len(P)-1); sp.use_endpoint_u = True; sp.order_u = min(4, len(P))
    for pt, p in zip(sp.points, P): pt.co = (*p, 1.0)
go = bpy.data.objects.new("SCULPT_HAIR_GUIDES", cu); coll.objects.link(go); go.hide_render = True; go.hide_viewport = False
print("HAIR verts", len(hair.data.vertices), "tris", sum(len(p.vertices)-2 for p in hair.data.polygons))
bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out)
