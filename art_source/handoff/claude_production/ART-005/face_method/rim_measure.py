# ART-015 review measurement, never saves: height of the head skin above the eye surface (ray straight back along +y)
# and how much it faces the viewer, in oval bands just outside the left eye opening. Run on a head blend, or after
# compose_inlay_demo.py in the same session.
import bpy, numpy as np
from mathutils.bvhtree import BVHTree
from mathutils import Vector
dg = bpy.context.evaluated_depsgraph_get()
def ev(o):
    e = o.evaluated_get(dg); m = e.to_mesh(); W = o.matrix_world
    P = [W @ v.co for v in m.vertices]; F = [tuple(p.vertices) for p in m.polygons]; N = np.array([(W.to_3x3() @ v.normal)[:] for v in m.vertices]); e.to_mesh_clear(); return P, F, N
eye = bpy.data.objects["SCULPT_EYE_L"]; EP, EF, _ = ev(eye); bvh = BVHTree.FromPolygons(EP, EF)
E = np.array([p[:] for p in EP]); C = 0.5*(E.min(0)+E.max(0))
HP, HF, HN = ev(bpy.data.objects["SCULPT_HEAD"]); H = np.array([p[:] for p in HP])
d = H - C; e = np.sqrt((d[:,0]/0.0174)**2 + (d[:,2]/np.where(d[:,2]<0, 0.94*0.0264, 0.0264))**2)
out = []
for lo, hi in ((1.0,1.08),(1.08,1.15),(1.15,1.3)):
    m = (d[:,1] < 0) & (e >= lo) & (e < hi); hts = []; fac = []
    for i in np.where(m)[0]:
        hit = bvh.ray_cast(Vector(H[i]) + Vector((0,-0.05,0)), Vector((0,1,0)), 0.2)   # eye surface straight behind this skin point
        if hit[0] is not None: hts.append((hit[0].y - H[i,1])*1000)
        fac.append(-HN[i,1])     # how much the skin faces the viewer (front is -y): 1 = straight at the camera
    hts = np.array(hts); fac = np.array(fac)
    out.append("e %.2f-%.2f: skin above eye surface mm p50 %.2f p90 %.2f max %.2f (n %d) | facing-viewer p50 %.2f" % (lo, hi, np.percentile(hts,50), np.percentile(hts,90), hts.max(), len(hts), np.percentile(fac,50)))
print("RIM", bpy.data.filepath.split('/')[-1]); [print("RIM", x) for x in out]
