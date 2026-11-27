import bpy, bmesh, numpy as np
from mathutils import Vector
bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.0)
o = bpy.context.active_object
before = np.array([v.co[:] for v in o.data.vertices])
res = {}
# 1) sculpt brush stroke headless
try:
    bpy.ops.object.mode_set(mode='SCULPT')
    stroke = [{"name": "s", "location": (0, -1, z), "mouse": (0, 0), "mouse_event": (0, 0), "pressure": 1.0, "size": 60, "pen_flip": False,
               "time": float(i), "is_start": i == 0, "x_tilt": 0, "y_tilt": 0} for i, z in enumerate(np.linspace(-0.3, 0.3, 8))]
    r = bpy.ops.sculpt.brush_stroke(stroke=stroke, mode='NORMAL')
    res["sculpt_brush_stroke"] = str(r)
except Exception as e:
    res["sculpt_brush_stroke"] = "ERR " + str(e)[:120]
bpy.ops.object.mode_set(mode='OBJECT')
after = np.array([v.co[:] for v in o.data.vertices]); res["sculpt_moved_max"] = float(np.abs(after - before).max())
# 2) sculpt filters (mesh filter) headless
try:
    bpy.ops.object.mode_set(mode='SCULPT'); r = bpy.ops.sculpt.mesh_filter(type='INFLATE', strength=0.2); res["mesh_filter"] = str(r)
except Exception as e: res["mesh_filter"] = "ERR " + str(e)[:120]
bpy.ops.object.mode_set(mode='OBJECT')
# 3) bmesh + modifiers: subsurf with crease, shape keys, hooks, lattice, corrective smooth, multires
m = o.modifiers.new("ss", 'SUBSURF'); m.levels = 2
bm = bmesh.new(); bm.from_mesh(o.data); cl = bm.edges.layers.crease.verify(); bm.edges.ensure_lookup_table(); bm.edges[0][cl] = 1.0; bm.to_mesh(o.data); bm.free()
mr = o.modifiers.new("mr", 'MULTIRES'); res["multires"] = "ok"
try:
    bpy.context.view_layer.objects.active = o; r = bpy.ops.object.multires_subdivide(modifier="mr", mode='CATMULL_CLARK'); res["multires_subdivide"] = str(r)
except Exception as e: res["multires_subdivide"] = "ERR " + str(e)[:120]
print("CAP", res)
