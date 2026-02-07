"""New Game+ difficulty scaling and utility functions."""

import pygame
from zelda_miloutte.sprites.effects import tint_surface

# Maximum NG+ cycle (cap at 5 to prevent absurdity)
NG_PLUS_MAX = 5

# Scaling factors per NG+ cycle (multiplicative)
ENEMY_HP_SCALE = 1.5       # +50% HP per cycle
ENEMY_ATTACK_SCALE = 1.3   # +30% attack per cycle
ENEMY_SPEED_SCALE = 1.15   # +15% speed per cycle

# Boss gets same scaling as enemies
BOSS_HP_SCALE = ENEMY_HP_SCALE
BOSS_ATTACK_SCALE = ENEMY_ATTACK_SCALE
BOSS_SPEED_SCALE = ENEMY_SPEED_SCALE

# NG+ tint color for enemies (red/purple)
NG_PLUS_TINT = (200, 80, 120)

# Elite enemy extra multiplier on top of NG+ scaling
ELITE_HP_MULT = 1.5
ELITE_ATTACK_MULT = 1.3
ELITE_XP_MULT = 2.0


def get_effective_ng_plus(ng_plus_count):
    """Return the effective NG+ count capped at the maximum."""
    return min(ng_plus_count, NG_PLUS_MAX)


def scale_enemy_stats(base_hp, base_attack, base_speed, ng_plus_count):
    """Scale enemy stats based on NG+ cycle count.

    Args:
        base_hp: Base enemy HP
        base_attack: Base enemy attack/damage
        base_speed: Base enemy speed
        ng_plus_count: Current NG+ cycle (0 = normal, 1 = NG+1, etc.)

    Returns:
        Tuple of (scaled_hp, scaled_attack, scaled_speed)
    """
    if ng_plus_count <= 0:
        return base_hp, base_attack, base_speed

    n = get_effective_ng_plus(ng_plus_count)
    scaled_hp = int(base_hp * (ENEMY_HP_SCALE ** n))
    scaled_attack = int(max(1, base_attack * (ENEMY_ATTACK_SCALE ** n)))
    scaled_speed = base_speed * (ENEMY_SPEED_SCALE ** n)
    return scaled_hp, scaled_attack, scaled_speed


def scale_boss_stats(base_hp, base_attack, base_speed, ng_plus_count):
    """Scale boss stats based on NG+ cycle count.

    Same as enemy scaling but bosses also get faster attack cooldowns.

    Args:
        base_hp: Base boss HP
        base_attack: Base boss attack/damage
        base_speed: Base boss speed
        ng_plus_count: Current NG+ cycle (0 = normal, 1 = NG+1, etc.)

    Returns:
        Tuple of (scaled_hp, scaled_attack, scaled_speed)
    """
    if ng_plus_count <= 0:
        return base_hp, base_attack, base_speed

    n = get_effective_ng_plus(ng_plus_count)
    scaled_hp = int(base_hp * (BOSS_HP_SCALE ** n))
    scaled_attack = int(max(1, base_attack * (BOSS_ATTACK_SCALE ** n)))
    scaled_speed = base_speed * (BOSS_SPEED_SCALE ** n)
    return scaled_hp, scaled_attack, scaled_speed


def get_boss_cooldown_scale(ng_plus_count):
    """Return a multiplier for boss attack cooldowns in NG+.

    Lower values = faster attacks. Capped at 0.5x cooldown.

    Returns:
        Float multiplier (1.0 = normal, 0.5 = 2x as fast)
    """
    if ng_plus_count <= 0:
        return 1.0
    n = get_effective_ng_plus(ng_plus_count)
    # Reduce cooldown by 10% per cycle, minimum 0.5
    return max(0.5, 1.0 - n * 0.1)


def should_have_phase3(ng_plus_count):
    """Return True if bosses should have a Phase 3 in this NG+ cycle."""
    return ng_plus_count >= 1


def get_phase3_threshold():
    """Return the HP ratio threshold for boss Phase 3."""
    return 0.25


def should_spawn_elite(ng_plus_count):
    """Return True if elite enemy variants should spawn."""
    return ng_plus_count >= 1


def get_elite_stats(base_hp, base_attack, base_speed, ng_plus_count):
    """Scale stats for an elite enemy variant (NG+ only).

    Elite enemies get NG+ scaling PLUS an extra multiplier.

    Returns:
        Tuple of (scaled_hp, scaled_attack, scaled_speed)
    """
    hp, attack, speed = scale_enemy_stats(base_hp, base_attack, base_speed, ng_plus_count)
    return int(hp * ELITE_HP_MULT), int(max(1, attack * ELITE_ATTACK_MULT)), speed


def tint_sprite_ng_plus(surface, ng_plus_count):
    """Apply a red/purple tint to a sprite surface for NG+ enemies.

    Returns the original surface if ng_plus_count <= 0.
    """
    if ng_plus_count <= 0:
        return surface
    return tint_surface(surface, NG_PLUS_TINT)


def tint_frames_ng_plus(frames_dict, ng_plus_count):
    """Tint all animation frames in a direction -> frame list dict.

    Args:
        frames_dict: Dict of {direction: [frame_surfaces]}
        ng_plus_count: Current NG+ cycle

    Returns:
        New dict with tinted frames, or original if ng_plus_count <= 0
    """
    if ng_plus_count <= 0:
        return frames_dict
    tinted = {}
    for direction, frame_list in frames_dict.items():
        tinted[direction] = [tint_sprite_ng_plus(f, ng_plus_count) for f in frame_list]
    return tinted


def get_ng_plus_label(ng_plus_count):
    """Return a display label like 'NG+1', 'NG+2', etc. or empty string."""
    if ng_plus_count <= 0:
        return ""
    return f"NG+{ng_plus_count}"


def init_ng_plus_save_data(save_data, player):
    """Create save data for a New Game+ cycle.

    Player keeps: level, stats (max_hp, attack, defense), XP, unlocked abilities
    Player loses: keys, quest progress, map exploration, chest states
    World resets: all bosses, chests, enemies, quests

    Args:
        save_data: Current save data dict
        player: Current Player entity

    Returns:
        New save data dict for the NG+ cycle
    """
    old_ng_count = save_data.get("ng_plus_count", 0)
    new_ng_count = old_ng_count + 1

    # Preserve player stats but reset consumables
    ng_data = {
        "ng_plus_count": new_ng_count,
        "player": {
            "hp": player.max_hp,   # Full heal
            "max_hp": player.max_hp,
            "keys": 0,            # Reset keys
            "level": player.level,
            "xp": player.xp,
            "xp_to_next": player.xp_to_next,
            "base_attack": player.base_attack,
            "base_defense": player.base_defense,
        },
        "unlocked_abilities": list(getattr(player, 'unlocked_abilities', [])),
        # Reset world state
        "world_state": {
            "defeated_bosses": [],
            "opened_chests": [],
            "current_area": "overworld",
            "story_progress": 0,
        },
        # Quest state will be reset when quests are re-initialized
        "current_area": "overworld",
        # Speedrun timer
        "play_time": save_data.get("play_time", 0.0),
        "total_play_time": save_data.get("total_play_time", 0.0)
                          + save_data.get("play_time", 0.0),
    }

    # NG+1 exclusive reward: Hero's Crown
    if new_ng_count >= 1:
        ng_data["has_heros_crown"] = True

    return ng_data


def format_play_time(seconds):
    """Format play time in seconds to HH:MM:SS string."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def check_speedrun_achievement(play_time):
    """Check if the speedrun achievement (under 30 minutes) is earned."""
    return play_time < 30 * 60  # 30 minutes in seconds
