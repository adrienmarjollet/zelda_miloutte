import pygame
from zelda_miloutte.settings import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from zelda_miloutte.world.tile import TileType
from zelda_miloutte.sprites.tile_sprites import get_tile_surface


class TileMap:
    def __init__(self, map_data):
        self.data = map_data
        self.rows = len(map_data)
        self.cols = len(map_data[0]) if self.rows > 0 else 0
        self.pixel_width = self.cols * TILE_SIZE
        self.pixel_height = self.rows * TILE_SIZE

        # Pre-build tile type grid
        self.tiles = []
        for row in map_data:
            tile_row = []
            for val in row:
                tile_row.append(TileType(val))
            self.tiles.append(tile_row)

        # Pre-build tile surfaces (keyed by tile value)
        self._tile_surfaces = {}
        for row in map_data:
            for val in row:
                if val not in self._tile_surfaces:
                    self._tile_surfaces[val] = get_tile_surface(val)

    def get_tile(self, col, row):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.tiles[row][col]
        return TileType.WALL  # Out of bounds is solid

    def get_tile_at(self, px, py):
        col = int(px) // TILE_SIZE
        row = int(py) // TILE_SIZE
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.tiles[row][col]
        return None

    def is_solid(self, col, row):
        return self.get_tile(col, row).solid

    def resolve_collision_x(self, entity):
        rect = entity.rect
        # Check tiles the entity overlaps
        left_col = rect.left // TILE_SIZE
        right_col = rect.right // TILE_SIZE
        top_row = rect.top // TILE_SIZE
        bottom_row = rect.bottom // TILE_SIZE

        for row in range(top_row, bottom_row + 1):
            for col in range(left_col, right_col + 1):
                if self.is_solid(col, row):
                    tile_rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE,
                                            TILE_SIZE, TILE_SIZE)
                    if rect.colliderect(tile_rect):
                        if entity.vx > 0:
                            entity.x = tile_rect.left - entity.width
                        elif entity.vx < 0:
                            entity.x = tile_rect.right
                        rect = entity.rect  # Refresh

    def resolve_collision_y(self, entity):
        rect = entity.rect
        left_col = rect.left // TILE_SIZE
        right_col = rect.right // TILE_SIZE
        top_row = rect.top // TILE_SIZE
        bottom_row = rect.bottom // TILE_SIZE

        for row in range(top_row, bottom_row + 1):
            for col in range(left_col, right_col + 1):
                if self.is_solid(col, row):
                    tile_rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE,
                                            TILE_SIZE, TILE_SIZE)
                    if rect.colliderect(tile_rect):
                        if entity.vy > 0:
                            entity.y = tile_rect.top - entity.height
                        elif entity.vy < 0:
                            entity.y = tile_rect.bottom
                        rect = entity.rect

    def draw(self, surface, camera):
        # Only draw visible tiles
        start_col = max(0, int(camera.x) // TILE_SIZE)
        end_col = min(self.cols, (int(camera.x) + SCREEN_WIDTH) // TILE_SIZE + 2)
        start_row = max(0, int(camera.y) // TILE_SIZE)
        end_row = min(self.rows, (int(camera.y) + SCREEN_HEIGHT) // TILE_SIZE + 2)

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                val = self.data[row][col]
                x = col * TILE_SIZE - int(camera.x)
                y = row * TILE_SIZE - int(camera.y)
                surface.blit(self._tile_surfaces[val], (x, y))
