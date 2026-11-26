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
# v009 (user: "looks like it's from Silent Hill ... the concept is very cute"): the v002 to v008 iris was wider than
# the lid opening, so each eye read as one black glossy oval with no white and no highlight. Now, as in the concept
# art: white shows at both sides, a warm brown iris touches both lids, and two catchlights are painted in and
# made emissive so they read in any light.
IA, IB, ICZ = 0.0163, 0.0262, 0.0000             # v010: iris fills more of the opening (less white), as the reference's dark ovals
# v009 was 0.0140             # lid opening is 0.0174 x 0.0264 (half sizes)
r_i = np.sqrt((px/IA)**2 + ((pz-ICZ)/IB)**2)
PA, PB = 0.0086, 0.0142                           # v010: larger pupil, darker read (v009 0.0068, 0.0118)
r_p = np.sqrt((px/PA)**2 + ((pz-ICZ+0.0015)/PB)**2)
sclera = srgb(236, 227, 215); ir_out = srgb(30, 18, 12); ir_low = srgb(92, 56, 32); pup = srgb(18, 11, 9)   # v010: darker iris, softer white
img = np.zeros((N, N, 3)); img[:] = sclera
shade = sstep((1.35 - r_i)/0.45)                 # soft grey toward the iris edge, so the white is not flat paper
img = img*(1 - 0.12*shade[..., None])
low = sstep((-(pz-ICZ)/IB + 0.10)/0.95)          # iris lighter and warmer toward the bottom
iris = ir_out[None, None, :]*(1-low[..., None]) + ir_low[None, None, :]*low[..., None]
ring = sstep((r_i - 0.82)/0.18)
iris = iris*(1 - 0.55*ring[..., None])           # dark outer ring
k = sstep((1.0 - r_i)/0.05)[..., None]; img = img*(1-k) + iris*k
k = sstep((1.0 - r_p)/0.12)[..., None]; img = img*(1-k) + pup[None, None, :]*k
def blob(cx, cz, ra, rb): return sstep((1.0 - np.sqrt(((px-cx)/ra)**2 + ((pz-cz)/rb)**2))/0.18)
glint = np.maximum(blob(0.0045, 0.0105, 0.0040, 0.0046), 0.85*blob(-0.0050, -0.0110, 0.0020, 0.0020))   # v010: catchlights kept, smaller
white = srgb(255, 252, 246); img = img*(1-glint[..., None]) + white[None, None, :]*glint[..., None]
eye_img = bpy.data.images.new("simm_head_eye_basecolor", N, N, alpha=False)
eye_img.pixels.foreach_set(np.concatenate([img, np.ones((N, N, 1))], 2).astype(np.float32).ravel())
eye_img.filepath_raw = os.path.join(texdir, "simm_head_eye_basecolor.png"); eye_img.file_format = 'PNG'; eye_img.save(); eye_img.pack()
em = np.repeat(glint[..., None], 3, 2)
eye_em = bpy.data.images.new("simm_head_eye_emissive", N, N, alpha=False)
eye_em.pixels.foreach_set(np.concatenate([em, np.ones((N, N, 1))], 2).astype(np.float32).ravel())
eye_em.filepath_raw = os.path.join(texdir, "simm_head_eye_emissive.png"); eye_em.file_format = 'PNG'; eye_em.save(); eye_em.pack()
m_eye = pbr("SCULPT_MAT_EYE", img=eye_img, rough=0.42, spec=0.35)   # v010: less glassy (v009 0.30 / 0.5)
et = m_eye.node_tree.nodes.new("ShaderNodeTexImage"); et.image = eye_em
eb_ = m_eye.node_tree.nodes["Principled BSDF"]; m_eye.node_tree.links.new(et.outputs[0], eb_.inputs["Emission"])
eb_.inputs["Emission Strength"].default_value = 1.0
for eo in (eyeL, eyeR):
    eo.data.materials.clear(); eo.data.materials.append(m_eye)
    for p in eo.data.polygons: p.use_smooth = True

