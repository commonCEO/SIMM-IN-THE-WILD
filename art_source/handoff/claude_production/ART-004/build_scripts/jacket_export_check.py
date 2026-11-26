# Checks and exports the jacket candidate (v002: jacket plus trim). Nothing is saved back to the .blend.
# blender -b jacket_candidate.blend --python jacket_export_check.py -- <absolute out.glb> <absolute out_vertex_map.json>
# Any failed assert stops the run before or after export; a GLB written by a failed run must not be delivered.
import bpy, sys, json, numpy as np
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
sys.dont_write_bytecode = True
out, out_json = sys.argv[sys.argv.index("--")+1:][:2]
body = bpy.data.objects["PROTECTED_BODY"]; rig = bpy.data.objects["SimmRig"]; sc = bpy.context.scene
PARTS = {"SCULPT_JACKET": "Simm golden canvas jacket.001", "SCULPT_JACKET_TRIM": "Simm golden seam binding.001"}
mat_index = {m.name: i for i, m in enumerate(body.data.materials) if m}
bco = [v.co.copy() for v in body.data.vertices]

# ---- manifest and preservation contract, per part ------------------------------------------------------------
parts = {}; vmap = {}
for name, src_mat in PARTS.items():
    assert [o.name for o in bpy.data.objects if o.name == name or o.name.startswith(name + ".")] == [name], "missing or duplicate part " + name
    ob = bpy.data.objects[name]; me = ob.data
    assert [g.name for g in ob.vertex_groups] == [g.name for g in body.vertex_groups], name + ": vertex group names or order differ"
    oi = [d.value for d in me.attributes["orig_index"].data]
    assert len(set(oi)) == len(oi) == len(me.vertices), name + ": orig_index is not one-to-one"
    sm_ = mat_index[src_mat]; src_faces = [tuple(sorted(p.vertices)) for p in body.data.polygons if p.material_index == sm_]
    src_verts = set(i for f in src_faces for i in f); S_ = set(oi)
    assert S_ <= src_verts, name + ": holds a vertex that is not in the source material"
    kept = sorted(f for f in src_faces if set(f) <= S_)
    assert sorted(tuple(sorted(oi[i] for i in p.vertices)) for p in me.polygons) == kept, name + ": face connectivity differs from the original"
    assert set(i for f in kept for i in f) == S_, name + ": a kept vertex has lost one of its original faces"
    maxinf = 0; moved = []
    for v, k in zip(me.vertices, oi):
        a = sorted((g.group, round(g.weight, 6)) for g in v.groups); b = sorted((g.group, round(g.weight, 6)) for g in body.data.vertices[k].groups)
        assert a == b, "%s: weights differ at original vertex %d" % (name, k)
        maxinf = max(maxinf, sum(1 for g in v.groups if g.weight > 0)); moved.append((v.co - bco[k]).length)
    bones = sorted(set(ob.vertex_groups[g.group].name for v in me.vertices for g in v.groups if g.weight > 0))
    co = np.array([v.co[:] for v in me.vertices]); tris = sum(len(p.vertices)-2 for p in me.polygons)
    print("PART %s: %d verts, %d tris, material %s, source material '%s' (%d of its %d vertices, %d of its %d faces kept)" % (name, len(oi), tris, [m.name for m in me.materials], src_mat, len(S_), len(src_verts), len(kept), len(src_faces)))
    print("  preserved: original vertices only, connectivity, group order and every weight identical; max influences %d; bones used %s" % (maxinf, bones))
    print("  moved: max %.1f mm, mean %.1f mm; bounds min %s max %s" % (max(moved)*1000, np.mean(moved)*1000, np.round(co.min(0), 3), np.round(co.max(0), 3)))
    parts[name] = (ob, oi); vmap[name] = [[k, [round(x, 6) for x in bco[k]], [round(x, 6) for x in v.co]] for v, k in zip(me.vertices, oi)]
jk, joi = parts["SCULPT_JACKET"]; tr, toi = parts["SCULPT_JACKET_TRIM"]
jm = mat_index[PARTS["SCULPT_JACKET"]]

# ---- frozen parts that sit on the jacket ---------------------------------------------------------------------
tree_of = lambda ob: BVHTree.FromPolygons([v.co.copy() for v in ob.data.vertices], [tuple(p.vertices) for p in ob.data.polygons])
new_t = tree_of(jk); trim_t = tree_of(tr)
old_t = BVHTree.FromPolygons(bco, [tuple(p.vertices) for p in body.data.polygons if p.material_index == jm])
def mat_verts(names):
    ids = [mat_index[n] for n in names]; vs = set()
    for p in body.data.polygons:
        if p.material_index in ids: vs.update(p.vertices)
    return vs
