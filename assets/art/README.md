# Simm diorama artwork — 0.6

Original generated artwork created for this project from the approved concept 2 and Mattias's character designs. No artwork was downloaded from another game. These are high-resolution renders in a stylized 3D diorama direction, used by the game's 2.5D renderer.

Active assets:

- `diorama-nature.png`: 4×4 trees, vegetation, rocks, ore, crystal, stump, caves and meteor.
- `diorama-people.png`: 4×4 Simm poses, the six NPCs, Nups, bat, zombie, skeleton, troll and whale. Diego has his rat; Bronkings stays bald.
- `diorama-wildlife.png`: 4×4 woodland, snow and jungle creatures. Not every supplementary animal in this sheet is spawned in this release.
- `diorama-props.png`: 4×4 camp props, cabin/cottage, volcano, furniture, stations, boat, lamps and beacon.
- `diorama-tools.png`: 4×4 tools, logs, water/potions, fibre, metal ingots, slabs, sand and salve.
- `diorama-items.png`: 4×4 food and loot materials.
- `diorama-ground.png`: 3×2 meadow, path, snow, jungle, desert and basalt ground materials.

The transparent PNG originals are retained. The runtime measures each cell's alpha bounds once at load time and caches source rectangles; it never scans pixels in the frame loop. Low-alpha transparent padding is excluded from bounds. Artwork uses high-quality image resampling; text is independently rasterized at screen pixel density. Terrain chunks are bounded and visible objects are culled. Generated walk poses, tool swings, bobbing, floating, light, weather and eruption effects animate locally. Small UI glyphs and some construction geometry are vector-drawn for clarity.

`npm run build` embeds these seven atlases and both licensed fonts into the two identical standalone HTML files. No image generation service or remote asset fetch runs while playing. The former `woodland-atlas.png`, `simm-walk.png`, `campsite-atlas.png` and `npcs-v05.png` are retained as historical source artwork; 0.6 does not load or embed them.
