extends SceneTree

func _initialize() -> void:
	create_timer(15.0).timeout.connect(func(): quit(1))
	call_deferred("_run")

func _run() -> void:
	var scene := load("res://scenes/camp.tscn") as PackedScene
	var camp: Node3D = scene.instantiate()
	root.add_child(camp)
	for i in range(15):
		await physics_frame
	var player: CharacterBody3D = camp.player
	assert(player.is_on_floor(), "Player must settle onto the actual collision floor")
	assert(absf(player.position.y) < 0.04, "Model root stays at foot level")
	assert(camp.try_interact(), "Nearby loose branch can be gathered")
	assert(camp.inventory.wood == 1)
	assert(not camp.slots.branch.active, "Gathered pickup disappears and cannot pay twice")
	var before: Vector3 = player.position
	Input.action_press("move_forward")
	for i in range(25):
		await physics_frame
	Input.action_release("move_forward")
	assert(player.position.z < before.z - 0.8, "Actual physics movement responds to input")
	var initial: float = camp.camera_size
	camp.adjust_zoom(-1.0)
	assert(camp.camera_size < initial)
	camp.adjust_zoom(-100.0)
	assert(camp.camera_size == 9.0)
	camp.adjust_zoom(100.0)
	assert(camp.camera_size == 23.0)
	print("PASS: Godot 3D camp loads; floor collision, movement, pickup and zoom bounds work.")
	print("Models pending: ", camp.missing_models.size(), ". This is not visual acceptance.")
	quit(0)
