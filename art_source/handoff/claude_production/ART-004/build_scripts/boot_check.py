# Checks and exports boot candidate v001. Nothing is saved back to the .blend (armature modifiers are added in memory).
# blender -b boot_candidate_v001.blend --python boot_check.py -- <absolute out.glb>        (SAMPLES=97 by default)
import bpy, sys, os, math, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode = True
out = sys.argv[sys.argv.index("--")+1]; NS = int(os.environ.get("SAMPLES", "97"))
rig = bpy.data.objects["SimmRig"]; bd = bpy.data.objects["PROTECTED_BODY"]; sc = bpy.context.scene
NAMES = {"SCULPT_BOOT_SHAFT_L": "shin_l", "SCULPT_BOOT_FOOT_L": "foot_l", "SCULPT_BOOT_SHAFT_R": "shin_r", "SCULPT_BOOT_FOOT_R": "foot_r"}
# ---- manifest -----------------------------------------------------------------------------------------------
for n, bone in NAMES.items():
    found = [o.name for o in bpy.data.objects if o.name == n or o.name.startswith(n + ".")]
    assert found == [n], "missing or duplicate part %s: %s" % (n, found)
    ob = bpy.data.objects[n]
    assert [g.name for g in ob.vertex_groups] == [bone] and ob.get("bind_bone") == bone, n + ": binding record wrong"
    assert all(len(v.groups) == 1 and abs(v.groups[0].weight - 1.0) < 1e-6 for v in ob.data.vertices), n + ": not 100 percent on one bone"
    assert not ob.modifiers, n + ": has a modifier"
    assert ob.parent and ob.parent.name == "SCULPT_BOOTS_ROOT", n + ": not under the root"
print("MANIFEST ok: %s" % ", ".join("%s -> %s" % kv for kv in NAMES.items()))
# ---- the original surfaces a study would hide -------------------------------------------------------------------
gn = [g.name for g in bd.vertex_groups]; mi = {m.name: i for i, m in enumerate(bd.data.materials) if m}
def owner(k): return tuple(sorted((gn[g.group], round(g.weight, 3)) for g in bd.data.vertices[k].groups if g.weight > 0))
FOOT = {(("foot_l", 1.0),), (("foot_r", 1.0),)}
tot = 0; kept = 0
for name in ("Simm dark soles", "Simm brown boot leather", "Simm worn jacket edges"):
    fs = [p for p in bd.data.polygons if p.material_index == mi[name]]
    foot = [p for p in fs if all(owner(k) in FOOT for k in p.vertices)]; other = [p for p in fs if p not in foot]
    tf = sum(len(p.vertices)-2 for p in foot); to = sum(len(p.vertices)-2 for p in other); tot += tf; kept += to
    oo = sorted(set(owner(k) for p in other for k in p.vertices))
    zr = (min(bd.data.vertices[k].co.z for p in other for k in p.vertices), max(bd.data.vertices[k].co.z for p in other for k in p.vertices)) if other else None
    print("HIDE %-26s %4d triangles in all: %4d foot-owned (hide), %4d NOT foot-owned (keep)%s" % (name, tf + to, tf, to, "" if not other else "; those are %s, Z %.3f..%.3f" % (oo, zr[0], zr[1])))
print("HIDE total: %d foot-owned triangles to hide; %d triangles of the same materials must stay (not foot-owned)" % (tot, kept))
# ---- clips --------------------------------------------------------------------------------------------------
tm = mi["Simm charcoal olive trousers"]; tro = sorted(set(k for p in bd.data.polygons if p.material_index == tm for k in p.vertices))
DIR = Vector((0.13, 0.27, 0.95)).normalized()
def inside(tree, c):
    n = 0; o = c.copy()
    for _ in range(16):
        h = tree.ray_cast(o, DIR, 1.0)
        if h[0] is None: break
        n += 1; o = h[0] + DIR*1e-5
    return n % 2 == 1
parts = {n: bpy.data.objects[n] for n in NAMES}
SHAFT_EDGE = min(v.co.z for v in parts["SCULPT_BOOT_SHAFT_R"].data.vertices) + 0.008      # the shaft's lower edge band
shoe = [k for p in bd.data.polygons if p.material_index in (mi["Simm dark soles"],) for k in p.vertices]
rest = {n: [v.co.copy() for v in o.data.vertices] for n, o in parts.items()}
for n, o in parts.items(): o.parent = None; o.modifiers.new("Armature", 'ARMATURE').object = rig      # in memory only
def ev(o, dg):
    e = o.evaluated_get(dg); m = e.to_mesh(); v = [x.co.copy() for x in m.vertices]; f = [tuple(p.vertices) for p in m.polygons]; e.to_mesh_clear(); return v, f
