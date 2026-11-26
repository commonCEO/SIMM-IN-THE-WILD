# Read-only evidence for the ART-004 hem method proposal. Nothing is saved. Weight changes, when asked for, are made
# on the candidate jacket copy in memory only, never on PROTECTED_BODY.
import bpy, sys, os, numpy as np, math
from mathutils.bvhtree import BVHTree
label, mode = sys.argv[sys.argv.index("--")+1:][:2]
WMAX = float(os.environ.get("WMAX", "0.5")); Z1 = float(os.environ.get("Z1", "0.635"))
body = bpy.data.objects["PROTECTED_BODY"]; jk = bpy.data.objects["SCULPT_JACKET"]; rig = bpy.data.objects["SimmRig"]; sc = bpy.context.scene
mi = {m.name: i for i, m in enumerate(body.data.materials) if m}
sstep = lambda t: 0.0 if t <= 0 else 1.0 if t >= 1 else t*t*(3-2*t)
co = np.array([v.co[:] for v in jk.data.vertices]); hem = co[:, 2].min()
changed = []
if mode == "thighs":
    g = {n: jk.vertex_groups[n] for n in ("hips", "thigh_l", "thigh_r")}
    for v in jk.data.vertices:
        z = v.co.z
        if z >= Z1 or abs(v.co.x) > 0.215: continue                 # torso only; sleeves are out at |x| > 0.215
        cur = {jk.vertex_groups[x.group].name: x.weight for x in v.groups}
        if set(cur) != {"hips"}: continue                            # only vertices that are 100 percent hips today
        fz = sstep((Z1 - z)/(Z1 - hem)); s = sstep(abs(v.co.x)/0.10)
        same, other = ("thigh_l", "thigh_r") if v.co.x < 0 else ("thigh_r", "thigh_l")   # thigh_l is on -X in this rig
        ws = fz*WMAX*(0.35 + 0.65*s); wo = fz*WMAX*0.35*(1 - s)
        if ws + wo < 0.005: continue
        g["hips"].add([v.index], 1.0 - ws - wo, 'REPLACE'); g[same].add([v.index], ws, 'REPLACE')
        if wo > 0.001: g[other].add([v.index], wo, 'REPLACE')
        changed.append(v.index)
tm, sm = mi["Simm charcoal olive trousers"], mi["Simm warm skin"]
def state(fr):
    sc.frame_set(int(fr), subframe=float(fr - int(fr))); dg = bpy.context.evaluated_depsgraph_get()
    eb = body.evaluated_get(dg); mb = eb.to_mesh(); bv = [v.co.copy() for v in mb.vertices]; polys = [(p.material_index, tuple(p.vertices)) for p in mb.polygons]
    ej = jk.evaluated_get(dg); mj = ej.to_mesh(); jv = [v.co.copy() for v in mj.vertices]; jp = [tuple(p.vertices) for p in mj.polygons]
    H = rig.evaluated_get(dg).pose.bones["hips"].matrix.copy(); eb.to_mesh_clear(); ej.to_mesh_clear()
    return bv, polys, jv, jp, H
tv_ids = sorted(set(i for p in body.data.polygons if p.material_index == mi["Simm charcoal olive trousers"] for i in p.vertices))
tv_ids = [i for i in tv_ids if 0.45 < body.data.vertices[i].co.z < 0.70]
NB = 36
def visible_breakthrough(bv, jv, jp, H):
    Hi = H.inverted(); jt = BVHTree.FromPolygons(jv, jp)
    loc = lambda c: Hi @ c                                       # hips space: y is up the spine, x and z across
    jl = [loc(c) for c in jv]; hem = np.full(NB, 9.0)
    for c in jl:
        if c.y > 0.12: continue
        k = int((math.atan2(c.x, c.z) + math.pi)/(2*math.pi)*NB) % NB; hem[k] = min(hem[k], c.y)
    n = 0; far = 0.0
    for i in tv_ids:
        p = bv[i]; c = loc(p); r = math.hypot(c.x, c.z)
        if r < 1e-4 or c.y > 0.12: continue
        k = int((math.atan2(c.x, c.z) + math.pi)/(2*math.pi)*NB) % NB
        if hem[k] > 8 or c.y < hem[k] + 0.006: continue          # below the hem: legs are meant to show there
        d_loc = (c.x/r, 0.0, c.z/r); dw = (H.to_3x3() @ __import__("mathutils").Vector(d_loc)).normalized()
        hit = jt.ray_cast(p + dw*0.0005, dw, 0.35)
        if hit[0] is None:
            n += 1; far = max(far, jt.find_nearest(p, 0.3)[3] or 0.0)
    return n, far
def hand_contact(bv, polys, jv):
    t = BVHTree.FromPolygons(bv, [f for m_, f in polys if m_ == sm]); n = 0; deep = 0.0
    for c in jv:
        loc_, nrm, idx, d = t.find_nearest(c, 0.03)
        if loc_ is not None and (c - loc_).dot(nrm) < -0.002: n += 1; deep = max(deep, d)
    return n, deep
tm, sm = mi["Simm charcoal olive trousers"], mi["Simm warm skin"]
if rig.animation_data is None: rig.animation_data_create()
print("RESULT %s: hem lowest Z %.3f; weights changed on %d vertices; trouser vertices tested %d" % (label, hem, len(changed), len(tv_ids)))
for an in ("idle", "walk", "gather"):
    act = bpy.data.actions[an]; rig.animation_data.action = act; f0, f1 = act.frame_range
    wn = 0; wf = 0.0; at = None; hn = 0; hd = 0.0
    for fr in np.linspace(f0, f1, 25):
        bv, polys, jv, jp, H = state(fr)
        n, far = visible_breakthrough(bv, jv, jp, H)
        if n > wn: wn = n; at = round(float(fr), 1)
        wf = max(wf, far)
        a_, b_ = hand_contact(bv, polys, jv); hn = max(hn, a_); hd = max(hd, b_)
    print("RESULT %s %-6s 25 samples: trouser points showing through the jacket above the hem: worst %3d at frame %s, up to %.1f mm outside | cloth >2 mm into a hand: worst %d vertices, up to %.1f mm" % (label, an, wn, at, wf*1000, hn, hd*1000))
