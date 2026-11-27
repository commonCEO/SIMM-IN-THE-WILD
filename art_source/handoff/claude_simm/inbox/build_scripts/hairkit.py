"""Hair authoring helpers. A lock is a hand-placed guide path over the scalp (azimuth, elevation, lift)
swept with a flattened, ridged, tapering section. Nothing here places locks: every path is authored in stage2."""
import bpy, bmesh, numpy as np, math
from mathutils import Vector
from mathutils.bvhtree import BVHTree

HC = np.array([0.0, 0.025, 1.235])     # head centre used for the scalp frame

def direction(az, el):
    a, e = math.radians(az), math.radians(el)
    return np.array([math.sin(a)*math.cos(e), -math.cos(a)*math.cos(e), math.sin(e)])

class Scalp:
    def __init__(self, obj):
        dg = bpy.context.evaluated_depsgraph_get()
        ev = obj.evaluated_get(dg); me = ev.to_mesh()
        vs = [v.co.copy() for v in me.vertices]; ps = [tuple(p.vertices) for p in me.polygons]
        self.bvh = BVHTree.FromPolygons(vs, ps); ev.to_mesh_clear()
    def radius(self, az, el):
        d = direction(az, el)
        # cast from outside inward so we always get the outer skin
        o = HC + d*0.6
        hit = self.bvh.ray_cast(Vector(o), Vector(-d))
        if hit[0] is None: return 0.16
        return float(np.linalg.norm(np.array(hit[0]) - HC))
    def point(self, az, el, lift=0.0):
        d = direction(az, el); return HC + d*(self.radius(az, el) + lift)

def catmull(P, n):
    P = np.asarray(P, float)
    if len(P) == 2: P = np.array([P[0], 0.5*(P[0]+P[1]), P[1]])
    ext = np.vstack([2*P[0]-P[1], P, 2*P[-1]-P[-2]])
    # chord-length parameterisation
    segs = len(P)-1; out = []
    L = np.linalg.norm(np.diff(P, axis=0), axis=1); cum = np.concatenate([[0], np.cumsum(L)])/L.sum()
    for s in np.linspace(0, 1, n+1):
        i = min(np.searchsorted(cum, s, side='right')-1, segs-1); i = max(i, 0)
        t = (s - cum[i])/max(cum[i+1]-cum[i], 1e-9)
        p0, p1, p2, p3 = ext[i], ext[i+1], ext[i+2], ext[i+3]
        out.append(0.5*((2*p1) + (-p0+p2)*t + (2*p0-5*p1+4*p2-p3)*t*t + (-p0+3*p1-3*p2+p3)*t**3))
    return np.array(out)

def width_profile(s, root=0.55, belly=0.30, tip_pow=1.5):
    """root fraction of full width at s=0, swelling to full at 'belly', then tapering to a point"""
    s = np.asarray(s, float)
    if belly <= 0: return np.maximum(1 - s**tip_pow, 0.0)
    up = root + (1-root)*np.sin(0.5*np.pi*np.clip(s/belly, 0, 1))
    down = 1 - np.clip((s-belly)/(1-belly), 0, 1)**tip_pow
    return np.where(s < belly, up, np.maximum(down, 0.0))

