# ART-015 review composite, never saved. Opens the held head v012 and, IN MEMORY, takes from a scratch inlay build
# (run_inlay_demo.sh -> <dir>/head.blend; INLAY_BLEND env): the two eyeballs and the lashes whole, and the SCULPT_HEAD
# base-mesh positions only around the openings (weight 1 up to oval coordinate e = 1.6, fading to 0 at e = 2.4, egg oval
# as stage1). Everything else (forehead, brows, cheeks, mouth, hair, costume, rig) stays exactly v012, because the full
# inlay build also lets stage1's brow smoothing and the hair rebuild drift slightly outside the eye region.
#   INLAY_BLEND=<abs head.blend> blender -b inbox/head_candidate_v012.blend --python compose_inlay_demo.py \
#       [--python eye_boundary_diag.py | --python eye_e1_apply.py] --python render_views.py -- <render args>
import bpy, os, numpy as np
src = os.environ["INLAY_BLEND"]
with bpy.data.libraries.load(src) as (fsrc, dst): dst.meshes = [m for m in fsrc.meshes if m in ("SCULPT_HEAD", "SCULPT_EYE_L", "SCULPT_EYE_R", "SCULPT_LASHES")]
NEW = {m.name.split(".")[0]: np.array([v.co[:] for v in m.vertices]) for m in dst.meshes}
def co(o): return np.array([v.co[:] for v in o.data.vertices])
def setco(o, P): o.data.vertices.foreach_set("co", P.astype(np.float32).ravel()); o.data.update()
rep = {}
for n in ("SCULPT_EYE_L", "SCULPT_EYE_R", "SCULPT_LASHES"):
    o = bpy.data.objects[n]; old = co(o); assert old.shape == NEW[n].shape, n
    setco(o, NEW[n]); rep[n] = round(float(np.linalg.norm(NEW[n] - old, axis=1).max()*1000), 2)
h = bpy.data.objects["SCULPT_HEAD"]; H0 = co(h); assert H0.shape == NEW["SCULPT_HEAD"].shape
W = np.array(h.matrix_world); Hw = H0 @ W[:3, :3].T + W[:3, 3]; w = np.zeros(len(H0))
for n in ("SCULPT_EYE_L", "SCULPT_EYE_R"):
    eo = bpy.data.objects[n]; E = np.array([eo.matrix_world @ v.co for v in eo.data.vertices]); C = 0.5*(E.min(0) + E.max(0))
    d = Hw - C; e = np.sqrt((d[:, 0]/0.0174)**2 + (d[:, 2]/np.where(d[:, 2] < 0, 0.94*0.0264, 0.0264))**2)
    t = np.clip((e - 1.6)/0.8, 0, 1); w = np.maximum(w, np.where(d[:, 1] < 0.02, 1 - t*t*(3 - 2*t), 0))
H = H0*(1 - w[:, None]) + NEW["SCULPT_HEAD"]*w[:, None]; setco(h, H)
dd = np.linalg.norm(H - H0, axis=1)
rep["SCULPT_HEAD"] = {"moved_over_0.05mm": int((dd > 5e-5).sum()), "max_mm": round(float(dd.max()*1000), 2), "weight_1": int((w >= 0.999).sum()), "blended": int(((w > 0) & (w < 0.999)).sum())}
print("INLAY composite (max moves, mm)", rep)
