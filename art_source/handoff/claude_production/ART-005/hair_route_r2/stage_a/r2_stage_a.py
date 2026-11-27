# ART-018 R2 Stage A (Codex brief at 634c089): ONE hair-only CLAY diagnostic on the held head v012.
#   blender -b inbox/head_candidate_v012.blend --python r2_stage_a.py -- <abs out.blend>
# Replaces SCULPT_HAIR (and drops SCULPT_HAIR_GUIDES) with:
#   (0) an UNDER-SURFACE grown from the head's own scalp: offset along the skin normals from 4 mm INSIDE the skin at the
#       hairline to 6 mm outside it above, so it never shows a cap edge; it sits beneath the pieces;
#   (1..) authored pieces, one per hand-placed cubic guide (no radial placement, no voxel or metaball fusion). Each piece
#       is swept along its guide with a broad rounded-ridge lens cross-section; width swells a little then tapers to a
#       point, depth thins steadily; the ridge faces away from the head; roots start on the under-surface and are covered
#       by the next layer. Guide points before the tip region are kept at least LIFT outside the head skin.
# Everything else in the file (face, eyes, brows, lashes, neck, body, rig, actions, socket) is untouched.
# Coordinates: head world frame, metres, Z up, front -Y, Simm's right -X. Crown whorl upper back, slightly to Simm's left.
import bpy, bmesh, sys, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
out = sys.argv[sys.argv.index("--")+1]
for n in ("SCULPT_HAIR", "SCULPT_HAIR_GUIDES"):
    o = bpy.data.objects.get(n)
    if o: bpy.data.objects.remove(o, do_unlink=True)
head = bpy.data.objects["SCULPT_HEAD"]; root = bpy.data.objects["SCULPT_HEAD_ROOT"]; coll = head.users_collection[0]
dg = bpy.context.evaluated_depsgraph_get(); eh = head.evaluated_get(dg); hm = eh.to_mesh()
HV = np.array([head.matrix_world @ v.co for v in hm.vertices]); HN = np.array([(head.matrix_world.to_3x3() @ v.normal).normalized() for v in hm.vertices])
HF = [tuple(p.vertices) for p in hm.polygons]; eh.to_mesh_clear()
bvh = BVHTree.FromPolygons([Vector(p) for p in HV], HF)
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3 - 2*x)
# ---- (0) under-surface from the scalp
phi = np.degrees(np.abs(np.arctan2(HV[:, 0], -(HV[:, 1] - 0.03))))          # 0 = front, 180 = back
zline = np.where(phi <= 90, 1.238 + (1.182 - 1.238)*sstep(phi/90), 1.182 + (1.075 - 1.182)*sstep((phi - 90)/90))
h = sstep((HV[:, 2] - zline)/0.03)
off = -0.004 + 0.010*h
EP = HV + HN*off[:, None]
bm = bmesh.new(); vs = [bm.verts.new(p) for p in EP]
for f in HF:
    if max(h[i] for i in f) > 0.01: bm.faces.new([vs[i] for i in f])
for v in [v for v in bm.verts if not v.link_faces]: bm.verts.remove(v)
pieces = [("under_surface", bm)]
# ---- (1..) authored pieces: name, P0 (root), P1, P2, P3 (tip), max width, max depth, layer
G = [("back_nape",      (0.000, 0.080, 1.330), (0.000, 0.170, 1.300), (0.000, 0.212, 1.200), (0.000, 0.192, 1.098), 0.150, 0.032, 1),
     ("back_right",     (-0.060, 0.090, 1.322), (-0.110, 0.170, 1.282), (-0.134, 0.190, 1.182), (-0.124, 0.170, 1.110), 0.120, 0.030, 1),
     ("back_left",      (0.060, 0.090, 1.322), (0.110, 0.170, 1.282), (0.134, 0.190, 1.182), (0.124, 0.170, 1.110), 0.120, 0.030, 1),
     ("side_right_back",(-0.060, 0.070, 1.330), (-0.142, 0.072, 1.302), (-0.182, 0.042, 1.222), (-0.178, 0.030, 1.165), 0.100, 0.028, 2),
     ("side_right",     (-0.050, 0.020, 1.336), (-0.132, 0.000, 1.312), (-0.172, -0.040, 1.232), (-0.170, -0.058, 1.175), 0.105, 0.030, 2),
     ("side_left_back", (0.070, 0.080, 1.326), (0.142, 0.082, 1.302), (0.178, 0.062, 1.242), (0.194, 0.052, 1.205), 0.090, 0.026, 2),
     ("side_left",      (0.060, 0.020, 1.332), (0.132, 0.000, 1.312), (0.172, -0.030, 1.252), (0.184, -0.040, 1.210), 0.092, 0.026, 2),
     ("temple_right",   (-0.040, -0.010, 1.338), (-0.110, -0.070, 1.312), (-0.150, -0.085, 1.250), (-0.158, -0.080, 1.200), 0.085, 0.026, 3),
     ("temple_left",    (0.050, -0.005, 1.334), (0.112, -0.068, 1.308), (0.146, -0.086, 1.256), (0.152, -0.084, 1.214), 0.078, 0.024, 3),
     ("top_cover",      (0.025, 0.080, 1.336), (0.000, 0.020, 1.362), (-0.020, -0.040, 1.354), (-0.030, -0.085, 1.332), 0.150, 0.028, 3),
     ("fringe_right",   (-0.020, -0.030, 1.340), (-0.072, -0.102, 1.314), (-0.112, -0.114, 1.256), (-0.124, -0.104, 1.214), 0.080, 0.025, 4),
     ("fringe_main",    (0.030, -0.020, 1.342), (0.000, -0.104, 1.328), (-0.040, -0.138, 1.270), (-0.064, -0.130, 1.208), 0.095, 0.028, 4),
     ("fringe_mid",     (0.052, -0.010, 1.336), (0.052, -0.102, 1.322), (0.026, -0.138, 1.262), (0.004, -0.130, 1.214), 0.078, 0.024, 4),
     ("fringe_left",    (0.072, 0.000, 1.326), (0.094, -0.092, 1.304), (0.080, -0.128, 1.256), (0.066, -0.124, 1.218), 0.070, 0.022, 4),
     ("crown_tuft",     (0.020, 0.030, 1.344), (0.024, 0.066, 1.398), (0.004, 0.104, 1.424), (-0.018, 0.138, 1.430), 0.078, 0.028, 5),
     ("flick_right",    (-0.040, 0.000, 1.344), (-0.084, -0.018, 1.376), (-0.122, -0.018, 1.388), (-0.150, -0.004, 1.384), 0.064, 0.022, 5),
     ("flick_left",     (0.062, 0.040, 1.338), (0.104, 0.050, 1.366), (0.132, 0.068, 1.380), (0.152, 0.086, 1.378), 0.062, 0.022, 5)]
