"""
GameEngine: owns the basket and all falling objects.
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT


MAX_MISSES = 5

# Task 3: controlled spawning
MIN_SPAWN_INTERVAL = 30
MAX_SPAWN_INTERVAL = 70
MAX_OBJECTS = 5
MIN_SPAWN_DISTANCE = 80


class GameEngine:
    def __init__(self):
        self.basket = Basket(
            x=WIDTH / 2,
            y=HEIGHT - 30
        )

        self.objects = []

        # Start with an immediate spawn.
        self.frames_until_spawn = 0

        self.score = 0
        self.misses = 0
        self.game_over = False

    def _spawn_object(self):
        """
        Spawn a falling object at a valid horizontal position.

        Task 3 requirements:
        - Keep the object inside the playable area.
        - Avoid spawning too close to existing objects.
        - Limit the number of objects on screen.
        """

        if len(self.objects) >= MAX_OBJECTS:
            return

        radius = 14

        min_x = radius
        max_x = WIDTH - radius

        possible_positions = []

        for x in range(min_x, max_x + 1):
            if all(
                abs(x - obj.x) >= MIN_SPAWN_DISTANCE
                for obj in self.objects
            ):
                possible_positions.append(x)

        if not possible_positions:
            return

        x = random.choice(possible_positions)

        self.objects.append(
            FallingObject(
                x=x,
                y=-radius,
                speed=3
            )
        )

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        if keys_pressed[pygame.K_LEFT]:
            self.basket.x -= self.basket.speed

        if keys_pressed[pygame.K_RIGHT]:
            self.basket.x += self.basket.speed

        # Keep the entire basket inside the screen.
        half_width = self.basket.width / 2

        self.basket.x = max(
            half_width,
            min(WIDTH - half_width, self.basket.x)
        )

    def handle_keydown(self, key):
        """
        Handle keys that are pressed once rather than held.
        """

        # Restart after game over.
        if self.game_over and key == pygame.K_r:
            self.__init__()
            return

        # Task 4: activate temporary speed boost.
        if not self.game_over and key == pygame.K_SPACE:
            self.basket.activate_boost()

    def update(self):
        if self.game_over:
            return

        # Task 4:
        # Update the basket's temporary speed boost timer.
        self.basket.update()

        # -----------------------------------------
        # TASK 3: CONTROLLED SPAWNING
        # -----------------------------------------

        self.frames_until_spawn -= 1

        if self.frames_until_spawn <= 0:
            self._spawn_object()

            self.frames_until_spawn = random.randint(
                MIN_SPAWN_INTERVAL,
                MAX_SPAWN_INTERVAL
            )

        # -----------------------------------------
        # UPDATE FALLING OBJECTS
        # -----------------------------------------

        for obj in self.objects:
            obj.update()

        # -----------------------------------------
        # TASK 1: CATCH DETECTION
        # -----------------------------------------

        basket_rect = self.basket.get_rect()

        # Iterate over a copy so removing caught objects
        # doesn't cause other objects to be skipped.
        for obj in self.objects[:]:
            if is_caught(basket_rect, obj):
                self.score += 1
                self.objects.remove(obj)

        # -----------------------------------------
        # MISSED OBJECTS
        # -----------------------------------------

        missed = [
            obj
            for obj in self.objects
            if obj.is_past_bottom(HEIGHT)
        ]

        if missed:
            self.objects = [
                obj
                for obj in self.objects
                if not obj.is_past_bottom(HEIGHT)
            ]

            self.misses += len(missed)

            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface,
            self.basket,
            self.objects
        )

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10)
        )

        renderer.draw_text(
            surface,
            font,
            f"Misses: {self.misses}/{MAX_MISSES}",
            (10, 36)
        )

        # Task 4: tell the player how to activate the boost.
        renderer.draw_text(
            surface,
            font,
            "SPACE: Speed Boost",
            (10, 62)
        )

        # Task 4: show a clear indicator while boost is active.
        if self.basket.is_boosted:
            renderer.draw_text(
                surface,
                font,
                "BOOST ACTIVE!",
                (WIDTH - 180, 10),
                (255, 220, 80)
            )

        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                f"Game Over! Final score: {self.score}. Press R to restart."
            )