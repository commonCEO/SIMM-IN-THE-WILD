# Checks and exports jacket candidate v004 (SCULPT_JACKET_LONG + SCULPT_JACKET_LONG_TRIM). Nothing is saved back.
# blender -b <v004 blend, optionally with the gather_handclear study action added> --python jacket_long_check.py -- \
#     <absolute out.glb> <absolute out_manifest.json> <absolute v003 source blend>
# SAMPLES env (default 97) sets samples per clip. Any failed assert stops the run; a GLB from a failed run is not delivered.
import bpy, sys, os, json, math, hashlib, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
sys.dont_write_bytecode = True
out, out_json, v003_blend = sys.argv[sys.argv.index("--")+1:][:3]
NS = int(os.environ.get("SAMPLES", "97")); Z_CUT, Z_HEM = 0.655, 0.480
body = bpy.data.objects["PROTECTED_BODY"]; rig = bpy.data.objects["SimmRig"]; sc = bpy.context.scene
PARTS = ("SCULPT_JACKET_LONG", "SCULPT_JACKET_LONG_TRIM"); V3 = {"SCULPT_JACKET_LONG": "SCULPT_JACKET", "SCULPT_JACKET_LONG_TRIM": "SCULPT_JACKET_TRIM"}
R = {"parts": {}, "clips": {}, "residuals": []}
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
R["sources"] = {"v004_build_input_v003_blend": os.path.basename(v003_blend), "v003_blend_sha256": sha(v003_blend), "checked_blend": os.path.basename(bpy.data.filepath)}

# ---- manifest -------------------------------------------------------------------------------------------------
for n in PARTS:
    assert [o.name for o in bpy.data.objects if o.name == n or o.name.startswith(n + ".")] == [n], "missing or duplicate part " + n
for n in V3.values(): assert n not in bpy.data.objects, "v003 part %s still in the candidate file" % n
for n in PARTS:
    ob = bpy.data.objects[n]
    assert [g.name for g in ob.vertex_groups] == [g.name for g in body.vertex_groups], n + ": vertex group names or order differ"
    assert ob.modifiers[0].type == 'ARMATURE' and ob.modifiers[0].object == rig and len(ob.modifiers) == 1, n + ": modifier stack"
with bpy.data.libraries.load(v003_blend, link=False) as (src, dst):
    dst.meshes = [m for m in src.meshes if m in ("SCULPT_JACKET", "SCULPT_JACKET_TRIM")]
v3m = {m.name.split(".")[0]: m for m in dst.meshes}
for n in PARTS:
    ob = bpy.data.objects[n]; me = ob.data; m3 = v3m[V3[n]]
    oi = [d.value for d in me.attributes["orig_index"].data]; oi3 = {d.value: i for i, d in enumerate(m3.attributes["orig_index"].data)}
    kept = [i for i, k in enumerate(oi) if k >= 0]; new = len(oi) - len(kept)
    assert len(set(oi[i] for i in kept)) == len(kept), n + ": orig_index repeats"
    moved = 0.0; wdiff = 0.0
    for i in kept:
        j = oi3[oi[i]]; moved = max(moved, (me.vertices[i].co - m3.vertices[j].co).length)
        a = {g.group: g.weight for g in me.vertices[i].groups}; b = {g.group: g.weight for g in m3.vertices[j].groups}
        wdiff = max([wdiff] + [abs(a.get(g, 0) - b.get(g, 0)) for g in set(a) | set(b)])
    gone = [j for k, j in oi3.items() if k not in set(oi[i] for i in kept)]
    gz = max(m3.vertices[j].co.z for j in gone) if gone else None
    assert moved < 1e-7 and wdiff < 1e-6, "%s: a kept v003 vertex moved %.2e m or changed weight %.2e" % (n, moved, wdiff)
    inf = [sum(1 for g in v.groups if g.weight > 0) for v in me.vertices]; ws = [sum(g.weight for g in v.groups) for v in me.vertices]
    assert max(inf) <= 4 and min(ws) > 0.999 and max(ws) < 1.001, n + ": weights over 4 influences or not normalised"
    nm = 0
    import bmesh
    bm = bmesh.new(); bm.from_mesh(me); nm = sum(1 for e in bm.edges if len(e.link_faces) != 2); bm.free()
    co = np.array([v.co[:] for v in me.vertices]); tris = sum(len(p.vertices)-2 for p in me.polygons)
    bones = sorted(set(ob.vertex_groups[g.group].name for v in me.vertices for g in v.groups if g.weight > 0))
    newbones = sorted(set(ob.vertex_groups[g.group].name for i, v in enumerate(me.vertices) if oi[i] < 0 for g in v.groups if g.weight > 0))
    R["parts"][n] = {"vertices": len(oi), "triangles": tris, "v003_vertices_kept_unchanged": len(kept), "new_vertices": new,
                     "v003_vertices_removed": len(gone), "highest_removed_v003_vertex_z": gz, "material": [m.name for m in me.materials],
                     "bones": bones, "bones_on_new_vertices": newbones, "max_influences": max(inf), "non_manifold_edges": nm,
                     "bounds_min": np.round(co.min(0), 4).tolist(), "bounds_max": np.round(co.max(0), 4).tolist(), "replaces": V3[n]}
    print("PART %s replaces %s: %d verts (%d v003 vertices kept with identical position and weights, %d new), %d tris, %d v003 vertices removed (highest at Z %s); non-manifold edges %d; max influences %d; bones %s" % (n, V3[n], len(oi), len(kept), new, tris, len(gone), ("%.3f" % gz) if gz is not None else "-", nm, max(inf), bones))

