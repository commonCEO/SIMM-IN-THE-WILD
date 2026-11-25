# Stage 3: brows, materials, base-colour textures, naming. work/stage2.blend -> inbox/head_candidate_vNNN.blend
import bpy, bmesh, sys, os, math, numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, hairkit; importlib.reload(hairkit)
from hairkit import *
from mathutils import Vector
argv = sys.argv[sys.argv.index("--")+1:]
out = argv[0]; texdir = argv[1]
coll = bpy.data.collections["10_SCULPT_NEW_HEAD"]
face = bpy.data.objects["SCULPT_BASE_FACE"]; hair = bpy.data.objects["SCULPT_HAIR"]
eyeL = bpy.data.objects["SCULPT_BASE_EYE_L"]; eyeR = bpy.data.objects["SCULPT_BASE_EYE_R"]
EYE_R = 0.036; OVAL_A = 0.0174; OVAL_B = 0.0264; OVAL_N = 2.2
def srgb(r, g, b):
    c = np.array([r, g, b], float)/255.0
    return np.where(c <= 0.04045, c/12.92, ((c + 0.055)/1.055)**2.4)
def activate(o):
    bpy.context.view_layer.objects.active = o
    for x in bpy.context.view_layer.objects: x.select_set(x is o)
def co_of(me):
    a = np.empty(len(me.vertices)*3); me.vertices.foreach_get('co', a); return a.reshape(-1, 3)
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
def bake_vertex_colour(obj, colours, path, size, margin=8):
    """write per-vertex linear colours into an image through the object's active UV map (emission bake)"""
    me = obj.data
    att = me.color_attributes.get("bakecol") or me.color_attributes.new("bakecol", 'FLOAT_COLOR', 'POINT')
    att.data.foreach_set('color', np.concatenate([colours, np.ones((len(colours), 1))], 1).ravel())
    img = bpy.data.images.new(os.path.basename(path)[:-4], size, size, alpha=False)
    m = bpy.data.materials.new("bake_tmp"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    a = nt.nodes.new("ShaderNodeVertexColor"); a.layer_name = "bakecol"
    e = nt.nodes.new("ShaderNodeEmission"); o = nt.nodes.new("ShaderNodeOutputMaterial")
    t = nt.nodes.new("ShaderNodeTexImage"); t.image = img
    nt.links.new(a.outputs[0], e.inputs[0]); nt.links.new(e.outputs[0], o.inputs[0]); nt.nodes.active = t
    me.materials.clear(); me.materials.append(m)
    activate(obj)
    sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 4
    sc.render.bake.margin = margin; sc.render.bake.use_clear = True
    hid = obj.hide_render; obj.hide_render = False
    bpy.ops.object.bake(type='EMIT')
    obj.hide_render = hid
    img.filepath_raw = path; img.file_format = 'PNG'; img.save()
    img.pack(); me.materials.clear(); bpy.data.materials.remove(m)
    me.color_attributes.remove(me.color_attributes["bakecol"])
    return img
def pbr(name, img=None, colour=None, rough=0.5, spec=0.5):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    b = nt.nodes.new("ShaderNodeBsdfPrincipled"); o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(b.outputs[0], o.inputs[0])
    b.inputs["Roughness"].default_value = rough; b.inputs["Specular"].default_value = spec; b.inputs["Metallic"].default_value = 0
    if img is not None:
        t = nt.nodes.new("ShaderNodeTexImage"); t.image = img; nt.links.new(t.outputs[0], b.inputs["Base Color"])
    else:
        b.inputs["Base Color"].default_value = (*colour, 1)
    return m

# ---------------- eyes: UV = straight-on projection, dark upright iris painted for that projection
eye_c = {}
for eo, sgn in ((eyeL, 1), (eyeR, -1)):
    co = co_of(eo.data); C = 0.5*(co.max(0) + co.min(0)); eye_c[sgn] = C
    # the base eye's cornea-bulge loops shade as a ring once spherical: rebuild the surface as a clean sphere
    eb = bmesh.new(); bmesh.ops.create_uvsphere(eb, u_segments=40, v_segments=24, radius=EYE_R)
    for v in eb.verts: v.co = v.co + Vector(C)
    eb.loops.layers.uv.verify()
    for f in eb.faces: f.smooth = True
    eb.to_mesh(eo.data); eb.free(); eo.data.update()
    co = co_of(eo.data)
    uvl = eo.data.uv_layers.active.data
    for lp in eo.data.loops:
        p = co[lp.vertex_index]
        uvl[lp.index].uv = (0.5 + (p[0]-C[0])*sgn/(2*EYE_R), 0.5 + (p[2]-C[2])/(2*EYE_R))
N = 512; yy, xx = np.mgrid[0:N, 0:N]
px = ((xx + 0.5)/N - 0.5)*2*EYE_R; pz = ((yy + 0.5)/N - 0.5)*2*EYE_R
IA, IB, ICZ = 0.0260, 0.0340, 0.0000          # v002: iris fills the opening, the eye reads as one dark oval           # iris taller than the lid opening: lids always rest on it
r_i = np.sqrt((px/IA)**2 + ((pz-ICZ)/IB)**2)
PA, PB = 0.0110, 0.0160
r_p = np.sqrt((px/PA)**2 + ((pz-ICZ+0.001)/PB)**2)
sclera = srgb(236, 228, 218); ir_out = srgb(34, 20, 15); ir_low = srgb(70, 42, 28); pup = srgb(16, 10, 9)
img = np.zeros((N, N, 3)); img[:] = sclera
shade = sstep((1.25 - r_i)/0.35)                 # soft darkening of the white toward the iris edge (limbus)
img = img*(1 - 0.10*shade[..., None])
low = sstep((-(pz-ICZ)/IB + 0.15)/0.9)           # warmer, lighter lower iris: pigment gradient, not a painted highlight
iris = ir_out[None, None, :]*(1-low[..., None]) + ir_low[None, None, :]*low[..., None]
ring = sstep((r_i - 0.80)/0.2)
iris = iris*(1 - 0.45*ring[..., None])
k = sstep((1.0 - r_i)/0.05)[..., None]; img = img*(1-k) + iris*k
k = sstep((1.0 - r_p)/0.10)[..., None]; img = img*(1-k) + pup[None, None, :]*k
eye_img = bpy.data.images.new("simm_head_eye_basecolor", N, N, alpha=False)
eye_img.pixels.foreach_set(np.concatenate([img, np.ones((N, N, 1))], 2).astype(np.float32).ravel())
eye_img.filepath_raw = os.path.join(texdir, "simm_head_eye_basecolor.png"); eye_img.file_format = 'PNG'; eye_img.save(); eye_img.pack()
m_eye = pbr("SCULPT_MAT_EYE", img=eye_img, rough=0.30, spec=0.5)
for eo in (eyeL, eyeR):
    eo.data.materials.clear(); eo.data.materials.append(m_eye)
    for p in eo.data.polygons: p.use_smooth = True

# ---------------- skin: albedo only (base tone, cheek warmth, lip tint, lash line). No painted shading.
tmp = face.copy(); tmp.data = face.data.copy(); coll.objects.link(tmp)
for md in tmp.modifiers: md.levels = 2
activate(tmp); bpy.ops.object.modifier_apply(modifier=tmp.modifiers[0].name)
co = co_of(tmp.data); x, y, z = co[:, 0], co[:, 1], co[:, 2]; ax = np.abs(x)
base = srgb(236, 186, 152); blush = srgb(226, 132, 112); lipc = srgb(186, 86, 80); lash = srgb(52, 31, 22); warm = srgb(224, 150, 122)
col = np.tile(base, (len(co), 1))
def mix(col, c, w): return col*(1-w[:, None]) + c[None, :]*w[:, None]
front = sstep((-y - 0.05)/0.04)
col = mix(col, blush, 0.42*np.exp(-(((ax-0.098)/0.034)**2 + ((z-1.116)/0.024)**2))*front)        # cheeks
col = mix(col, warm, 0.22*np.exp(-((ax/0.016)**2 + ((z-1.130)/0.012)**2))*front)                 # nose tip
col = mix(col, warm, 0.30*sstep((ax-0.150)/0.012)*sstep((z-1.09)/0.02)*sstep((1.21-z)/0.02))      # ears
MW = 0.0220; u = np.clip(x/MW, -1.2, 1.2); zl = 1.0900 - 0.0014 + 0.0058*np.abs(u)**2
dz = z - zl; sig = np.where(dz < 0, 0.0040, 0.0026)
lipw = np.exp(-(dz/sig)**2)*sstep((1.08 - np.abs(u))/0.25)*front*sstep((0.14 + y)/0.02 + 1.0)
col = mix(col, lipc, 0.85*lipw)
for sgn in (1, -1):                                                                               # upper lash line
    C = eye_c[sgn]; p = (x - C[0])*sgn; q = z - C[2]
    rho = ((np.abs(p)/OVAL_A)**OVAL_N + (np.abs(q)/np.where(q < 0, OVAL_B*0.94, OVAL_B))**OVAL_N)**(1/OVAL_N)
    band = sstep((rho - 0.88)/0.06)*sstep((1.24 - rho)/0.07)
    upper = sstep((q + 0.010)/0.016)
    near = sstep((0.09 - np.sqrt(p*p + q*q))/0.02)*front
    col = mix(col, lash, 0.35*sstep((rho - 0.92)/0.05)*sstep((1.10 - rho)/0.05)*upper*near)   # faint root tone under the lash geometry
    lower = (1-upper)*band*near
    col = mix(col, warm*0.85, 0.18*lower)                                                          # soft lower lid tone
skin_img = bake_vertex_colour(tmp, col, os.path.join(texdir, "simm_head_skin_basecolor.png"), 2048, margin=4)
bpy.data.objects.remove(tmp)
m_skin = pbr("SCULPT_MAT_SKIN", img=skin_img, rough=0.58, spec=0.35)
face.data.materials.clear(); face.data.materials.append(m_skin)

# ---------------- hair: unwrap the fused sculpt, bake a root-to-tip tone
scalp = Scalp(face)
activate(hair); bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.002); bpy.ops.object.mode_set(mode='OBJECT')
co = co_of(hair.data); lift = np.empty(len(co))
for i, p in enumerate(co):
    d = p - HC; r = np.linalg.norm(d)
    az = math.degrees(math.atan2(d[0], -d[1])); el = math.degrees(math.asin(d[2]/r))
    lift[i] = r - scalp.radius(az, el)
