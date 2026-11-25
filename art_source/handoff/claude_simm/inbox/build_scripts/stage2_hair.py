# Stage 2: hair. work/stage1.blend -> work/stage2.blend
# Built like a clay sculpt: (1) one thick hair mass over the scalp, (2) hand-placed clumps merged into it at the
# roots, (3) thin accent strands, then everything fused into a single surface and relaxed.
# Each clump is an individually authored guide path: (azimuth, elevation, offset from the hair-mass surface in m).
# azimuth 0 = face front, + = Simm's left (+X), - = Simm's right (-X), 180 = back. elevation 90 = crown.
import bpy, bmesh, sys, os, math, numpy as np
sys.dont_write_bytecode = True
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
HL_EL = [23, 22, 15, 5, 1, 0, -3, -26, -30, -31]      # stays above the ear so the mass never cuts through it
def wrap(az): return ((az + 180) % 360) - 180
def hairline(az): return float(np.interp(abs(wrap(az)), HL_AZ, HL_EL))
def mass(az, el):
    """thickness of the under-mass above the skin. v003: low over the crown (the Godot view showed a tall round
    dome), full at the sides and back where the reference carries its volume, heavier on Simm's right."""
    hl = hairline(az); a = wrap(az); back = sstep((abs(a) - 90)/70)
    heavy = sstep((a + 160)/50)*sstep((-15 - a)/50)*sstep((el - hl)/30)
    top = sstep((el - 55)/25)
    side = sstep((abs(a) - 50)/30)*sstep((155 - abs(a))/40)*sstep((el - hl)/26)*sstep((80 - el)/30)
    front = sstep((70 - abs(a))/20)
    return (0.004 + (0.008 - 0.004*front)*sstep((el - (hl-10))/10)
            + (0.026 + 0.008*back)*sstep((el - hl)/32)*(1 - 0.40*top) + 0.010*heavy + (0.020 + 0.016*(a < 0))*side)

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

# v003 layout (after Codex's Godot review of v002): five DOMINANT locks are shaped first, each with its own arc,
# depth and tip length; SUBORDINATE locks then fill between them at lower depth; a few thin accents break edges.
# Dominant locks ride clearly above their neighbours (offsets of 10 to 20 mm), so they overlap instead of sharing
# one smooth shell.
DOM = dict(t=.030)
SUB = dict(t=.020)
# ===== DOMINANT 1 (v004): the arc over Simm's right is three overlapping curved volumes, not one plate.
# Different roots, different depths, different tip directions; each rises off the head, bends and twists as it tapers.
L("D1a_arc_upper", [(-28, 79, -.014), (-56, 66, .014), (-82, 51, .034), (-98, 41, .058), (-104, 37, .074)], .080, n=20,
  grooves=[(-.25, .45)], ridge_at=.25, tip_pow=1.7, root=.40, belly=.32, t=.026, roll=(-8, 26))
L("D1b_arc_front", [(-44, 71, -.012), (-66, 54, .008), (-85, 34, .022), (-96, 18, .040), (-99, 10, .050)], .074, n=20,
  grooves=[(.2, .45)], ridge_at=-.2, tip_pow=1.8, root=.45, belly=.3, t=.024, roll=(6, -22))
L("D1c_arc_rear",  [(-60, 78, -.012), (-88, 66, .010), (-108, 52, .026), (-120, 44, .046)], .066, n=18,
  grooves=[(0, .4)], ridge_at=.3, tip_pow=1.6, root=.45, belly=.3, t=.022, roll=(0, 18))
# ===== DOMINANT 2: arcing temple lock: bows forward over the temple and hooks down in front of the ear
L("D2_temple_arc",  [(-38, 66, -.010), (-56, 46, .012), (-70, 24, .018), (-74, 2, .016), (-70, -12, .014)], .100, n=20,
  grooves=[(.25, .45), (-.3, .35)], ridge_at=-.2, tip_pow=2.1, root=.5, belly=.3, **DOM)
