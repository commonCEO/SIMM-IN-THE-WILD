# ART-004 jacket material m002 (Codex brief at 68e1524): material-only packet on the held f002 geometry.
#   blender -b work/jacket_finish_f002.blend --python build_scripts/jacket_material_m002.py -- <out.blend> <texture dir>
# Geometry, normals, weights, modifiers and every other object are left as they are (asserted). What changes, on the three
# jacket parts only: the f002 UV layers (UVMap, SurfaceUV: overlapping, outside 0..1, never used by a texture) are replaced
# by one shared unwrap M002_UV; the flat materials are replaced by two textured ones that share one 1024 albedo (sRGB) and
# one 1024 roughness map (linear). The maps are baked as emission from per-vertex values, so no lighting, occlusion or
# curvature enters them. Colour plan (all low frequency, documented in the notes):
#   front panels = the f002 jacket colour; sleeves lighter and slightly more lemon; back panel and the lower band deeper
#   ochre; a 3D value noise at about 9 and 4.5 cm for slight dye variation; trim a restrained darker ochre.
import bpy, sys, os, json, math, hashlib, numpy as np
sys.dont_write_bytecode = True
out_blend, texdir = sys.argv[sys.argv.index("--")+1:][:2]
os.makedirs(texdir, exist_ok=True)
SIZE = 1024
PARTS = ("SCULPT_JACKET_LONG", "SCULPT_JACKET_LONG_TRIM", "SCULPT_JACKET_POCKETS")
# linear base colours and panel multipliers
BASE = np.array((0.723, 0.381, 0.027))          # f002 SCULPT_MAT_JACKET, unchanged as the front-panel colour
SLEEVE = np.array((1.06, 1.13, 1.10))           # lighter, a touch more lemon
BACK = np.array((0.88, 0.84, 0.80))             # deeper ochre
HEM = np.array((0.90, 0.86, 0.82))              # lower band, fading in below z 0.60
TRIM = np.array((0.400, 0.190, 0.022))          # f002 trim was (0.468, 0.220, 0.019)
A_VAL, A_HUE = 0.06, 0.05                       # noise amplitudes (linear multipliers)
R_SHELL, R_SHELL_VAR, R_TRIM = 0.88, 0.025, 0.80
sc = bpy.context.scene
for n in PARTS:
    assert [o.name for o in bpy.data.objects if o.name == n or o.name.startswith(n + ".")] == [n], "missing or duplicate part " + n
objs = [bpy.data.objects[n] for n in PARTS]
rig = bpy.data.objects["SimmRig"]

def snapshot():
    s = {}
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        me = o.data; me.calc_normals_split()
        s[o.name] = (np.array([v.co[:] for v in me.vertices]), np.array([l.normal[:] for l in me.loops]),
                     [sorted((g.group, g.weight) for g in v.groups) for v in me.vertices], [tuple(p.vertices) for p in me.polygons],
                     [(m.type, m.name) for m in o.modifiers], np.array(o.matrix_world))
    return s
def same(a, b):   # positions, weights, faces, modifiers and transforms exact; split normals within 1e-5 (edit-mode float noise)
    return (a[0].shape == b[0].shape and np.array_equal(a[0], b[0]) and a[1].shape == b[1].shape and np.abs(a[1] - b[1]).max() < 1e-5
            and a[2] == b[2] and a[3] == b[3] and a[4] == b[4] and np.array_equal(a[5], b[5]))
before = snapshot()

# ---- one shared unwrap for the three parts
for o in objs:
    me = o.data
    while len(me.uv_layers): me.uv_layers.remove(me.uv_layers[0])
    me.uv_layers.new(name="M002_UV")
for o in bpy.data.objects: o.select_set(False)
for o in objs: o.hide_set(False); o.select_set(True)
bpy.context.view_layer.objects.active = objs[0]
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.006, area_weight=0.0, correct_aspect=True, scale_to_bounds=False)
bpy.ops.object.mode_set(mode='OBJECT')

