"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Normal and boosted movement speeds.
        self.normal_speed = speed
        self.boost_speed = speed * 2

        self.speed = self.normal_speed

        # Number of frames remaining for the boost.
        self.boosted_frames = 0

        # 3 seconds at approximately 60 FPS.
        self.boost_duration = 180

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            self.width,
            self.height,
        )

    def activate_boost(self):
        """
        Activate or refresh the temporary speed boost.
        """

        self.boosted_frames = self.boost_duration
        self.speed = self.boost_speed

    def update(self):
        """
        Update the temporary boost timer.
        """

        if self.boosted_frames > 0:
            self.boosted_frames -= 1

            # Boost has expired.
            if self.boosted_frames == 0:
                self.speed = self.normal_speed

    @property
    def is_boosted(self):
        """
        Return True while the speed boost is active.
        """

        return self.boosted_frames > 0