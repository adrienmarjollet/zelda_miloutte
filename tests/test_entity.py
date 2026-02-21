"""Tests for the base Entity class."""

import math
import pytest
from zelda_miloutte.entities.entity import Entity


class TestEntityInit:
    def test_position(self):
        e = Entity(10, 20, 32, 32, (255, 0, 0))
        assert e.x == 10.0
        assert e.y == 20.0

    def test_dimensions(self):
        e = Entity(0, 0, 28, 28, (0, 0, 0))
        assert e.width == 28
        assert e.height == 28

    def test_defaults(self):
        e = Entity(0, 0, 10, 10, (0, 0, 0))
        assert e.alive is True
        assert e.facing == "down"
        assert e.vx == 0.0
        assert e.vy == 0.0
        assert e.knockback_timer == 0.0


class TestEntityProperties:
    def test_center(self):
        e = Entity(10, 20, 32, 32, (0, 0, 0))
        assert e.center_x == 26.0  # 10 + 32/2
        assert e.center_y == 36.0  # 20 + 32/2

    def test_rect(self):
        e = Entity(10.5, 20.7, 32, 32, (0, 0, 0))
        r = e.rect
        assert r.x == 10
        assert r.y == 20
        assert r.width == 32
        assert r.height == 32

    def test_is_moving_false(self):
        e = Entity(0, 0, 10, 10, (0, 0, 0))
        assert e.is_moving is False

    def test_is_moving_true(self):
        e = Entity(0, 0, 10, 10, (0, 0, 0))
        e.vx = 50.0
        assert e.is_moving is True


class TestKnockback:
    def test_apply_knockback_direction(self):
        e = Entity(100, 100, 32, 32, (0, 0, 0))
        # Source to the left means knockback pushes right
        e.apply_knockback(50, 116, 200)
        assert e.knockback_vx > 0
        assert e.knockback_timer == e.knockback_duration

    def test_apply_knockback_from_above(self):
        e = Entity(100, 100, 32, 32, (0, 0, 0))
        # Source above means knockback pushes down
        e.apply_knockback(116, 50, 200)
        assert e.knockback_vy > 0

    def test_apply_knockback_zero_distance(self):
        """When source is exactly at entity center, should use default direction."""
        e = Entity(100, 100, 32, 32, (0, 0, 0))
        e.apply_knockback(e.center_x, e.center_y, 200)
        assert e.knockback_vx == 200
        assert e.knockback_vy == 0

    def test_knockback_strength_normalized(self):
        e = Entity(100, 100, 32, 32, (0, 0, 0))
        e.apply_knockback(0, 116, 100)
        magnitude = math.sqrt(e.knockback_vx**2 + e.knockback_vy**2)
        assert abs(magnitude - 100) < 1.0

    def test_update_knockback_decay(self):
        e = Entity(100, 100, 32, 32, (0, 0, 0))
        e.apply_knockback(50, 116, 200)
        initial_vx = e.knockback_vx
        e.update_knockback(0.01)
        # Velocity should decay
        assert abs(e.knockback_vx) < abs(initial_vx)

    def test_update_knockback_expires(self):
        e = Entity(100, 100, 32, 32, (0, 0, 0))
        e.apply_knockback(50, 116, 200)
        # Advance past knockback duration
        e.update_knockback(e.knockback_duration + 0.1)
        assert e.knockback_vx == 0
        assert e.knockback_vy == 0
        assert e.knockback_timer == 0


class TestCollision:
    def test_collides_overlapping(self):
        a = Entity(0, 0, 32, 32, (0, 0, 0))
        b = Entity(16, 16, 32, 32, (0, 0, 0))
        assert a.collides_with(b) is True

    def test_no_collision_far_apart(self):
        a = Entity(0, 0, 32, 32, (0, 0, 0))
        b = Entity(100, 100, 32, 32, (0, 0, 0))
        assert a.collides_with(b) is False

    def test_dead_entity_no_collision(self):
        a = Entity(0, 0, 32, 32, (0, 0, 0))
        b = Entity(0, 0, 32, 32, (0, 0, 0))
        b.alive = False
        assert a.collides_with(b) is False

    def test_collision_symmetric(self):
        a = Entity(0, 0, 32, 32, (0, 0, 0))
        b = Entity(16, 16, 32, 32, (0, 0, 0))
        assert a.collides_with(b) == b.collides_with(a)