# ---- clips -----------------------------------------------------------------------------------------------------
mi = {m.name: i for i, m in enumerate(body.data.materials) if m}; gn = [g.name for g in body.vertex_groups]
def handv(k): return any(gn[g.group] in ("hand_l", "hand_r") and g.weight > 0.5 for g in body.data.vertices[k].groups)
hand_f = [tuple(p.vertices) for p in body.data.polygons if p.material_index == mi["Simm warm skin"] and all(handv(k) for k in p.vertices)]
tro = sorted(set(k for p in body.data.polygons if p.material_index == mi["Simm charcoal olive trousers"] for k in p.vertices))
tro = [k for k in tro if Z_HEM + 0.003 < body.data.vertices[k].co.z < 0.70]
DIR = Vector((0.13, 0.27, 0.95)).normalized()
def parity(t, c):
    n = 0; o = c.copy()
    for _ in range(24):
        h = t.ray_cast(o, DIR, 2.0)
        if h[0] is None: break
        n += 1; o = h[0] + DIR*1e-6
    return n % 2 == 1
def inside_hand(t, c):
    loc, nrm, idx, d = t.find_nearest(c, 0.03)
    if loc is None or (c - loc).dot(nrm) > -0.001: return 0.0
    return d if parity(t, c) else 0.0
