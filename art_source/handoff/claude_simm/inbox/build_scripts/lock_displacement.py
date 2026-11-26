# Surface displacement between two head files' SCULPT_HAIR (read only), and how far the moved vertices lie from guide 4 (D2).
# blender -b --python lock_displacement.py -- <control.blend> <candidate.blend> <out.json>
import bpy, sys, os, json, numpy as np
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hairkit import catmull
a, b, out = sys.argv[sys.argv.index("--")+1:][:3]
def load(p):
    with bpy.data.libraries.load(p) as (src, dst): dst.meshes = ["SCULPT_HAIR"]; dst.curves = ["SCULPT_HAIR_GUIDES"]
    m = dst.meshes[0]; V = np.array([v.co[:] for v in m.vertices]); return V, [tuple(p.vertices) for p in m.polygons], dst.curves[0]
A, FA, ga = load(a); B, FB, gb = load(b)
ta = BVHTree.FromPolygons([tuple(x) for x in A], FA); tb = BVHTree.FromPolygons([tuple(x) for x in B], FB)
dB = np.array([ta.find_nearest(x)[3] for x in B]); dA = np.array([tb.find_nearest(x)[3] for x in A])
sp = gb.splines[4]; spine = catmull(np.array([p.co[:3] for p in sp.points]), 200)
def dist_to_spine(X): return np.array([np.linalg.norm(spine - x, axis=1).min() for x in X])
mB = dB > 0.001; mA = dA > 0.001
r = {"new_vertices": len(B), "moved_over_1mm_new_to_old": int(mB.sum()), "max_mm": round(float(dB.max())*1000, 1), "p99_mm": round(float(np.percentile(dB, 99))*1000, 2),
     "old_vertices_over_1mm_from_new": int(mA.sum()), "max_old_to_new_mm": round(float(dA.max())*1000, 1),
     "moved_vertices_distance_to_D2_guide_mm_max": round(float(dist_to_spine(B[mB]).max())*1000, 1) if mB.any() else None,
     "moved_vertices_distance_to_D2_guide_mm_p95": round(float(np.percentile(dist_to_spine(B[mB]), 95))*1000, 1) if mB.any() else None,
     "moved_over_3mm_far_from_D2_over_70mm": int(((dB > 0.003) & (dist_to_spine(B) > 0.07)).sum())}
json.dump(r, open(out, "w"), indent=1); print("DISP", r)
