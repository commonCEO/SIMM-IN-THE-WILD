# ART-015 diagnostic carrier (Codex brief at d64a9e4). Exports the EXISTING reviewed composite (compose_inlay_demo.py,
# no retuning) once, as a static GLB of SCULPT_HEAD, SCULPT_EYE_L, SCULPT_EYE_R and SCULPT_LASHES only, under the same
# root, units and axes as head v012 (SCULPT_HEAD_ROOT, Y-up, modifiers applied, held materials), plus evidence.
#   INLAY_BLEND=<abs scratch inlay head.blend from run_inlay_demo.sh> blender -b inbox/head_candidate_v012.blend \
#       --python compose_inlay_demo.py --python inlay_carrier_export.py -- <abs empty out dir> <abs head_candidate_v012.glb>
# Nothing is saved to any .blend. Writes: simm_inlay_carrier.glb, inlay_carrier_manifest.json, base_vertex_moves.json.
import bpy, sys, os, json, struct, hashlib, numpy as np
out, held_glb = sys.argv[sys.argv.index("--")+1:][:2]
assert os.path.isabs(out) and (not os.path.exists(out) or not os.listdir(out)), "output dir must be absolute and empty"
os.makedirs(out, exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
PARTS = ["SCULPT_HEAD", "SCULPT_EYE_L", "SCULPT_EYE_R", "SCULPT_LASHES"]
# ---- base-mesh moves against the held file (the composite changed the in-memory meshes only)
import tempfile, shutil
held_blend = bpy.data.filepath
tmpd = tempfile.mkdtemp(); held_copy = os.path.join(tmpd, "held_v012_copy.blend"); shutil.copy(held_blend, held_copy)   # Blender
with bpy.data.libraries.load(held_copy) as (src, dst): dst.meshes = [m for m in src.meshes if m in PARTS]          # cannot load from its own open file
HELD = {m.name.split(".")[0]: m for m in dst.meshes}
moves = {}; R = {"packet": "ART-015 inlay diagnostic carrier (Codex brief d64a9e4); NOT a production head", "parts": {}}
for n in PARTS:
    cur = np.array([v.co[:] for v in bpy.data.objects[n].data.vertices]); old = np.array([v.co[:] for v in HELD[n].vertices])
    assert cur.shape == old.shape, n
    dd = np.linalg.norm(cur - old, axis=1); ids = np.where(dd > 5e-8)[0]
    moves[n] = [{"id": int(i), "held": old[i].round(6).tolist(), "carrier": cur[i].round(6).tolist(), "move_mm": round(float(dd[i]*1000), 4)} for i in ids]
    R["parts"][n] = {"base_vertices": len(cur), "base_vertices_moved": int(len(ids)), "base_moved_over_0.05mm": int((dd > 5e-5).sum()), "base_max_move_mm": round(float(dd.max()*1000), 3)}
# composite weights for the head (same rule as compose_inlay_demo.py), reported per moved vertex
h = bpy.data.objects["SCULPT_HEAD"]; W = np.array(h.matrix_world)
H0 = np.array([v.co[:] for v in HELD["SCULPT_HEAD"].vertices]); Hw = H0 @ W[:3, :3].T + W[:3, 3]
def oval_e(P, eye):
    E = np.array([eye.matrix_world @ v.co for v in HELD[eye.name].vertices]); C = 0.5*(E.min(0) + E.max(0)); d = P - C
    return np.sqrt((d[:, 0]/0.0174)**2 + (d[:, 2]/np.where(d[:, 2] < 0, 0.94*0.0264, 0.0264))**2), d
eL, dL = oval_e(Hw, bpy.data.objects["SCULPT_EYE_L"]); eR, dR = oval_e(Hw, bpy.data.objects["SCULPT_EYE_R"])
e_min = np.minimum(eL, eR)
w = np.zeros(len(H0))
for e_, d_ in ((eL, dL), (eR, dR)):
    t = np.clip((e_ - 1.6)/0.8, 0, 1); w = np.maximum(w, np.where(d_[:, 1] < 0.02, 1 - t*t*(3 - 2*t), 0))
for m in moves["SCULPT_HEAD"]: m["composite_weight"] = round(float(w[m["id"]]), 4); m["oval_e"] = round(float(e_min[m["id"]]), 3)
json.dump(moves, open(os.path.join(out, "base_vertex_moves.json"), "w"), indent=0)
# ---- export: same options as stage4_export.py, only the four parts under SCULPT_HEAD_ROOT
glb = os.path.join(out, "simm_inlay_carrier.glb")
for o in bpy.context.view_layer.objects: o.select_set(False)
for n in ["SCULPT_HEAD_ROOT"] + PARTS:
    o = bpy.data.objects[n]; o.hide_set(False); o.select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects["SCULPT_HEAD_ROOT"]
bpy.ops.export_scene.gltf(filepath=glb, export_format='GLB', use_selection=True, export_apply=True, export_yup=True,
                          export_animations=False, export_skins=False, export_cameras=False, export_lights=False,
                          export_materials='EXPORT', export_image_format='AUTO', export_texcoords=True, export_normals=True,
                          export_morph=False, export_extras=False)
# ---- exported comparison against the held v012 GLB (raw accessors)
def load(p):
    d = open(p, "rb").read(); n = struct.unpack("<I", d[12:16])[0]; g = json.loads(d[20:20+n]); o = 20 + n
    return g, d[o+8:]
CT = {5126: np.float32, 5123: np.uint16, 5125: np.uint32}; NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3}
def acc(g, b, i):
    a = g["accessors"][i]; v = g["bufferViews"][a["bufferView"]]
    return np.frombuffer(b, dtype=CT[a["componentType"]], count=a["count"]*NC[a["type"]], offset=v.get("byteOffset", 0) + a.get("byteOffset", 0)).reshape(a["count"], -1)
