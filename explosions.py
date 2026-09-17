import pygame
import random
import math


# =========================
# EXPLOSION MANAGER
# =========================

class ExplosionManager:

    def __init__(self):

        self.explosions = []


    # =========================
    # CREATE EXPLOSION
    # =========================

    def create(self, x, y, size=1):

        particles = []

        particle_count = int(
            18 * size
        )

        for _ in range(particle_count):

            angle = random.uniform(
                0,
                math.pi * 2
            )

            speed = random.uniform(
                2,
                6 * size
            )

            particles.append({

                "x": x,
                "y": y,

                "dx":
                    math.cos(angle) * speed,

                "dy":
                    math.sin(angle) * speed,

                "size":
                    random.randint(2, 5),

                "life":
                    random.randint(20, 35)
            })

        self.explosions.append({

            "x": x,
            "y": y,

            "radius": 5,

            "max_radius":
                35 * size,

            "life": 30,

            "particles":
                particles
        })


    # =========================
    # UPDATE EXPLOSIONS
    # =========================

    def update(self):

        for explosion in self.explosions[:]:

            explosion["life"] -= 1

            explosion["radius"] += (
                explosion["max_radius"] / 30
            )

            for particle in explosion[
                "particles"
            ]:

                particle["x"] += (
                    particle["dx"]
                )

                particle["y"] += (
                    particle["dy"]
                )

                particle["dx"] *= 0.97

                particle["dy"] *= 0.97

                particle["life"] -= 1

            if explosion["life"] <= 0:

                self.explosions.remove(
                    explosion
                )


    # =========================
    # DRAW EXPLOSIONS
    # =========================

    def draw(self, screen):

        for explosion in self.explosions:

            x = int(
                explosion["x"]
            )

            y = int(
                explosion["y"]
            )

            radius = int(
                explosion["radius"]
            )

            # Outer explosion
            pygame.draw.circle(
                screen,
                (255, 150, 40),
                (x, y),
                radius,
                3
            )

            # Inner explosion
            pygame.draw.circle(
                screen,
                (255, 230, 40),
                (x, y),
                max(
                    2,
                    radius // 2
                )
            )

            # Particles
            for particle in explosion[
                "particles"
            ]:

                if particle["life"] > 0:

                    pygame.draw.circle(
                        screen,
                        (255, 230, 40),
                        (
                            int(
                                particle["x"]
                            ),
                            int(
                                particle["y"]
                            )
                        ),
                        max(
                            1,
                            particle["size"]
                        )
                    )


    # =========================
    # CLEAR EXPLOSIONS
    # =========================

    def clear(self):

        self.explosions.clear()