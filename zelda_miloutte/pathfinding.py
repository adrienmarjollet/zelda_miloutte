"""A* pathfinding on the tile grid for enemy AI."""

import heapq
import math
from .settings import TILE_SIZE
from .world.tile import TileType


# Tiles that enemies should avoid (hazards they are aware of)
HAZARD_TILES = {TileType.WATER, TileType.LAVA, TileType.SPIKES, TileType.PIT}

# Maximum number of pathfinding calls allowed per frame across all enemies
MAX_PATHFINDS_PER_FRAME = 3

# Global frame counter for limiting pathfinding calls
_pathfind_calls_this_frame = 0


def reset_pathfind_budget():
    """Call once per frame to reset the pathfinding budget."""
    global _pathfind_calls_this_frame
    _pathfind_calls_this_frame = 0


def can_pathfind():
    """Check if the per-frame pathfinding budget has remaining calls."""
    return _pathfind_calls_this_frame < MAX_PATHFINDS_PER_FRAME


def _consume_pathfind():
    """Consume one pathfinding call from the budget."""
    global _pathfind_calls_this_frame
    _pathfind_calls_this_frame += 1


def pixel_to_tile(px, py):
    """Convert pixel coordinates to tile coordinates."""
    return int(px) // TILE_SIZE, int(py) // TILE_SIZE


def tile_to_pixel(col, row):
    """Convert tile coordinates to pixel center of that tile."""
    return col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2


def _is_walkable(tilemap, col, row, avoid_hazards=True):
    """Check if a tile is walkable for an enemy."""
    if col < 0 or row < 0 or row >= tilemap.rows or col >= tilemap.cols:
        return False
    tile = tilemap.get_tile(col, row)
    if tile.solid:
        return False
    if avoid_hazards and tile in HAZARD_TILES:
        return False
    return True


