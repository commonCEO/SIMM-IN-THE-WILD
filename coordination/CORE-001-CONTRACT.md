# CORE-001: isolated clock/survival/migration contract

Owner Codex. First bounded implementation preparation,26November2026,23:01UTC.
Status DOING: local prototype only, not integrated into the live camp or save loader.
Source of truth: browser model.js advanceTime and game.js frame/update/sleepUntilMorning/updateDeath; existing native progression.gd validation/loading and camp tick.

## Calendar and active time

Calendar day begins at1; time is seconds within[0,360). Daylight is time<300, night time>=300. advanceTime increments worldAge and time by active delta, wraps all complete360s days and reduces hunger by0.045*delta with a zero floor. Calendar hunger and world-age arithmetic can be tested independently of rendering.

Browser frame caps delta at0.05s and does not accumulate wall-clock catch-up when hidden or paused. Its frame gate prevents ordinary update while menus are paused. An imported save does not simulate the hours the application was closed. Preserve these timing domains explicitly; do not infer calendar day from worldAge, which also advances differently under rest.

The native world_age increment must have exactly ONE owner after integration. Existing camp._tick_inventory_state currently owns it; adding a calendar module without removing/delegating that increment would double crop/regrowth/companion time. Drops currently use remaining lifetime rather than browser absolute expiry. The clock prototype deliberately does not tick drops, effects, fuel, crops or Nups; their integration order and one-tick ownership need explicit tests.

## Events versus the pure model

advanceTime itself does not award survived nights or XP. game.update performs transitions using the pre-step night flag: entering night spawns zombies; dawn removes them, increments nightsSurvived and awards20XP. Browser normal frames are capped, so this transition code is not a generic multi-day bulk reward API.

The prototype's large-delta cases validate ONLY the pure calendar/hunger model. They must not be interpreted as permission to award hundreds of nights/XP on load or a bulk delta. Add short-step dawn/dusk event fixtures before wiring live rewards.

## Rest and defeat differ

sleepUntilMorning advances worldAge by360-current time, increments day, resets time0, increments nightsSurvived, restores maximum health and floors hunger at25/thirst at50. It clears zombies, checks house completion and regrowth, then saves. It does not use hunger drain over the skipped interval and does not explicitly grant the natural-dawn20XP. Camp tent and bed use this same browser function.

Defeat is a separate transient overlay: restore ONCE at1s and finish at2.7s. Restore returns to base, exits cave/interior/boat, restores max health/hunger100/thirst100, increments day and sets time0, clears zombies and resets hostile homes with12active seconds of calm, then gives3s invulnerability and moves the companion context. It does NOT explicitly advance worldAge to dawn or increment nightsSurvived. Heat is not reset there. Do not implement sleep by calling defeat, or vice versa.

Animation/death elapsed time is not the ordinary calendar. Browser tickEffects still runs through the death update path; ordinary world/calendar advance is skipped by the death branch. Implement and test that distinction before changing native damage_player's current instant full recovery.

## Survival to implement after calendar primitives

Starvation accumulates while hunger<=0 and damages when its accumulator is strictly>15s, resetting it; not >=15. Desert heat rises2/s and thirst drains0.8/s, oasis proximity restores thirst8/s; outside desert heat falls3/s. At zero thirst, heat damage accumulator triggers strictly>8s. Existing guardian invulnerability, damage-source sharing and defeat cancellation must remain consistent.

These rates are source-inspected requirements, not implemented or passed by the first clock prototype. Region-aware desert behavior depends CORE-005; do not invent the full world while building the local clock foundation.

## Native legacy state and tentative version5 fields

Current loader supports native schema versions1through4, with strict unknown-field rejection. Additive proposed calendar fields are day, time and nights_survived under version5; preserve world_age, hunger, inventory/tools/crafted, drops, resources/wildlife and all Nups fields.

Conservative legacy policy: versions1..4 lacked calendar history. Initialize day1/time0/nights0 while preserving stored world_age and current health/hunger/thirst/etc. Do not derive retroactive nights, rewards, starvation or calendar progress from accumulated world_age. Existing loader defaults for missing world_age0 and hunger100 remain. This policy is tested only at the clock-field transformation level so far.

Complete old-schema validation must happen BEFORE transformation. Validate the entire proposed new document BEFORE mutating live state or committing a file. The local clock-only transform is not a permissive replacement for progression.gd._valid_save. Its small synthetic dictionaries are not full legacy save fixtures. Preserve support for valid nativev1/v2 as well asv3/v4 when updating the complete loader.