def mesh(g, b, name):
    nd = [x for x in g["nodes"] if x.get("name") == name and "mesh" in x]; assert len(nd) == 1, name
    prims = g["meshes"][nd[0]["mesh"]]["primitives"]; outp = []
    for pr in prims:
        at = pr["attributes"]
        outp.append({"P": acc(g, b, at["POSITION"]).astype(float), "N": acc(g, b, at["NORMAL"]).astype(float), "UV": acc(g, b, at["TEXCOORD_0"]).astype(float),
                     "I": acc(g, b, pr["indices"]).ravel(), "mat": g["materials"][pr["material"]]["name"], "attrs": sorted(at)})
    return outp, nd[0]
G, Bn = load(glb); HG, HB = load(held_glb)
R["glb"] = {"file": "simm_inlay_carrier.glb", "sha256": sha(glb), "bytes": os.path.getsize(glb), "held_v012_glb_sha256": sha(held_glb),
            "nodes": [x.get("name") for x in G["nodes"]], "skins": len(G.get("skins", [])), "animations": len(G.get("animations", [])),
            "cameras": len(G.get("cameras", [])), "materials": [m["name"] for m in G["materials"]]}
assert sorted(n for n in R["glb"]["nodes"] if n) == sorted(["SCULPT_HEAD_ROOT"] + PARTS), R["glb"]["nodes"]
root_c = [x for x in G["nodes"] if x.get("name") == "SCULPT_HEAD_ROOT"][0]; root_h = [x for x in HG["nodes"] if x.get("name") == "SCULPT_HEAD_ROOT"][0]
R["glb"]["root_transform_identical_to_held"] = {k: root_c.get(k) for k in ("translation", "rotation", "scale")} == {k: root_h.get(k) for k in ("translation", "rotation", "scale")}
heat = None
for n in PARTS:
    C_, nc = mesh(G, Bn, n); H_, nh = mesh(HG, HB, n)
    assert len(C_) == len(H_) and nc.get("translation") == nh.get("translation") and nc.get("rotation") == nh.get("rotation") and nc.get("scale") == nh.get("scale"), n
    rec = {"primitives": len(C_), "materials": [p["mat"] for p in C_], "materials_held": [p["mat"] for p in H_], "attributes": C_[0]["attrs"]}
    for k, (c, hh) in enumerate(zip(C_, H_)):
        same_order = c["P"].shape == hh["P"].shape and np.array_equal(c["UV"], hh["UV"]) and np.array_equal(c["I"], hh["I"])
        rec["vertices"] = [len(c["P"]), len(hh["P"])]; rec["triangles"] = [len(c["I"])//3, len(hh["I"])//3]
        if same_order:
            dP = np.linalg.norm(c["P"] - hh["P"], axis=1); mv = dP > 1e-7
            rec.update({"correspondence": "index-wise: identical UV arrays and identical triangle index arrays",
                        "exported_vertices_moved": int(mv.sum()), "exported_moved_over_0.05mm": int((dP > 5e-5).sum()), "exported_max_move_mm": round(float(dP.max()*1000), 3),
                        "moved_bounds_min": (c["P"][mv].min(0).round(4).tolist() if mv.any() else None), "moved_bounds_max": (c["P"][mv].max(0).round(4).tolist() if mv.any() else None),
                        "normals_changed_vertices": int((np.abs(c["N"] - hh["N"]).max(1) > 1e-4).sum())})
            if n == "SCULPT_HEAD": heat = (hh["P"], dP)
        else:
            uvs_c = set(map(tuple, np.round(c["UV"], 6))); uvs_h = set(map(tuple, np.round(hh["UV"], 6)))
            tri_c = sorted(tuple(sorted(tuple(np.round(c["UV"][i], 6)) for i in c["I"][3*t:3*t+3])) for t in range(len(c["I"])//3))
            tri_h = sorted(tuple(sorted(tuple(np.round(hh["UV"][i], 6)) for i in hh["I"][3*t:3*t+3])) for t in range(len(hh["I"])//3))
            rec.update({"correspondence": "as sets (triangle order not stable between exports, documented since v010): UV set and triangles-as-UV-sets compared",
                        "uv_sets_identical": uvs_c == uvs_h, "triangles_as_uv_sets_identical": tri_c == tri_h})
            assert uvs_c == uvs_h and tri_c == tri_h, n + ": topology/UV differs"
    R["parts"][n].update(rec)
    print("PART", n, json.dumps(rec)[:400])
# ---- locality of the exported head (glTF is Y-up: x, y=up, z=forward toward the viewer)
P, dP = heat
pb = np.stack([P[:, 0], -P[:, 2], P[:, 1]], 1)                          # back to Blender axes (x, y, z-up)
eLx, _ = oval_e(pb, bpy.data.objects["SCULPT_EYE_L"]); eRx, _ = oval_e(pb, bpy.data.objects["SCULPT_EYE_R"]); ex = np.minimum(eLx, eRx)
mv = dP > 1e-7
nose = (np.abs(pb[:, 0]) < 0.022) & (pb[:, 2] > 1.10) & (pb[:, 2] < 1.165) & (pb[:, 1] < -0.09)
mouth = (np.abs(pb[:, 0]) < 0.045) & (pb[:, 2] > 1.04) & (pb[:, 2] < 1.10) & (pb[:, 1] < -0.07)
R["locality_exported_head"] = {"moved_vertices": int(mv.sum()), "max_oval_e_of_any_moved_vertex": round(float(ex[mv].max()), 3),
                               "moved_vertices_beyond_e_2.4_subdivision_halo": int((mv & (ex > 2.4)).sum()), "max_move_beyond_e_2.4_mm": round(float(dP[ex > 2.4].max()*1000), 4),
                               "unmoved_vertices_beyond_halo_e_gt_max": int((ex > ex[mv].max()).sum()),
                               "nose_vertices": int(nose.sum()), "nose_max_move_mm": round(float(dP[nose].max()*1000), 6),
                               "mouth_vertices": int(mouth.sum()), "mouth_max_move_mm": round(float(dP[mouth].max()*1000), 6),
                               "moved_bounds_blender_min": pb[mv].min(0).round(4).tolist(), "moved_bounds_blender_max": pb[mv].max(0).round(4).tolist()}
# nose and mouth are REPORTED, not asserted: the reviewed mask's fade (oval e 1.6 to 2.4) is periorbital and may reach them
for nm_, k_ in (("nose", nose), ("mouth", mouth)):
    mm_ = k_ & mv
    R["locality_exported_head"][nm_ + "_vertices_moved"] = int(mm_.sum())
    R["locality_exported_head"][nm_ + "_moved_over_0.05mm"] = int((k_ & (dP > 5e-5)).sum())
    if mm_.any(): R["locality_exported_head"][nm_ + "_moved_bounds_blender"] = [pb[mm_].min(0).round(4).tolist(), pb[mm_].max(0).round(4).tolist()]
np.save(os.path.join(out, "_heat.npy"), np.concatenate([pb, dP[:, None], ex[:, None]], 1))   # scratch for the heatmap; removed after
# ---- held materials and images: byte-identical embedded images
def images(g, b):
    o = {}
    for i in g.get("images", []):
        v = g["bufferViews"][i["bufferView"]]; o[i["name"]] = hashlib.sha256(b[v.get("byteOffset", 0):v.get("byteOffset", 0) + v["byteLength"]]).hexdigest()
    return o
ic, ih = images(G, Bn), images(HG, HB)
R["images"] = {k: {"sha256": v, "identical_to_held_v012_embedded": ih.get(k) == v} for k, v in ic.items()}
assert all(x["identical_to_held_v012_embedded"] for x in R["images"].values()), R["images"]
mc = {m["name"]: m for m in G["materials"]}; mh = {m["name"]: m for m in HG["materials"]}
def resolved(m, g):   # texture references resolved to image names (indices shift because the hair image is not in the carrier)
    def fix(o):
        if isinstance(o, dict):
            return {k: (g["images"][g["textures"][v]["source"]]["name"] if k == "index" else fix(v)) for k, v in o.items()}
        return [fix(x) for x in o] if isinstance(o, list) else o
    return json.dumps(fix(m), sort_keys=True)
R["materials_identical_to_held_v012"] = {k: resolved(mc[k], G) == resolved(mh[k], HG) for k in mc}
assert all(R["materials_identical_to_held_v012"].values()), R["materials_identical_to_held_v012"]
json.dump(R, open(os.path.join(out, "inlay_carrier_manifest.json"), "w"), indent=1)
print("CARRIER", R["glb"]["sha256"], json.dumps(R["locality_exported_head"]), json.dumps(R["materials_identical_to_held_v012"]))
