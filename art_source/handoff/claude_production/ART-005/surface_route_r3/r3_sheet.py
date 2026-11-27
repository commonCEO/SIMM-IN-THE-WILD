# ART-019 diagram sheet (PIL only): python3 -I r3_sheet.py <render dir from r3_mass_diagram.py> <out png>
import sys, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
R, out = sys.argv[1:3]
Fn = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16); Fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
def lab(im, t):
    d = ImageDraw.Draw(im); d.rectangle([0, 0, im.size[0], 24], fill=(25, 25, 25)); d.text((6, 3), t, fill=(255, 255, 255), font=Fn); return im
C = 520; o = Image.new('RGB', (4*C, C+330), (255, 255, 255))
for k, (f, t) in enumerate((('p1_cage', '1  editable cage: mass (blue) + tucked tip (orange)'), ('p2_front', '2  subdivided, front'), ('p3_three_quarter', '3  subdivided, side'))):
    o.paste(lab(Image.open('%s/%s.png' % (R, f)).convert('RGB').resize((C, C), Image.LANCZOS), t), (k*C, 0))
J = json.load(open(R + '/r3_mass_sections.json')); pl = Image.new('RGB', (C, C), (250, 250, 250)); d = ImageDraw.Draw(pl)
sx, sy, ox, oy = 3000, 3000, C/2, 0
cols = {'-0.012': (30, 30, 30), '-0.030': (30, 90, 220), '-0.048': (210, 30, 30)}
for i, z in enumerate(('-0.012', '-0.030', '-0.048')):
    base = 140 + i*150; d.line([20, base, C-20, base], fill=(200, 170, 150), width=2)
    d.text((20, base + 6), 'section %s mm below the root' % abs(int(round(-float(z)*1000))), fill=cols[z], font=Fs)
    for nm, c in (('mass', cols[z]), ('secondary', (230, 130, 20))):
        P = np.array(J['sections'].get('%s_%s' % (nm, z), []))
        if len(P): 
            for a, r in P: d.ellipse([ox + a*sx - 1.2, base - r*sy - 1.2, ox + a*sx + 1.2, base - r*sy + 1.2], fill=c)
d.text((20, C - 40), 'tan line = skin, true scale; orange = tucked tip', fill=(60, 60, 60), font=Fs)
o.paste(lab(pl, '4  cross-sections of the subdivided mass'), (3*C, 0))
dd = ImageDraw.Draw(o); y = C + 12
for l in ['METHOD EVIDENCE ONLY (ART-019). One abstract fringe-scale mass on a forehead stand-in, not a head, not exported. Blender review render, not native.',
          'What the cage CAN express (shown): one connected volume with a D-shaped section (domed outside, flat against the skin), thick root, three UNEQUAL tips grown',
          'from the same topology (no separate roots, no root bulb), creased groove lines running from each notch up into the mass, a separate tucked tip whose root is buried',
          'inside the mass (overlap = its own shadow edge), and every vertex editable by hand in Blender (198 + 40 cage vertices).',
          'What it does NOT show, honestly: hair. Placed by coordinates from a script, without live viewport feedback, the mass reads as a melted wax drape with drips,',
          'not as the reference\'s tousled interlocking masses. Three passes (thin drape, thick drips, pointed drips with grooves) moved it only a little.',
          'Capability check in this container: sculpt brush strokes FAIL headless (no 3D viewport); mesh filters do nothing; cage editing, creases, subdivision,',
          'multires subdivision, shape keys, hooks, lattices, renders and cross-sections all work. So the route is authorable, but not by me at the needed quality.']:
    dd.text((10, y), l, fill=(20, 20, 20), font=Fs); y += 24
o.save(out); print(o.size)
