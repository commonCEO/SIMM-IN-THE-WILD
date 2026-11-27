# SAVE-001: local compatibility audit

26November2026 Tallinn. Partial evidence, not complete campaign save certification.

## Isolation

Ran copied current progression/catalog sources and existing tests in
`work/save-audit-project`, a separate minimal Godot project named
`SIMM isolated save audit 20261126`. Its user data is separate from the playable
prototype. No native player save was read, copied, replaced or restored. No
game process was stopped/restarted. No save payload is in this report or Git.
Godot4.7.2 console, headless. Gameplay source unchanged.

## Actually executed

| Check | Result | Evidence / scope |
|---|---|---|
| progression_smoke.gd | PASS, exit0 | Recipe/station transactions, ownership, replacement save, legacyv1 and rejected invalid input |
| inventory_state.gd original | FAIL, exit1 | Line7 still expected37materials after approved bucket made38; it stopped before migration assertions |
| inventory_state.gd corrected | PASS, exit0 | Explicit38materials/bucket0, capacity/drop/transaction checks and v1/v2 migrations |
| nups_save.gd | PASS, exit0;129checks | v4companion roundtrip, legacy missing fields, scene/wait/work state and transactional invalid-load rejection |
| bucket_recipe.gd | PASS, exit0 | Recipe/stock/workbench transaction and bucket save/load |

Local logs: work/save-audit-progression.log, save-audit-inventory.log,
save-audit-inventory-fixed.log, save-audit-nups.log, save-audit-bucket.log.
The corrected test's printed37-item label was also changed to38after the
successful rerun; this wording-only change was not rerun. The successful log
therefore contains the old label. No test result is inferred from exit alone.

Only test code changed: godot/tests/inventory_state.gd now expects the explicit
37browser materials plus bucket, asserts bucket starts0, and fixes its label.
This is a stale test correction, not a save-schema/gameplay change.
Test source publication remains covered by the pending broader source-export
approval; this report publishes evidence only, not the source patch.

## Compatibility matrix

| Input | Status | Boundary |
|---|---|---|
| v1material/tool saves | Tested by progression and inventory checks | Sparse legacy inventory defaults, ownership and quantities retained |
| v2inventory/drop/state | Tested by inventory check | Explicit use/drop/recovery and invalid-drop transactional handling |
| v3skills/gear/world objects | Validator/loader reviewed only | Dedicated valid v3 ->v4 roundtrip remains TODO; do not call tested |
| v4without companion fields | Tested by129companion checks | Defaults do not recruit or replay rewards; clock derives from world_age |
| Currentv4bucket | Tested by bucket check | Roundtrip; older absent bucket accepted in validator, dedicated absence fixture still TODO |
| Browser0.6save import | NOT IMPLEMENTED | Distinct from preserving local Godot progress |
| Future versions / corrupt/truncated/oversize files | Partial code review only | Version1..4 and1MiB load limit; dedicated malformed-file suite still TODO |
| Filesystem failure/crash during temp write/rename | NOT TESTED | .tmp write/flush/rename code exists, but crash recovery/IO fault handling not certified |
| Native user's latest campaign save | NOT exercised here | No new proof about its current bytes or campaign-wide transitions |

## Read-path observations

progression.gd validates a full dictionary before assigning live fields.
Recognized versions are1through4; version-gated unknown/new fields reject.
Missing legacy fields get defaults. The bucket is optional for older saves;
other post-v1 material IDs are required. Data migrates in memory and save_game
emitsv4only on an explicit save. This audit did not change those rules.

The writer validates, writes path.tmp, flushes and renames. That is useful
structure, not proof of crash durability on every Windows failure mode.

## Next bounded work

1. Add synthetic validv3roundtrip and pre-bucketv4absence cases in the isolated
   harness; exact retained fields plus rejection must leave state unchanged.
2. Add truncated/oversize/future-schema and failed-write fixtures without
   accessing user data. Make harness fail on SCRIPT ERROR/assertion as well
   as nonzero exit; tests may otherwise stop before all checks run.
3. Run read-only real-save compatibility only on a fresh local backup when
   needed for an actual schema change; never publish or restore that fixture.
4. Campaign scene/player/quest/time migration remains downstream of those
   systems. SAVE-001 stays DOING, not DONE.

The immutable PROD-002 snapshot predates this test-only correction. If source
publication is approved, keep its provenance explicit and deliver the corrected
test separately only within that authorization; do not silently rewrite hashes.

## Follow-up: synthetic boundary suite,26November2026

