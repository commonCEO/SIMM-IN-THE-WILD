extends SceneTree
## Requires the temporary branch.glb made by create_blender_fixture.py.
func _initialize() -> void:
	create_timer(15.0).timeout.connect(func(): quit(1))
	call_deferred("_run")

func _run() -> void:
	var camp: Node3D = load("res://scenes/camp.tscn").instantiate()
	root.add_child(camp)
	await process_frame
	assert(not camp.missing_models.has("branch"), "Expected real Blender GLB to replace the branch blockout")
	var visual: Node3D = camp.slots.branch.visual
	var meshes: Array[Node] = visual.find_children("*", "MeshInstance3D", true, false)
	assert(meshes.size() == 1)
	var mesh := meshes[0] as MeshInstance3D
	var bounds: AABB = mesh.global_transform * mesh.get_aabb()
	assert(absf(bounds.size.x - 0.6) < 0.001, "Metre scale: X width")
	assert(absf(bounds.size.y - 0.12) < 0.001, "Blender Z maps to Godot Y height")
	assert(absf(bounds.size.z - 0.2) < 0.001, "Blender Y maps to Godot Z depth")
	assert(absf(bounds.position.y) < 0.001, "Pivot remains on ground")
	print("PASS: Blender GLB replaces blockout with correct metre scale, Y-up conversion and ground pivot.")
	quit(0)
