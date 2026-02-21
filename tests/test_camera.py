"""Tests for the Camera system."""

import math
import pytest
from zelda_miloutte.camera import Camera
from zelda_miloutte.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class MockTarget:
    def __init__(self, x, y, w=28, h=28):
        self.x = x
        self.y = y
        self.width = w
        self.height = h


class TestCameraFollow:
    def test_center_on_target(self):
        cam = Camera(2000, 2000)
        target = MockTarget(500, 400)
        cam.follow(target)
        expected_x = target.x + target.width / 2 - SCREEN_WIDTH / 2
        expected_y = target.y + target.height / 2 - SCREEN_HEIGHT / 2
        assert cam.true_x == pytest.approx(expected_x)
        assert cam.true_y == pytest.approx(expected_y)

    def test_clamp_to_left(self):
        cam = Camera(2000, 2000)
        target = MockTarget(0, 500)
        cam.follow(target)
        assert cam.true_x == 0  # Can't go negative

    def test_clamp_to_top(self):
        cam = Camera(2000, 2000)
        target = MockTarget(500, 0)
        cam.follow(target)
        assert cam.true_y == 0

    def test_clamp_to_right(self):
        cam = Camera(2000, 2000)
        target = MockTarget(1990, 500)
        cam.follow(target)
        assert cam.true_x == 2000 - SCREEN_WIDTH

    def test_clamp_to_bottom(self):
        cam = Camera(2000, 2000)
        target = MockTarget(500, 1990)
        cam.follow(target)
        assert cam.true_y == 2000 - SCREEN_HEIGHT

    def test_small_map_centered(self):
        """When map is smaller than screen, camera centers the map."""
        cam = Camera(400, 300)  # Smaller than SCREEN_WIDTH x SCREEN_HEIGHT
        target = MockTarget(200, 150)
        cam.follow(target)
        assert cam.true_x == (400 - SCREEN_WIDTH) / 2
        assert cam.true_y == (300 - SCREEN_HEIGHT) / 2


class TestSetPosition:
    def test_set_position(self):
        cam = Camera(2000, 2000)
        cam.set_position(100, 200)
        assert cam.true_x == 100
        assert cam.true_y == 200
        assert cam.x == 100  # No shake active
        assert cam.y == 200


class TestScreenShake:
    def test_shake_starts(self):
        cam = Camera(2000, 2000)
        cam.shake(8, 0.5)
        assert cam.shake_timer == 0.5
        assert cam.shake_intensity == 8

    def test_shake_decays(self):
        cam = Camera(2000, 2000)
        cam.shake(8, 0.5)
        cam.update_shake(0.25)
        # Timer should decrease
        assert cam.shake_timer == pytest.approx(0.25)
        # Offsets should be within decayed intensity
        decay = 0.25 / 0.5
        max_offset = 8 * decay
        assert abs(cam.shake_offset_x) <= max_offset + 0.01
        assert abs(cam.shake_offset_y) <= max_offset + 0.01

    def test_shake_ends(self):
        cam = Camera(2000, 2000)
        cam.shake(8, 0.5)
        cam.update_shake(1.0)  # Past duration
        assert cam.shake_timer == 0
        assert cam.shake_offset_x == 0.0
        assert cam.shake_offset_y == 0.0

    def test_no_shake_no_offset(self):
        cam = Camera(2000, 2000)
        cam.update_shake(0.016)
        assert cam.shake_offset_x == 0.0
        assert cam.shake_offset_y == 0.0

    def test_shake_affects_position(self):
        cam = Camera(2000, 2000)
        cam.set_position(100, 100)
        cam.shake(10, 0.5)
        cam.update_shake(0.1)
        cam.set_position(100, 100)  # Re-apply to get shaken position
        # x/y should differ from true_x/true_y by shake offset
        assert cam.x == cam.true_x + cam.shake_offset_x
        assert cam.y == cam.true_y + cam.shake_offset_y


class TestZoom:
    def test_initial_zoom(self):
        cam = Camera(2000, 2000)
        assert cam.zoom == 1.0

    def test_start_zoom(self):
        cam = Camera(2000, 2000)
        cam.start_zoom(1.5, speed=2.0)
        cam.update_zoom(0.1)
        assert cam.zoom > 1.0
        assert cam.zoom < 1.5

    def test_zoom_reaches_target(self):
        cam = Camera(2000, 2000)
        cam.start_zoom(1.3, speed=10.0)
        # Run enough time to reach target
        for _ in range(100):
            cam.update_zoom(0.1)
        assert cam.zoom == pytest.approx(1.3)

    def test_zoom_out(self):
        cam = Camera(2000, 2000)
        cam.zoom = 1.5
        cam.start_zoom(1.0, speed=2.0)
        cam.update_zoom(0.1)
        assert cam.zoom < 1.5


class TestCameraPunch:
    def test_punch_starts(self):
        cam = Camera(2000, 2000)
        cam.punch(intensity=0.05, duration=0.2)
        assert cam._punch_timer == 0.2

    def test_punch_affects_zoom(self):
        cam = Camera(2000, 2000)
        cam.punch(intensity=0.1, duration=0.4)
        cam.update_zoom(0.1)
        # During punch, zoom should be above 1.0
        assert cam.zoom > 1.0

    def test_punch_ends(self):
        cam = Camera(2000, 2000)
        cam.punch(intensity=0.05, duration=0.2)
        cam.update_zoom(0.5)  # Past duration
        assert cam._punch_timer == 0.0