h_root = srgb(84, 46, 29); h_mid = srgb(110, 62, 38); h_tip = srgb(134, 80, 48)
# smooth the lift value over the surface first, so the tone has no flecks at clump junctions
ed = np.empty(len(hair.data.edges)*2, dtype=np.int32); hair.data.edges.foreach_get('vertices', ed); ed = ed.reshape(-1, 2)
dg_ = np.bincount(ed.ravel(), minlength=len(co)).astype(float)
for _ in range(25):
    acc = np.zeros(len(co)); np.add.at(acc, ed[:, 0], lift[ed[:, 1]]); np.add.at(acc, ed[:, 1], lift[ed[:, 0]])
    lift = 0.5*lift + 0.5*acc/np.maximum(dg_, 1)
t = sstep(lift/0.045)[:, None]; t2 = sstep((lift-0.04)/0.06)[:, None]
hcol = h_root[None]*(1-t) + h_mid[None]*t; hcol = hcol*(1-t2) + h_tip[None]*t2
hair_img = bake_vertex_colour(hair, hcol, os.path.join(texdir, "simm_head_hair_basecolor.png"), 1024, margin=10)
m_hair = pbr("SCULPT_MAT_HAIR", img=hair_img, rough=0.52, spec=0.4)
hair.data.materials.clear(); hair.data.materials.append(m_hair)

