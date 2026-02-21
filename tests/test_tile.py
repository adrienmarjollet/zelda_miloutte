"""Tests for TileType enum and TileMap."""

import pytest
from zelda_miloutte.world.tile import TileType
from zelda_miloutte.world.tilemap import TileMap
from zelda_miloutte.entities.entity import Entity
from zelda_miloutte.settings import TILE_SIZE


class TestTileType:
    def test_solid_tiles(self):
        """WALL, TREE, ROCK, WATER, PIT should be solid."""
        solids = [
            TileType.WALL, TileType.TREE, TileType.ROCK,
            TileType.WATER, TileType.PIT, TileType.BARRIER_RED,
            TileType.BARRIER_BLUE, TileType.FROZEN_WALL, TileType.CRACKED_WALL,
        ]
        for tile in solids:
            assert tile.solid is True, f"{tile.name} should be solid"

    def test_non_solid_tiles(self):
        """GRASS, FLOOR, DOOR, SPIKES, ICE, SAND should not be solid."""
        non_solids = [
            TileType.GRASS, TileType.FLOOR, TileType.DOOR,
            TileType.SPIKES, TileType.ICE, TileType.SAND,
            TileType.BRIDGE, TileType.SNOW, TileType.LAVA,
        ]
        for tile in non_solids:
            assert tile.solid is False, f"{tile.name} should not be solid"

    def test_all_tiles_have_color(self):
        """Every tile type should have a color defined."""
        for tile in TileType:
            color = tile.color
            assert isinstance(color, tuple)
            assert len(color) == 3

    def test_tile_value_range(self):
        """Tile values should be sequential from 0 to 29."""
        values = [t.value for t in TileType]
        assert values == list(range(30))


class TestTileMap:
    def test_dimensions(self, simple_map_data):
        tm = TileMap(simple_map_data)
        assert tm.rows == 5
        assert tm.cols == 5
        assert tm.pixel_width == 5 * TILE_SIZE
        assert tm.pixel_height == 5 * TILE_SIZE

    def test_get_tile(self, simple_map_data):
        tm = TileMap(simple_map_data)
        assert tm.get_tile(0, 0) == TileType.WALL
        assert tm.get_tile(1, 1) == TileType.GRASS

    def test_get_tile_out_of_bounds(self, simple_map_data):
        tm = TileMap(simple_map_data)
        assert tm.get_tile(-1, 0) == TileType.WALL
        assert tm.get_tile(100, 0) == TileType.WALL

    def test_get_tile_at_pixel(self, simple_map_data):
        tm = TileMap(simple_map_data)
        # Center of tile (1,1)
        tile = tm.get_tile_at(TILE_SIZE + 1, TILE_SIZE + 1)
        assert tile == TileType.GRASS

    def test_get_tile_at_out_of_bounds(self, simple_map_data):
        tm = TileMap(simple_map_data)
        assert tm.get_tile_at(-10, -10) is None

    def test_is_solid(self, simple_map_data):
        tm = TileMap(simple_map_data)
        assert tm.is_solid(0, 0) is True  # WALL
        assert tm.is_solid(2, 2) is False  # GRASS


class TestTileMapCollision:
    def test_resolve_collision_x_right(self, simple_map_data):
        tm = TileMap(simple_map_data)
        e = Entity(3 * TILE_SIZE - 5, TILE_SIZE + 2, 28, 28, (0, 0, 0))
        e.vx = 100  # Moving right toward wall at col 4
        tm.resolve_collision_x(e)
        # Entity should be pushed back so it doesn't overlap the wall
        assert e.x + e.width <= 4 * TILE_SIZE

    def test_resolve_collision_x_left(self, simple_map_data):
        tm = TileMap(simple_map_data)
        e = Entity(TILE_SIZE + 2, TILE_SIZE + 2, 28, 28, (0, 0, 0))
        e.vx = -100  # Moving left toward wall at col 0
        tm.resolve_collision_x(e)
        # Entity should be pushed right so it doesn't overlap the wall
        assert e.x >= TILE_SIZE

    def test_resolve_collision_y_down(self, simple_map_data):
        tm = TileMap(simple_map_data)
        e = Entity(TILE_SIZE + 2, 3 * TILE_SIZE - 5, 28, 28, (0, 0, 0))
        e.vy = 100  # Moving down toward wall at row 4
        tm.resolve_collision_y(e)
        assert e.y + e.height <= 4 * TILE_SIZE

    def test_no_collision_in_open_space(self, simple_map_data):
        tm = TileMap(simple_map_data)
        e = Entity(2 * TILE_SIZE, 2 * TILE_SIZE, 28, 28, (0, 0, 0))
        original_x = e.x
        e.vx = 10
        tm.resolve_collision_x(e)
        assert e.x == original_x  # No change; no wall nearby
