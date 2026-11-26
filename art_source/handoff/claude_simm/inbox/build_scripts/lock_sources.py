# Which source piece forms the top surface of a lock's section (read only). Needs a stage 2 file built with
# HAIR_SOURCE_COPY=1 (unfused source with a per-vertex "piece" index, names in the HAIR_PIECES text).
# blender -b stage2_diag.blend --python lock_sources.py -- <guide index> <absolute out.json>
# At 25, 50 and 75 percent of the guide, both the unfused source and the fused SCULPT_HAIR are cut by the plane normal
# to the guide (stage 2 coordinates, before the head drop and crown map). In the +-25 mm window, for every 2 mm of
# lateral position, the outermost source surface is attributed to its piece; the fused top curve gives the flat share
# (slope under 12 degrees), as in lock_sections.py.
import bpy, sys, os, json, math, numpy as np
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hairkit import catmull, HC
gi, out = sys.argv[sys.argv.index("--")+1:][:2]; gi = int(gi)
names = bpy.data.texts["HAIR_PIECES"].as_string().split("\n")
g = bpy.data.objects["SCULPT_HAIR_GUIDES"]; sp = g.data.splines[gi]
spine = catmull(np.array([(g.matrix_world @ pt.co.to_3d())[:] for pt in sp.points]), 200)
seg = np.linalg.norm(np.diff(spine, axis=0), axis=1); cum = np.concatenate([[0], np.cumsum(seg)])/seg.sum()
def mesh(name):
    o = bpy.data.objects[name]; V = np.array([(o.matrix_world @ v.co)[:] for v in o.data.vertices])
    return V, [tuple(p.vertices) for p in o.data.polygons], o.data
SV, SF, sme = mesh("SCULPT_HAIR_SOURCE"); piece = np.array([d.value for d in sme.attributes["piece"].data])
FV, FF, _ = mesh("SCULPT_HAIR")
def cut(V, F, p, T, tag=None):
    d = (V - p) @ T; pts = []; tags = []
    for f in F:
        for k in range(len(f)):
            a, b = f[k], f[(k+1) % len(f)]
            if (d[a] > 0) != (d[b] > 0):
                t = d[a]/(d[a] - d[b]); q = V[a] + (V[b] - V[a])*t
                if np.linalg.norm(q - p) < 0.06: pts.append(q); tags.append(tag[a] if tag is not None else -1)
    return np.array(pts), np.array(tags)
res = {"guide_index": gi, "sections": {}}
for s in (0.25, 0.50, 0.75):
    i = int(np.searchsorted(cum, s)); p = spine[i]; T = spine[min(i+1, len(spine)-1)] - spine[max(i-1, 0)]; T /= np.linalg.norm(T)
    N = p - HC; N -= N.dot(T)*T; N /= np.linalg.norm(N); B = np.cross(T, N)
    Q, tg = cut(SV, SF, p, T, piece); bb = (Q - p) @ B; nn = (Q - p) @ N
    owners = []
    for x in np.arange(-0.025, 0.0251, 0.002):
        m = np.abs(bb - x) < 0.001
        if m.any(): owners.append(names[tg[m][np.argmax(nn[m])]])
    Qf, _ = cut(FV, FF, p, T); bf = (Qf - p) @ B; nf = (Qf - p) @ N; top = []
    for x in np.arange(-0.025, 0.0251, 0.002):
        m = np.abs(bf - x) < 0.001
        if m.any(): top.append((x, nf[m].max()))
    top = np.array(top); slope = np.abs(np.gradient(top[:, 1], top[:, 0]))
    share = Counter(owners); tot = sum(share.values())
    res["sections"][str(s)] = {"top_owner_share": {k: round(v/tot, 3) for k, v in share.most_common()},
                               "fused_flat_share_under_12deg": round(float((slope < math.tan(math.radians(12))).mean()), 3)}
    print("SOURCES s=%.2f fused flat share %.2f; top surface owners %s" % (s, res["sections"][str(s)]["fused_flat_share_under_12deg"], res["sections"][str(s)]["top_owner_share"]))
json.dump(res, open(out, "w"), indent=1)