G = bpy.data.objects[PARTS[0]]; T = bpy.data.objects[PARTS[1]]
oiG = [d.value for d in G.data.attributes['orig_index'].data]; oiT = [d.value for d in T.data.attributes['orig_index'].data]
eG = [tuple(e.vertices) for e in G.data.edges]; eT = [tuple(e.vertices) for e in T.data.edges]
newG = np.array([oiG[a] < 0 or oiG[b] < 0 for a, b in eG]); newT = np.array([oiT[a] < 0 or oiT[b] < 0 for a, b in eT])
rlG = np.array([(G.data.vertices[a].co - G.data.vertices[b].co).length for a, b in eG]); rlT = np.array([(T.data.vertices[a].co - T.data.vertices[b].co).length for a, b in eT])
if rig.animation_data is None: rig.animation_data_create()
for tr_ in rig.animation_data.nla_tracks: tr_.mute = True
clips = [c for c in ("idle", "walk", "gather", "gather_handclear") if c in bpy.data.actions]
for an in clips:
    act = bpy.data.actions[an]; rig.animation_data.action = act; f0, f1 = act.frame_range; mid = 0.5*(f0 + f1)
    W = {}; mincl = (9.0, None, None); hgap = (9.0, None, None, None)
    for fr in np.linspace(f0, f1, NS):
        half = "all" if an != "walk" else ("first half" if fr < mid else "second half")
        w = W.setdefault(half, {"tro": (0, 0.0, None, []), "hand": (0, 0.0, None, []), "stG": (0.0, None, None), "stT": (0.0, None, None), "stGn": (0.0, None, None), "stTn": (0.0, None, None)})
        sc.frame_set(int(fr), subframe=float(fr - int(fr))); dg = bpy.context.evaluated_depsgraph_get()
        eb = body.evaluated_get(dg); mb = eb.to_mesh(); bv = [v.co.copy() for v in mb.vertices]; eb.to_mesh_clear()
        meshes = {}
        for ob in (G, T):
            e = ob.evaluated_get(dg); m = e.to_mesh(); meshes[ob.name] = ([v.co.copy() for v in m.vertices], [tuple(p.vertices) for p in m.polygons]); e.to_mesh_clear()
        gv, gf = meshes[G.name]; tv, tf = meshes[T.name]; gt = BVHTree.FromPolygons(gv, gf)
        Hm = rig.evaluated_get(dg).pose.bones["hips"].matrix; ax = Hm.translation; up = (Hm.to_3x3() @ Vector((0, 1, 0))).normalized()
        bad = []
        for k in tro:
            p = bv[k]; rel = p - ax; rad = rel - up*rel.dot(up); rl = rad.length
            if rl < 1e-4: continue
            d = rad/rl; near = gt.find_nearest(p, 0.05)
            if parity(gt, p): bad.append((k, near[3] if near[0] is not None else 0.0, "inside the cloth")); continue
            if gt.ray_cast(p + d*1e-4, d, 0.25)[0] is None:
                if gt.ray_cast(p - d*1e-4, -d, rl)[0] is not None: bad.append((k, near[3] if near[0] is not None else 0.0, "outside the cloth"))
            elif near[0] is not None and near[3] < mincl[0]: mincl = (near[3], round(float(fr), 2), k)
        if len(bad) > w["tro"][0]: w["tro"] = (len(bad), max(b[1] for b in bad), round(float(fr), 2), bad)
        for b in bad: R["residuals"].append({"clip": an, "frame": round(float(fr), 2), "kind": "trousers " + b[2], "body_vertex": b[0], "depth_mm": round(b[1]*1000, 2)})
        ht = BVHTree.FromPolygons(bv, hand_f); hb = []
        for nm_, vs in ((G.name, gv), (T.name, tv)):
            for i, c in enumerate(vs):
                dd = inside_hand(ht, c)
                if dd > 0: hb.append((nm_, i, dd))
                else:
                    nr = ht.find_nearest(c, 0.03)
                    if nr[0] is not None and nr[3] < hgap[0]: hgap = (nr[3], round(float(fr), 2), nm_, i)
        if len(hb) > w["hand"][0]: w["hand"] = (len(hb), max(h[2] for h in hb), round(float(fr), 2), hb)
        for h in hb: R["residuals"].append({"clip": an, "frame": round(float(fr), 2), "kind": "cloth inside a hand", "part": h[0], "vertex": h[1], "depth_mm": round(h[2]*1000, 2)})
        for key, vs, ed, rl_, nw in (("stG", gv, eG, rlG, newG), ("stT", tv, eT, rlT, newT)):
            pl = np.array([(vs[a] - vs[b]).length for a, b in ed]); r_ = pl/np.maximum(rl_, 1e-6)
            for kk, sel in ((key, ~nw), (key + "n", nw)):
                rr = np.where(sel, r_, 0.0); i = int(rr.argmax())
                if rr[i] > w[kk][0]: w[kk] = (float(rr[i]), round(float(fr), 2), ed[i])
    R["clips"][an] = {}
    for half, w in W.items():
        R["clips"][an][half] = {"trouser_points_through_cloth_worst": w["tro"][0], "deepest_mm": round(w["tro"][1]*1000, 2), "at_frame": w["tro"][2],
                                "cloth_vertices_in_hand_worst": w["hand"][0], "hand_deepest_mm": round(w["hand"][1]*1000, 2), "hand_at_frame": w["hand"][2],
                                "jacket_edge_stretch_max": round(w["stG"][0], 3), "jacket_stretch_frame": w["stG"][1], "jacket_stretch_edge": w["stG"][2],
                                "trim_edge_stretch_max": round(w["stT"][0], 3), "trim_stretch_frame": w["stT"][1],
                                "held_v003_edges": "stretch_max above is for edges between kept v003 vertices; _new below is for edges touching new vertices",
                                "jacket_new_edge_stretch_max": round(w["stGn"][0], 3), "jacket_new_stretch_frame": w["stGn"][1], "jacket_new_stretch_edge": w["stGn"][2],
                                "trim_new_edge_stretch_max": round(w["stTn"][0], 3), "trim_new_stretch_frame": w["stTn"][1], "trim_new_stretch_edge": w["stTn"][2]}
        print("CLIP %-16s %-11s %d samples: trouser points through the cloth worst %d (deepest %.1f mm) at %s | cloth vertices in a hand worst %d (deepest %.1f mm) at %s | stretch held v003 jacket %.2f trim %.2f; NEW jacket %.2f at %s, NEW trim %.2f at %s" % (an, half, NS, w["tro"][0], w["tro"][1]*1000, w["tro"][2], w["hand"][0], w["hand"][1]*1000, w["hand"][2], w["stG"][0], w["stT"][0], w["stGn"][0], w["stGn"][1], w["stTn"][0], w["stTn"][1]))
    R["clips"][an]["smallest_hand_to_cloth_gap_mm"] = round(hgap[0]*1000, 2) if hgap[1] is not None else None; R["clips"][an]["smallest_hand_gap_at"] = list(hgap[1:])
    print("CLIP %-16s smallest gap between a hand and a cloth vertex outside it: %s mm (frame %s, %s vertex %s)" % (an, round(hgap[0]*1000, 2) if hgap[1] is not None else "over 30", hgap[1], hgap[2], hgap[3]))
    R["clips"][an]["closest_covered_trouser_point_mm"] = round(mincl[0]*1000, 2); R["clips"][an]["closest_at"] = [mincl[1], mincl[2]]
    print("CLIP %-16s closest covered trouser point to the cloth: %.1f mm (frame %s, body vertex %s)" % (an, mincl[0]*1000, mincl[1], mincl[2]))
