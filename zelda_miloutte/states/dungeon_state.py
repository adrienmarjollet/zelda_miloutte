import pygame
from zelda_miloutte.states.gameplay_state import GameplayState
from zelda_miloutte.entities.player import Player
from zelda_miloutte.entities.enemy import Enemy
from zelda_miloutte.entities.boss import Boss
from zelda_miloutte.entities.item import Item
from zelda_miloutte.camera import Camera
from zelda_miloutte.world.tilemap import TileMap
from zelda_miloutte.world.maps import DUNGEON, DUNGEON_SPAWNS, DUNGEON2, DUNGEON2_SPAWNS
from zelda_miloutte.hud import HUD
from zelda_miloutte.settings import (
    TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GOLD,
    BOSS2_HP, BOSS2_SPEED, BOSS2_CHASE_SPEED, BOSS2_CHARGE_SPEED, BOSS2_DAMAGE, ICE_BLUE,
)
from zelda_miloutte.particles import ParticleSystem
from zelda_miloutte.sounds import get_sound_manager


class DungeonState(GameplayState):
    def __init__(self, game, play_state, dungeon_map=None, dungeon_spawns=None,
                 boss_config=None, boss_class=None, victory_message=None):
        super().__init__(game)
        self.play_state = play_state

        # Use defaults if not specified
        if dungeon_map is None:
            dungeon_map = DUNGEON
        if dungeon_spawns is None:
            dungeon_spawns = DUNGEON_SPAWNS
        if victory_message is None:
            victory_message = "Miloutte saved the land!"

        self.dungeon_spawns = dungeon_spawns
        self.victory_text = victory_message
        self.tilemap = TileMap(dungeon_map)

        spawn = dungeon_spawns["player"]
        # Carry over player stats from overworld
        self.player = Player(spawn[0] * TILE_SIZE, spawn[1] * TILE_SIZE)
        self.player.hp = play_state.player.hp
        self.player.max_hp = play_state.player.max_hp
        self.player.mp = play_state.player.mp
        self.player.max_mp = play_state.player.max_mp
        self.player.keys = play_state.player.keys
        self.player.level = play_state.player.level
        self.player.xp = play_state.player.xp
        self.player.xp_to_next = play_state.player.xp_to_next
        self.player.base_attack = play_state.player.base_attack
        self.player.base_defense = play_state.player.base_defense
        self.player.gold = play_state.player.gold
        self.player.inventory = play_state.player.inventory
        self.player.unlocked_abilities = play_state.player.unlocked_abilities
        # Copy ability instances (not just names)
        self.player.abilities = play_state.player.abilities
        self.player.active_ability_index = play_state.player.active_ability_index

        # Carry companion from overworld to dungeon
        self.companion = play_state.companion
        if self.companion is not None:
            # Reposition companion near player in dungeon
            self.companion.x = self.player.x - 30
            self.companion.y = self.player.y
            self.companion.target_x = self.companion.x
            self.companion.target_y = self.companion.y

        self.camera = Camera(self.tilemap.pixel_width, self.tilemap.pixel_height)
        self.hud = HUD()

        # Enemies
        from zelda_miloutte.entities.archer import Archer
        from zelda_miloutte.entities.vine_snapper import VineSnapper
        from zelda_miloutte.entities.ice_wraith import IceWraith
        from zelda_miloutte.entities.frost_golem import FrostGolem
        from zelda_miloutte.ng_plus import scale_enemy_stats
        self.enemies = []
        for edata in dungeon_spawns.get("enemies", []):
            # Check enemy type
            if edata.get("type") == "archer":
                e = Archer(
                    edata["x"] * TILE_SIZE, edata["y"] * TILE_SIZE,
                    edata.get("patrol", []),
                )
            elif edata.get("type") == "vine_snapper":
                e = VineSnapper(
                    edata["x"] * TILE_SIZE, edata["y"] * TILE_SIZE,
                )
            elif edata.get("type") == "ice_wraith":
                e = IceWraith(
                    edata["x"] * TILE_SIZE, edata["y"] * TILE_SIZE,
                )
            elif edata.get("type") == "frost_golem":
                e = FrostGolem(
                    edata["x"] * TILE_SIZE, edata["y"] * TILE_SIZE,
                )
            else:
                e = Enemy(
                    edata["x"] * TILE_SIZE, edata["y"] * TILE_SIZE,
                    edata.get("patrol", []),
                )

            # Apply NG+ scaling if in a New Game+ cycle
            if self.game.ng_plus_count > 0:
                scaled_hp, scaled_damage, scaled_speed = scale_enemy_stats(
                    e.hp, e.damage, e.speed, self.game.ng_plus_count
                )
                e.hp = scaled_hp
                e.max_hp = scaled_hp
                e.damage = scaled_damage
                e.speed = scaled_speed
                # Scale chase_speed if enemy has it
                if hasattr(e, 'chase_speed'):
                    _, _, scaled_chase = scale_enemy_stats(
                        e.max_hp, e.damage, e.chase_speed, self.game.ng_plus_count
                    )
                    e.chase_speed = scaled_chase

            self.enemies.append(e)

        # Boss - use custom class if provided, otherwise default Boss
        from zelda_miloutte.ng_plus import scale_boss_stats, get_boss_cooldown_scale
        bdata = dungeon_spawns["boss"]
        if boss_class is not None:
            # Use custom boss class (e.g., ForestGuardian)
            self.boss = boss_class(bdata["x"] * TILE_SIZE, bdata["y"] * TILE_SIZE)
        elif boss_config is None:
            self.boss = Boss(bdata["x"] * TILE_SIZE, bdata["y"] * TILE_SIZE)
        else:
            self.boss = Boss(bdata["x"] * TILE_SIZE, bdata["y"] * TILE_SIZE, **boss_config)

        # Apply NG+ scaling to boss if in a New Game+ cycle
        if self.game.ng_plus_count > 0:
            scaled_hp, scaled_damage, scaled_speed = scale_boss_stats(
                self.boss.hp, self.boss.damage, self.boss.speed, self.game.ng_plus_count
            )
            self.boss.hp = scaled_hp
            self.boss.max_hp = scaled_hp
            self.boss.damage = scaled_damage
            self.boss.speed = scaled_speed
            # Scale chase_speed and charge_speed if boss has them
            if hasattr(self.boss, 'chase_speed'):
                _, _, scaled_chase = scale_boss_stats(
                    self.boss.max_hp, self.boss.damage, self.boss.chase_speed, self.game.ng_plus_count
                )
                self.boss.chase_speed = scaled_chase
            if hasattr(self.boss, 'charge_speed'):
                _, _, scaled_charge = scale_boss_stats(
                    self.boss.max_hp, self.boss.damage, self.boss.charge_speed, self.game.ng_plus_count
                )
                self.boss.charge_speed = scaled_charge
            # Apply faster attack cooldowns for all boss types
            cooldown_scale = get_boss_cooldown_scale(self.game.ng_plus_count)
            # Standard Boss charge attack
            if hasattr(self.boss, 'charge_cooldown'):
                if not hasattr(self.boss, '_base_charge_cooldown'):
                    from zelda_miloutte.settings import BOSS_CHARGE_COOLDOWN
                    self.boss._base_charge_cooldown = BOSS_CHARGE_COOLDOWN
                self.boss.charge_cooldown = self.boss._base_charge_cooldown * cooldown_scale
            # Forest Guardian root slam
            if hasattr(self.boss, 'root_slam_cooldown'):
                if not hasattr(self.boss, '_base_root_slam_cooldown'):
                    self.boss._base_root_slam_cooldown = self.boss.root_slam_cooldown
                self.boss.root_slam_cooldown = self.boss._base_root_slam_cooldown * cooldown_scale
            if hasattr(self.boss, 'vine_summon_cooldown'):
                if not hasattr(self.boss, '_base_vine_summon_cooldown'):
                    self.boss._base_vine_summon_cooldown = self.boss.vine_summon_cooldown
                self.boss.vine_summon_cooldown = self.boss._base_vine_summon_cooldown * cooldown_scale
            # Inferno Drake fire breath and meteors
            if hasattr(self.boss, 'fire_breath_cooldown'):
                if not hasattr(self.boss, '_base_fire_breath_cooldown'):
                    self.boss._base_fire_breath_cooldown = self.boss.fire_breath_cooldown
                self.boss.fire_breath_cooldown = self.boss._base_fire_breath_cooldown * cooldown_scale
            if hasattr(self.boss, 'meteor_cooldown'):
                if not hasattr(self.boss, '_base_meteor_cooldown'):
                    self.boss._base_meteor_cooldown = self.boss.meteor_cooldown
                self.boss.meteor_cooldown = self.boss._base_meteor_cooldown * cooldown_scale

        # Items
        self.items = []
        for idata in dungeon_spawns.get("items", []):
            item = Item(
                idata["x"] * TILE_SIZE, idata["y"] * TILE_SIZE,
                idata["type"],
            )
            self.items.append(item)

        # Chests
        from zelda_miloutte.entities.chest import Chest
        self.chests = []
        for cdata in dungeon_spawns.get("chests", []):
            chest = Chest(
                cdata["x"] * TILE_SIZE, cdata["y"] * TILE_SIZE,
                cdata["contents"],
            )
            self.chests.append(chest)

        # Store boss config for ID tracking
        self._boss_config = boss_config
        self.victory = False
        self.victory_timer = 0.0
        self.victory_duration = 3.0
        self.victory_font = None

        self.particles = ParticleSystem()
        self.projectiles = []
        self.boss_death_emitted = False
        self._boss_prev_phase = 1
        self._boss_intro_timer = 1.5  # Brief zoom-in when boss appears
        self.camera.start_zoom(1.15, speed=0.3)  # Gentle zoom in

        # Initialize signs
        self._spawn_signs()

        # Initialize puzzles
        self._spawn_puzzles(dungeon_spawns)

    def enter(self):
        """Called when entering this state."""
        get_sound_manager().play_music('boss')
        # Track boss fight start for achievements
        self.game.achievement_manager.on_boss_fight_start()
        # Discover boss in bestiary
        boss_class = type(self.boss).__name__
        self.game.bestiary.discover(boss_class)
        # Clear fire trails on dungeon entry to prevent visual artifacts
        self.fire_trails = []

    def _spawn_signs(self):
        from zelda_miloutte.entities.sign import Sign
        self.signs = []
        for sdata in self.dungeon_spawns.get("signs", []):
            sign = Sign(
                sdata["x"] * TILE_SIZE, sdata["y"] * TILE_SIZE,
                sdata["text"],
            )
            self.signs.append(sign)

    def _copy_stats_back(self):
        """Copy all player stats back to the overworld PlayState player."""
        p = self.play_state.player
        p.hp = self.player.hp
        p.max_hp = self.player.max_hp
        p.mp = self.player.mp
        p.max_mp = self.player.max_mp
        p.keys = self.player.keys
        p.level = self.player.level
        p.xp = self.player.xp
        p.xp_to_next = self.player.xp_to_next
        p.base_attack = self.player.base_attack
        p.base_defense = self.player.base_defense
        p.gold = self.player.gold
        p.inventory = self.player.inventory
        p.unlocked_abilities = self.player.unlocked_abilities
        # Copy ability instances back
        p.abilities = self.player.abilities
        p.active_ability_index = self.player.active_ability_index

        # Copy companion back to overworld
        self.play_state.companion = self.companion
        if self.companion is not None:
            # Reposition companion near player in overworld
            self.companion.x = p.x - 30
            self.companion.y = p.y
            self.companion.target_x = self.companion.x
            self.companion.target_y = self.companion.y

    def handle_event(self, event):
        pass

    def update(self, dt):
        # Check for pause
        if self.game.input.pause:
            from zelda_miloutte.states.pause_state import PauseState
            self.game.push_state(PauseState(self.game))
            return

        # Victory state handling
        if self.victory:
            self.victory_timer += dt
            if self.victory_timer >= self.victory_duration:
                # Determine boss type for cutscene triggers
                boss_class_name = type(self.boss).__name__

                def return_to_overworld():
                    self._copy_stats_back()
                    self.game.pop_state()

                if boss_class_name == "ForestGuardian":
                    # Mid-game cutscene after forest boss
                    def show_midgame_cutscene():
                        self._copy_stats_back()
                        self.game.pop_state()  # pop dungeon
                        from zelda_miloutte.states.cinematic_state import CinematicState
                        self.game.push_state(CinematicState(
                            self.game, cutscene_type="midgame",
                            on_complete=lambda: self.game.pop_state()
                        ))
                    self.game.transition_to(show_midgame_cutscene)
                elif boss_class_name == "InfernoDrake":
                    # Ending cutscene after final boss -> NG+ choice
                    # Capture player ref before state changes
                    player_ref = self.play_state.player

                    def show_ending():
                        self._copy_stats_back()
                        self.game.pop_state()  # pop dungeon
                        from zelda_miloutte.states.cinematic_state import CinematicState

                        def on_cinematic_complete():
                            self.game.pop_state()  # pop cinematic
                            from zelda_miloutte.states.ng_plus_choice_state import NGPlusChoiceState
                            self.game.change_state(NGPlusChoiceState(
                                self.game, player_ref=player_ref
                            ))

                        self.game.push_state(CinematicState(
                            self.game, cutscene_type="ending",
                            on_complete=on_cinematic_complete,
                        ))
                    self.game.transition_to(show_ending)
                else:
                    self.game.transition_to(return_to_overworld)
            return

        # If textbox is active, only update textbox (pauses game)
        if self.textbox.active:
            self._update_textbox(dt)
            return

        # Check for sign interaction
        self._check_sign_interaction()

        # Shared gameplay updates
        self._update_movement(dt)

        # Update puzzles
        self._update_puzzles(dt)

        # Check push block interactions
        self._check_push_block_interaction()

        # Resolve push block collision (prevent player from walking through blocks)
        self._resolve_push_block_collision()

        # Update abilities
        for ability in self.player.abilities:
            ability.update(dt, self.player, self.enemies, self.projectiles, self.particles)

        self._update_enemies(dt)
        self._update_projectiles(dt)

        # Update boss (DungeonState-specific)
        if self.boss.alive:
            # Check if boss just started charging to trigger screen shake
            was_charging = getattr(self.boss, 'charging', False)
            self.boss.update(dt, self.player, self.tilemap)
            # If boss just started charging, trigger screen shake
            if not was_charging and getattr(self.boss, 'charging', False):
                self.camera.shake(8, 0.4)

        # Boss intro zoom timer
        if self._boss_intro_timer > 0:
            self._boss_intro_timer -= dt
            if self._boss_intro_timer <= 0:
                self.camera.start_zoom(1.0, speed=0.5)  # Zoom back to normal

        self.camera.update_zoom(dt)

        # Detect boss phase change -> screen flash
        boss_phase = getattr(self.boss, 'phase', 1)
        if boss_phase != self._boss_prev_phase:
            self._boss_prev_phase = boss_phase
            self._screen_flash_alpha = 200
            self.camera.shake(10, 0.5)
            get_sound_manager().play_boss_roar()

        # Decay screen flash
        if self._screen_flash_alpha > 0:
            self._screen_flash_alpha = max(0, self._screen_flash_alpha - 400 * dt)

        # Handle vine summons from Forest Guardian
        if hasattr(self.boss, 'pending_summons') and self.boss.pending_summons:
            from zelda_miloutte.entities.vine_snapper import VineSnapper
            for summon_data in self.boss.pending_summons:
                vs = VineSnapper(summon_data['x'], summon_data['y'])
                self.enemies.append(vs)
            self.boss.pending_summons = []

        # Combat - shared for regular enemies, plus boss-specific
        self._update_combat(dt)

        # Boss-specific combat (DungeonState-specific)
        player = self.player
        if player.attacking and player.sword_rect:
            # Check invulnerable flag (e.g., Sand Worm when burrowed)
            if self.boss.alive and player.sword_rect.colliderect(self.boss.rect):
                if not getattr(self.boss, 'invulnerable', False):
                    self.boss.take_damage(player.attack_power)
                    # Apply reduced knockback to boss (it's big and heavy)
                    self.boss.apply_knockback(player.center_x, player.center_y, 100)
                    # Emit sword sparks on boss hit
                    self.particles.emit_sword_sparks(self.boss.center_x, self.boss.center_y)

        # Enemy collision - shared, then boss-specific
        self._update_enemy_collision()

        # Handle root slam AOE damage from Forest Guardian
        if hasattr(self.boss, 'root_slam_active') and self.boss.root_slam_active:
            dist = ((player.center_x - self.boss.center_x)**2 + (player.center_y - self.boss.center_y)**2)**0.5
            if dist < 60:
                if player.take_damage(self.boss.damage):
                    self.camera.shake(6, 0.3)
                player.apply_knockback(self.boss.center_x, self.boss.center_y, 250)

        # Handle emerge slam AOE damage from Sand Worm
        if hasattr(self.boss, 'emerge_slam_active') and self.boss.emerge_slam_active:
            dist = ((player.center_x - self.boss.center_x)**2 + (player.center_y - self.boss.center_y)**2)**0.5
            if dist < 80:
                if player.take_damage(self.boss.damage):
                    self.camera.shake(6, 0.3)
                player.apply_knockback(self.boss.center_x, self.boss.center_y, 250)

        # Handle sand burst particles from Sand Worm
        if hasattr(self.boss, 'pending_sand_burst') and self.boss.pending_sand_burst:
            self.particles.emit_sand_burst(self.boss.center_x, self.boss.center_y)
            self.boss.pending_sand_burst = False

        # Handle fire breath damage from Inferno Drake
        if hasattr(self.boss, 'fire_breath_active') and self.boss.fire_breath_active:
            if hasattr(self.boss, 'fire_breath_rect') and self.boss.fire_breath_rect:
                if player.rect.colliderect(self.boss.fire_breath_rect):
                    if player.take_damage(self.boss.damage):
                        self.camera.shake(6, 0.3)
                    player.apply_knockback(self.boss.center_x, self.boss.center_y, 250)

        # Handle meteor attacks from Inferno Drake
        if hasattr(self.boss, 'pending_meteors'):
            for meteor in self.boss.pending_meteors[:]:
                meteor['timer'] -= dt
                if meteor['timer'] <= 0 and not meteor['exploded']:
                    # Meteor explodes - check AOE damage
                    meteor['exploded'] = True
                    explosion_radius = 60
                    dist = ((player.center_x - meteor['x'])**2 + (player.center_y - meteor['y'])**2)**0.5
                    if dist < explosion_radius:
                        if player.take_damage(self.boss.damage):
                            self.camera.shake(8, 0.4)
                        player.apply_knockback(meteor['x'], meteor['y'], 300)
                    # Emit fire particles
                    self.particles.emit(
                        meteor['x'], meteor['y'],
                        count=20,
                        color=[(255, 120, 30), (200, 80, 20), (255, 200, 50)],
                        speed_range=(100, 200),
                        lifetime_range=(0.3, 0.6),
                        size_range=(3, 6),
                        gravity=150
                    )
            # Remove exploded meteors
            self.boss.pending_meteors = [m for m in self.boss.pending_meteors if not m['exploded']]

        # Boss vs player (DungeonState-specific) - skip if burrowed
        if self.boss.alive and not getattr(self.boss, 'invulnerable', False) and player.collides_with(self.boss):
            if player.take_damage(self.boss.damage):
                # Trigger screen shake on damage
                self.camera.shake(5, 0.3)
                self._trigger_damage_vignette()
            # Apply stronger knockback to player from boss
            player.apply_knockback(self.boss.center_x, self.boss.center_y, 350)

        # Separate player from boss so player can't get stuck inside it (skip if burrowed)
        if self.boss.alive and not getattr(self.boss, 'invulnerable', False):
            prect = player.rect
            brect = self.boss.rect
            if prect.colliderect(brect):
                overlap_x = min(prect.right, brect.right) - max(prect.left, brect.left)
                overlap_y = min(prect.bottom, brect.bottom) - max(prect.top, brect.top)
                if overlap_x > 0 and overlap_y > 0:
                    if overlap_x < overlap_y:
                        if player.center_x < self.boss.center_x:
                            player.x -= overlap_x
                        else:
                            player.x += overlap_x
                    else:
                        if player.center_y < self.boss.center_y:
                            player.y -= overlap_y
                        else:
                            player.y += overlap_y

        # Shared item and cleanup logic
        self._update_items(dt)
        self._check_hazards()
        self._cleanup_dead()

        # Update companion (if exists)
        self._update_companion(dt)

        # Check companion petting (if exists)
        self._check_companion_pet()

        # Boss defeated (DungeonState-specific)
        if not self.boss.alive and not self.victory:
            if not self.boss_death_emitted:
                self.particles.emit_boss_death(self.boss.center_x, self.boss.center_y)
                self.boss_death_emitted = True
                self.camera.shake(12, 0.8)
                get_sound_manager().play_victory_fanfare()
                get_sound_manager().stop_music()
                drop = self.boss.get_drop()
                if drop is not None:
                    item = Item(self.boss.rect.centerx, self.boss.rect.centery, drop)
                    self.items.append(item)
                # Grant boss XP
                from zelda_miloutte.ui.floating_text import FloatingText
                xp_val = getattr(self.boss, 'xp_value', 50)
                leveled = self.player.gain_xp(xp_val)
                self.floating_texts.append(FloatingText(
                    f"+{xp_val} XP", self.boss.center_x, self.boss.center_y, (100, 200, 255), size=24
                ))
                if leveled:
                    self.floating_texts.append(FloatingText(
                        "LEVEL UP!", self.player.center_x, self.player.center_y - 20,
                        (255, 255, 100), size=28, duration=1.5
                    ))
                # Track boss defeat for quests
                boss_id = getattr(self.boss, 'boss_id', None)
                if boss_id is None:
                    # Infer boss_id from class name or config
                    class_name = type(self.boss).__name__
                    boss_id_map = {
                        "Boss": "boss_1",
                        "ForestGuardian": "forest_guardian",
                        "SandWorm": "sand_worm",
                        "InfernoDrake": "inferno_drake",
                    }
                    boss_id = boss_id_map.get(class_name, class_name.lower())
                    # Check if this is boss_2 (Ice Demon) via config
                    if class_name == "Boss" and self._boss_config and self._boss_config.get("color") == ICE_BLUE:
                        boss_id = "boss_2"
                if boss_id not in self.game.world_state["defeated_bosses"]:
                    self.game.world_state["defeated_bosses"].append(boss_id)
                self.game.quest_manager.update_objective("defeat_boss", boss_id)
                # Unlock ability if this boss grants one
                from zelda_miloutte.abilities import BOSS_ABILITY_UNLOCKS
                if boss_id in BOSS_ABILITY_UNLOCKS:
                    ability_name = BOSS_ABILITY_UNLOCKS[boss_id]
                    if self.player.unlock_ability(ability_name):
                        # Show notification for new ability
                        from zelda_miloutte.ui.floating_text import FloatingText
                        from zelda_miloutte.abilities import create_ability
                        ability = create_ability(ability_name)
                        if ability:
                            self.floating_texts.append(FloatingText(
                                f"New Ability: {ability.display_name}!",
                                self.player.center_x, self.player.center_y - 40,
                                (255, 200, 100), size=24, duration=2.0
                            ))
                # Auto-complete any quests whose objectives are now met
                for quest in self.game.quest_manager.get_active_quests():
                    if self.game.quest_manager.check_quest_complete(quest.id):
                        rewards = self.game.quest_manager.complete_quest(quest.id)
                        self.game.world_state["story_progress"] = len(
                            self.game.quest_manager.get_completed_quests()
                        )
                        self.show_quest_notification(f"Quest Complete: {quest.name}!")
                        if rewards and "xp" in rewards:
                            leveled = self.player.gain_xp(rewards["xp"])
                            self.floating_texts.append(FloatingText(
                                f"+{rewards['xp']} XP", self.player.center_x,
                                self.player.center_y - 20, (100, 200, 255)
                            ))
                            if leveled:
                                self.floating_texts.append(FloatingText(
                                    "LEVEL UP!", self.player.center_x,
                                    self.player.center_y - 40, (255, 255, 100),
                                    size=28, duration=1.5
                                ))
                        if rewards and "keys" in rewards:
                            self.player.keys += rewards.get("keys", 0)
            self.victory = True
            self.victory_timer = 0.0

        # Check exit (door tile) (DungeonState-specific)
        tile_type = self.tilemap.get_tile_at(player.center_x, player.center_y)
        if tile_type is not None and tile_type.name == "DOOR":
            # Exit dungeon

            def exit_dungeon():
                self._copy_stats_back()
                self.game.pop_state()

            self.game.transition_to(exit_dungeon)
            return

        # Check player death
        self._check_player_death()

        # Update camera, particles, floating text, polish
        self._update_camera(dt)
        self._update_particles(dt)
        self._update_floating_texts(dt)
        self._update_damage_vignette(dt)
        self._update_item_glow(dt)
        self._update_minimap(dt)

    def draw(self, surface):
        # Draw tilemap, chests, items, enemies, player, particles
        self.tilemap.draw(surface, self.camera)

        # Draw puzzles (before enemies so they appear under entities)
        self._draw_puzzles(surface)

        for chest in self.chests:
            chest.draw(surface, self.camera)
        for item in self.items:
            item.draw(surface, self.camera)
        for enemy in self.enemies:
            enemy.draw(surface, self.camera)

        # Draw boss (DungeonState-specific)
        if self.boss.alive or self.boss.dying:
            self.boss.draw(surface, self.camera)

        # Draw meteor warnings (Inferno Drake)
        if hasattr(self.boss, 'pending_meteors'):
            for meteor in self.boss.pending_meteors:
                if not meteor['exploded']:
                    screen_x = int(meteor['x'] - self.camera.x)
                    screen_y = int(meteor['y'] - self.camera.y)
                    # Warning circle (orange)
                    radius = 30
                    if meteor['timer'] > 0:
                        # Pulsing warning
                        pulse = int(abs(meteor['timer'] * 10 % 1.0 - 0.5) * 100) + 150
                        color = (255, pulse, 0, 180)
                        temp_surf = pygame.Surface((radius * 2 + 10, radius * 2 + 10), pygame.SRCALPHA)
                        pygame.draw.circle(temp_surf, color, (radius + 5, radius + 5), radius, 3)
                        surface.blit(temp_surf, (screen_x - radius - 5, screen_y - radius - 5))

        # Draw player and particles
        self.player.draw(surface, self.camera)
        self.particles.draw(surface, self.camera)
        # Floating texts
        for ft in self.floating_texts:
            ft.draw(surface, self.camera)

        # Draw HUD with boss health bar (DungeonState-specific)
        self.hud.draw(surface, self.player, self.boss if self.boss.alive else None)

        # Draw minimap
        self._draw_minimap(surface)

        # Victory overlay (DungeonState-specific)
        if self.victory:
            if self.victory_font is None:
                self.victory_font = pygame.font.Font(None, 48)
            # Dark overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            alpha = min(180, int(self.victory_timer / self.victory_duration * 180))
            overlay.fill((0, 0, 0, alpha))
            surface.blit(overlay, (0, 0))
            # Victory text
            text = self.victory_font.render("Victory!", True, GOLD)
            tx = (SCREEN_WIDTH - text.get_width()) // 2
            ty = SCREEN_HEIGHT // 2 - 20
            surface.blit(text, (tx, ty))
            sub_font = pygame.font.Font(None, 28)
            sub = sub_font.render(self.victory_text, True, WHITE)
            surface.blit(sub, ((SCREEN_WIDTH - sub.get_width()) // 2, ty + 50))
