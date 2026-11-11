extends Node3D
## Real 3D integration scaffold. Primitive placeholders are deliberately labelled.
## Assets are loaded at authored scale: importing must not silently resize bad exports.
const MANIFEST_PATH := "res://assets/manifest.json"
const SPEED := 4.0
var player: CharacterBody3D
var camera: Camera3D
var status: Label
var message: Label
var slots: Dictionary = {}
var inventory: Dictionary = {"wood": 0, "stone": 0}
var missing_models: Array[String] = []
var camera_size := 15.0

func _ready() -> void:
	_setup_input()
	_build_ground_and_light()
	var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(MANIFEST_PATH))
	for definition: Dictionary in manifest["assets"]:
		_build_asset(definition)
	camera = Camera3D.new()
	camera.name = "FollowCamera"
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = camera_size
	camera.current = true
	add_child(camera)
	_follow_camera(1.0)
	_build_hud()

func _setup_input() -> void:
	var keys := {"move_left": KEY_A, "move_right": KEY_D, "move_forward": KEY_W, "move_back": KEY_S, "interact": KEY_E}
	for action: String in keys:
		if not InputMap.has_action(action):
			InputMap.add_action(action, 0.2)
		var key := InputEventKey.new()
		key.physical_keycode = keys[action]
		InputMap.action_add_event(action, key)
	for data: Array in [["move_left", JOY_AXIS_LEFT_X, -1.0], ["move_right", JOY_AXIS_LEFT_X, 1.0], ["move_forward", JOY_AXIS_LEFT_Y, -1.0], ["move_back", JOY_AXIS_LEFT_Y, 1.0]]:
		var stick := InputEventJoypadMotion.new()
		stick.axis = data[1]
		stick.axis_value = data[2]
		InputMap.action_add_event(data[0], stick)
	var button := InputEventJoypadButton.new()
	button.button_index = JOY_BUTTON_A
	InputMap.action_add_event("interact", button)

func _material(color: Color) -> StandardMaterial3D:
	var material := StandardMaterial3D.new()
	material.albedo_color = color
	material.roughness = 0.9
	return material

func _build_ground_and_light() -> void:
	var ground := StaticBody3D.new()
	ground.name = "Ground"
	add_child(ground)
	var mesh := MeshInstance3D.new()
	var plane := PlaneMesh.new()
	plane.size = Vector2(40, 40)
	mesh.mesh = plane
	mesh.material_override = _material(Color("718659"))
	ground.add_child(mesh)
	var collider := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(40, 0.2, 40)
	collider.shape = shape
	collider.position.y = -0.1
	ground.add_child(collider)
	var sun := DirectionalLight3D.new()
	sun.name = "Sun"
	sun.rotation_degrees = Vector3(-50, -30, 0)
	sun.light_color = Color("fff0d3")
	sun.light_energy = 1.4
	sun.shadow_enabled = true
	add_child(sun)
	var world := WorldEnvironment.new()
	var environment := Environment.new()
	environment.background_mode = Environment.BG_COLOR
	environment.background_color = Color("c3d5ce")
	environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.ambient_light_color = Color("c7d6cf")
	environment.ambient_light_energy = 0.65
	environment.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	environment.ssao_enabled = true
	world.environment = environment
	add_child(world)

func _build_asset(definition: Dictionary) -> void:
	var id: String = definition["id"]
	var kind: String = definition["kind"]
	var height: float = definition["height"]
	var body: Node3D
	if kind == "player":
		player = CharacterBody3D.new()
		body = player
	elif kind in ["pickup", "decoration"]:
		body = Node3D.new()
	else:
		body = StaticBody3D.new()
	body.name = id
	add_child(body)
	var pos: Array = definition["position"]
	body.position = Vector3(pos[0], pos[1], pos[2])
	if body is PhysicsBody3D:
		var collider := CollisionShape3D.new()
		if kind in ["player", "npc", "tree"]:
			var capsule := CapsuleShape3D.new()
			capsule.radius = 0.25 if kind != "tree" else 0.32
			capsule.height = height if kind != "tree" else 1.2
			collider.shape = capsule
			collider.position.y = capsule.height * 0.5
		else:
			var box := BoxShape3D.new()
			box.size = Vector3(definition["width"], height, definition["depth"])
			collider.shape = box
			collider.position.y = height * 0.5
		body.add_child(collider)
	var visual := Node3D.new()
	visual.name = "Visual"
	body.add_child(visual)
	var path: String = "res://assets/models/" + definition["file"]
	if ResourceLoader.exists(path):
		var scene := load(path) as PackedScene
		if scene:
			visual.add_child(scene.instantiate())
		else:
			push_error("Model is not an imported PackedScene: " + path)
	else:
		missing_models.append(id)
		_add_placeholder(visual, definition)
	slots[id] = {"node": body, "visual": visual, "definition": definition, "active": true}