from collections import Counter
cnt = Counter((r["clip"], r["kind"]) for r in R["residuals"]); print("RESIDUAL vertex-sample counts:", dict(cnt) if cnt else "none")
rig.animation_data.action = None; sc.frame_set(0)
for pb in rig.pose.bones: pb.matrix_basis.identity()

# ---- export: copies on a rest copy of the skeleton, no animation --------------------------------------------------
rc = rig.copy(); rc.data = rig.data.copy(); rc.name = "SimmRigRestCopy"; rc.animation_data_clear()
sc.collection.objects.link(rc); rc.hide_select = False; rc.hide_viewport = False
for pb in rc.pose.bones: pb.matrix_basis.identity()
copies = []
for n in PARTS:
    ob = bpy.data.objects[n]; c = ob.copy(); c.data = ob.data.copy(); sc.collection.objects.link(c); ob.name = n + "_SRC"; c.name = n
    c.modifiers["Armature"].object = rc; c.parent = rc; copies.append(c)
bpy.context.view_layer.update()
for o in bpy.data.objects: o.select_set(False)
for o in copies + [rc]: o.hide_set(False); o.select_set(True)
bpy.context.view_layer.objects.active = copies[0]
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=True, export_animations=False, export_skins=True, export_yup=True, export_apply=False, export_def_bones=False)
before = set(bpy.data.objects); n_act = len(bpy.data.actions)
bpy.ops.import_scene.gltf(filepath=out)
newo = [o for o in bpy.data.objects if o not in before]
arm = [o for o in newo if o.type == 'ARMATURE']; meshes = [o for o in newo if o.type == 'MESH']
assert len(arm) == 1 and len(meshes) == len(PARTS) and len(bpy.data.actions) == n_act, [o.name for o in newo]
ib = {b.name: b for b in arm[0].data.bones}; rb = {b.name: b for b in rig.data.bones}; assert sorted(ib) == sorted(rb)
wh = max(((arm[0].matrix_world @ ib[n].head_local) - (rig.matrix_world @ b.head_local)).length for n, b in rb.items())
assert wh < 1e-5, wh
R["glb"] = {"file": os.path.basename(out), "sha256": sha(out), "bytes": os.path.getsize(out), "bones": len(ib), "largest_rest_joint_difference_m": wh, "animations": 0, "parts": {}}
for n in PARTS:
    src = bpy.data.objects[n + "_SRC"]; m = [x for x in meshes if x.name.split(".")[0] == n]; assert len(m) == 1, n; m = m[0]
    gi = {g.index: g.name for g in m.vertex_groups}; gs = {g.index: g.name for g in src.vertex_groups}
    kd = KDTree(len(src.data.vertices))
    for i, v in enumerate(src.data.vertices): kd.insert(v.co, i)
    kd.balance(); hit = set(); un = 0; wbad = 0
    for v in m.data.vertices:
        w_ = m.matrix_world @ v.co; cands = kd.find_range(w_, 2e-5)
        if not cands: un += 1; continue
        a = {gi[g.group]: g.weight for g in v.groups if g.weight > 1e-6}; best = 9.0; bi = None
        for _, i, _ in cands:
            b = {gs[g.group]: g.weight for g in src.data.vertices[i].groups if g.weight > 1e-6}
            dd = max(abs(a.get(k, 0) - b.get(k, 0)) for k in set(a) | set(b))
            if dd < best: best = dd; bi = i
        hit.add(bi); wbad += best > 1e-5
    co = np.array([m.matrix_world @ v.co for v in m.data.vertices])
    R["glb"]["parts"][n] = {"vertices_in_file": len(m.data.vertices), "triangles": sum(len(p.vertices)-2 for p in m.data.polygons), "materials": [x.name.split(".")[0] for x in m.data.materials],
                            "bounds_min_blender_zup": np.round(co.min(0), 4).tolist(), "bounds_max_blender_zup": np.round(co.max(0), 4).tolist(), "unmatched": un, "source_vertices_covered": len(hit), "source_vertices": len(src.data.vertices), "weight_mismatches": wbad}
    print("GLB %s: %d vertices, %d tris, bounds %s..%s; unmatched %d; source covered %d of %d; weight mismatches %d" % (n, len(m.data.vertices), R["glb"]["parts"][n]["triangles"], np.round(co.min(0), 3), np.round(co.max(0), 3), un, len(hit), len(src.data.vertices), wbad))
    assert un == 0 and len(hit) == len(src.data.vertices) and wbad == 0, n + ": GLB accounting failed"
json.dump(R, open(out_json, "w"), indent=1)
print("EXPORTED", out, R["glb"]["sha256"])
