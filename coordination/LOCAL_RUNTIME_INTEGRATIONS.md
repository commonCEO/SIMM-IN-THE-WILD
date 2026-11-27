# Local runtime integration register

Codex-owned. This records intentional tested local changes while broad source publication (PROD-002) remains blocked pending explicit approval. It is not a source export or art approval.

##27November2026 — current camp camera far plane

- File: godot/scripts/camp.gd, camera construction; camera depth default64m plus two comments only. Original angle, offset, zoom, lights/assets/state/save schema retained. Applies to new instances; no live game restart.
- Before SHA256: a7870da5272e5647dee8b5c45308a70421aab5a9626fcf6612c961567b0f574e.
- After SHA256: b981524d90ebc795d92ea174c574d4416e9f95bb510de0360ade9841ebe27a10.
- Current expected41file baseline: work/simm-runtime-baseline-camera64.json. Original work/simm-head-baseline.json stays unchanged and intentionally differs for camp.gd only; remaining40files unchanged.
- Local record: work/camera64-integration/record.json; pre-edit source backup camp.before.gd in that directory. Never publish the backup/native saves or overwrite later local edits with it. Rollback requires an inverse camera-only patch after checking current content/hash, preserving subsequent work.
- Evidence: native matched day/wide-day/torch controls at far4000/64/96; six static bounding probes max45.197m; post-change default64assertion and360manual physics steps/26coverage checkpoints with actual displacement, fixed camera basis and cave enter/leave. persist=false before scene entry; real save not accessed.
- Limits: current40m prototype, synthetic inventory, mapped action injection rather than physical controller; animations disabled in travel study; labels/particles/MultiMesh/future campaign and full performance not covered. Existing cave ground-edge/portal occlusion not fixed. Full proof/details in latest codex_deliveries.md.

Original rig/rest/actions/socket and runtime art remain unchanged. Fitted Simm candidates are still study-only; A1 unpassed.
