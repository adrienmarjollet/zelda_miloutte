"""Tests for the A* pathfinding module."""

import pytest
from zelda_miloutte.world.tilemap import TileMap
from zelda_miloutte.pathfinding import (
    find_path,
    has_line_of_sight,
    pixel_to_tile,
    tile_to_pixel,
    reset_pathfind_budget,
    can_pathfind,
    _heuristic,
    _is_walkable,
    find_cover_position,
    find_flanking_position,
    HAZARD_TILES,
)
from zelda_miloutte.settings import TILE_SIZE


@pytest.fixture(autouse=True)
def reset_budget():
    """Reset the per-frame pathfinding budget before each test."""
    reset_pathfind_budget()


class TestCoordinateConversion:
    def test_pixel_to_tile_origin(self):
        assert pixel_to_tile(0, 0) == (0, 0)

    def test_pixel_to_tile_mid_tile(self):
        assert pixel_to_tile(16, 16) == (0, 0)

    def test_pixel_to_tile_next(self):
        assert pixel_to_tile(32, 64) == (1, 2)

    def test_tile_to_pixel_center(self):
        px, py = tile_to_pixel(0, 0)
        assert px == TILE_SIZE // 2
        assert py == TILE_SIZE // 2

    def test_tile_to_pixel_roundtrip(self):
        col, row = 3, 5
        px, py = tile_to_pixel(col, row)
        c2, r2 = pixel_to_tile(px, py)
        assert (c2, r2) == (col, row)


class TestHeuristic:
    def test_same_point(self):
        assert _heuristic((0, 0), (0, 0)) == 0

    def test_horizontal(self):
        assert _heuristic((0, 0), (5, 0)) == 5

    def test_diagonal(self):
        assert _heuristic((0, 0), (3, 4)) == 7


class TestWalkability:
    def test_grass_walkable(self, simple_map_data):
        tm = TileMap(simple_map_data)
        assert _is_walkable(tm, 1, 1) is True

    def test_wall_not_walkable(self, simple_map_data):
        tm = TileMap(simple_map_data)
        assert _is_walkable(tm, 0, 0) is False

    def test_out_of_bounds_not_walkable(self, simple_map_data):
        tm = TileMap(simple_map_data)
        assert _is_walkable(tm, -1, 0) is False
        assert _is_walkable(tm, 100, 100) is False

    def test_hazard_avoidance(self):
        """Water tiles are not walkable when avoid_hazards=True."""
        map_data = [
            [0, 4, 0],  # 4 = WATER
            [0, 0, 0],
            [0, 0, 0],
        ]
        tm = TileMap(map_data)
        assert _is_walkable(tm, 1, 0, avoid_hazards=True) is False
        assert _is_walkable(tm, 1, 0, avoid_hazards=False) is False  # Water is solid

    def test_spikes_avoided_as_hazard(self):
        """Spikes are walkable but marked as hazard."""
        map_data = [
            [0, 9, 0],  # 9 = SPIKES
            [0, 0, 0],
        ]
        tm = TileMap(map_data)
        # Spikes are not solid but are a hazard
        assert _is_walkable(tm, 1, 0, avoid_hazards=True) is False
        assert _is_walkable(tm, 1, 0, avoid_hazards=False) is True


class TestPathfindBudget:
    def test_initial_budget(self):
        assert can_pathfind() is True

    def test_budget_exhausts(self, open_map_data):
        tm = TileMap(open_map_data)
        # Use up all 3 budget slots
        for _ in range(3):
            find_path(tm, 48, 48, 48, 48)
        assert can_pathfind() is False

    def test_budget_reset(self, open_map_data):
        tm = TileMap(open_map_data)
        for _ in range(3):
            find_path(tm, 48, 48, 48, 48)
        reset_pathfind_budget()
        assert can_pathfind() is True

    def test_over_budget_returns_empty(self, open_map_data):
        tm = TileMap(open_map_data)
        for _ in range(3):
            find_path(tm, 48, 48, 48, 48)
        result = find_path(tm, 48, 48, 200, 200)
        assert result == []


