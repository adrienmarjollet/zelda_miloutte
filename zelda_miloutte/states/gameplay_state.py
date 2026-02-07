import random
import pygame
from zelda_miloutte.states.state import State
from zelda_miloutte.settings import RED, SCREEN_WIDTH, SCREEN_HEIGHT
from zelda_miloutte.entities.item import Item
from zelda_miloutte.entities.gold import Gold
from zelda_miloutte.world.tile import TileType
from zelda_miloutte.ui.textbox import TextBox
from zelda_miloutte.ui.shop_ui import ShopUI


class GameplayState(State):
    """Base class for states with shared gameplay logic (PlayState, DungeonState)."""

    def __init__(self, game):
        super().__init__(game)
        # These should be initialized by subclasses:
        # self.tilemap
        # self.player
        # self.camera
        # self.enemies
        # self.items
        # self.chests
        # self.hud
        # self.particles
        # self.projectiles
        # self.signs
        self.textbox = TextBox()
        self.floating_texts = []
        self.npcs = []
        self._interacting_npc = None
        self.fire_trails = []
        self._ambient_timer = 0.0
        self._damage_vignette_timer = 0.0
        self._quest_notification = None
        self._quest_notification_timer = 0.0
        self._screen_flash_alpha = 0
        self.campfires = []
        self.gold_pickups = []
        self.shop_ui = ShopUI()
        self._init_dialogue_box()

        # Achievement popup system
        self._achievement_popups = []  # list of [Achievement, timer]

        # Companion (initialized by subclasses that support companions)
        self.companion = None

        # Puzzle entities (initialized by subclasses that use puzzles)
        self.push_blocks = []
        self.pressure_plates = []
        self.crystal_switches = []
        self.torches = []

        # Minimap (shared across gameplay states)
        from zelda_miloutte.ui.minimap import Minimap
        self.minimap = Minimap()

    def _init_dialogue_box(self):
        from zelda_miloutte.ui.dialogue_box import DialogueBox
        self.dialogue_box = DialogueBox()

    def _update_movement(self, dt):
        """Handle player input and movement with tile collision."""
        player = self.player
        input_h = self.game.input

        # Pass companion to player for speed bonus calculation
        player.apply_input(input_h, self.companion)

        # Move with tile collision (axis-separated)
        player.move_x(dt)
        self.tilemap.resolve_collision_x(player)
        player.move_y(dt)
        self.tilemap.resolve_collision_y(player)

        # Apply companion MP regen bonus (Fairy) before player.update()
        if self.companion is not None:
            from zelda_miloutte.entities.companion import Fairy
            if isinstance(self.companion, Fairy):
                player._companion_mp_bonus = 0.50  # +50% MP regen
            else:
                player._companion_mp_bonus = 0.0
        else:
            player._companion_mp_bonus = 0.0

        player.update(dt)

        # Emit dust particles when player is moving
        if player.is_moving:
            self.particles.emit_dust(player.center_x, player.y + player.height)

        # Handle ability cycling (Q key)
        if input_h.cycle_ability:
            player.cycle_ability()

        # Handle ability activation (R key)
        if input_h.use_ability and player.active_ability is not None:
            player.active_ability.use(player, self.enemies, self.projectiles, self.particles, self.camera)

    def _update_enemies(self, dt):
        """Update all enemies and collect projectiles from archers, vine snappers, and magma golems. Collect fire trails from fire imps."""
        from zelda_miloutte.entities.archer import Archer
        from zelda_miloutte.entities.vine_snapper import VineSnapper
        from zelda_miloutte.entities.shadow_stalker import ShadowStalker
        from zelda_miloutte.entities.fire_imp import FireImp
        from zelda_miloutte.entities.magma_golem import MagmaGolem
        from zelda_miloutte.pathfinding import reset_pathfind_budget
        from zelda_miloutte.ai_state import update_group_behavior

        # Reset pathfinding budget each frame (max 3 pathfinds per frame)
        reset_pathfind_budget()

        # Update group behavior (flanking/spread) for enemies chasing the player
        update_group_behavior(self.enemies, self.player)

        # Apply companion stealth factor to enemy detection ranges (Cat)
        stealth_factor = 0.0
        if self.companion is not None:
            stealth_factor = self.companion.get_stealth_factor()

        for enemy in self.enemies:
            # Temporarily reduce detection range based on stealth factor
            original_detection = getattr(enemy, 'detection_range', None)
            if original_detection is not None and stealth_factor > 0:
                enemy.detection_range = original_detection * (1.0 - stealth_factor)

            enemy.update(dt, self.player, self.tilemap)

            # Restore original detection range
            if original_detection is not None and stealth_factor > 0:
                enemy.detection_range = original_detection
            # Discover enemy in bestiary on first encounter
            enemy_class = type(enemy).__name__
            self.game.bestiary.discover(enemy_class)
            # Collect projectiles from archers
            if isinstance(enemy, Archer) and enemy.pending_projectile:
                self.projectiles.append(enemy.pending_projectile)
                enemy.pending_projectile = None
            # Collect projectiles from vine snappers
            if isinstance(enemy, VineSnapper) and enemy.pending_projectile:
                self.projectiles.append(enemy.pending_projectile)
                enemy.pending_projectile = None
            # Collect projectiles from magma golems
            if isinstance(enemy, MagmaGolem) and enemy.pending_projectile:
                self.projectiles.append(enemy.pending_projectile)
                enemy.pending_projectile = None
            # Emit teleport particles for shadow stalkers
            if isinstance(enemy, ShadowStalker) and enemy.teleport_particles:
                self.particles.emit(enemy.center_x, enemy.center_y, count=12, color=(80, 40, 120), speed_range=(40, 80), lifetime_range=(0.3, 0.6), size_range=(2, 4), gravity=0)
                enemy.teleport_particles = False
            # Collect fire trails from fire imps
            if isinstance(enemy, FireImp) and enemy.pending_fire_trails:
                for trail in enemy.pending_fire_trails:
                    trail["rect"] = pygame.Rect(int(trail["x"]) - 8, int(trail["y"]) - 8, 16, 16)
                    self.fire_trails.append(trail)
                enemy.pending_fire_trails = []

        # Update fire trails
        for trail in self.fire_trails:
            trail["timer"] -= dt
        self.fire_trails = [t for t in self.fire_trails if t["timer"] > 0]

    def _update_combat(self, dt):
        """Handle sword vs enemies collision with particles, knockback, and camera shake."""
        player = self.player
        damage = player.attack_power
        if player.attacking and player.sword_rect:
            for enemy in self.enemies:
                if enemy.alive and player.sword_rect.colliderect(enemy.rect):
                    enemy.take_damage(damage)
                    # Apply knockback to enemy
                    enemy.apply_knockback(player.center_x, player.center_y, 200)
                    # Emit sword sparks on hit
                    self.particles.emit_sword_sparks(enemy.center_x, enemy.center_y)

            # Check for chest hits
            for chest in self.chests:
                if not chest.opened and player.sword_rect.colliderect(chest.rect):
                    item_type = chest.open(player)
                    if item_type:
                        if item_type == "gold":
                            # Gold was already added directly to player in chest.open()
                            from zelda_miloutte.ui.floating_text import FloatingText
                            self.floating_texts.append(FloatingText(
                                f"+{chest.gold_amount}G", chest.center_x,
                                chest.center_y - 10, (255, 200, 50), size=22, duration=1.0
                            ))
                        else:
                            # Spawn the item at chest center
                            item = Item(chest.rect.centerx, chest.rect.centery, item_type)
                            self.items.append(item)
                        # Emit sparkles when chest opens
                        self.particles.emit_sword_sparks(chest.center_x, chest.center_y)
                        # Track chest open in achievements
                        self.game.achievement_manager.on_chest_open()

            # Check for crystal switch hits
            for switch in self.crystal_switches:
                if player.sword_rect.colliderect(switch.rect):
                    if switch.try_toggle():
                        self.particles.emit_sword_sparks(switch.center_x, switch.center_y)
                        self._on_crystal_switch_toggled(switch)

            # Check for torch hits (sword lights torches)
            for torch_ent in self.torches:
                if not torch_ent.lit and player.sword_rect.colliderect(torch_ent.rect):
                    if torch_ent.try_light():
                        self.particles.emit(
                            torch_ent.center_x, torch_ent.center_y - 8,
                            count=10, color=(255, 200, 50),
                            speed_range=(40, 80), lifetime_range=(0.3, 0.6),
                            size_range=(2, 4), gravity=0)
                        self._check_all_torches_lit()

    def _update_puzzles(self, dt):
        """Update all puzzle entities and check activations."""
        for block in self.push_blocks:
            block.update(dt)
        for sw in self.crystal_switches:
            sw.update(dt)
        for tc in self.torches:
            tc.update(dt)
        for plate in self.pressure_plates:
            if plate.check_activation(self.player, self.push_blocks):
                self._on_pressure_plate_activated(plate)

    def _spawn_puzzles(self, spawn_dict):
        """Spawn puzzle entities from spawn data.

        Args:
            spawn_dict: Dictionary containing puzzle spawn data with a "puzzles" key
        """
        from zelda_miloutte.entities.puzzle import PushBlock, PressurePlate, CrystalSwitch, Torch

        self.push_blocks = []
        self.pressure_plates = []
        self.crystal_switches = []
        self.torches = []

        puzzle_data = spawn_dict.get("puzzles", [])
        for pdata in puzzle_data:
            ptype = pdata.get("type")
            x = pdata["x"]
            y = pdata["y"]
            puzzle_id = pdata.get("id")
            trigger = pdata.get("trigger")

            if ptype == "push_block":
                block = PushBlock(x, y, block_id=puzzle_id)
                self.push_blocks.append(block)

            elif ptype == "pressure_plate":
                linked_targets = [trigger] if trigger else []
                plate = PressurePlate(x, y, plate_id=puzzle_id, linked_targets=linked_targets)
                self.pressure_plates.append(plate)

            elif ptype == "crystal_switch":
                linked_targets = [trigger] if trigger else []
                initial_state = pdata.get("state", False)
                switch = CrystalSwitch(x, y, switch_id=puzzle_id, linked_targets=linked_targets, state=initial_state)
                self.crystal_switches.append(switch)

            elif ptype == "torch":
                linked_targets = [trigger] if trigger else []
                torch = Torch(x, y, torch_id=puzzle_id, linked_targets=linked_targets)
                self.torches.append(torch)

        # Store puzzle door configuration for later use
        self._puzzle_doors = spawn_dict.get("puzzle_doors", {})

        # Store original map data for barrier restoration when crystal switches toggle
        import copy
        self._original_map_data = copy.deepcopy(self.tilemap.data)

    def _check_push_block_interaction(self):
        """Check if player is pushing into a push block."""
        if not self.player.is_moving:
            return
        for block in self.push_blocks:
            if not block.is_sliding and self.player.rect.colliderect(block.rect):
                block.try_push(self.player.facing, self.tilemap, self.push_blocks)

    def _resolve_push_block_collision(self):
        """Prevent player from walking through push blocks."""
        p = self.player
        for block in self.push_blocks:
            pr, br = p.rect, block.rect
            if not pr.colliderect(br):
                continue
            ox = min(pr.right, br.right) - max(pr.left, br.left)
            oy = min(pr.bottom, br.bottom) - max(pr.top, br.top)
            if ox <= 0 or oy <= 0:
                continue
            if ox < oy:
                p.x += (-ox if p.center_x < block.center_x else ox)
            else:
                p.y += (-oy if p.center_y < block.center_y else oy)

    def _on_crystal_switch_toggled(self, switch):
        """Update barrier tiles when crystal switch is toggled."""
        from zelda_miloutte.sounds import get_sound_manager
        from zelda_miloutte.world.tile import TileType
        get_sound_manager().play_door_open()
        orig = getattr(self, '_original_map_data', None)
        for ri in range(self.tilemap.rows):
            for ci in range(self.tilemap.cols):
                t = self.tilemap.tiles[ri][ci]
                if t == TileType.BARRIER_RED and switch.state:
                    self.tilemap.tiles[ri][ci] = TileType.FLOOR
                    self.tilemap.data[ri][ci] = TileType.FLOOR.value
                elif t == TileType.BARRIER_BLUE and not switch.state:
                    self.tilemap.tiles[ri][ci] = TileType.FLOOR
                    self.tilemap.data[ri][ci] = TileType.FLOOR.value
                elif t == TileType.FLOOR and orig:
                    ov = orig[ri][ci]
                    if ov == TileType.BARRIER_RED.value and not switch.state:
                        self.tilemap.tiles[ri][ci] = TileType.BARRIER_RED
                        self.tilemap.data[ri][ci] = TileType.BARRIER_RED.value
                    elif ov == TileType.BARRIER_BLUE.value and switch.state:
                        self.tilemap.tiles[ri][ci] = TileType.BARRIER_BLUE
                        self.tilemap.data[ri][ci] = TileType.BARRIER_BLUE.value
        from zelda_miloutte.sprites.tile_sprites import get_tile_surface_variant
        for ri in range(self.tilemap.rows):
            for ci in range(self.tilemap.cols):
                self.tilemap._tile_surface_grid[ri][ci] = get_tile_surface_variant(
                    self.tilemap.data[ri][ci], ci, ri)

    def _on_pressure_plate_activated(self, plate):
        """Check if all linked plates pressed and trigger target."""
        from zelda_miloutte.world.tile import TileType
        for tid in plate.linked_targets:
            if all(p.pressed for p in self.pressure_plates if tid in p.linked_targets):
                self._trigger_puzzle_target(tid)

    def _check_all_torches_lit(self):
        """Check if all torches sharing linked_targets are lit."""
        if not self.torches:
            return
        groups = {}
        for tc in self.torches:
            for tid in tc.linked_targets:
                groups.setdefault(tid, []).append(tc)
        for tid, grp in groups.items():
            if all(tc.lit for tc in grp):
                self._trigger_puzzle_target(tid)

    def _trigger_puzzle_target(self, target_id):
        """Trigger puzzle target by ID - converts tagged tiles to floor."""
        from zelda_miloutte.sounds import get_sound_manager
        from zelda_miloutte.sprites.tile_sprites import get_tile_surface_variant
        from zelda_miloutte.world.tile import TileType
        get_sound_manager().play_door_open()
        doors = getattr(self, '_puzzle_doors', {})
        if target_id in doors:
            for (col, row) in doors[target_id]:
                self.tilemap.tiles[row][col] = TileType.FLOOR
                self.tilemap.data[row][col] = TileType.FLOOR.value
                self.tilemap._tile_surface_grid[row][col] = get_tile_surface_variant(
                    TileType.FLOOR.value, col, row)
            self.camera.shake(3, 0.3)

    def _draw_puzzles(self, surface):
        """Draw all puzzle entities."""
        for plate in self.pressure_plates:
            plate.draw(surface, self.camera)
        for block in self.push_blocks:
            block.draw(surface, self.camera)
        for sw in self.crystal_switches:
            sw.draw(surface, self.camera)
        for tc in self.torches:
            tc.draw(surface, self.camera)

    def _update_enemy_collision(self):
        """Handle enemy vs player damage with particles, knockback, and camera shake."""
        player = self.player
        for enemy in self.enemies:
            if enemy.alive and player.collides_with(enemy):
                if player.take_damage(enemy.damage):
                    # Trigger screen shake on damage
                    self.camera.shake(5, 0.3)
                    self._trigger_damage_vignette()
                    # Apply status effects from special enemies
                    if hasattr(enemy, 'applies_poison') and enemy.applies_poison:
                        player.apply_status("poison", 6.0, {"tick_damage": 1, "tick_interval": 2.0})
                    if hasattr(enemy, 'applies_slow') and enemy.applies_slow:
                        player.apply_status("slow", 4.0, {"speed_multiplier": 0.5})
                # Apply knockback to player
                player.apply_knockback(enemy.center_x, enemy.center_y, 200)

        # Physically separate player from all overlapping enemies so the player
        # never gets trapped between multiple enemies.
        self._separate_player_from_enemies()

    def _separate_player_from_enemies(self):
        """Push player out of any overlapping enemy rects."""
        player = self.player
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            prect = player.rect
            erect = enemy.rect
            if not prect.colliderect(erect):
                continue

            # Compute overlap on each axis
            overlap_x = min(prect.right, erect.right) - max(prect.left, erect.left)
            overlap_y = min(prect.bottom, erect.bottom) - max(prect.top, erect.top)

            if overlap_x <= 0 or overlap_y <= 0:
                continue

            # Push along the axis with the smallest overlap
            if overlap_x < overlap_y:
                if player.center_x < enemy.center_x:
                    player.x -= overlap_x
                else:
                    player.x += overlap_x
            else:
                if player.center_y < enemy.center_y:
                    player.y -= overlap_y
                else:
                    player.y += overlap_y

    def _update_items(self, dt):
        """Update items and gold pickups, handle player pickup."""
        player = self.player
        for item in self.items:
            item.update(dt)

        # Player vs items
        for item in self.items:
            if item.alive and player.collides_with(item):
                item.pickup(player)

        # Gold pickups
        for gold in self.gold_pickups:
            gold.update(dt)
        for gold in self.gold_pickups:
            if gold.alive and player.collides_with(gold):
                from zelda_miloutte.ui.floating_text import FloatingText
                amount = gold.amount
                gold.pickup(player)
                self.floating_texts.append(FloatingText(
                    f"+{amount}G", player.center_x, player.center_y - 10,
                    (255, 200, 50), size=20, duration=0.8
                ))
        self.gold_pickups = [g for g in self.gold_pickups if g.alive]

    def _update_projectiles(self, dt):
        """Update projectiles and handle collisions."""
        player = self.player
        for projectile in self.projectiles:
            projectile.update(dt, self.tilemap)

        # Projectile vs player collision
        for projectile in self.projectiles:
            if projectile.alive and player.collides_with(projectile):
                if player.take_damage(projectile.damage):
                    # Trigger screen shake on projectile hit
                    self.camera.shake(4, 0.2)
                # Apply knockback from projectile direction
                player.apply_knockback(
                    projectile.center_x - projectile.vx * 0.1,
                    projectile.center_y - projectile.vy * 0.1,
                    150
                )
                projectile.alive = False

        # Remove dead projectiles
        self.projectiles = [p for p in self.projectiles if p.alive]

    def _check_hazards(self):
        """Check if player is on a hazard tile or fire trail and apply damage."""
        player = self.player
        tile_type = self.tilemap.get_tile_at(player.center_x, player.center_y)

        if tile_type == TileType.SPIKES:
            # Spikes damage player - take_damage handles invincibility cooldown
            if player.take_damage(1):
                # Damage was applied (not invincible)
                self.camera.shake(3, 0.2)
                # Emit red damage particles at player's feet
                self.particles.emit(
                    player.center_x,
                    player.center_y,
                    count=8,
                    color=RED,
                    speed_range=(60, 100),
                    lifetime_range=(0.2, 0.4),
                    size_range=(2, 4),
                    gravity=0
                )
        elif tile_type == TileType.LAVA:
            # Lava damage player (2 damage) - take_damage handles invincibility cooldown
            if player.take_damage(2):
                # Damage was applied (not invincible)
                self.camera.shake(4, 0.3)
                # Emit orange/red particles at player's feet
                self.particles.emit(
                    player.center_x,
                    player.center_y,
                    count=12,
                    color=(255, 100, 20),
                    speed_range=(80, 120),
                    lifetime_range=(0.3, 0.5),
                    size_range=(3, 6),
                    gravity=0
                )

        # Check fire trail collisions
        for trail in self.fire_trails:
            if player.rect.colliderect(trail["rect"]):
                if player.take_damage(1):
                    # Damage was applied (not invincible)
                    self.camera.shake(3, 0.2)
                    # Emit orange fire particles
                    self.particles.emit(
                        player.center_x,
                        player.center_y,
                        count=8,
                        color=(255, 120, 30),
                        speed_range=(60, 100),
                        lifetime_range=(0.2, 0.4),
                        size_range=(2, 4),
                        gravity=0
                    )
                break

    def _cleanup_dead(self):
        """Remove dead enemies/items and emit death particles. Spawn drops and XP from dead enemies."""
        from zelda_miloutte.ui.floating_text import FloatingText
        for enemy in self.enemies:
            if not enemy.alive:
                self.particles.emit_death_burst_dramatic(enemy.center_x, enemy.center_y, enemy.color)
                # Check for item drops
                drop = enemy.get_drop()
                if drop is not None:
                    item = Item(enemy.rect.centerx, enemy.rect.centery, drop)
                    self.items.append(item)
                # Check for gold drops
                gold_amount = enemy.get_gold_drop()
                if gold_amount > 0:
                    gold = Gold(enemy.rect.centerx, enemy.rect.centery, gold_amount)
                    self.gold_pickups.append(gold)
                # Grant XP
                xp_val = getattr(enemy, 'xp_value', 10)
                leveled = self.player.gain_xp(xp_val)
                # Spawn floating XP text
                self.floating_texts.append(FloatingText(
                    f"+{xp_val} XP", enemy.center_x, enemy.center_y, (100, 200, 255)
                ))
                if leveled:
                    self.floating_texts.append(FloatingText(
                        "LEVEL UP!", self.player.center_x, self.player.center_y - 20,
                        (255, 255, 100), size=28, duration=1.5
                    ))
                    self.particles.emit_levelup_burst(self.player.center_x, self.player.center_y)
                # Track enemy kills for sidequests
                enemy_type = type(enemy).__name__.lower()
                self.game.quest_manager.update_objective("kill", enemy_type)
                # Also count as generic "enemy" for broad kill quests
                self.game.quest_manager.update_objective("kill", "enemy")
                # Track kill in achievements and bestiary
                enemy_class = type(enemy).__name__
                self.game.achievement_manager.on_enemy_kill()
                self.game.bestiary.record_kill(enemy_class)
                # Check level-up achievement
                if leveled and self.player.level >= 10:
                    self.game.achievement_manager.on_level_up(self.player.level)
                # Auto-complete quests whose objectives are now met
                for quest in self.game.quest_manager.get_active_quests():
                    if self.game.quest_manager.check_quest_complete(quest.id):
                        rewards = self.game.quest_manager.complete_quest(quest.id)
                        self.game.world_state["story_progress"] = len(
                            self.game.quest_manager.get_completed_quests()
                        )
                        self.show_quest_notification(f"Quest Complete: {quest.name}!")
                        # Apply rewards
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
                                self.particles.emit_levelup_burst(
                                    self.player.center_x, self.player.center_y
                                )
                        if rewards and "keys" in rewards:
                            self.player.keys += rewards.get("keys", 0)
        self.enemies = [e for e in self.enemies if e.alive]
        self.items = [i for i in self.items if i.alive]

    def _check_player_death(self):
        """Check if player is dead and transition to game over."""
        if not self.player.alive:
            def show_game_over():
                from zelda_miloutte.states.gameover_state import GameOverState
                self.game.change_state(GameOverState(self.game))

            self.game.transition_to(show_game_over)

    def _update_camera(self, dt):
        """Update camera to follow player and handle shake."""
        self.camera.follow(self.player)
        self.camera.update_shake(dt)

    def _update_particles(self, dt):
        """Update particle system."""
        self.particles.update(dt)

    def _check_npc_interaction(self):
        """Check if player is interacting with an NPC."""
        if not self.game.input.interact:
            return False

        player = self.player
        interaction_rect = player.rect.inflate(16, 16)

        for npc in self.npcs:
            if interaction_rect.colliderect(npc.rect):
                dx = npc.rect.centerx - player.rect.centerx
                dy = npc.rect.centery - player.rect.centery
                is_facing = False
                if player.facing == "up" and dy < 0:
                    is_facing = True
                elif player.facing == "down" and dy > 0:
                    is_facing = True
                elif player.facing == "left" and dx < 0:
                    is_facing = True
                elif player.facing == "right" and dx > 0:
                    is_facing = True

                if is_facing:
                    messages = npc.get_dialogue()
                    choices = npc.get_choices()
                    self.dialogue_box.show(npc.name, messages, choices)
                    self._interacting_npc = npc
                    return True
        return False

    def _update_dialogue_box(self, dt):
        """Update dialogue box state."""
        if not self.dialogue_box.active:
            return
        self.dialogue_box.update(dt)
        inp = self.game.input
        if inp.interact:
            self.dialogue_box.advance()

        if not self.dialogue_box.active:
            # Dialogue just ended - check if a choice was made
            npc = getattr(self, '_interacting_npc', None)
            if npc and self.dialogue_box.selected_choice is not None:
                self._handle_npc_choice(npc, self.dialogue_box.selected_choice)
            # Open shop if NPC is a merchant with a shop_id
            if npc and getattr(npc, 'shop_id', None):
                self.shop_ui.open(npc.shop_id, self.player)
            self._interacting_npc = None

    def _handle_npc_choice(self, npc, choice_index):
        """Handle a dialogue choice selection. Override in subclasses for quest logic."""
        pass

    def _check_sign_interaction(self):
        """Check if player is interacting with a sign."""
        if not self.game.input.interact or not hasattr(self, 'signs'):
            return False

        player = self.player
        # Check if player is near any sign
        # "Near" means player rect inflated by ~8px overlaps sign rect AND player is facing the sign
        interaction_rect = player.rect.inflate(16, 16)

        for sign in self.signs:
            if interaction_rect.colliderect(sign.rect):
                # Check if player is facing the sign
                dx = sign.rect.centerx - player.rect.centerx
                dy = sign.rect.centery - player.rect.centery

                # Determine if player is facing the sign based on direction
                is_facing = False
                if player.facing == "up" and dy < 0:
                    is_facing = True
                elif player.facing == "down" and dy > 0:
                    is_facing = True
                elif player.facing == "left" and dx < 0:
                    is_facing = True
                elif player.facing == "right" and dx > 0:
                    is_facing = True

                if is_facing:
                    self.textbox.show(sign.text)
                    return True

        return False

    def _update_ambient_particles(self, dt):
        """Spawn area-specific ambient particles."""
        from zelda_miloutte.settings import SCREEN_WIDTH, SCREEN_HEIGHT
        self._ambient_timer += dt
        area_id = getattr(self, 'area_id', None)
        # Spawn ~3 ambient particles per second
        if self._ambient_timer >= 0.33:
            self._ambient_timer = 0.0
            cx, cy = self.camera.true_x, self.camera.true_y
            if area_id == "overworld":
                self.particles.emit_ambient_grass(SCREEN_WIDTH, SCREEN_HEIGHT, cx, cy)
            elif area_id == "forest":
                self.particles.emit_ambient_spores(SCREEN_WIDTH, SCREEN_HEIGHT, cx, cy)
            elif area_id == "desert":
                self.particles.emit_ambient_sand(SCREEN_WIDTH, SCREEN_HEIGHT, cx, cy)
            elif area_id == "volcano":
                self.particles.emit_ambient_embers(SCREEN_WIDTH, SCREEN_HEIGHT, cx, cy)

    def _update_damage_vignette(self, dt):
        """Update damage vignette timer."""
        if self._damage_vignette_timer > 0:
            self._damage_vignette_timer -= dt

    def _trigger_damage_vignette(self):
        """Trigger red edge flash on player hit."""
        self._damage_vignette_timer = 0.3

    def _update_quest_notification(self, dt):
        """Update quest notification popup."""
        if self._quest_notification_timer > 0:
            self._quest_notification_timer -= dt
            if self._quest_notification_timer <= 0:
                self._quest_notification = None

    def show_quest_notification(self, text):
        """Show a quest notification banner."""
        self._quest_notification = text
        self._quest_notification_timer = 2.5

    def _update_minimap(self, dt):
        """Update minimap: reveal tiles and animate."""
        area_id = getattr(self, 'area_id', 'dungeon')
        self.minimap.reveal_tiles(area_id, self.player.center_x, self.player.center_y, self.tilemap)
        self.minimap.update(dt)

        # Toggle minimap with N key
        if self.game.input.toggle_minimap:
            self.minimap.toggle()

    def _draw_minimap(self, surface):
        """Draw the minimap overlay."""
        area_id = getattr(self, 'area_id', 'dungeon')
        self.minimap.draw(
            surface, self.tilemap, self.player,
            self.enemies, self.chests, self.npcs, area_id
        )


    # ── Day/Night cycle helpers ────────────────────────────────────

    def _update_campfires(self, dt):
        """Update campfire animations."""
        for campfire in self.campfires:
            campfire.update(dt)

    def _check_campfire_interaction(self):
        """Check if player is interacting with a campfire. Returns True if resting."""
        if not self.game.input.interact:
            return False
        player = self.player
        interaction_rect = player.rect.inflate(16, 16)
        for campfire in self.campfires:
            if campfire.alive and interaction_rect.colliderect(campfire.rect):
                self.game.time_system.skip_to_dawn()
                player.hp = player.max_hp
                self.textbox.show("You rest by the campfire... Dawn breaks anew. HP restored!")
                self.particles.emit(
                    campfire.center_x, campfire.center_y,
                    count=15,
                    color=[(255, 200, 80), (255, 160, 40), (255, 220, 100)],
                    speed_range=(20, 60),
                    lifetime_range=(0.5, 1.0),
                    size_range=(2, 4),
                    gravity=-20,
                )
                return True
        return False

    def _update_night_enemies(self):
        """Apply night-time stat boosts to enemies.

        Night scaling (1.5x HP/damage) is applied multiplicatively on top of NG+ scaling.
        Example: NG+2 enemy with base HP=10 becomes 22 HP (10 * 1.5^2), then 33 HP at night (22 * 1.5).
        """
        time_sys = self.game.time_system
        for enemy in self.enemies:
            if not hasattr(enemy, '_night_boosted'):
                enemy._night_boosted = False
            if time_sys.is_night and not enemy._night_boosted:
                enemy.hp = int(enemy.hp * 1.5)
                enemy.max_hp = int(enemy.max_hp * 1.5)
                enemy.damage = max(1, int(enemy.damage * 1.5))
                enemy._night_boosted = True
                enemy._night_tinted = True
            elif not time_sys.is_night and enemy._night_boosted:
                enemy._night_boosted = False
                enemy._night_tinted = False

    def _update_npc_night_state(self):
        """Update NPCs for night behavior -- show night dialogue."""
        time_sys = self.game.time_system
        for npc in self.npcs:
            if not hasattr(npc, '_night_hidden'):
                npc._night_hidden = False
                npc._original_dialogue_state = None
            if time_sys.is_night and not npc._night_hidden:
                npc._night_hidden = True
                npc._original_dialogue_state = npc.dialogue_state
                if "night" not in npc.dialogue_tree:
                    npc.dialogue_tree["night"] = ["Zzz... Come back in the morning."]
                npc.dialogue_state = "night"
            elif not time_sys.is_night and npc._night_hidden:
                npc._night_hidden = False
                if npc._original_dialogue_state:
                    npc.dialogue_state = npc._original_dialogue_state

    def _draw_day_night_overlay(self, surface):
        """Draw the day/night cycle overlay after all game entities but before HUD."""
        time_sys = self.game.time_system
        player_screen_x = self.player.center_x - self.camera.x
        player_screen_y = self.player.center_y - self.camera.y
        has_lantern = getattr(self.player, 'has_lantern', False)
        time_sys.draw_overlay(surface, player_screen_x, player_screen_y, has_lantern)

    def _draw_time_hud(self, surface):
        """Draw the time-of-day HUD element (sun/moon icon + clock)."""
        from zelda_miloutte.sprites.time_hud_sprites import (
            get_sun_icon, get_moon_icon, get_dawn_icon, get_dusk_icon,
        )
        time_sys = self.game.time_system
        phase = time_sys.phase
        if phase == "dawn":
            icon = get_dawn_icon()
        elif phase == "day":
            icon = get_sun_icon()
        elif phase == "dusk":
            icon = get_dusk_icon()
        else:
            icon = get_moon_icon()
        icon_x = SCREEN_WIDTH - icon.get_width() - 8
        icon_y = 8
        surface.blit(icon, (icon_x, icon_y))
        font = pygame.font.Font(None, 18)
        time_text = font.render(time_sys.time_string, True, (200, 200, 200))
        tx = SCREEN_WIDTH - time_text.get_width() - 12
        ty = icon_y + icon.get_height() + 2
        surface.blit(time_text, (tx, ty))

    def _update_night_chest_glow(self, dt):
        """Emit glow particles around night-only chests when it is night."""
        time_sys = self.game.time_system
        if not time_sys.is_night:
            return
        for chest in self.chests:
            if not chest.opened and getattr(chest, 'night_only', False):
                if random.random() < dt * 3:
                    self.particles.emit(
                        chest.center_x, chest.center_y,
                        count=1,
                        color=[(100, 100, 255), (150, 150, 255)],
                        speed_range=(5, 15),
                        lifetime_range=(0.5, 1.0),
                        size_range=(1, 3),
                        gravity=-10,
                    )

    def _update_item_glow(self, dt):
        """Emit glow particles around items on the ground."""
        for item in self.items:
            if item.alive and random.random() < dt * 2:
                self.particles.emit_item_glow(item.center_x, item.center_y)

    def _update_companion(self, dt):
        """Update companion position, animation, secret detection, and fairy sparkles."""
        if self.companion is None:
            return
        self.companion.update(dt, self.player)
        # Check for nearby secrets (hidden chests)
        self.companion.check_nearby_secrets(self.chests)
        # Fairy sparkle trail
        from zelda_miloutte.entities.companion import Fairy
        if isinstance(self.companion, Fairy) and self.companion.state == "follow":
            if random.random() < dt * 4:
                self.particles.emit_fairy_sparkle(self.companion.center_x, self.companion.center_y)

    def _check_companion_pet(self):
        """Check if player presses interact near companion to pet it."""
        if self.companion is None:
            return False
        if not self.game.input.interact:
            return False
        if self.companion.try_pet(self.player):
            self.particles.emit_companion_happy(self.companion.center_x, self.companion.center_y)
            from zelda_miloutte.ui.floating_text import FloatingText
            self.floating_texts.append(FloatingText(
                "+1 HP", self.player.center_x, self.player.center_y - 20,
                (255, 100, 120), size=20
            ))
            return True
        return False

    def _update_floating_texts(self, dt):
        """Update floating texts and remove expired ones."""
        for ft in self.floating_texts:
            ft.update(dt)
        self.floating_texts = [ft for ft in self.floating_texts if ft.alive]

    def _update_textbox(self, dt):
        """Update textbox state."""
        self.textbox.update(dt)

        # If textbox is active and player presses interact, dismiss it
        if self.textbox.active and self.game.input.interact:
            # Only dismiss if text is fully revealed
            if self.textbox._fully_revealed:
                self.textbox.dismiss()
            else:
                # Skip to end of text reveal
                self.textbox._revealed_chars = len(self.textbox.text)
                self.textbox._fully_revealed = True

    def _draw_world(self, surface):
        """Draw the world in standard order: tilemap, chests, items, signs, fire trails, enemies, projectiles, player, particles, HUD, textbox."""
        self.tilemap.draw(surface, self.camera)
        for chest in self.chests:
            chest.draw(surface, self.camera)
        if hasattr(self, 'signs'):
            for sign in self.signs:
                sign.draw(surface, self.camera)
        for npc in self.npcs:
            npc.draw(surface, self.camera)
        # Draw fire trails before items/enemies
        for trail in self.fire_trails:
            sx = int(trail["x"] - 8 - self.camera.x)
            sy = int(trail["y"] - 8 - self.camera.y)
            pygame.draw.rect(surface, (255, 120, 30), (sx, sy, 16, 16))
            pygame.draw.rect(surface, (255, 200, 50), (sx+3, sy+3, 10, 10))
        # Draw campfires
        for campfire in self.campfires:
            campfire.draw(surface, self.camera)
        for item in self.items:
            item.draw(surface, self.camera)
        for gold in self.gold_pickups:
            gold.draw(surface, self.camera)
        for enemy in self.enemies:
            enemy.draw(surface, self.camera)
        for projectile in self.projectiles:
            projectile.draw(surface, self.camera)
        self.player.draw(surface, self.camera)
        # Draw companion after player (on top)
        if self.companion is not None:
            self.companion.draw(surface, self.camera)
        # Draw active ability visual effects
        for ability in self.player.abilities:
            if ability.active:
                ability.draw(surface, self.camera, self.player)
        self.particles.draw(surface, self.camera)
        # Day/night overlay (drawn after entities, before HUD)
        self._draw_day_night_overlay(surface)
        # Floating texts (world-space)
        for ft in self.floating_texts:
            ft.draw(surface, self.camera)
        self.hud.draw(surface, self.player)
        # Time of day HUD
        self._draw_time_hud(surface)
        # Damage vignette overlay
        if self._damage_vignette_timer > 0:
            vignette_alpha = int(80 * (self._damage_vignette_timer / 0.3))
            vig_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            # Red edges only — draw rectangles on edges
            edge = 40
            for i in range(edge):
                a = int(vignette_alpha * (1 - i / edge))
                vig_surf.fill((200, 0, 0, a), (0, i, SCREEN_WIDTH, 1))
                vig_surf.fill((200, 0, 0, a), (0, SCREEN_HEIGHT - 1 - i, SCREEN_WIDTH, 1))
                vig_surf.fill((200, 0, 0, a), (i, 0, 1, SCREEN_HEIGHT))
                vig_surf.fill((200, 0, 0, a), (SCREEN_WIDTH - 1 - i, 0, 1, SCREEN_HEIGHT))
            surface.blit(vig_surf, (0, 0))
        # Screen flash (boss phase change)
        if self._screen_flash_alpha > 0:
            flash_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, int(self._screen_flash_alpha)))
            surface.blit(flash_surf, (0, 0))
        # Quest notification popup
        if self._quest_notification and self._quest_notification_timer > 0:
            self._draw_quest_notification(surface)
        # Draw minimap
        self._draw_minimap(surface)
        # Draw UI layers last
        self.textbox.draw(surface)
        if self.dialogue_box:
            self.dialogue_box.draw(surface)
        # Draw shop UI on top of everything
        if self.shop_ui.active:
            self.shop_ui.draw(surface)
        # Draw achievement popups on top of everything
        self._draw_achievement_popups(surface)

    def _update_achievement_popups(self, dt):
        """Check for pending achievement unlocks and manage popup display."""
        am = self.game.achievement_manager
        # Collect newly unlocked achievements
        while am.pending_popups:
            ach = am.pending_popups.pop(0)
            self._achievement_popups.append([ach, 3.0])  # 3 seconds display
        # Update timers
        for popup in self._achievement_popups:
            popup[1] -= dt
        self._achievement_popups = [p for p in self._achievement_popups if p[1] > 0]
        # Update play time
        am.update_play_time(dt)

    def _draw_achievement_popups(self, surface):
        """Draw achievement popup notifications sliding in from the top."""
        if not self._achievement_popups:
            return
        from zelda_miloutte.sprites.achievement_sprites import get_achievement_icon
        font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 18)

        for i, (ach, timer) in enumerate(self._achievement_popups):
            # Calculate slide animation
            total_time = 3.0
            if timer > total_time - 0.3:
                # Sliding in (first 0.3s)
                progress = (total_time - timer) / 0.3
                y_offset = int(-40 + 40 * progress)
            elif timer < 0.3:
                # Sliding out (last 0.3s)
                progress = timer / 0.3
                y_offset = int(-40 * (1 - progress))
            else:
                y_offset = 0

            y = 60 + i * 50 + y_offset

            # Background
            popup_w = 250
            popup_h = 40
            x = (SCREEN_WIDTH - popup_w) // 2
            bg = pygame.Surface((popup_w, popup_h), pygame.SRCALPHA)
            bg.fill((20, 20, 40, 200))
            pygame.draw.rect(bg, (255, 200, 50), (0, 0, popup_w, popup_h), 1)
            surface.blit(bg, (x, y))

            # Icon
            icon = get_achievement_icon(ach.icon_id)
            surface.blit(icon, (x + 6, y + (popup_h - 16) // 2))

            # Text
            title = font.render(f"Achievement: {ach.name}", True, (255, 220, 50))
            surface.blit(title, (x + 28, y + 4))
            desc = small_font.render(ach.description, True, (200, 200, 200))
            surface.blit(desc, (x + 28, y + 22))

    def _draw_quest_notification(self, surface):
        """Draw floating quest notification banner."""
        font = pygame.font.Font(None, 32)
        text_surf = font.render(self._quest_notification, True, (255, 220, 50))
        # Fade based on timer
        if self._quest_notification_timer > 2.0:
            alpha = int(255 * (2.5 - self._quest_notification_timer) / 0.5)
        elif self._quest_notification_timer < 0.5:
            alpha = int(255 * self._quest_notification_timer / 0.5)
        else:
            alpha = 255
        alpha = max(0, min(255, alpha))
        text_surf.set_alpha(alpha)
        # Draw centered near top
        x = (SCREEN_WIDTH - text_surf.get_width()) // 2
        y = 50
        # Background bar
        bg = pygame.Surface((text_surf.get_width() + 20, text_surf.get_height() + 10), pygame.SRCALPHA)
        bg.fill((0, 0, 0, int(alpha * 0.6)))
        surface.blit(bg, (x - 10, y - 5))
        surface.blit(text_surf, (x, y))