# ---------------- brows: thin relaxed arcs resting on the brow, hair-coloured
old = bpy.data.objects.get("SCULPT_BROWS")
if old: bpy.data.objects.remove(old)
bm = bmesh.new()
for sgn in (1, -1):
    pts = [(sgn*16.0, -1.4, .0008), (sgn*21, -0.7, .0014), (sgn*27, -1.0, .0014), (sgn*32.0, -2.8, .0008)]
    P = [scalp.point(a, e, l) for a, e, l in pts]
    sweep(bm, catmull(P, 12), 0.0052, thick=0.0018, n_around=10, root=.55, belly=.35, tip_pow=1.6, under=0.4, ridge=0.1)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
for f in bm.faces: f.smooth = True
bme = bpy.data.meshes.new("SCULPT_BROWS"); bm.to_mesh(bme); bm.free()
brows = bpy.data.objects.new("SCULPT_BROWS", bme); coll.objects.link(brows)
m_brow = pbr("SCULPT_MAT_BROW", colour=tuple(srgb(150, 98, 68)), rough=0.6, spec=0.3)
bme.materials.append(m_brow)

# ---------------- upper lashes: real geometry on the lid edge (crisp from any angle, nothing painted)
old = bpy.data.objects.get("SCULPT_LASHES")
if old: bpy.data.objects.remove(old)
bm = bmesh.new()
for sgn in (1, -1):
    C = eye_c[sgn]; P = []
    for ph in np.radians(np.linspace(18, 162, 13)):
        c_, s_ = np.cos(ph), np.sin(ph); e_ = 2.0/OVAL_N; up = max(s_, 0.0)
        g = 0.0012 + 0.0012*up
        p_ = (OVAL_A+g)*np.sign(c_)*abs(c_)**e_; q_ = (OVAL_B+g)*np.sign(s_)*abs(s_)**e_
        if q_ < 0: q_ *= 0.94
        Rr = EYE_R + 0.0012 + 0.0022*up - 0.0002
        P.append(np.array([C[0] + p_*sgn, C[1] - math.sqrt(max(Rr*Rr - p_*p_ - q_*q_, 1e-8)), C[2] + q_]))
    sweep(bm, catmull(P, 28), 0.0022, thick=0.0010, n_around=10, root=.35, belly=.30, tip_pow=1.5, under=0.5, ridge=0.0, root_cap=0.0004)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
