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
