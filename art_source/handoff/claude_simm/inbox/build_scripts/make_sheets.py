# Labelled review sheets. python3 make_sheets.py <version> <renders_dir> <reference_png> "<count line>"
import sys
from PIL import Image, ImageDraw, ImageFont
ver, R, refp, counts = sys.argv[1], sys.argv[2].rstrip('/') + '/', sys.argv[3], sys.argv[4]
def font(sz): return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", sz)
F = font(26); Fs = font(20)
labels = {'ref': 'Reference angle (3/4, elevated)', 'front': 'Front', 'side': "Side: Simm's right  [interpreted]",
          'sideL': "Side: Simm's left  [interpreted]", 'back': 'Back  [invented: not visible in reference]'}
for mode, title in (('clay', 'CLAY: neutral grey, soft directional light'), ('colour', 'COLOUR: base colour only, soft directional light')):
    vs = ['ref', 'front', 'side', 'sideL', 'back']; w = 640
    sheet = Image.new('RGB', (w*3, w*2 + 60), (40, 40, 40)); d = ImageDraw.Draw(sheet)
    d.text((16, 14), f"Simm head_candidate_{ver}   " + title, font=F, fill=(255, 255, 255))
    for i, v in enumerate(vs):
        im = Image.open(f'{R}head_{ver}_{mode}_{v}.png').resize((w, w), Image.LANCZOS)
        x, y = (i % 3)*w, 60 + (i//3)*w; sheet.paste(im, (x, y)); d = ImageDraw.Draw(sheet)
        d.rectangle((x, y, x + w, y + 34), fill=(0, 0, 0)); d.text((x + 10, y + 5), labels[v], font=Fs, fill=(255, 255, 255))
    x, y = 2*w, 60 + w; d.rectangle((x, y, x + w, y + w), fill=(28, 28, 28))
    txt = ["Geometry only: no image planes,", "no projected reference, no painted", "shadows or highlights.", "",
           "Invented (hidden in the reference):", "back of hair, nape, both ear sides,", "Simm's left profile.", "",
           "Base: Blender Studio CC0 Human", "Base Meshes v1.0.0 (stylized head).", ""] + counts.split('|')
    for k, t in enumerate(txt): d.text((x + 24, y + 40 + k*34), t, font=Fs, fill=(230, 230, 230))
    sheet.save(f'{R}head_{ver}_{mode}_sheet.png')
ref = Image.open(refp).convert('RGB').crop((812, 512, 980, 680)).resize((820, 820), Image.LANCZOS)
a = Image.open(f'{R}head_{ver}_colour_ref.png').resize((820, 820), Image.LANCZOS)
b = Image.open(f'{R}head_{ver}_clay_ref.png').resize((820, 820), Image.LANCZOS)
sheet = Image.new('RGB', (820*3, 820 + 110), (40, 40, 40)); d = ImageDraw.Draw(sheet)
d.text((16, 10), f"Reference vs head_candidate_{ver} (similar three-quarter angle). NOT a parity claim.", font=F, fill=(255, 255, 255))
caps = ["Reference: APPROVED_REFERENCE.png, unaltered crop, enlarged", "New model, colour, neutral studio light (Blender Cycles)", "New model, clay"]
for i, (im, c) in enumerate(zip((ref, a, b), caps)):
    sheet.paste(im, (i*820, 110)); d.text((i*820 + 12, 56), c, font=Fs, fill=(235, 235, 235))
d.text((16, 84), "Reference is lit by warm sun, the model neutrally. Camera is matched by eye, not pixel-aligned. Godot is the real test.", font=font(17), fill=(255, 200, 120))
sheet.save(f'{R}head_{ver}_reference_comparison.png')
c = Image.open(f'{R}head_{ver}_onbody_clay_ref.png'); e = Image.open(f'{R}head_{ver}_onbody_clay_front.png')
s2 = Image.new('RGB', (2000, 1060), (40, 40, 40)); s2.paste(c, (0, 60)); s2.paste(e, (1000, 60)); d = ImageDraw.Draw(s2)
d.text((16, 14), "Fit check on the frozen PROTECTED_BODY (body unchanged, shown for scale only, not exported)", font=F, fill=(255, 255, 255))
s2.save(f'{R}head_{ver}_fit_on_frozen_body.png')
