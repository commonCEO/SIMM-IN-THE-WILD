# Run after render_views.py with ONE view, in the same Blender session. Projects head landmarks through the scene
# camera and writes them as pixel positions: eye centres (eye object bounds), chin (the midline point furthest forward-and-down),
# hair top, face width 25 mm above the chin, visible head width on the eye-line row, fringe edge on the midline (lowest hair point in front of the forehead within 15 mm of the midline).
# blender -b head.blend --python render_views.py --python head_landmarks.py -- <render args...> ; env LM_OUT=<json>
import bpy, os, json, numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
sc = bpy.context.scene; cam = sc.camera; dg = bpy.context.evaluated_depsgraph_get()
W, H = sc.render.resolution_x, sc.render.resolution_y
def px(p):
    v = world_to_camera_view(sc, cam, Vector(p)); return [round(v.x*W, 1), round((1 - v.y)*H, 1)]
def verts(name):
    o = bpy.data.objects[name]; e = o.evaluated_get(dg); m = e.to_mesh()
    a = np.array([(e.matrix_world @ v.co)[:] for v in m.vertices]); e.to_mesh_clear(); return a
out = {}
for n in ("SCULPT_EYE_L", "SCULPT_EYE_R"):
    a = verts(n); out[n] = px(0.5*(a.min(0) + a.max(0)))
hd = verts("SCULPT_HEAD"); f = hd[(abs(hd[:, 0]) < 0.010) & (hd[:, 2] < 1.075) & (hd[:, 2] > 0.98)]
c = f[(-f[:, 1] - f[:, 2]).argmax()]                      # chin point: the midline's extreme toward forward-and-down
out["chin"] = px(c); out["chin_z"] = float(c[2]); out["chin_y"] = float(c[1])
w = hd[(abs(hd[:, 2] - (c[2] + 0.025)) < 0.004) & (hd[:, 1] < -0.02)]
out["face_width_25mm_above_chin_m"] = float(w[:, 0].max() - w[:, 0].min())
hr = verts("SCULPT_HAIR"); out["hair_top"] = px(hr[hr[:, 2].argmax()])
fr = hr[(abs(hr[:, 0]) < 0.015) & (hr[:, 1] < -0.06)]
out["fringe_midline_low"] = px(fr[fr[:, 2].argmin()]) if len(fr) else None
out["fringe_midline_low_z"] = float(fr[:, 2].min()) if len(fr) else None
ey = [out["SCULPT_EYE_L"], out["SCULPT_EYE_R"]]; out["eye_line_y"] = round(0.5*(ey[0][1] + ey[1][1]), 1)
out["eye_to_chin_px"] = round(out["chin"][1] - out["eye_line_y"], 1)
# visible head width at eye level: horizontal extent of the projected skin and hair (ears included) on the image row
# through the eye-line midpoint, +-3 px. Vertex-sampled silhouette; the meshes are dense enough for about 1 px.
pr = []
for n in ("SCULPT_HEAD", "SCULPT_HAIR"):
    for p_ in verts(n):
        v = world_to_camera_view(sc, cam, Vector(p_)); pr.append((v.x*W, (1 - v.y)*H))
pr = np.array(pr); row = pr[np.abs(pr[:, 1] - out["eye_line_y"]) < 3.0]
out["visible_head_width_at_eye_line_px"] = round(float(row[:, 0].max() - row[:, 0].min()), 1)
out["eye_dx_px"] = round(abs(ey[0][0] - ey[1][0]), 1)
out["eye_dx_over_head_width"] = round(out["eye_dx_px"]/out["visible_head_width_at_eye_line_px"], 4)
json.dump(out, open(os.environ["LM_OUT"], "w"), indent=1); print("LANDMARKS", json.dumps(out))
