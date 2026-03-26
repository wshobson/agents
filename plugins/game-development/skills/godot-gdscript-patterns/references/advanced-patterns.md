# Godot GDScript: Advanced Patterns

Advanced patterns for scene management, save systems, performance optimization, and best practices.

## Pattern 6: Scene Management

```gdscript
# scene_manager.gd (Autoload)
extends Node

signal scene_loading_started(scene_path: String)
signal scene_loading_progress(progress: float)
signal scene_loaded(scene: Node)
signal transition_started
signal transition_finished

@export var transition_scene: PackedScene
@export var loading_scene: PackedScene

var _current_scene: Node
var _transition: CanvasLayer
var _loader: ResourceLoader

func _ready() -> void:
    _current_scene = get_tree().current_scene

    if transition_scene:
        _transition = transition_scene.instantiate()
        add_child(_transition)
        _transition.visible = false

func change_scene(scene_path: String, with_transition: bool = true) -> void:
    if with_transition:
        await _play_transition_out()

    _load_scene(scene_path)

func change_scene_packed(scene: PackedScene, with_transition: bool = true) -> void:
    if with_transition:
        await _play_transition_out()

    _swap_scene(scene.instantiate())

func _load_scene(path: String) -> void:
    scene_loading_started.emit(path)

    # Check if already loaded
    if ResourceLoader.has_cached(path):
        var scene := load(path) as PackedScene
        _swap_scene(scene.instantiate())
        return

    # Async loading
    ResourceLoader.load_threaded_request(path)

    while true:
        var progress := []
        var status := ResourceLoader.load_threaded_get_status(path, progress)

        match status:
            ResourceLoader.THREAD_LOAD_IN_PROGRESS:
                scene_loading_progress.emit(progress[0])
                await get_tree().process_frame
            ResourceLoader.THREAD_LOAD_LOADED:
                var scene := ResourceLoader.load_threaded_get(path) as PackedScene
                _swap_scene(scene.instantiate())
                return
            _:
                push_error("Failed to load scene: %s" % path)
                return

func _swap_scene(new_scene: Node) -> void:
    if _current_scene:
        _current_scene.queue_free()

    _current_scene = new_scene
    get_tree().root.add_child(_current_scene)
    get_tree().current_scene = _current_scene

    scene_loaded.emit(_current_scene)
    await _play_transition_in()

func _play_transition_out() -> void:
    if not _transition:
        return

    transition_started.emit()
    _transition.visible = true

    if _transition.has_method("transition_out"):
        await _transition.transition_out()
    else:
        await get_tree().create_timer(0.3).timeout

func _play_transition_in() -> void:
    if not _transition:
        transition_finished.emit()
        return

    if _transition.has_method("transition_in"):
        await _transition.transition_in()
    else:
        await get_tree().create_timer(0.3).timeout

    _transition.visible = false
    transition_finished.emit()
```

## Pattern 7: Save System

```gdscript
# save_manager.gd (Autoload)
extends Node

const SAVE_PATH := "user://savegame.save"
const ENCRYPTION_KEY := "your_secret_key_here"

signal save_completed
signal load_completed
signal save_error(message: String)

func save_game(data: Dictionary) -> void:
    var file := FileAccess.open_encrypted_with_pass(
        SAVE_PATH,
        FileAccess.WRITE,
        ENCRYPTION_KEY
    )

    if file == null:
        save_error.emit("Could not open save file")
        return

    var json := JSON.stringify(data)
    file.store_string(json)
    file.close()

    save_completed.emit()

func load_game() -> Dictionary:
    if not FileAccess.file_exists(SAVE_PATH):
        return {}

    var file := FileAccess.open_encrypted_with_pass(
        SAVE_PATH,
        FileAccess.READ,
        ENCRYPTION_KEY
    )

    if file == null:
        save_error.emit("Could not open save file")
        return {}

    var json := file.get_as_text()
    file.close()

    var parsed := JSON.parse_string(json)
    if parsed == null:
        save_error.emit("Could not parse save data")
        return {}

    load_completed.emit()
    return parsed

func delete_save() -> void:
    if FileAccess.file_exists(SAVE_PATH):
        DirAccess.remove_absolute(SAVE_PATH)

func has_save() -> bool:
    return FileAccess.file_exists(SAVE_PATH)
```

```gdscript
# saveable.gd (Attach to saveable nodes)
class_name Saveable
extends Node

@export var save_id: String

func _ready() -> void:
    if save_id.is_empty():
        save_id = str(get_path())

func get_save_data() -> Dictionary:
    var parent := get_parent()
    var data := {"id": save_id}

    if parent is Node2D:
        data["position"] = {"x": parent.position.x, "y": parent.position.y}

    if parent.has_method("get_custom_save_data"):
        data.merge(parent.get_custom_save_data())

    return data

func load_save_data(data: Dictionary) -> void:
    var parent := get_parent()

    if data.has("position") and parent is Node2D:
        parent.position = Vector2(data.position.x, data.position.y)

    if parent.has_method("load_custom_save_data"):
        parent.load_custom_save_data(data)
```

## Performance Tips

```gdscript
# 1. Cache node references
@onready var sprite := $Sprite2D  # Good
# $Sprite2D in _process()  # Bad - repeated lookup

# 2. Use object pooling for frequent spawning
# See Pattern 4 in the main skill

# 3. Avoid allocations in hot paths
var _reusable_array: Array = []

func _process(_delta: float) -> void:
    _reusable_array.clear()  # Reuse instead of creating new

# 4. Use static typing
func calculate(value: float) -> float:  # Good
    return value * 2.0

# 5. Disable processing when not needed
func _on_off_screen() -> void:
    set_process(false)
    set_physics_process(false)
```

## Best Practices

### Do's

- **Use signals for decoupling** - Avoid direct references
- **Type everything** - Static typing catches errors
- **Use resources for data** - Separate data from logic
- **Pool frequently spawned objects** - Avoid GC hitches
- **Use Autoloads sparingly** - Only for truly global systems

### Don'ts

- **Don't use `get_node()` in loops** - Cache references
- **Don't couple scenes tightly** - Use signals
- **Don't put logic in resources** - Keep them data-only
- **Don't ignore the Profiler** - Monitor performance
- **Don't fight the scene tree** - Work with Godot's design
