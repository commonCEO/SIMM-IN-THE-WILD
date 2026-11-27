# ART-018 review sheets (PIL only). python3 -I r2a_sheets.py <scratch dir> <out dir>
# Inputs in <scratch>: p1/ref_full.png (reference, read with git cat-file, never committed), b1/mask_ref_full.png (its
# hue-threshold hair mask), b1/eyes_render.npy (eye centres in the 700 px ref render), b1/R_held_clay_{ref,alt}.png,
# b1/mask_held.png, r2/A_clay_{ref,alt}.png, r2/A_colour_ref.png, r2/I_colour_{ref,alt}.png (render_views.py outputs).
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S, D = sys.argv[1:3]
def hm(p):
    h = np.asarray(Image.open(p).convert('HSV')).astype(int); return (h[..., 0] >= 11) & (h[..., 0] <= 16) & (h[..., 1] > 120)
Image.fromarray((hm(S+'/r2/A_colour_ref.png')*255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5)).save(S+'/r2/mask_A.png')
Fn = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16); Fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
def lab(im, t):
    d = ImageDraw.Draw(im); d.rectangle([0, 0, im.size[0], 24], fill=(25, 25, 25)); d.text((6, 3), t, fill=(255, 255, 255), font=Fn); return im
E = np.load(S+'/b1/eyes_render.npy'); rL, rR = E[0], E[1]; fL, fR = np.array([912., 592.]), np.array([889., 596.])
vr = rL-rR; vf = fL-fR; s = np.linalg.norm(vr)/np.linalg.norm(vf); ang = np.arctan2(vr[1], vr[0])-np.arctan2(vf[1], vf[0])
A = s*np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]]); t = rR-A@fR; Ai = np.linalg.inv(A)
def warp(img):
    a, b_ = Ai[0]; d, e = Ai[1]; tx, ty = -(Ai@t); return img.transform((700, 700), Image.AFFINE, (a, b_, tx, d, e, ty), resample=Image.BICUBIC)
REF = Image.open(S+'/p1/ref_full.png').convert('RGB')
mr = warp(Image.open(S+'/b1/mask_ref_full.png').convert('L')).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3)).point(lambda x: 255 if x > 127 else 0)
outer = np.asarray(mr.filter(ImageFilter.MaxFilter(25))) > 0; band = outer & ~(np.asarray(mr.filter(ImageFilter.MinFilter(25))) > 0)
def edge(m):
    m = m.point(lambda x: 255 if x > 127 else 0); return np.asarray(m.filter(ImageFilter.MaxFilter(5))).astype(int)-np.asarray(m.filter(ImageFilter.MinFilter(5))).astype(int) > 0
px = np.asarray(Image.blend(warp(REF), Image.new('RGB', (700, 700), (255, 255, 255)), 0.6)).copy().astype(float)
px[band] = px[band]*0.55+np.array([255, 215, 0])*0.45
mH = Image.open(S+'/b1/mask_held.png').convert('L'); mA = Image.open(S+'/r2/mask_A.png').convert('L')
for m, colr in ((mr, (0, 0, 0)), (mH, (210, 30, 30)), (mA, (30, 90, 220))): px[edge(m.filter(ImageFilter.MedianFilter(5)))] = colr
ov = Image.fromarray(px.astype(np.uint8)); d = ImageDraw.Draw(ov)
for p in (rL, rR): d.ellipse([p[0]-5, p[1]-5, p[0]+5, p[1]+5], outline=(0, 150, 0), width=2)
outA = int(((np.asarray(mA) > 127) & ~outer).sum()); outH = int(((np.asarray(mH) > 127) & ~outer).sum())
print('hair pixels outside reference envelope + band: Stage A', outA, 'held', outH)
W = H = 700; o = Image.new('RGB', (3*W, H+200), (255, 255, 255))
o.paste(lab(ov, 'ANALYTICAL overlay, ref view (not the original)'), (0, 0))
o.paste(lab(Image.open(S+'/r2/I_colour_ref.png').convert('RGB'), 'invention map, ref view'), (W, 0))
o.paste(lab(Image.open(S+'/r2/I_colour_alt.png').convert('RGB'), 'invention map, alt view'), (2*W, 0))
dd = ImageDraw.Draw(o); y = H+10
for col, tx in (((0, 0, 0), 'black: reference hair envelope (hue threshold)'), ((255, 215, 0), 'yellow: +-12 px edge uncertainty band'),
                ((210, 30, 30), 'red: held v012 hair edge'), ((30, 90, 220), 'blue: R2 Stage A hair edge'), ((0, 150, 0), 'green: eye centres used to align')):
    dd.rectangle([10, y, 30, y+14], fill=col); dd.text((38, y), tx, fill=(20, 20, 20), font=Fs); y += 22
dd.text((10, y+4), 'Outside envelope + band: Stage A %d px, held %d px.' % (outA, outH), fill=(20, 20, 20), font=Fs)
y = H+10
for col, tx in (((204, 77, 10), "orange: pieces the reference shows (fringe, Simm's right side and temple, top, crown tuft, right flick)"),
                ((204, 166, 13), "yellow: pieces it shows only in part (left fringe tip, left flick, right back side)"),
                ((90, 30, 153), "purple: invented, no reference (back, nape, Simm's left side and temple)"), ((64, 64, 64), 'grey: under-surface (should never be seen)')):
    dd.rectangle([W+10, y, W+30, y+14], fill=col); dd.text((W+38, y), tx, fill=(20, 20, 20), font=Fs); y += 22
dd.text((W+10, y+6), 'Flat colours, Blender review render, not native. Reference camera unknown and more top-down. Ignore below the chin.', fill=(20, 20, 20), font=Fs)
o.save(D+'/r2a_overlay.png')
C = 500
def L(p): return Image.open(p).convert('RGB').resize((C, C), Image.LANCZOS)
o2 = Image.new('RGB', (3*C, 2*C+120), (255, 255, 255))
o2.paste(lab(REF.crop((820, 505, 960, 645)).resize((C, C), Image.LANCZOS), 'reference (original pixels, unaltered)'), (0, 0))
blank = Image.new('RGB', (C, C), (235, 235, 235)); db = ImageDraw.Draw(blank)
db.text((20, C//2-20), 'no reference for this view:', fill=(60, 60, 60), font=Fn); db.text((20, C//2+4), "the back and Simm's left are invented", fill=(60, 60, 60), font=Fn)
o2.paste(lab(blank, 'reference, alt view'), (0, C))
for r, v in enumerate(('ref', 'alt')):
    o2.paste(lab(L(S+'/b1/R_held_clay_%s.png' % v), 'CONTROL held v012, clay, %s' % v), (C, r*C))
    o2.paste(lab(L(S+'/r2/A_clay_%s.png' % v), 'CANDIDATE R2 Stage A, clay, %s' % v), (2*C, r*C))
dd = ImageDraw.Draw(o2); y = 2*C+10
for l in ['Blender review renders (render_views.py, same lights, cameras and clay), NOT native. Only the hair differs: face, eyes, brows, lashes, neck, body, rig unchanged.',
          'Stage A: an under-surface grown from the scalp plus 17 authored pieces on hand-placed guides, ridged lens sections, separate overlapping islands, no fusion.',
          'Collar v004 appended unchanged for context. The reference is sunlit, painted, blurred, about 120 px for the head, camera unknown.']:
    dd.text((10, y), l, fill=(20, 20, 20), font=Fs); y += 24
o2.save(D+'/r2a_comparison.png'); print('sheets', o.size, o2.size)