HC = np.array([0.0, 0.03, 1.20]); NS, M, LIFT = 48, 18, 0.004
def bez(P, t): return ((1-t)**3)[:, None]*P[0] + (3*(1-t)**2*t)[:, None]*P[1] + (3*(1-t)*t*t)[:, None]*P[2] + (t**3)[:, None]*P[3]
def section(w, d):
    s = np.linspace(-1, 1, M//2 + 1)
    top = [(x*w/2, d*(1 - x*x)**0.6) for x in s]                     # broad rounded ridge, no razor edge
    bot = [(x*w/2, -0.42*d*(1 - x*x)**0.9) for x in s[::-1][1:-1]]   # flatter underside
    return top + bot
report = {}
for name, p0, p1, p2, p3, W, D, layer in G:
    P = np.array([p0, p1, p2, p3]); t = np.linspace(0, 1, NS); C = bez(P, t)
    for i in range(NS):                         # keep the guide on the scalp (tips may lift)
        if t[i] > 0.82: continue
        hit = bvh.find_nearest(Vector(C[i]))
        if hit[0] is None: continue
        q, n = np.array(hit[0]), np.array(hit[1]); sd = np.dot(C[i] - q, n)
        need = LIFT + 0.010*(1 - t[i])
        if sd < need: C[i] = C[i] + n*(need - sd)
    T = np.gradient(C, axis=0); T /= np.linalg.norm(T, axis=1)[:, None]
    wt = W*(0.80 + 0.20*sstep(t/0.2))*(1 - sstep((t - 0.30)/0.70))**0.75; dt = D*(1 - t)**0.8 + 0.0004   # broad body, pointed end
    bmp = bmesh.new(); rings = []
    for i in range(NS):
        up = C[i] - HC; up -= T[i]*np.dot(up, T[i]); up /= np.linalg.norm(up); side = np.cross(T[i], up)
        if i == NS - 1:
            rings.append([bmp.verts.new(C[i])]); break
        rings.append([bmp.verts.new(C[i] + side*x + up*y) for x, y in section(wt[i], dt[i])])
    for a, b in zip(rings[:-2], rings[1:-1]):
        n_ = len(a)
        for k in range(n_): bmp.faces.new((a[k], a[(k+1) % n_], b[(k+1) % n_], b[k]))
    last, tip = rings[-2], rings[-1][0]
    for k in range(len(last)): bmp.faces.new((last[k], last[(k+1) % len(last)], tip))
    bmp.faces.new(rings[0][::-1])               # root cap (buried)
    pieces.append((name, bmp)); report[name] = {"layer": layer, "max_width_mm": W*1000, "max_depth_mm": D*1000, "tip": [round(x, 3) for x in C[-1]]}
# ---- one object, separate islands (no fusion)
me = bpy.data.meshes.new("SCULPT_HAIR"); allb = bmesh.new()
for name, b in pieces:
    tmp = bpy.data.meshes.new("tmp_" + name); b.to_mesh(tmp); b.free(); allb.from_mesh(tmp); bpy.data.meshes.remove(tmp)
bmesh.ops.recalc_face_normals(allb, faces=allb.faces[:])
for f in allb.faces: f.smooth = True
allb.to_mesh(me); allb.free()
hair = bpy.data.objects.new("SCULPT_HAIR", me); coll.objects.link(hair); hair.parent = root
mat = bpy.data.materials.get("SCULPT_MAT_HAIR") or bpy.data.materials.new("SCULPT_MAT_HAIR"); me.materials.append(mat)
co = np.array([v.co[:] for v in me.vertices])
print("R2A pieces", len(pieces), "verts", len(me.vertices), "faces", len(me.polygons), "bounds", co.min(0).round(3), co.max(0).round(3))
import json; json.dump({"pieces": report, "under_surface": "scalp offset -4 mm at the hairline to +6 mm above it"}, open(out[:-6] + "_pieces.json", "w"), indent=1)
bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out)
