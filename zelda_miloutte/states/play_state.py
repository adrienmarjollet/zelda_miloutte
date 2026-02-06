import pygame
from zelda_miloutte.states.gameplay_state import GameplayState
from zelda_miloutte.entities.player import Player
from zelda_miloutte.camera import Camera
from zelda_miloutte.world.tilemap import TileMap
from zelda_miloutte.world.maps import AREAS, DUNGEON2, DUNGEON2_SPAWNS
from zelda_miloutte.world.tile import TileType
from zelda_miloutte.hud import HUD
from zelda_miloutte.settings import (
    TILE_SIZE, BOSS2_HP, BOSS2_SPEED, BOSS2_CHASE_SPEED, BOSS2_CHARGE_SPEED, BOSS2_DAMAGE, ICE_BLUE, WHITE,
)
from zelda_miloutte.sounds import get_sound_manager
from zelda_miloutte.particles import ParticleSystem


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

        # Area name banner
        self.area_banner_timer = 2.0  # Show for 2 seconds
        self.area_name = area_data["name"]

        # Initialize enemies, items, chests, signs, and NPCs
        self._spawn_enemies()
        self._spawn_items()
        self._spawn_chests()
        self._spawn_signs()
        self._spawn_npcs()

        # Restore player stats from save data
        if load_data is not None:
            pdata = load_data.get("player", {})
            self.player.hp = pdata.get("hp", self.player.hp)
            self.player.max_hp = pdata.get("max_hp", self.player.max_hp)
            self.player.keys = pdata.get("keys", self.player.keys)
            self.player.level = pdata.get("level", 1)
            self.player.xp = pdata.get("xp", 0)
            self.player.xp_to_next = pdata.get("xp_to_next", 100)
            self.player.base_attack = pdata.get("base_attack", 0)
            self.player.base_defense = pdata.get("base_defense", 0)

    def enter(self):
        """Called when entering this state."""
        area_data = AREAS[self.area_id]
        get_sound_manager().play_music(area_data["music"])

    def _spawn_enemies(self):
        from zelda_miloutte.entities.enemy import Enemy
        from zelda_miloutte.entities.archer import Archer
        from zelda_miloutte.entities.shadow_stalker import ShadowStalker
        from zelda_miloutte.entities.vine_snapper import VineSnapper
        from zelda_miloutte.entities.scorpion import Scorpion
        from zelda_miloutte.entities.mummy import Mummy
        from zelda_miloutte.entities.fire_imp import FireImp
        from zelda_miloutte.entities.magma_golem import MagmaGolem
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
            else:
                e = Enemy(
                    edata["x"] * TILE_SIZE, edata["y"] * TILE_SIZE,
                    edata.get("patrol", []),
                )
            self.enemies.append(e)

    def _spawn_items(self):
        from zelda_miloutte.entities.item import Item
        self.items = []
        area_spawns = AREAS[self.area_id]["spawns"]
        for idata in area_spawns.get("items", []):
            item = Item(
                idata["x"] * TILE_SIZE, idata["y"] * TILE_SIZE,
                idata["type"],
            )
            self.items.append(item)

    def _spawn_chests(self):
        from zelda_miloutte.entities.chest import Chest
        self.chests = []
        area_spawns = AREAS[self.area_id]["spawns"]
        for cdata in area_spawns.get("chests", []):
            chest = Chest(
                cdata["x"] * TILE_SIZE, cdata["y"] * TILE_SIZE,
                cdata["contents"],
            )
            self.chests.append(chest)

    def _spawn_signs(self):
        from zelda_miloutte.entities.sign import Sign
        self.signs = []
        area_spawns = AREAS[self.area_id]["spawns"]
        for sdata in area_spawns.get("signs", []):
            sign = Sign(
                sdata["x"] * TILE_SIZE, sdata["y"] * TILE_SIZE,
                sdata["text"],
            )
            self.signs.append(sign)

    def _spawn_npcs(self):
        from zelda_miloutte.entities.npc import NPC
        self.npcs = []
        area_spawns = AREAS[self.area_id]["spawns"]
        for ndata in area_spawns.get("npcs", []):
            npc = NPC(
                ndata["x"] * TILE_SIZE, ndata["y"] * TILE_SIZE,
                name=ndata["name"],
                variant=ndata.get("variant", "villager"),
                dialogue_tree=ndata.get("dialogue", {"default": ["..."]}),
                quest_id=ndata.get("quest_id"),
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

        # Calculate current player position in tile coordinates
        player_tile_x = int(player.center_x / TILE_SIZE)
        player_tile_y = int(player.center_y / TILE_SIZE)

        # Store player stats
        player_data = {
            "hp": player.hp,
            "max_hp": player.max_hp,
            "keys": player.keys,
            "level": player.level,
            "xp": player.xp,
            "xp_to_next": player.xp_to_next,
            "base_attack": player.base_attack,
            "base_defense": player.base_defense,
        }

        def do_transition():
            # Create new PlayState for target area
            new_state = PlayState(self.game, area_id=target_area, load_data={"player": player_data})

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

        # Check for pause
        if self.game.input.pause:
            from zelda_miloutte.states.pause_state import PauseState
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

        # Check for NPC interaction first, then sign interaction
        if not self._check_npc_interaction():
            self._check_sign_interaction()

        # Shared gameplay updates
        self._update_movement(dt)
        self._update_enemies(dt)
        self._update_combat(dt)
        self._update_enemy_collision()
        self._update_projectiles(dt)
        self._update_items(dt)
        self._check_hazards()
        self._cleanup_dead()

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
                        from zelda_miloutte.states.dungeon_state import DungeonState
                        from zelda_miloutte.world.maps import FOREST_DUNGEON, FOREST_DUNGEON_SPAWNS
                        from zelda_miloutte.entities.forest_guardian import ForestGuardian
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
                        from zelda_miloutte.states.dungeon_state import DungeonState
                        from zelda_miloutte.world.maps import DESERT_DUNGEON, DESERT_DUNGEON_SPAWNS
                        from zelda_miloutte.entities.sand_worm import SandWorm
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
                        from zelda_miloutte.states.dungeon_state import DungeonState
                        from zelda_miloutte.world.maps import VOLCANO_DUNGEON, VOLCANO_DUNGEON_SPAWNS
                        from zelda_miloutte.entities.inferno_drake import InfernoDrake
                        self.game.push_state(DungeonState(
                            self.game, self,
                            dungeon_map=VOLCANO_DUNGEON,
                            dungeon_spawns=VOLCANO_DUNGEON_SPAWNS,
                            boss_class=InfernoDrake,
                            victory_message="The Inferno Drake is slain! The seal is restored!"
                        ))
                    self.game.transition_to(enter_volcano_dungeon)
                else:
                    # Default dungeon (overworld)
                    def enter_dungeon():
                        from zelda_miloutte.states.dungeon_state import DungeonState
                        self.game.push_state(DungeonState(self.game, self))

                    self.game.transition_to(enter_dungeon)
        elif tile_type is not None and tile_type.name == "DUNGEON_ENTRANCE_2":
            if player.keys > 0:
                player.keys -= 1
                get_sound_manager().play_dungeon_enter()

                def enter_dungeon2():
                    from zelda_miloutte.states.dungeon_state import DungeonState
                    from zelda_miloutte.sprites.boss_sprites import get_boss2_frames_phase1, get_boss2_frames_phase2
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

        # Check player death
        self._check_player_death()

        # Update camera, particles, floating text
        self._update_camera(dt)
        self._update_particles(dt)
        self._update_floating_texts(dt)

    def draw(self, surface):
        # Use base class drawing
        self._draw_world(surface)

        # Draw area name banner if timer is active
        if self.area_banner_timer > 0:
            self._draw_area_banner(surface)

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
