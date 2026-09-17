import pygame
import random


# =========================
# STARFIELD
# =========================

class Starfield:

    def __init__(self, width, height, number_of_stars=100):

        self.width = width
        self.height = height

        self.stars = []

        for _ in range(number_of_stars):

            self.stars.append({
                "x": random.randint(
                    0,
                    self.width
                ),

                "y": random.randint(
                    0,
                    self.height
                ),

                "size": random.randint(
                    1,
                    3
                ),

                "speed": random.randint(
                    1,
                    4
                )
            })


    # =========================
    # UPDATE STARS
    # =========================

    def update(self):

        for star in self.stars:

            star["y"] += star["speed"]

            if star["y"] > self.height:

                star["y"] = 0

                star["x"] = random.randint(
                    0,
                    self.width
                )


    # =========================
    # DRAW STARS
    # =========================

    def draw(self, screen):

        for star in self.stars:

            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (
                    star["x"],
                    star["y"]
                ),
                star["size"]
            )