def sweep(bm, spine, width, thick=0.016, n_around=22, ridge=0.3, ridge_at=0.0, grooves=(), roll=(0.0, 0.0),
          root=1.0, belly=0.0, tip_pow=2.1, under=0.45, uv_layer=None, uv_u=(0, 1), root_cap=0.004,
          vol=False, channels=(), taper_from=0.62, section="plate", round_w=0.78, round_t=1.0):
    """vol=True (v005): a rounded, inflated volume instead of a flattened strap. Full round section through
    root and middle, thickness tapering only in the final third. channels = occasional shallow asymmetric
    channels that drift across the lock: (v_start, v_end, depth, s_start, s_end)."""
    n = len(spine)-1
    s = np.linspace(0, 1, n+1)
    wp = width_profile(s, root, belly, tip_pow)
    T = np.gradient(spine, axis=0); T /= np.linalg.norm(T, axis=1)[:, None]
    N = spine - HC; N -= (N*T).sum(1)[:, None]*T; N /= np.linalg.norm(N, axis=1)[:, None]
    B = np.cross(T, N)
    # more vertices over the visible top than the hidden underside
    nt = int(n_around*0.7); nb = n_around - nt
    th = np.concatenate([np.linspace(0, np.pi, nt, endpoint=False), np.linspace(np.pi, 2*np.pi, nb, endpoint=False)])
    rings = []
    for i in range(n):          # last sample is the tip point
        r = math.radians(roll[0] + roll[1]*s[i]); cr, sr = math.cos(r), math.sin(r)
        Bi = B[i]*cr + N[i]*sr; Ni = N[i]*cr - B[i]*sr
        w = 0.5*width*wp[i]; t = thick*(wp[i]**0.6)
        if section == "round":
            # v012 method prototype (Codex brief at d6b9555): a narrower, fuller clump. Half-width 78 percent of the
            # plate's, thickness kept, so the section goes from about 3.5:1 to about 2.7:1 wide-to-high; the top is a
            # convex ellipse (exponent 1.0, not the plate's flat-topped 0.55) with its crest skewed toward the leading
            # edge; thickness holds to 75 percent of the length and only the last quarter flattens to a blade.
            w *= round_w                      # 0.78 by default; per-lock values are annotated in stage 2
        if vol and section == "round":
            swell = 0.60 + 0.40*math.sin(0.5*math.pi*min(s[i]/0.30, 1.0))          # soft root: rises over 30 percent
            t = round_t*thick*swell*(1.0 - min(max((s[i] - 0.75)/0.25, 0.0), 1.0)**1.4)   # round_t: D1 diagnostic B
        elif vol:
            swell = 0.72 + 0.28*math.sin(0.5*math.pi*min(s[i]/0.38, 1.0))
            t = thick*swell*(1.0 - min(max((s[i] - taper_from)/(1.0 - taper_from), 0.0), 1.0)**1.7)
        c, sn = np.cos(th), np.sin(th)
        lat = np.sign(c)*np.abs(c)**(1.0 if vol else 0.85)
        top = np.clip(sn, 0, None)**(0.55 if vol else 0.8)
        if section == "round":
            top = np.clip(sn, 0, None)**1.0*(1.0 + 0.22*lat)/(1.0 + 0.22*np.clip(lat, -1, 1).max())*1.12   # convex, crest toward +lat
        prof = top*(1 + ridge*np.exp(-((lat - ridge_at)/0.5)**2))
        gd = 0.0
        for gv, gdep in grooves:
            depth = gdep*np.clip(s[i]/0.25, 0.15, 1)*np.clip((1 - s[i])/0.12, 0, 1)
            gd = gd + depth*np.exp(-((lat - gv)/0.15)**2)
        for v0, v1, cdep, s0, s1 in channels:
            if s0 < s[i] < s1:
                k = (s[i] - s0)/(s1 - s0)
                gd = gd + cdep*math.sin(math.pi*k)*np.exp(-((lat - (v0 + (v1 - v0)*k))/0.22)**2)
        prof = prof*(1 - np.clip(gd, 0, 0.75))
        h = np.where(sn >= 0, t*prof, t*under*sn)
        ring = [bm.verts.new(spine[i] + Bi*(w*l) + Ni*hh) for l, hh in zip(lat, h)]
        rings.append(ring)
    tipv = bm.verts.new(spine[-1]); rootv = bm.verts.new(spine[0] - T[0]*root_cap)
    uvl = bm.loops.layers.uv.verify()
    def setuv(f, uvs):
        for l, uv in zip(f.loops, uvs): l[uvl].uv = uv
    u0, u1 = uv_u
    U = lambda k: u0 + (u1-u0)*k/n_around
    for i in range(n-1):
        for k in range(n_around):
            k2 = (k+1) % n_around
            f = bm.faces.new((rings[i][k], rings[i][k2], rings[i+1][k2], rings[i+1][k]))
            setuv(f, [(U(k), s[i]), (U(k+1), s[i]), (U(k+1), s[i+1]), (U(k), s[i+1])])
    for k in range(n_around):
        k2 = (k+1) % n_around
        f = bm.faces.new((rings[n-1][k], rings[n-1][k2], tipv)); setuv(f, [(U(k), s[n-1]), (U(k+1), s[n-1]), (U(k+0.5), 1.0)])
        f = bm.faces.new((rings[0][k2], rings[0][k], rootv)); setuv(f, [(U(k+1), 0.0), (U(k), 0.0), (U(k+0.5), 0.0)])
    return rings
