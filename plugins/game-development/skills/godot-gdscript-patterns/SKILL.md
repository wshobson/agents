---
name: godot-gdscript-patterns
description: Master Godot 4 GDScript patterns including signals, scenes, state machines, and optimization. Use when building Godot games, implementing game systems, or learning GDScript best practices.
---

# Godot GDScript Patterns

Production patterns for Godot 4.x game development with GDScript, covering architecture, signals, scenes, and optimization.

## When to Use This Skill

- Building games with Godot 4
- Implementing game systems in GDScript
- Designing scene architecture
- Managing game state
- Optimizing GDScript performance
- Learning Godot best practices

## Core Concepts

### 1. Godot Architecture

```
Node: Base building block
├── Scene: Reusable node tree (saved as .tscn)
├── Resource: Data container (saved as .tres)
├── Signal: Event communication
└── Group: Node categorization
```

### 2. GDScript Basics

```gdscript
class_name Player
extends CharacterBody2D

# Signals
signal health_changed(new_health: int)
signal died

# Exports (Inspector-editable)
@export var speed: float = 200.0
@export var max_health: int = 100
@export_range(0, 1) var damage_reduction: float = 0.0
@export_group("Combat")
@export var attack_damage: int = 10
@export var attack_cooldown: float = 0.5

# Onready (initialized when ready)
@onready var sprite: Sprite2D = $Sprite2D
@onready var animation: AnimationPlayer = $AnimationPlayer
@onready var hitbox: Area2D = $Hitbox

# Private variables (convention: underscore prefix)
var _health: int
var _can_attack: bool = true

func _ready() -> void:
    _health = max_health

func _physics_process(delta: float) -> void:
    var direction := Input.get_vector("left", "right", "up", "down")
    velocity = direction * speed
    move_and_slide()

func take_damage(amount: int) -> void:
    var actual_damage := int(amount * (1.0 - damage_reduction))
    _health = max(_health - actual_damage, 0)
    health_changed.emit(_health)

    if _health <= 0:
        died.emit()
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

