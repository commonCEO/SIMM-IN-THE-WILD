# ART-005 critique demo (Codex brief at a66d488). Review only: changes the eye material of the held head v012 IN MEMORY
# and saves nothing; run before render_views.py in the same Blender session:
#   blender -b inbox/head_candidate_v012.blend --python eye_e1_demo.py --python inbox/build_scripts/render_views.py -- <render args>
# E1 hypothesis (eyes only; geometry, lids, skin, hair and every other material held):
#   1. catchlights stop glowing: the emission link is removed; ONE soft catchlight stays, painted into the albedo
#      (sRGB about 225, 215, 200, 80 percent opacity), so it is lit like the face and dims in shade;
#   2. less gloss: roughness 0.42 -> 0.55, specular 0.35 -> 0.25 (fewer specular glints and less bright edge where
#      the eyeball meets the lids);
#   3. no pale rim: the iris oval is widened to cover the lid opening (0.0174 x 0.0264 half sizes) so no sclera ring
#      shows; the iris turns from near-black to dark warm brown, lighter toward the bottom, with a darker brown pupil.
#      Not v002-v008 (black, glossy, no highlight): colour is brown, the surface matte and one highlight stays.
# E1_OFF=1 renders the held v012 eye unchanged (control) through the same script.
import bpy, os, numpy as np
if not os.environ.get("E1_OFF"):
    EYE_R = None
    def srgb(r, g, b): c = np.array([r, g, b])/255.0; return np.where(c <= 0.04045, c/12.92, ((c + 0.055)/1.055)**2.4)
    def sstep(x): x = np.clip(x, 0, 1); return x*x*(3 - 2*x)
    # eye radius from the held eye mesh (same projection as stage3_finish.py)
    eo = bpy.data.objects["SCULPT_EYE_L"]; co = np.array([v.co[:] for v in eo.data.vertices]); EYE_R = float((co.max(0) - co.min(0))[0]/2)
    N = 512; yy, xx = np.mgrid[0:N, 0:N]
    px = ((xx + 0.5)/N - 0.5)*2*EYE_R; pz = ((yy + 0.5)/N - 0.5)*2*EYE_R
    IA, IB, ICZ = 0.0182, 0.0272, 0.0000            # covers the lid opening 0.0174 x 0.0264: no sclera ring
    r_i = np.sqrt((px/IA)**2 + ((pz-ICZ)/IB)**2)
    PA, PB = 0.0082, 0.0136
    r_p = np.sqrt((px/PA)**2 + ((pz-ICZ+0.0015)/PB)**2)
    ir_out = srgb(58, 34, 22); ir_low = srgb(122, 78, 46); pup = srgb(30, 18, 12); sclera = srgb(214, 190, 168)
    img = np.zeros((N, N, 3)); img[:] = sclera
    low = sstep((-(pz-ICZ)/IB + 0.10)/0.95)
    iris = ir_out[None, None, :]*(1-low[..., None]) + ir_low[None, None, :]*low[..., None]
    ring = sstep((r_i - 0.80)/0.20); iris = iris*(1 - 0.35*ring[..., None])
    k = sstep((1.0 - r_i)/0.05)[..., None]; img = img*(1-k) + iris*k
    k = sstep((1.0 - r_p)/0.20)[..., None]; img = img*(1-k) + pup[None, None, :]*k
    glint = 0.8*sstep((1.0 - np.sqrt(((px-0.0045)/0.0034)**2 + ((pz-0.0105)/0.0040)**2))/0.30)
    hi = srgb(225, 215, 200); img = img*(1-glint[..., None]) + hi[None, None, :]*glint[..., None]
    im = bpy.data.images.new("E1_eye_albedo", N, N, alpha=False)
    im.pixels.foreach_set(np.concatenate([img, np.ones((N, N, 1))], 2).astype(np.float32).ravel())
    m = bpy.data.materials["SCULPT_MAT_EYE"]; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    for l in list(nt.links):
        if l.to_socket == b.inputs["Emission"]: nt.links.remove(l)
        elif l.to_socket == b.inputs["Base Color"]: l.from_node.image = im
    b.inputs["Emission Strength"].default_value = 0.0
    b.inputs["Roughness"].default_value = 0.55; b.inputs["Specular"].default_value = 0.25
    print("E1 applied: eye radius %.4f" % EYE_R)
else:
    print("E1 control: held v012 eye")
