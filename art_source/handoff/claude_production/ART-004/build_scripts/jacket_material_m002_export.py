# Exports the m002 material candidate and proves the geometry is f002's. Nothing is saved back.
#   blender -b <m002 blend> --python jacket_material_m002_export.py -- <absolute out.glb> <absolute out_manifest.json> <absolute f002 glb>
# Export as jacket_finish_check.py (three parts on a rest copy of the 17-bone skeleton, no animation), then:
#  1. Blender re-import: every GLB vertex matches a source vertex within 20 micrometres with identical weights, and every
#     source vertex is covered (asserted).
#  2. Raw GLB comparison with the f002 GLB, per mesh: the set of distinct (position, joints, weights) records, bit-exact, is
#     the same in both files, and every normal is within 5e-4 of f002's at that record (asserted; f001 notes the same
#     export float noise). The UV seams of the new unwrap only duplicate records; they cannot add new ones. Index lists
#     are compared as triangles of records (asserted equal as multisets).
#  3. Materials, UV sets, colour sets and embedded images of both files are listed.
import bpy, sys, os, json, struct, hashlib, numpy as np
from mathutils.kdtree import KDTree
sys.dont_write_bytecode = True
out, out_json, f002 = sys.argv[sys.argv.index("--")+1:][:3]
PARTS = ("SCULPT_JACKET_LONG", "SCULPT_JACKET_LONG_TRIM", "SCULPT_JACKET_POCKETS")
sc = bpy.context.scene; rig = bpy.data.objects["SimmRig"]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
for n in PARTS:
    assert [o.name for o in bpy.data.objects if o.name == n or o.name.startswith(n + ".")] == [n], "missing or duplicate part " + n
if rig.animation_data:
    rig.animation_data.action = None
    for t in rig.animation_data.nla_tracks: t.mute = True
sc.frame_set(0)
for pb in rig.pose.bones: pb.matrix_basis.identity()
rc = rig.copy(); rc.data = rig.data.copy(); rc.name = "SimmRigRestCopy"; rc.animation_data_clear()
sc.collection.objects.link(rc); rc.hide_select = False; rc.hide_viewport = False
copies = []
for n in PARTS:
    ob = bpy.data.objects[n]; c = ob.copy(); c.data = ob.data.copy(); sc.collection.objects.link(c); ob.name = n + "_SRC"; c.name = n
    c.modifiers["Armature"].object = rc; c.parent = rc; copies.append(c)
bpy.context.view_layer.update()
for o in bpy.data.objects: o.select_set(False)
for o in copies + [rc]: o.hide_set(False); o.select_set(True)
bpy.context.view_layer.objects.active = copies[0]
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=True, export_animations=False, export_skins=True, export_yup=True, export_apply=False, export_def_bones=False)

R = {"glb": {"file": os.path.basename(out), "sha256": sha(out), "bytes": os.path.getsize(out)}, "f002_glb_sha256": sha(f002), "parts": {}}
before = set(bpy.data.objects); n_act = len(bpy.data.actions)
bpy.ops.import_scene.gltf(filepath=out)
newo = [o for o in bpy.data.objects if o not in before]
arm = [o for o in newo if o.type == 'ARMATURE']; meshes = [o for o in newo if o.type == 'MESH']
assert len(arm) == 1 and len(meshes) == len(PARTS) and len(bpy.data.actions) == n_act, [o.name for o in newo]
ib = {b.name: b for b in arm[0].data.bones}; rb = {b.name: b for b in rig.data.bones}; assert sorted(ib) == sorted(rb)
wh = max(((arm[0].matrix_world @ ib[n].head_local) - (rig.matrix_world @ b.head_local)).length for n, b in rb.items()); assert wh < 1e-5, wh
for n in PARTS:
    src = bpy.data.objects[n + "_SRC"]; m = [x for x in meshes if x.name.split(".")[0] == n]; assert len(m) == 1, n; m = m[0]
    gi = {g.index: g.name for g in m.vertex_groups}; gs = {g.index: g.name for g in src.vertex_groups}
    kd = KDTree(len(src.data.vertices))
    for i, v in enumerate(src.data.vertices): kd.insert(v.co, i)
    kd.balance(); hit = set(); un = 0; wbad = 0
    for v in m.data.vertices:
        cands = kd.find_range(m.matrix_world @ v.co, 2e-5)
        if not cands: un += 1; continue
        a = {gi[g.group]: g.weight for g in v.groups if g.weight > 1e-6}; best = 9.0; bi = None
        for _, i, _ in cands:
            b = {gs[g.group]: g.weight for g in src.data.vertices[i].groups if g.weight > 1e-6}
            dd = max(abs(a.get(k, 0) - b.get(k, 0)) for k in set(a) | set(b))
            if dd < best: best = dd; bi = i
        hit.add(bi); wbad += best > 1e-5
    co = np.array([m.matrix_world @ v.co for v in m.data.vertices])
    R["parts"][n] = {"reimport_vertices_in_file": len(m.data.vertices), "triangles": sum(len(p.vertices) - 2 for p in m.data.polygons),
                     "bounds_min": np.round(co.min(0), 4).tolist(), "bounds_max": np.round(co.max(0), 4).tolist(),
                     "unmatched": un, "covered": len(hit), "source_vertices": len(src.data.vertices), "weight_mismatches": wbad}
    print("GLBACC", n, "unmatched", un, "covered", len(hit), "of", len(src.data.vertices), "weight mismatches", wbad)
    assert un == 0 and len(hit) == len(src.data.vertices) and wbad == 0, n + ": GLB accounting failed"