# ===== DOMINANT 3: the central fringe point, longest lock of the fringe, to between the brows
L("D3_fringe_point", [(-26, 70, -.012), (-16, 48, .010), (-5, 22, .014), (6, -8, .010), (9, -13, .008)], .096, n=20,
  grooves=[(-.3, .45), (.3, .4)], ridge_at=.15, tip_pow=2.2, root=.5, belly=.3, t=.026)
# ===== DOMINANT 4: one broad lock sweeping across Simm's left brow
L("D4_fringe_sweep", [(-12, 74, -.012), (10, 56, .012), (32, 32, .016), (48, 6, .014), (53, -6, .012)], .124, n=20,
  grooves=[(-.35, .45), (.05, .4), (.4, .35)], ridge_at=-.2, tip_pow=2.3, root=.5, belly=.3, **DOM)
# ===== DOMINANT 5: the main flick on Simm's left, kicking out and up
L("D5_left_flick",   [(32, 77, -.012), (58, 64, .012), (80, 50, .030), (95, 40, .054), (101, 36, .072)], .084, n=20,
  grooves=[(.25, .45)], ridge_at=-.2, tip_pow=1.5, root=.42, belly=.3, t=.026, roll=(6, -24))
# ===== SUBORDINATE, Simm's right: a shorter side flick under the big arc, sideburn, behind the ear
L("S_right_flick",  [(-62, 58, -.010), (-84, 40, .004), (-98, 24, .020), (-105, 12, .044)], .078, grooves=[(.1, .4)], ridge_at=.3, tip_pow=1.7, **SUB)
L("S_right_upper",  [(-92, 70, -.010), (-114, 58, .004), (-128, 44, .012), (-137, 32, .026)], .070, grooves=[(.1, .4)], ridge_at=-.3, tip_pow=1.7, **SUB)
L("S_right_burn",   [(-86, 38, -.008), (-88, 16, .000), (-86, -4, .004), (-80, -20, .010)], .064, t=.016, grooves=[(.15, .4)], ridge_at=-.2)
L("S_right_behind", [(-106, 36, -.008), (-108, 10, .002), (-108, -12, .008), (-104, -31, .024)], .084, grooves=[(-.2, .4)], ridge_at=.2, **SUB)
L("S_right_spike",  [(-72, 82, -.008), (-88, 76, .016), (-99, 70, .056)], .040, t=.014, n=12, grooves=[(0, .3)], tip_pow=1.5, root=.6, belly=.3)
# ===== SUBORDINATE, fringe: short lock by the parting (leaves the window over the right eye), far-left temple lock
L("S_fringe_part",  [(-28, 60, -.010), (-26, 44, .002), (-24, 28, .004), (-21, 11, .004)], .068, t=.016, grooves=[(0, .4)], tip_pow=2.2)
L("S_fringe_right", [(-32, 67, -.010), (-44, 48, .004), (-57, 30, .010), (-68, 14, .014), (-73, 8, .016)], .086, grooves=[(.1, .4)], ridge_at=.2, tip_pow=2.0, roll=(0, 16), **SUB)   # offset, swept sideways to the temple
L("S_fringe_left",  [(4, 76, -.012), (32, 62, .000), (56, 40, .006), (72, 14, .014), (77, 0, .018)], .092, grooves=[(.15, .4)], ridge_at=.2, tip_pow=2.0, **SUB)
L("S_fringe_mid",   [(-18, 72, -.010), (-4, 52, .004), (9, 30, .008), (16, 9, .008)], .088, grooves=[(-.1, .4)], ridge_at=-.2, tip_pow=3.4, **SUB)   # shorter, rounded end
L("S_fringe_under", [(0, 44, -.004), (10, 28, .005), (20, 10, .005), (25, -1, .005)], .096, t=.017, n=12, tip_pow=3.2)
L("S_fringe_under2", [(-22, 42, -.004), (-15, 24, .005), (-9, 5, .005)], .078, t=.016, n=10, tip_pow=3.0)
L("S_fringe_under3", [(40, 40, -.004), (52, 20, .005), (63, -8, .006)], .086, t=.016, n=10, tip_pow=2.3)
L("S_temple_under", [(-46, 36, -.004), (-58, 18, .005), (-68, 2, .008), (-73, -6, .010)], .080, t=.016, n=12, tip_pow=2.2)
# ===== SUBORDINATE, Simm's left: two lesser flicks of different length under the main one, sideburn, behind ear
L("S_left_mid",    [(54, 68, -.010), (78, 50, .004), (94, 28, .020), (104, 8, .048), (106, 0, .056)], .070, grooves=[(-.2, .4)], ridge_at=.2, tip_pow=1.7, **SUB)
L("S_left_low",    [(74, 54, -.008), (87, 34, .000), (94, 12, .008), (97, -6, .022)], .074, grooves=[(.1, .4)], ridge_at=-.3, tip_pow=1.8, t=.018)
L("S_left_burn",   [(82, 34, -.008), (82, 14, .000), (80, -4, .004), (76, -18, .008)], .058, t=.015, grooves=[(-.15, .4)], ridge_at=.2)
L("S_left_behind", [(108, 40, -.008), (110, 14, .002), (110, -10, .008), (106, -29, .026)], .084, grooves=[(.2, .4)], ridge_at=-.2, **SUB)
# ===== top: low masses rolling off the crown, feeding the dominant locks (kept thin: no dome)
TOP = dict(t=.022, root=.35, belly=.3)
L("top_to_part",  [(172, 80, -.010), (-120, 85, .000), (-70, 79, .003), (-48, 70, .004)], .108, grooves=[(-.3, .4), (.3, .4)], ridge_at=.1, **TOP)
L("top_to_left",  [(160, 79, -.010), (92, 85, .000), (52, 81, .003), (36, 78, .004)], .108, grooves=[(.25, .4)], ridge_at=-.2, **TOP)
L("top_to_front", [(-176, 78, -.010), (-20, 89, .001), (-16, 80, .003), (-16, 74, .004)], .096, grooves=[(-.2, .4)], ridge_at=.2, **TOP)
L("top_right_bk", [(-166, 74, -.010), (-134, 68, .000), (-108, 66, .005), (-96, 62, .010)], .096, grooves=[(.1, .4)], ridge_at=-.3, **TOP)
L("top_left_bk",  [(166, 74, -.010), (134, 68, .000), (108, 66, .005), (96, 62, .010)], .092, grooves=[(-.1, .4)], ridge_at=.3, **TOP)
# ===== tuft: ONE tapering swept lock rising out of the crown flow, root narrow and buried (no lobes, no pit)
L("tuft",        [(-30, 80, -.016), (-8, 87, .000), (16, 88, .028), (36, 82, .066), (50, 74, .106)], .050, n=24, t=.020,
  grooves=[(.2, .4)], ridge_at=-.2, tip_pow=1.25, root=.30, belly=.40, roll=(0, 20))
