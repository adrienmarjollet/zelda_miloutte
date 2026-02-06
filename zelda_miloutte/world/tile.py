from enum import Enum
from zelda_miloutte.settings import (
    GREEN, DARK_GREEN, GRAY, DARK_GRAY, BROWN, BLUE, FLOOR_COLOR,
    LIGHT_BROWN, BOSS_PURPLE, WATER_BLUE, ICE_BLUE, FOREST_GREEN,
    SAND_TAN, LAVA_ORANGE,
)


class TileType(Enum):
    GRASS = 0
    WALL = 1
    TREE = 2
    ROCK = 3
    WATER = 4
    FLOOR = 5
    DOOR = 6
    DUNGEON_ENTRANCE = 7
    BOSS_DOOR = 8
    SPIKES = 9
    PIT = 10
    DUNGEON_ENTRANCE_2 = 11
    TRANSITION_N = 12
    TRANSITION_S = 13
    TRANSITION_E = 14
    TRANSITION_W = 15
    FOREST_FLOOR = 16
    SAND = 17
    LAVA = 18

    @property
    def solid(self):
        return self in (TileType.WALL, TileType.TREE, TileType.ROCK, TileType.WATER, TileType.PIT)

    @property
    def color(self):
        return {
            TileType.GRASS: GREEN,
            TileType.WALL: GRAY,
            TileType.TREE: DARK_GREEN,
            TileType.ROCK: DARK_GRAY,
            TileType.WATER: WATER_BLUE,
            TileType.FLOOR: FLOOR_COLOR,
            TileType.DOOR: LIGHT_BROWN,
            TileType.DUNGEON_ENTRANCE: BROWN,
            TileType.BOSS_DOOR: BOSS_PURPLE,
            TileType.SPIKES: DARK_GRAY,
            TileType.PIT: (0, 0, 0),
            TileType.DUNGEON_ENTRANCE_2: ICE_BLUE,
            TileType.TRANSITION_N: GREEN,
            TileType.TRANSITION_S: GREEN,
            TileType.TRANSITION_E: GREEN,
            TileType.TRANSITION_W: GREEN,
            TileType.FOREST_FLOOR: FOREST_GREEN,
            TileType.SAND: SAND_TAN,
            TileType.LAVA: LAVA_ORANGE,
        }[self]