for f in bm.faces: f.smooth = True
lme = bpy.data.meshes.new("SCULPT_LASHES"); bm.to_mesh(lme); bm.free()
lashes = bpy.data.objects.new("SCULPT_LASHES", lme); coll.objects.link(lashes)
m_lash = pbr("SCULPT_MAT_LASH", colour=tuple(srgb(60, 36, 26)), rough=0.6, spec=0.3)
lme.materials.append(m_lash)

# ---------------- names, export root, tidy
face.name = "SCULPT_HEAD"; face.data.name = "SCULPT_HEAD"
eyeL.name = "SCULPT_EYE_L"; eyeL.data.name = "SCULPT_EYE_L"; eyeR.name = "SCULPT_EYE_R"; eyeR.data.name = "SCULPT_EYE_R"
hair.data.name = "SCULPT_HAIR"
root = bpy.data.objects.get("SCULPT_HEAD_ROOT") or bpy.data.objects.new("SCULPT_HEAD_ROOT", None)
if root.name not in coll.objects: coll.objects.link(root)
root.empty_display_size = 0.05
for o in (face, eyeL, eyeR, hair, brows, lashes): o.parent = root
for im in list(bpy.data.images):
    if im.users == 0 and im.name.startswith("simm_head") is False and im.name not in ("Render Result",): pass
# seat the head a little lower on the collar (mesh data only; frozen rig untouched)
DROP = -0.018
for o in (face, eyeL, eyeR, hair, brows, lashes):
    c = co_of(o.data); c[:, 2] += DROP; o.data.vertices.foreach_set('co', c.ravel()); o.data.update()
g = bpy.data.objects.get("SCULPT_HAIR_GUIDES")
if g:
    for sp in g.data.splines:
        for pt in sp.points: pt.co.z += DROP
    g.parent = root
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.view_layer.objects.active = face
tx = bpy.data.texts.get("SCULPT_HEAD_NOTES") or bpy.data.texts.new("SCULPT_HEAD_NOTES")
tx.clear(); tx.write("Head candidate. New objects: SCULPT_HEAD (Blender Studio CC0 Human Base Meshes v1.0.0 stylized head, reshaped; Subdivision modifier level 1), SCULPT_EYE_L/R, SCULPT_HAIR (fused sculpt), SCULPT_HAIR_GUIDES (authoring curves, not exported), SCULPT_BROWS, SCULPT_HEAD_ROOT (identity export root). Frozen reference collection untouched. See inbox/HEAD_CANDIDATE_NOTES.md.\n")
bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out)
