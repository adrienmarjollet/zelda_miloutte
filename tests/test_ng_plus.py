"""Tests for the NG+ scaling system."""

import pytest
from zelda_miloutte.ng_plus import (
    get_effective_ng_plus,
    scale_enemy_stats,
    scale_boss_stats,
    get_boss_cooldown_scale,
    should_have_phase3,
    get_phase3_threshold,
    should_spawn_elite,
    get_elite_stats,
    get_ng_plus_label,
    format_play_time,
    check_speedrun_achievement,
    init_ng_plus_save_data,
    NG_PLUS_MAX,
    ENEMY_HP_SCALE,
    ENEMY_ATTACK_SCALE,
    ENEMY_SPEED_SCALE,
    ELITE_HP_MULT,
    ELITE_ATTACK_MULT,
)


class TestEffectiveNgPlus:
    def test_zero(self):
        assert get_effective_ng_plus(0) == 0

    def test_within_cap(self):
        assert get_effective_ng_plus(3) == 3

    def test_at_cap(self):
        assert get_effective_ng_plus(NG_PLUS_MAX) == NG_PLUS_MAX

    def test_above_cap(self):
        assert get_effective_ng_plus(100) == NG_PLUS_MAX


class TestEnemyScaling:
    def test_no_scaling_at_zero(self):
        hp, atk, spd = scale_enemy_stats(10, 2, 50.0, 0)
        assert (hp, atk, spd) == (10, 2, 50.0)

    def test_ng_plus_1(self):
        hp, atk, spd = scale_enemy_stats(10, 2, 50.0, 1)
        assert hp == int(10 * ENEMY_HP_SCALE)
        assert atk == int(2 * ENEMY_ATTACK_SCALE)
        assert spd == pytest.approx(50.0 * ENEMY_SPEED_SCALE)

    def test_ng_plus_2(self):
        hp, atk, spd = scale_enemy_stats(10, 2, 50.0, 2)
        assert hp == int(10 * ENEMY_HP_SCALE ** 2)
        assert atk == int(2 * ENEMY_ATTACK_SCALE ** 2)
        assert spd == pytest.approx(50.0 * ENEMY_SPEED_SCALE ** 2)

    def test_negative_ng_plus(self):
        hp, atk, spd = scale_enemy_stats(10, 2, 50.0, -1)
        assert (hp, atk, spd) == (10, 2, 50.0)

    def test_attack_minimum_1(self):
        # With very low base attack
        _, atk, _ = scale_enemy_stats(10, 0, 50.0, 1)
        assert atk >= 1

    def test_capped_at_max(self):
        hp_5, _, _ = scale_enemy_stats(10, 2, 50.0, NG_PLUS_MAX)
        hp_100, _, _ = scale_enemy_stats(10, 2, 50.0, 100)
        assert hp_5 == hp_100

    def test_monotonic_increase(self):
        prev_hp = 0
        for n in range(6):
            hp, _, _ = scale_enemy_stats(10, 2, 50.0, n)
            assert hp >= prev_hp
            prev_hp = hp


class TestBossScaling:
    def test_no_scaling_at_zero(self):
        hp, atk, spd = scale_boss_stats(100, 5, 80.0, 0)
        assert (hp, atk, spd) == (100, 5, 80.0)

    def test_ng_plus_1(self):
        hp, atk, spd = scale_boss_stats(100, 5, 80.0, 1)
        assert hp == int(100 * ENEMY_HP_SCALE)
        assert atk == int(5 * ENEMY_ATTACK_SCALE)

    def test_cooldown_scale_normal(self):
        assert get_boss_cooldown_scale(0) == 1.0

    def test_cooldown_scale_ng_plus_1(self):
        assert get_boss_cooldown_scale(1) == pytest.approx(0.9)

    def test_cooldown_scale_capped(self):
        assert get_boss_cooldown_scale(NG_PLUS_MAX) == 0.5

    def test_cooldown_scale_above_cap(self):
        assert get_boss_cooldown_scale(100) == 0.5


class TestPhase3:
    def test_no_phase3_at_zero(self):
        assert should_have_phase3(0) is False

    def test_phase3_at_ng_plus_1(self):
        assert should_have_phase3(1) is True

    def test_phase3_threshold(self):
        assert get_phase3_threshold() == 0.25


class TestElites:
    def test_no_elites_at_zero(self):
        assert should_spawn_elite(0) is False

    def test_elites_at_ng_plus_1(self):
        assert should_spawn_elite(1) is True

    def test_elite_stats(self):
        hp, atk, spd = get_elite_stats(10, 2, 50.0, 1)
        base_hp, base_atk, base_spd = scale_enemy_stats(10, 2, 50.0, 1)
        assert hp == int(base_hp * ELITE_HP_MULT)
        assert atk == int(max(1, base_atk * ELITE_ATTACK_MULT))


class TestLabels:
    def test_label_zero(self):
        assert get_ng_plus_label(0) == ""

    def test_label_positive(self):
        assert get_ng_plus_label(1) == "NG+1"
        assert get_ng_plus_label(3) == "NG+3"


class TestFormatPlayTime:
    def test_seconds_only(self):
        assert format_play_time(45) == "00:45"

    def test_minutes_and_seconds(self):
        assert format_play_time(125) == "02:05"

    def test_hours(self):
        assert format_play_time(3661) == "1:01:01"

    def test_zero(self):
        assert format_play_time(0) == "00:00"


class TestSpeedrun:
    def test_under_30_minutes(self):
        assert check_speedrun_achievement(29 * 60) is True

    def test_exactly_30_minutes(self):
        assert check_speedrun_achievement(30 * 60) is False

    def test_over_30_minutes(self):
        assert check_speedrun_achievement(31 * 60) is False


class TestInitNgPlusSaveData:
    def test_basic_save_data(self):
        class MockPlayer:
            max_hp = 10
            level = 5
            xp = 200
            xp_to_next = 400
            base_attack = 3
            base_defense = 2
            unlocked_abilities = ["fireball"]

        save_data = {"ng_plus_count": 0, "play_time": 600.0, "total_play_time": 0.0}
        result = init_ng_plus_save_data(save_data, MockPlayer())

        assert result["ng_plus_count"] == 1
        assert result["player"]["hp"] == 10  # Full heal
        assert result["player"]["keys"] == 0  # Reset
        assert result["player"]["level"] == 5  # Preserved
        assert result["player"]["base_attack"] == 3  # Preserved
        assert result["unlocked_abilities"] == ["fireball"]
        assert result["world_state"]["defeated_bosses"] == []
        assert result["has_heros_crown"] is True
        assert result["total_play_time"] == 600.0

    def test_increment_ng_count(self):
        class MockPlayer:
            max_hp = 6
            level = 1
            xp = 0
            xp_to_next = 100
            base_attack = 0
            base_defense = 0
            unlocked_abilities = []

        save_data = {"ng_plus_count": 2, "play_time": 0.0, "total_play_time": 1000.0}
        result = init_ng_plus_save_data(save_data, MockPlayer())
        assert result["ng_plus_count"] == 3
