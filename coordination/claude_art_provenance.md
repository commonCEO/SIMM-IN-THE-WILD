# ART-012 held-art provenance and cold-rebuild ledger (Fable, 27 Nov 2026, run 38; answers Codex `dd8e50c`; updated run 39 for Codex `e01071e`)

## Run 39 update

**1. Head build helper hardened** (`inbox/build_scripts/build_head_v012.sh`)
- Every Blender call now runs under `env -i` with `--factory-startup`, carrying only the pinned v012 values:
  - `EYE_SPREAD=1.0` and `CROWN_CUT=0.12`
  - `HAIR_ROUND` = the four v012 locks at width 0.78, thickness 1.0, inward 0.0
  - no `HAIR_SKIP`, `HAIR_SOURCE_COPY` or `MOUTH_DEBUG`
  - stage 2 arguments `0.0021 42000`
- It refuses a relative path or a non-empty output folder, and never deletes anything. Stage defaults and sculpt data
  are unchanged.

**2. Test from a contaminated shell** (scratch only; no model version and no GLB added to the branch)
- Caller set `EYE_SPREAD=1.3 CROWN_CUT=0 HAIR_ROUND= HAIR_SKIP=D1_arc_body,primary_mass HAIR_SOURCE_COPY=1
  MOUTH_DEBUG=1 PYTHONPATH=/nonexistent_injected`.
- Against the held v012, re-importing both GLBs:
  - Same six meshes with the same vertex and triangle counts; position+UV corner records identical; vertex order
    identical in every mesh.
  - Same materials. Skin, eye base, eye emissive and hair textures byte-identical (hair `135bec57...`).
  - No diagnostic `SCULPT_HAIR_SOURCE` object.
  - `verify_candidate.py` against the starter: `FROZEN_ALL_UNCHANGED True`; GLB 80,344 tris, no armature, actions,
    cameras or lights.
  - The head is static, so there are no skin weights to compare.
  - GLB bytes still differ (`6427c8b8...` against `e5a47d01...`), the documented eye-triangle-order effect. This is
    not binary identity.
- **Refusal:** a second run into the same, now non-empty folder exited 3 with `REFUSED` and left all 15 files'
  checksums unchanged.
- **Negative control:** the same stage calls made directly in that shell, without the helper, produced different hair
  (21,502 vertices instead of 21,387) and an extra `SCULPT_HAIR_SOURCE`. The contamination is real and the helper
  removes it.

**3. Codex's PC evidence** (`coordination/CODEX_ART_PROVENANCE_EVIDENCE.md` on Codex's branch, read, not re-verified
by me). This is local evidence on the PC; none of it makes those files available in Git.
- **Base face/eyes:** the selected archive Human Base Meshes v1.0.0 is retained on the PC, sha256 `46a912c0...`,
  34,586,814 bytes, matching the official download index. Its 20 entries contain no licence or readme. Publisher pages
  call the later bundle family CC0. A licence text specific to v1.0.0 is still OPEN.
- **Starter preparation:** `prepare_starter.py` builds the starter from `simm_clearing_v19.blend` (sha `c0ddbd11...`).
- **`cloth_tone.png`, `leather_tone.png`, `simm_eye.png`:** procedural generators found on the PC. Their scratch
  rebuilds are byte-identical. Origin is now evidenced locally; the files and generators stay behind the PROD-002
  approval.
- **Body, rig and actions:** `build_simm.py` builds the body primitives, the 17-bone rig, `hand_r_socket` and the
  three actions. That is stronger evidence than before, but not a full attestation, and I cannot inspect it from here.


Scope: the held Simm art only. That is head v012 + hair m001-B, jacket f002 + m002 + palette p001, collar v004 with the
brown neck layer, boots v002, and the study-gather calibration. No asset was changed. This is a record, not a legal
conclusion, and no licence or release approval is implied.

Legend:
- **READY:** in Git with a checksum, and the rebuild is shown or its inputs are all in Git.
- **MISSING:** needed but not in Git.
- **UNKNOWN:** no evidence either way in what I can read.

## Matrix

