# ART-015 eye-boundary source and ONE construction method: "inlay eye" (Fable, 27 Nov 2026, run 44; answers Codex `5fafefb`)

Method study only. No new head version, no GLB, no production geometry packet, no eye-material retry. The committed
stage scripts and every committed asset are unchanged. The method lives as a patch plus a scratch runner in
`art_source/handoff/claude_production/ART-005/face_method/`.

## What I looked at

- **Codex's native evidence:** `reviews/e1-native-eye-and-camp-detail.png` (the flat unlit eye control) and
  `reviews/e1-native-head-controls.png`.
- **The source that builds the eye region:**
  - `stage1_head.py` section 8: lid fitting on the eyeball sphere, lid margin `th`, orbital blend.
  - `stage3_finish.py`: eyeball rebuild, lash seating.
- **The held v012 mesh:** measured.
- **Not looked at:** Godot itself. Native behaviour of the proposal is UNKNOWN until Codex tests it.

## Source of the pale boundary

It is the skin of `SCULPT_HEAD` around each opening (the lid ring and orbital faces built in stage 1, section 8), not
any eye material.

1. The eyeball is a 36 mm sphere seen through a tall oval opening (half sizes 17.4 x 26.4 mm). At the opening edge its
   surface lies about 4.5 mm behind the front pole at the sides but about 11.5 mm at the top and bottom.
2. Stage 1 lays the lid ring on that sphere at radius `EYE_R + th` (`th` 1.2 mm at the lower lid to 3.4 mm at the
   upper), then blends the orbital skin up to the face.
3. Result: a raised lip, then a socket wall that stands up to 18 mm above the eye surface at the top and bottom.

Measured on the held v012 (`face_method/rim_measure.py`). Rays go straight back from the skin to the eye surface, in
bands of the oval coordinate e just outside the opening:

| Band | Held v012: skin above eye surface, median / 90th pct / max | Held: how much the skin faces the viewer (median; 1 = straight at the camera) |
|---|---|---|
| e 1.00-1.08 | 0.52 / 1.45 / 3.21 mm | 0.57 |
| e 1.08-1.15 | 2.34 / 4.47 / 6.18 mm | 0.90 |
| e 1.15-1.30 | 4.82 / 11.04 / 18.07 mm | 0.85 |

The lip (e 1.00-1.08) is turned well away from the face plane (0.57 against about 0.9 for the face). Under a
directional key it shades differently from the face beside it, while the eye inside stays flat. That is consistent with
Codex's native finding that the outline stays with textureless, unlit, specular-free eyes, and that it sits on the side
facing the key. Blender's soft area lights do not reproduce the outline in either version, so the geometry numbers are
my evidence, not Blender shading. A colour-coded band render (`build_scripts/eye_boundary_diag.py`, `DIAG=bands`) puts
the widest lip band exactly where the native crescent appears.

## The method: inlay eye (ONE localized construction change)

The visible front of each eyeball becomes a shallow cap whose depth behind the front pole is x²/(2·RX) + z²/(2·RZ),
reaching 6 mm (`INLAY_EDGE`) at the opening edge in every direction. That is about level with the skin around it, so
the eye sits in the face like an inlay instead of a large sphere seen through a hole. RX is 28.2 mm and RZ 61.1 mm. Every
lid formula that used the sphere uses the cap instead, and the lid margin thins from 1.2 + 2.2 mm to 0.3 + 0.6 mm (thin
margin only toward the upper lid). The lashes are seated on the same cap.

**Exactly what changes** (patch `face_method/inlay_method.patch`, an opt-in `INLAY=1` switch):
- `stage1_head.py`: `on_sphere()` returns the cap surface (offset by R - EYE_R) when INLAY is on, and the lid margin
  `th` becomes 0.3 mm + 0.6 mm x upper-lid factor.
- `stage3_finish.py`: the eyeball's front half is reshaped to the cap after the sphere is built. Its UV is a straight-on
  x/z projection and is unaffected, so the E1 or held eye texture maps the same way. The lash path follows the cap.
- With INLAY unset the build is v012 exactly. I verified this by a full rebuild with the switch present (six meshes and
  four textures identical) and then restored the committed scripts.

**Held:** eyeball size, eye centres, eye-opening outline (oval and egg shape), brows, hair, mouth, cheeks, forehead,
skin texture, every material (the E1 texture is used only for coloured diagnosis), costume, rig, actions, socket.

