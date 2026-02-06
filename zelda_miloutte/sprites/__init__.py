"""Animated sprite system for pixel art entities."""

import pygame


class AnimatedSprite:
    """Holds directional animation frames and cycles walk frames.

    Usage:
        anim = AnimatedSprite(frames, frame_duration=0.15)
        anim.update(dt, moving=True)
        surface.blit(anim.get_frame("down"), dest)

    Args:
        frames: dict mapping direction ("up","down","left","right")
                to a list of pygame.Surface (at least 1 frame each).
        frame_duration: seconds between frame changes while moving.
    """

    def __init__(self, frames, frame_duration=0.15):
        self.frames = frames  # {"down": [surf0, surf1], ...}
        self.frame_duration = frame_duration
        self._timer = 0.0
        self._index = 0

    def update(self, dt, moving):
        """Advance animation timer.  Resets to frame 0 when not moving."""
        if moving:
            self._timer += dt
            if self._timer >= self.frame_duration:
                self._timer -= self.frame_duration
                # Cycle through available frames for any direction
                max_frames = max(len(f) for f in self.frames.values())
                self._index = (self._index + 1) % max_frames
        else:
            self._timer = 0.0
            self._index = 0

    def get_frame(self, facing):
        """Return the current surface for the given direction."""
        dir_frames = self.frames.get(facing, self.frames.get("down"))
        idx = self._index % len(dir_frames)
        return dir_frames[idx]
