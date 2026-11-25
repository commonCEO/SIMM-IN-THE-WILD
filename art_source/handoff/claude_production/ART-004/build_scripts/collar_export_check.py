# Export ONLY the collar parts to GLB and measure rest-pose clearance to the held head and hair.
# blender -b collar_packet.blend --python collar_export_check.py -- out.glb
import bpy, sys, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode = True
out = sys.argv[sys.argv.index("--")+1]
PARTS = ["SCULPT_HOOD", "SCULPT_SCARF"]          # named part manifest: the build fails if one is missing or duplicated
names = [o.name for o in bpy.data.objects]
for p in PARTS:
    assert names.count(p) == 1, "part manifest: %s present %d times" % (p, names.count(p))
    o = bpy.data.objects[p]
    g = o.vertex_groups.get("chest"); assert g is not None and len(o.vertex_groups) == 1, p + ": must carry only the chest group"
    assert all(len(v.groups) == 1 and abs(v.groups[0].weight - 1.0) < 1e-6 for v in o.data.vertices), p + ": every vertex must be 1.0 on chest"
    assert not any(m.type == 'ARMATURE' for m in o.modifiers), p + ": no armature modifier in source"
print("MANIFEST ok", PARTS, "each 100 percent chest, no armature modifier")
dg = bpy.context.evaluated_depsgraph_get()
def bvh(name):
    ev = bpy.data.objects[name].evaluated_get(dg); me = ev.to_mesh()
    t = BVHTree.FromPolygons([v.co.copy() for v in me.vertices], [tuple(p.vertices) for p in me.polygons]); ev.to_mesh_clear(); return t
head, hair, body = bvh("SCULPT_HEAD"), bvh("SCULPT_HAIR"), bvh("PROTECTED_BODY")
for p in PARTS:
    o = bpy.data.objects[p]; co = [v.co.copy() for v in o.data.vertices]
    a = np.array([c[:] for c in co])
    print("PART", p, "verts", len(co), "tris", sum(len(f.vertices)-2 for f in o.data.polygons), "bounds min", a.min(0).round(3), "max", a.max(0).round(3))
    # the neck itself passes through the scarf by design; what must stay clear is everything that moves with the
    # head above the collar: jaw and chin (front), skull base and nape (back), and the hair
    for nm, tree, test in (("jaw and chin (head skin, z>1.015, front half)", head, lambda l: l.z > 1.015 and l.y < 0.03),
                           ("skull base and nape (head skin, z>1.015, back half)", head, lambda l: l.z > 1.015 and l.y >= 0.03),
                           ("hair", hair, lambda l: True)):
        best = (9, None)
        for c in co:
            loc, nrm, idx, d = tree.find_nearest(c)
            if loc is not None and test(loc) and d < best[0]: best = (d, (round(c.x, 3), round(c.y, 3), round(c.z, 3)))
        print("  nearest", nm, "%.1f mm at part point" % (best[0]*1000), best[1])
    # how much of the part sits outside the frozen body surface (roots are meant to be inside the collar)
    inside = 0
    for c in co:
        loc, nrm, idx, d = body.find_nearest(c)
        if loc is not None and (c - loc).dot(nrm) < 0: inside += 1
    print("  vertices inside the frozen body surface: %d of %d" % (inside, len(co)))
for o in bpy.context.view_layer.objects: o.select_set(False)
for n in ["SCULPT_COLLAR_ROOT"] + PARTS:
    bpy.data.objects[n].hide_set(False); bpy.data.objects[n].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects["SCULPT_COLLAR_ROOT"]
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=True, export_apply=True, export_yup=True, export_animations=False,
                          export_skins=False, export_cameras=False, export_lights=False, export_materials='EXPORT', export_morph=False)
print("EXPORTED", out)