Added a LOCAL-ONLY audit harness at
`work/save-audit-project/tests/migration_boundaries.gd`; production sources
were not changed. After correcting an audit-fixture typed-array assignment,
the suite completed295checks, failed=false, exit0. The initial setup attempt
timed out with exit2 before exercising migration; it was a harness error,
not a production-load failure. Final evidence: work/save-audit-boundaries.log.

Newly tested (supersedes the corresponding TODO rows above):

- Valid syntheticv3 with inventory/tools/crafting/skills/gear/XP/placed chest
  loads without changing any supplied field, writesv4only when explicitly
  saved to a separate target, reloads, and leaves originalv3file bytes intact.
- Pre-bucketv4 accepts absent bucket as0and retains all other item quantities.
- Truncated JSON, null, array root, over1MiB input and future schemav5reject;
  each rejection preserves every populated live-state field.
- Invalid live state cannot overwrite an existing good destination. A
  missing-parent write returns failure and preserves an existing valid file.
- User-data namespace was asserted separate from the playable prototype.
  The native player save was never opened or written.

The truncated-JSON case intentionally emits Godot's `Parse JSON failed`
diagnostic; this is expected evidence of the exercised invalid input, not a
clean-log claim. Final run had no SCRIPT ERROR or failed assertion. Checks
use explicit failure accounting; exit code alone is not sufficient evidence.

Still untested: real OS crash/power interruption during flush/rename,
recovery of leftover.tmp files, permissions/disk-full faults, browser import,
and full campaign-scene migration. No guarantee of those behaviors is made.
The audit project is isolated and source-only publication remains pending
approval; no test code or save fixture was added to the remote branch.


## Real Windows destination-lock fault —27November2026,15:00UTC

Exercised the CURRENT production Progression.load_game/save_game code with explicit absolute SYNTHETIC paths under work/save-rename-lock-study/. No user:// path or native player save read/write. The full v4 fixture is the previously generated test document, not a copy of player progress.

A parent PowerShell .NET FileStream held the existing fixture open with FileShare.ReadWrite but without delete sharing. This permits reads/writes while blocking destination replacement. Under that real OS lock, the native serializer wrote/flushed its complete temporary candidate (wood53) but DirAccess.rename_absolute returned FAILED(1). Eight checks passed: destination SHA256 stayed exactly30ada6a946a89a1556d9de56e46886bf2a0d589df31e1b186f9e8180c894bc4d, a fresh loader still read original wood37, in-memory wood53 was preserved, and the leftover.tmp validated as the intended full v4 candidate.

After the parent released its own lock in finally, a fresh invocation changed the synthetic desired state to wood57 and called the actual save path again.76checks passed: replacement returnedOK, .tmp was consumed, a fresh loader read57 rather than stale staged53, complete schema validated and all other populated fixture fields/ingredients were preserved. Setup1 +locked8 +retry76 =85checks; all three native runs exited0 with explicit failure flagsfalse.

This is real Windows replacement-lock failure/retry evidence for CURRENT v4 saving, not an injected fake return code. It closes one concrete OS-fault case. It does NOT establish v5 migration atomicity, crash/power-loss durability, disk-full/ACL behavior, automatic recovery/promotion of leftovers, multi-process race safety or full campaign migration. Retry regenerates the temporary state through save_game; no automatic stale.tmp promotion was implemented or claimed.

Local script work/save-rename-lock-study.gd, per-phase own logs and synthetic manifests/result JSONs under work/save-rename-lock-study/. Native certificate-store diagnostic persists; no clean-log claim. All test code/fixtures remain local behind PROD-002; only these owned findings published. Runtime source, art, rig, live game and native save untouched.


## Populated collection compatibility —27November,16:00UTC

131checks PASS on one synthetic rich-v4 actual-load/actual-save ->work-only proposed-v5 envelope/JSON roundtrip fixture. Covers6station/storage/garden/nest objects,3drops including both scenes and absent legacy source_scene,3resource states,6wildlife types,13skills,4gear flags, bow stats and companion/effect clocks. All existing fields/optional absence preserved; only proposed calendar defaults added. Current loader's future-v5 rejection preserves the complete populated in-memory v4 state, and original input bytes remain unchanged.

Eleven malformed nested variants reject without mutation. See CORE-001-CONTRACT.md for precise scope. This supplements the previous sparse fixtures; not exhaustive schema fuzzing, earned-game legality or production migration. Workspace-only files, native save untouched, no runtime version change. Root-certificate-store error remains. All new code/data stay local behind PROD-002.
