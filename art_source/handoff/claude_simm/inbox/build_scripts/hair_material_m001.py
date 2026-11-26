# ART-001 hair MATERIAL test m001 on frozen head v011 (Codex brief at 4f9ac05). Nothing is saved back to any .blend.
# blender -b head_candidate_v011.blend --python hair_material_m001.py -- <absolute out albedo.png> <absolute out uv_proof.json>
# Bakes ONE new chestnut albedo for SCULPT_HAIR through the hair's EXISTING UV map at the same 1024 px size as v011's
# hair texture. Geometry, normals, UVs, transforms and every other texture are read only.
# Colour design (albedo only, no lighting baked in):
#   - root and body masses: deeper warm brown, by depth of the hair surface above the scalp;
#   - outer surfaces of the locks: restrained amber, a little more where a lock faces upward and forward (a broad,
#     smoothed term over whole locks, so it does not draw a camera-dependent highlight);
#   - one broad, soft value/hue drift across the head (a few low-frequency waves, wavelength 9 to 15 cm);
#   - no grooves, no comb lines, no noise finer than the locks.
import bpy, sys, os, math, json, hashlib, numpy as np
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode = True
out_png, out_json = sys.argv[sys.argv.index("--")+1:][:2]
def srgb(r, g, b): return np.array([((c/255)/12.92 if c/255 <= 0.04045 else ((c/255 + 0.055)/1.055)**2.4) for c in (r, g, b)])
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
ROOT, BODY, AMBER = srgb(72, 39, 24), srgb(104, 58, 34), srgb(146, 90, 50)

hair = bpy.data.objects["SCULPT_HAIR"]; head = bpy.data.objects["SCULPT_HEAD"]; me = hair.data
assert len(me.uv_layers) == 1, "expected the hair's single UV map"
uv = np.empty(len(me.loops)*2); me.uv_layers[0].data.foreach_get("uv", uv)
uv_sha = hashlib.sha256(uv.astype(np.float32).tobytes()).hexdigest()
co = np.empty(len(me.vertices)*3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
nrm = np.empty(len(me.vertices)*3); me.vertices.foreach_get("normal", nrm); nrm = nrm.reshape(-1, 3)
geo_sha = hashlib.sha256(co.astype(np.float32).tobytes()).hexdigest()
hm = head.data; hc = np.empty(len(hm.vertices)*3); hm.vertices.foreach_get("co", hc); hc = hc.reshape(-1, 3)
tree = BVHTree.FromPolygons([tuple(p) for p in hc], [tuple(p.vertices) for p in hm.polygons])
lift = np.array([tree.find_nearest(p)[3] or 0.0 for p in co])
ed = np.empty(len(me.edges)*2, dtype=np.int32); me.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
deg = np.bincount(ed.ravel(), minlength=len(co)).astype(float)
def smooth(v, it):
    v = v.copy()
    for _ in range(it):
        acc = np.zeros_like(v); np.add.at(acc, ed[:, 0], v[ed[:, 1]]); np.add.at(acc, ed[:, 1], v[ed[:, 0]])
        v = 0.5*v + 0.5*acc/np.maximum(deg, 1)[:, None] if v.ndim > 1 else 0.5*v + 0.5*acc/np.maximum(deg, 1)
    return v
lift = smooth(lift, 25)
L = np.array([-0.30, -0.55, 0.78]); L /= np.linalg.norm(L)                         # up and toward the front
face_up = smooth(np.clip(nrm @ L, 0, 1), 40)                                       # broad, per lock, not per facet
t_body = sstep(lift/0.035)[:, None]; t_out = sstep((lift - 0.022)/0.05)[:, None]
col = ROOT*(1 - t_body) + BODY*t_body
amber_w = 0.50*t_out*(0.35 + 0.65*face_up[:, None])
col = col*(1 - amber_w) + AMBER*amber_w
rs = np.random.RandomState(11); drift = np.zeros(len(co)); hue = np.zeros(len(co))
for _ in range(4):
    k = rs.normal(size=3); k /= np.linalg.norm(k); wl = rs.uniform(0.09, 0.15); ph = rs.uniform(0, 2*math.pi)
    drift += np.sin(co @ k*2*math.pi/wl + ph)/4
    k2 = rs.normal(size=3); k2 /= np.linalg.norm(k2); hue += np.sin(co @ k2*2*math.pi/rs.uniform(0.10, 0.16) + rs.uniform(0, 6.28))/4
col = col*(1 + 0.07*drift[:, None])                                                # +-7 percent value, broad
col = col*(1 + 0.04*hue[:, None]*np.array([1.0, 0.0, -1.0]))                       # +-4 percent toward red or toward yellow
col = np.clip(col, 0, 1)

# bake per-vertex colour through the existing UV map (same method and size as stage 3's hair bake)
att = me.color_attributes.new("bakecol_m001", 'FLOAT_COLOR', 'POINT')
att.data.foreach_set("color", np.concatenate([col, np.ones((len(col), 1))], 1).ravel())
img = bpy.data.images.new("simm_head_hair_basecolor_m001", 1024, 1024, alpha=False)
m = bpy.data.materials.new("bake_tmp_m001"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
a = nt.nodes.new("ShaderNodeVertexColor"); a.layer_name = "bakecol_m001"
e = nt.nodes.new("ShaderNodeEmission"); o = nt.nodes.new("ShaderNodeOutputMaterial"); t = nt.nodes.new("ShaderNodeTexImage"); t.image = img
nt.links.new(a.outputs[0], e.inputs[0]); nt.links.new(e.outputs[0], o.inputs[0]); nt.nodes.active = t
old_mats = list(me.materials); me.materials.clear(); me.materials.append(m)
for x in bpy.context.view_layer.objects: x.select_set(x is hair)
bpy.context.view_layer.objects.active = hair; hair.hide_render = False
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 4
sc.render.bake.margin = 10; sc.render.bake.use_clear = True
bpy.ops.object.bake(type='EMIT')
img.filepath_raw = out_png; img.file_format = 'PNG'; img.save()
uv2 = np.empty(len(me.loops)*2); me.uv_layers[0].data.foreach_get("uv", uv2)
assert np.array_equal(uv, uv2), "UVs changed during the bake"
srgb_med = lambda c: [int(round(255*((x*12.92) if x <= 0.0031308 else (1.055*x**(1/2.4) - 0.055)))) for x in np.median(c, 0)]
json.dump({"hair_vertices": len(co), "uv_loops": len(me.loops), "uv_sha256_float32": uv_sha, "uv_unchanged_after_bake": True,
           "hair_positions_sha256_float32": geo_sha, "image_size": [1024, 1024], "bake_margin_px": 10,
           "palette_srgb": {"root": [72, 39, 24], "body": [104, 58, 34], "amber": [146, 90, 50]},
           "vertex_albedo_median_srgb": srgb_med(col)}, open(out_json, "w"), indent=1)
print("BAKED", out_png, "uv sha", uv_sha[:16], "median srgb", srgb_med(col))