func _add_placeholder(parent: Node3D, definition: Dictionary) -> void:
	var mesh := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = Vector3(definition["width"], definition["height"], definition["depth"])
	mesh.mesh = box
	mesh.position.y = definition["height"] * 0.5
	mesh.material_override = _material(Color("d5ba70") if definition["kind"] == "player" else Color("9ca69a"))
	parent.add_child(mesh)

func _build_hud() -> void:
	var layer := CanvasLayer.new()
	add_child(layer)
	var panel := PanelContainer.new()
	panel.position = Vector2(20, 20)
	layer.add_child(panel)
	var content := VBoxContainer.new()
	panel.add_child(content)
	status = Label.new()
	status.text = "SIMM • GODOT 3D BLOCKOUT • %d model exports pending" % missing_models.size()
	content.add_child(status)
	var controls := Label.new()
	controls.text = "WASD / left stick: move • E / A: interact • wheel / hold R3 + right stick: zoom"
	content.add_child(controls)
	message = Label.new()
	message.text = "Integration scaffold only. Visual target has not been achieved or approved."
	content.add_child(message)

func _physics_process(delta: float) -> void:
	if not is_instance_valid(player):
		return
	var input := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	player.velocity.x = input.x * SPEED
	player.velocity.z = input.y * SPEED
	if not player.is_on_floor():
		player.velocity.y -= 9.8 * delta
	else:
		player.velocity.y = 0
	player.move_and_slide()
	if input.length() > 0.05:
		var visual: Node3D = slots["simm"]["visual"]
		visual.rotation.y = lerp_angle(visual.rotation.y, atan2(input.x, input.y), minf(1.0, delta * 12.0))
	_play_player_animation("walk" if input.length() > 0.05 else "idle")
	if Input.is_action_just_pressed("interact"):
		try_interact()
	for device: int in Input.get_connected_joypads():
		if Input.is_joy_button_pressed(device, JOY_BUTTON_RIGHT_STICK):
			var axis := Input.get_joy_axis(device, JOY_AXIS_RIGHT_Y)
			if absf(axis) > 0.2:
				adjust_zoom(axis * delta * 8.0)
	_follow_camera(delta)

func _play_player_animation(animation: String) -> void:
	var visual: Node3D = slots["simm"]["visual"]
	var players: Array[Node] = visual.find_children("*", "AnimationPlayer", true, false)
	if not players.is_empty():
		var animations := players[0] as AnimationPlayer
		if animations.has_animation(animation) and animations.current_animation != animation:
			animations.play(animation, 0.15)

func _follow_camera(delta: float) -> void:
	var target := player.global_position + Vector3(0, 0.6, 0)
	var desired := target + Vector3(0, 10, 12)
	camera.global_position = camera.global_position.lerp(desired, minf(1.0, delta * 10.0))
	camera.look_at(target)
	camera.size = camera_size

func adjust_zoom(amount: float) -> void:
	camera_size = clampf(camera_size + amount, 9.0, 23.0)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			adjust_zoom(-1.0)
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			adjust_zoom(1.0)

func try_interact() -> bool:
	var selected := ""
	var distance := 1.8
	for id: String in ["branch", "pebble", "workbench", "leina", "bronkings"]:
		var slot: Dictionary = slots[id]
		var node: Node3D = slot["node"]
		var current := player.global_position.distance_to(node.global_position)
		if slot["active"] and current < distance:
			selected = id
			distance = current
	if selected.is_empty():
		message.text = "Move closer to a branch, pebble, workbench or NPC."
		return false
	if selected in ["branch", "pebble"]:
		var item := "wood" if selected == "branch" else "stone"
		inventory[item] += 1
		slots[selected]["active"] = false
		slots[selected]["node"].hide()
		message.text = "Picked up %s. Wood: %d • Stone: %d" % [item, inventory["wood"], inventory["stone"]]
	elif selected == "leina":
		message.text = "LEINA: A seed can grow into a big idea."
	elif selected == "bronkings":
		message.text = "BRONKINGS: Good work begins with a fair deal."
	else:
		message.text = "Workbench integration point. Crafting migration follows visual approval."
	return true
