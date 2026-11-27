# ART-020 shared helpers: protected-geometry fingerprints (used by build, check and export). Blender 3.5+.
import bpy, hashlib, numpy as np
PROTECTED = ["SCULPT_HEAD", "SCULPT_EYE_L", "SCULPT_EYE_R", "SCULPT_BROWS", "SCULPT_LASHES"]
def mesh_fp(me):
    """sha256 over base-mesh vertex positions (float32, rounded to 1e-6 m) and polygon vertex indices; modifiers ignored."""
    co = np.empty(len(me.vertices)*3, dtype=np.float32); me.vertices.foreach_get("co", co)
    co = np.round(co.astype(np.float64), 6).astype(np.float32)
    ix = np.empty(len(me.loops), dtype=np.int32); me.loops.foreach_get("vertex_index", ix)
    st = np.empty(len(me.polygons), dtype=np.int32); me.polygons.foreach_get("loop_total", st)
    h = hashlib.sha256(); h.update(co.tobytes()); h.update(ix.tobytes()); h.update(st.tobytes()); return h.hexdigest()
def obj_record(o):
    me = o.data; co = np.array([v.co[:] for v in me.vertices]) if len(me.vertices) else np.zeros((1, 3))
    W = np.array(o.matrix_world); P = co @ W[:3, :3].T + W[:3, 3]
    return {"mesh": me.name, "vertices": len(me.vertices), "polygons": len(me.polygons), "fingerprint": mesh_fp(me),
            "modifiers": [m.type for m in o.modifiers], "parent": o.parent.name if o.parent else None,
            "matrix_world_identity": bool(np.allclose(np.array(o.matrix_world), np.eye(4), atol=1e-7)),
            "bounds_min": P.min(0).round(4).tolist(), "bounds_max": P.max(0).round(4).tolist()}
