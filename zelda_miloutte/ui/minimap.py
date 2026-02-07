"""Minimap overlay showing current area tile layout, entities, and fog of war."""

import pygame
from zelda_miloutte.settings import SCREEN_WIDTH, TILE_SIZE


# Minimap dimensions
MINIMAP_WIDTH = 120
MINIMAP_HEIGHT = 90
MINIMAP_MARGIN = 8
MINIMAP_BG_ALPHA = 140
MINIMAP_BORDER_COLOR = (200, 200, 200)
MINIMAP_FOG_COLOR = (20, 20, 30)

# Tile colors for the minimap (1 pixel per tile)
TILE_COLORS = {
    0: (34, 139, 34),      # GRASS - green
    1: (128, 128, 128),    # WALL - gray
    2: (0, 80, 0),         # TREE - dark green
    3: (80, 80, 80),       # ROCK - dark gray
    4: (50, 120, 200),     # WATER - blue
    5: (160, 140, 110),    # FLOOR - tan
    6: (180, 130, 70),     # DOOR - light brown
    7: (139, 90, 43),      # DUNGEON_ENTRANCE - brown
    8: (120, 40, 160),     # BOSS_DOOR - purple
    9: (100, 100, 100),    # SPIKES - gray
    10: (0, 0, 0),         # PIT - black
    11: (100, 180, 230),   # DUNGEON_ENTRANCE_2 - ice blue
    12: (34, 139, 34),     # TRANSITION_N - green
    13: (34, 139, 34),     # TRANSITION_S - green
    14: (34, 139, 34),     # TRANSITION_E - green
    15: (34, 139, 34),     # TRANSITION_W - green
    16: (40, 80, 30),      # FOREST_FLOOR - forest green
    17: (210, 180, 120),   # SAND - tan
    18: (200, 60, 20),     # LAVA - orange
}


