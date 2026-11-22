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
const TEMP_SAVE_PATH := SAVE_PATH + ".tmp"
const BACKUP_SAVE_PATH := SAVE_PATH + ".bak"
const RECOVERY_SAVE_PATH := SAVE_PATH + ".recover"
const ENCRYPTION_KEY := "your_secret_key_here"

signal save_completed
signal load_completed
signal save_error(message: String)

func save_game(data: Dictionary) -> void:
    # A failed copy may leave a partial SAVE_PATH. Validate it even if it exists.
    var recovery: Error = _recover_pending_backup()
    if recovery != OK:
        save_error.emit("Could not recover previous save: %s" % error_string(recovery))
        return

    var payload: String = JSON.stringify(data)
    var file := FileAccess.open_encrypted_with_pass(
        TEMP_SAVE_PATH, FileAccess.WRITE, ENCRYPTION_KEY
    )
    if file == null:
        save_error.emit("Could not open temporary save file: %s" % error_string(FileAccess.get_open_error()))
        return

    # Encrypted FileAccess buffers data; close() persists the encrypted bytes.
    file.store_string(payload)
    file.close()

    # Reopening verifies that close() successfully wrote and encrypted the file.
    if not _verify_temp(payload):
        _remove_temp()
        save_error.emit("Could not verify written save data")
        return

    # Godot's Windows rename may delete the destination before moving the source.
    # Preserve a verified backup before attempting replacement.
    var backup_error: Error = _backup_existing_save()
    if backup_error != OK:
        _remove_temp()
        save_error.emit("Could not back up previous save: %s" % error_string(backup_error))
        return

    var result: Error = _replace_temp()
    if result != OK:
        var recovery_error: Error = _restore_backup()
        _remove_temp()
        if recovery_error != OK:
            save_error.emit("Replacement failed (%s); recovery failed (%s). Backup retained at %s" % [
                error_string(result), error_string(recovery_error), BACKUP_SAVE_PATH
            ])
        else:
            save_error.emit("Could not replace existing save: %s" % error_string(result))
        return

    # The backup is no longer needed once replacement succeeds.
    if FileAccess.file_exists(BACKUP_SAVE_PATH):
        DirAccess.remove_absolute(ProjectSettings.globalize_path(BACKUP_SAVE_PATH))
    save_completed.emit()

func _verify_temp(expected_payload: String) -> bool:
    var file := FileAccess.open_encrypted_with_pass(
        TEMP_SAVE_PATH, FileAccess.READ, ENCRYPTION_KEY
    )
    if file == null:
        return false
    var actual_payload: String = file.get_as_text()
    file.close()
    return actual_payload == expected_payload

func _backup_existing_save() -> Error:
    # Never overwrite a backup left by an unresolved earlier failure.
    if FileAccess.file_exists(BACKUP_SAVE_PATH):
        return ERR_ALREADY_EXISTS
    if not FileAccess.file_exists(SAVE_PATH):
        return OK
    var result: Error = DirAccess.copy_absolute(
        ProjectSettings.globalize_path(SAVE_PATH),
        ProjectSettings.globalize_path(BACKUP_SAVE_PATH)
    )
    if result != OK:
        return result
    var old_hash: String = FileAccess.get_sha256(SAVE_PATH)
    var backup_hash: String = FileAccess.get_sha256(BACKUP_SAVE_PATH)
    if old_hash.is_empty() or old_hash != backup_hash:
        return ERR_FILE_CORRUPT
    return OK

func _replace_temp() -> Error:
    return DirAccess.rename_absolute(
        ProjectSettings.globalize_path(TEMP_SAVE_PATH),
        ProjectSettings.globalize_path(SAVE_PATH)
    )

func _is_valid_save_file(path: String) -> bool:
    if not FileAccess.file_exists(path):
        return false
    var file := FileAccess.open_encrypted_with_pass(
        path, FileAccess.READ, ENCRYPTION_KEY
    )
    if file == null:
        return false
    var contents: String = file.get_as_text()
    file.close()
    if _has_nonstandard_json(contents):
        return false
    var parser := JSON.new()
    return parser.parse(contents) == OK and parser.data is Dictionary

func _recover_pending_backup() -> Error:
    if not FileAccess.file_exists(BACKUP_SAVE_PATH):
        return OK
    # A complete primary save may be either the old save or a successfully
    # replaced new one whose backup cleanup was interrupted.
    if not _is_valid_save_file(SAVE_PATH):
        var recovery: Error = _restore_backup()
        if recovery != OK:
            return recovery
    # Failure to remove the old backup blocks a new save rather than letting
    # _backup_existing_save() overwrite the only recoverable copy.
    return DirAccess.remove_absolute(ProjectSettings.globalize_path(BACKUP_SAVE_PATH))

