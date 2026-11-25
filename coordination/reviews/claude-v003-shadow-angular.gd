extends SceneTree
## Isolated review window: live 3D Simm beside the original reference crop.
## No progression or save loading/writing. Launch with --script scripts/simm_head_review.gd.
var model:Node3D
var camera:Camera3D
var animation:AnimationPlayer
var meshes:Array[MeshInstance3D]=[]
var reference:TextureRect
var reference_image:Texture2D
var portrait:=false
var clay_enabled:=false
var title:Label
func _initialize()->void:call_deferred("run")
func set_pose(_clip:String,_time:float)->void:
 pass
func set_view(_head:bool=true,side:int=0)->void:
 portrait=true
 var atlas=AtlasTexture.new();atlas.atlas=reference_image
 atlas.region=Rect2(823,530,145,130);reference.texture=atlas
 camera.size=.65
 var target=Vector3(0,1.215,0)
 camera.position=Vector3(0,1.505,3) if side==1 else (Vector3(-3,1.295,0) if side==2 else Vector3(-.829,1.659,1.435))
 camera.look_at(target)
func clay_toggle()->void:
 clay_enabled=not clay_enabled
 var mat=StandardMaterial3D.new();mat.albedo_color=Color("b7b3a9");mat.roughness=.92
 for mesh in meshes:mesh.material_override=mat if clay_enabled else null
func label(text:String,pos:Vector2,size:int=26)->Label:
 var node=Label.new();node.text=text;node.position=pos;node.add_theme_font_size_override("font_size",size);root.add_child(node);return node
func button(text:String,x:float,action:Callable)->void:
 var b=Button.new();b.text=text;b.position=Vector2(x,1128);b.size=Vector2(190,50);b.add_theme_font_size_override("font_size",22);root.add_child(b);b.pressed.connect(action)
func shot(name:String)->void:
 for i in range(24):await process_frame
 await RenderingServer.frame_post_draw
 var folder=ProjectSettings.globalize_path("res://../work/claude-v003-shadow-qa/")
 DirAccess.make_dir_recursive_absolute(folder)
 assert(root.get_texture().get_image().save_png(folder+name+".png")==OK)
func run()->void:
 root.title="SIMM — Claude v003 native review"
 root.content_scale_size=Vector2i.ZERO
 DisplayServer.window_set_size(Vector2i(2000,1200));root.size=Vector2i(2000,1200)
 var bg=ColorRect.new();bg.color=Color("26352e");bg.size=Vector2(2000,1200);root.add_child(bg)
 reference=TextureRect.new();reference.position=Vector2(10,75);reference.size=Vector2(980,1030);reference.expand_mode=TextureRect.EXPAND_IGNORE_SIZE;reference.stretch_mode=TextureRect.STRETCH_KEEP_ASPECT_CENTERED;root.add_child(reference)
 var img=Image.load_from_file(ProjectSettings.globalize_path("res://../docs/ART-DIRECTION-REFERENCE.png"));assert(img!=null)
 reference_image=ImageTexture.create_from_image(img)
 var container=SubViewportContainer.new();container.position=Vector2(1000,75);container.size=Vector2(990,990);container.stretch=true;root.add_child(container)
 var view=SubViewport.new();view.size=Vector2i(990,990);view.own_world_3d=true;view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;container.add_child(view);view.use_taa=true
 label("REFERENTS · muutmata originaalpildi väljalõige",Vector2(20,20),25)
 label("GODOT · Claude v003 · NATIVE GODOT",Vector2(1020,20),25)
 var stage=Node3D.new();view.add_child(stage)
 var world=WorldEnvironment.new();var env=Environment.new();world.environment=env
 env.background_mode=Environment.BG_COLOR;env.background_color=Color("758178")
 env.ambient_light_source=Environment.AMBIENT_SOURCE_COLOR;env.ambient_light_color=Color("b7c9d2");env.ambient_light_energy=.6
 env.tonemap_mode=Environment.TONE_MAPPER_FILMIC;env.ssao_enabled=true;env.ssao_radius=.20;env.ssao_intensity=.45
 stage.add_child(world)
 var sun=DirectionalLight3D.new();sun.rotation_degrees=Vector3(-40,-30,0);sun.light_energy=1.5;sun.light_color=Color.WHITE;sun.shadow_enabled=true;sun.light_angular_distance=2.0;sun.directional_shadow_max_distance=8;stage.add_child(sun)
 RenderingServer.directional_shadow_atlas_set_size(8192,true)
 RenderingServer.directional_soft_shadow_filter_set_quality(RenderingServer.SHADOW_QUALITY_SOFT_ULTRA)
 var fill=DirectionalLight3D.new();fill.rotation_degrees=Vector3(-20,140,0);fill.light_energy=0.0;fill.light_color=Color("bccdd5");stage.add_child(fill)
 var floor=MeshInstance3D.new();var plane=PlaneMesh.new();plane.size=Vector2(200,200);floor.position.y=-.5;floor.mesh=plane
 var fm=StandardMaterial3D.new();fm.albedo_color=Color("b0ad97");fm.roughness=1;floor.material_override=fm;stage.add_child(floor)
 model=load("res://assets/studies/claude_simm_head_v003.glb").instantiate();stage.add_child(model)
 # Static candidate; original rig is not attached during this visual review.
 camera=Camera3D.new();camera.projection=Camera3D.PROJECTION_PERSPECTIVE;camera.fov=24.0;camera.size=1.70;stage.add_child(camera);camera.current=true
 for mesh:MeshInstance3D in model.find_children("*","MeshInstance3D",true,false):meshes.append(mesh)

 set_pose("idle",0);set_view(true)
 button("Reference view",15,func():set_view(true))
 button("Front",215,func():set_view(true,1))
 button("Värvid / savi",415,clay_toggle)
 button("Eest",615,func():set_view(portrait,1))
 button("Küljelt",815,func():set_view(false,2))
 button("Kolmveerand",1015,func():set_view(portrait,0))
 button("Back",1415,func():
  camera.position=Vector3(0,1.60,-3);camera.look_at(Vector3(0,1.19,0))
 )
 if "--capture-and-quit" in OS.get_cmdline_user_args():
  sun.light_energy=.8;sun.light_color=Color("fff0df");env.ambient_light_energy=.35
  sun.directional_shadow_max_distance=3.0;sun.shadow_bias=.1;sun.shadow_normal_bias=2.0
  sun.light_angular_distance=.25
  await shot("head-v003-shadow-angular025")
  quit(0)
