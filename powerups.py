import pygame
import random

# =========================
# POWER-UP MANAGER
# =========================

class PowerUpManager:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.powerups = []

        self.speed = 3

    # =========================
    # CREATE POWER-UP
    # =========================

    def spawn(self):

        powerup_type = random.choice([
            "rapid",
            "shield",
            "life"
        ])

        size = 30

        powerup = {

            "type": powerup_type,

            "x": random.randint(
                20,
                self.width - size - 20
            ),

            "y": -size,

            "width": size,
            "height": size,

            "speed": self.speed
        }

        self.powerups.append(powerup)

    # =========================
    # UPDATE POWER-UPS
    # =========================

    def update(self):

        for powerup in self.powerups[:]:

            powerup["y"] += powerup["speed"]

            # Remove if it leaves
            # the bottom of screen

            if powerup["y"] > self.height:

                self.powerups.remove(
                    powerup
                )

    # =========================
    # DRAW POWER-UPS
    # =========================

    def draw(self, screen):

        for powerup in self.powerups:

            x = int(powerup["x"])
            y = int(powerup["y"])

            width = powerup["width"]
            height = powerup["height"]

            # -------------------------
            # RAPID FIRE
            # -------------------------

            if powerup["type"] == "rapid":

                pygame.draw.circle(
                    screen,
                    (60, 255, 100),
                    (
                        x + width // 2,
                        y + height // 2
                    ),
                    width // 2
                )

                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    (
                        x + width // 2,
                        y + height // 2
                    ),
                    width // 2,
                    2
                )

                font = pygame.font.Font(
                    None,
                    20
                )

                text = font.render(
                    "R",
                    True,
                    (0, 0, 0)
                )

                text_rect = text.get_rect(
                    center=(
                        x + width // 2,
                        y + height // 2
                    )
                )

                screen.blit(
                    text,
                    text_rect
                )

            # -------------------------
            # SHIELD
            # -------------------------

            elif powerup["type"] == "shield":

                pygame.draw.circle(
                    screen,
                    (60, 240, 255),
                    (
                        x + width // 2,
                        y + height // 2
                    ),
                    width // 2
                )

                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    (
                        x + width // 2,
                        y + height // 2
                    ),
                    width // 2,
                    2
                )

                font = pygame.font.Font(
                    None,
                    20
                )

                text = font.render(
                    "S",
                    True,
                    (0, 0, 0)
                )

                text_rect = text.get_rect(
                    center=(
                        x + width // 2,
                        y + height // 2
                    )
                )

                screen.blit(
                    text,
                    text_rect
                )

            # -------------------------
            # EXTRA LIFE
            # -------------------------

            elif powerup["type"] == "life":

                pygame.draw.circle(
                    screen,
                    (255, 230, 40),
                    (
                        x + width // 2,
                        y + height // 2
                    ),
                    width // 2
                )

                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    (
                        x + width // 2,
                        y + height // 2
                    ),
                    width // 2,
                    2
                )

                font = pygame.font.Font(
                    None,
                    20
                )

                text = font.render(
                    "+",
                    True,
                    (0, 0, 0)
                )

                text_rect = text.get_rect(
                    center=(
                        x + width // 2,
                        y + height // 2
                    )
                )

                screen.blit(
                    text,
                    text_rect
                )

    # =========================
    # GET POWER-UP RECTANGLE
    # =========================

    def get_rect(self, powerup):

        return pygame.Rect(
            int(powerup["x"]),
            int(powerup["y"]),
            powerup["width"],
            powerup["height"]
        )

    # =========================
    # COLLECT POWER-UP
    # =========================

    def collect(self, powerup):

        powerup_type = powerup["type"]

        if powerup in self.powerups:

            self.powerups.remove(
                powerup
            )

        return powerup_type

    # =========================
    # CLEAR POWER-UPS
    # =========================

    def clear(self):

        self.powerups.clear()