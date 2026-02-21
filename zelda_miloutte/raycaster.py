"""Wolfenstein 3D-style raycasting renderer for the 3D dungeon level."""

import math
import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT


# Wall colors by tile value in the 3D map
# 1 = stone wall, 2 = mossy wall, 3 = brick wall, 4 = boss door wall
WALL_COLORS = {
    1: (130, 130, 140),   # Stone gray
    2: (80, 110, 70),     # Mossy green-gray
    3: (140, 90, 55),     # Brick brown
    4: (120, 40, 160),    # Boss purple
    5: (100, 60, 60),     # Dark red stone
}

CEILING_COLOR = (30, 30, 50)
FLOOR_COLOR = (60, 50, 40)
FOG_COLOR = (15, 12, 20)

FOV = math.pi / 3       # 60 degree field of view
HALF_FOV = FOV / 2
MAX_DEPTH = 20


class Raycaster:
    """Casts rays against a 2D tile grid and renders a first-person 3D view."""

    def __init__(self, map_data):
        self.map_data = map_data
        self.map_height = len(map_data)
        self.map_width = len(map_data[0]) if self.map_height > 0 else 0
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

        # Column rendering strip width (2px strips for performance)
        self.strip_width = 2
        self.num_rays = self.width // self.strip_width
        self.delta_angle = FOV / self.num_rays

        # Pre-create the rendering surface
        self.surface = pygame.Surface((self.width, self.height))

    def _is_wall(self, x, y):
        """Check if map position is a wall (non-zero)."""
        if x < 0 or x >= self.map_width or y < 0 or y >= self.map_height:
            return True
        return self.map_data[y][x] > 0

    def _get_wall_type(self, x, y):
        """Get the wall type at a position."""
        if x < 0 or x >= self.map_width or y < 0 or y >= self.map_height:
            return 1
        return self.map_data[y][x]

    def cast_rays(self, px, py, angle):
        """Cast all rays and return list of (perp_dist, wall_type, side) tuples.

        Uses DDA (Digital Differential Analyzer) algorithm.
        """
        results = []
        ray_angle = angle - HALF_FOV

        for _ in range(self.num_rays):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # Avoid division by zero
            if abs(cos_a) < 1e-8:
                cos_a = 1e-8 if cos_a >= 0 else -1e-8
            if abs(sin_a) < 1e-8:
                sin_a = 1e-8 if sin_a >= 0 else -1e-8

            # Current map cell
            map_x = int(px)
            map_y = int(py)

            # Length of ray from one side to next
            delta_dist_x = abs(1.0 / cos_a)
            delta_dist_y = abs(1.0 / sin_a)

            # Step direction and initial side distance
            if cos_a < 0:
                step_x = -1
                side_dist_x = (px - map_x) * delta_dist_x
            else:
                step_x = 1
                side_dist_x = (map_x + 1.0 - px) * delta_dist_x

            if sin_a < 0:
                step_y = -1
                side_dist_y = (py - map_y) * delta_dist_y
            else:
                step_y = 1
                side_dist_y = (map_y + 1.0 - py) * delta_dist_y

            # DDA loop
            hit = False
            side = 0  # 0 = vertical wall (x-side), 1 = horizontal wall (y-side)

            for _ in range(MAX_DEPTH * 2):
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist_x
                    map_x += step_x
                    side = 0
                else:
                    side_dist_y += delta_dist_y
                    map_y += step_y
                    side = 1

                if self._is_wall(map_x, map_y):
                    hit = True
                    break

            if not hit:
                results.append((MAX_DEPTH, 1, 0))
            else:
                # Calculate perpendicular distance to avoid fish-eye
                if side == 0:
                    perp_dist = side_dist_x - delta_dist_x
                else:
                    perp_dist = side_dist_y - delta_dist_y

                # Fix fish-eye: correct for angle difference from center
                perp_dist *= math.cos(ray_angle - angle)

                if perp_dist < 0.01:
                    perp_dist = 0.01

                wall_type = self._get_wall_type(map_x, map_y)
                results.append((perp_dist, wall_type, side))

            ray_angle += self.delta_angle

        return results

    def render(self, surface, px, py, angle, sprites=None):
        """Render the 3D view onto the given surface.

        Args:
            surface: pygame Surface to render onto
            px, py: player position in tile-space (float)
            angle: player viewing angle in radians
            sprites: optional list of (world_x, world_y, color, size, sprite_surface) for entities
        """
        self.surface.fill(FOG_COLOR)

        # Draw ceiling gradient
        half_h = self.height // 2
        for y in range(half_h):
            t = y / half_h
            r = int(CEILING_COLOR[0] * t + FOG_COLOR[0] * (1 - t))
            g = int(CEILING_COLOR[1] * t + FOG_COLOR[1] * (1 - t))
            b = int(CEILING_COLOR[2] * t + FOG_COLOR[2] * (1 - t))
            pygame.draw.line(self.surface, (r, g, b), (0, y), (self.width, y))

        # Draw floor gradient
        for y in range(half_h, self.height):
            t = (y - half_h) / half_h
            r = int(FLOOR_COLOR[0] * t + FOG_COLOR[0] * (1 - t))
            g = int(FLOOR_COLOR[1] * t + FOG_COLOR[1] * (1 - t))
            b = int(FLOOR_COLOR[2] * t + FOG_COLOR[2] * (1 - t))
            pygame.draw.line(self.surface, (r, g, b), (0, y), (self.width, y))

        # Cast rays
        wall_data = self.cast_rays(px, py, angle)

        # Store z-buffer for sprite clipping
        z_buffer = []

        # Draw walls
        for i, (dist, wall_type, side) in enumerate(wall_data):
            z_buffer.append(dist)

            if dist >= MAX_DEPTH:
                continue

            # Wall height based on distance
            wall_height = int(self.height / dist)
            if wall_height > self.height * 4:
                wall_height = self.height * 4

            # Center vertically
            draw_start = half_h - wall_height // 2
            draw_end = half_h + wall_height // 2

            # Get base color
            base_color = WALL_COLORS.get(wall_type, WALL_COLORS[1])

            # Darken one side for depth perception
            if side == 1:
                color = tuple(max(0, c - 35) for c in base_color)
            else:
                color = base_color

            # Distance fog
            fog_factor = min(1.0, dist / MAX_DEPTH)
            color = tuple(
                int(c * (1 - fog_factor) + FOG_COLOR[ci] * fog_factor)
                for ci, c in enumerate(color)
            )

            x = i * self.strip_width
            pygame.draw.rect(
                self.surface, color,
                (x, draw_start, self.strip_width, draw_end - draw_start)
            )

        # Draw sprites (enemies, items, etc.)
        if sprites:
            self._render_sprites(px, py, angle, sprites, z_buffer)

        surface.blit(self.surface, (0, 0))

    def _render_sprites(self, px, py, angle, sprites, z_buffer):
        """Render billboarded sprites sorted by distance (painter's algorithm)."""
        # Calculate distance and screen position for each sprite
        sprite_data = []
        for sprite in sprites:
            sx, sy = sprite[0], sprite[1]
            color = sprite[2]
            size = sprite[3]
            sprite_surface = sprite[4] if len(sprite) > 4 else None
            hp_ratio = sprite[5] if len(sprite) > 5 else None

            # Vector from player to sprite
            dx = sx - px
            dy = sy - py
            dist = math.sqrt(dx * dx + dy * dy)

            if dist < 0.1:
                continue

            # Angle to sprite relative to player's viewing direction
            sprite_angle = math.atan2(dy, dx)
            relative_angle = sprite_angle - angle

            # Normalize to [-pi, pi]
            while relative_angle > math.pi:
                relative_angle -= 2 * math.pi
            while relative_angle < -math.pi:
                relative_angle += 2 * math.pi

            # Skip if behind the player (outside FOV with margin)
            if abs(relative_angle) > HALF_FOV + 0.3:
                continue

            sprite_data.append((dist, relative_angle, color, size, sprite_surface, hp_ratio))

        # Sort far to near (painter's algorithm)
        sprite_data.sort(key=lambda s: -s[0])

        for dist, rel_angle, color, size, sprite_surf, hp_ratio in sprite_data:
            if dist >= MAX_DEPTH:
                continue

            # Screen x position
            screen_x = int((rel_angle / FOV + 0.5) * self.width)

            # Sprite size on screen
            sprite_height = int(self.height / dist * size)
            sprite_width = sprite_height

            if sprite_height < 1:
                continue

            # Sprite draw position (centered)
            draw_x = screen_x - sprite_width // 2
            draw_y = self.height // 2 - sprite_height // 2

            # Distance fog factor
            fog_factor = min(1.0, dist / MAX_DEPTH)

            if sprite_surf is not None:
                # Scale and draw the provided sprite surface
                scaled = pygame.transform.scale(sprite_surf, (sprite_width, sprite_height))
                # Apply fog by blending
                fog_overlay = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
                fog_alpha = int(fog_factor * 200)
                fog_overlay.fill((*FOG_COLOR, fog_alpha))
                scaled.blit(fog_overlay, (0, 0))
                # Clip against z-buffer column by column
                for col in range(max(0, draw_x), min(self.width, draw_x + sprite_width)):
                    buf_idx = col // self.strip_width
                    if buf_idx < len(z_buffer) and dist < z_buffer[buf_idx]:
                        src_col = col - draw_x
                        self.surface.blit(
                            scaled, (col, draw_y),
                            (src_col, 0, 1, sprite_height)
                        )
            else:
                # Draw as a colored rectangle with shading
                fogged_color = tuple(
                    int(c * (1 - fog_factor) + FOG_COLOR[ci] * fog_factor)
                    for ci, c in enumerate(color)
                )

                # Draw column by column, checking z-buffer
                for col in range(max(0, draw_x), min(self.width, draw_x + sprite_width)):
                    buf_idx = col // self.strip_width
                    if buf_idx < len(z_buffer) and dist < z_buffer[buf_idx]:
                        pygame.draw.line(
                            self.surface, fogged_color,
                            (col, max(0, draw_y)), (col, min(self.height, draw_y + sprite_height))
                        )

            # Draw health bar above sprite if hp_ratio is provided
            if hp_ratio is not None and hp_ratio < 1.0:
                bar_w = sprite_width
                bar_h = max(2, sprite_height // 10)
                bar_y = draw_y - bar_h - 2
                if bar_y >= 0:
                    # Background
                    for col in range(max(0, draw_x), min(self.width, draw_x + bar_w)):
                        buf_idx = col // self.strip_width
                        if buf_idx < len(z_buffer) and dist < z_buffer[buf_idx]:
                            pygame.draw.line(
                                self.surface, (40, 40, 40),
                                (col, bar_y), (col, bar_y + bar_h)
                            )
                    # Health fill
                    fill_w = int(bar_w * hp_ratio)
                    for col in range(max(0, draw_x), min(self.width, draw_x + fill_w)):
                        buf_idx = col // self.strip_width
                        if buf_idx < len(z_buffer) and dist < z_buffer[buf_idx]:
                            pygame.draw.line(
                                self.surface, (220, 30, 30),
                                (col, bar_y), (col, bar_y + bar_h)
                            )

    def draw_minimap(self, surface, px, py, angle, enemies=None, items=None):
        """Draw a small minimap overlay in the corner."""
        map_size = 120
        tile_size = map_size // max(self.map_width, self.map_height)
        if tile_size < 2:
            tile_size = 2

        actual_w = self.map_width * tile_size
        actual_h = self.map_height * tile_size

        # Position in top-right corner
        offset_x = self.width - actual_w - 10
        offset_y = 10

        # Semi-transparent background
        bg = pygame.Surface((actual_w + 4, actual_h + 4), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 160))
        surface.blit(bg, (offset_x - 2, offset_y - 2))

        # Draw tiles
        for row in range(self.map_height):
            for col in range(self.map_width):
                val = self.map_data[row][col]
                x = offset_x + col * tile_size
                y = offset_y + row * tile_size
                if val > 0:
                    color = WALL_COLORS.get(val, (100, 100, 100))
                    color = tuple(min(255, c + 40) for c in color)
                else:
                    color = (50, 45, 35)
                pygame.draw.rect(surface, color, (x, y, tile_size, tile_size))

        # Draw items on minimap
        if items:
            for item in items:
                if item.get("alive", True):
                    ix = offset_x + int(item["x"] * tile_size)
                    iy = offset_y + int(item["y"] * tile_size)
                    pygame.draw.circle(surface, (255, 255, 50), (ix, iy), max(2, tile_size // 3))

        # Draw enemies on minimap
        if enemies:
            for enemy in enemies:
                if enemy.get("alive", True):
                    ex = offset_x + int(enemy["x"] * tile_size)
                    ey = offset_y + int(enemy["y"] * tile_size)
                    pygame.draw.circle(surface, (220, 50, 50), (ex, ey), max(2, tile_size // 3))

        # Draw player position and direction
        player_mx = offset_x + int(px * tile_size)
        player_my = offset_y + int(py * tile_size)
        pygame.draw.circle(surface, (50, 200, 50), (player_mx, player_my), max(3, tile_size // 2))

        # Direction indicator
        dir_len = tile_size * 2
        end_x = player_mx + int(math.cos(angle) * dir_len)
        end_y = player_my + int(math.sin(angle) * dir_len)
        pygame.draw.line(surface, (100, 255, 100), (player_mx, player_my), (end_x, end_y), 2)
