# ART-019 method evidence ONLY (Codex dispatch fd3a745): one abstract hair MASS authored as a connected low-resolution cage,
# not a head, not exported. Shows a broad mass turning into UNEQUAL subordinate tips with one tucked secondary tip.
#   blender -b --factory-startup --python r3_mass_diagram.py -- <abs out dir>
# Representation: a closed quad cage (top sheet + bottom sheet joined round the rim), every vertex placed from named
# rows and columns; per-vertex thickness; creased ridge loop; Catmull-Clark subdivision (level 3) as the only smoothing.
# Units: metres at roughly fringe scale (mass about 11 cm wide). Z up, the mass hangs toward -Z over a cylinder (forehead).
import bpy, bmesh, sys, os, json, numpy as np
from mathutils import Vector
out = sys.argv[sys.argv.index("--")+1]; os.makedirs(out, exist_ok=True)
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
NU, NV = 11, 9
u = np.linspace(0, 1, NU); v = np.linspace(0, 1, NV)
# lower-edge contour: notch level 0.45, three unequal tips (centre u, length to v=1 scale, half width in u)
TIPS = [("tip_long", 0.25, 1.00, 0.16), ("tip_mid", 0.62, 0.72, 0.12), ("tip_short", 0.88, 0.58, 0.10)]
def depth(uu):                                   # how far down (0..1) each column reaches
    d = 0.45
    for _, c, L, hw in TIPS:
        x = np.clip(1 - np.abs(uu - c)/hw, 0, 1); d = max(d, 0.45 + (L - 0.45)*x**1.6)
    return d
def pinch(uu, f):                                # in the tip region columns gather toward their tip centre
    best = min(TIPS, key=lambda t: abs(uu - t[1]))
    if abs(uu - best[1]) > best[3]: return uu
    return uu + (best[1] - uu)*f
W, H, R = 0.11, 0.075, 0.09                      # width, full length, forehead radius
def surf(uu, vv):                                # point ON the forehead cylinder (radius R, axis Z) and its outward normal
    a = (uu - 0.5)*W/R; z = -vv*H
    return np.array([R*np.sin(a), -R*np.cos(a), z]), np.array([np.sin(a), -np.cos(a), 0.0])
def thick(uu, vv, dcol):                         # VOLUME: domed across the mass (D-shaped section), thick root, steady taper
    dome = 0.35 + 0.65*np.sqrt(max(0.0, 1 - (2*uu - 1)**2))
    return 0.026*dome*max(1 - 0.85*(vv/dcol)**1.5, 0.08)
NOTCH = (0.44, 0.76)                             # columns between the tips: grooves run up from each notch into the mass
def GROOVE(uu, vv):
    return max([0.45*np.clip(1 - abs(uu - c)/0.07, 0, 1)*np.clip((vv - 0.10)/0.25, 0, 1) for c in NOTCH])
top, bot = {}, {}
bm = bmesh.new()
for i, uu in enumerate(u):
    dcol = depth(uu)
    for j, vv in enumerate(v):
        vvv = vv*dcol; f = np.clip((vvv - 0.40)/(dcol - 0.40 + 1e-6), 0, 1) if dcol > 0.46 else 0
        up = pinch(uu, min(1.0, 1.05*f**1.2)) - 0.035*f**2          # columns meet at a point; tips sweep toward -X (Simm's right)
        g = GROOVE(uu, vvv)                                          # flow groove: thinner along the notch columns
        p, n = surf(up, vvv); t = thick(uu, vvv, dcol)*(1 - g); lift = 0.002 + 0.012*f**2   # underside hugs the skin; tips curl outward
        top[i, j] = bm.verts.new(p + n*(lift + t)); bot[i, j] = bm.verts.new(p + n*lift)
for i in range(NU - 1):
    for j in range(NV - 1):
        bm.faces.new((top[i, j], top[i+1, j], top[i+1, j+1], top[i, j+1]))
        bm.faces.new((bot[i, j+1], bot[i+1, j+1], bot[i+1, j], bot[i, j]))