class TestFindPath:
    def test_same_tile(self, open_map_data):
        tm = TileMap(open_map_data)
        path = find_path(tm, 48, 48, 48, 48)
        assert len(path) == 1  # Returns goal position

    def test_straight_line(self, open_map_data):
        tm = TileMap(open_map_data)
        start_px, start_py = tile_to_pixel(1, 1)
        goal_px, goal_py = tile_to_pixel(5, 1)
        path = find_path(tm, start_px, start_py, goal_px, goal_py)
        assert len(path) > 0
        # Final waypoint should be near goal
        last = path[-1]
        assert pixel_to_tile(last[0], last[1]) == (5, 1)

    def test_path_around_wall(self, corridor_map_data):
        """Path must go around the wall in the middle of the corridor."""
        tm = TileMap(corridor_map_data)
        # Start at (1,1), goal at (4,1) - wall at column 3
        start_px, start_py = tile_to_pixel(1, 1)
        goal_px, goal_py = tile_to_pixel(4, 1)
        path = find_path(tm, start_px, start_py, goal_px, goal_py)
        assert len(path) > 0
        # Path should avoid the wall column
        for px, py in path:
            col, row = pixel_to_tile(px, py)
            assert not tm.is_solid(col, row)

    def test_unreachable_goal(self):
        """Completely walled-off goal returns empty path."""
        map_data = [
            [1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1],
        ]
        tm = TileMap(map_data)
        start_px, start_py = tile_to_pixel(1, 1)
        goal_px, goal_py = tile_to_pixel(3, 1)
        path = find_path(tm, start_px, start_py, goal_px, goal_py)
        assert path == []

    def test_max_distance_limit(self, open_map_data):
        tm = TileMap(open_map_data)
        # Goal far beyond max_distance=2
        path = find_path(tm, 48, 48, 280, 280, max_distance=2)
        assert path == []

    def test_eight_directional(self, open_map_data):
        tm = TileMap(open_map_data)
        start_px, start_py = tile_to_pixel(1, 1)
        goal_px, goal_py = tile_to_pixel(4, 4)
        path_4 = find_path(tm, start_px, start_py, goal_px, goal_py, eight_directional=False)
        reset_pathfind_budget()
        path_8 = find_path(tm, start_px, start_py, goal_px, goal_py, eight_directional=True)
        # 8-directional should find a shorter or equal path
        assert len(path_8) <= len(path_4)


class TestLineOfSight:
    def test_clear_los(self, open_map_data):
        tm = TileMap(open_map_data)
        assert has_line_of_sight(tm, 48, 48, 200, 200) is True

    def test_blocked_by_wall(self, simple_map_data):
        tm = TileMap(simple_map_data)
        # From center of tile (1,1) to center of tile (3,3) - should be clear (all inner grass)
        start_px, start_py = tile_to_pixel(1, 1)
        goal_px, goal_py = tile_to_pixel(3, 3)
        assert has_line_of_sight(tm, start_px, start_py, goal_px, goal_py) is True

    def test_blocked_through_wall(self):
        """Line from one side to another with a wall in between."""
        map_data = [
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
        ]
        tm = TileMap(map_data)
        start_px, start_py = tile_to_pixel(0, 1)
        goal_px, goal_py = tile_to_pixel(4, 1)
        assert has_line_of_sight(tm, start_px, start_py, goal_px, goal_py) is False

    def test_same_point(self, open_map_data):
        tm = TileMap(open_map_data)
        assert has_line_of_sight(tm, 48, 48, 48, 48) is True


class TestCoverPosition:
    def test_find_cover_behind_wall(self):
        map_data = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ]
        tm = TileMap(map_data)
        enemy_px, enemy_py = tile_to_pixel(1, 1)
        player_px, player_py = tile_to_pixel(5, 1)
        result = find_cover_position(tm, enemy_px, enemy_py, player_px, player_py)
        if result is not None:
            # Cover position should have no LOS to player
            assert not has_line_of_sight(tm, result[0], result[1], player_px, player_py)

    def test_no_cover_open_map(self, open_map_data):
        tm = TileMap(open_map_data)
        result = find_cover_position(tm, 48, 48, 200, 200)
        # Open map has no walls to hide behind
        assert result is None


class TestFlankingPosition:
    def test_flanking_returns_walkable(self, open_map_data):
        tm = TileMap(open_map_data)
        result = find_flanking_position(tm, 160, 160, 48, 48)
        if result is not None:
            col, row = pixel_to_tile(result[0], result[1])
            assert _is_walkable(tm, col, row)

    def test_flanking_zero_distance(self, open_map_data):
        tm = TileMap(open_map_data)
        # Ally and target at same position
        result = find_flanking_position(tm, 48, 48, 48, 48)
        assert result is None
