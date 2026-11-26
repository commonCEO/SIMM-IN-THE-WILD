import bpy, os
WMAX = float(os.environ.get("WMAX", "0.5")); Z1 = 0.635
if os.environ.get("WEIGHTS") == "thighs":
    jk = bpy.data.objects["SCULPT_JACKET"]; hem = min(v.co.z for v in jk.data.vertices)
    sstep = lambda t: 0.0 if t <= 0 else 1.0 if t >= 1 else t*t*(3-2*t)
    g = {n: jk.vertex_groups[n] for n in ("hips", "thigh_l", "thigh_r")}; n = 0
    for v in jk.data.vertices:
        if v.co.z >= Z1 or abs(v.co.x) > 0.215: continue
        if {jk.vertex_groups[x.group].name for x in v.groups} != {"hips"}: continue
        fz = sstep((Z1 - v.co.z)/(Z1 - hem)); s = sstep(abs(v.co.x)/0.10)
        same, other = ("thigh_l", "thigh_r") if v.co.x < 0 else ("thigh_r", "thigh_l")
        ws = fz*WMAX*(0.35 + 0.65*s); wo = fz*WMAX*0.35*(1 - s)
        if ws + wo < 0.005: continue
        g["hips"].add([v.index], 1.0 - ws - wo, 'REPLACE'); g[same].add([v.index], ws, 'REPLACE')
        if wo > 0.001: g[other].add([v.index], wo, 'REPLACE')
        n += 1
    print("WEIGHTS changed", n); bpy.context.view_layer.update()