for i in range(NU - 1):                          # rim: root edge and lower edge
    bm.faces.new((top[i+1, 0], top[i, 0], bot[i, 0], bot[i+1, 0])); bm.faces.new((top[i, NV-1], top[i+1, NV-1], bot[i+1, NV-1], bot[i, NV-1]))
for j in range(NV - 1):                          # rim: two sides
    bm.faces.new((top[0, j+1], top[0, j], bot[0, j], bot[0, j+1])); bm.faces.new((top[NU-1, j], top[NU-1, j+1], bot[NU-1, j+1], bot[NU-1, j]))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
cl = bm.edges.layers.crease.verify()
ridge = []                                       # creased ridge loop down the long tip's top (gives a lit plane and a shade plane)
ic = int(round(TIPS[0][1]*(NU - 1)))
for j in range(2, NV - 1):
    e = [e for e in top[ic, j].link_edges if e.other_vert(top[ic, j]) is top[ic, j+1]][0]; e[cl] = 0.55; ridge.append(e)
for c in NOTCH:                                  # crease the groove lines (valley breaks)
    ig = int(round(c*(NU - 1)))
    for j in range(1, NV - 1):
        e = [e for e in top[ig, j].link_edges if e.other_vert(top[ig, j]) is top[ig, j+1]]
        if e: e[0][cl] = 0.7
me = bpy.data.meshes.new("R3_MASS_CAGE"); bm.to_mesh(me); bm.free()
mass = bpy.data.objects.new("R3_MASS", me); bpy.context.collection.objects.link(mass)
ss = mass.modifiers.new("subd", 'SUBSURF'); ss.levels = ss.render_levels = 3
# secondary tip: its own small cage, root buried INSIDE the mass volume, lying under the notch between long and mid tips
bm = bmesh.new(); S = {}
for i, uu in enumerate(np.linspace(0.36, 0.52, 4)):
    for j, vv in enumerate(np.linspace(0.30, 0.66, 5)):
        f = j/4; up = 0.44 + (uu - 0.44)*(1 - 0.8*f**1.4); p, n = surf(up, vv)
        t = 0.009*(1 - 0.75*f); lift = 0.003 + 0.004*f   # root buried inside the main mass; emerges under the notch
        S[i, j, 0] = bm.verts.new(p + n*(lift + t)); S[i, j, 1] = bm.verts.new(p + n*lift)
for i in range(3):
    for j in range(4):
        bm.faces.new((S[i, j, 0], S[i+1, j, 0], S[i+1, j+1, 0], S[i, j+1, 0])); bm.faces.new((S[i, j+1, 1], S[i+1, j+1, 1], S[i+1, j, 1], S[i, j, 1]))
for i in range(3):
    bm.faces.new((S[i+1, 0, 0], S[i, 0, 0], S[i, 0, 1], S[i+1, 0, 1])); bm.faces.new((S[i, 4, 0], S[i+1, 4, 0], S[i+1, 4, 1], S[i, 4, 1]))
for j in range(4):
    bm.faces.new((S[0, j+1, 0], S[0, j, 0], S[0, j, 1], S[0, j+1, 1])); bm.faces.new((S[3, j, 0], S[3, j+1, 0], S[3, j+1, 1], S[3, j, 1]))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
me2 = bpy.data.meshes.new("R3_SECONDARY_CAGE"); bm.to_mesh(me2); bm.free()
sec = bpy.data.objects.new("R3_SECONDARY", me2); bpy.context.collection.objects.link(sec)
s2 = sec.modifiers.new("subd", 'SUBSURF'); s2.levels = s2.render_levels = 3
# forehead stand-in (cylinder) so the mass reads in context
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=R, depth=0.16, location=(0, 0, -0.06)); fh = bpy.context.active_object; fh.name = "FOREHEAD_STANDIN"
for p in fh.data.polygons: p.use_smooth = True
for o in (mass, sec):
    for p in o.data.polygons: p.use_smooth = True
