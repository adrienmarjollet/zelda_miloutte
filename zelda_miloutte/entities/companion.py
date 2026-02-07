"""Companion/pet entity that follows the player and provides perks."""

import math
import random
import pygame
from zelda_miloutte.entities.entity import Entity


# Companion constants
COMPANION_SIZE = 16
COMPANION_FOLLOW_DIST = 40.0
COMPANION_FOLLOW_SPEED = 0.08  # Lerp factor per frame
COMPANION_PET_COOLDOWN = 30.0  # Seconds between pet interactions
COMPANION_PET_HEAL = 1
COMPANION_SNIFF_RANGE = 100.0  # Distance to detect hidden chests

# Perk values
CAT_STEALTH_FACTOR = 0.3   # Enemies detect 30% later (multiplied onto chase range)
FOX_SPEED_BONUS = 0.10     # +10% movement speed
FAIRY_MP_REGEN_BONUS = 0.50  # +50% MP regen rate


class Companion(Entity):
    """Base companion that follows the player. Subclass for type-specific perks."""

    # Override in subclasses
    companion_type = "companion"
    companion_name = "Companion"
    perk_description = ""

    def __init__(self, x, y):
        super().__init__(x, y, COMPANION_SIZE, COMPANION_SIZE, (255, 255, 255))
        self.state = "idle"  # "idle", "follow", "happy"
        self.facing = "down"

        # Follow target (will be set to player position)
        self.target_x = x
        self.target_y = y

        # Animation
        self._anim_timer = 0.0
        self._anim_index = 0
        self._anim_duration = 0.3
        self._frames = None
        self._load_frames()

        # Pet interaction
        self.pet_cooldown = 0.0
        self.happy_timer = 0.0
        self.happy_duration = 1.0

        # Sniff / alert state (near hidden items)
        self.alert = False
        self._alert_timer = 0.0

    def _load_frames(self):
        """Load sprite frames. Override in subclasses."""
        pass

    def _get_current_frame(self):
        """Return the current animation frame surface."""
        if self._frames is None:
            return None
        anim_set = self._frames.get(self.state, self._frames.get("idle"))
        if anim_set is None:
            return None
        dir_frames = anim_set.get(self.facing, anim_set.get("down"))
        if dir_frames is None:
            return None
        idx = self._anim_index % len(dir_frames)
        return dir_frames[idx]

    def follow_player(self, player):
        """Update target position to follow player with offset."""
        # Calculate desired position behind the player
        offset_x, offset_y = 0, 0
        if player.facing == "down":
            offset_x, offset_y = -15, -COMPANION_FOLLOW_DIST
        elif player.facing == "up":
            offset_x, offset_y = 15, COMPANION_FOLLOW_DIST
        elif player.facing == "left":
            offset_x, offset_y = COMPANION_FOLLOW_DIST, -10
        elif player.facing == "right":
            offset_x, offset_y = -COMPANION_FOLLOW_DIST, -10

        self.target_x = player.x + offset_x
        self.target_y = player.y + offset_y

    def update(self, dt, player=None):
        """Update companion position and animation."""
        # Update pet cooldown
        if self.pet_cooldown > 0:
            self.pet_cooldown -= dt

        # Update happy state
        if self.happy_timer > 0:
            self.happy_timer -= dt
            self.state = "happy"
            if self.happy_timer <= 0:
                self.state = "follow" if player and player.is_moving else "idle"

        # Follow player if provided
        if player is not None and self.happy_timer <= 0:
            self.follow_player(player)

            # Smoothly lerp toward target
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = math.sqrt(dx * dx + dy * dy)

            if dist > 2.0:
                # Use faster lerp when far away
                lerp = COMPANION_FOLLOW_SPEED
                if dist > COMPANION_FOLLOW_DIST * 2:
                    lerp = 0.15  # Catch up faster
                if dist > COMPANION_FOLLOW_DIST * 4:
                    # Teleport if way too far (e.g., area transition)
                    self.x = self.target_x
                    self.y = self.target_y
                else:
                    self.x += dx * lerp
                    self.y += dy * lerp

                self.state = "follow"

                # Update facing based on movement direction
                if abs(dx) > abs(dy):
                    self.facing = "left" if dx < 0 else "right"
                else:
                    self.facing = "up" if dy < 0 else "down"
            else:
                if self.happy_timer <= 0:
                    self.state = "idle"

        # Update animation
        self._anim_timer += dt
        if self._anim_timer >= self._anim_duration:
            self._anim_timer -= self._anim_duration
            self._anim_index = (self._anim_index + 1) % 2

        # Alert timer
        if self._alert_timer > 0:
            self._alert_timer -= dt
            if self._alert_timer <= 0:
                self.alert = False

    def check_nearby_secrets(self, chests):
        """Check if companion is near any unopened hidden chests. Sets alert state."""
        for chest in chests:
            if chest.opened:
                continue
            dx = self.center_x - chest.center_x
            dy = self.center_y - chest.center_y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < COMPANION_SNIFF_RANGE:
                self.alert = True
                self._alert_timer = 0.5  # Reset alert timer
                return True
        self.alert = False
        return False

    def try_pet(self, player):
        """Attempt to pet the companion. Returns True if successful."""
        if self.pet_cooldown > 0:
            return False

        # Check distance to player
        dx = self.center_x - player.center_x
        dy = self.center_y - player.center_y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > COMPANION_FOLLOW_DIST * 1.5:
            return False

        # Pet successful
        self.pet_cooldown = COMPANION_PET_COOLDOWN
        self.happy_timer = self.happy_duration
        self.state = "happy"

        # Heal player
        player.heal(COMPANION_PET_HEAL)

        return True

    def apply_perk(self, player):
        """Apply this companion's passive perk. Called each frame by GameplayState."""
        pass

    def get_perk_speed_bonus(self):
        """Return speed multiplier bonus from this companion. Default 0."""
        return 0.0

    def get_stealth_factor(self):
        """Return enemy detection range reduction factor. Default 0."""
        return 0.0

    def get_mp_regen_bonus(self):
        """Return MP regen multiplier bonus from this companion. Default 0."""
        return 0.0

    def draw(self, surface, camera):
        if not self.alive:
            return

        frame = self._get_current_frame()
        if frame is None:
            # Fallback: draw colored rect
            r = self.rect.move(-camera.x, -camera.y)
            pygame.draw.rect(surface, self.color, r)
            return

        ox, oy = -camera.x, -camera.y
        r = self.rect.move(ox, oy)
        fx = r.centerx - frame.get_width() // 2
        fy = r.centery - frame.get_height() // 2
        surface.blit(frame, (fx, fy))

        # Draw alert indicator (exclamation mark) when sniffing secrets
        if self.alert:
            alert_x = r.centerx - 3
            alert_y = r.top - 14
            font = pygame.font.Font(None, 18)
            alert_surf = font.render("!", True, (255, 220, 50))
            surface.blit(alert_surf, (alert_x, alert_y))

    def to_dict(self):
        """Serialize companion state for saving."""
        return {
            "type": self.companion_type,
            "pet_cooldown": self.pet_cooldown,
        }


