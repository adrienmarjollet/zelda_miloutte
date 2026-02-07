"""Puzzle entities: push blocks, pressure plates, crystal switches, and torches."""

import pygame
from .entity import Entity
from ..settings import TILE_SIZE, GRAY, BROWN, DARK_GRAY
from ..sprites.puzzle_sprites import (
    get_push_block, get_pressure_plate_up, get_pressure_plate_down,
    get_crystal_switch_on, get_crystal_switch_off,
    get_torch_unlit, get_torch_lit,
)
from ..sounds import get_sound_manager


class PushBlock(Entity):
    """A block the player can push by walking into it. Moves one tile in the push direction.
    Snaps to the grid. Stops at walls and other push blocks."""

    def __init__(self, x, y, block_id=None):
        """Create a push block at tile coordinates (converted to pixels internally).

        Args:
            x: Tile X coordinate
            y: Tile Y coordinate
            block_id: Optional string ID for linking with puzzle targets
        """
        px = x * TILE_SIZE
        py = y * TILE_SIZE
        super().__init__(px, py, TILE_SIZE, TILE_SIZE, GRAY)
        self.block_id = block_id
        self.tile_x = x
        self.tile_y = y
        self.sprite = get_push_block()

        # Sliding state
        self._sliding = False
        self._slide_target_x = 0.0
        self._slide_target_y = 0.0
        self._slide_speed = 200.0  # pixels per second

    @property
    def is_sliding(self):
        return self._sliding

    def try_push(self, direction, tilemap, push_blocks):
        """Attempt to push the block one tile in the given direction.

        Args:
            direction: "up", "down", "left", "right"
            tilemap: TileMap for collision checking
            push_blocks: List of all PushBlock instances for block-on-block collision

        Returns:
            True if push succeeded, False if blocked
        """
        if self._sliding:
            return False

        dx, dy = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}[direction]
        new_tx = self.tile_x + dx
        new_ty = self.tile_y + dy

        # Check tile collision
        if tilemap.is_solid(new_tx, new_ty):
            return False

        # Check collision with other push blocks
        for other in push_blocks:
            if other is not self and other.tile_x == new_tx and other.tile_y == new_ty:
                return False

        # Start sliding
        self._sliding = True
        self.tile_x = new_tx
        self.tile_y = new_ty
        self._slide_target_x = float(new_tx * TILE_SIZE)
        self._slide_target_y = float(new_ty * TILE_SIZE)
        get_sound_manager().play_push_block()
        return True

    def update(self, dt):
        """Update sliding animation."""
        if not self._sliding:
            return

        # Move toward target
        target_x = self._slide_target_x
        target_y = self._slide_target_y
        dist_x = target_x - self.x
        dist_y = target_y - self.y
        move = self._slide_speed * dt

        if abs(dist_x) > 0:
            if abs(dist_x) <= move:
                self.x = target_x
            else:
                self.x += move if dist_x > 0 else -move

        if abs(dist_y) > 0:
            if abs(dist_y) <= move:
                self.y = target_y
            else:
                self.y += move if dist_y > 0 else -move

        # Check if arrived
        if abs(self.x - target_x) < 0.5 and abs(self.y - target_y) < 0.5:
            self.x = target_x
            self.y = target_y
            self._sliding = False

    def draw(self, surface, camera):
        """Draw the push block sprite."""
        sx = int(self.x - camera.x)
        sy = int(self.y - camera.y)
        surface.blit(self.sprite, (sx, sy))


