# New Game+ Enemy Scaling Fix - Implementation Report

## Summary

Fixed the New Game+ difficulty scaling system. The scaling functions existed in `ng_plus.py` but were never called during enemy/boss spawning. All enemies and bosses now properly scale based on the NG+ cycle count.

## Issues Fixed

### 1. Enemy Scaling Not Applied (PlayState)
**File**: `zelda_miloutte/states/play_state.py`
**Location**: `_spawn_enemies()` method (lines 106-165)

**Problem**: Enemies spawned in overworld areas with base stats only.

**Fix**: Added NG+ scaling after enemy instantiation:
```python
# Apply NG+ scaling if in a New Game+ cycle
if self.game.ng_plus_count > 0:
    scaled_hp, scaled_damage, scaled_speed = scale_enemy_stats(
        e.hp, e.damage, e.speed, self.game.ng_plus_count
    )
    e.hp = scaled_hp
    e.max_hp = scaled_hp
    e.damage = scaled_damage
    e.speed = scaled_speed
    # Scale chase_speed if enemy has it
    if hasattr(e, 'chase_speed'):
        _, _, scaled_chase = scale_enemy_stats(
            e.max_hp, e.damage, e.chase_speed, self.game.ng_plus_count
        )
        e.chase_speed = scaled_chase
```

**Affected enemy types**: Enemy, Archer, ShadowStalker, VineSnapper, Scorpion, Mummy, FireImp, MagmaGolem, IceWraith, FrostGolem

### 2. Enemy Scaling Not Applied (DungeonState)
**File**: `zelda_miloutte/states/dungeon_state.py`
**Location**: Enemy spawning (lines 69-117)

**Problem**: Dungeon enemies spawned with base stats only.

**Fix**: Applied same scaling logic as PlayState to all dungeon enemies.

**Affected enemy types**: Enemy, Archer, VineSnapper, IceWraith, FrostGolem

### 3. Boss Scaling Not Applied
**File**: `zelda_miloutte/states/dungeon_state.py`
**Location**: Boss spawning and initialization (lines 119-195)

**Problem**: Bosses (standard Boss, ForestGuardian, SandWorm, InfernoDrake, and Ice Cavern Crystal Dragon) spawned with base stats.

**Fix**: Added comprehensive boss scaling after instantiation:
- Scaled HP, damage, speed, chase_speed, charge_speed
- Scaled attack cooldowns using `get_boss_cooldown_scale()`
- Handled all boss-specific cooldowns:
  - Standard Boss: `charge_cooldown`
  - ForestGuardian: `root_slam_cooldown`, `vine_summon_cooldown`
  - InfernoDrake: `fire_breath_cooldown`, `meteor_cooldown`
  - SandWorm: inherits standard patterns

### 4. Night + NG+ Interaction Documented
**File**: `zelda_miloutte/states/gameplay_state.py`
**Location**: `_update_night_enemies()` (line 796)

**Documentation**: Added docstring clarifying that night scaling (1.5x) multiplies with NG+ scaling.
- NG+ scaling applied at spawn time
- Night scaling applied at runtime
- Example: NG+2 enemy with base HP=10 → 22 HP (NG+) → 33 HP (night)

## Scaling Formulas

### Enemy Stats
- **HP**: `base_hp * (1.5 ^ ng_plus_count)`
- **Attack**: `base_attack * (1.3 ^ ng_plus_count)`
- **Speed**: `base_speed * (1.15 ^ ng_plus_count)`

### Boss Stats
- Uses same multipliers as enemies (1.5x HP, 1.3x attack, 1.15x speed per cycle)
- **Attack Cooldowns**: `base_cooldown * max(0.5, 1.0 - ng_plus_count * 0.1)`
  - NG+1: 0.9x cooldown (11% faster attacks)
  - NG+2: 0.8x cooldown (25% faster attacks)
  - NG+3: 0.7x cooldown (43% faster attacks)
  - NG+5: 0.5x cooldown (100% faster attacks - capped)

### Cap
All scaling capped at NG+5 to prevent absurd difficulty.

## Expected Difficulty Progression

### NG+1
- Enemies: 50% more HP, 30% more damage, 15% faster
- Bosses: Same as enemies + 10% faster attacks

### NG+2
- Enemies: 125% more HP, 69% more damage, 32% faster
- Bosses: Same as enemies + 20% faster attacks

### NG+3
- Enemies: 238% more HP, 120% more damage, 52% faster
- Bosses: Same as enemies + 30% faster attacks

## Verification

All changes have been:
1. Syntax-checked using `python -m py_compile`
2. Formula-tested using standalone test script
3. Applied consistently across all enemy and boss types
4. Documented for future maintenance

## Files Modified

1. `/Users/adrienmarjollet/Desktop/projects/zelda_miloutte/zelda_miloutte/states/play_state.py`
   - Added enemy scaling in `_spawn_enemies()` method

2. `/Users/adrienmarjollet/Desktop/projects/zelda_miloutte/zelda_miloutte/states/dungeon_state.py`
   - Added enemy scaling in enemy spawn loop
   - Added boss scaling after boss instantiation
   - Added cooldown scaling for all boss types

3. `/Users/adrienmarjollet/Desktop/projects/zelda_miloutte/zelda_miloutte/states/gameplay_state.py`
   - Added documentation for Night + NG+ interaction

## Elite Enemy System

The `should_spawn_elite(ng_plus_count)` function exists and returns `True` for NG+1+, but no Elite enemy class is currently implemented. This is acceptable as:
- The function is not called anywhere
- Regular enemies with scaled stats provide sufficient challenge
- Elite system can be added later if desired

**Recommendation**: If elite enemies are desired, either:
- Create an Elite enemy class with visual distinction (different color, size, particle effects)
- Or use the `get_elite_stats()` function to spawn extra-scaled variants of existing enemies

## Testing Recommendations

To verify the fix works in-game:
1. Start a new game and complete it to unlock NG+
2. Start NG+1 and verify enemies are noticeably tougher
3. Check HUD shows correct boss HP values (scaled)
4. Verify enemies attack more frequently in NG+ (especially bosses)
5. Test at night to confirm multiplicative stacking (enemies should be very difficult)

## Implementation Date
2026-02-07