A proposed version5 calendar field must be finite, integral where appropriate, and in a sensible documented range. time must remain[0,360). Unknown/future/corrupt files must fail transactionally. Retain atomic temporary-write/rename and original bytes on failure; no auto-rewrite merely because a file was read.

## Current evidence, honestly bounded

A read-only Node exporter executes CURRENT browser advanceTime over336cases (days1/3, four times around dusk/dawn, two world ages, three hunger levels and seven deltas including0.05s and multi-wrap). It records browser source hashes. Local Godot pure prototype matches calendar/day/world_age/hunger fields, verifies pause/invalid delta atomicity, clock-only legacy defaults/preserved fields and idempotence.

Final local native run PASS2382assertions, exit0. Root-certificate-store error remains; not a clean-log pass. No actual save loader/file migration, night reward, sleep, defeat, starvation, desert hazard or native scene integration was exercised. Runtime41file baseline unchanged and native player save never opened/written.

Prototype, oracle and harness remain under work/core001/ only. Only this prose contract/receipt is published while PROD-002 source export approval is pending. No source-export workaround.

## Next bounded pull and fences

Next: extend the isolated harness with source-derived sleep/defeat and short-step dawn/dusk event oracles; build a complete cloned-state migration fixture path around the existing native validator. Keep all code/data under an isolated work project until reviewed. Then integrate once with explicit clock/tick ownership and meaningful pause/save/defeat checks, preserving latest native save.

User-approved manual evening test controls must not be silently removed or used as an alternate untested calendar/reward source. Resolve their debug-versus-calendar integration in a concrete review before live wiring. No rig, animation, art, world layout or controller redesign belongs to this first clock task.

## Recovery prototype evidence — 26 November,23:58UTC

Advanced the work-only prototype with sleep and defeat state transitions. An independent Node VM executes the ACTUAL current browser sleepUntilMorning/updateDeath function declarations extracted from game.js, using original model.maxHealth/resetHostilesAfterDefeat. DOM, save, house-completion, regrowth, notification and companion callbacks are stubbed/counted; no browser app or native player save is loaded.

Oracle:288sleep combinations across calendar phase, hunger/thirst floors, combat/guardian/charm health capacity;16defeat scenarios with four boundary steps each. Final native PASS6768assertions over state fields, callback intentions, hostile-home/calm values, one-time restore and completion idempotence. Both functions preserve inventory/tools/XP and the distinct calendar/world-age/night semantics. Heat remains unchanged.

This is function-level evidence only. Direct large boundary steps are test inputs, not actual0.05s browser frame playback. The full update wrapper's effect/invulnerability ticking, input/charge cancellation, zombie spawning/clearing nodes, overlay rendering, physical base placement, actual home completion/regrowth/Nups movement and real file saving are NOT validated by stub callback counts. A return value describing intended work is not a world integration.

Native exit0; root-certificate-store error remains, no script/assertion failures. All41runtime baseline hashes unchanged, no live scene/save hook or new save version written. All source/oracles/harnesses remain under work/core001/; only prose contract/board/receipt published.

Next bounded foundation work: short-step dusk/dawn reward events and complete-schema legacy fixtures in an isolated cloned-state path. Then starvation/region hazards and one-tick world-age/effect/fuel/drop ownership before any live integration. CORE-001 is DOING, not browser survival complete.

## Short-step natural-night evidence — 27 November,01:00UTC

Actual game.update dusk/dawn slice plus original model.advanceTime/gainXP executed in independent VM at0.05s per step.33sequences /14658steps cover boundary starts near300/360, existing night counts and level/XP carry, including one continuous two-day sequence. Source hashes were verified current after native execution. Work-only native prototype PASS18097assertions over calendar/hunger/age, natural-night count,20XP/level/points and exact callback intentions. Night-entry spawn and dawn clear use stub zombie counts; no actual enemy-node construction/house/DOM integration.

A VM block-scope harness error and JSON numeric Dictionary comparison error were corrected before the final pass. A premature missing-oracle run was stopped through its own session only. Root-certificate-store error persists. Full update gates and effect timers, paused/death transitions, drop expiry, manual night-debug controls and one-tick fuel/world ownership are still outside this slice. Passing it does not authorize live reward hooks or demonstrate controller/campaign completion.

Next: complete-schema legacy fixtures around the original strict validator, then starvation/hazard and world-tick ownership checks before a single reviewed runtime integration. All source/data/harness files remain local in work/core001; no player-save read/write and all41runtime baseline files held.

## Complete-schema fixture evidence — 27 November,01:59UTC