class PressurePlate(Entity):
    """Activates when a PushBlock or Player stands on it. Triggers linked targets."""

    def __init__(self, x, y, plate_id=None, linked_targets=None):
        """Create a pressure plate at tile coordinates.

        Args:
            x: Tile X coordinate
            y: Tile Y coordinate
            plate_id: Optional string ID for this plate
            linked_targets: List of target IDs to trigger when pressed
        """
        px = x * TILE_SIZE
        py = y * TILE_SIZE
        super().__init__(px, py, TILE_SIZE, TILE_SIZE, BROWN)
        self.plate_id = plate_id
        self.linked_targets = linked_targets or []
        self.tile_x = x
        self.tile_y = y
        self.pressed = False
        self._was_pressed = False
        self._sprite_up = get_pressure_plate_up()
        self._sprite_down = get_pressure_plate_down()

    def check_activation(self, player, push_blocks):
        """Check if something is standing on the plate.

        Args:
            player: The Player entity
            push_blocks: List of PushBlock entities

        Returns:
            True if the plate just became pressed (state changed to pressed)
        """
        was_pressed = self.pressed

        # Check if player center is on this tile
        player_on = (int(player.center_x) // TILE_SIZE == self.tile_x and
                     int(player.center_y) // TILE_SIZE == self.tile_y)

        # Check if any push block is on this tile
        block_on = any(
            b.tile_x == self.tile_x and b.tile_y == self.tile_y and not b.is_sliding
            for b in push_blocks
        )

        self.pressed = player_on or block_on

        # Return True if just became pressed
        if self.pressed and not was_pressed:
            get_sound_manager().play_switch_click()
            return True
        return False

    def draw(self, surface, camera):
        """Draw the pressure plate."""
        sx = int(self.x - camera.x)
        sy = int(self.y - camera.y)
        sprite = self._sprite_down if self.pressed else self._sprite_up
        surface.blit(sprite, (sx, sy))


class CrystalSwitch(Entity):
    """Hit with sword to toggle. Swaps colored barriers (red open <-> blue open)."""

    def __init__(self, x, y, switch_id=None, linked_targets=None, state=False):
        """Create a crystal switch at tile coordinates.

        Args:
            x: Tile X coordinate
            y: Tile Y coordinate
            switch_id: Optional string ID
            linked_targets: List of target IDs to affect
            state: Initial state (False = red/off, True = blue/on)
        """
        px = x * TILE_SIZE + 2  # center the 28x28 sprite on the 32x32 tile
        py = y * TILE_SIZE + 2
        super().__init__(px, py, 28, 28, DARK_GRAY)
        self.switch_id = switch_id
        self.linked_targets = linked_targets or []
        self.tile_x = x
        self.tile_y = y
        self.state = state  # False = red barriers solid, blue open. True = red open, blue solid.
        self._hit_cooldown = 0.0
        self._sprite_on = get_crystal_switch_on()
        self._sprite_off = get_crystal_switch_off()

    def try_toggle(self):
        """Attempt to toggle the switch. Returns True if toggled.

        Has a cooldown to prevent rapid re-toggling.
        """
        if self._hit_cooldown > 0:
            return False
        self.state = not self.state
        self._hit_cooldown = 0.5
        get_sound_manager().play_switch_click()
        return True

    def update(self, dt):
        if self._hit_cooldown > 0:
            self._hit_cooldown -= dt

    def draw(self, surface, camera):
        """Draw the crystal switch."""
        sx = int(self.x - camera.x)
        sy = int(self.y - camera.y)
        sprite = self._sprite_on if self.state else self._sprite_off
        surface.blit(sprite, (sx, sy))


class Torch(Entity):
    """Unlit by default. Sword interaction lights it. Light all torches to open a linked door."""

    def __init__(self, x, y, torch_id=None, linked_targets=None):
        """Create a torch at tile coordinates.

        Args:
            x: Tile X coordinate
            y: Tile Y coordinate
            torch_id: Optional string ID
            linked_targets: List of target IDs to trigger when all torches are lit
        """
        px = x * TILE_SIZE + 2  # center the 28x28 sprite
        py = y * TILE_SIZE + 2
        super().__init__(px, py, 28, 28, BROWN)
        self.torch_id = torch_id
        self.linked_targets = linked_targets or []
        self.tile_x = x
        self.tile_y = y
        self.lit = False
        self._hit_cooldown = 0.0
        self._sprite_unlit = get_torch_unlit()
        self._sprite_lit = get_torch_lit()

    def try_light(self):
        """Attempt to light the torch. Returns True if just lit.

        Once lit, stays lit (cannot be unlit).
        """
        if self.lit or self._hit_cooldown > 0:
            return False
        self.lit = True
        self._hit_cooldown = 0.5
        get_sound_manager().play_torch_ignite()
        return True

    def update(self, dt):
        if self._hit_cooldown > 0:
            self._hit_cooldown -= dt

    def draw(self, surface, camera):
        """Draw the torch."""
        sx = int(self.x - camera.x)
        sy = int(self.y - camera.y)
        sprite = self._sprite_lit if self.lit else self._sprite_unlit
        surface.blit(sprite, (sx, sy))