if rig.animation_data is None: rig.animation_data_create()
tro_rest = {k: bd.data.vertices[k].co.copy() for k in tro}
for an in ("idle", "walk", "gather"):
    act = bpy.data.actions[an]; rig.animation_data.action = act; f0, f1 = act.frame_range
    w = {"trousers": (0, None), "crack": (0, 0.0, None), "sole": (9.0, -9.0)}
    for fr in np.linspace(f0, f1, NS):
        sc.frame_set(int(fr), subframe=float(fr - int(fr))); dg = bpy.context.evaluated_depsgraph_get()
        e = bd.evaluated_get(dg); m = e.to_mesh(); bv = [x.co.copy() for x in m.vertices]; e.to_mesh_clear()
        nt = 0; nc = 0; hc = 0.0; zboth = 9.0
        for tag, side in (("L", -1), ("R", 1)):
            sv, sf = ev(parts["SCULPT_BOOT_SHAFT_" + tag], dg); fv, ff = ev(parts["SCULPT_BOOT_FOOT_" + tag], dg)
            st = BVHTree.FromPolygons(sv, sf); ft = BVHTree.FromPolygons(fv, ff)
            for k, c0 in tro_rest.items():                       # trouser leg inside the shaft's height band stays inside
                if 0.140 < c0.z < 0.275 and math.copysign(1, c0.x) == side and not inside(st, bv[k]): nt += 1
            for c0, c in zip(rest["SCULPT_BOOT_SHAFT_" + tag], sv):   # the shaft's lower edge stays inside the boot foot
                if c0.z < SHAFT_EDGE and not inside(ft, c):
                    nc += 1; hc = max(hc, ft.find_nearest(c, 0.1)[3] or 0.0)
            zboth = min(zboth, min(c.z for c in fv))
        w["sole"] = (min(w["sole"][0], zboth), max(w["sole"][1], zboth))
        oz = min(bv[k].z for k in shoe); w["orig"] = (min(w.get("orig", (9, -9))[0], oz), max(w.get("orig", (9, -9))[1], oz))
        if nt > w["trousers"][0]: w["trousers"] = (nt, round(float(fr), 2))
        if nc > w["crack"][0] or hc > w["crack"][1]: w["crack"] = (max(nc, w["crack"][0]), max(hc, w["crack"][1]), round(float(fr), 2))
    print("CLIP %-6s %d samples: trouser vertices outside a shaft: worst %d at %s | shaft lower edge outside the boot foot: worst %d vertices, up to %.1f mm, at %s | lowest point of either boot Z %.3f to %.3f (original soles, same samples: %.3f to %.3f)" % (an, NS, w["trousers"][0], w["trousers"][1], w["crack"][0], w["crack"][1]*1000, w["crack"][2], w["sole"][0], w["sole"][1], w["orig"][0], w["orig"][1]))
rig.animation_data.action = None; sc.frame_set(0)
for pb in rig.pose.bones: pb.matrix_basis.identity()
for n, o in parts.items(): o.modifiers.clear(); o.parent = bpy.data.objects["SCULPT_BOOTS_ROOT"]
# ---- export: identity root with the four static parts, actor space ----------------------------------------
root = bpy.data.objects["SCULPT_BOOTS_ROOT"]; assert root.matrix_world == root.matrix_world.Identity(4)
for o in bpy.data.objects: o.select_set(False)
for o in [root] + list(parts.values()): o.hide_set(False); o.select_set(True)
bpy.context.view_layer.objects.active = root
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=True, export_apply=True, export_yup=True, export_animations=False, export_skins=False,
                          export_cameras=False, export_lights=False, export_extras=True, export_materials='EXPORT')
before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=out); new = [o for o in bpy.data.objects if o not in before]
meshes = {o.name.split(".")[0]: o for o in new if o.type == 'MESH'}
assert sorted(meshes) == sorted(NAMES), sorted(meshes)
assert not [o for o in new if o.type in ('ARMATURE', 'CAMERA', 'LIGHT')]
tt = 0
for n, o in sorted(meshes.items()):
    co = np.array([o.matrix_world @ v.co for v in o.data.vertices]); tris = sum(len(p.vertices)-2 for p in o.data.polygons); tt += tris
    print("GLB %-20s bind_bone %-7s verts %5d tris %5d materials %s bounds min %s max %s" % (n, o.get("bind_bone"), len(co), tris, [m.name.split(".")[0] for m in o.data.materials], np.round(co.min(0), 3), np.round(co.max(0), 3)))
print("GLB total %d triangles, 4 parts, no armature, camera or light. EXPORTED %s" % (tt, out))