class Minimap:
    """Small map overlay in the top-right corner of the HUD."""

    def __init__(self):
        self.visible = True
        self._blink_timer = 0.0
        self._player_visible = True
        # Visited tiles: dict of area_id -> set of (col, row)
        self.visited_tiles = {}
        # Reveal radius around the player (in tiles)
        self._reveal_radius = 5
        # Cached surfaces
        self._cached_area_id = None
        self._cached_tile_surface = None
        self._cached_fog_surface = None
        self._cached_visited_count = 0
        self._cached_scale = 1
        self._cached_map_size = (0, 0)

    def toggle(self):
        """Toggle minimap visibility."""
        self.visible = not self.visible

    def reveal_tiles(self, area_id, player_x, player_y, tilemap):
        """Reveal tiles around the player's position."""
        if area_id not in self.visited_tiles:
            self.visited_tiles[area_id] = set()

        visited = self.visited_tiles[area_id]
        old_count = len(visited)
        player_col = int(player_x) // TILE_SIZE
        player_row = int(player_y) // TILE_SIZE
        r = self._reveal_radius

        for row in range(max(0, player_row - r), min(tilemap.rows, player_row + r + 1)):
            for col in range(max(0, player_col - r), min(tilemap.cols, player_col + r + 1)):
                visited.add((col, row))

        # Invalidate cache if area changed or new tiles revealed
        if self._cached_area_id != area_id:
            self._cached_area_id = area_id
            self._cached_tile_surface = None
            self._cached_fog_surface = None
            self._cached_visited_count = len(visited)
        elif len(visited) != old_count:
            # New tiles revealed, fog cache is stale
            self._cached_fog_surface = None
            self._cached_visited_count = len(visited)

    def update(self, dt):
        """Update blink timer for player dot."""
        self._blink_timer += dt
        if self._blink_timer >= 0.4:
            self._blink_timer = 0.0
            self._player_visible = not self._player_visible

    def draw(self, surface, tilemap, player, enemies, chests, npcs, area_id):
        """Draw the minimap on the given surface."""
        if not self.visible:
            return

        visited = self.visited_tiles.get(area_id, set())

        # Calculate scale: fit map into MINIMAP_WIDTH x MINIMAP_HEIGHT
        # Each tile = 1 pixel minimum, scale up if map is small
        scale_x = MINIMAP_WIDTH / tilemap.cols if tilemap.cols > 0 else 1
        scale_y = MINIMAP_HEIGHT / tilemap.rows if tilemap.rows > 0 else 1
        scale = min(scale_x, scale_y)
        scale = max(1, scale)  # At least 1 pixel per tile

        map_pixel_w = int(tilemap.cols * scale)
        map_pixel_h = int(tilemap.rows * scale)
        map_size = (map_pixel_w, map_pixel_h)

        # ── STATIC LAYER: Base tiles (cached, drawn once per area) ──
        if self._cached_tile_surface is None or self._cached_scale != scale or self._cached_map_size != map_size:
            # Pre-render all tiles to a cached surface
            self._cached_tile_surface = pygame.Surface((map_pixel_w + 4, map_pixel_h + 4), pygame.SRCALPHA)
            self._cached_tile_surface.fill((0, 0, 0, MINIMAP_BG_ALPHA))

            for row in range(tilemap.rows):
                for col in range(tilemap.cols):
                    tile_val = tilemap.data[row][col]
                    color = TILE_COLORS.get(tile_val, (60, 60, 60))
                    px = int(col * scale) + 2
                    py = int(row * scale) + 2
                    if scale >= 2:
                        pygame.draw.rect(self._cached_tile_surface, color, (px, py, int(scale), int(scale)))
                    else:
                        self._cached_tile_surface.set_at((px, py), (*color, 255))

            self._cached_scale = scale
            self._cached_map_size = map_size

        # ── FOG OF WAR LAYER: Cached, updated only when new tiles revealed ──
        if self._cached_fog_surface is None:
            self._cached_fog_surface = pygame.Surface((map_pixel_w + 4, map_pixel_h + 4), pygame.SRCALPHA)
            self._cached_fog_surface.fill((0, 0, 0, 0))  # Transparent base

            # Draw fog over unvisited tiles
            for row in range(tilemap.rows):
                for col in range(tilemap.cols):
                    if (col, row) not in visited:
                        px = int(col * scale) + 2
                        py = int(row * scale) + 2
                        if scale >= 2:
                            pygame.draw.rect(self._cached_fog_surface, MINIMAP_FOG_COLOR,
                                           (px, py, int(scale), int(scale)))
                        else:
                            self._cached_fog_surface.set_at((px, py), (*MINIMAP_FOG_COLOR, 255))

        # ── COMPOSITE: Combine static layers ──
        minimap_surf = self._cached_tile_surface.copy()
        minimap_surf.blit(self._cached_fog_surface, (0, 0))

        # ── DYNAMIC LAYER: Entities (drawn every frame) ──

        # Draw chests (yellow dots, only if visited and not opened)
        for chest in chests:
            if chest.opened:
                continue
            cx = int(chest.center_x / TILE_SIZE)
            cy = int(chest.center_y / TILE_SIZE)
            if (cx, cy) in visited:
                px = int(cx * scale) + 2
                py = int(cy * scale) + 2
                dot_size = max(2, int(scale))
                pygame.draw.rect(minimap_surf, (255, 215, 0, 255),
                                 (px, py, dot_size, dot_size))

        # Draw NPCs (blue dots)
        for npc in npcs:
            nx = int(npc.center_x / TILE_SIZE)
            ny = int(npc.center_y / TILE_SIZE)
            if (nx, ny) in visited:
                px = int(nx * scale) + 2
                py = int(ny * scale) + 2
                dot_size = max(2, int(scale))
                pygame.draw.rect(minimap_surf, (60, 140, 255, 255),
                                 (px, py, dot_size, dot_size))

        # Draw enemies (red dots)
        for enemy in enemies:
            if not enemy.alive:
                continue
            ex = int(enemy.center_x / TILE_SIZE)
            ey = int(enemy.center_y / TILE_SIZE)
            if (ex, ey) in visited:
                px = int(ex * scale) + 2
                py = int(ey * scale) + 2
                dot_size = max(1, int(scale) - 1)
                pygame.draw.rect(minimap_surf, (220, 40, 40, 255),
                                 (px, py, dot_size, dot_size))

        # Draw player (white blinking dot)
        if self._player_visible:
            player_col = int(player.center_x / TILE_SIZE)
            player_row = int(player.center_y / TILE_SIZE)
            px = int(player_col * scale) + 2
            py = int(player_row * scale) + 2
            dot_size = max(2, int(scale) + 1)
            pygame.draw.rect(minimap_surf, (255, 255, 255, 255),
                             (px, py, dot_size, dot_size))

        # Draw border
        pygame.draw.rect(minimap_surf, MINIMAP_BORDER_COLOR,
                         (0, 0, map_pixel_w + 4, map_pixel_h + 4), 1)

        # Position in top-right corner, below HUD
        dest_x = SCREEN_WIDTH - map_pixel_w - 4 - MINIMAP_MARGIN
        dest_y = 44  # Below the HUD bar (HUD_HEIGHT = 40 + small gap)
        surface.blit(minimap_surf, (dest_x, dest_y))

    def get_save_data(self):
        """Return visited tiles data for saving."""
        result = {}
        for area_id, tiles in self.visited_tiles.items():
            result[area_id] = list(tiles)
        return result

    def load_save_data(self, data):
        """Load visited tiles from save data."""
        if data is None:
            return
        self.visited_tiles = {}
        for area_id, tile_list in data.items():
            self.visited_tiles[area_id] = set(tuple(t) for t in tile_list)
