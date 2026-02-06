"""JSON-based save/load system for game persistence."""

import json
import time
from pathlib import Path


SAVE_VERSION = 1


class SaveManager:
    """Manages saving and loading game state to JSON files."""

    def __init__(self):
        self.save_dir = Path.home() / ".zelda_miloutte"
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def _slot_path(self, slot):
        return self.save_dir / f"save_slot_{slot}.json"

    def save_game(self, slot, data):
        """Save game data to a slot.

        Args:
            slot: Integer slot number (1-3)
            data: Dict with player state, world state, quest state
        """
        save_data = {
            "version": SAVE_VERSION,
            "timestamp": time.time(),
            "slot": slot,
            **data,
        }
        path = self._slot_path(slot)
        path.write_text(json.dumps(save_data, indent=2))

    def load_game(self, slot):
        """Load game data from a slot.

        Args:
            slot: Integer slot number (1-3)

        Returns:
            Dict with save data, or None if slot is empty
        """
        path = self._slot_path(slot)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            return None

    def list_saves(self):
        """Return dict of slot -> save info (or None if empty) for slots 1-3."""
        saves = {}
        for slot in range(1, 4):
            data = self.load_game(slot)
            if data:
                saves[slot] = {
                    "timestamp": data.get("timestamp", 0),
                    "level": data.get("player", {}).get("level", 1),
                    "area": data.get("current_area", "overworld"),
                }
            else:
                saves[slot] = None
        return saves

    def delete_save(self, slot):
        """Delete a save slot."""
        path = self._slot_path(slot)
        if path.exists():
            path.unlink()
