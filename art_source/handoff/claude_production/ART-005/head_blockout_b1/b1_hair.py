# ART-016 head blockout B1 (Codex brief at faa8749): silhouette-first hair, CLAY blockout only.
#   blender -b <stage3 or head blend> --python b1_hair.py -- <abs out.blend>
# Replaces SCULPT_HAIR (and drops SCULPT_HAIR_GUIDES) with ONE soft mass made of a scalp cap and NINE dominant clumps,
# built as metaball chains (balls tapering from root to tip along a quadratic curve) so neighbouring clumps fuse softly,
# then converted to a mesh. No strands, no locks, no texture. Coordinates are the head's world frame (metres, Z up,
# front -Y, Simm's right -X). The clump layout follows the reference's read, not measured proportions:
#   a taller crown with tufts swept up and back, a fringe sweeping down over the forehead toward Simm's right to about
#   brow level, a heavier side mass on Simm's right over the temple, a shorter one on the left, a full back/nape mass.
import bpy, sys, numpy as np
from mathutils import Vector
out = sys.argv[sys.argv.index("--")+1]
for n in ("SCULPT_HAIR", "SCULPT_HAIR_GUIDES"):
    o = bpy.data.objects.get(n)
    if o: bpy.data.objects.remove(o, do_unlink=True)
root = bpy.data.objects["SCULPT_HEAD_ROOT"]; coll = bpy.data.objects["SCULPT_HEAD"].users_collection[0]
CAP = dict(centre=(0.0, 0.045, 1.288), radii=(0.168, 0.170, 0.118))
#        name             root                   control                tip                    r_root  r_tip
CLUMPS = [("fringe_main",  (0.020, -0.060, 1.345), (-0.040, -0.140, 1.305), (-0.082, -0.130, 1.218), 0.046, 0.013),
          ("fringe_left",  (0.055, -0.050, 1.335), (0.078, -0.134, 1.290), (0.055, -0.126, 1.226), 0.036, 0.012),
          ("side_right",   (-0.120, 0.000, 1.310), (-0.186, -0.030, 1.240), (-0.180, -0.020, 1.150), 0.050, 0.013),
          ("side_left",    (0.120, 0.000, 1.310), (0.172, -0.028, 1.252), (0.166, -0.040, 1.196), 0.040, 0.012),
          ("crown_back",   (-0.020, 0.060, 1.380), (-0.040, 0.120, 1.425), (-0.085, 0.172, 1.428), 0.060, 0.015),
          ("crown_right",  (0.030, 0.020, 1.390), (0.075, 0.010, 1.428), (0.132, 0.018, 1.422), 0.052, 0.015),
          ("top_front",    (-0.050, -0.030, 1.380), (-0.110, -0.068, 1.415), (-0.162, -0.062, 1.408), 0.050, 0.015),
          ("back_nape",    (0.000, 0.120, 1.310), (0.000, 0.205, 1.210), (0.000, 0.182, 1.085), 0.070, 0.022),
          ("back_tuft",    (-0.100, 0.120, 1.310), (-0.172, 0.152, 1.262), (-0.208, 0.142, 1.215), 0.042, 0.013)]
N_BALLS = 20
mb = bpy.data.metaballs.new("B1_HAIR_MB"); mb.resolution = 0.004; mb.render_resolution = 0.004; mb.threshold = 0.6
mo = bpy.data.objects.new("B1_HAIR_MB", mb); coll.objects.link(mo)
# calibration: the visible radius of a lone ball is K x its element radius (depends on threshold/stiffness)
K = np.sqrt(1 - np.sqrt(0.6/2.0))
e = mb.elements.new(); e.type = 'ELLIPSOID'; e.co = CAP["centre"]; e.radius = 1.0/K
e.size_x, e.size_y, e.size_z = CAP["radii"]
for name, p0, p1, p2, r0, r1 in CLUMPS:
    P0, P1, P2 = map(np.array, (p0, p1, p2))
    for t in np.linspace(0, 1, N_BALLS):
        p = (1-t)**2*P0 + 2*(1-t)*t*P1 + t*t*P2
        r = r0*(1-t)**1.2 + r1*(1-(1-t)**1.2)
        b = mb.elements.new(); b.type = 'BALL'; b.co = p.tolist(); b.radius = r/K
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get(); me = bpy.data.meshes.new_from_object(mo.evaluated_get(dg))
me.name = "SCULPT_HAIR"; hair = bpy.data.objects.new("SCULPT_HAIR", me); coll.objects.link(hair)
bpy.data.objects.remove(mo, do_unlink=True)
for p in me.polygons: p.use_smooth = True
hair.parent = root
mat = bpy.data.materials.get("SCULPT_MAT_HAIR") or bpy.data.materials.new("SCULPT_MAT_HAIR")
me.materials.clear(); me.materials.append(mat)
co = np.array([v.co[:] for v in me.vertices])
print("B1 HAIR verts", len(me.vertices), "tris approx", sum(len(p.vertices) - 2 for p in me.polygons), "bounds", co.min(0).round(3), co.max(0).round(3))
bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out)
