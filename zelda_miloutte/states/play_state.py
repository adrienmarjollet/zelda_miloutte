import pygame
from .gameplay_state import GameplayState
from ..entities.player import Player
from ..camera import Camera
from ..world.tilemap import TileMap
from ..world.maps import AREAS, DUNGEON2, DUNGEON2_SPAWNS
from ..world.tile import TileType
from ..hud import HUD
from ..settings import (
    TILE_SIZE, BOSS2_HP, BOSS2_SPEED, BOSS2_CHASE_SPEED, BOSS2_CHARGE_SPEED, BOSS2_DAMAGE, ICE_BLUE, WHITE,
)
from ..sounds import get_sound_manager
from ..particles import ParticleSystem


class PlayState(GameplayState):
    def __init__(self, game, area_id="overworld", load_data=None):
        super().__init__(game)
        self.area_id = area_id

        # Load map and spawns from area registry
        area_data = AREAS[area_id]
        self.tilemap = TileMap(area_data["map"])
        spawn = area_data["spawns"]["player"]
        self.player = Player(spawn[0] * TILE_SIZE, spawn[1] * TILE_SIZE)
        self.camera = Camera(self.tilemap.pixel_width, self.tilemap.pixel_height)
        self.enemies = []
        self.items = []
        self.chests = []
        self.projectiles = []
        self.hud = HUD()
        self.particles = ParticleSystem()

        # World map
        from ..ui.world_map import WorldMap
        self.world_map = WorldMap()

        # Area name banner
        self.area_banner_timer = 2.0  # Show for 2 seconds
        self.area_name = area_data["name"]

        # Initialize enemies, items, chests, signs, and NPCs
        self._spawn_enemies()
        self._spawn_items()
        self._spawn_chests()
        self._spawn_signs()
        self._spawn_npcs()
        # Note: Campfires added to world but spawn method not yet implemented

        # Night ghost spawning tracker
        self._night_ghost_spawned = False
        self._night_ghost_timer = 0.0

        # Restore player stats from save data
        if load_data is not None:
            pdata = load_data.get("player", {})
            self.player.hp = pdata.get("hp", self.player.hp)
            self.player.max_hp = pdata.get("max_hp", self.player.max_hp)
            self.player.mp = pdata.get("mp", self.player.mp)
            self.player.max_mp = pdata.get("max_mp", self.player.max_mp)
            self.player.keys = pdata.get("keys", self.player.keys)
            self.player.level = pdata.get("level", 1)
            self.player.xp = pdata.get("xp", 0)
            self.player.xp_to_next = pdata.get("xp_to_next", 100)
            self.player.base_attack = pdata.get("base_attack", 0)
            self.player.base_defense = pdata.get("base_defense", 0)
            self.player.gold = pdata.get("gold", 0)
            # Restore inventory
            if "inventory" in pdata:
                from ..data.inventory import Inventory
                self.player.inventory = Inventory.from_dict(pdata["inventory"])
            # Restore unlocked abilities
            if "unlocked_abilities" in pdata:
                self.player.unlocked_abilities = pdata["unlocked_abilities"]
                # Recreate ability instances from unlocked names
                from ..abilities import create_ability
                self.player.abilities = []
                for ability_name in self.player.unlocked_abilities:
                    ability = create_ability(ability_name)
                    if ability is not None:
                        self.player.abilities.append(ability)
            # Restore minimap visited tiles
            visited = load_data.get("visited_tiles")
            if visited:
                self.minimap.load_save_data(visited)
            # Restore companion
            if "companion" in load_data:
                from ..entities.companion import create_companion
                companion_data = load_data["companion"]
                companion_type = companion_data.get("type", "cat")
                self.companion = create_companion(companion_type, self.player.x - 30, self.player.y)
                self.companion.pet_cooldown = companion_data.get("pet_cooldown", 0.0)

    def enter(self):
        """Called when entering this state."""
        area_data = AREAS[self.area_id]
        get_sound_manager().play_music(area_data["music"])
        # Track area visits for quest objectives
        self.game.world_state["current_area"] = self.area_id
        self.game.quest_manager.update_objective("visit", self.area_id)
        # Track area visit for achievements
        self.game.achievement_manager.on_area_enter(self.area_id)
        # Auto-start side_2 (goblin slayer) since it has no prerequisites
        self.game.quest_manager.start_quest("side_2")
        # Clear fire trails on area entry to prevent visual artifacts from previous visits
        self.fire_trails = []

    def _spawn_enemies(self):
        from ..entities.enemy import Enemy
        from ..entities.archer import Archer
        from ..entities.shadow_stalker import ShadowStalker
        from ..entities.vine_snapper import VineSnapper
        from ..entities.scorpion import Scorpion
        from ..entities.mummy import Mummy
        from ..entities.fire_imp import FireImp
        from ..entities.magma_golem import MagmaGolem
        from ..entities.ice_wraith import IceWraith
        from ..entities.frost_golem import FrostGolem
        from ..ng_plus import scale_enemy_stats
        self.enemies = []
        area_spawns = AREAS[self.area_id]["spawns"]
        for edata in area_spawns.get("enemies", []):
            # Check enemy type
            if edata.get("type") == "archer":
                e = Archer(
                    edata["x"] * TILE_SIZE, edata["y"] * TILE_SIZE,
                    edata.get("patrol", []),
                )
            elif edata.get("type") == "shadow_stalker":
                e = ShadowStalker(edata["x"] * TILE_SIZE, edata["y"] * TILE_SIZE)
            elif edata.get("type") == "vine_snapper":
                e = VineSnapper(edata["x"] * TILE_SIZE, edata["y"] * TILE_SIZE)
            elif edata.get("type") == "scorpion":
                e = Scorpion(edata["x"] * TILE_SIZE, edata["y"] * TILE_SIZE)
            elif edata.get("type") == "mummy":
                e = Mummy(edata["x"] * TILE_SIZE, edata["y"] * TILE_SIZE)
            elif edata.get("type") == "fire_imp":
                e = FireImp(edata["x"] * TILE_SIZE, edata["y"] * TILE_SIZE)
            elif edata.get("type") == "magma_golem":
                e = MagmaGolem(edata["x"] * TILE_SIZE, edata["y"] * TILE_SIZE)
            elif edata.get("type") == "ice_wraith":
                e = IceWraith(edata["x"] * TILE_SIZE, edata["y"] * TILE_SIZE)
            elif edata.get("type") == "frost_golem":
                e = FrostGolem(edata["x"] * TILE_SIZE, edata["y"] * TILE_SIZE)
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

    def _spawn_items(self):
        from ..entities.item import Item
        self.items = []
        area_spawns = AREAS[self.area_id]["spawns"]
        for idata in area_spawns.get("items", []):
            item = Item(
                idata["x"] * TILE_SIZE, idata["y"] * TILE_SIZE,
                idata["type"],
            )
            self.items.append(item)

    def _spawn_chests(self):
        from ..entities.chest import Chest
        self.chests = []
        area_spawns = AREAS[self.area_id]["spawns"]
        for cdata in area_spawns.get("chests", []):
            chest = Chest(
                cdata["x"] * TILE_SIZE, cdata["y"] * TILE_SIZE,
                cdata["contents"],
            )
            self.chests.append(chest)

    def _spawn_signs(self):
        from ..entities.sign import Sign
        self.signs = []
        area_spawns = AREAS[self.area_id]["spawns"]
        for sdata in area_spawns.get("signs", []):
            sign = Sign(
                sdata["x"] * TILE_SIZE, sdata["y"] * TILE_SIZE,
                sdata["text"],
            )
            self.signs.append(sign)

    def _spawn_npcs(self):
        from ..entities.npc import NPC
        self.npcs = []
        area_spawns = AREAS[self.area_id]["spawns"]
        for ndata in area_spawns.get("npcs", []):
            npc = NPC(
                ndata["x"] * TILE_SIZE, ndata["y"] * TILE_SIZE,
                name=ndata["name"],
                variant=ndata.get("variant", "villager"),
                dialogue_tree=ndata.get("dialogue", {"default": ["..."]}),
                quest_id=ndata.get("quest_id"),
                shop_id=ndata.get("shop_id"),
            )
            self.npcs.append(npc)

    def _check_area_transition(self):
        """Check if player is on a transition tile and trigger area swap."""
        player = self.player
        tile_type = self.tilemap.get_tile_at(player.center_x, player.center_y)

        if tile_type is None:
            return

        direction = None
        if tile_type == TileType.TRANSITION_E:
            direction = "east"
        elif tile_type == TileType.TRANSITION_W:
            direction = "west"
        elif tile_type == TileType.TRANSITION_N:
            direction = "north"
        elif tile_type == TileType.TRANSITION_S:
            direction = "south"

        if direction is None:
            return

        connections = AREAS[self.area_id].get("connections", {})
        if direction not in connections:
            return

        conn = connections[direction]
        target_area = conn["area"]
        spawn_edge = conn["spawn_edge"]

        # Area gating based on story progress
        qm = self.game.quest_manager
        gate_msg = None
        if target_area == "forest":
            q = qm.get_quest("story_1")
            if q and q.status == "inactive":
                gate_msg = "Talk to Elder Mira before heading to the forest."
        elif target_area == "desert":
            q = qm.get_quest("story_2")
            if q and q.status != "completed":
                gate_msg = "Cleanse the forest before entering the desert."
        elif target_area == "volcano":
            q = qm.get_quest("story_4")
            if q and q.status != "completed":
                gate_msg = "Defeat the Sand Worm before entering the volcano."

        if gate_msg:
            self.textbox.show(gate_msg)
            # Push player back slightly
            if direction == "east":
                self.player.x -= 8
            elif direction == "west":
                self.player.x += 8
            elif direction == "north":
                self.player.y += 8
            elif direction == "south":
                self.player.y -= 8
            return

        # Calculate current player position in tile coordinates
        player_tile_x = int(player.center_x / TILE_SIZE)
        player_tile_y = int(player.center_y / TILE_SIZE)

        # Store player stats
        player_data = {
            "hp": player.hp,
            "max_hp": player.max_hp,
            "mp": player.mp,
            "max_mp": player.max_mp,
            "keys": player.keys,
            "level": player.level,
            "xp": player.xp,
            "xp_to_next": player.xp_to_next,
            "base_attack": player.base_attack,
            "base_defense": player.base_defense,
            "gold": player.gold,
            "inventory": player.inventory.to_dict(),
            "unlocked_abilities": player.unlocked_abilities,
        }

        # Carry minimap visited tiles across transitions
        minimap_data = self.minimap.get_save_data()

        # Carry companion across transitions
        companion_data = None
        if self.companion is not None:
            companion_data = self.companion.to_dict()

        def do_transition():
            # Create new PlayState for target area
            load_data = {"player": player_data}
            if companion_data is not None:
                load_data["companion"] = companion_data
            new_state = PlayState(self.game, area_id=target_area, load_data=load_data)

            # Carry minimap data
            new_state.minimap.load_save_data(minimap_data)

            # Position player on the correct edge of the new area
            target_map = AREAS[target_area]["map"]
            map_width = len(target_map[0])
            map_height = len(target_map)

            if spawn_edge == "west":
                new_state.player.x = 1 * TILE_SIZE
                new_state.player.y = player_tile_y * TILE_SIZE
            elif spawn_edge == "east":
                new_state.player.x = (map_width - 2) * TILE_SIZE
                new_state.player.y = player_tile_y * TILE_SIZE
            elif spawn_edge == "north":
                new_state.player.y = 1 * TILE_SIZE
                new_state.player.x = player_tile_x * TILE_SIZE
            elif spawn_edge == "south":
                new_state.player.y = (map_height - 2) * TILE_SIZE
                new_state.player.x = player_tile_x * TILE_SIZE

            self.game.change_state(new_state)

        self.game.transition_to(do_transition)

    def handle_event(self, event):
        # Shop UI intercepts all events when active
        if self.shop_ui.active:
            self.shop_ui.handle_event(event)
            return

        # World map intercepts events when active
        if self.world_map.active:
            result = self.world_map.handle_event(event)
            if result == "close":
                self.world_map.close()
            elif result and result.startswith("fast_travel:"):
                target_area = result.split(":")[1]
                self._handle_fast_travel(target_area)
            return

        if self.dialogue_box and self.dialogue_box.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.dialogue_box.move_choice(-1)
                elif event.key == pygame.K_DOWN:
                    self.dialogue_box.move_choice(1)

    def update(self, dt):
        # Update area banner timer
        if self.area_banner_timer > 0:
            self.area_banner_timer -= dt

        # Shop UI pauses gameplay while open
        if self.shop_ui.active:
            self.shop_ui.update(dt)
            return

        # World map pauses gameplay while open
        if self.world_map.active:
            self.world_map.update(dt)
            return

        # Toggle world map with M key
        if self.game.input.toggle_world_map:
            self.world_map.open(self.area_id)
            return

        # Check for pause
        if self.game.input.pause:
            from .pause_state import PauseState
            self.game.push_state(PauseState(self.game))
            return

        # If dialogue box is active, update it (pauses game)
        if self.dialogue_box and self.dialogue_box.active:
            self._update_dialogue_box(dt)
            return

        # If textbox is active, only update textbox (pauses game)
        if self.textbox.active:
            self._update_textbox(dt)
            return

        # Update time system (overworld only, not paused during menus/dialogue)
        self.game.time_system.update(dt)

        # Day/night gameplay effects
        self._update_night_enemies()
        self._update_npc_night_state()
        self._update_campfires(dt)

        # Update NPC dialogue states based on quest progress
        for npc in self.npcs:
            npc.update_dialogue_state(self.game.quest_manager)

        # Check for campfire interaction first, then NPC, then sign
        if not self._check_campfire_interaction():
            if not self._check_npc_interaction():
                self._check_sign_interaction()

        # Hit stop: freeze gameplay briefly on impactful hits
        if self._update_hitstop(dt):
            self._update_camera(dt)
            self._update_particles(dt)
            self._update_floating_texts(dt)
            return

        # Shared gameplay updates
        self._update_movement(dt)

        # Update abilities
        for ability in self.player.abilities:
            ability.update(dt, self.player, self.enemies, self.projectiles, self.particles)

        self._update_enemies(dt)
        self._update_combat(dt)
        self._update_enemy_collision()
        self._update_projectiles(dt)
        self._update_items(dt)
        self._check_hazards()
        self._cleanup_dead()

        # Update companion (if exists)
        self._update_companion(dt)

        # Check companion petting (if exists)
        self._check_companion_pet()

        # Check area transitions
        self._check_area_transition()

        # Check dungeon entrances (PlayState-specific)
        player = self.player
        tile_type = self.tilemap.get_tile_at(player.center_x, player.center_y)
        if tile_type is not None and tile_type.name == "DUNGEON_ENTRANCE":
            if player.keys > 0:
                player.keys -= 1
                get_sound_manager().play_dungeon_enter()

                # Check which area we're in to determine which dungeon
                if self.area_id == "forest":
                    def enter_forest_dungeon():
                        from .dungeon_state import DungeonState
                        from ..world.maps import FOREST_DUNGEON, FOREST_DUNGEON_SPAWNS
                        from ..entities.forest_guardian import ForestGuardian
                        self.game.push_state(DungeonState(
                            self.game, self,
                            dungeon_map=FOREST_DUNGEON,
                            dungeon_spawns=FOREST_DUNGEON_SPAWNS,
                            boss_class=ForestGuardian,
                            victory_message="The Forest Guardian is defeated! The corruption fades..."
                        ))
                    self.game.transition_to(enter_forest_dungeon)
                elif self.area_id == "desert":
                    def enter_desert_dungeon():
                        from .dungeon_state import DungeonState
                        from ..world.maps import DESERT_DUNGEON, DESERT_DUNGEON_SPAWNS
                        from ..entities.sand_worm import SandWorm
                        self.game.push_state(DungeonState(
                            self.game, self,
                            dungeon_map=DESERT_DUNGEON,
                            dungeon_spawns=DESERT_DUNGEON_SPAWNS,
                            boss_class=SandWorm,
                            victory_message="The Sand Worm is defeated! The desert is safe..."
                        ))
                    self.game.transition_to(enter_desert_dungeon)
                elif self.area_id == "volcano":
                    def enter_volcano_dungeon():
                        from .dungeon_state import DungeonState
                        from ..world.maps import VOLCANO_DUNGEON, VOLCANO_DUNGEON_SPAWNS
                        from ..entities.inferno_drake import InfernoDrake
                        self.game.push_state(DungeonState(
                            self.game, self,
                            dungeon_map=VOLCANO_DUNGEON,
                            dungeon_spawns=VOLCANO_DUNGEON_SPAWNS,
                            boss_class=InfernoDrake,
                            victory_message="The Inferno Drake is slain! The seal is restored!"
                        ))
                    self.game.transition_to(enter_volcano_dungeon)
                elif self.area_id == "frozen_peaks":
                    def enter_ice_cavern():
                        from .dungeon_state import DungeonState
                        from ..world.maps import ICE_CAVERN, ICE_CAVERN_SPAWNS
                        from ..sprites.boss_sprites import get_boss2_frames_phase1, get_boss2_frames_phase2
                        # Configure Ice Cavern boss (Crystal Dragon variant of Boss)
                        ice_boss_config = {
                            'hp': BOSS2_HP,
                            'speed': BOSS2_SPEED,
                            'chase_speed': BOSS2_CHASE_SPEED,
                            'charge_speed': BOSS2_CHARGE_SPEED,
                            'damage': BOSS2_DAMAGE,
                            'frames_phase1_fn': get_boss2_frames_phase1,
                            'frames_phase2_fn': get_boss2_frames_phase2,
                            'color': ICE_BLUE,
                        }
                        self.game.push_state(DungeonState(
                            self.game, self,
                            dungeon_map=ICE_CAVERN,
                            dungeon_spawns=ICE_CAVERN_SPAWNS,
                            boss_config=ice_boss_config,
                            victory_message="The Crystal Dragon is defeated! The final seal is restored!"
                        ))
                    self.game.transition_to(enter_ice_cavern)
                else:
                    # Default dungeon (overworld)
                    def enter_dungeon():
                        from .dungeon_state import DungeonState
                        self.game.push_state(DungeonState(self.game, self))

                    self.game.transition_to(enter_dungeon)
        elif tile_type is not None and tile_type.name == "DUNGEON_ENTRANCE_2":
            if player.keys > 0:
                player.keys -= 1
                get_sound_manager().play_dungeon_enter()

                def enter_dungeon2():
                    from .dungeon_state import DungeonState
                    from ..sprites.boss_sprites import get_boss2_frames_phase1, get_boss2_frames_phase2
                    # Configure Boss 2 (Ice Demon)
                    boss2_config = {
                        'hp': BOSS2_HP,
                        'speed': BOSS2_SPEED,
                        'chase_speed': BOSS2_CHASE_SPEED,
                        'charge_speed': BOSS2_CHARGE_SPEED,
                        'damage': BOSS2_DAMAGE,
                        'frames_phase1_fn': get_boss2_frames_phase1,
                        'frames_phase2_fn': get_boss2_frames_phase2,
                        'color': ICE_BLUE,
                    }
                    self.game.push_state(DungeonState(
                        self.game, self,
                        dungeon_map=DUNGEON2,
                        dungeon_spawns=DUNGEON2_SPAWNS,
                        boss_config=boss2_config,
                        victory_message="The ice demon is vanquished!"
                    ))

                self.game.transition_to(enter_dungeon2)

        elif tile_type is not None and tile_type.name == "DUNGEON_3D_ENTRANCE":
            if player.keys > 0:
                player.keys -= 1
                get_sound_manager().play_dungeon_enter()

                def enter_3d_dungeon():
                    from .dungeon3d_state import Dungeon3DState
                    self.game.push_state(Dungeon3DState(self.game, self))

                self.game.transition_to(enter_3d_dungeon)

        # Check player death
        self._check_player_death()

        # Update camera, particles, floating text, ambient
        self._update_camera(dt)
        self._update_particles(dt)
        self._update_floating_texts(dt)
        self._update_ambient_particles(dt)
        self._update_damage_vignette(dt)
        self._update_quest_notification(dt)
        self._update_item_glow(dt)
        self._update_night_chest_glow(dt)
        self._update_minimap(dt)
        self._update_achievement_popups(dt)

    def draw(self, surface):
        # Use base class drawing
        self._draw_world(surface)

        # Draw area name banner if timer is active
        if self.area_banner_timer > 0:
            self._draw_area_banner(surface)

        # Draw world map overlay (on top of everything)
        if self.world_map.active:
            self.world_map.draw(
                surface, self.area_id, self.game.world_state,
                self.game.quest_manager
            )

    def _handle_npc_choice(self, npc, choice_index):
        """Handle dialogue choice — start/complete quests via quest_manager."""
        qm = self.game.quest_manager
        if not npc.quest_id:
            return
        quest = qm.get_quest(npc.quest_id)
        if quest is None:
            return

        if choice_index == 0:  # Accept / positive choice
            if quest.status == "inactive":
                # Start the quest
                if qm.start_quest(npc.quest_id):
                    self.show_quest_notification(f"New Quest: {quest.name}!")
                    # Update objective for "talk" type quests
                    qm.update_objective("talk", npc.name.split()[0].lower())
                    # Check for immediate completion (talk-only quests)
                    if qm.check_quest_complete(npc.quest_id):
                        rewards = qm.complete_quest(npc.quest_id)
                        self._apply_quest_rewards(rewards)
                        self.show_quest_notification(f"Quest Complete: {quest.name}!")
                    self.game.world_state["story_progress"] = len(qm.get_completed_quests())
            elif quest.status == "active":
                # Try to complete if objectives met
                if qm.check_quest_complete(npc.quest_id):
                    rewards = qm.complete_quest(npc.quest_id)
                    self._apply_quest_rewards(rewards)
                    self.game.world_state["story_progress"] = len(qm.get_completed_quests())

    def _apply_quest_rewards(self, rewards):
        """Apply quest rewards to the player."""
        if rewards is None:
            return
        from ..ui.floating_text import FloatingText
        if "xp" in rewards:
            leveled = self.player.gain_xp(rewards["xp"])
            self.floating_texts.append(FloatingText(
                f"+{rewards['xp']} XP", self.player.center_x, self.player.center_y - 20,
                (100, 200, 255), size=24
            ))
            if leveled:
                self.floating_texts.append(FloatingText(
                    "LEVEL UP!", self.player.center_x, self.player.center_y - 40,
                    (255, 255, 100), size=28, duration=1.5
                ))
        if "keys" in rewards:
            self.player.keys += rewards["keys"]

    def _handle_fast_travel(self, target_area):
        """Handle fast travel from the world map."""
        # Can't fast travel to current area
        if target_area == self.area_id:
            self.world_map.show_message("You are already here!")
            return

        # Check if target area is unlocked
        if not self.world_map._is_area_unlocked(target_area, self.game.quest_manager):
            self.world_map.show_message("This area is locked!")
            return

        # Only allow fast travel from safe zones (village area or near dungeon entrances)
        # For simplicity: allow from overworld (village) or any area's spawn area
        safe = False
        if self.area_id == "overworld":
            # Village is always safe
            safe = True
        else:
            # Check if player is near the area's spawn point (within 5 tiles)
            area_data = AREAS[self.area_id]
            spawn = area_data["spawns"]["player"]
            spawn_px = spawn[0] * TILE_SIZE
            spawn_py = spawn[1] * TILE_SIZE
            dist = ((self.player.center_x - spawn_px) ** 2 + (self.player.center_y - spawn_py) ** 2) ** 0.5
            if dist < 5 * TILE_SIZE:
                safe = True

        if not safe:
            self.world_map.show_message("Find a safe zone to fast travel!")
            return

        # Close world map and travel
        self.world_map.close()

        # Store player stats
        player_data = {
            "hp": self.player.hp,
            "max_hp": self.player.max_hp,
            "mp": self.player.mp,
            "max_mp": self.player.max_mp,
            "keys": self.player.keys,
            "level": self.player.level,
            "xp": self.player.xp,
            "xp_to_next": self.player.xp_to_next,
            "base_attack": self.player.base_attack,
            "base_defense": self.player.base_defense,
            "gold": self.player.gold,
            "inventory": self.player.inventory.to_dict(),
            "unlocked_abilities": self.player.unlocked_abilities,
        }

        # Carry minimap visited tiles
        minimap_data = self.minimap.get_save_data()

        # Carry companion across fast travel
        companion_data = None
        if self.companion is not None:
            companion_data = self.companion.to_dict()

        def do_fast_travel():
            load_data = {"player": player_data}
            if companion_data is not None:
                load_data["companion"] = companion_data
            new_state = PlayState(self.game, area_id=target_area, load_data=load_data)
            new_state.minimap.load_save_data(minimap_data)
            self.game.change_state(new_state)

        self.game.transition_to(do_fast_travel)

    def _draw_area_banner(self, surface):
        """Draw area name banner with fade-in/fade-out."""
        # Calculate alpha based on timer (fade in first 0.5s, fade out last 0.5s)
        if self.area_banner_timer > 1.5:
            alpha = int((2.0 - self.area_banner_timer) / 0.5 * 255)
        elif self.area_banner_timer < 0.5:
            alpha = int(self.area_banner_timer / 0.5 * 255)
        else:
            alpha = 255

        alpha = max(0, min(255, alpha))

        # Create text surface
        font = pygame.font.Font(None, 48)
        text_surf = font.render(self.area_name, True, WHITE)

        # Apply alpha
        text_surf.set_alpha(alpha)

        # Draw centered
        rect = text_surf.get_rect(center=(surface.get_width() // 2, 100))
        surface.blit(text_surf, rect)
