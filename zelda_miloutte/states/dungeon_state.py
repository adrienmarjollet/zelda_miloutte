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
        self.player.keys = play_state.player.keys
        self.player.level = play_state.player.level
        self.player.xp = play_state.player.xp
        self.player.xp_to_next = play_state.player.xp_to_next
        self.player.base_attack = play_state.player.base_attack
        self.player.base_defense = play_state.player.base_defense

        self.camera = Camera(self.tilemap.pixel_width, self.tilemap.pixel_height)
        self.hud = HUD()

        # Enemies
        from zelda_miloutte.entities.archer import Archer
        from zelda_miloutte.entities.vine_snapper import VineSnapper
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
            else:
                e = Enemy(
                    edata["x"] * TILE_SIZE, edata["y"] * TILE_SIZE,
                    edata.get("patrol", []),
                )
            self.enemies.append(e)

        # Boss - use custom class if provided, otherwise default Boss
        bdata = dungeon_spawns["boss"]
        if boss_class is not None:
            # Use custom boss class (e.g., ForestGuardian)
            self.boss = boss_class(bdata["x"] * TILE_SIZE, bdata["y"] * TILE_SIZE)
        elif boss_config is None:
            self.boss = Boss(bdata["x"] * TILE_SIZE, bdata["y"] * TILE_SIZE)
        else:
            self.boss = Boss(bdata["x"] * TILE_SIZE, bdata["y"] * TILE_SIZE, **boss_config)

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

        self.victory = False
        self.victory_timer = 0.0
        self.victory_duration = 3.0
        self.victory_font = None

        self.particles = ParticleSystem()
        self.projectiles = []
        self.boss_death_emitted = False

        # Initialize signs
        self._spawn_signs()

    def enter(self):
        """Called when entering this state."""
        get_sound_manager().play_music('dungeon')

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
        p.keys = self.player.keys
        p.level = self.player.level
        p.xp = self.player.xp
        p.xp_to_next = self.player.xp_to_next
        p.base_attack = self.player.base_attack
        p.base_defense = self.player.base_defense

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
                # Return to overworld

                def return_to_overworld():
                    self._copy_stats_back()
                    self.game.pop_state()

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

        # Boss defeated (DungeonState-specific)
        if not self.boss.alive and not self.victory:
            if not self.boss_death_emitted:
                self.particles.emit_boss_death(self.boss.center_x, self.boss.center_y)
                self.boss_death_emitted = True
                self.camera.shake(12, 0.8)
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

        # Update camera, particles, floating text
        self._update_camera(dt)
        self._update_particles(dt)
        self._update_floating_texts(dt)

    def draw(self, surface):
        # Draw tilemap, chests, items, enemies, player, particles
        self.tilemap.draw(surface, self.camera)
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
