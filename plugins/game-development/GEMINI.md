# Game Development

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `minecraft-bukkit-pro` | opus | Master Minecraft server plugin development with Bukkit, Spigot, and Paper APIs. Specializes in event-driven architect... |
| `unity-developer` | opus | Build Unity games with optimized C# scripts, efficient rendering, and proper asset management. Masters Unity 6 LTS, U... |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `godot-gdscript-patterns` | Master Godot 4 GDScript patterns including signals, scenes, state machines, and optimization. Use when building Godot games, implementing... |
| `unity-ecs-patterns` | Master Unity ECS (Entity Component System) with DOTS, Jobs, and Burst for high-performance game development. Use when building data-orien... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Master Minecraft server plugin development with Bukkit, Spigot, and Paper APIs" → activates `minecraft-bukkit-pro`
- "Master Godot 4 GDScript patterns including signals, scenes, state machines, and optimization" → activates `godot-gdscript-patterns` skill

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