class Cat(Companion):
    """Miloutte the Cat - stealth perk (enemies detect player 30% later)."""

    companion_type = "cat"
    companion_name = "Miloutte"
    perk_description = "Stealth: enemies detect you 30% later"

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (220, 140, 50)

    def _load_frames(self):
        from zelda_miloutte.sprites.companion_sprites import get_cat_frames
        self._frames = get_cat_frames()

    def get_stealth_factor(self):
        return CAT_STEALTH_FACTOR


class Fox(Companion):
    """Rusty the Fox - speed perk (+10% player movement speed)."""

    companion_type = "fox"
    companion_name = "Rusty"
    perk_description = "Speed: +10% movement speed"

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (200, 70, 30)

    def _load_frames(self):
        from zelda_miloutte.sprites.companion_sprites import get_fox_frames
        self._frames = get_fox_frames()

    def get_perk_speed_bonus(self):
        return FOX_SPEED_BONUS


class Fairy(Companion):
    """Lumina the Fairy - MP regen perk (+50% MP regen, glows)."""

    companion_type = "fairy"
    companion_name = "Lumina"
    perk_description = "Glow: +50% MP regen, sparkle trail"

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (100, 180, 255)
        self._glow_timer = 0.0

    def _load_frames(self):
        from zelda_miloutte.sprites.companion_sprites import get_fairy_frames
        self._frames = get_fairy_frames()

    def get_mp_regen_bonus(self):
        return FAIRY_MP_REGEN_BONUS

    def update(self, dt, player=None):
        super().update(dt, player)
        self._glow_timer += dt

    def draw(self, surface, camera):
        """Draw fairy with glow effect."""
        if not self.alive:
            return

        # Draw a subtle glow circle behind the fairy
        ox, oy = -camera.x, -camera.y
        glow_x = int(self.center_x + ox)
        glow_y = int(self.center_y + oy)

        # Pulsing glow
        pulse = 0.6 + 0.4 * math.sin(self._glow_timer * 3.0)
        glow_radius = int(12 * pulse)
        glow_alpha = int(40 * pulse)

        glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (100, 180, 255, glow_alpha), (glow_radius, glow_radius), glow_radius)
        surface.blit(glow_surf, (glow_x - glow_radius, glow_y - glow_radius))

        # Draw the sprite on top
        super().draw(surface, camera)


def create_companion(companion_type, x, y):
    """Factory function to create a companion by type string."""
    types = {
        "cat": Cat,
        "fox": Fox,
        "fairy": Fairy,
    }
    cls = types.get(companion_type, Cat)
    return cls(x, y)
