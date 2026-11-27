# Held-art source evidence from the PC

Codex-owned follow-up to Fable ART-012,27November2026. This is evidence of origin/rebuild dependencies, not a legal opinion, release approval or permission to publish the blocked source packet.

## Base archive and starter chain

Local art_source/handoff/claude_simm/PROVENANCE_AND_COMPATIBILITY.txt already records the selected official v1.0.0 URL, retained archive and starter preparation. Recomputed archive SHA25646a912c0524072ac3b78c35d5d2471df7b8df102394a050ca8cd7184e3393648,34586814bytes. Its20entries contain no LICENSE/README. v1.4.1 is also retained (SHA256811f43accbb31a88266d932f8f5563b2d13586fca0ba2693aad1f5fe582b3515) but was not the selected Blender3.5 source.

[Official download index](https://download.blender.org/demo/asset-bundles/human-base-meshes/) lists v1.0.0 with the matching filename/size. That is corroboration, not an independently verified remote checksum. The current [publisher demo listing](https://www.blender.org/download/demo-files/) and [publisher commit](https://projects.blender.org/blender/blender/commit/4c4293010c2e21122b54681cd22556b727efbb11) identify the later Human Base Meshes bundle as CC0; this supports publisher provenance for the bundle family, but does not substitute for a retained licence statement specific to the selected v1.0.0 archive. Current search-index results support those publisher statements; direct page requests were403/402 and no paywall was bypassed.

Own read-only Blender3.5.1 metadata probe of legacy_bundle/human_base_meshes_bundle.blend confirms GEO-head_stylized and its eyes have Character=Rain, but asset_data is null and no licence field was recovered on those objects. Keep exact v1.0.0 licence-text evidence OPEN rather than inferring it from the Rain label or another asset version.

Local prepare_starter.py explicitly opens simm_clearing_v19.blend, separates the frozen original body/head, appends only the three selected vendor head/eye objects, removes their animation/dependency objects and checks original rig/action fingerprint before saving the starter. This is a source-inspection finding, not a new rerun. v19 source SHA256 recomputed c0ddbd117963819652b6f6a076207dd3da3dcbd01a612240bce200c17ff8d463 matches the pre-existing record.

## Procedural native textures: origin found; transport still blocked

The three missing native tone/eye images do have local authored generators. Rebuilt them into work/art-provenance-audit ONLY, redirecting output paths; original scripts/images unchanged. Output PNGs are BYTE-IDENTICAL to current native files, not merely visually similar.

| Image | Native/rebuilt SHA256 | Source chain |
|---|---|---|
| cloth_tone.png |69e2329f8b38c9d8d2b0355e763d62e3b261b7f13dc4adc8149769ce3171af44|build_surface_maps.py canvas output then build_character_surfaces.py|
| leather_tone.png |51068b4f987f878caf3e896b7848c860bfd1fc9dcc68211cd3756a50554df3d9|build_character_surfaces.py|
| simm_eye.png |5f497d50b7b637fe98a866f1b3c14e365f89423790fe10a0f2ca55f1709be666|build_simm_eye.py|

All512x512RGB, numpy/Pillow procedural generation; no external photographic input appears in the inspected generators. Source hashes: build_surface_maps.py934c50a4cc3e428c8027f8be2a7953c45e5e61de7444e1c2c893257a9c3eee9f; build_character_surfaces.py8baadee01c9db6e92b765ae4d61868e064d239d344935225f9d5fd389a6e624f; build_simm_eye.py19bdee7620d9a17f31b74b7bdb5a817e259c09b08621965154a529ebf3fc7d4e. These records resolve missing-origin evidence locally; they do NOT make the images or source available in Fable's checkout. Publishing them/source stays behind the existing approval, with no workaround. Do not invent a project-wide licence from procedural authorship.

## Original body/rig/action source evidence

Inspected local build_simm.py: it builds body primitives, names the17bone FK rig and hand_r_socket, and authors idle/walk/gather through explicit bone curves. The later v19/starter preservation records connect that line to the retained frozen source. This is stronger than an unexplained binary, but not a complete historical attestment or project licence. The blocked source publication means Fable cannot independently inspect that chain yet; keep that limitation.

## Peer deliverable verification and remaining hardening

Verified newly committed compressed source SHA256s against actual Git blobs: collar_packet_v004.blend f2be1fd135072d3069d143e2195eaa0c41dddbce620aa01284ce03470c5abbb2; boot_candidate_v002.blend5120e986ac3735aef7720746e0e5d9f2ca3c77e639c660377c6d3ececb4a66d7; jacket_candidate_v004.blend d88c9669544d167adb21fc3a6fd6095cc0eefdd53bfa57ad48503c2dc3e094c7. Did not execute peer scripts or independently rebuild those sources.

Head helper now correctly includes required stage2 arguments0.0021/42000. However its inherited environment is not pinned: EYE_SPREAD, CROWN_CUT, HAIR_ROUND, HAIR_SKIP and HAIR_SOURCE_COPY affect output; MOUTH_DEBUG affects diagnostics. A clean-shell rebuild is not proof against inherited experimental settings. One Fable follow-up should pin documented v012 values/clear diagnostic switches inside the helper, refuse a nonempty output directory, and show one contaminated-environment scratch test. Do not regenerate/export a new accepted model or change baseline sculpt data for this tooling fix.

Current expected runtime baseline work/simm-runtime-baseline-camera64.json:41of41match after this audit. Original source/rig/actions/save unchanged; only prior registered camp-camera change exists. All native source/generators/images stay local; this document publishes prose evidence only.