def mat(n, c, r=0.6):
    m = bpy.data.materials.new(n); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = c + (1,); b.inputs["Roughness"].default_value = r; return m
mass.data.materials.append(mat("clay", (0.6, 0.6, 0.6))); sec.data.materials.append(mat("clay2", (0.6, 0.6, 0.6))); fh.data.materials.append(mat("skin", (0.75, 0.62, 0.52)))
# cage wire copies for the diagram
def wire(src, name, col):
    o = bpy.data.objects.new(name, src.data.copy()); bpy.context.collection.objects.link(o)
    w = o.modifiers.new("w", 'WIREFRAME'); w.thickness = 0.0007; o.data.materials.clear(); o.data.materials.append(mat(name + "_m", col, 0.9)); return o
wm = wire(mass, "WIRE_MASS", (0.05, 0.25, 0.8)); ws = wire(sec, "WIRE_SEC", (0.85, 0.35, 0.05))
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 48; sc.cycles.device = 'CPU'
sc.render.resolution_x = sc.render.resolution_y = 560; sc.render.film_transparent = False
sc.world = bpy.data.worlds.new("w"); sc.world.use_nodes = True; sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.56, 0.58, 1); sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.35
ld = bpy.data.lights.new("key", 'SUN'); ld.energy = 3.2; ld.angle = 0.05; lo = bpy.data.objects.new("key", ld); sc.collection.objects.link(lo); lo.rotation_euler = (0.75, 0.0, -0.55)
cd = bpy.data.cameras.new("cam"); cd.lens = 85; cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam
def shoot(name, az, el, dist, vis):
    for o in sc.objects:
        if o.type == 'MESH': o.hide_render = o.name not in vis
    tgt = Vector((0, -0.10, -0.04)); a, e = np.radians(az), np.radians(el)
    cam.location = tgt + Vector((dist*np.sin(a)*np.cos(e), -dist*np.cos(a)*np.cos(e), dist*np.sin(e)))
    cam.rotation_euler = (tgt - cam.location).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(out, name + ".png"); bpy.ops.render.render(write_still=True)
shoot("p1_cage", 0, 5, 0.42, {"WIRE_MASS", "WIRE_SEC", "FOREHEAD_STANDIN"})
shoot("p2_front", 0, 5, 0.42, {"R3_MASS", "R3_SECONDARY", "FOREHEAD_STANDIN"})
shoot("p3_three_quarter", 62, 12, 0.42, {"R3_MASS", "R3_SECONDARY", "FOREHEAD_STANDIN"})
# cross-sections of the EVALUATED (subdivided) mass at three heights, in the mass's own frame (angle around Z, radius)
dg = bpy.context.evaluated_depsgraph_get(); sec_out = {}
for nm, o in (("mass", mass), ("secondary", sec)):
    em = o.evaluated_get(dg).to_mesh(); P = np.array([vv.co[:] for vv in em.vertices]); E = np.array([[e.vertices[0], e.vertices[1]] for e in em.edges]); o.evaluated_get(dg).to_mesh_clear()
    for z in (-0.012, -0.030, -0.048):
        a, b = P[E[:, 0]], P[E[:, 1]]; s = (a[:, 2] - z)*(b[:, 2] - z) < 0; t = (z - a[s, 2])/(b[s, 2] - a[s, 2]); q = a[s] + (b[s] - a[s])*t[:, None]
        ang = np.arctan2(q[:, 0], -q[:, 1])*R; rad = np.hypot(q[:, 0], q[:, 1]) - R   # arc length across, height off the skin
        sec_out["%s_%.3f" % (nm, z)] = np.stack([ang, rad], 1).round(5).tolist()
json.dump({"cage_vertices": {"mass": len(me.vertices), "secondary": len(me2.vertices)}, "subdivision_level": 3, "ridge_crease": 0.55,
           "tips": [{"name": n, "centre_u": c, "reach": L} for n, c, L, _ in TIPS], "sections": sec_out}, open(os.path.join(out, "r3_mass_sections.json"), "w"))
print("R3 MASS", len(me.vertices), len(me2.vertices))
