# ART-016 review only, never saved. Run before render_views.py on head v012 or head_b1.blend:
#   [B1_FLAT=1] blender -b <head blend> --python b1_review_prep.py --python render_views.py -- <args>
# Appends the held collar v004 parts (SCULPT_HOOD, SCULPT_SCARF) from ART-004/sources/collar_packet_v004.blend for neck
# and collar context (unchanged). B1_FLAT=1 gives every SCULPT_ object a simple flat colour (skin, hair, brows, lashes and
# non-glowing dark eyes) so the hair/face read can be compared with the reference without texture detail.
import bpy, os
here = os.path.dirname(os.path.abspath(__file__))
src = os.path.normpath(os.path.join(here, "..", "..", "ART-004", "sources", "collar_packet_v004.blend"))
with bpy.data.libraries.load(src, link=False) as (f, t): t.objects = [n for n in f.objects if n in ("SCULPT_HOOD", "SCULPT_SCARF")]
for o in t.objects: bpy.context.scene.collection.objects.link(o)
def flat(name, rgb, rough=0.7):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    c = [x/255.0 for x in rgb]; c = [(x/12.92 if x <= 0.04045 else ((x + 0.055)/1.055)**2.4) for x in c]
    b.inputs["Base Color"].default_value = c + [1]; b.inputs["Roughness"].default_value = rough; b.inputs["Specular"].default_value = 0.3; return m
if os.environ.get("B1_FLAT"):
    M = {"SCULPT_HEAD": flat("F_SKIN", (236, 196, 166)), "SCULPT_HAIR": flat("F_HAIR", (128, 74, 44)), "SCULPT_BROWS": flat("F_BROW", (90, 52, 32)),
         "SCULPT_LASHES": flat("F_LASH", (50, 32, 24)), "SCULPT_EYE_L": flat("F_EYE", (52, 34, 26), 0.6), "SCULPT_EYE_R": None}
    M["SCULPT_EYE_R"] = M["SCULPT_EYE_L"]
    for n, m in M.items():
        o = bpy.data.objects.get(n)
        if o:
            for s in o.material_slots: s.material = m
print("B1 review prep: collar context appended from", src, "flat" if os.environ.get("B1_FLAT") else "")