def _heuristic(a, b):
    """Manhattan distance heuristic for 4-directional movement."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# 4-directional neighbors
_DIRS_4 = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# 8-directional neighbors (4 cardinal + 4 diagonal)
_DIRS_8 = [(0, -1), (0, 1), (-1, 0), (1, 0),
           (-1, -1), (-1, 1), (1, -1), (1, 1)]


def find_path(tilemap, start_px, start_py, goal_px, goal_py,
              max_distance=20, avoid_hazards=True, eight_directional=False):
    """Find a path from start to goal using A* on the tile grid.

    Args:
        tilemap: TileMap instance
        start_px, start_py: Start position in pixels
        goal_px, goal_py: Goal position in pixels
        max_distance: Maximum search distance in tiles (to prevent expensive searches)
        avoid_hazards: If True, avoid water, lava, spikes
        eight_directional: If True, allow diagonal movement

    Returns:
        List of (px, py) waypoints in pixels (tile centers), or empty list if no path found.
        The first waypoint is the next tile to move to (not the start tile).
    """
    if not can_pathfind():
        return []

    _consume_pathfind()

    start = pixel_to_tile(start_px, start_py)
    goal = pixel_to_tile(goal_px, goal_py)

    # If start and goal are the same tile, no path needed
    if start == goal:
        return [tile_to_pixel(goal[0], goal[1])]

    # If goal is not walkable, try to find nearest walkable tile to goal
    if not _is_walkable(tilemap, goal[0], goal[1], avoid_hazards):
        goal = _find_nearest_walkable(tilemap, goal, avoid_hazards)
        if goal is None:
            return []

    # Quick distance check
    if _heuristic(start, goal) > max_distance * 2:
        return []

    dirs = _DIRS_8 if eight_directional else _DIRS_4

    # A* search
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: _heuristic(start, goal)}

    visited = set()
    max_nodes = max_distance * max_distance * 4  # Limit search space

    while open_set:
        if len(visited) >= max_nodes:
            break

        _, current = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            # Reconstruct path
            path = []
            node = current
            while node in came_from:
                path.append(tile_to_pixel(node[0], node[1]))
                node = came_from[node]
            path.reverse()
            return path

        for dx, dy in dirs:
            neighbor = (current[0] + dx, current[1] + dy)

            if neighbor in visited:
                continue

            if not _is_walkable(tilemap, neighbor[0], neighbor[1], avoid_hazards):
                continue

            # For diagonal movement, ensure both cardinal tiles are walkable
            # to prevent cutting through wall corners
            if eight_directional and dx != 0 and dy != 0:
                if (not _is_walkable(tilemap, current[0] + dx, current[1], avoid_hazards) or
                        not _is_walkable(tilemap, current[0], current[1] + dy, avoid_hazards)):
                    continue

            # Cost: 1 for cardinal, ~1.414 for diagonal
            move_cost = 1.414 if (dx != 0 and dy != 0) else 1.0
            tentative_g = g_score[current] + move_cost

            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + _heuristic(neighbor, goal)
                f_score[neighbor] = f
                heapq.heappush(open_set, (f, neighbor))

    return []  # No path found


def _find_nearest_walkable(tilemap, goal, avoid_hazards, search_radius=3):
    """Find the nearest walkable tile to the given goal tile."""
    for r in range(1, search_radius + 1):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                if abs(dx) != r and abs(dy) != r:
                    continue  # Only check the ring at distance r
                nx, ny = goal[0] + dx, goal[1] + dy
                if _is_walkable(tilemap, nx, ny, avoid_hazards):
                    return (nx, ny)
    return None


def has_line_of_sight(tilemap, x1, y1, x2, y2):
    """Check line of sight between two pixel positions using Bresenham-like raycast on tiles.

    Returns True if no solid tiles block the line between (x1,y1) and (x2,y2).
    """
    col1, row1 = pixel_to_tile(x1, y1)
    col2, row2 = pixel_to_tile(x2, y2)

    # Bresenham's line algorithm on tile grid
    dcol = abs(col2 - col1)
    drow = abs(row2 - row1)
    col, row = col1, row1
    step_col = 1 if col2 > col1 else -1
    step_row = 1 if row2 > row1 else -1

    # Handle the case where start == end
    if dcol == 0 and drow == 0:
        return True

    if dcol >= drow:
        err = dcol // 2
        for _ in range(dcol):
            col += step_col
            err -= drow
            if err < 0:
                row += step_row
                err += dcol
            # Check if this tile is solid (blocks LOS)
            if tilemap.is_solid(col, row):
                return False
    else:
        err = drow // 2
        for _ in range(drow):
            row += step_row
            err -= dcol
            if err < 0:
                col += step_col
                err += drow
            # Check if this tile is solid (blocks LOS)
            if tilemap.is_solid(col, row):
                return False

    return True


def find_cover_position(tilemap, enemy_x, enemy_y, player_x, player_y,
                        search_radius=6):
    """Find a tile that provides cover from the player (a wall between enemy and player).

    Used by archers to find positions behind walls relative to the player.
    Returns (px, py) pixel position or None.
    """
    enemy_col, enemy_row = pixel_to_tile(enemy_x, enemy_y)
    best_pos = None
    best_score = float('inf')

    for dx in range(-search_radius, search_radius + 1):
        for dy in range(-search_radius, search_radius + 1):
            cx, cy = enemy_col + dx, enemy_row + dy
            if not _is_walkable(tilemap, cx, cy, avoid_hazards=True):
                continue
            px_pos, py_pos = tile_to_pixel(cx, cy)
            # Check if this position has no LOS to player (behind cover)
            if not has_line_of_sight(tilemap, px_pos, py_pos, player_x, player_y):
                # Score by distance from enemy (prefer nearby cover)
                dist = abs(dx) + abs(dy)
                if dist < best_score:
                    best_score = dist
                    best_pos = (px_pos, py_pos)

    return best_pos


def find_flanking_position(tilemap, target_x, target_y, ally_x, ally_y,
                           flank_distance=4):
    """Find a position on the opposite side of the target from an ally.

    Used for group flanking behavior.
    Returns (px, py) pixel position or None.
    """
    # Direction from ally to target
    dx = target_x - ally_x
    dy = target_y - ally_y
    dist = math.sqrt(dx * dx + dy * dy)
    if dist < 1:
        return None

    # Desired position: on the opposite side of the target from the ally
    nx, ny = dx / dist, dy / dist
    flank_px = target_x + nx * flank_distance * TILE_SIZE
    flank_py = target_y + ny * flank_distance * TILE_SIZE

    # Snap to tile and check walkability
    col, row = pixel_to_tile(flank_px, flank_py)
    if _is_walkable(tilemap, col, row, avoid_hazards=True):
        return tile_to_pixel(col, row)

    # Try nearby tiles
    for r in range(1, 3):
        for ddx in range(-r, r + 1):
            for ddy in range(-r, r + 1):
                nc, nr = col + ddx, row + ddy
                if _is_walkable(tilemap, nc, nr, avoid_hazards=True):
                    return tile_to_pixel(nc, nr)

    return None
