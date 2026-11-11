SIMM — Godot 3D integration scaffold

Open project.godot in Godot 4.6 or a compatible newer Godot 4 release.
Cloud verification used Godot 4.6.3. Forward+ is selected for the future lit
3D scene; local GPU/rendering still needs to be checked on the user's Windows PC.

This is a deliberately labelled primitive blockout, NOT the approved visual
result. It leaves the browser 0.6 game intact. It establishes the scene, real
physics, a camera and the asset contract so Blender and Godot work can proceed
together without changing scale/paths after every asset delivery.

Controls:
WASD / controller left stick — move
E / controller A — gather a nearby branch/pebble or interact with bench/NPC
Mouse wheel / hold R3 and move right stick vertically — zoom

Art delivery:
Read ../docs/FABLE-BLENDER-HANDOVER.txt. Export the GLBs named in
assets/manifest.json into assets/models/. The prototype automatically replaces
its placeholder when the corresponding imported GLB exists. No scale correction
is applied: 1 unit = 1 metre, pivot at feet/ground, model front +Z in Godot.
The level places authored instances at the manifest positions.

Current scope:
One clearing, Simm, Leina, Bronkings, camp objects, pickups, trees and simple
placeholder dialogue. This is not a port of crafting, inventory UI, quests,
biomes, saves, house upgrades or multiplayer. Those follow visual acceptance.

Tests (run with Godot executable on PATH, or substitute full Windows path):
godot --headless --path godot --editor --import --quit
godot --headless --path godot --script tests/smoke.gd
Run those from the repository root. On Windows prefer Godot's _console.exe
build for captured logs. Open the editor with --editor --path godot, then F5.

MCP:
The cloud conversation had no callable Godot/Blender MCP tools. Its command-line
Godot and Blender installations do not imply local installations or local MCP
access. For Windows setup use ../docs/LOCAL-CODEX-GODOT-HANDOVER.txt in a Codex
conversation attached to THIS COMPUTER and this project folder.

Optional Blender-to-Godot contract test (only when branch.glb does not exist):
blender --background --factory-startup --threads 1 --python godot/tests/create_blender_fixture.py -- <absolute-repo>/godot/assets/models/branch.glb
Import with the editor command above, then run:
godot --headless --path godot --script tests/import_smoke.gd
Remove ONLY the generated branch.glb and its branch.glb.import after this test,
then rescan/reimport. The fixture generator refuses to overwrite a real model.