442assertions PASS, native exit0. Actual current progression.gd._valid_save/load_game/save_game accepted constructed v1..v4 files under work/core001, normalized them to full v4 in a separate file, then a work-only transform added tentative v5 day1/time0/nights0. The proposed validator strips ONLY calendar keys and projects version4 through the original strict validator, in addition to validating every clock field. It is not wired to production.

Preserved every normalized field and original supplied progress, tested JSON roundtrip and unchanged original fixture hashes; rejected unknown/future/clock-injected legacy data and invalid v5 clock/nested inventory/progression values without mutating input. Distinct v4 world_age1234.5/companion_clock57.25 preserved; older loader defaults remain0. No retroactive day/reward history invented. Collections for resource/wildlife/drop payloads remain default-empty in these fixtures, so complete schema means full-document envelope coverage, not exhaustive nested content/campaign coverage.

Initial fixture StringName keys from dot assignment were corrected to explicit String keys; strict validation remains unchanged. Final logs retain root-certificate-store error. Runtime still accepts only1..4; no production v5 file/loader migration, atomic migration rollback or native player save touched. Next bounded foundation: survival/hazard source oracle and single world/effect/drop/fuel tick ownership, plus richer migration payload and OS fault cases before live integration. Source/data/harness files remain local while export approval is pending.

## Survival/damage slice evidence — 27 November,03:00UTC

Independent VM oracle uses actual desert/starvation source slices, original advanceTime, actual damagePlayer and the actual invulnerability decrement expression.155scenarios /5341steps; native work-only counterpart PASS85456assertions, exit0. Source hashes verified current. Tests cover heat/thirst bounds and oasis ordering, hunger crossing zero, strict>8/>15 thresholds, guardian/shared invulnerability, damage-attempt versus accepted damage, repeated active0.05s steps and stop-at-death intent. Region/oasis/death/DOM/sound/burst callbacks are stubs; full update and biome/volcano journey are not exercised.

Preserve source semantics: feeding/positive hunger does not reset starve; rehydration/leaving desert does not explicitly reset heatDamage. Threshold crossing resets an accumulator even if shared invulnerability suppresses damage. No offline catchup, automatic extra resets or immediate defeat recovery added.

An initial VM fixture omitted the game-initialized player position; corrected in the synthetic context. Native root-certificate-store error persists. No production code/save hooks, all41runtime baselines unchanged. Next bounded foundation is single world-age/effect/drop/fuel ownership and full pause/death wrapper semantics, before live wiring and production migration. Source/oracles/harness remain work-only while export approval is pending.

## Full-frame gating and ownership evidence — 27 November,03:58UTC

2496assertions PASS /exit0 from64actual-frame gate scenarios. VM executes current frame, update prefix/returns, original tickEffects/advanceTime and actual fuel statement; omitted gameplay body and callback stubs prevent a full-update claim. Covers first frame,50ms and14s-gap timestamps, all started/ready/paused/hidden/death/health gates; compares effects/jump/invulnerability, active age/calendar/hunger, drop identities/fuel and callback counts. Source hashes current; root-certificate-store error persists.

The OUTER frame suppresses update for pause/hidden/not-started/not-ready, so effects and invulnerability do not tick then. Active death runs the effect/invulnerability prefix then returns before world/calendar/drop/fuel. Do not extrapolate pause semantics from update's prefix without its caller. Long gaps cap active delta0.05; no offline catchup. Windows focus/visibility and Godot physics catchup remain unvalidated mappings.

Single-owner integration plan:
- One orchestrator owns active calendar/world_age/hunger advance; remove existing camp world_age+=delta at the integration site. Night-event and survival prototype helpers currently each advance for their independent tests; refactor into pre/post phases before combining, never call both advances.
- One effect/invulnerability prefix under the outer frame gate, including death but excluding pause. Remove/route old camp effect/invulnerability decrements so there is no duplicate.
- Fuel only under ordinary active-world gate; companion/wildlife/bow each tick once, retaining their distinct clocks/contracts.
- Browser absolute drop expiry versus native remaining lifetime needs an explicit adapter, preserving source_scene/IDs/content. Sleep worldAge skip expires old drops on next active browser step; effects/fuel do not retroactively drain. Defeat does not advance worldAge. Prior recovery field comparisons did not validate drop handling.
- Before live wiring: isolated combined-controller sequence with sleep/save/drop conversion and pause/death/clock transitions; then actual non-saving scene/controller checks and production version/migration fault path. Current tests do not install any of that behavior.

All41runtime baselines unchanged; no native player save read/write. Code/data remain work-only; source export approval is still pending.


## Recovery/drop lifetime adapter evidence —27November,12:00UTC

