"""Small sculpt toolkit: brush-style deformations on mesh vertex arrays (numpy).
Each call is one deliberate stroke: grab / inflate / scale / smooth with a soft falloff."""
import bpy, bmesh, numpy as np

def get_co(o):
    a = np.empty(len(o.data.vertices)*3); o.data.vertices.foreach_get('co', a); return a.reshape(-1, 3).copy()
def set_co(o, co):
    o.data.vertices.foreach_set('co', np.ascontiguousarray(co, dtype=np.float64).ravel()); o.data.update()
def apply_world(o):
    import mathutils
    co = get_co(o); M = np.array(o.matrix_world)
    co = co @ M[:3, :3].T + M[:3, 3]
    set_co(o, co); o.matrix_world = mathutils.Matrix.Identity(4)
def normals(o):
    o.data.calc_normals() if hasattr(o.data, "calc_normals") else None
    a = np.empty(len(o.data.vertices)*3); o.data.vertices.foreach_get('normal', a); return a.reshape(-1, 3)
def edges(o):
    a = np.empty(len(o.data.edges)*2, dtype=np.int32); o.data.edges.foreach_get('vertices', a); return a.reshape(-1, 2)
def face_sets(o):
    a = np.empty(len(o.data.polygons), dtype=np.int32); o.data.attributes['.sculpt_face_set'].data.foreach_get('value', a); return a
def vert_face_sets(o):
    """dict faceset -> boolean vertex mask (vertex belongs to at least one face of the set)"""
    fs = face_sets(o); n = len(o.data.vertices); out = {}
    for p in o.data.polygons:
        s = int(fs[p.index])
        m = out.get(s)
        if m is None: m = out[s] = np.zeros(n, bool)
        m[list(p.vertices)] = True
    return out
def falloff(d, r, sharp=1.0):
    t = np.clip(1.0 - (d/r)**2, 0, 1)
    return t**(2*sharp)
def sym(c):
    c = np.asarray(c, float); return [c, c*np.array([-1, 1, 1])]

class Sculpt:
    def __init__(self, o):
        self.o = o; self.co = get_co(o); self.E = edges(o); self.n = len(self.co)
        # adjacency for smoothing
        self.deg = np.bincount(self.E.ravel(), minlength=self.n).astype(float)
    def commit(self): set_co(self.o, self.co)
    def w(self, c, r, sharp=1.0, mask=None):
        d = np.linalg.norm(self.co - np.asarray(c, float), axis=1)
        w = falloff(d, r, sharp)
        if mask is not None: w = w*mask
        return w
    def grab(self, c, r, delta, sharp=1.0, mask=None, mirror=False):
        delta = np.asarray(delta, float)
        if mirror:
            for s in (1, -1):
                cc = np.array(c, float)*[s, 1, 1]; dd = delta*[s, 1, 1]
                self.co += self.w(cc, r, sharp, mask)[:, None]*dd
        else:
            self.co += self.w(c, r, sharp, mask)[:, None]*delta
    def inflate(self, c, r, amount, sharp=1.0, mask=None, mirror=False):
        self.commit(); N = normals(self.o)
        cs = sym(c) if mirror else [np.asarray(c, float)]
        for cc in cs:
            self.co += (self.w(cc, r, sharp, mask)*amount)[:, None]*N
    def scale(self, c, r, s, sharp=1.0, mask=None, mirror=False, pivot=None):
        s = np.asarray(s, float)*np.ones(3)
        cs = sym(c) if mirror else [np.asarray(c, float)]
        ps = (sym(pivot) if mirror else [np.asarray(pivot, float)]) if pivot is not None else cs
        for cc, pp in zip(cs, ps):
            w = self.w(cc, r, sharp, mask)[:, None]
            self.co += w*((self.co - pp)*(s - 1.0))
    def smooth(self, c=None, r=None, it=5, k=0.5, sharp=1.0, mask=None, mirror=False):
        if c is None:
            w = np.ones(self.n) if mask is None else mask.astype(float)
        else:
            w = np.zeros(self.n)
            for cc in (sym(c) if mirror else [np.asarray(c, float)]):
                w = np.maximum(w, self.w(cc, r, sharp, mask))
        E = self.E
        for _ in range(it):
            acc = np.zeros_like(self.co)
            np.add.at(acc, E[:, 0], self.co[E[:, 1]]); np.add.at(acc, E[:, 1], self.co[E[:, 0]])
            avg = acc/np.maximum(self.deg, 1)[:, None]
            self.co += (w*k)[:, None]*(avg - self.co)
    def symmetrize(self):
        """average with mirrored twin (base mesh is topologically symmetric); keeps x=0 seam exact"""
        from mathutils import kdtree
        if not hasattr(self, "_twin"):
            raise RuntimeError("call find_twins first")
        t = self._twin; m = self.co[t]*[-1, 1, 1]
        self.co = 0.5*(self.co + m)
    def find_twins(self):
        from mathutils import kdtree
        kd = kdtree.KDTree(self.n)
        for i, p in enumerate(self.co): kd.insert(p, i)
        kd.balance()
        tw = np.empty(self.n, int); md = 0
        for i, p in enumerate(self.co):
            _, j, d = kd.find((-p[0], p[1], p[2])); tw[i] = j; md = max(md, d)
        self._twin = tw; return md

def smooth_table(xs, ys, sigma, lo, hi, n=2000):
    """monotone remap table: piecewise-linear knots smoothed by a gaussian so the warp has no creases"""
    g = np.linspace(lo, hi, n); v = np.interp(g, xs, ys)
    step = (hi-lo)/(n-1); k = int(3*sigma/step)
    x = np.arange(-k, k+1)*step; ker = np.exp(-0.5*(x/sigma)**2); ker /= ker.sum()
    # extend linearly at the ends to avoid edge shrink
    vl = v[0] + (np.arange(-k, 0))*(v[1]-v[0]); vr = v[-1] + (np.arange(1, k+1))*(v[-1]-v[-2])
    vv = np.convolve(np.concatenate([vl, v, vr]), ker, mode='valid')
    return g, vv
def remap(z, table):
    return np.interp(z, table[0], table[1])
