"""Persistent user settings stored in ~/.zelda_miloutte/settings.json."""

import json
from pathlib import Path


_DEFAULT_SETTINGS = {
    "music_volume": 50,      # 0-100
    "sfx_volume": 50,        # 0-100
    "screen_scale": 1,       # 1, 2, or 3
    "fullscreen": False,
}

_settings_dir = Path.home() / ".zelda_miloutte"
_settings_path = _settings_dir / "settings.json"
_cached = None


def load_settings():
    """Load settings from disk, returning a dict with defaults filled in."""
    global _cached
    if _cached is not None:
        return _cached
    settings = dict(_DEFAULT_SETTINGS)
    try:
        if _settings_path.exists():
            data = json.loads(_settings_path.read_text())
            for key in _DEFAULT_SETTINGS:
                if key in data:
                    settings[key] = data[key]
    except (json.JSONDecodeError, OSError):
        pass
    _cached = settings
    return settings


def save_settings(settings=None):
    """Save settings dict to disk."""
    global _cached
    if settings is None:
        settings = _cached or _DEFAULT_SETTINGS
    _cached = settings
    try:
        _settings_dir.mkdir(parents=True, exist_ok=True)
        _settings_path.write_text(json.dumps(settings, indent=2))
    except OSError:
        pass


def get_setting(key):
    """Get a single setting value."""
    return load_settings().get(key, _DEFAULT_SETTINGS.get(key))


def set_setting(key, value):
    """Set a single setting value and save."""
    settings = load_settings()
    settings[key] = value
    save_settings(settings)