# ---------------- skin: albedo only (base tone, cheek warmth, lip tint, lash line). No painted shading.
tmp = face.copy(); tmp.data = face.data.copy(); coll.objects.link(tmp)
for md in tmp.modifiers: md.levels = 2
activate(tmp); bpy.ops.object.modifier_apply(modifier=tmp.modifiers[0].name)
co = co_of(tmp.data); x, y, z = co[:, 0], co[:, 1], co[:, 2]; ax = np.abs(x)
base = srgb(244, 186, 148); blush = srgb(232, 124, 104); lipc = srgb(150, 62, 58); lash = srgb(52, 31, 22); warm = srgb(228, 146, 116)   # v009: warmer
col = np.tile(base, (len(co), 1))
def mix(col, c, w): return col*(1-w[:, None]) + c[None, :]*w[:, None]
front = sstep((-y - 0.05)/0.04)
col = mix(col, blush, 0.58*np.exp(-(((ax-0.096)/0.036)**2 + ((z-1.114)/0.026)**2))*front)        # cheeks (v009: rosier)
col = mix(col, warm, 0.22*np.exp(-((ax/0.016)**2 + ((z-1.130)/0.012)**2))*front)                 # nose tip
col = mix(col, warm, 0.30*sstep((ax-0.150)/0.012)*sstep((z-1.09)/0.02)*sstep((1.21-z)/0.02))      # ears
MW = 0.0220; u = np.clip(x/MW, -1.6, 1.6); zl = 1.0900 - 0.0016 + 0.0050*np.abs(u)**2 + 0.0016*np.abs(u)**4
dz = z - zl; sig = np.where(dz < 0, 0.0024, 0.0016)          # v009: a crisp smile line, wider than the mouth seam,
lipw = np.exp(-(dz/sig)**2)*sstep((1.42 - np.abs(u))/0.22)*front*sstep((0.14 + y)/0.02 + 1.0)   # corners turned up
col = mix(col, lipc, 0.92*lipw)
for sgn in (1, -1):                                          # small dimples at the smile corners
    col = mix(col, lipc, 0.35*np.exp(-(((x - sgn*1.47*MW)/0.0016)**2 + ((z - (1.0884 + 0.0050*2.16 + 0.0016*4.67 + 0.0006))/0.0016)**2))*front)
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
# v008 (user review, 26 Nov 2026): lighter, warmer and more saturated, measured against the reference's hair
# (median 138, 76, 36; shadows 88, 37, 12; highlights 179, 111, 56). Was root 84, 46, 29 / mid 110, 62, 38 / tip 134, 80, 48.
h_root = srgb(102, 52, 24); h_mid = srgb(128, 70, 32); h_tip = srgb(162, 100, 50)
# smooth the lift value over the surface first, so the tone has no flecks at clump junctions
ed = np.empty(len(hair.data.edges)*2, dtype=np.int32); hair.data.edges.foreach_get('vertices', ed); ed = ed.reshape(-1, 2)
dg_ = np.bincount(ed.ravel(), minlength=len(co)).astype(float)
for _ in range(25):
    acc = np.zeros(len(co)); np.add.at(acc, ed[:, 0], lift[ed[:, 1]]); np.add.at(acc, ed[:, 1], lift[ed[:, 0]])
    lift = 0.5*lift + 0.5*acc/np.maximum(dg_, 1)
t = sstep(lift/0.045)[:, None]; t2 = sstep((lift-0.04)/0.06)[:, None]
hcol = h_root[None]*(1-t) + h_mid[None]*t; hcol = hcol*(1-t2) + h_tip[None]*t2
hair_img = bake_vertex_colour(hair, hcol, os.path.join(texdir, "simm_head_hair_basecolor.png"), 1024, margin=10)
m_hair = pbr("SCULPT_MAT_HAIR", img=hair_img, rough=0.70, spec=0.25)          # v008: less gloss (was rough 0.52, spec 0.4)
hair.data.materials.clear(); hair.data.materials.append(m_hair)

