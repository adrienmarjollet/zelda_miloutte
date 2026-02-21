"""Tests for the AchievementManager."""

import pytest
from zelda_miloutte.achievements import (
    AchievementManager,
    ALL_BOSS_IDS,
    ALL_AREA_IDS,
    TOTAL_CHESTS,
)


@pytest.fixture
def am():
    return AchievementManager()


class TestUnlock:
    def test_unlock_new(self, am):
        assert am.unlock("first_blood") is True
        assert am.achievements["first_blood"].unlocked is True

    def test_unlock_already_unlocked(self, am):
        am.unlock("first_blood")
        assert am.unlock("first_blood") is False

    def test_unlock_nonexistent(self, am):
        assert am.unlock("nonexistent") is False

    def test_unlock_adds_popup(self, am):
        am.unlock("first_blood")
        assert len(am.pending_popups) == 1
        assert am.pending_popups[0].id == "first_blood"


class TestCounts:
    def test_initial_counts(self, am):
        assert am.get_unlocked_count() == 0
        assert am.get_total_count() == 10

    def test_unlocked_count(self, am):
        am.unlock("first_blood")
        am.unlock("level_10")
        assert am.get_unlocked_count() == 2


class TestEnemyKills:
    def test_first_blood(self, am):
        am.on_enemy_kill()
        assert am.achievements["first_blood"].unlocked is True

    def test_monster_slayer_at_50(self, am):
        for _ in range(49):
            am.on_enemy_kill()
        assert am.achievements["monster_slayer"].unlocked is False
        am.on_enemy_kill()
        assert am.achievements["monster_slayer"].unlocked is True

    def test_kill_counter(self, am):
        for _ in range(10):
            am.on_enemy_kill()
        assert am.total_kills == 10


class TestBossKills:
    def test_boss_hunter_all_bosses(self, am):
        am.on_boss_fight_start()
        for boss_id in ALL_BOSS_IDS:
            am.on_boss_kill(boss_id)
        assert am.achievements["boss_hunter"].unlocked is True

    def test_boss_hunter_partial(self, am):
        am.on_boss_kill("boss_1")
        am.on_boss_kill("boss_2")
        assert am.achievements["boss_hunter"].unlocked is False

    def test_untouchable(self, am):
        am.on_boss_fight_start()
        # No damage taken
        am.on_boss_kill("boss_1")
        assert am.achievements["untouchable"].unlocked is True

    def test_untouchable_failed(self, am):
        am.on_boss_fight_start()
        am.on_player_damaged_in_boss_fight()
        am.on_boss_kill("boss_1")
        assert am.achievements["untouchable"].unlocked is False


class TestExplorer:
    def test_visit_all_areas(self, am):
        for area in ALL_AREA_IDS:
            am.on_area_enter(area)
        assert am.achievements["explorer"].unlocked is True

    def test_visit_partial(self, am):
        am.on_area_enter("overworld")
        assert am.achievements["explorer"].unlocked is False


class TestChests:
    def test_treasure_hunter(self, am):
        for _ in range(TOTAL_CHESTS):
            am.on_chest_open()
        assert am.achievements["treasure_hunter"].unlocked is True


class TestLevelUp:
    def test_level_10(self, am):
        am.on_level_up(9)
        assert am.achievements["level_10"].unlocked is False
        am.on_level_up(10)
        assert am.achievements["level_10"].unlocked is True


class TestGameComplete:
    def test_speed_demon(self, am):
        am.play_time = 25 * 60  # 25 minutes
        am.on_game_complete()
        assert am.achievements["speed_demon"].unlocked is True

    def test_speed_demon_too_slow(self, am):
        am.play_time = 35 * 60  # 35 minutes
        am.on_game_complete()
        assert am.achievements["speed_demon"].unlocked is False

    def test_completionist(self, am):
        # Must have: all bosses, all areas, all chests, game completed
        for boss_id in ALL_BOSS_IDS:
            am.on_boss_kill(boss_id)
        for area in ALL_AREA_IDS:
            am.on_area_enter(area)
        for _ in range(TOTAL_CHESTS):
            am.on_chest_open()
        am.on_game_complete()
        assert am.achievements["completionist"].unlocked is True

    def test_completionist_missing_bosses(self, am):
        for area in ALL_AREA_IDS:
            am.on_area_enter(area)
        for _ in range(TOTAL_CHESTS):
            am.on_chest_open()
        am.on_game_complete()
        assert am.achievements["completionist"].unlocked is False


class TestPlayTime:
    def test_update_play_time(self, am):
        am.update_play_time(1.5)
        am.update_play_time(2.5)
        assert am.play_time == pytest.approx(4.0)


class TestSerialization:
    def test_roundtrip(self, am):
        am.on_enemy_kill()
        am.on_area_enter("overworld")
        am.on_boss_kill("boss_1")
        am.on_chest_open()
        am.update_play_time(100.0)

        data = am.to_dict()

        am2 = AchievementManager()
        am2.from_dict(data)

        assert am2.achievements["first_blood"].unlocked is True
        assert am2.total_kills == 1
        assert "overworld" in am2.visited_areas
        assert "boss_1" in am2.defeated_bosses
        assert am2.total_chests_opened == 1
        assert am2.play_time == pytest.approx(100.0)

    def test_from_dict_none(self, am):
        am.from_dict(None)  # Should not crash
        assert am.total_kills == 0