# ---- per-vertex albedo and roughness (rest positions, world space)
rng = np.random.default_rng(20261127); LAT = rng.random((4, 32, 32, 32)) * 2 - 1
def vnoise(p, scale, ch):
    q = p / scale + 64.0; i = np.floor(q).astype(int); f = q - i; f = f*f*(3 - 2*f); acc = 0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (f[:, 0] if dx else 1 - f[:, 0]) * (f[:, 1] if dy else 1 - f[:, 1]) * (f[:, 2] if dz else 1 - f[:, 2])
                acc = acc + w * LAT[ch, (i[:, 0]+dx) % 32, (i[:, 1]+dy) % 32, (i[:, 2]+dz) % 32]
    return acc
def fbm(p, ch): return (vnoise(p, 0.09, ch) + 0.5*vnoise(p, 0.045, ch)) / 1.5
def sstep(a, b, x): t = np.clip((x - a)/(b - a), 0, 1); return t*t*(3 - 2*t)
def world(o): M = np.array(o.matrix_world); co = np.array([v.co[:] for v in o.data.vertices]); return co @ M[:3, :3].T + M[:3, 3]
def armw(o):
    gn = [g.name for g in o.vertex_groups]; arm = {"upper_arm_l", "forearm_l", "hand_l", "upper_arm_r", "forearm_r", "hand_r"}
    return np.array([sum(g.weight for g in v.groups if gn[g.group] in arm) for v in o.data.vertices])
shell = bpy.data.objects["SCULPT_JACKET_LONG"]; P0 = world(shell); a0 = armw(shell)
torso = P0[a0 < 0.3]; zb = np.arange(torso[:, 2].min(), torso[:, 2].max() + 0.02, 0.02)
yc = np.array([torso[np.abs(torso[:, 2] - z) < 0.02, 1].mean() if (np.abs(torso[:, 2] - z) < 0.02).any() else np.nan for z in zb])
ok = ~np.isnan(yc); zb, yc = zb[ok], yc[ok]
REC = {}
def shell_values(P, aw):
    fs = sstep(0.35, 0.75, aw)
    fb = sstep(-0.015, 0.035, P[:, 1] - np.interp(P[:, 2], zb, yc)) * (1 - fs)
    fh = (1 - sstep(0.53, 0.60, P[:, 2])) * (1 - fs)
    n1, n2, n3 = fbm(P, 0), fbm(P, 1), fbm(P, 2)
    col = BASE[None] * (1 + (SLEEVE - 1)[None]*fs[:, None]) * (1 + (BACK - 1)[None]*fb[:, None]) * (1 + (HEM - 1)[None]*fh[:, None])
    col = col * (1 + A_VAL*n1)[:, None]; col[:, 1] *= (1 + A_HUE*n2)
    return col, R_SHELL + R_SHELL_VAR*n3, dict(sleeve=fs, back=fb, hem=fh)
for o in objs:
    P = world(o)
    if o.name == "SCULPT_JACKET_LONG_TRIM":
        col = TRIM[None] * (1 + 0.5*A_VAL*fbm(P, 0))[:, None]; rgh = np.full(len(P), R_TRIM)
    else:
        col, rgh, F = shell_values(P, armw(o))
    col = np.clip(col, 0, 1); rgh = np.clip(rgh, 0, 1)
    REC[o.name] = {"albedo_linear_min": col.min(0).round(4).tolist(), "albedo_linear_max": col.max(0).round(4).tolist(),
                   "albedo_linear_mean": col.mean(0).round(4).tolist(), "roughness_min": round(float(rgh.min()), 4), "roughness_max": round(float(rgh.max()), 4)}
    for nm, val in (("M002_ALB", col), ("M002_RGH", np.repeat(rgh[:, None], 3, 1))):
        at = o.data.color_attributes.new(nm, 'FLOAT_COLOR', 'POINT')
        at.data.foreach_set("color", np.concatenate([val, np.ones((len(val), 1))], 1).ravel().astype(np.float32))

