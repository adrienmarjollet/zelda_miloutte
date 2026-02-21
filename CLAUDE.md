# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Zelda Miloutte is a 2D top-down Zelda-like adventure game built with pygame-ce (Community Edition). The player explores an overworld, fights enemies, collects items, and enters dungeons with boss fights.

## Commands

```bash
# Run the game
uv run zelda-miloutte

# Install dependencies
uv sync

# Run tests
uv run pytest tests/ -v
```

## Architecture

**Game loop & state stack** (`game.py`): `Game` owns a stack of `State` objects. States are pushed/popped/changed. The game loop delegates `update(dt)`, `draw(surface)`, and `handle_event(event)` to the top state. Transitions (fade-in/fade-out) are managed by `Transition` and block input/updates while active.

**State hierarchy** (`states/`):
- `State` (ABC) — base with `enter()`, `exit()`, `update(dt)`, `draw(surface)`, `handle_event(event)`
- `GameplayState` — shared gameplay logic (movement, combat, enemy AI, items, projectiles, hazards, particles, death checking, drawing). Subclasses must initialize `self.tilemap`, `self.player`, `self.camera`, `self.enemies`, `self.items`, `self.chests`, `self.hud`, `self.particles`, `self.projectiles`, `self.signs`
- `PlayState` (overworld) and `DungeonState` (dungeon with boss) extend `GameplayState`
- `TitleState`, `CinematicState`, `PauseState`, `GameOverState` — menu/UI states

**Entity system** (`entities/`): `Entity` base class provides position, velocity, rect-based collision, facing direction, knockback, and alive state. Subclasses: `Player`, `Enemy`, `Archer`, `Boss`, `Item`, `Chest`, `Projectile`, `Sign`.

**World** (`world/`):
- `TileType` enum (0-11): GRASS, WALL, TREE, ROCK, WATER, FLOOR, DOOR, DUNGEON_ENTRANCE, BOSS_DOOR, SPIKES, PIT, DUNGEON_ENTRANCE_2. `solid` property determines collision.
- `TileMap` handles tile lookup, axis-separated collision resolution (`resolve_collision_x/y`), and camera-culled rendering.
- Maps are defined as 2D integer arrays in `maps.py` with companion spawn dictionaries (player position, enemy configs with patrol paths, items, chests, signs).

**Sprites** (`sprites/`): All pixel art is procedurally generated using `surface_from_grid()` (ASCII grid + color palette → pygame Surface). No external image assets. Each entity type has a sprite module (e.g., `player_sprites.py`, `enemy_sprites.py`) that produces animation frames.

**Input** (`input_handler.py`): Arrow keys / WASD for movement, Space to attack, E/Enter to interact, Escape to pause. Diagonal movement is normalized.

**Other systems**: `Camera` with lerp follow and screen shake, `ParticleSystem` for visual effects, `HUD` for hearts/keys/boss health bar, `TextBox` for sign messages, `SoundManager` for music/SFX (loads from `assets/sounds/`).

## Key Patterns

- All coordinates are in pixels; map spawn data uses tile coordinates (multiply by `TILE_SIZE` = 32)
- Combat uses rect collision between `player.sword_rect` and entity rects
- Player stats (hp, keys) are carried between PlayState and DungeonState by copying on state transitions
- Boss configuration is passed as a dict to DungeonState for variant bosses (e.g., Ice Demon)
- Enemies can drop items on death via `get_drop()`
