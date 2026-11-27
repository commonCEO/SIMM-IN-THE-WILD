# ART-014 E1 eye-only packet (Codex brief at 975040e). Opens the held head v012 and writes, into an EMPTY new folder:
#   simm_eye_e1_albedo.png        512 x 512 8-bit RGB, sRGB-encoded
#   simm_eye_e1_carrier.glb       ONLY SCULPT_EYE_L and SCULPT_EYE_R (unchanged geometry/UVs) with the E1 SCULPT_MAT_EYE
#   eye_e1_manifest.json          identity checks against head_candidate_v012.glb, exported material fields, parameters
#   blender -b inbox/head_candidate_v012.blend --python eye_e1_build.py -- <absolute empty out dir> <absolute held v012 glb>
# Nothing is saved back to any .blend. Same painting formula as eye_e1_demo.py (the reviewed demo), with ONE correction:
# the colours are now ENCODED to sRGB before they are written. stage3_finish.py (v009 to v012) and the demo wrote linear
# values straight into the 8-bit sRGB image, so their eyes render darker than authored (sclera 236 -> stored 214, warm
# lower iris 92,56,32 -> about 27,10,4). The packet records both, with evidence.
import bpy, sys, os, json, struct, hashlib, numpy as np
out, held_glb = sys.argv[sys.argv.index("--")+1:][:2]
assert os.path.isabs(out) and (not os.path.exists(out) or not os.listdir(out)), "output dir must be absolute and empty"
os.makedirs(out, exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
def lin(r, g, b): c = np.array([r, g, b])/255.0; return np.where(c <= 0.04045, c/12.92, ((c + 0.055)/1.055)**2.4)
def enc(x): x = np.clip(x, 0, 1); return np.where(x <= 0.0031308, 12.92*x, 1.055*x**(1/2.4) - 0.055)
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3 - 2*x)
P = {"iris_half_sizes_m": [0.0182, 0.0272], "lid_opening_half_sizes_m": [0.0174, 0.0264], "pupil_half_sizes_m": [0.0082, 0.0136],
     "iris_top_srgb": [58, 34, 22], "iris_bottom_srgb": [122, 78, 46], "pupil_srgb": [30, 18, 12], "sclera_srgb": [214, 190, 168],
     "iris_outer_ring_darkening": 0.35, "catchlight": {"centre_m": [0.0045, 0.0105], "half_sizes_m": [0.0034, 0.0040], "srgb": [225, 215, 200], "opacity": 0.8},
     "second_catchlight": "removed", "emission": "none (no emissive texture, emissive factor 0)", "roughness": 0.55, "blender_specular": 0.25}
eyes = [bpy.data.objects["SCULPT_EYE_L"], bpy.data.objects["SCULPT_EYE_R"]]
co = np.array([v.co[:] for v in eyes[0].data.vertices]); EYE_R = float((co.max(0) - co.min(0))[0]/2)
N = 512; yy, xx = np.mgrid[0:N, 0:N]
px = ((xx + 0.5)/N - 0.5)*2*EYE_R; pz = ((yy + 0.5)/N - 0.5)*2*EYE_R
IA, IB = P["iris_half_sizes_m"]; PA, PB = P["pupil_half_sizes_m"]
r_i = np.sqrt((px/IA)**2 + (pz/IB)**2); r_p = np.sqrt((px/PA)**2 + ((pz + 0.0015)/PB)**2)
img = np.zeros((N, N, 3)); img[:] = lin(*P["sclera_srgb"])          # painted in LINEAR light, as the demo
low = sstep((-pz/IB + 0.10)/0.95)
iris = lin(*P["iris_top_srgb"])[None, None, :]*(1 - low[..., None]) + lin(*P["iris_bottom_srgb"])[None, None, :]*low[..., None]
iris = iris*(1 - P["iris_outer_ring_darkening"]*sstep((r_i - 0.80)/0.20)[..., None])
k = sstep((1.0 - r_i)/0.05)[..., None]; img = img*(1 - k) + iris*k
k = sstep((1.0 - r_p)/0.20)[..., None]; img = img*(1 - k) + lin(*P["pupil_srgb"])[None, None, :]*k
c = P["catchlight"]; glint = c["opacity"]*sstep((1.0 - np.sqrt(((px - c["centre_m"][0])/c["half_sizes_m"][0])**2 + ((pz - c["centre_m"][1])/c["half_sizes_m"][1])**2))/0.30)
img = img*(1 - glint[..., None]) + lin(*c["srgb"])[None, None, :]*glint[..., None]
png = os.path.join(out, "simm_eye_e1_albedo.png")
im = bpy.data.images.new("simm_eye_e1_albedo", N, N, alpha=False)                 # 8-bit; pixels are stored as given,
im.pixels.foreach_set(np.concatenate([enc(img), np.ones((N, N, 1))], 2).astype(np.float32).ravel())   # so ENCODE first
im.filepath_raw = png; im.file_format = 'PNG'; im.save(); bpy.data.images.remove(im)
tex = bpy.data.images.load(png); tex.colorspace_settings.name = 'sRGB'
# E1 material: the held SCULPT_MAT_EYE with the base colour swapped, emission removed, roughness and specular set
m = bpy.data.materials["SCULPT_MAT_EYE"]; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
for l in list(nt.links):
    if l.to_socket == b.inputs["Base Color"]: l.from_node.image = tex
for l in list(nt.links):
    if l.to_socket == b.inputs["Emission"]:
        src = l.from_node; nt.links.remove(l)
        if src.type == 'TEX_IMAGE' and not any(src.outputs[0].links): nt.nodes.remove(src)
