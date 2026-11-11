"""Synthetic export fixture only; never a game art asset. Run with Blender --python."""
import sys
from pathlib import Path
import bpy

output = Path(sys.argv[sys.argv.index('--') + 1]).resolve()
if output.exists():
    raise RuntimeError(f'Refusing to overwrite an existing model: {output}')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.scale_length = 1.0
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.06))
model = bpy.context.object
model.name = 'branch'
model.dimensions = (0.6, 0.2, 0.12)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bpy.ops.export_scene.gltf(filepath=str(output), export_format='GLB', use_selection=True, export_yup=True)
