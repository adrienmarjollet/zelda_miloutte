# Zelda Miloutte - Remaining Work

## Phase 14: Story & Sidequests Integration

Wire story quests, sidequests, NPCs, dialogue, and ending together.

### Tasks:
- [ ] **Finalize quest triggers in `data/quests.py`** - Ensure all 6 story quests + 6 sidequests have proper triggers
- [ ] **Place NPCs in all areas** (`world/maps.py`) - Elder in overworld, hermit in forest, archaeologist in desert, old warrior in volcano
- [ ] **Quest-conditional NPC dialogue** (`entities/npc.py`) - Different lines based on quest state (not started, active, complete)
- [ ] **Gate areas behind story progress** (`states/play_state.py`) - Forest needs quest 1 started, desert needs quest 2 complete, volcano needs quest 4 complete. Show message if player tries to transition without meeting prereqs.
- [ ] **Handle quest completion in gameplay** - Wire `_handle_npc_choice()` in PlayState to start/complete quests via `game.quest_manager`
- [ ] **Track boss defeats** - When a boss is defeated in DungeonState, call `game.quest_manager.update_objective("defeat_boss", boss_id)` and add boss to `game.world_state["defeated_bosses"]`
- [ ] **Track enemy kills for sidequests** - In `_cleanup_dead()`, call `game.quest_manager.update_objective("kill", enemy_type)` for relevant quests
- [ ] **Add mid-game cutscene** (`states/cinematic_state.py`) - After forest boss: reveal desert corruption
- [ ] **Add ending cutscene** - After final boss: victory sequence + credits
- [ ] **Add `story_progress` tracking** to `game.py` - Increment after each story quest completion
- [ ] **Save/load quest state** - Persist quest_manager state in save files via `save_manager.py`

### Story outline:
- Act 1 (Overworld): Elder warns of corruption. Sends Miloutte east to Forest.
- Act 2 (Forest): Dark magic corrupts the forest. Defeat Forest Guardian. Learn corruption comes from desert tomb.
- Act 3 (Desert): Archaeologist reveals tomb history. Defeat Sand Worm. Volcano seal is breaking.
- Act 4 (Volcano): Final confrontation. Defeat Inferno Drake. Restore seal. Ending + credits.

---

## Phase 15: Visual & Audio Polish

Improve graphics, particles, screen effects, and sound.

### Tasks:
- [ ] **Ambient particles per area** (`particles.py`) - Grass sway (overworld), floating spores (forest), sand wind (desert), embers (volcano)
- [ ] **Improved death bursts** - More dramatic enemy/boss death particles
- [ ] **Level-up particle explosion** - Burst of golden particles on level up
- [ ] **Screen flash on boss phase change** (`sprites/effects.py`) - White flash overlay
- [ ] **Damage vignette** - Red edge flash on player hit
- [ ] **Item glow effect** - Pulsing glow around pickups
- [ ] **Tile variation** (`sprites/tile_sprites.py`) - 2-3 variants per grass/floor tile selected by position hash
- [ ] **Smooth XP bar animation** (`hud.py`) - Animated fill rather than instant
- [ ] **Quest notification popup** - "New Quest!" / "Quest Complete!" floating banner
- [ ] **Status effect timers on HUD** - Show remaining duration for poison/slow
- [ ] **Area-specific ambient sounds** (`sounds.py`) - Wind, bird calls, etc.
- [ ] **Boss-specific music** - Unique track for boss fights
- [ ] **Victory fanfare sound** - After boss defeat
- [ ] **Environmental particles in gameplay** (`states/gameplay_state.py`) - Spawn ambient particles based on area
- [ ] **Smooth camera zoom for boss intros** (`camera.py`) - Brief zoom-in when boss appears