Work-only drop_clock_adapter.gd bridges fully validated native v4 remaining-lifetime entries to canonical absolute expiries. It does NOT advance time, own a frame tick, write a file or alter the production schema. A single caller-owned Clock.advance runs before strict expiry pruning. Native drop IDs/items/amounts/positions and optional source_scene survive unchanged; absent source_scene remains absent. This is not a browser-save import or cave/interior coordinate migration.

Source oracle executes the actual browser sleepUntilMorning/updateDeath functions in a VM and imports original advanceTime.54sequences across3ages x6day times x sleep/two sleeps/defeat, each followed by active deltas0/.01/.04/.05. Tests compare immediate save projection AND next-active survivors, with synthetic save/reload roundtrip. Native2060assertions PASS/exit0; current game/model source hashes verified. Each projected drop payload is accepted by the real full native v4 validator using an existing synthetic full-document fixture. No native player save opened.

Important ordering: sleep advances worldAge but does NOT immediately filter drops before save. The native projection retains expired entries at lifetime0 until the next active advance, including delta0, whose strict expires>worldAge filter removes them. Filtering during sleep/save would change browser-visible saved state/order. Reload may map old expired absolute timestamps to current age at lifetime0; tested next-active survivor semantics remain equal, not byte-identical absolute browser timestamps. Two consecutive sleeps before an active step are covered.

Defeat increments the day without worldAge skip, so drop remaining lifetimes do not bulk drain. Sleep/recovery do not bulk drain the fixture effects/fuel either; this is recovery-slice evidence, NOT a full combined frame/effect/fuel integration. Source save/scene/house/regrowth callbacks remain stubs. Tests also cover non-mutating rejection of malformed lifetime fields and the native600second cap.

Local files work/core001/export-drop-recovery.mjs, drop-recovery-oracle.json, drop_clock_adapter.gd and drop_recovery_audit.gd. Initial fixture/validator-method harness setup errors corrected before successful final run. Root-certificate-store diagnostic remains; no clean-log claim. All runtime/source/save hooks held, all new code stays local behind PROD-002.

Next: combine independent night/survival/frame helpers into pre/post phases under ONE clock owner; do not chain their present Clock.advance calls. Use this adapter when sleep/save/drop representation crosses that owner. Production migrations/OS-fault/native non-saving scene tests remain necessary before live wiring.


## Combined single-owner prototype —27November,13:00UTC

Work-only combined_clock_prototype.gd composes heat pre-phase, ONE Clock.advance, strict drop pruning/night transitions and starvation/fuel post-phase under the actual outer-frame gate semantics. Effects/jump/invulnerability have ONE prefix owner, including active death frames but excluding hidden/paused/not-started/not-ready frames. It reuses Survival.damage and Recovery.sleep_until_morning only; does NOT call either independent night/survival step helper that advances the clock internally. No live camp hook.

Source VM uses actual frame/update prefix, desert/night/starve/fuel/damage/sleep slices and original model advanceTime/tickEffects/gainXP/maxHealth; omitted movement/world/combat body, death recovery/UI/scene/save callbacks are explicit stubs.64sequences /704steps span dusk/dawn, heat/starve/shared invulnerability, guardian, low health, hidden/pause/ready transitions, long timestamp gaps, repeated raw sleep calls, expired drop removal and death-prefix gating. Some raw sleep calls occur during a stubbed active death; this exercises callable ordering, NOT a legitimate controller/bed interaction or a revived-player journey.

Native17602assertions PASS/exit0; current source hashes verified. Per-step oracle comparisons include day/age/hunger, heat/thirst/accumulators/health, effects/jump/invulnerability, nights/XP/level/points, canonical drop content/scenes, fuel, death state, clocks and callback counts.32sequences include a frame that both reaches death and still advances world time: browser does not retroactively abort that current update after damage; the next update takes the death gate. Do not insert a mid-step early return that silently changes those source semantics.

Raw sleep changes calendar/age and callback intentions once, but does not invoke an extra ordinary clock/effect/fuel step. The previously validated save/drop projection is still a separate adapter boundary; no actual serializer or atomic save path in this combined test. Active death recovery itself remains a stub; original independent defeat recovery tests do NOT mean it is now integrated into this owner.

Local files export-combined-clock.mjs, combined-clock-oracle.json, combined_clock_prototype.gd and combined_clock_audit.gd under work/core001/. Runtime/source/native save untouched; code remains local behind PROD-002. Root-certificate-store error remains, no clean-log or full-game parity claim. Next integration boundary: actual defeat-recovery phase plus non-saving scene/frame mapping and versioned migration/OS faults, before any live wiring.
