# Cross-sections of ONE hair lock on the final fused hair (method gate, Codex brief at d6b9555). Read only.
# blender -b head.blend --python lock_sections.py -- <guide index> <absolute out.json>
# The lock's authored guide (SCULPT_HAIR_GUIDES spline, already carried through the head drop and the crown map) is
# resampled as in stage 2. At 25, 50 and 75 percent of its length the final SCULPT_HAIR mesh is cut by the plane
# normal to the guide; segments within 60 mm are kept and written in the lock's own frame: b across the lock, n out
# from the head. The outer top curve (highest n per 2 mm of b within +-25 mm) gets a least-squares circle; its radius
# and the share of that window flatter than 12 degrees describe how plate-like the surface is.
import bpy, sys, os, json, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hairkit import catmull, HC
gi, out = sys.argv[sys.argv.index("--")+1:][:2]; gi = int(gi)
g = bpy.data.objects["SCULPT_HAIR_GUIDES"]; sp = g.data.splines[gi]
P = np.array([(g.matrix_world @ pt.co.to_3d())[:] for pt in sp.points]); spine = catmull(P, 200)
seg = np.linalg.norm(np.diff(spine, axis=0), axis=1); cum = np.concatenate([[0], np.cumsum(seg)])/seg.sum()
h = bpy.data.objects["SCULPT_HAIR"]; me = h.data
V = np.array([(h.matrix_world @ v.co)[:] for v in me.vertices]); F = [tuple(p.vertices) for p in me.polygons]
C = HC + np.array([0, 0, -0.018])                    # stage 3's head drop
res = {"guide_index": gi, "sections": {}}
for s in (0.25, 0.50, 0.75):
    i = int(np.searchsorted(cum, s)); p = spine[i]; T = spine[min(i+1, len(spine)-1)] - spine[max(i-1, 0)]; T /= np.linalg.norm(T)
    N = p - C; N -= N.dot(T)*T; N /= np.linalg.norm(N); Bv = np.cross(T, N)
    d = (V - p) @ T; segs = []
    for f in F:
        for k in range(len(f)):
            a, b = f[k], f[(k+1) % len(f)]
            if (d[a] > 0) != (d[b] > 0):
                t = d[a]/(d[a] - d[b]); q = V[a] + (V[b] - V[a])*t
                if np.linalg.norm(q - p) < 0.06: segs.append(q)
    Q = np.array(segs); bb = (Q - p) @ Bv; nn = (Q - p) @ N
    top = []
    for x in np.arange(-0.025, 0.0251, 0.002):
        m = np.abs(bb - x) < 0.001
        if m.any(): top.append((x, nn[m].max()))
    top = np.array(top)
    A = np.c_[2*top[:, 0], 2*top[:, 1], np.ones(len(top))]; rhs = (top**2).sum(1)
    cx, cy, c0 = np.linalg.lstsq(A, rhs, rcond=None)[0]; R = math.sqrt(max(c0 + cx*cx + cy*cy, 0))
    slope = np.abs(np.gradient(top[:, 1], top[:, 0]))
    res["sections"][str(s)] = {"points_b_n_mm": np.round(np.c_[bb, nn]*1000, 2).tolist(), "top_curve_b_n_mm": np.round(top*1000, 2).tolist(),
                               "top_circle_radius_mm": round(R*1000, 1), "flat_share_under_12deg": round(float((slope < math.tan(math.radians(12))).mean()), 3),
                               "top_rise_mm": round(float((top[:, 1].max() - top[:, 1].min())*1000), 1)}
    print("SECTION s=%.2f: top circle radius %.1f mm, flat share %.2f, rise across +-25 mm %.1f mm" % (s, R*1000, res["sections"][str(s)]["flat_share_under_12deg"], res["sections"][str(s)]["top_rise_mm"]))
json.dump(res, open(out, "w"))