def load(p):
    d = open(p, "rb").read(); n = struct.unpack("<I", d[12:16])[0]; g = json.loads(d[20:20+n]); o = 20 + n
    bl = struct.unpack("<I", d[o:o+4])[0]; return g, d[o+8:o+8+bl]
CT = {5126: np.float32, 5123: np.uint16, 5125: np.uint32, 5121: np.uint8}
NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}
def acc(g, b, i):
    a = g["accessors"][i]; v = g["bufferViews"][a["bufferView"]]; off = v.get("byteOffset", 0) + a.get("byteOffset", 0); nc = NC[a["type"]]
    x = np.frombuffer(b, dtype=CT[a["componentType"]], count=a["count"]*nc, offset=off).reshape(a["count"], nc)
    if a.get("normalized"): x = x.astype(np.float64) / np.iinfo(x.dtype).max
    return x
def records(g, b, mesh):
    # key = exact position, joints and weights; the normal is kept beside the key and compared with a tolerance
    out_ = {"norm": {}, "tris": [], "verts": 0, "attrs": set(), "materials": []}
    for pr in mesh["primitives"]:
        at = pr["attributes"]; P = acc(g, b, at["POSITION"]); N = acc(g, b, at["NORMAL"]); J = acc(g, b, at["JOINTS_0"]); W = acc(g, b, at["WEIGHTS_0"])
        keys = [P[i].tobytes() + J[i].astype(np.uint16).tobytes() + W[i].astype(np.float32).tobytes() for i in range(len(P))]
        for k, nv in zip(keys, N): out_["norm"].setdefault(k, []).append(nv.astype(float))
        idx = acc(g, b, pr["indices"]).ravel()
        out_["tris"] += [tuple(sorted((keys[idx[3*t]], keys[idx[3*t+1]], keys[idx[3*t+2]]))) for t in range(len(idx)//3)]
        out_["verts"] += len(P); out_["attrs"].update(at); out_["materials"].append(g["materials"][pr["material"]]["name"] if "material" in pr else None)
    return out_
NTOL = 5e-4   # exports of the same blend differ in a few jacket normals by up to about 1e-4 (float noise)
G = {}
for tag, p in (("m002", out), ("f002", f002)):
    g, b = load(p); G[tag] = (g, b)
for n in PARTS:
    me = {tag: [G[tag][0]["meshes"][nd["mesh"]] for nd in G[tag][0]["nodes"] if nd.get("name") == n and "mesh" in nd] for tag in G}
    assert all(len(v) == 1 for v in me.values()), n + ": node missing or duplicated in a GLB"
    A = records(*G["m002"], me["m002"][0]); F = records(*G["f002"], me["f002"][0])
    same_keys = set(A["norm"]) == set(F["norm"]); same_tris = sorted(A["tris"]) == sorted(F["tris"])
    dn = max(float(np.abs(np.array(a) - np.array(f)).max()) for k in A["norm"] if k in F["norm"] for a in A["norm"][k] for f in F["norm"][k][:1])
    R["parts"][n].update({"glb_vertices_m002": A["verts"], "glb_vertices_f002": F["verts"], "distinct_records_m002": len(A["norm"]), "distinct_records_f002": len(F["norm"]), "max_normal_difference": round(dn, 7),
                          "same_position_joint_weight_records_as_f002": same_keys, "normals_within": NTOL, "same_triangles_as_f002": same_tris,
                          "attributes_m002": sorted(A["attrs"]), "attributes_f002": sorted(F["attrs"]), "materials_m002": A["materials"], "materials_f002": F["materials"]})
    print("F002CMP", n, "records", len(A["norm"]), len(F["norm"]), "same", same_keys, "max normal diff", dn, "tris same", same_tris, sorted(A["attrs"]), "vs", sorted(F["attrs"]))
    assert same_keys and same_tris and dn < NTOL, n + ": geometry differs from f002 GLB"
g, b = G["m002"]
R["glb"]["images"] = []
for im in g.get("images", []):
    v = g["bufferViews"][im["bufferView"]]; data = b[v.get("byteOffset", 0):v.get("byteOffset", 0) + v["byteLength"]]
    R["glb"]["images"].append({"name": im.get("name"), "mimeType": im.get("mimeType"), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
R["glb"]["materials"] = g["materials"]; R["glb"]["textures"] = g.get("textures", []); R["glb"]["samplers"] = g.get("samplers", [])
R["glb"]["skins"] = len(g.get("skins", [])); R["glb"]["animations"] = len(g.get("animations", [])); R["glb"]["cameras"] = len(g.get("cameras", []))
R["glb"]["extensionsUsed"] = g.get("extensionsUsed", [])
json.dump(R, open(out_json, "w"), indent=1)
print("EXPORTED", out, R["glb"]["sha256"], json.dumps(R["glb"]["images"]))
