import pygame
from zelda_miloutte.settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE

# Room dimensions in tiles (screen-sized rooms)
ROOM_WIDTH_TILES = 25   # 25 * 32 = 800 pixels
ROOM_HEIGHT_TILES = 18  # 18 * 32 = 576 pixels
ROOM_WIDTH_PX = ROOM_WIDTH_TILES * TILE_SIZE   # 800
ROOM_HEIGHT_PX = ROOM_HEIGHT_TILES * TILE_SIZE  # 576

# Transition timing
ROOM_TRANSITION_PAUSE = 0.08   # Brief pause before scroll starts
ROOM_TRANSITION_DURATION = 0.5  # Scroll duration in seconds


class RoomManager:
    """Divides a map into screen-sized rooms and manages room transitions.

    Each room is identified by (room_x, room_y) grid coordinates.
    Provides room-locked camera bounds and smooth scroll transitions
    when the player crosses room boundaries.
    """

    def __init__(self, map_cols, map_rows):
        self.map_cols = map_cols
        self.map_rows = map_rows
        self.map_pixel_width = map_cols * TILE_SIZE
        self.map_pixel_height = map_rows * TILE_SIZE

        # Number of rooms in each direction (at least 1)
        self.rooms_x = max(1, (map_cols + ROOM_WIDTH_TILES - 1) // ROOM_WIDTH_TILES)
        self.rooms_y = max(1, (map_rows + ROOM_HEIGHT_TILES - 1) // ROOM_HEIGHT_TILES)

        # Current room
        self.current_room = (0, 0)

        # Transition state
        self.transitioning = False
        self._transition_timer = 0.0
        self._transition_phase = "pause"  # "pause" -> "scroll"
        self._transition_direction = (0, 0)  # (dx, dy) in room coords
        self._old_room = (0, 0)
        self._new_room = (0, 0)
        self._old_camera_x = 0.0
        self._old_camera_y = 0.0
        self._new_camera_x = 0.0
        self._new_camera_y = 0.0

        # Track cleared rooms: set of (room_x, room_y) per area
        self.cleared_rooms = set()

        # Combat lock state (dungeon rooms that lock doors when entered)
        self.combat_locked = False
        self._combat_lock_rooms = set()  # rooms that should lock when entered with enemies
        self._door_flash_timer = 0.0

    def get_room_at(self, px, py):
        """Get room coordinates for a pixel position."""
        room_x = max(0, min(int(px) // ROOM_WIDTH_PX, self.rooms_x - 1))
        room_y = max(0, min(int(py) // ROOM_HEIGHT_PX, self.rooms_y - 1))
        return (room_x, room_y)

    def get_room_bounds(self, room_x, room_y):
        """Get the pixel bounds of a room as (left, top, right, bottom).

        Clamps to map edges so edge rooms don't extend past the map.
        """
        left = room_x * ROOM_WIDTH_PX
        top = room_y * ROOM_HEIGHT_PX
        right = min(left + ROOM_WIDTH_PX, self.map_pixel_width)
        bottom = min(top + ROOM_HEIGHT_PX, self.map_pixel_height)
        return (left, top, right, bottom)

    def get_camera_pos_for_room(self, room_x, room_y):
        """Get the camera top-left position that shows this room.

        Centers the view if the room is smaller than the screen.
        """
        left, top, right, bottom = self.get_room_bounds(room_x, room_y)
        room_w = right - left
        room_h = bottom - top

        if room_w < SCREEN_WIDTH:
            cam_x = left - (SCREEN_WIDTH - room_w) / 2
        else:
            cam_x = float(left)

        if room_h < SCREEN_HEIGHT:
            cam_y = top - (SCREEN_HEIGHT - room_h) / 2
        else:
            cam_y = float(top)

        return cam_x, cam_y

    def set_room_from_player(self, player):
        """Set current room based on player position (no transition)."""
        self.current_room = self.get_room_at(player.center_x, player.center_y)

    def check_room_transition(self, player):
        """Check if the player has crossed into a new room.

        Returns True if a transition was started.
        """
        if self.transitioning:
            return False

        new_room = self.get_room_at(player.center_x, player.center_y)
        if new_room == self.current_room:
            return False

        # Determine direction
        dx = new_room[0] - self.current_room[0]
        dy = new_room[1] - self.current_room[1]

        # Start transition
        self._start_transition(self.current_room, new_room, (dx, dy))
        return True

    def _start_transition(self, old_room, new_room, direction):
        """Begin a room scroll transition."""
        self.transitioning = True
        self._transition_phase = "pause"
        self._transition_timer = 0.0
        self._transition_direction = direction
        self._old_room = old_room
        self._new_room = new_room
        self._old_camera_x, self._old_camera_y = self.get_camera_pos_for_room(*old_room)
        self._new_camera_x, self._new_camera_y = self.get_camera_pos_for_room(*new_room)

    def update_transition(self, dt, player):
        """Update the room transition scroll.

        Returns (camera_x, camera_y) during transition, or None if not transitioning.
        Also moves the player with the scroll.
        """
        if not self.transitioning:
            return None

        self._transition_timer += dt

        if self._transition_phase == "pause":
            if self._transition_timer >= ROOM_TRANSITION_PAUSE:
                self._transition_timer = 0.0
                self._transition_phase = "scroll"
                # Store player's position relative to the scroll start
                self._player_start_x = player.x
                self._player_start_y = player.y
            # During pause, keep camera at old room
            return (self._old_camera_x, self._old_camera_y)

        # Scroll phase
        progress = min(1.0, self._transition_timer / ROOM_TRANSITION_DURATION)
        # Smooth ease in/out
        t = self._ease_in_out(progress)

        cam_x = self._old_camera_x + (self._new_camera_x - self._old_camera_x) * t
        cam_y = self._old_camera_y + (self._new_camera_y - self._old_camera_y) * t

        # Move player with the scroll
        player_offset_x = (self._new_camera_x - self._old_camera_x) * t
        player_offset_y = (self._new_camera_y - self._old_camera_y) * t
        player.x = self._player_start_x + player_offset_x
        player.y = self._player_start_y + player_offset_y

        if progress >= 1.0:
            # Transition complete
            self.transitioning = False
            self.current_room = self._new_room

        return (cam_x, cam_y)

    @staticmethod
    def _ease_in_out(t):
        """Smooth ease-in-out interpolation."""
        if t < 0.5:
            return 2 * t * t
        return 1 - (-2 * t + 2) ** 2 / 2

    def is_entity_in_current_room(self, entity):
        """Check if an entity is in the current room."""
        room = self.get_room_at(entity.center_x, entity.center_y)
        return room == self.current_room

    def get_enemies_in_room(self, enemies, room=None):
        """Return enemies that are in the specified room (or current room)."""
        if room is None:
            room = self.current_room
        return [e for e in enemies if self.get_room_at(e.center_x, e.center_y) == room]

    def check_room_cleared(self, enemies):
        """Check if the current room has been cleared of all enemies.

        Returns True if the room was just cleared (first time).
        """
        if self.current_room in self.cleared_rooms:
            return False

        room_enemies = self.get_enemies_in_room(enemies)
        if len(room_enemies) == 0:
            # Check if there were ever enemies in this room by checking if
            # any dead enemies existed here (we track by marking cleared)
            self.cleared_rooms.add(self.current_room)
            return True
        return False

    def mark_combat_lock_room(self, room):
        """Mark a room as one that should lock doors when entered with enemies."""
        self._combat_lock_rooms.add(room)

    def should_lock_combat(self, enemies):
        """Check if the current room should be combat-locked.

        Returns True if the room has enemies and is marked for combat lock.
        """
        if self.current_room not in self._combat_lock_rooms:
            return False
        room_enemies = self.get_enemies_in_room(enemies)
        return len(room_enemies) > 0

    def update_combat_lock(self, enemies, dt):
        """Update combat lock state. Returns True when lock is first released."""
        was_locked = self.combat_locked

        if self.combat_locked:
            room_enemies = self.get_enemies_in_room(enemies)
            alive_enemies = [e for e in room_enemies if e.alive]
            if len(alive_enemies) == 0:
                self.combat_locked = False
                self._door_flash_timer = 0.5  # Flash doors for 0.5s
                return True  # Just unlocked

        if self._door_flash_timer > 0:
            self._door_flash_timer -= dt

        return False

    def enter_room(self, enemies):
        """Called when player enters a new room. Sets up combat lock if needed."""
        if self.current_room in self._combat_lock_rooms:
            room_enemies = self.get_enemies_in_room(enemies)
            alive_enemies = [e for e in room_enemies if e.alive]
            if len(alive_enemies) > 0:
                self.combat_locked = True

    @property
    def door_flash_active(self):
        """Whether doors should be flashing (just unlocked)."""
        return self._door_flash_timer > 0

    @property
    def door_flash_alpha(self):
        """Alpha for door flash effect (0-255)."""
        if self._door_flash_timer <= 0:
            return 0
        # Pulsing flash
        import math
        pulse = abs(math.sin(self._door_flash_timer * 20))
        return int(200 * pulse)