for names in (("Simm olive canvas", "Simm woven olive straps", "Simm canvas seams"), ("Simm folded hood canvas",)):
    sunk = 0; fl = []; n = 0; was = []
    for k in mat_verts(names):
        c = bco[k]; lo = old_t.find_nearest(c, 0.012)
        if lo[0] is None: continue
        n += 1; ln = new_t.find_nearest(c, 0.08); sd = (c - ln[0]).dot(ln[1]); was.append(lo[3])
        if sd < -0.001: sunk += 1
        else: fl.append(ln[3])
    print("ONJACKET %-52s tracked %3d (they sat up to %.1f mm, mean %.1f mm, above the old jacket); now under the cloth: %d; above it: max %.1f mm, mean %.1f mm" % ("/".join(names), n, max(was)*1000, np.mean(was)*1000, sunk, max(fl)*1000, np.mean(fl)*1000))
btn = [k for k in mat_verts(("Simm brass fasteners",)) if 0.03 < bco[k].x < 0.06 and 0.85 < bco[k].z < 0.90 and bco[k].y < -0.10]
bd = [min(trim_t.find_nearest(bco[k], 0.1)[3], new_t.find_nearest(bco[k], 0.1)[3]) for k in btn]
back = [d for k, d in zip(btn, bd) if bco[k].y > -0.1385]
print("BUTTON %d frozen vertices; its back face is %.1f to %.1f mm from the trim or jacket surface; whole button within %.1f mm" % (len(btn), min(back)*1000, max(back)*1000, max(bd)*1000))

# ---- clips: cloth against the hands, 25 samples per clip -------------------------------------------------------
# Hand triangles only: warm-skin triangles whose every vertex is more than 50 percent on hand_l or hand_r.
# Inside test: a cloth vertex counts when it is more than 1 mm behind the nearest hand surface AND a ray from it
# along that surface normal leaves the hand (an odd number of hand crossings), so thin or open surfaces do not count.
gn_ = [g.name for g in body.vertex_groups]
def hand_side(k):
    w = {gn_[g.group]: g.weight for g in body.data.vertices[k].groups}
    return "hand_l" if w.get("hand_l", 0) > 0.5 else "hand_r" if w.get("hand_r", 0) > 0.5 else None
sm = mat_index["Simm warm skin"]
hand_faces = [tuple(p.vertices) for p in body.data.polygons if p.material_index == sm and all(hand_side(k) for k in p.vertices)]
other_skin = sum(1 for p in body.data.polygons if p.material_index == sm) - len(hand_faces)
print("HANDS %d hand triangles used (all vertices over 50 percent on hand_l or hand_r); %d other warm-skin faces excluded" % (len(hand_faces), other_skin))
from mathutils import Vector
def inside_hand(tree, c):
    loc, nrm, idx, d = tree.find_nearest(c, 0.03)
    if loc is None or (c - loc).dot(nrm) > -0.001: return 0.0
    n = 0; o = c.copy(); dirv = Vector((0.13, 0.27, 0.95)).normalized()
    for _ in range(12):
        h = tree.ray_cast(o, dirv, 0.2)
        if h[0] is None: break
        n += 1; o = h[0] + dirv*1e-5
    return d if n % 2 == 1 else 0.0
import os
NS = int(os.environ.get("SAMPLES", "25"))               # samples per clip; 25 by default, more for a dense check
if rig.animation_data is None: rig.animation_data_create()
contacts = []
for an in ("idle", "walk", "gather"):
    act = bpy.data.actions[an]; rig.animation_data.action = act; f0, f1 = act.frame_range; per = {}
    for fr in np.linspace(f0, f1, NS):
        sc.frame_set(int(fr), subframe=float(fr - int(fr))); dg = bpy.context.evaluated_depsgraph_get()
        eb = body.evaluated_get(dg); mb = eb.to_mesh(); bv = [v.co.copy() for v in mb.vertices]
        t = BVHTree.FromPolygons(bv, hand_faces)
        for name, (ob, oi) in parts.items():
            ev = ob.evaluated_get(dg); me_ = ev.to_mesh(); n = 0; deep = 0.0
            for i, v in enumerate(me_.vertices):
                d = inside_hand(t, v.co)
                if d > 0: n += 1; deep = max(deep, d); contacts.append((an, round(float(fr), 2), name, oi[i], round(d*1000, 1)))
            ev.to_mesh_clear(); w = per.get(name, (0, 0.0, None)); per[name] = (n, deep, round(float(fr), 2)) if n > w[0] else w
        eb.to_mesh_clear()
    for name in parts:
        n, deep, at = per.get(name, (0, 0.0, None))
        print("CLIP %-6s %-18s inside a hand, worst of %d samples: %d vertices, up to %.1f mm, at frame %s" % (an, name, NS, n, deep*1000, at))
for c in contacts[:40]: print("CONTACT clip %s frame %s part %s original vertex %d depth %.1f mm" % c)
print("CONTACT total vertex-frame contacts: %d" % len(contacts))
rig.animation_data.action = None; sc.frame_set(0)
for pb in rig.pose.bones: pb.matrix_basis.identity()        # in memory only: back to rest before export

