"""Tests for the TimeSystem (day/night cycle)."""

import pytest
from zelda_miloutte.time_system import (
    TimeSystem,
    PHASE_DAWN,
    PHASE_DAY,
    PHASE_DUSK,
    PHASE_NIGHT,
    DAWN_START,
    DAY_START,
    DUSK_START,
    NIGHT_START,
    HOURS_IN_DAY,
    LIGHT_RADIUS_DEFAULT,
    LIGHT_RADIUS_LANTERN,
)


class TestTimePhases:
    def test_default_is_day(self):
        ts = TimeSystem()  # Default 8:00
        assert ts.phase == PHASE_DAY

    def test_dawn(self):
        ts = TimeSystem(game_hour=6.0)
        assert ts.phase == PHASE_DAWN

    def test_day(self):
        ts = TimeSystem(game_hour=12.0)
        assert ts.phase == PHASE_DAY

    def test_dusk(self):
        ts = TimeSystem(game_hour=19.0)
        assert ts.phase == PHASE_DUSK

    def test_night_after_20(self):
        ts = TimeSystem(game_hour=22.0)
        assert ts.phase == PHASE_NIGHT

    def test_night_before_dawn(self):
        ts = TimeSystem(game_hour=3.0)
        assert ts.phase == PHASE_NIGHT

    def test_is_night(self):
        ts = TimeSystem(game_hour=22.0)
        assert ts.is_night is True

    def test_is_not_night(self):
        ts = TimeSystem(game_hour=12.0)
        assert ts.is_night is False


class TestTimeUpdate:
    def test_advance_time(self):
        ts = TimeSystem(game_hour=8.0)
        ts.update(60.0)  # 60 seconds = 1 game hour
        assert ts.game_hour == pytest.approx(9.0)

    def test_wrap_around(self):
        ts = TimeSystem(game_hour=23.5)
        ts.update(60.0)  # Advance 1 hour past midnight
        assert ts.game_hour == pytest.approx(0.5)

    def test_paused_no_advance(self):
        ts = TimeSystem(game_hour=8.0)
        ts.paused = True
        ts.update(60.0)
        assert ts.game_hour == pytest.approx(8.0)

    def test_small_dt(self):
        ts = TimeSystem(game_hour=8.0)
        ts.update(1.0)  # 1 second = 1/60 hour
        assert ts.game_hour == pytest.approx(8.0 + 1.0 / 60.0)


class TestSkipToDawn:
    def test_skip_to_dawn(self):
        ts = TimeSystem(game_hour=22.0)
        ts.skip_to_dawn()
        assert ts.game_hour == DAWN_START


class TestTimeString:
    def test_format(self):
        ts = TimeSystem(game_hour=14.5)  # 14:30
        assert ts.time_string == "14:30"

    def test_format_midnight(self):
        ts = TimeSystem(game_hour=0.0)
        assert ts.time_string == "00:00"

    def test_hour_int(self):
        ts = TimeSystem(game_hour=14.5)
        assert ts.hour_int == 14

    def test_minute_int(self):
        ts = TimeSystem(game_hour=14.5)
        assert ts.minute_int == 30


class TestLightRadius:
    def test_no_light_during_day(self):
        ts = TimeSystem(game_hour=12.0)
        assert ts.get_light_radius(False) == 0
        assert ts.get_light_radius(True) == 0

    def test_default_radius_at_night(self):
        ts = TimeSystem(game_hour=22.0)
        assert ts.get_light_radius(False) == LIGHT_RADIUS_DEFAULT

    def test_lantern_radius_at_night(self):
        ts = TimeSystem(game_hour=22.0)
        assert ts.get_light_radius(True) == LIGHT_RADIUS_LANTERN


class TestColorInterpolation:
    def test_lerp_color_start(self):
        c = TimeSystem._lerp_color((0, 0, 0, 0), (255, 255, 255, 255), 0.0)
        assert c == (0, 0, 0, 0)

    def test_lerp_color_end(self):
        c = TimeSystem._lerp_color((0, 0, 0, 0), (255, 255, 255, 255), 1.0)
        assert c == (255, 255, 255, 255)

    def test_lerp_color_mid(self):
        c = TimeSystem._lerp_color((0, 0, 0, 0), (200, 100, 50, 100), 0.5)
        assert c == (100, 50, 25, 50)

    def test_lerp_color_clamps(self):
        c = TimeSystem._lerp_color((0, 0, 0, 0), (255, 255, 255, 255), 2.0)
        assert c == (255, 255, 255, 255)

    def test_lerp_color_clamps_negative(self):
        c = TimeSystem._lerp_color((100, 100, 100, 100), (200, 200, 200, 200), -1.0)
        assert c == (100, 100, 100, 100)


class TestTimeSerialization:
    def test_roundtrip(self):
        ts = TimeSystem(game_hour=14.5)
        data = ts.to_dict()
        ts2 = TimeSystem()
        ts2.from_dict(data)
        assert ts2.game_hour == pytest.approx(14.5)

    def test_from_dict_wraps(self):
        ts = TimeSystem()
        ts.from_dict({"game_hour": 25.0})
        assert ts.game_hour == pytest.approx(1.0)

    def test_from_dict_default(self):
        ts = TimeSystem()
        ts.from_dict({})
        assert ts.game_hour == pytest.approx(8.0)
