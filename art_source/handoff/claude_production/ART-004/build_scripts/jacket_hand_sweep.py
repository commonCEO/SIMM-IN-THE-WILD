# Read-only measurement, nothing saved to the .blend: where the frozen hands and thighs travel in idle, walk and gather,
# expressed in the rest space of the bones the cloth is bound to. The build reads the result as plain data.
# blender -b collar_packet_v002.blend --python jacket_hand_sweep.py -- <absolute out.json>
import bpy, sys, json, numpy as np
sys.dont_write_bytecode = True
out = sys.argv[sys.argv.index("--")+1]
body = bpy.data.objects["PROTECTED_BODY"]; rig = bpy.data.objects["SimmRig"]; sc = bpy.context.scene
sm = [i for i, m in enumerate(body.data.materials) if m and m.name == "Simm warm skin"][0]
hand_faces = [tuple(p.vertices) for p in body.data.polygons if p.material_index == sm
              and all(abs(body.data.vertices[k].co.x) > 0.17 and body.data.vertices[k].co.z < 0.72 for k in p.vertices)]
BONES = {"hips": 0, "forearm_l": -1, "forearm_r": 1}             # forearm_l is on negative X in this rig
tm = [i for i, m in enumerate(body.data.materials) if m and m.name == "Simm charcoal olive trousers"][0]
leg_faces = [tuple(p.vertices) for p in body.data.polygons if p.material_index == tm and any(0.45 < body.data.vertices[k].co.z < 0.70 for k in p.vertices)]
legs = set(); LEG_KEEP = (0.520, 0.660); LEG_GRID = 0.004       # trousers near the hem, in hips rest space
KEEP = {"hips": (0.50, 0.68), "forearm_l": (0.630, 0.700), "forearm_r": (0.630, 0.700)}   # heights the cloth can reach
GRID = {"hips": 0.003, "forearm_l": 0.002, "forearm_r": 0.002}
N = 4; BARY = [(i/N, j/N, 1 - i/N - j/N) for i in range(N+1) for j in range(N+1-i)]       # surface samples, not only corners
rest = {b: rig.data.bones[b].matrix_local.copy() for b in BONES}
pts = {b: set() for b in BONES}
if rig.animation_data is None: rig.animation_data_create()
for an in ("idle", "walk", "gather"):
    act = bpy.data.actions[an]; rig.animation_data.action = act; f0, f1 = act.frame_range
    for fr in np.linspace(f0, f1, 17):
        sc.frame_set(int(fr), subframe=float(fr - int(fr))); dg = bpy.context.evaluated_depsgraph_get()
        eb = body.evaluated_get(dg); mb = eb.to_mesh(); pb = rig.evaluated_get(dg).pose.bones
        co = [v.co.copy() for v in mb.vertices]
        for b, sd in BONES.items():
            inv = (pb[b].matrix @ rest[b].inverted()).inverted(); G = GRID[b]; lo, hi = KEEP[b]
            for f in hand_faces:
                if sd and (body.data.vertices[f[0]].co.x < 0) != (sd < 0): continue
                loc = [inv @ co[k] for k in f]
                for t in range(1, len(loc) - 1):
                    A_, B_, C_ = loc[0], loc[t], loc[t+1]
                    for u, v_, w in BARY:
                        c = A_*u + B_*v_ + C_*w
                        if lo <= c.z <= hi: pts[b].add((round(c.x/G)*G, round(c.y/G)*G, round(c.z/G)*G))
        inv = (pb["hips"].matrix @ rest["hips"].inverted()).inverted()
        for f in leg_faces:
            loc = [inv @ co[k] for k in f]
            for t in range(1, len(loc) - 1):
                for u, v_, w in BARY:
                    c = loc[0]*u + loc[t]*v_ + loc[t+1]*w
                    if LEG_KEEP[0] <= c.z <= LEG_KEEP[1]: legs.add((round(c.x/LEG_GRID)*LEG_GRID, round(c.y/LEG_GRID)*LEG_GRID, round(c.z/LEG_GRID)*LEG_GRID))
        eb.to_mesh_clear()
json.dump({"note": "points on the hand skin surface of PROTECTED_BODY over 17 samples of idle, walk and gather, in each bone's rest space, snapped to a 2 or 3 mm grid, Blender axes, metres",
           "hand_faces": len(hand_faces), **{b: sorted([round(x, 4) for x in p] for p in v) for b, v in pts.items()},
           "hips_trousers_note": "points on the trousers surface near the hem over the same samples, hips rest space, 4 mm grid",
           "hips_trousers": sorted([round(x, 4) for x in p] for p in legs)}, open(out, "w"), separators=(",", ":"))
print("SWEEP trouser points %d; hand faces %d; points: %s" % (len(legs), len(hand_faces), {b: len(v) for b, v in pts.items()}))
