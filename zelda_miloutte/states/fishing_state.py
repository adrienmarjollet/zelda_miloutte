"""Fishing minigame state.

Phases: CAST -> WAIT -> BITE -> REEL -> RESULT
Pushed on top of the gameplay state when the player interacts with water.
"""

import random
import math
import pygame

from zelda_miloutte.states.state import State
from zelda_miloutte.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GOLD
from zelda_miloutte.data.fish import pick_random_fish
from zelda_miloutte.sprites.fish_sprites import get_fish_sprite
from zelda_miloutte.sounds import get_sound_manager


# Fishing phase constants
PHASE_CAST = "cast"
PHASE_WAIT = "wait"
PHASE_BITE = "bite"
PHASE_REEL = "reel"
PHASE_RESULT = "result"

# Reel minigame constants
REEL_BAR_HEIGHT = 200
REEL_BAR_WIDTH = 30
REEL_BAR_X = SCREEN_WIDTH // 2 + 100
REEL_BAR_Y = (SCREEN_HEIGHT - REEL_BAR_HEIGHT) // 2


class FishingState(State):
    """Overlay state for the fishing minigame."""

    def __init__(self, game, player, area_id, water_x, water_y):
        """
        Args:
            game: Game instance
            player: Player entity (to heal / add fish)
            area_id: Current area id for fish selection
            water_x: World x of the water tile being fished
            water_y: World y of the water tile being fished
        """
        super().__init__(game)
        self.player = player
        self.area_id = area_id
        self.water_x = water_x
        self.water_y = water_y

        # Phase
        self.phase = PHASE_CAST
        self.phase_timer = 0.0

        # Cast phase
        self.cast_power = 0.0        # 0-1, oscillates
        self.cast_power_dir = 1      # 1 = going up, -1 = going down
        self.cast_speed = 1.5        # oscillation speed

        # Wait phase
        self.wait_duration = 0.0     # random 2-8 seconds
        self.bobber_y_offset = 0.0
        self.bobber_bob_timer = 0.0
        self.ripple_timer = 0.0

        # Bite phase
        self.bite_timer = 0.0
        self.bite_window = 1.0       # 1 second to react

        # Reel phase
        self.fish = None             # FishData
        self.reel_indicator_y = 0.5  # 0-1, position of moving indicator
        self.reel_indicator_dir = 1
        self.reel_indicator_speed = 0.0
        self.sweet_spot_y = 0.0      # 0-1, center of sweet spot
        self.sweet_spot_size = 0.0   # 0-1, height of sweet spot
        self.reel_progress = 0.0     # 0-1, filling up when in sweet spot
        self.reel_decay = 0.15       # decay rate when outside sweet spot
        self.reel_fill_rate = 0.4    # fill rate when in sweet spot

        # Result phase
        self.result_success = False
        self.result_timer = 0.0
        self.result_message = ""

        # Fonts (lazy init)
        self._font = None
        self._small_font = None
        self._title_font = None

        # Particle effects
        self._particles = []

        # Fishing ambient music
        sm = get_sound_manager()
        self._prev_track = sm._current_track

    @property
    def font(self):
        if self._font is None:
            self._font = pygame.font.Font(None, 28)
        return self._font

    @property
    def small_font(self):
        if self._small_font is None:
            self._small_font = pygame.font.Font(None, 22)
        return self._small_font

    @property
    def title_font(self):
        if self._title_font is None:
            self._title_font = pygame.font.Font(None, 42)
        return self._title_font

    def enter(self):
        """Start the fishing sequence."""
        self.phase = PHASE_CAST
        self.cast_power = 0.0
        self.cast_power_dir = 1
        get_sound_manager().play_fishing_cast()

    def exit(self):
        """Restore previous music when fishing ends."""
        sm = get_sound_manager()
        if self._prev_track:
            sm.play_music(self._prev_track)

    # ── Event handling ────────────────────────────────────────────

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            # Cancel fishing at any phase
            self.game.pop_state()
            return

        if event.key == pygame.K_SPACE:
            self._on_space()

    def _on_space(self):
        """Handle space press based on current phase."""
        if self.phase == PHASE_CAST:
            self._end_cast()
        elif self.phase == PHASE_BITE:
            self._start_reel()
        elif self.phase == PHASE_REEL:
            # Tap space to push indicator toward sweet spot
            self._reel_tap()
        elif self.phase == PHASE_RESULT:
            self._finish()

    # ── Phase transitions ─────────────────────────────────────────

    def _end_cast(self):
        """Lock in cast power and move to wait phase."""
        self.phase = PHASE_WAIT
        self.wait_duration = random.uniform(2.0, 8.0)
        # Higher cast power = slightly shorter wait
        self.wait_duration *= (1.2 - self.cast_power * 0.4)
        self.phase_timer = 0.0
        get_sound_manager().play_fishing_plop()
        # Spawn initial ripple particles
        self._spawn_ripple_particles()

    def _start_bite(self):
        """Fish bites! Player has bite_window seconds to react."""
        self.phase = PHASE_BITE
        self.bite_timer = 0.0
        # Pick the fish now
        self.fish = pick_random_fish(self.area_id)
        if self.fish is None:
            # Fallback: no fish available, fail gracefully
            self._fail("Nothing bites...")
            return
        get_sound_manager().play_fishing_bite()

    def _start_reel(self):
        """Begin the reel minigame."""
        self.phase = PHASE_REEL
        self.phase_timer = 0.0

        # Configure difficulty based on fish
        diff = self.fish.difficulty

        # Sweet spot: easier fish = bigger sweet spot
        self.sweet_spot_size = max(0.1, 0.4 - diff * 0.3)
        self.sweet_spot_y = random.uniform(
            self.sweet_spot_size / 2, 1.0 - self.sweet_spot_size / 2
        )

        # Indicator speed: harder fish = faster
        self.reel_indicator_speed = 0.8 + diff * 1.2
        self.reel_indicator_y = 0.0
        self.reel_indicator_dir = 1

        # Progress fill/decay rates
        self.reel_fill_rate = 0.35 + (1.0 - diff) * 0.15
        self.reel_decay = 0.1 + diff * 0.15

        self.reel_progress = 0.0

    def _succeed(self):
        """Player caught the fish!"""
        self.phase = PHASE_RESULT
        self.result_success = True
        self.result_timer = 0.0

        # Add fish to player inventory
        self.player.inventory.add(self.fish.fish_id, 1)

        # Track in fish collection
        fish_collection = self.game.world_state.setdefault("fish_collection", {})
        fish_collection[self.fish.fish_id] = fish_collection.get(self.fish.fish_id, 0) + 1

        # Update quest objectives
        self.game.quest_manager.update_objective("fish", self.fish.fish_id)

        rarity_colors = {
            "common": (180, 180, 180),
            "uncommon": (100, 200, 100),
            "rare": (255, 200, 50),
        }
        rarity_color = rarity_colors.get(self.fish.rarity, WHITE)
        self.result_message = f"Caught: {self.fish.name}!"
        self.result_color = rarity_color

        get_sound_manager().play_fishing_catch()

    def _fail(self, message="The fish got away!"):
        """Fish escaped."""
        self.phase = PHASE_RESULT
        self.result_success = False
        self.result_timer = 0.0
        self.result_message = message
        self.result_color = (200, 80, 80)
        get_sound_manager().play_fishing_fail()

    def _finish(self):
        """Close fishing state and optionally heal."""
        if self.result_success and self.fish:
            # Offer to eat the fish immediately
            heal = self.fish.heal_value
            if heal > 0 and self.player.hp < self.player.max_hp:
                self.player.heal(heal)
                self.player.inventory.remove(self.fish.fish_id, 1)
        self.game.pop_state()

    def _reel_tap(self):
        """Player taps space during reel — bump indicator toward sweet spot."""
        # Move indicator toward sweet spot with a small impulse
        self.reel_indicator_dir = -1 if self.reel_indicator_y > 0.5 else 1
        # Give a small bump
        bump = 0.08
        self.reel_indicator_y += bump * (-1 if self.reel_indicator_y > self.sweet_spot_y else 1)
        self.reel_indicator_y = max(0.0, min(1.0, self.reel_indicator_y))

    # ── Particles ─────────────────────────────────────────────────

    def _spawn_ripple_particles(self):
        """Spawn water ripple particles at bobber location."""
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2 + 40
        for _ in range(5):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(10, 30)
            self._particles.append({
                "x": cx, "y": cy,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed * 0.3,
                "life": random.uniform(0.5, 1.0),
                "max_life": 1.0,
                "size": random.uniform(2, 4),
                "color": (100, 180, 255),
            })

    def _update_particles(self, dt):
        for p in self._particles:
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt
            p["life"] -= dt
        self._particles = [p for p in self._particles if p["life"] > 0]

    def _draw_particles(self, surface):
        for p in self._particles:
            alpha = int(200 * (p["life"] / p["max_life"]))
            size = int(p["size"])
            if size < 1:
                size = 1
            temp = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            color = (*p["color"], alpha)
            pygame.draw.circle(temp, color, (size, size), size)
            surface.blit(temp, (int(p["x"]) - size, int(p["y"]) - size))

    # ── Update ────────────────────────────────────────────────────

    def update(self, dt):
        self.phase_timer += dt
        self._update_particles(dt)

        if self.phase == PHASE_CAST:
            self._update_cast(dt)
        elif self.phase == PHASE_WAIT:
            self._update_wait(dt)
        elif self.phase == PHASE_BITE:
            self._update_bite(dt)
        elif self.phase == PHASE_REEL:
            self._update_reel(dt)
        elif self.phase == PHASE_RESULT:
            self._update_result(dt)

    def _update_cast(self, dt):
        """Oscillate the power bar."""
        self.cast_power += self.cast_speed * self.cast_power_dir * dt
        if self.cast_power >= 1.0:
            self.cast_power = 1.0
            self.cast_power_dir = -1
        elif self.cast_power <= 0.0:
            self.cast_power = 0.0
            self.cast_power_dir = 1

    def _update_wait(self, dt):
        """Wait for the fish to bite."""
        # Bobber bobbing animation
        self.bobber_bob_timer += dt
        self.bobber_y_offset = math.sin(self.bobber_bob_timer * 3) * 3

        # Ripple particles
        self.ripple_timer += dt
        if self.ripple_timer >= 1.5:
            self.ripple_timer = 0.0
            self._spawn_ripple_particles()

        # Check if bite time
        if self.phase_timer >= self.wait_duration:
            self._start_bite()

    def _update_bite(self, dt):
        """Waiting for player to press Space."""
        self.bite_timer += dt
        if self.bite_timer >= self.bite_window:
            self._fail("Too slow! The fish got away!")

    def _update_reel(self, dt):
        """Move indicator and check sweet spot."""
        # Move indicator up/down
        self.reel_indicator_y += self.reel_indicator_speed * self.reel_indicator_dir * dt
        if self.reel_indicator_y >= 1.0:
            self.reel_indicator_y = 1.0
            self.reel_indicator_dir = -1
        elif self.reel_indicator_y <= 0.0:
            self.reel_indicator_y = 0.0
            self.reel_indicator_dir = 1

        # Slowly drift sweet spot
        self.sweet_spot_y += random.uniform(-0.2, 0.2) * dt
        self.sweet_spot_y = max(
            self.sweet_spot_size / 2,
            min(1.0 - self.sweet_spot_size / 2, self.sweet_spot_y)
        )

        # Check if indicator is in sweet spot
        half_sweet = self.sweet_spot_size / 2
        in_sweet = abs(self.reel_indicator_y - self.sweet_spot_y) <= half_sweet

        if in_sweet:
            self.reel_progress += self.reel_fill_rate * dt
        else:
            self.reel_progress -= self.reel_decay * dt

        self.reel_progress = max(0.0, min(1.0, self.reel_progress))

        # Win/lose conditions
        if self.reel_progress >= 1.0:
            self._succeed()

        # Timeout: fail after 10 seconds of reeling
        if self.phase_timer > 10.0:
            self._fail("The line snapped!")

    def _update_result(self, dt):
        """Show result, wait for dismiss."""
        self.result_timer += dt

    # ── Draw ──────────────────────────────────────────────────────

    def draw(self, surface):
        # Draw the underlying game state
        if len(self.game.states) >= 2:
            self.game.states[-2].draw(surface)

        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 40, 120))
        surface.blit(overlay, (0, 0))

        # Draw phase-specific UI
        if self.phase == PHASE_CAST:
            self._draw_cast(surface)
        elif self.phase == PHASE_WAIT:
            self._draw_wait(surface)
        elif self.phase == PHASE_BITE:
            self._draw_bite(surface)
        elif self.phase == PHASE_REEL:
            self._draw_reel(surface)
        elif self.phase == PHASE_RESULT:
            self._draw_result(surface)

        self._draw_particles(surface)

        # Instructions
        self._draw_instructions(surface)

    def _draw_cast(self, surface):
        """Draw the cast power bar."""
        # Title
        title = self.title_font.render("Cast!", True, WHITE)
        surface.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 80))

        # Power bar background
        bar_w = 200
        bar_h = 24
        bar_x = (SCREEN_WIDTH - bar_w) // 2
        bar_y = SCREEN_HEIGHT // 2 - bar_h // 2

        pygame.draw.rect(surface, (40, 40, 60), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_w, bar_h), 2)

        # Fill
        fill_w = int(bar_w * self.cast_power)
        # Color goes from blue to green to yellow to red
        if self.cast_power < 0.5:
            r = int(self.cast_power * 2 * 200)
            g = 200
        else:
            r = 200
            g = int((1.0 - (self.cast_power - 0.5) * 2) * 200)
        fill_color = (r, g, 50)
        pygame.draw.rect(surface, fill_color, (bar_x + 2, bar_y + 2, fill_w - 4, bar_h - 4))

        # Label
        label = self.small_font.render("Press SPACE to cast!", True, (200, 200, 200))
        surface.blit(label, ((SCREEN_WIDTH - label.get_width()) // 2, bar_y + 40))

        # Draw bobber preview
        self._draw_bobber(surface, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80, 0)

    def _draw_wait(self, surface):
        """Draw bobber on water with ripples."""
        title = self.font.render("Waiting...", True, (150, 200, 255))
        surface.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 100))

        # Draw water area
        water_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 20, 160, 100)
        water_surf = pygame.Surface((water_rect.w, water_rect.h), pygame.SRCALPHA)
        water_surf.fill((40, 100, 200, 100))
        surface.blit(water_surf, water_rect.topleft)

        # Draw bobber
        self._draw_bobber(surface, SCREEN_WIDTH // 2,
                          SCREEN_HEIGHT // 2 + 20 + int(self.bobber_y_offset), 0)

        # Draw ripple rings
        t = self.bobber_bob_timer
        for i in range(3):
            radius = int(10 + (t * 15 + i * 12) % 40)
            alpha = max(0, 120 - radius * 3)
            if alpha > 0:
                ring_surf = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)
                pygame.draw.circle(ring_surf, (150, 200, 255, alpha),
                                   (radius + 2, radius + 2), radius, 1)
                surface.blit(ring_surf,
                             (SCREEN_WIDTH // 2 - radius - 2,
                              SCREEN_HEIGHT // 2 + 20 - radius - 2 + int(self.bobber_y_offset)))

    def _draw_bite(self, surface):
        """Draw bite indicator with ! alert."""
        # Flash effect
        flash_alpha = int(abs(math.sin(self.bite_timer * 8)) * 60)
        flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        flash.fill((255, 255, 100, flash_alpha))
        surface.blit(flash, (0, 0))

        # Big ! indicator
        alert = self.title_font.render("!", True, (255, 50, 50))
        ax = SCREEN_WIDTH // 2 - alert.get_width() // 2
        ay = SCREEN_HEIGHT // 2 - 60 + int(math.sin(self.bite_timer * 15) * 5)
        surface.blit(alert, (ax, ay))

        # Draw bobber dipping
        self._draw_bobber(surface, SCREEN_WIDTH // 2,
                          SCREEN_HEIGHT // 2 + 30, 8)

        # Timer bar (shrinking)
        remaining = max(0, 1.0 - self.bite_timer / self.bite_window)
        bar_w = 150
        bar_h = 8
        bar_x = (SCREEN_WIDTH - bar_w) // 2
        bar_y = SCREEN_HEIGHT // 2 + 70
        pygame.draw.rect(surface, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h))
        fill_color = (255, 200, 50) if remaining > 0.3 else (255, 60, 60)
        pygame.draw.rect(surface, fill_color, (bar_x, bar_y, int(bar_w * remaining), bar_h))

        label = self.small_font.render("Press SPACE!", True, (255, 220, 100))
        surface.blit(label, ((SCREEN_WIDTH - label.get_width()) // 2, bar_y + 16))

    def _draw_reel(self, surface):
        """Draw the reel timing minigame."""
        title = self.font.render("Reel it in!", True, WHITE)
        surface.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 60))

        # Fish name and rarity
        if self.fish:
            rarity_colors = {
                "common": (180, 180, 180),
                "uncommon": (100, 200, 100),
                "rare": (255, 200, 50),
            }
            color = rarity_colors.get(self.fish.rarity, WHITE)
            name_text = self.font.render(f"? {self.fish.rarity.upper()} ?", True, color)
            surface.blit(name_text, ((SCREEN_WIDTH - name_text.get_width()) // 2, 95))

        # Vertical reel bar
        bx, by = REEL_BAR_X, REEL_BAR_Y

        # Bar background
        pygame.draw.rect(surface, (30, 30, 50), (bx, by, REEL_BAR_WIDTH, REEL_BAR_HEIGHT))
        pygame.draw.rect(surface, WHITE, (bx, by, REEL_BAR_WIDTH, REEL_BAR_HEIGHT), 2)

        # Sweet spot zone (green area)
        sweet_top = by + int((self.sweet_spot_y - self.sweet_spot_size / 2) * REEL_BAR_HEIGHT)
        sweet_h = int(self.sweet_spot_size * REEL_BAR_HEIGHT)
        sweet_surf = pygame.Surface((REEL_BAR_WIDTH - 4, sweet_h), pygame.SRCALPHA)
        sweet_surf.fill((50, 200, 80, 120))
        surface.blit(sweet_surf, (bx + 2, sweet_top))
        pygame.draw.rect(surface, (80, 255, 120),
                         (bx + 2, sweet_top, REEL_BAR_WIDTH - 4, sweet_h), 1)

        # Moving indicator (horizontal line)
        ind_y = by + int(self.reel_indicator_y * REEL_BAR_HEIGHT)
        # Check if in sweet spot for color
        half_sweet = self.sweet_spot_size / 2
        in_sweet = abs(self.reel_indicator_y - self.sweet_spot_y) <= half_sweet
        ind_color = (100, 255, 100) if in_sweet else (255, 80, 80)
        pygame.draw.line(surface, ind_color, (bx + 2, ind_y), (bx + REEL_BAR_WIDTH - 2, ind_y), 3)

        # Progress bar (horizontal, below the reel bar)
        prog_y = by + REEL_BAR_HEIGHT + 20
        prog_w = 160
        prog_h = 16
        prog_x = bx + REEL_BAR_WIDTH // 2 - prog_w // 2
        pygame.draw.rect(surface, (40, 40, 60), (prog_x, prog_y, prog_w, prog_h))
        pygame.draw.rect(surface, WHITE, (prog_x, prog_y, prog_w, prog_h), 1)
        fill_w = int(prog_w * self.reel_progress)
        prog_color = (80, 200, 100) if self.reel_progress > 0.3 else (200, 200, 50)
        if self.reel_progress > 0.7:
            prog_color = (50, 255, 80)
        pygame.draw.rect(surface, prog_color, (prog_x + 1, prog_y + 1, fill_w - 2, prog_h - 2))

        label = self.small_font.render("Tap SPACE to reel!", True, (200, 200, 200))
        surface.blit(label, ((SCREEN_WIDTH - label.get_width()) // 2, prog_y + 24))

        # Draw fish silhouette on the left side
        if self.fish:
            fish_sprite = get_fish_sprite(self.fish.sprite_id)
            # Scale up 3x for visibility
            big = pygame.transform.scale(fish_sprite, (48, 48))
            # Oscillate position
            fx = SCREEN_WIDTH // 2 - 100
            fy = SCREEN_HEIGHT // 2 + int(math.sin(self.phase_timer * 2) * 20)
            # Make it semi-transparent (silhouette)
            big.set_alpha(120)
            surface.blit(big, (fx, fy))

    def _draw_result(self, surface):
        """Draw catch/fail result screen."""
        if self.result_success and self.fish:
            # Show fish sprite scaled up
            fish_sprite = get_fish_sprite(self.fish.sprite_id)
            big = pygame.transform.scale(fish_sprite, (64, 64))
            fx = (SCREEN_WIDTH - 64) // 2
            fy = SCREEN_HEIGHT // 2 - 80
            surface.blit(big, (fx, fy))

            # Fish name
            name_text = self.title_font.render(self.fish.name, True, self.result_color)
            surface.blit(name_text,
                         ((SCREEN_WIDTH - name_text.get_width()) // 2,
                          SCREEN_HEIGHT // 2))

            # Rarity
            rarity_text = self.font.render(
                f"({self.fish.rarity.upper()})", True, self.result_color)
            surface.blit(rarity_text,
                         ((SCREEN_WIDTH - rarity_text.get_width()) // 2,
                          SCREEN_HEIGHT // 2 + 35))

            # Stats
            stats = f"Heals: {self.fish.heal_value} HP  |  Sell: {self.fish.sell_price}g"
            stats_text = self.small_font.render(stats, True, (200, 200, 200))
            surface.blit(stats_text,
                         ((SCREEN_WIDTH - stats_text.get_width()) // 2,
                          SCREEN_HEIGHT // 2 + 65))

            if self.fish.heal_value > 0 and self.player.hp < self.player.max_hp:
                eat_text = self.small_font.render(
                    "Press SPACE to eat and heal!", True, (100, 255, 100))
                surface.blit(eat_text,
                             ((SCREEN_WIDTH - eat_text.get_width()) // 2,
                              SCREEN_HEIGHT // 2 + 95))
            else:
                dismiss = self.small_font.render("Press SPACE to continue", True, (180, 180, 180))
                surface.blit(dismiss,
                             ((SCREEN_WIDTH - dismiss.get_width()) // 2,
                              SCREEN_HEIGHT // 2 + 95))
        else:
            # Fail message
            msg = self.title_font.render(self.result_message, True, self.result_color)
            surface.blit(msg, ((SCREEN_WIDTH - msg.get_width()) // 2, SCREEN_HEIGHT // 2 - 20))

            dismiss = self.small_font.render("Press SPACE to continue", True, (180, 180, 180))
            surface.blit(dismiss,
                         ((SCREEN_WIDTH - dismiss.get_width()) // 2, SCREEN_HEIGHT // 2 + 30))

    def _draw_bobber(self, surface, cx, cy, dip):
        """Draw a small bobber at (cx, cy) with optional dip offset."""
        # Bobber: red/white circle
        by = cy + dip
        pygame.draw.circle(surface, (200, 50, 30), (cx, by), 6)
        pygame.draw.circle(surface, WHITE, (cx, by - 2), 3)
        # Line going up
        pygame.draw.line(surface, (120, 120, 120), (cx, by - 6), (cx, by - 30), 1)

    def _draw_instructions(self, surface):
        """Draw ESC to cancel hint."""
        hint = self.small_font.render("ESC: Cancel", True, (100, 100, 120))
        surface.blit(hint, (10, SCREEN_HEIGHT - 25))
