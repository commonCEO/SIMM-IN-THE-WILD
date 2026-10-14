# Simm first art pass

Original generated artwork created specifically for Simm. These are not downloaded stock assets or reproductions of another game's sprites.

- `woodland-atlas.png`: oak, spruce, birch, berries, mossy rock, ore, crystal, workbench, furnace, campfire, alien nest, Nups, rabbit, deer, gentle zombie.
- `simm-walk.png`: four animation frames of the same yellow-coated woodland adventurer.
- `campsite-atlas.png`: cave, tent, friendly bat, stump, modular log walls, wood and stone floors.

The original transparent PNGs are retained. The runtime uses explicit source rectangles in `src/game.js` because the generated layouts do not have perfectly uniform grid cells. Terrain textures, shore boundaries, interaction markers, lighting, particles, UI glyphs and bow effects are drawn in code. Walking, floating, hopping, tool swings and fire flicker are runtime animations.

`npm run build` embeds all three atlases and fonts into both standalone HTML files. No art download or image-generation API call happens while playing. The source assets can be replaced with a later consistent art pass by updating the atlas source rectangles and build asset list.
