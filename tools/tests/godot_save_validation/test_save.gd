extends SceneTree

const FIXED := preload("res://save_manager_fixed.gd")
const RENAME_FAIL := preload("res://save_manager_windows_rename_fail.gd")
const PARTIAL_FAIL := preload("res://save_manager_partial_restore_fail.gd")
var assertions: int = 0
var failures: int = 0

func _initialize() -> void:
    call_deferred("_run_tests")

func _check(ok: bool, title: String) -> void:
    assertions += 1
    if ok:
        print("PASS: ", title)
    else:
        failures += 1
        printerr("FAIL: ", title)

func _clear() -> void:
    for path in [
        "user://savegame.save", "user://savegame.save.tmp",
        "user://savegame.save.bak", "user://savegame.save.recover"
    ]:
        if FileAccess.file_exists(path):
            DirAccess.remove_absolute(ProjectSettings.globalize_path(path))

func _write_json(payload: String) -> void:
    var f := FileAccess.open_encrypted_with_pass(
        "user://savegame.save", FileAccess.WRITE, "your_secret_key_here"
    )
    if f == null:
        printerr("Fixture setup error: ", error_string(FileAccess.get_open_error()))
        quit(2)
        return
    f.store_string(payload)
    f.close()

func _run_tests() -> void:
    _clear()
    var normal = FIXED.new()
    var broken_move = RENAME_FAIL.new()
    var broken_restore = PARTIAL_FAIL.new()
    var load_calls: Array[int] = []
    var save_calls: Array[int] = []
    var errors: Array[String] = []
    normal.load_completed.connect(func() -> void: load_calls.append(1))
    normal.save_completed.connect(func() -> void: save_calls.append(1))
    normal.save_error.connect(func(msg: String) -> void: errors.append(msg))

    normal.save_game({"hp": 12})
    _check(save_calls.size() == 1, "initial save succeeds")
    _check(normal.load_game().get("hp") == 12, "encrypted round-trip succeeds")
    normal.save_game({"hp": 13})
    _check(normal.load_game().get("hp") == 13, "existing save can be replaced")
    _check(not FileAccess.file_exists("user://savegame.save.bak"), "successful save cleans backup")

    # Windows can delete the destination and then fail the rename.
    broken_move.save_game({"hp": 0})
    _check(normal.load_game().get("hp") == 13, "Windows rename failure preserves old data")

    # A failed restore may leave partial bytes at an existing SAVE_PATH.
    _clear()
    normal.save_game({"hp": 44})
    var old_hash: String = FileAccess.get_sha256("user://savegame.save")
    var no_success: Array[int] = []
    var partial_errors: Array[String] = []
    broken_restore.save_completed.connect(func() -> void: no_success.append(1))
    broken_restore.save_error.connect(func(msg: String) -> void: partial_errors.append(msg))
    broken_restore.save_game({"hp": 0})
    _check(partial_errors.size() == 1, "partial restoration failure emits an error")
    _check(no_success.is_empty(), "partial restoration failure cannot signal success")
    _check(FileAccess.file_exists("user://savegame.save"), "partial destination exists")
    _check(FileAccess.get_sha256("user://savegame.save.bak") == old_hash, "intact backup survives failed restoration")
    broken_restore.save_game({"hp": 1})
    _check(partial_errors.size() == 2, "later save refuses while backup recovery is blocked")
    _check(no_success.is_empty(), "blocked later save cannot signal success")
    _check(FileAccess.get_sha256("user://savegame.save.bak") == old_hash, "blocked later save does not overwrite backup")
    _check(normal.load_game().get("hp") == 44, "next load recovers despite partial destination")
    _check(not FileAccess.file_exists("user://savegame.save.bak"), "verified recovery clears backup")

    # Saving without an intermediate load must also recover the old save.
    _clear()
    normal.save_game({"hp": 55})
    old_hash = FileAccess.get_sha256("user://savegame.save")
    broken_restore.save_game({"hp": 0})
    _check(FileAccess.get_sha256("user://savegame.save.bak") == old_hash, "repeated failure keeps backup")
    normal.save_game({"hp": 66})
    _check(normal.load_game().get("hp") == 66, "new save follows successful recovery")
    _check(not FileAccess.file_exists("user://savegame.save.bak"), "new save removes old backup")

    # Invalid JSON numbers must not emit load_completed.
    _clear()
    var invalid: Array[String] = [
        '{"level":01}', '{"level":-01}', '{"level":1.}',
        '{"level":1e}', '{"level":+1}', '{"level":.5}'
    ]
    for payload in invalid:
        _write_json(payload)
        var loads_before: int = load_calls.size()
        var errors_before: int = errors.size()
        _check(normal.load_game().is_empty(), "reject malformed numeric token: " + payload)
        _check(load_calls.size() == loads_before, "no load_completed for malformed token: " + payload)
        _check(errors.size() == errors_before + 1, "save_error for malformed token: " + payload)

    _write_json('{"level":1.5e+2,"label":"01,}"}')
    var valid: Dictionary = normal.load_game()
    _check(valid.get("level") == 150.0, "accept valid exponent number")
    _check(valid.get("label") == "01,}", "quoted numbers and punctuation remain valid")
    _write_json('{"level":1,}')
    _check(normal.load_game().is_empty(), "reject trailing object comma")
    _write_json('{"level":"raw\nnewline"}')
    _check(normal.load_game().is_empty(), "reject raw control character")

    _clear()
    normal.save_game({"hp": 99})
    normal.delete_save()
    _check(not normal.has_save(), "delete_save cleans all recovery files")
    _check(normal.load_game().is_empty(), "deleted save cannot reappear")

    broken_move.free()
    broken_restore.free()
    normal.free()
    _clear()
    print("TEST RESULTS: %d assertions, %d failures" % [assertions, failures])
    quit(0 if failures == 0 else 1)