# ---------------- brows: thin relaxed arcs resting on the brow, hair-coloured
old = bpy.data.objects.get("SCULPT_BROWS")
if old: bpy.data.objects.remove(old)
bm = bmesh.new()
for sgn in (1, -1):
    # v009: brows sit close above the eyes, thicker and darker, with a friendly arch (were 36 mm above the eye, thin, pale)
    pts = [(sgn*15.0, -6.6, .0010), (sgn*20, -5.2, .0018), (sgn*26, -5.0, .0018), (sgn*31.5, -6.8, .0010)]
    ES = float(os.environ.get("EYE_SPREAD", "1.0"))      # v011 study: brows keep their place over the eyes when the eyes move apart
    pts = [(a*ES, e, l) for a, e, l in pts]
    P = [scalp.point(a, e, l) for a, e, l in pts]
    sweep(bm, catmull(P, 14), 0.0078, thick=0.0026, n_around=10, root=.60, belly=.45, tip_pow=1.5, under=0.4, ridge=0.1)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
for f in bm.faces: f.smooth = True
bme = bpy.data.meshes.new("SCULPT_BROWS"); bm.to_mesh(bme); bm.free()
brows = bpy.data.objects.new("SCULPT_BROWS", bme); coll.objects.link(brows)
m_brow = pbr("SCULPT_MAT_BROW", colour=tuple(srgb(98, 54, 30)), rough=0.7, spec=0.2)          # v009: darker
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
# v011 study (Codex brief at eb48d10): lower the upper hair and crown. CROWN_CUT (env; default 0.12 = v011, 0 = v010) is the share
# of the height from the eye line to the hair top to remove. Hair, upper scalp and the guide curves get the same
# smooth vertical compression above Z_CS only, so the hair stays seated on the scalp. Below Z_CS nothing moves: eyes,
# brows (top 1.208), lashes, fringe tips, face, ears and neck. The compression starts with zero slope change and ramps
# over W_CS, so there is no crease at Z_CS.
CROWN_CUT = float(os.environ.get("CROWN_CUT", "0.12"))   # v011 default; CROWN_CUT=0 rebuilds v010
if CROWN_CUT > 0:
    Z_CS, W_CS = 1.235, 0.040
    ez = float(np.mean([co_of(o.data)[:, 2].mean() for o in (eyeL, eyeR)]))
    top = float(co_of(hair.data)[:, 2].max()); R_ = CROWN_CUT*(top - ez); s_ = 1.0 - R_/((top - Z_CS) - W_CS/2)
    def crown_map(z):
        u = np.maximum(z - Z_CS, 0.0)
        g_ = np.where(u < W_CS, u - (1 - s_)*u*u/(2*W_CS), u - (1 - s_)*(u - W_CS/2))
        return np.where(z > Z_CS, Z_CS + g_, z)
    moved = {}
    for o in (face, hair):
        c = co_of(o.data); z0 = c[:, 2].copy(); c[:, 2] = crown_map(z0); o.data.vertices.foreach_set('co', c.ravel()); o.data.update()
        m = np.abs(c[:, 2] - z0) > 1e-6; moved[o.name] = (int(m.sum()), float(z0[m].min()) if m.any() else None)
    if g:
        for sp in g.data.splines:
            for pt in sp.points: pt.co.z = float(crown_map(np.array([pt.co.z]))[0])
    print("CROWN_CUT %.3f: eye line Z %.4f, hair top %.4f -> %.4f (removes %.1f mm), upper slope factor %.3f above Z %.3f; moved %s" % (CROWN_CUT, ez, top, float(co_of(hair.data)[:, 2].max()), R_*1000, s_, Z_CS, moved))
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.view_layer.objects.active = face
tx = bpy.data.texts.get("SCULPT_HEAD_NOTES") or bpy.data.texts.new("SCULPT_HEAD_NOTES")
tx.clear(); tx.write("Head candidate. New objects: SCULPT_HEAD (Blender Studio CC0 Human Base Meshes v1.0.0 stylized head, reshaped; Subdivision modifier level 1), SCULPT_EYE_L/R, SCULPT_HAIR (fused sculpt), SCULPT_HAIR_GUIDES (authoring curves, not exported), SCULPT_BROWS, SCULPT_HEAD_ROOT (identity export root). Frozen reference collection untouched. See inbox/HEAD_CANDIDATE_NOTES.md.\n")
bpy.ops.wm.save_as_mainfile(filepath=out)
print("SAVED", out)