func _restore_backup() -> Error:
    if not FileAccess.file_exists(BACKUP_SAVE_PATH):
        return OK
    if not _is_valid_save_file(BACKUP_SAVE_PATH):
        return ERR_FILE_CORRUPT
    var backup_hash: String = FileAccess.get_sha256(BACKUP_SAVE_PATH)
    if backup_hash.is_empty():
        return ERR_FILE_CORRUPT

    # A failed copy can truncate its destination. Stage recovery separately,
    # verify it, then rename while keeping the original backup intact.
    var result: Error = DirAccess.copy_absolute(
        ProjectSettings.globalize_path(BACKUP_SAVE_PATH),
        ProjectSettings.globalize_path(RECOVERY_SAVE_PATH)
    )
    if result != OK:
        return result
    if FileAccess.get_sha256(RECOVERY_SAVE_PATH) != backup_hash:
        return ERR_FILE_CORRUPT
    result = DirAccess.rename_absolute(
        ProjectSettings.globalize_path(RECOVERY_SAVE_PATH),
        ProjectSettings.globalize_path(SAVE_PATH)
    )
    if result != OK:
        return result
    if FileAccess.get_sha256(SAVE_PATH) != backup_hash:
        return ERR_FILE_CORRUPT
    return OK

func _remove_temp() -> void:
    if FileAccess.file_exists(TEMP_SAVE_PATH):
        DirAccess.remove_absolute(ProjectSettings.globalize_path(TEMP_SAVE_PATH))

# Godot accepts trailing commas and raw control characters in strings.
# Detect both before reporting a successful load.
func _has_nonstandard_json(text: String) -> bool:
    var number_rule := RegEx.new()
    if number_rule.compile("^-?(0|[1-9][0-9]*)(\\.[0-9]+)?([eE][+-]?[0-9]+)?$") != OK:
        return true
    var in_string: bool = false
    var escaped: bool = false
    var i: int = 0
    while i < text.length():
        var ch: String = text[i]
        if in_string:
            if text.unicode_at(i) < 32:
                return true
            if escaped:
                escaped = false
            elif ch == "\\":
                escaped = true
            elif ch == "\"":
                in_string = false
        elif ch == "\"":
            in_string = true
        elif text.unicode_at(i) < 32 and ch != "\t" and ch != "\r" and ch != "\n":
            return true
        elif ch == ",":
            var j: int = i + 1
            while j < text.length() and (text[j] == " " or text[j] == "\t" or text[j] == "\r" or text[j] == "\n"):
                j += 1
            if j < text.length() and (text[j] == "}" or text[j] == "]"):
                return true
        elif ch == "-" or (ch >= "0" and ch <= "9"):
            var j: int = i + 1
            while j < text.length():
                var candidate: String = text[j]
                if (candidate >= "0" and candidate <= "9") or candidate == "." or candidate == "+" or candidate == "-" or candidate == "e" or candidate == "E":
                    j += 1
                else:
                    break
            if number_rule.search(text.substr(i, j - i)) == null:
                return true
            i = j
            continue
        elif ch == "+" or ch == ".":
            return true
        i += 1
    return false

func load_game() -> Dictionary:
    var recovery: Error = _recover_pending_backup()
    if recovery != OK:
        save_error.emit("Could not recover previous save: %s" % error_string(recovery))
        return {}
    if not FileAccess.file_exists(SAVE_PATH):
        return {}

    var file := FileAccess.open_encrypted_with_pass(
        SAVE_PATH, FileAccess.READ, ENCRYPTION_KEY
    )
    if file == null:
        save_error.emit("Could not open save file: %s" % error_string(FileAccess.get_open_error()))
        return {}

    var json: String = file.get_as_text()
    file.close()

    # Unlike JSON.parse_string(), JSON.parse() returns structured error data
    # instead of printing a built-in engine error for malformed JSON.
    if _has_nonstandard_json(json):
        save_error.emit("Save data contains nonstandard JSON syntax")
        return {}

    var parser := JSON.new()
    var parse_error: Error = parser.parse(json)
    if parse_error != OK:
        save_error.emit("Could not parse save data at line %d: %s" % [
            parser.get_error_line(), parser.get_error_message()
        ])
        return {}

    var parsed: Variant = parser.data
    if not parsed is Dictionary:
        save_error.emit("Save data must be a JSON dictionary")
        return {}

    load_completed.emit()
    return parsed

func delete_save() -> void:
    # Do not leave a backup that can resurrect an explicitly deleted save.
    for path in [SAVE_PATH, BACKUP_SAVE_PATH, TEMP_SAVE_PATH, RECOVERY_SAVE_PATH]:
        if FileAccess.file_exists(path):
            var result: Error = DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
            if result != OK:
                save_error.emit("Could not delete %s: %s" % [path, error_string(result)])
                return

func has_save() -> bool:
    return FileAccess.file_exists(SAVE_PATH) or FileAccess.file_exists(BACKUP_SAVE_PATH)

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
