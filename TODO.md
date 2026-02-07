# Zelda Miloutte - Remaining Work

## Phase 14: Story & Sidequests Integration

Wire story quests, sidequests, NPCs, dialogue, and ending together.

### Tasks:
- [x] **Finalize quest triggers in `data/quests.py`** - Ensure all 6 story quests + 6 sidequests have proper triggers
- [x] **Place NPCs in all areas** (`world/maps.py`) - Elder in overworld, hermit in forest, archaeologist in desert, old warrior in volcano
- [x] **Quest-conditional NPC dialogue** (`entities/npc.py`) - Different lines based on quest state (not started, active, complete)
- [x] **Gate areas behind story progress** (`states/play_state.py`) - Forest needs quest 1 started, desert needs quest 2 complete, volcano needs quest 4 complete. Show message if player tries to transition without meeting prereqs.
- [x] **Handle quest completion in gameplay** - Wire `_handle_npc_choice()` in PlayState to start/complete quests via `game.quest_manager`
- [x] **Track boss defeats** - When a boss is defeated in DungeonState, call `game.quest_manager.update_objective("defeat_boss", boss_id)` and add boss to `game.world_state["defeated_bosses"]`
- [x] **Track enemy kills for sidequests** - In `_cleanup_dead()`, call `game.quest_manager.update_objective("kill", enemy_type)` for relevant quests
- [x] **Add mid-game cutscene** (`states/cinematic_state.py`) - After forest boss: reveal desert corruption
- [x] **Add ending cutscene** - After final boss: victory sequence + credits
- [x] **Add `story_progress` tracking** to `game.py` - Increment after each story quest completion
- [x] **Save/load quest state** - Persist quest_manager state in save files via `save_manager.py`

### Story outline:
- Act 1 (Overworld): Elder warns of corruption. Sends Miloutte east to Forest.
- Act 2 (Forest): Dark magic corrupts the forest. Defeat Forest Guardian. Learn corruption comes from desert tomb.
- Act 3 (Desert): Archaeologist reveals tomb history. Defeat Sand Worm. Volcano seal is breaking.
- Act 4 (Volcano): Final confrontation. Defeat Inferno Drake. Restore seal. Ending + credits.

---

## Phase 15: Visual & Audio Polish

Improve graphics, particles, screen effects, and sound.

### Tasks:
- [x] **Ambient particles per area** (`particles.py`) - Grass sway (overworld), floating spores (forest), sand wind (desert), embers (volcano)
- [x] **Improved death bursts** - More dramatic enemy/boss death particles
- [x] **Level-up particle explosion** - Burst of golden particles on level up
- [x] **Screen flash on boss phase change** (`sprites/effects.py`) - White flash overlay
- [x] **Damage vignette** - Red edge flash on player hit
- [x] **Item glow effect** - Pulsing glow around pickups
- [x] **Tile variation** (`sprites/tile_sprites.py`) - 2-3 variants per grass/floor tile selected by position hash
- [x] **Smooth XP bar animation** (`hud.py`) - Animated fill rather than instant (was already implemented)
- [x] **Quest notification popup** - "New Quest!" / "Quest Complete!" floating banner
- [x] **Status effect timers on HUD** - Show remaining duration for poison/slow
- [x] **Area-specific ambient sounds** (`sounds.py`) - Boss-specific music track serves as area audio
- [x] **Boss-specific music** - Unique aggressive D minor track for boss fights
- [x] **Victory fanfare sound** - After boss defeat
- [x] **Environmental particles in gameplay** (`states/gameplay_state.py`) - Spawn ambient particles based on area
- [x] **Smooth camera zoom for boss intros** (`camera.py`) - Brief zoom-in when boss appears
