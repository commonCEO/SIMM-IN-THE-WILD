# Review only, never saved. Applies a supporting-palette JSON (simm_support_palette_p001.json) as candidate-only material
# copies, after jacket_review_prep.py and boot_review_prep.py and before render_views.py:
#   SUPPORT_PALETTE=<json> blender -b f.blend --python jacket_review_prep.py --python boot_review_prep.py \
#       --python support_palette_apply.py --python render_views.py -- <render args>
# Without SUPPORT_PALETTE it only runs the checks (the control). PALETTE_REPORT=<json> writes the shared-use report.
# Checks (a failure stops the run): every source material exists exactly once; on PROTECTED_BODY its faces are counted
# with bounds and dominant bones; any other object that uses it is listed with its own face count.
# Override: for each mesh shown in review (REVIEW_BODY, or PROTECTED_BODY when the body itself is shown) the slot holding
# the source material gets a copy whose MULTIPLY Color1 (the glTF baseColorFactor) is the proposed factor. The source
# material, the mesh and the file are not changed.
import bpy, os, json, collections, numpy as np
path = os.environ.get("SUPPORT_PALETTE", ""); report = os.environ.get("PALETTE_REPORT", "")
TARGETS = ["Simm charcoal olive trousers", "Simm olive canvas", "Simm woven olive straps", "Simm canvas seams"]
P = json.load(open(path)) if path else None
if P: TARGETS = [o["source_material"] for o in P["overrides"]]
body = bpy.data.objects["PROTECTED_BODY"]; me = body.data; gn = [g.name for g in body.vertex_groups]
co = np.array([v.co[:] for v in me.vertices]); R = {}
for t in TARGETS:
    hits = [m for m in bpy.data.materials if m.name == t]; assert len(hits) == 1, "material missing or duplicated: " + t
    users = {}
    for o in bpy.data.objects:
        if o.type != 'MESH' or o.name == "REVIEW_BODY": continue
        idx = [i for i, m in enumerate(o.data.materials) if m and m.name == t]
        if idx: users[o.name] = sum(1 for p in o.data.polygons if p.material_index in idx)
    idx = [i for i, m in enumerate(me.materials) if m and m.name == t]
    fs = [p for p in me.polygons if p.material_index in idx]; vs = sorted(set(k for p in fs for k in p.vertices)); c = co[vs]
    dom = collections.Counter(gn[max(me.vertices[k].groups, key=lambda g: g.weight).group] for k in vs if len(me.vertices[k].groups))
    R[t] = {"body_faces": len(fs), "rest_min": c.min(0).round(3).tolist(), "rest_max": c.max(0).round(3).tolist(),
            "dominant_bones": dict(dom.most_common()), "face_counts_by_object": users}
    print("PALETTE CHECK %-30s %s" % (t, R[t]))
if report: json.dump(R, open(report, "w"), indent=1)
if P:
    shown = [o for o in bpy.data.objects if o.type == 'MESH' and o.name in ("REVIEW_BODY", "PROTECTED_BODY") and not o.hide_render]
    for ov in P["overrides"]:
        src = bpy.data.materials[ov["source_material"]]; cp = src.copy(); cp.name = ov["candidate_copy"]
        mix = [n for n in cp.node_tree.nodes if n.type == 'MIX_RGB' and n.blend_type == 'MULTIPLY']; assert len(mix) == 1, cp.name
        mix[0].inputs["Color1"].default_value = list(ov["proposed_factor_linear"]) + [1.0]
        b = cp.node_tree.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = ov["roughness"]; b.inputs["Specular"].default_value = ov["specular_blender"]
        n = 0
        for o in shown:
            for i, m in enumerate(o.data.materials):
                if m == src: o.data.materials[i] = cp; n += 1
        print("PALETTE APPLY", cp.name, "slots", n, "on", [o.name for o in shown])