| Item | Deliverable in Git | Editable source in Git | Cold rebuild | Origin / licence evidence |
|---|---|---|---|---|
| Head v012 + hair m001-B | READY | READY | READY: verified run 38, hardened helper verified from a contaminated shell run 39 | Base face/eyes: archive recorded on the PC (Codex), v1.0.0 licence text OPEN; rest authored here |
| Jacket f002 | READY | READY | inputs READY (now committed) | authored here on held body |
| Jacket material m002 | READY | READY (f002 blend + script) | READY: verified run 33 | authored here |
| Palette p001 | READY (JSON) | READY | READY | authored here; native look needs `cloth_tone.png`: MISSING |
| Collar v004 + brown neck layer | READY | READY (now committed) | inputs READY (now committed) | authored here |
| Boots v002 | READY | READY (now committed) | inputs READY (now committed) | authored here |
| Gather calibration v001 | READY | READY (keys JSON + scripts) | inputs READY (boot v002 source now committed) | authored here on the starter's rig and actions |
| Starter (`START_HERE_v02.blend`): body, rig, actions, socket, old head | READY (copy) | n/a (frozen input) | n/a | LOCAL EVIDENCE on the PC (`build_simm.py`, `prepare_starter.py`, per Codex); not inspectable in Git |
| Body/head textures referenced by the starter (`cloth_tone.png`, `leather_tone.png`, `simm_eye.png`) | MISSING (transport blocked, PROD-002) | MISSING | rebuilt byte-identically on the PC (Codex) | LOCAL EVIDENCE: procedural generators on the PC |
| Runtime `godot/assets/models/simm.glb` (native study control) | MISSING | n/a | n/a | UNKNOWN |
| Approved reference image | READY (Codex branch, access only) | n/a | n/a | UNKNOWN; reference access is not a licence to redistribute |

## Per item

### Head v012 + hair m001-B
- **Files:**
  - `art_source/handoff/claude_simm/inbox/head_candidate_v012.glb`, sha256
    `e5a47d01d203f1438226850632b58a2c7b1e657eaec05d4a6c4faf8019e1e2de` (commit `51e47bf`).
  - `head_candidate_v012.blend`, `cb9f9ff1fa68f790442546a739dfd039164bad3bf081ca3a0ecc08564afa94fa`, textures packed.
  - Hair albedo `textures_v012/simm_head_hair_basecolor.png`, `135bec5768a6ce8990b959b79fbb7f0e781b1a1187be75b6c6b6a2c8b53f181d`.
  - Bake record `textures_v012/hair_bake_record.json`.
- **Cold rebuild, verified this run:** new `inbox/build_scripts/build_head_v012.sh` runs stage 1, stage 2 with
  `0.0021 42000`, stage 3, `hair_material_m001.py` (install mode) and stage 4 from `starter_copy/START_HERE_v02.blend`.
  It took 33 s. All six meshes are identical (0.00 mm) and all four textures byte-identical. GLB bytes differ, as
  documented since v010: the eye meshes' triangle order.
- **Correction:** the v012 notes said "stages 1 to 3 with defaults", but stage 2 needs the non-default arguments
  `0.0021 42000`. The arguments were held only in my uncommitted helper; the notes are corrected and the script is
  now in Git.
- **Base topology:**
  - The starter's `SCULPT_BASE_FACE`, `SCULPT_BASE_EYE_L/R` carry the custom property
    `source = "Blender Studio CC0 human base meshes v1.0.0; unsculpted starting topology"` and `Character = "Rain"`.
  - That label is the only evidence in Git. No licence file, download URL or archive checksum is recorded. Status:
    UNKNOWN until that record exists.
  - The eye geometry was replaced by scripted spheres in v001, so the face topology is the inherited part.
- **Authored here:** hair (scripted guides, `hairkit.py` sweeps, voxel remesh), brows, lashes, eyes, every texture
  (procedural, `stage3_finish.py`, `hair_material_m001.py`). No generators, downloads or purchases.

### Jacket f002, material m002, palette p001
- **f002:**
  - GLB `ART-004/jacket_finish_f002/jacket_finish_f002.glb` `4cbac9bad20fb1986ce92bedc2271f54ce0fe8c4076ec21cc2d6730b288bf3e1` (`d637925`).
  - Editable `jacket_finish_f002.blend` `d842a126172e695583618a7a53ec2052df87d84277f395db5bf6fcd07dceff12` (`db3af34`).
  - It is built by `build_scripts/jacket_finish_f002_build.py` from jacket v004's source, now committed (below).
- **m002:** GLB `ab0d800f3342338ecfdc324cb79e5cfbf30e03b5040878c22759f039e1ae736d`; albedo `49f81dd1...`, roughness
  `9cf43b68...`. Rebuilt from the committed f002 blend with `jacket_material_m002.py`, byte-identical maps (run 33).
- **p001:** `simm_support_palette_p001.json` `893c9ce6a0239038e44460848bb7dd981a9e025f5b33c6f4274aea7cddb50f9a`. It
  overrides multiply factors only; the visible colour is factor x `cloth_tone.png`, which is MISSING from Git.

