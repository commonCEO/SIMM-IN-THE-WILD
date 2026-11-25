extends SceneTree
## Isolated review window: live 3D Simm beside the original reference crop.
## No progression or save loading/writing. Launch with --script scripts/simm_reference_review.gd.
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
func set_pose(clip:String,time:float)->void:
 animation.play(clip);animation.seek(time,true);animation.advance(0);animation.pause()
 for sk:Skeleton3D in model.find_children("*","Skeleton3D",true,false):sk.force_update_all_bone_transforms()
func set_view(head:bool,side:int=0)->void:
 portrait=head
 var atlas=AtlasTexture.new();atlas.atlas=reference_image
 atlas.region=Rect2(810,515,180,310) if not head else Rect2(823,530,145,130)
 reference.texture=atlas
 camera.size=1.70 if not head else .66
 var target=Vector3(0,.72 if not head else 1.20,0)
 camera.position=Vector3(0,.90,4) if side==1 else (Vector3(4,.92,0) if side==2 else Vector3(-2.2,1.80,4))
 if head:camera.position=Vector3(0,1.37,3) if side==1 else Vector3(.85,1.45,3)
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
 var folder=ProjectSettings.globalize_path("res://../work/simm-v007-body-fit/")
 DirAccess.make_dir_recursive_absolute(folder)
 assert(root.get_texture().get_image().save_png(folder+name+".png")==OK)
func run()->void:
 root.title="SIMM — v007 isolated body fit"
 root.content_scale_size=Vector2i.ZERO
 DisplayServer.window_set_size(Vector2i(2000,1200));root.size=Vector2i(2000,1200)
 var bg=ColorRect.new();bg.color=Color("26352e");bg.size=Vector2(2000,1200);root.add_child(bg)
 reference=TextureRect.new();reference.position=Vector2(10,75);reference.size=Vector2(980,1030);reference.expand_mode=TextureRect.EXPAND_IGNORE_SIZE;reference.stretch_mode=TextureRect.STRETCH_KEEP_ASPECT_CENTERED;root.add_child(reference)
 var img=Image.load_from_file(ProjectSettings.globalize_path("res://../docs/ART-DIRECTION-REFERENCE.png"));assert(img!=null)
 reference_image=ImageTexture.create_from_image(img)
 var container=SubViewportContainer.new();container.position=Vector2(1000,75);container.size=Vector2(990,1030);container.stretch=true;root.add_child(container)
 var view=SubViewport.new();view.size=Vector2i(990,1030);view.own_world_3d=true;view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;container.add_child(view);view.use_taa=true
 label("REFERENTS · muutmata originaalpildi väljalõige",Vector2(20,20),25)
 label("GODOT · v007 HEAD + ORIGINAL BODY",Vector2(1020,20),25)
 var stage=Node3D.new();view.add_child(stage)
 var world=WorldEnvironment.new();var env=Environment.new();world.environment=env
 env.background_mode=Environment.BG_COLOR;env.background_color=Color("758178")
 env.ambient_light_source=Environment.AMBIENT_SOURCE_COLOR;env.ambient_light_color=Color("b7c9d2");env.ambient_light_energy=.35
 env.tonemap_mode=Environment.TONE_MAPPER_FILMIC;env.ssao_enabled=true;env.ssao_radius=.20;env.ssao_intensity=.45
 stage.add_child(world)
 var sun=DirectionalLight3D.new();sun.rotation_degrees=Vector3(-40,-30,0);sun.light_energy=.8;sun.light_color=Color("fff0df");sun.shadow_enabled=true;sun.light_angular_distance=.25;sun.directional_shadow_max_distance=3;stage.add_child(sun)
 RenderingServer.directional_shadow_atlas_set_size(8192,true)
 RenderingServer.directional_soft_shadow_filter_set_quality(RenderingServer.SHADOW_QUALITY_SOFT_ULTRA)
 var fill=DirectionalLight3D.new();fill.rotation_degrees=Vector3(-20,140,0);fill.light_energy=0.0;fill.light_color=Color("bccdd5");stage.add_child(fill)
 var floor=MeshInstance3D.new();var plane=PlaneMesh.new();plane.size=Vector2(200,200);floor.mesh=plane
 var fm=StandardMaterial3D.new();fm.albedo_color=Color("b0ad97");fm.roughness=1;floor.material_override=fm;stage.add_child(floor)
 model=load("res://assets/models/simm.glb").instantiate();stage.add_child(model)
 replace_head_for_study()
 animation=model.find_children("*","AnimationPlayer",true,false)[0]
 camera=Camera3D.new();camera.projection=Camera3D.PROJECTION_ORTHOGONAL;camera.size=1.70;stage.add_child(camera);camera.current=true
 for mesh:MeshInstance3D in model.find_children("*","MeshInstance3D",true,false):meshes.append(mesh)

 for clip:String in ["idle","walk"]:animation.get_animation(clip).loop_mode=Animation.LOOP_LINEAR
 animation.animation_finished.connect(func(clip:String):
  if clip=="gather":animation.play("idle")
 )
 set_pose("idle",0);set_view(false)
 button("Terve tegelane",15,func():set_view(false))
 button("Näo lähivaade",215,func():set_view(true))
 button("Värvid / savi",415,clay_toggle)
 button("Eest",615,func():set_view(portrait,1))
 button("Küljelt",815,func():set_view(false,2))
 button("Kolmveerand",1015,func():set_view(portrait,0))
 button("Kõnd",1215,func():animation.play("walk"))
 button("Korjamine",1415,func():animation.play("gather"))
 button("Seis",1615,func():animation.play("idle"))
 if "--capture-and-quit" in OS.get_cmdline_user_args():
  await shot("body-fit-idle")
  set_view(false,2);await shot("body-fit-side")
  set_view(false);set_pose("walk",.25);await shot("body-fit-walk")
  set_pose("gather",.55);await shot("body-fit-gather")
  set_pose("idle",0);clay_toggle();await shot("body-fit-clay")
  print("FIT: poses sampled; original rig/rest/actions retained, no save system loaded")
  quit(0)

