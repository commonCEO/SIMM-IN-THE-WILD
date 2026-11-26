# Run after hair_material_apply.py in the same Blender session (review only, nothing saved):
#   HAIR_ALBEDO=<png> HAIR_ROUGH=<r> blender -b head_candidate_v011.blend --python hair_material_apply.py \
#       --python hair_material_probe.py -- <absolute probe.glb> <absolute out.json>
# Exports SCULPT_HAIR alone with the Blender 3.5.1 glTF exporter (the same options as stage4_export.py) and records
# exactly what the exporter wrote for SCULPT_MAT_HAIR: pbrMetallicRoughness, extensions (specular, IOR), the image
# size and checksum, and a checksum of the TEXCOORD_0 and POSITION data, so the UVs and geometry can be compared
# byte for byte with the v011 GLB. The probe GLB is a measuring device, not a delivery.
import bpy, sys, json, struct, hashlib
out_glb, out_json = sys.argv[sys.argv.index("--")+1:][:2]
for o in bpy.context.view_layer.objects: o.select_set(False)
h = bpy.data.objects["SCULPT_HAIR"]; h.hide_set(False); h.select_set(True); bpy.context.view_layer.objects.active = h
bpy.ops.export_scene.gltf(filepath=out_glb, export_format='GLB', use_selection=True, export_apply=True, export_yup=True,
                          export_animations=False, export_skins=False, export_cameras=False, export_lights=False,
                          export_materials='EXPORT', export_image_format='AUTO', export_texcoords=True, export_normals=True,
                          export_morph=False, export_extras=False)
def chunks(p):
    d = open(p, "rb").read(); n = struct.unpack("<I", d[12:16])[0]; g = json.loads(d[20:20+n]); b = d[20+n+8:]; return g, b
def view_bytes(g, b, acc):
    a = g["accessors"][acc]; v = g["bufferViews"][a["bufferView"]]; o = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    return b[o:o + v["byteLength"] - a.get("byteOffset", 0)]
def hair_info(p):
    g, b = chunks(p)
    mi = [i for i, m in enumerate(g["meshes"]) if m["name"] == "SCULPT_HAIR"][0]; prim = g["meshes"][mi]["primitives"][0]
    mat = g["materials"][prim["material"]]
    img = None
    bc = mat.get("pbrMetallicRoughness", {}).get("baseColorTexture")
    if bc is not None:
        im = g["images"][g["textures"][bc["index"]]["source"]]; v = g["bufferViews"][im["bufferView"]]
        data = b[v.get("byteOffset", 0):v.get("byteOffset", 0) + v["byteLength"]]
        img = {"name": im.get("name"), "mimeType": im.get("mimeType"), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
               "size": list(struct.unpack(">II", data[16:24])) if data[:8] == b"\x89PNG\r\n\x1a\n" else None}
    return {"material": mat, "image": img,
            "texcoord0_sha256": hashlib.sha256(view_bytes(g, b, prim["attributes"]["TEXCOORD_0"])).hexdigest(),
            "position_sha256": hashlib.sha256(view_bytes(g, b, prim["attributes"]["POSITION"])).hexdigest(),
            "vertex_count": g["accessors"][prim["attributes"]["POSITION"]]["count"], "extensionsUsed": g.get("extensionsUsed", [])}
json.dump(hair_info(out_glb), open(out_json, "w"), indent=1)
print("PROBE", out_json)
