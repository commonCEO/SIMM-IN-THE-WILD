# ART-018 review prep only (never exported): colours SCULPT_HAIR by how much of each piece the reference shows.
# Run before render_views.py. Face ranges follow r2_stage_a.py's build order (under-surface first, then G in order,
# (NS-2)*M + M + 1 faces per piece). Flat emission-free colours: seen = orange, partly seen = yellow,
# invented (back, Simm's left) = purple, under-surface = grey.
import bpy
SEEN = {"fringe_right", "fringe_main", "fringe_mid", "temple_right", "side_right", "top_cover", "crown_tuft", "flick_right"}
PART = {"fringe_left", "flick_left", "side_right_back"}
ORDER = ["back_nape", "back_right", "back_left", "side_right_back", "side_right", "side_left_back", "side_left", "temple_right",
         "temple_left", "top_cover", "fringe_right", "fringe_main", "fringe_mid", "fringe_left", "crown_tuft", "flick_right", "flick_left"]
NS, M = 48, 18; PER = (NS - 2)*M + M + 1
me = bpy.data.objects["SCULPT_HAIR"].data; nU = len(me.polygons) - PER*len(ORDER); assert nU > 0
def mat(n, c):
    m = bpy.data.materials.new(n); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = c + (1,); b.inputs["Roughness"].default_value = 0.7; return m
me.materials.clear()
for n, c in (("INV_UNDER", (0.25, 0.25, 0.25)), ("INV_SEEN", (0.80, 0.30, 0.04)), ("INV_PART", (0.80, 0.65, 0.05)), ("INV_INVENTED", (0.35, 0.12, 0.60))):
    me.materials.append(mat(n, c))
idx = [0]*nU
for n in ORDER: idx += [1 if n in SEEN else 2 if n in PART else 3]*PER
me.polygons.foreach_set("material_index", idx); me.update()
print("INVENTION PREP", nU, "under-surface faces")