func replace_head_for_study()->void:
 var sk:Skeleton3D=model.find_children("*","Skeleton3D",true,false)[0]
 var original:MeshInstance3D=model.find_children("*","MeshInstance3D",true,false)[0]
 var head=sk.find_bone("head");assert(head>=0 and sk.get_bone_count()==17)
 var binds:Array[int]=[]
 for i in range(original.skin.get_bind_count()):
  if original.skin.get_bind_bone(i)==head or original.skin.get_bind_name(i)=="head":binds.append(i)
 assert(not binds.is_empty())
 var replacement=ArrayMesh.new();var removed=0;var kept=0
 for surface in range(original.mesh.get_surface_count()):
  var arrays=original.mesh.surface_get_arrays(surface)
  var vertices:PackedVector3Array=arrays[Mesh.ARRAY_VERTEX]
  var bones=arrays[Mesh.ARRAY_BONES];var weights=arrays[Mesh.ARRAY_WEIGHTS]
  var stride=int(bones.size()/vertices.size())
  var old_indices:PackedInt32Array=arrays[Mesh.ARRAY_INDEX]
  if old_indices.is_empty():
   for v in range(vertices.size()):old_indices.append(v)
  var indices=PackedInt32Array()
  for i in range(0,old_indices.size(),3):
   var all_head=true
   for k in range(3):
    var v=old_indices[i+k];var head_weight=0.0
    for j in range(stride):
     if int(bones[v*stride+j]) in binds:head_weight+=weights[v*stride+j]
    if head_weight<.99:all_head=false
   if all_head:removed+=1
   else:
    kept+=1
    for k in range(3):indices.append(old_indices[i+k])
  if indices.is_empty():continue
  arrays[Mesh.ARRAY_INDEX]=indices
  replacement.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES,arrays)
  replacement.surface_set_material(replacement.get_surface_count()-1,original.mesh.surface_get_material(surface))
 assert(removed>0 and kept>0)
 original.mesh=replacement
 var attach=BoneAttachment3D.new();attach.bone_name="head";sk.add_child(attach)
 var candidate=load("res://assets/studies/claude_simm_head_v007.glb").instantiate()
 attach.add_child(candidate);candidate.transform=sk.get_bone_global_rest(head).affine_inverse()
 print("FIT: removed old head triangles=",removed," kept original body triangles=",kept," head binds=",binds)
 print("FIT: inverse rest attachment=",candidate.transform," bones=",sk.get_bone_count())
