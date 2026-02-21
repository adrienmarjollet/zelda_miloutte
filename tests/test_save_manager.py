"""Tests for the SaveManager."""

import json
import pytest
from pathlib import Path
from zelda_miloutte.save_manager import SaveManager, SAVE_VERSION


@pytest.fixture
def save_mgr(tmp_path):
    """Create a SaveManager that uses a temporary directory."""
    sm = SaveManager()
    sm.save_dir = tmp_path
    return sm


class TestSaveAndLoad:
    def test_save_and_load(self, save_mgr):
        data = {"player": {"hp": 6, "level": 3}, "current_area": "forest"}
        save_mgr.save_game(1, data)
        loaded = save_mgr.load_game(1)
        assert loaded is not None
        assert loaded["player"]["hp"] == 6
        assert loaded["player"]["level"] == 3
        assert loaded["current_area"] == "forest"

    def test_save_adds_metadata(self, save_mgr):
        save_mgr.save_game(1, {"player": {"hp": 6}})
        loaded = save_mgr.load_game(1)
        assert loaded["version"] == SAVE_VERSION
        assert "timestamp" in loaded
        assert loaded["slot"] == 1

    def test_load_empty_slot(self, save_mgr):
        assert save_mgr.load_game(1) is None

    def test_load_corrupt_file(self, save_mgr):
        path = save_mgr._slot_path(1)
        path.write_text("not json{{{")
        assert save_mgr.load_game(1) is None

    def test_overwrite_slot(self, save_mgr):
        save_mgr.save_game(1, {"player": {"hp": 6}})
        save_mgr.save_game(1, {"player": {"hp": 2}})
        loaded = save_mgr.load_game(1)
        assert loaded["player"]["hp"] == 2

    def test_multiple_slots(self, save_mgr):
        save_mgr.save_game(1, {"player": {"level": 1}})
        save_mgr.save_game(2, {"player": {"level": 5}})
        save_mgr.save_game(3, {"player": {"level": 10}})
        assert save_mgr.load_game(1)["player"]["level"] == 1
        assert save_mgr.load_game(2)["player"]["level"] == 5
        assert save_mgr.load_game(3)["player"]["level"] == 10


class TestDeleteSave:
    def test_delete_existing(self, save_mgr):
        save_mgr.save_game(1, {"player": {}})
        save_mgr.delete_save(1)
        assert save_mgr.load_game(1) is None

    def test_delete_nonexistent(self, save_mgr):
        save_mgr.delete_save(1)  # Should not raise


class TestListSaves:
    def test_all_empty(self, save_mgr):
        saves = save_mgr.list_saves()
        assert saves[1] is None
        assert saves[2] is None
        assert saves[3] is None

    def test_with_saves(self, save_mgr):
        save_mgr.save_game(1, {
            "player": {"level": 5},
            "current_area": "desert",
            "ng_plus_count": 1,
            "play_time": 1200.0,
        })
        saves = save_mgr.list_saves()
        assert saves[1] is not None
        assert saves[1]["level"] == 5
        assert saves[1]["area"] == "desert"
        assert saves[1]["ng_plus_count"] == 1
        assert saves[1]["play_time"] == 1200.0
        assert saves[2] is None

    def test_slot_path(self, save_mgr):
        path = save_mgr._slot_path(1)
        assert path.name == "save_slot_1.json"