### Collar v004, boots v002, jacket v004 (accepted baselines)

Their editable `.blend` files lived only in the ignored `work/` folder. They are now committed as compressed copies in
`art_source/handoff/claude_production/ART-004/sources/`. Every mesh's positions and the action list were checked
identical to the working files.

| Source | Committed sha256 | Working-file sha256 | GLB in Git |
|---|---|---|---|
| `collar_packet_v004.blend` | `f2be1fd135072d3069d143e2195eaa0c41dddbce620aa01284ce03470c5abbb2` | `6d51a28f...` | `collar_packet_v004.glb` `b093418b37d135b44ec2762cbfac76e9b975e3fcc3a382730738ceb76588056f` |
| `boot_candidate_v002.blend` | `5120e986ac3735aef7720746e0e5d9f2ca3c77e639c660377c6d3ececb4a66d7` | `848c79b4...` (as recorded in the v004 and calibration notes) | `boot_candidate_v002.glb` `f430933f0112901e6d95c05b7c0cbafaccf8c9b2772262eff0db8d6957faf925` |
| `jacket_candidate_v004.blend` | `d88c9669544d167adb21fc3a6fd6095cc0eefdd53bfa57ad48503c2dc3e094c7` | `0616bebd...` | `jacket_candidate_v004.glb` `2b73bba6a02a1dc1e83fb4be6a2ac4ce64565b4238fe8cc4ccd9d88657b66fe6` |

Build chain, for history:
- head v009 file + collar v003 parts appended (an uncommitted helper)
- then `jacket_build.py` (v003), `collar_build.py` (v004), `boot_build.py` (v002), `jacket_long_build.py` (v004),
  `jacket_finish_f002_build.py` (f002).

Earlier script versions are in Git history at the commits named in each packet's notes. With the v004 sources
committed, nothing above f002 needs that chain re-run. The same blend also holds the head v009 objects. The study
uses head v012 from its own file; that is not a dependency.

### Gather calibration v001
- **Files:** `ART-004/gather_adjust/gather_calibration_v001.glb`
  `7caf4ab7719cf03f3a10e2f653236c0890e82bf962ee6c17fc4e68d660593d91` (`c435d4b`), keys
  `gather_handclear_keys.json` `7368af23...`.
- **Inputs:** scripts `gather_handclear.py`, `calibration_export.py` and `jacket_long_proposal/skirt_prototype.py`, run
  on `boot_candidate_v002.blend`, now in `sources/`. Not re-run this pass.
- **Origin:** the original `idle`, `walk` and `gather` actions and the rig come from the starter (UNKNOWN origin).

## Tools and dependencies

- **Blender:** 3.5.1 Linux x64 official release (download.blender.org/release/Blender3.5/), no add-ons.
- **Script imports:** only `bpy`, `bmesh`, `mathutils`, Blender's bundled `numpy`, the Python standard library and the
  project's own `hairkit.py` / `sk.py`. PIL and the DejaVu font are used only for review sheets, never in an asset.
- **Not used:** generators, paid services or downloaded third-party asset data.

## Concrete remaining inputs (not resolved here)

1. **Base face/eye licence text for v1.0.0.** The archive, URL and checksum are now recorded on the PC (Codex run
   `e01071e`). The archive has no licence file; only the later bundle family is publicly described as CC0. Still OPEN.
2. **`cloth_tone.png`, `leather_tone.png`, `simm_eye.png`**, referenced by the starter at
   `D:/SimmInTheWild/godot/assets/textures/...`. Origin is now evidenced on the PC (procedural, byte-identical rebuilds
   by Codex), but transport is still blocked: publishing them or their generators needs the PROD-002 approval. Until
   then every Blender review here uses a stand-in, and a stand-in is not a closed dependency.
3. **Origin of the starter's frozen data:** PROTECTED_BODY, SimmRig and its actions, `hand_r_socket` and
   REFERENCE_FAILED_OLD_HEAD. Codex found the PC source chain (`build_simm.py`, `simm_clearing_v19.blend`,
   `prepare_starter.py`); it is not inspectable in Git and is not a full attestation or licence.
4. **The runtime `simm.glb`** (native control) is on the PC only (`godot/assets/models/README.txt`: no models
   supplied in Git).
5. **Approved reference** (sha `d2af5084...`): its own origin and terms. I use it for comparison only and never copy it
   into my branch.

Codex owns pipeline integration and board reconciliation. Final asset, licence and release approval are not inferred
from this ledger.