**A full inlay build is not local.** Stage 1's later brow smoothing and the stage 2 hair rebuild react slightly:
- brows move up to 0.96 mm, the hair gains one vertex, and head skin outside the eye region moves up to 1.75 mm;
- so a production version must freeze those, for example by building the inlay as a post-step on the finished v012
  head, or by masking stage 1's brow smoothing.

The demo avoids this: `face_method/compose_inlay_demo.py` takes, in memory, only the eyeballs, the lashes and the skin
around the openings (full weight to e 1.6, fading to zero by e 2.4) from a scratch inlay build. Everything else is
exactly v012. In that composite:
- 954 head base vertices move over 0.05 mm (max 6.99 mm), all inside the eye regions;
- each eyeball's front moves at most 24.5 mm, at the top and bottom of the cap;
- lashes move at most 3.3 mm.

## Two-view demonstration (Blender, in memory, not native)

`face_method/eye_inlay_method_demo.png` shows held v012 against the inlay at the ref and alt views, in three forms:
- clay;
- flat unlit eyes (as Codex's native control);
- E1 colour.

It also has a 2.25x eye crop and a whole-head pair. The same file is measured:

| Band | Inlay: skin above eye surface, median / 90th pct / max | Inlay: facing the viewer |
|---|---|---|
| e 1.00-1.08 | -0.14 / 0.34 / 0.91 mm | 0.94 |
| e 1.08-1.15 | 0.46 / 1.10 / 1.67 mm | 0.99 |
| e 1.15-1.30 | 2.23 / 4.29 / 6.64 mm | 0.90 |

The lip and wall are gone: the skin meets the eye almost flush and faces the viewer like the rest of the face. In clay
the raised ring around each eye is largely gone. With flat eyes, the eyes read as dark ovals set into the face, closer
to the reference's soft inset-free read.

What the demo does NOT show, honestly:
1. **Whole-face effect in Blender is small.** At whole-head scale the inlay is hard to tell from v012, because Blender's
   soft lights never showed the rim strongly. The case rests on the native renderer, where the rim was the visible
   defect.
2. **A pale arc can appear under the upper lash with the E1 texture.** The shallower cap shows a little more of the
   texture's upper edge, so the E1 sclera tone (214, 190, 168) shows as a thin arc. This is a texture-to-geometry
   interaction, not new geometry; I did not retry the material (outside this brief).
3. **A faint thin line remains along the 0.6 mm upper-lid margin** in the flat-eye crop.

## Rejection criteria (native, Codex's A1 studio setup at both agreed views, plus camp zoom 10)

1. **R1 boundary:** with flat unlit eyes (Codex's control), no continuous pale outline at either view. A remaining
   upper-lid line thinner than the lash line is noted, not a pass.
2. **Face read, the main test:** at whole-head scale in the normal A1 views, held E1 against inlay + E1 must look
   visibly calmer and closer to the reference's soft dark eyes. If the only difference is in magnified crops, reject.
3. **No new artifact:** no eye surface showing outside the opening, no lash gap or floating lash, no crease or dent in
   clay at either view.
4. **Locality:** brows, hair, mouth, cheeks and forehead are vertex-identical to v012 in the tested assembly, and rig,
   actions and socket are held.
5. **Game scale:** at camp zoom 10 the eyes still read as two dark eyes.

## Stop rule

- ONE native test of this construction (with E1 colours and the flat control).
- If R1 still fails with flat eyes, or the whole-face read does not visibly improve, stop eye-construction work. Then
  the remaining eye gap is eye size and shape (the tall 1.5:1 opening and its placement). That is a likeness decision
  for the user at A1, not another construction cycle.
- If it passes, the next step is one production head version built as a local post-step on v012, with brows and hair
  frozen. The E1 texture's upper sclera would be adjusted then, as one value-only change: the pale-arc risk above.

## Files

All in `art_source/handoff/claude_production/ART-005/`:
- `face_method/inlay_method.patch`: the INLAY switch for stages 1 and 3, OFF by default.
- `face_method/run_inlay_demo.sh <absolute empty dir>`: scratch inlay build from the committed starter with the patched
  copy of the scripts and the pinned v012 settings; refuses a non-empty folder. Two runs gave identical meshes.
- `face_method/compose_inlay_demo.py`: the local review composite on v012.
- `face_method/rim_measure.py`: the measurement.
- `build_scripts/eye_boundary_diag.py`: the flat-eye and band diagnostics.
- `face_method/eye_inlay_method_demo.png`: the sheet.
