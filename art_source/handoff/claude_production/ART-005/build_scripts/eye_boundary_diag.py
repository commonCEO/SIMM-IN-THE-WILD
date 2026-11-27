# ART-015 diagnostic (Codex brief at 5fafefb). Review only, never saved; run before render_views.py on head v012:
#   DIAG=flat|bands blender -b inbox/head_candidate_v012.blend --python eye_boundary_diag.py --python render_views.py -- ...
# DIAG=flat : eyes become a flat unlit constant brown (emission only), like Codex's native flat-eye control; skin as held.
# DIAG=bands: as flat, and SCULPT_HEAD vertex colours mark the bands around each eye opening by oval coordinate
#             e = |(x/0.0174, z/0.0264)| about the eye centre (front half only): 1.00-1.15 red (lid rim),
#             1.15-1.50 orange (inner socket wall), 1.50-2.20 yellow (outer slope); the rest stays skin.
import bpy, os, numpy as np
mode = os.environ.get("DIAG", "flat")
for n in ("SCULPT_EYE_L", "SCULPT_EYE_R"):
    o = bpy.data.objects[n]; m = bpy.data.materials.new("DIAG_FLAT_EYE"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = (0.10, 0.055, 0.032, 1); out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs[0], out.inputs[0])
    for s in o.material_slots: s.material = m
if mode == "bands":
    h = bpy.data.objects["SCULPT_HEAD"]; me = h.data; W = np.array(h.matrix_world)
    P = np.array([v.co[:] for v in me.vertices]) @ W[:3, :3].T + W[:3, 3]
    col = np.tile([0.80, 0.62, 0.50, 1.0], (len(P), 1))
    for n in ("SCULPT_EYE_L", "SCULPT_EYE_R"):
        eo = bpy.data.objects[n]; E = np.array([eo.matrix_world @ v.co for v in eo.data.vertices]); C = 0.5*(E.min(0) + E.max(0)); R = (E.max(0) - E.min(0))[0]/2
        d = P - C; ov = np.sqrt((d[:, 0]/0.0174)**2 + (d[:, 2]/0.0264)**2); fr = d[:, 1] < -0.4*R
        for lo, hi, c in ((1.0, 1.15, (0.9, 0.1, 0.1)), (1.15, 1.5, (1.0, 0.55, 0.0)), (1.5, 2.2, (0.95, 0.9, 0.1))):
            k = fr & (ov >= lo) & (ov < hi); col[k, :3] = c
    a = me.color_attributes.new("diag", 'FLOAT_COLOR', 'POINT'); a.data.foreach_set("color", col.astype(np.float32).ravel())
    m = bpy.data.materials.new("DIAG_BANDS"); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    at = nt.nodes.new("ShaderNodeAttribute"); at.attribute_name = "diag"; nt.links.new(at.outputs["Color"], b.inputs["Base Color"])
    for s in h.material_slots: s.material = m
print("DIAG", mode)
