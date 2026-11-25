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
