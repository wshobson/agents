extends "res://save_manager_fixed.gd"

func _replace_temp() -> Error:
    if FileAccess.file_exists(SAVE_PATH):
        DirAccess.remove_absolute(ProjectSettings.globalize_path(SAVE_PATH))
    return FAILED

func _restore_backup() -> Error:
    var f := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
    if f != null:
        f.store_string("partial encrypted save")
        f.close()
    return ERR_FILE_CORRUPT
