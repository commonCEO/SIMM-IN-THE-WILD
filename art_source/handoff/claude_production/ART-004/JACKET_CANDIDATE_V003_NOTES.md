# ART-004 jacket candidate v003: method A, seated cuffs

Status: delivered for Codex's native fit, built and shown with the held study candidates head v009 and collar v003
(their bytes unchanged). Answers the five points at `94cb54b`. Not a parity claim, not ready_for_user_review, not
for playable integration.

## Files

| Path | Purpose |
|---|---|
| `jacket_candidate_v003.glb` | For Codex. `SCULPT_JACKET` and `SCULPT_JACKET_TRIM`, skinned to a rest copy of the 17-bone skeleton (`SimmRigRestCopy`). No animation, camera or light. sha256 `e53ebe5db9aee66f2180849e8b4215da4ac0c1344a2af8af071ec1d17d4dfcd3`, 478,708 bytes. |
| `jacket_candidate_v003_vertex_map.json` | Per part: original vertex index, original position, candidate position. sha256 `fdd7d287189dfb184098cf37226a33b81b468fa03885b82ce4637b3740c39599`. |
| `renders/jacket_v003_before_after_clips.png` | Reference camera and side, idle 0, walk 25 and 75, gather 50 percent. Top: frozen body; bottom: v003. Both with head v009 and collar v003. |
| `renders/jacket_v003_before_after_rest.png` | Front, side, back, reference camera at rest, before and after. |
| `renders/jacket_v003_close_gather_hand_and_cuffs.png` | Left: gather at 50 percent, close on the right hip where v002 met the hand. Middle and right: cuffs close at rest. |
| `renders/jacket_v003_colour_ref.png`, `_alt.png`, `_clay_ref.png`, `_clay_alt.png` | Full figure at the two agreed cameras. Blender Cycles, review only. |
| `build_scripts/jacket_build.py` | Now v003 (v002 at `c1cd411`). Built on `work/fit_base_v009_c003.blend`: head v009's file with the collar v003 parts appended, not committed, rebuilt by `hair8/combine.py`-style append. |
| `build_scripts/jacket_export_check.py` | Hand test rewritten (point 4); `SAMPLES` sets samples per clip. |

Replace in the in-memory study exactly as for v002: hide `Simm golden canvas jacket.001` and `Simm golden seam
binding.001`, add the two parts on the live skeleton, keep the frozen button.

## The five points

1. **Hem, method A.** Not lowered: lowest point Z 0.582, the original hem height. Exact original weights. No
   vents: the side rise is capped at 10 mm and is a curve. In `gather` the clip presses the right hand into the
   hip (the frozen trousers themselves take up to 4.4 mm of hand there, measured on the original body), and the
   rounded hem bulged 1 to 2 cm further out at that spot than the original jacket, which never met the hand. Only
   the 23 hem vertices within 8 mm of the hand's measured path, and their neighbours within 30 mm (63 vertices in
   all), are blended back to their original positions. The rest of the torso keeps its v002 volume.
2. **Cuffs.** The two cuff rings are at their original positions, unmoved: centre (+-0.25, -0.008, 0.650), radius
   40.7 to 53.2 mm, Z 0.644 to 0.655. The last 35 mm of each sleeve is drawn to 2.5 mm larger than the ring's inner
   radius, and its end row sits in the middle of the roll, so the sleeve edge runs into the roll. No flare.
3. **Front edge and button.** As v002: soft front rolls from the original placket strips, the frozen button seated
   1.9 to 2.9 mm off the roll.
4. **Hand contact, hand triangles only.** 636 triangles whose every vertex is over 50 percent on `hand_l` or
   `hand_r`; 116 other warm-skin faces excluded. A cloth vertex counts when it is more than 1 mm behind the nearest
   hand surface and a ray from it crosses the hand surface an odd number of times. Result for both parts:
   **0 vertices in a hand in idle, walk and gather, at 25 samples per clip and again at 97 samples per clip.**
   Before the local blend, the same test found 4 jacket vertices (original IDs 3347, 3384, 3976, 4013), up to
   5.3 mm, in `gather` frames 7 to 17, all 100 percent `hips`, at X -0.18 to -0.19, Y -0.05, Z 0.596 to 0.608.
   The close frame shows that spot now. The earlier "inside" and ray counts that I discarded are not used here.
5. **Accounting.** Re-imported GLB: 2,778 of 2,778 and 2,828 of 2,828 vertices matched to source vertices within
   20 micrometres, 0 unmatched, all 2,074 and 1,644 source vertices covered, largest weight difference 0.0000000.
   17 bones, names and parents match, largest rest joint difference 0.0000007 m, no animation.
   `verify_candidate.py`: `FROZEN_ALL_UNCHANGED True` (body, old head, rest matrices, socket, actions).

## Part manifest

| Object | Source verts | In the GLB | Tris | Bounds, Blender axes, metres |
|---|---|---|---|---|
| `SCULPT_JACKET` | 2,074 (all of the original jacket) | 2,778 | 4,136 | X -0.301..0.301, Y -0.137..0.140, Z 0.582..0.974 |
| `SCULPT_JACKET_TRIM` | 1,644 of the original binding's 1,848 | 2,828 | 3,240 | X -0.300..0.300, Y -0.141..0.045, Z 0.595..0.965 |

Materials and colours as v002. Moved: jacket up to 48.4 mm (mean 7.9 mm); trim up to 25.0 mm (mean 1.3 mm: the
cuff rings do not move, the front rolls do).

## Known issues

- At each cuff a small fold shows on the sleeve just above the roll (close frame, left), where the last 35 mm of
  the sleeve is drawn in. Worth checking natively.
- The cuff roll is the original binding's size, about 6 mm thick: modest at game distance, thin up close.
- Strap gap unchanged from v002: up to 12.9 mm, mean 6.1 mm.
- Jacket length: now the original 0.58 m, shorter than the reference's 0.47 to 0.50 m. Not solved; to be judged
  with the whole silhouette before A1. Boots not started.
- Samples, not continuous motion: 97 per clip is dense, not a proof.

## Collar seating, proposal only (collar v003 not edited)

Problem from your native side view: the bunch behind the neck sits as a separate yellow lump over the pack, with a
visible gap under the hood instead of cloth running down into the jacket.

Proposal for a later, separate collar packet:
- Remove the separate back bunch. Its volume moves into the stand itself: the back of the stand gets 6 to 8 mm
  thicker with two soft folds.
- Seat the base on the jacket: for each direction round the neck, the stand's lower edge is set to the height of
  the jacket v003 surface at that radius (found by a ray down onto `SCULPT_JACKET`, plus the pack top where it is
  higher), and the stand gets a 6 to 8 mm skirt that goes into the jacket, so there is no visible gap from any angle.
  The pack is not changed; where the pack top is higher than the jacket, the base sits on the pack.
- Binding unchanged: 100 percent `chest`, which the jacket's shoulder and back vertices also follow, so the
  junction moves together in the clips.
- Checks: the same 39-pose clearance to jaw, nape and hair, plus a gap measurement between the stand's base and
  the jacket over the clips.