json.dump({"source_object": "PROTECTED_BODY", "axes": "Blender Z-up, metres, front -Y",
           "format": "per part: [original vertex index, original rest position, candidate position]", "parts": vmap}, open(out_json, "w"), separators=(",", ":"))

# ---- export: throwaway copies of the parts on a throwaway rest copy of the skeleton, no animation ------------
rc = rig.copy(); rc.data = rig.data.copy(); rc.name = "SimmRigRestCopy"; rc.animation_data_clear()
sc.collection.objects.link(rc); rc.hide_select = False; rc.hide_viewport = False
for pb in rc.pose.bones: pb.matrix_basis.identity()
copies = []
for name, (ob, oi) in parts.items():
    c = ob.copy(); c.data = ob.data.copy(); sc.collection.objects.link(c); ob.name = name + "_SRC"; c.name = name
    c.modifiers["Armature"].object = rc; c.parent = rc; copies.append(c)
bpy.context.view_layer.update()
for o in bpy.data.objects: o.select_set(False)
for o in copies + [rc]:
    o.hide_set(False); o.select_set(True)
    assert o.select_get()
bpy.context.view_layer.objects.active = copies[0]
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=True, export_animations=False, export_skins=True, export_yup=True, export_apply=False, export_def_bones=False)

# ---- re-import the delivered file and account for every vertex in it -----------------------------------------
TOL = 2e-5                                                    # metres. Float32 round trip, no rounding buckets.
before = set(bpy.data.objects); n_act = len(bpy.data.actions)
bpy.ops.import_scene.gltf(filepath=out)
new = [o for o in bpy.data.objects if o not in before]
arm = [o for o in new if o.type == 'ARMATURE']; meshes = [o for o in new if o.type == 'MESH']
assert len(arm) == 1 and len(meshes) == len(PARTS), [o.name for o in new]
assert len(bpy.data.actions) == n_act, "the GLB carries an animation"
ib = {b.name: b for b in arm[0].data.bones}; rb = {b.name: b for b in rig.data.bones}
assert sorted(ib) == sorted(rb), "bone names differ"
worst_head = 0.0
for n_, b in rb.items():
    assert (ib[n_].parent.name if ib[n_].parent else None) == (b.parent.name if b.parent else None), "parent differs for " + n_
    worst_head = max(worst_head, ((arm[0].matrix_world @ ib[n_].head_local) - (rig.matrix_world @ b.head_local)).length)
assert worst_head < 1e-5, "rest joint position differs by %.6f" % worst_head
print("GLB skeleton: %d bones, names and parents match the rig, largest rest joint difference %.7f m, animations 0" % (len(ib), worst_head))
total = 0
for name, (ob, oi) in parts.items():
    m = [x for x in meshes if x.name.split(".")[0] == name]
    assert len(m) == 1, "part %s not found once in the GLB: %s" % (name, [x.name for x in meshes])
    m = m[0]; gi = {g.index: g.name for g in m.vertex_groups}; gs = {g.index: g.name for g in ob.vertex_groups}
    kd = KDTree(len(ob.data.vertices))
    for i, v in enumerate(ob.data.vertices): kd.insert(v.co, i)
    kd.balance(); hit = set(); unmatched = 0; wbad = 0; worst = 0.0; far = 0.0
    for v in m.data.vertices:
        w = m.matrix_world @ v.co; cands = kd.find_range(w, TOL)
        if not cands: unmatched += 1; far = max(far, kd.find(w)[2]); continue
        a = {gi[g.group]: g.weight for g in v.groups if g.weight > 1e-6}; best = 9.0
        for c_, i, dist in cands:                              # coincident source vertices are all tried
            b = {gs[g.group]: g.weight for g in ob.data.vertices[i].groups if g.weight > 1e-6}
            dd = max(abs(a.get(k, 0) - b.get(k, 0)) for k in set(a) | set(b))
            if dd < best: best = dd; bi = i
        hit.add(bi); worst = max(worst, best); wbad += best > 1e-5
    n = len(m.data.vertices); total += n; co = np.array([m.matrix_world @ v.co for v in m.data.vertices])
    print("GLB %s: %d vertices in the file, %d tris, materials %s, bounds min %s max %s" % (name, n, sum(len(p.vertices)-2 for p in m.data.polygons), [x.name.split(".")[0] for x in m.data.materials], np.round(co.min(0), 3), np.round(co.max(0), 3)))
    print("  matched to a source vertex within %.0f micrometres: %d of %d; unmatched %d; source vertices covered %d of %d; largest weight difference %.7f; vertices over 0.00001: %d" % (TOL*1e6, n - unmatched, n, unmatched, len(hit), len(oi), worst, wbad))
    assert unmatched == 0, "%s: %d exported vertices have no source vertex within tolerance (farthest %.6f m)" % (name, unmatched, far)
    assert len(hit) == len(oi), "%s: %d source vertices are not in the export" % (name, len(oi) - len(hit))
    assert wbad == 0, "%s: %d exported vertices differ in weight" % (name, wbad)
print("GLB all %d vertices accounted for. EXPORTED %s" % (total, out))
