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
HL_EL = [29, 28, 19, 4, -5, -8, -13, -30, -35, -36]
def wrap(az): return ((az + 180) % 360) - 180
def hairline(az): return float(np.interp(abs(wrap(az)), HL_AZ, HL_EL))
def mass(az, el):
    """thickness of the primary hair mass above the skin"""
    hl = hairline(az); back = sstep((abs(wrap(az)) - 90)/70)
    a = wrap(az)
    heavy = sstep((a + 150)/40)*sstep((-25 - a)/40)*sstep((el - hl)/30)     # Simm's right carries more volume
    crown = sstep((el - 62)/20)
    return 0.004 + 0.008*sstep((el - (hl-10))/10) + (0.023 + 0.006*back)*sstep((el - hl)/30) + 0.007*heavy + 0.006*crown

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

# ===== back: lower tier down to the nape, tips kicking out                      [not visible in reference: invented]
L("back_c",   [(180, 58, -.006), (180, 10, .000), (180, -32, .004), (180, -60, .022)], .110, grooves=[(-.35, .4), (.3, .35)], ridge_at=.1)
L("back_l1",  [(150, 58, -.006), (148, 10, .000), (150, -30, .004), (157, -56, .028)], .105, grooves=[(.25, .4), (-.4, .3)], ridge_at=-.2)
L("back_r1",  [(-150, 58, -.006), (-148, 10, .000), (-149, -29, .004), (-154, -54, .026)], .105, grooves=[(-.25, .4), (.4, .3)], ridge_at=.2)
L("back_l2",  [(122, 56, -.006), (118, 12, .000), (115, -20, .005), (120, -45, .032)], .095, grooves=[(.1, .4)], ridge_at=-.3)
L("back_r2",  [(-122, 56, -.006), (-119, 12, .000), (-117, -20, .005), (-123, -43, .030)], .095, grooves=[(-.1, .4)], ridge_at=.3)
# ===== nape: short under-clumps that feather the lower edge                      [invented]
NP = dict(t=.010, n=10, tip_pow=1.8)
L("nape_a", [(168, -18, -.002), (167, -36, .003), (165, -50, .010)], .070, **NP)
L("nape_b", [(-168, -18, -.002), (-167, -35, .003), (-164, -48, .010)], .070, **NP)
L("nape_c", [(138, -14, -.002), (136, -32, .003), (133, -46, .012)], .066, **NP)
L("nape_d", [(-138, -14, -.002), (-136, -31, .003), (-134, -44, .012)], .066, **NP)
L("nape_e", [(114, -2, -.002), (112, -18, .003), (110, -32, .012)], .056, **NP)
L("nape_f", [(-114, -2, -.002), (-112, -18, .003), (-110, -31, .012)], .056, **NP)
# ===== back: upper tier, shorter, staggered over the gaps of the lower tier      [invented]
L("back_u1",  [(166, 70, -.004), (167, 34, .006), (169, -2, .010), (173, -24, .028)], .090, grooves=[(.3, .4), (-.2, .3)], ridge_at=-.2)
L("back_u2",  [(-166, 70, -.004), (-166, 34, .006), (-165, 0, .010), (-160, -21, .026)], .092, grooves=[(-.3, .4), (.2, .3)], ridge_at=.2)
L("back_u3",  [(136, 68, -.004), (133, 34, .006), (130, 2, .010), (134, -18, .032)], .084, grooves=[(0, .4)], ridge_at=.3)
L("back_u4",  [(-136, 68, -.004), (-134, 34, .006), (-133, 2, .010), (-139, -16, .030)], .084, grooves=[(.1, .4)], ridge_at=-.3)
# ===== Simm's right side (screen-left in the reference): the heavy swept mass over the ear
L("sideR_ear",  [(-97, 60, -.006), (-99, 26, .002), (-98, -4, .006), (-92, -25, .016)], .095, grooves=[(-.25, .4), (.35, .35)], ridge_at=.2)
L("sideR_burn", [(-76, 60, -.006), (-75, 28, .002), (-72, 4, .005), (-64, -14, .010)], .075, grooves=[(.2, .4)], ridge_at=-.2)
L("sideR_kick", [(-114, 62, -.004), (-116, 30, .008), (-119, 8, .016), (-127, -8, .040)], .072, grooves=[(0, .35)], ridge_at=.3)
# ===== Simm's left side (screen-right): lighter, flicking outward
L("sideL_ear",  [(97, 60, -.006), (98, 28, .002), (99, 0, .008), (104, -18, .030)], .086, grooves=[(.2, .4), (-.3, .3)], ridge_at=-.2)
L("sideL_burn", [(77, 60, -.006), (77, 30, .002), (75, 8, .006), (70, -10, .014)], .068, grooves=[(-.15, .35)], ridge_at=.2)
L("sideL_flick",[(90, 64, -.004), (95, 42, .010), (102, 24, .030), (112, 13, .062)], .060, grooves=[(.1, .35)], ridge_at=-.3, tip_pow=1.4)
L("sideL_kick", [(114, 64, -.004), (118, 36, .008), (122, 16, .020), (131, 3, .046)], .066, grooves=[(-.1, .35)], ridge_at=.3)
# ===== fringe: one central point between the brows, a forehead window either side
L("fringe_c",   [(-8, 66, -.006), (-6, 44, .003), (-2, 24, .007), (3, 5, .009)], .082, grooves=[(-.3, .45), (.3, .35)], ridge_at=.15, tip_pow=1.5)
L("fringe_r1",  [(-30, 64, -.006), (-35, 44, .003), (-42, 26, .007), (-48, 9, .010)], .084, grooves=[(.2, .45), (-.35, .3)], ridge_at=-.2, tip_pow=1.5)
L("fringe_r2",  [(-54, 62, -.006), (-63, 42, .003), (-72, 20, .007), (-77, 0, .010)], .086, grooves=[(-.2, .4), (.35, .35)], ridge_at=.2)
L("fringe_r0",  [(-18, 65, -.006), (-20, 47, .003), (-23, 30, .007), (-29, 12, .009)], .074, grooves=[(.1, .4)], ridge_at=.2, tip_pow=1.6)
L("fringe_l0",  [(7, 65, -.006), (9, 49, .003), (11, 36, .007), (13, 25, .009)], .058, grooves=[(-.1, .4)], ridge_at=-.2, tip_pow=1.6)
L("fringe_l15", [(32, 63, -.006), (38, 47, .003), (43, 33, .008), (48, 18, .012)], .068, grooves=[(.15, .4)], ridge_at=.2, tip_pow=1.6)
L("fringe_l1",  [(20, 64, -.006), (25, 46, .003), (29, 29, .007), (33, 11, .009)], .076, grooves=[(-.2, .45)], ridge_at=.2, tip_pow=1.5)
L("fringe_l2",  [(44, 62, -.006), (53, 44, .003), (61, 25, .010), (67, 7, .018)], .086, grooves=[(.2, .4), (-.3, .3)], ridge_at=-.2)
L("fringe_l3",  [(64, 62, -.004), (73, 42, .006), (82, 26, .020), (91, 14, .044)], .060, grooves=[(0, .35)], ridge_at=.3, tip_pow=1.4)
# ===== under-fringe: short clumps that break the hairline so it never reads as a band
U = dict(t=.011, n=10, tip_pow=1.9)
L("under_a", [(-12, 42, .000), (-13, 29, .004), (-15, 18, .004)], .060, **U)
L("under_b", [(-30, 40, .000), (-33, 24, .004), (-38, 8, .004)], .066, **U)
L("under_c", [(14, 42, .000), (16, 30, .004), (18, 20, .004)], .054, **U)
L("under_d", [(36, 40, .000), (40, 24, .004), (46, 9, .004)], .062, **U)
L("under_e", [(-50, 34, .000), (-55, 22, .004), (-59, 10, .004)], .056, **U)
L("under_f", [(54, 34, .000), (59, 19, .004), (65, 3, .004)], .058, **U)
L("under_g", [(2, 44, .000), (3, 34, .004), (5, 26, .004)], .044, **U)
L("fill_r", [(-46, 66, -.004), (-51, 50, .002), (-56, 36, .005), (-61, 22, .008)], .072, grooves=[(.1, .35)], tip_pow=1.7)
L("fill_l", [(60, 64, -.004), (66, 48, .002), (72, 34, .006), (78, 20, .012)], .064, grooves=[(-.1, .35)], tip_pow=1.7)
# ===== top: broad masses sweeping forward from the crown whorl over the fringe roots
L("top_r1",  [(-150, 80, -.014), (-92, 84, .004), (-44, 74, .008), (-32, 58, .012)], .105, grooves=[(-.3, .4), (.3, .35)], root=.30, belly=.30, ridge_at=.1)
L("top_r2",  [(-158, 76, -.014), (-114, 72, .004), (-76, 68, .008), (-62, 54, .013)], .100, grooves=[(.2, .4)], root=.30, belly=.30, ridge_at=-.2)
L("top_c",   [(-170, 82, -.014), (-30, 88, .005), (-10, 74, .009), (-8, 60, .013)], .105, grooves=[(-.2, .4), (.35, .35)], root=.30, belly=.30, ridge_at=.2)
L("top_l1",  [(165, 82, -.014), (62, 86, .004), (27, 74, .008), (22, 58, .012)], .100, grooves=[(.25, .4)], root=.30, belly=.30, ridge_at=-.2)
L("top_l2",  [(150, 78, -.014), (102, 74, .004), (68, 70, .008), (55, 56, .013)], .092, grooves=[(-.2, .35)], root=.30, belly=.30, ridge_at=.2)
L("top_r3",  [(-165, 74, -.014), (-132, 62, .004), (-102, 62, .009), (-88, 52, .015)], .092, grooves=[(.1, .35)], root=.30, belly=.30, ridge_at=-.3)
L("top_l3",  [(165, 74, -.014), (132, 62, .004), (106, 62, .009), (93, 52, .016)], .086, grooves=[(-.1, .35)], root=.30, belly=.30, ridge_at=.3)
# ===== cowlicks: the upward tufts that make the silhouette asymmetric
L("cowlick_main", [(-40, 76, -.008), (0, 86, .014), (52, 79, .040), (84, 66, .070)], .074, t=.020, grooves=[(.25, .45), (-.3, .3)], ridge_at=-.2, tip_pow=1.7, root=.5, belly=.3)
L("cowlick_m2",   [(-10, 72, -.008), (26, 78, .012), (62, 70, .028), (88, 56, .048)], .070, t=.018, grooves=[(0, .4)], ridge_at=.2, tip_pow=1.7, root=.5, belly=.3)
L("cowlick_m3",   [(-60, 80, -.008), (-20, 88, .010), (42, 84, .024), (72, 74, .044)], .060, t=.016, grooves=[(.1, .35)], tip_pow=1.6, root=.5, belly=.3)
L("cowlick_l",    [(56, 76, -.004), (80, 68, .016), (97, 60, .050)], .052, n=12, grooves=[(0, .35)], tip_pow=1.4)
L("cowlick_r",    [(-94, 72, -.004), (-106, 64, .016), (-115, 56, .048)], .048, n=12, grooves=[(0, .35)], tip_pow=1.4)
L("cowlick_back", [(150, 82, -.004), (170, 74, .014), (-176, 64, .042)], .052, n=12, grooves=[(.1, .35)], tip_pow=1.4)
# ===== accent strands: thin, slightly lifted, breaking the big shapes with direction changes
A = dict(t=.008, n=12, tip_pow=1.3)
L("acc_fr_a", [(-17, 62, .004), (-19, 46, .010), (-22, 32, .012), (-27, 22, .012)], .026, **A)
L("acc_fr_b", [(10, 62, .004), (12, 48, .010), (13, 36, .012), (12, 26, .011)], .024, **A)
L("acc_fr_c", [(-44, 62, .004), (-50, 46, .010), (-55, 32, .013), (-58, 20, .014)], .026, **A)
L("acc_fr_d", [(34, 62, .004), (38, 48, .010), (41, 36, .013), (42, 26, .014)], .024, **A)
L("acc_sr_a", [(-88, 58, .004), (-88, 34, .010), (-86, 12, .013), (-82, -6, .016)], .028, **A)
L("acc_sl_a", [(88, 58, .004), (89, 36, .010), (91, 18, .016), (96, 4, .028)], .026, **A)
L("acc_bk_a", [(174, 60, .004), (176, 30, .010), (178, 2, .012), (-178, -16, .020)], .028, **A)
L("acc_bk_b", [(-146, 60, .004), (-145, 32, .010), (-144, 8, .012), (-147, -10, .022)], .028, **A)
L("acc_bk_c", [(146, 60, .004), (144, 32, .010), (142, 8, .012), (145, -10, .022)], .028, **A)
L("acc_tp_a", [(-120, 80, .004), (-70, 82, .010), (-48, 70, .014), (-42, 60, .016)], .028, **A)
L("acc_tp_b", [(120, 82, .004), (50, 86, .010), (36, 74, .014), (34, 62, .016)], .026, **A)

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
m = hair.modifiers.new("relax", 'SMOOTH'); m.factor = 0.5; m.iterations = 6
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