b.inputs["Emission"].default_value = (0, 0, 0, 1); b.inputs["Emission Strength"].default_value = 0.0
b.inputs["Roughness"].default_value = P["roughness"]; b.inputs["Specular"].default_value = P["blender_specular"]
glb = os.path.join(out, "simm_eye_e1_carrier.glb")
for o in bpy.context.view_layer.objects: o.select_set(False)
for o in eyes: o.hide_set(False); o.select_set(True)
bpy.context.view_layer.objects.active = eyes[0]
bpy.ops.export_scene.gltf(filepath=glb, export_format='GLB', use_selection=True, export_apply=True, export_yup=True,
                          export_animations=False, export_skins=False, export_cameras=False, export_lights=False,
                          export_materials='EXPORT', export_image_format='AUTO', export_texcoords=True, export_normals=True,
                          export_morph=False, export_extras=False)
# ---- checks: re-import both GLBs; the carrier's eye meshes must equal the held v012 eye meshes
def load_glb(p):
    d = open(p, "rb").read(); n = struct.unpack("<I", d[12:16])[0]; g = json.loads(d[20:20+n]); o = 20 + n
    return g, d[o+8:]
def imp(p):
    before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=p)
    return {o.name.split(".")[0]: o for o in bpy.data.objects if o not in before and o.type == 'MESH'}
def recs(o):
    me = o.data; uv = me.uv_layers.active; W = np.array(o.matrix_world)
    P_ = np.array([v.co[:] for v in me.vertices]) @ W[:3, :3].T + W[:3, 3]
    corners = set(tuple(np.round(P_[l.vertex_index], 6)) + tuple(np.round(list(uv.data[l.index].uv), 6)) for l in me.loops)
    tris = sorted(tuple(sorted(tuple(np.round(P_[i], 6)) for i in p.vertices)) for p in me.polygons)
    return {"vertices": len(me.vertices), "triangles": len(me.polygons), "uv_layers": len(me.uv_layers), "corners": corners, "tris": tris,
            "bounds_min": P_.min(0).round(5).tolist(), "bounds_max": P_.max(0).round(5).tolist()}
C = imp(glb); H = imp(held_glb)
assert sorted(C) == ["SCULPT_EYE_L", "SCULPT_EYE_R"], sorted(C)
R = {"packet": "ART-014 E1 eye-only (Codex brief 975040e)", "files": {}, "identity_vs_held_v012": {}, "parameters": P}
for n in ("SCULPT_EYE_L", "SCULPT_EYE_R"):
    a, h = recs(C[n]), recs(H[n])
    same = a["corners"] == h["corners"] and a["tris"] == h["tris"] and a["vertices"] == h["vertices"] and a["triangles"] == h["triangles"]
    R["identity_vs_held_v012"][n] = {"vertices": [a["vertices"], h["vertices"]], "triangles": [a["triangles"], h["triangles"]], "uv_layers": [a["uv_layers"], h["uv_layers"]],
        "position_uv_corner_records_identical": a["corners"] == h["corners"], "triangles_identical_as_sets": a["tris"] == h["tris"],
        "bounds_min": a["bounds_min"], "bounds_max": a["bounds_max"]}
    print("IDENTITY", n, R["identity_vs_held_v012"][n])
    assert same, n + ": carrier eye differs from held v012"
g, bin_ = load_glb(glb)
R["exported_gltf"] = {"materials": g["materials"], "textures": g.get("textures"), "samplers": g.get("samplers"),
                      "images": [{"name": i.get("name"), "mimeType": i.get("mimeType")} for i in g.get("images", [])],
                      "meshes": [mm["name"] for mm in g["meshes"]], "nodes": [nd.get("name") for nd in g["nodes"]],
                      "skins": len(g.get("skins", [])), "animations": len(g.get("animations", [])), "cameras": len(g.get("cameras", [])),
                      "extensionsUsed": g.get("extensionsUsed", [])}
assert not any("emissiveTexture" in mm or any(mm.get("emissiveFactor", [0, 0, 0])) for mm in g["materials"]), "emission still exported"
for i in g.get("images", []):
    v = g["bufferViews"][i["bufferView"]]; data = bin_[v.get("byteOffset", 0):v.get("byteOffset", 0) + v["byteLength"]]
    R["exported_gltf"]["images"][[x["name"] for x in R["exported_gltf"]["images"]].index(i.get("name"))]["sha256"] = hashlib.sha256(data).hexdigest()
from_png = np.asarray(bpy.data.images.load(png).pixels[:]).reshape(N, N, 4)[::-1, :, :3]   # top row first, as in the PNG
def at(x, z):   # sample the PNG at eye-plane coordinates (m)
    i = int((z/(2*EYE_R) + 0.5)*N); j = int((x/(2*EYE_R) + 0.5)*N); return [int(round(v*255)) for v in from_png[N - 1 - i, j]]
R["sample_colours_srgb"] = {"iris_upper (0, +0.020)": at(0.0, 0.020), "iris_lower (0, -0.022)": at(0.0, -0.022), "pupil (0, -0.0015)": at(0.0, -0.0015),
                            "catchlight centre": at(0.0045, 0.0105), "sclera corner (0.034, 0.034)": at(0.034, 0.034)}
R["files"] = {"simm_eye_e1_albedo.png": {"sha256": sha(png), "size": [N, N], "encoding": "8-bit RGB PNG, sRGB-encoded"},
              "simm_eye_e1_carrier.glb": {"sha256": sha(glb), "bytes": os.path.getsize(glb)}, "held_v012_glb_sha256": sha(held_glb)}
R["eye_radius_m"] = round(EYE_R, 5)
json.dump(R, open(os.path.join(out, "eye_e1_manifest.json"), "w"), indent=1, default=list)
print("E1 PACKET", json.dumps(R["files"]), json.dumps(R["sample_colours_srgb"]))