L("tuft_strand", [(-10, 84, -.006), (14, 87, .012), (36, 82, .036), (50, 76, .060)], .026, t=.012, n=14, tip_pow=1.3, root=.4, belly=.4)
L("tuft_second", [(44, 80, -.012), (70, 75, .010), (90, 68, .040), (103, 62, .072)], .044, t=.016, grooves=[(.1, .35)], tip_pow=1.5, root=.4, belly=.35)
L("rise_front",  [(8, 80, -.008), (28, 78, .012), (46, 72, .032)], .034, t=.012, n=12, tip_pow=1.4, root=.5, belly=.35)
L("tuft_back",   [(150, 83, -.010), (174, 76, .006), (-172, 66, .034)], .048, t=.016, n=12, grooves=[(.1, .35)], tip_pow=1.4, root=.4, belly=.35)
# ===== back, lower tier: down to the nape, tips kicking out, lengths varied       [not visible in reference: invented]
L("back_c",   [(180, 54, -.010), (180, 10, .000), (180, -32, .004), (180, -60, .026)], .122, grooves=[(-.35, .45), (.3, .4)], ridge_at=.1, t=.026)
L("back_l1",  [(148, 54, -.010), (146, 10, .000), (148, -28, .006), (155, -50, .034)], .116, grooves=[(.25, .45), (-.4, .35)], ridge_at=-.2, t=.026)
L("back_r1",  [(-148, 54, -.010), (-146, 10, .000), (-147, -30, .004), (-153, -57, .028)], .118, grooves=[(-.25, .45), (.4, .35)], ridge_at=.2, t=.026)
L("back_l2",  [(120, 52, -.010), (117, 12, .000), (115, -20, .006), (121, -45, .038)], .104, grooves=[(.1, .45)], ridge_at=-.3, t=.026)
L("back_r2",  [(-120, 52, -.010), (-118, 12, .000), (-117, -18, .008), (-125, -38, .040)], .104, grooves=[(-.1, .45)], ridge_at=.3, t=.026)
# ===== back, upper tier: shorter, riding above the lower tier, tips lifting         [invented]
L("back_u1",  [(165, 72, -.008), (166, 36, .010), (168, 0, .018), (173, -22, .044)], .104, grooves=[(.3, .45), (-.2, .35)], ridge_at=-.2, t=.026)
L("back_u2",  [(-165, 72, -.008), (-165, 38, .010), (-164, 8, .018), (-158, -10, .040)], .106, grooves=[(-.3, .45), (.2, .35)], ridge_at=.2, t=.026)
L("back_u3",  [(134, 70, -.008), (131, 38, .010), (128, 10, .018), (133, -8, .044)], .096, grooves=[(0, .45)], ridge_at=.3, t=.026)
L("back_u4",  [(-134, 70, -.008), (-132, 36, .010), (-131, 2, .018), (-138, -18, .042)], .098, grooves=[(.1, .45)], ridge_at=-.3, t=.026)
# ===== nape: short under-clumps that feather the lower edge                         [invented]
NP = dict(t=.012, n=10, tip_pow=1.8, root=.3, belly=.35)
L("nape_a", [(168, -8, -.012), (167, -36, .003), (165, -50, .012)], .074, **NP)
L("nape_b", [(-168, -8, -.012), (-167, -35, .003), (-164, -48, .012)], .074, **NP)
L("nape_c", [(138, -4, -.012), (136, -32, .003), (133, -46, .014)], .070, **NP)
L("nape_d", [(-138, -4, -.012), (-136, -31, .003), (-134, -44, .014)], .070, **NP)
L("nape_e", [(114, 8, -.012), (112, -18, .003), (110, -32, .014)], .060, **NP)
L("nape_f", [(-114, 8, -.012), (-112, -18, .003), (-110, -31, .014)], .060, **NP)
# ===== accents: thin strands that split from the dominant locks and break their edges
A = dict(t=.009, n=14, tip_pow=1.3, root=.6, belly=.3)
L("acc_arc",    [(-46, 72, .004), (-74, 58, .020), (-96, 42, .040), (-108, 32, .062)], .028, **A)
L("acc_temple", [(-48, 62, .004), (-62, 44, .018), (-74, 26, .024), (-80, 10, .026)], .026, **A)
L("acc_point",  [(-20, 66, .004), (-8, 44, .016), (4, 24, .018), (13, 6, .016)], .026, **A)
L("acc_sweep",  [(0, 72, .004), (22, 54, .018), (42, 34, .022), (56, 16, .022)], .028, **A)
L("acc_flick",  [(44, 74, .004), (72, 60, .020), (90, 46, .040), (101, 37, .060)], .026, **A)
L("acc_bk_a",   [(174, 62, .004), (176, 30, .018), (178, 2, .024), (-178, -16, .034)], .030, **A)
L("acc_bk_b",   [(-146, 62, .004), (-145, 32, .018), (-144, 8, .024), (-148, -10, .038)], .030, **A)
L("acc_bk_c",   [(146, 62, .004), (144, 32, .018), (142, 8, .024), (146, -10, .038)], .030, **A)

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
m = hair.modifiers.new("relax", 'SMOOTH'); m.factor = 0.5; m.iterations = 3
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