# ---- bake the per-vertex values into the shared maps (emission: no lighting)
# Each part is baked on its own: Blender paints one object's bake margin over other objects' islands when several bake
# into one image (that put trim-coloured flecks inside shell islands). Per part and map: a bake with a 16 px margin and a
# bake without margin, both onto a magenta sentinel. Composite: background fill, then each part's margin pixels, then every
# part's own island pixels on top, so no island is ever overwritten by another part's margin.
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 4; sc.cycles.use_denoising = False; sc.cycles.seed = 0
sc.render.bake.margin_type = 'EXTEND'; sc.render.bake.use_clear = False
rig.data.pose_position = 'REST'
SENT = np.array((1.0, 0.0, 1.0, 1.0), dtype=np.float32)
tmp = bpy.data.images.new("m002_tmp", SIZE, SIZE, alpha=False, float_buffer=False)
bake_mats = []
for o in objs:
    m = bpy.data.materials.new("M002_BAKE_" + o.name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    at = nt.nodes.new("ShaderNodeAttribute"); em = nt.nodes.new("ShaderNodeEmission"); ou = nt.nodes.new("ShaderNodeOutputMaterial")
    tx = nt.nodes.new("ShaderNodeTexImage"); tx.image = tmp; nt.links.new(at.outputs["Color"], em.inputs["Color"]); nt.links.new(em.outputs[0], ou.inputs["Surface"])
    nt.nodes.active = tx; bake_mats.append((o, m, at, tx))
orig = {o.name: [s.material for s in o.material_slots] for o in objs}
for o, m, at, tx in bake_mats:
    for s in o.material_slots: s.material = m
def bake_one(o, margin):
    tmp.pixels.foreach_set(np.tile(SENT, SIZE*SIZE))
    for x in bpy.data.objects: x.select_set(False)
    o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.bake(type='EMIT', margin=margin, use_clear=False)
    px = np.empty(SIZE*SIZE*4, dtype=np.float32); tmp.pixels.foreach_get(px); px = px.reshape(-1, 4)
    return px, ~np.all(np.abs(px - SENT) < 1e-6, axis=1)
OVERLAP = {}
for key, attr, cs in (("albedo", "M002_ALB", 'sRGB'), ("roughness", "M002_RGH", 'Non-Color')):
    tmp.colorspace_settings.name = cs
    for o, m, at, tx in bake_mats: at.attribute_name = attr
    # background outside the islands: the front-panel colour (sRGB-encoded) and the shell roughness, not black, so the
    # far mip levels used at game scale do not darken island edges
    fill = [(1.055*c**(1/2.4) - 0.055) if c > 0.0031308 else 12.92*c for c in BASE] if key == "albedo" else [R_SHELL]*3
    out_px = np.tile(np.array(fill + [1.0], dtype=np.float32), (SIZE*SIZE, 1))
    isl = []
    for o in objs:
        pm, cm = bake_one(o, 16); pi, ci = bake_one(o, 0)
        out_px[cm] = pm[cm]; isl.append((pi, ci))
    cover = np.zeros(SIZE*SIZE, dtype=int)
    for pi, ci in isl: out_px[ci] = pi[ci]; cover += ci
    OVERLAP[key] = int((cover > 1).sum())
    im = bpy.data.images.new("jacket_m002_" + key, SIZE, SIZE, alpha=False, float_buffer=False); im.colorspace_settings.name = cs
    im.pixels.foreach_set(out_px.ravel())
    path = os.path.join(texdir, "jacket_m002_%s.png" % key); im.filepath_raw = path; im.file_format = 'PNG'; im.save(); bpy.data.images.remove(im)
bpy.data.images.remove(tmp)
print("ISLAND PIXELS COVERED BY MORE THAN ONE PART", OVERLAP)
rig.data.pose_position = 'POSE'
for o, m, at, tx in bake_mats: bpy.data.materials.remove(m)
for o in objs:
    for nm in ("M002_ALB", "M002_RGH"): o.data.color_attributes.remove(o.data.color_attributes[nm])

# ---- final materials: f002 values except base colour and roughness, which now come from the maps
def textured(name, src):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    sb = src.node_tree.nodes["Principled BSDF"]
    for k in ("Metallic", "Specular", "Specular Tint", "Sheen", "Clearcoat", "IOR"):
        b.inputs[k].default_value = sb.inputs[k].default_value
    uv = nt.nodes.new("ShaderNodeUVMap"); uv.uv_map = "M002_UV"
    ta = nt.nodes.new("ShaderNodeTexImage"); ta.image = bpy.data.images.load(os.path.join(texdir, "jacket_m002_albedo.png")); ta.image.colorspace_settings.name = 'sRGB'
    tr = nt.nodes.new("ShaderNodeTexImage"); tr.image = bpy.data.images.load(os.path.join(texdir, "jacket_m002_roughness.png")); tr.image.colorspace_settings.name = 'Non-Color'
    sp = nt.nodes.new("ShaderNodeSeparateRGB")
    for t in (ta, tr): nt.links.new(uv.outputs["UV"], t.inputs["Vector"])
    nt.links.new(ta.outputs["Color"], b.inputs["Base Color"]); nt.links.new(tr.outputs["Color"], sp.inputs[0]); nt.links.new(sp.outputs["G"], b.inputs["Roughness"])
    return m
mj = textured("SCULPT_MAT_JACKET_M002", bpy.data.materials["SCULPT_MAT_JACKET"])
mt = textured("SCULPT_MAT_JACKET_TRIM_M002", bpy.data.materials["SCULPT_MAT_JACKET_TRIM"])
for o in objs:
    for s in o.material_slots: s.material = mt if orig[o.name][0].name == "SCULPT_MAT_JACKET_TRIM" else mj

after = snapshot()
changed = [k for k in before if k not in after or not same(before[k], after[k])]
assert not changed and set(before) == set(after), "geometry, normals, weights or modifiers changed: %s" % changed
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
uvs = {}
for o in objs:
    uv = np.array([d.uv[:] for d in o.data.uv_layers["M002_UV"].data])
    assert uv.min() >= 0 and uv.max() <= 1, o.name + ": UV outside 0..1"
    uvs[o.name] = {"uv_layers": [u.name for u in o.data.uv_layers], "uv_min": uv.min(0).round(4).tolist(), "uv_max": uv.max(0).round(4).tolist()}
R = {"textures": {k: {"file": "jacket_m002_%s.png" % k, "sha256": sha(os.path.join(texdir, "jacket_m002_%s.png" % k)), "size": SIZE,
                      "colour_space": "sRGB" if k == "albedo" else "linear (Non-Color); value in R, G and B"} for k in ("albedo", "roughness")},
     "per_part_values": REC, "island_pixels_shared_by_two_parts": OVERLAP, "uv": uvs, "mesh_snapshot_unchanged": True,
     "materials": {"SCULPT_MAT_JACKET_M002": ["SCULPT_JACKET_LONG", "SCULPT_JACKET_POCKETS"], "SCULPT_MAT_JACKET_TRIM_M002": ["SCULPT_JACKET_LONG_TRIM"]},
     "parameters": {"base_linear": BASE.tolist(), "sleeve_mult": SLEEVE.tolist(), "back_mult": BACK.tolist(), "hem_mult": HEM.tolist(), "trim_linear": TRIM.tolist(),
                    "noise_value_amp": A_VAL, "noise_green_amp": A_HUE, "noise_scales_m": [0.09, 0.045], "noise_seed": 20261127,
                    "roughness_shell": R_SHELL, "roughness_shell_var": R_SHELL_VAR, "roughness_trim": R_TRIM,
                    "specular_metallic_ior": "copied from the f002 materials, unchanged"}}
json.dump(R, open(os.path.join(texdir, "m002_build_record.json"), "w"), indent=1)
bpy.ops.wm.save_as_mainfile(filepath=out_blend, compress=True)
print("M002 DONE", json.dumps(R["textures"]))
