import pygame
from zelda_miloutte.states.state import State
from zelda_miloutte.settings import SWORD_DAMAGE, RED
from zelda_miloutte.entities.item import Item
from zelda_miloutte.world.tile import TileType
from zelda_miloutte.ui.textbox import TextBox


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
        self.dialogue_box = None
        self.fire_trails = []
        self._init_dialogue_box()

    def _init_dialogue_box(self):
        from zelda_miloutte.ui.dialogue_box import DialogueBox
        self.dialogue_box = DialogueBox()

    def _update_movement(self, dt):
        """Handle player input and movement with tile collision."""
        player = self.player
        input_h = self.game.input

        player.apply_input(input_h)

        # Move with tile collision (axis-separated)
        player.move_x(dt)
        self.tilemap.resolve_collision_x(player)
        player.move_y(dt)
        self.tilemap.resolve_collision_y(player)

        player.update(dt)

        # Emit dust particles when player is moving
        if player.is_moving:
            self.particles.emit_dust(player.center_x, player.y + player.height)

    def _update_enemies(self, dt):
        """Update all enemies and collect projectiles from archers, vine snappers, and magma golems. Collect fire trails from fire imps."""
        from zelda_miloutte.entities.archer import Archer
        from zelda_miloutte.entities.vine_snapper import VineSnapper
        from zelda_miloutte.entities.shadow_stalker import ShadowStalker
        from zelda_miloutte.entities.fire_imp import FireImp
        from zelda_miloutte.entities.magma_golem import MagmaGolem
        for enemy in self.enemies:
            enemy.update(dt, self.player, self.tilemap)
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
                        # Spawn the item at chest center
                        item = Item(chest.rect.centerx, chest.rect.centery, item_type)
                        self.items.append(item)
                        # Emit sparkles when chest opens
                        self.particles.emit_sword_sparks(chest.center_x, chest.center_y)

    def _update_enemy_collision(self):
        """Handle enemy vs player damage with particles, knockback, and camera shake."""
        player = self.player
        for enemy in self.enemies:
            if enemy.alive and player.collides_with(enemy):
                if player.take_damage(enemy.damage):
                    # Trigger screen shake on damage
                    self.camera.shake(5, 0.3)
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
        """Update items and handle player pickup."""
        player = self.player
        for item in self.items:
            item.update(dt)

        # Player vs items
        for item in self.items:
            if item.alive and player.collides_with(item):
                item.pickup(player)

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
                self.particles.emit_death_burst(enemy.center_x, enemy.center_y, enemy.color)
                # Check for item drops
                drop = enemy.get_drop()
                if drop is not None:
                    item = Item(enemy.rect.centerx, enemy.rect.centery, drop)
                    self.items.append(item)
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
        if hasattr(inp, 'move_y'):
            # Check for up/down on this frame for choice navigation
            pass  # Choices handled via handle_event in subclass

        if not self.dialogue_box.active:
            # Dialogue just ended - check if a choice was made
            npc = getattr(self, '_interacting_npc', None)
            if npc and self.dialogue_box.selected_choice is not None:
                self._handle_npc_choice(npc, self.dialogue_box.selected_choice)
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
        for item in self.items:
            item.draw(surface, self.camera)
        for enemy in self.enemies:
            enemy.draw(surface, self.camera)
        for projectile in self.projectiles:
            projectile.draw(surface, self.camera)
        self.player.draw(surface, self.camera)
        self.particles.draw(surface, self.camera)
        # Floating texts (world-space)
        for ft in self.floating_texts:
            ft.draw(surface, self.camera)
        self.hud.draw(surface, self.player)
        # Draw UI layers last
        self.textbox.draw(surface)
        if self.dialogue_box:
            self.dialogue_box.draw(surface)
