import pygame
import random


# =========================
# ENEMY MANAGER
# =========================

class EnemyManager:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.enemies = []

        # Bullets fired by shooter enemies

        self.projectiles = []

        self.projectile_speed = 7

    # =========================
    # CREATE ENEMY
    # =========================

    def spawn(self, difficulty=1):

        enemy_type = random.choice([
            "normal",
            "fast",
            "large",
            "shooter"
        ])

        # -------------------------
        # NORMAL ENEMY
        # -------------------------

        if enemy_type == "normal":

            width = 40
            height = 40

            enemy = {
                "type": "normal",

                "x": random.randint(
                    0,
                    self.width - width
                ),

                "y": -height,

                "width": width,
                "height": height,

                "speed":
                    4 + (difficulty - 1) * 0.2,

                "hp": 1,

                "points": 10
            }

        # -------------------------
        # FAST ENEMY
        # -------------------------

        elif enemy_type == "fast":

            width = 32
            height = 32

            enemy = {
                "type": "fast",

                "x": random.randint(
                    0,
                    self.width - width
                ),

                "y": -height,

                "width": width,
                "height": height,

                "speed":
                    7 + (difficulty - 1) * 0.2,

                "hp": 1,

                "points": 20
            }

        # -------------------------
        # LARGE ENEMY
        # -------------------------

        elif enemy_type == "large":

            width = 60
            height = 60

            enemy = {
                "type": "large",

                "x": random.randint(
                    0,
                    self.width - width
                ),

                "y": -height,

                "width": width,
                "height": height,

                "speed":
                    3 + (difficulty - 1) * 0.2,

                "hp": 2,

                "points": 30
            }

        # -------------------------
        # SHOOTER ENEMY
        # -------------------------

        else:

            width = 48
            height = 48

            enemy = {
                "type": "shooter",

                "x": random.randint(
                    0,
                    self.width - width
                ),

                "y": -height,

                "width": width,
                "height": height,

                "speed":
                    3.5 + (difficulty - 1) * 0.2,

                "hp": 2,

                "points": 40,

                # Individual shooting timer

                "shoot_timer": random.randint(
                    60,
                    120
                ),

                "shoot_delay": 120
            }

        self.enemies.append(enemy)

    # =========================
    # UPDATE ENEMIES
    # =========================

    def update(self, player_x=None, player_y=None):

        for enemy in self.enemies[:]:

            enemy["y"] += enemy["speed"]

            # -------------------------
            # SHOOTER ENEMY ATTACK
            # -------------------------

            if enemy["type"] == "shooter":

                enemy["shoot_timer"] -= 1

                if enemy["shoot_timer"] <= 0:

                    self.shoot(
                        enemy,
                        player_x,
                        player_y
                    )

                    enemy["shoot_timer"] = (
                        enemy["shoot_delay"]
                    )

            # Remove enemy if it
            # leaves the screen

            if enemy["y"] > self.height:

                self.enemies.remove(
                    enemy
                )

        # =========================
        # UPDATE SHOOTER PROJECTILES
        # =========================

        for projectile in self.projectiles[:]:

            projectile["y"] += (
                self.projectile_speed
            )

            if projectile["y"] > self.height:

                self.projectiles.remove(
                    projectile
                )

    # =========================
    # SHOOTER ATTACK
    # =========================

    def shoot(
        self,
        enemy,
        player_x=None,
        player_y=None
    ):

        projectile = {

            "x":
                enemy["x"]
                + enemy["width"] // 2,

            "y":
                enemy["y"]
                + enemy["height"],

            "width": 10,

            "height": 20
        }

        self.projectiles.append(
            projectile
        )

    # =========================
    # DRAW ENEMIES
    # =========================

    def draw(self, screen):

        for enemy in self.enemies:

            x = int(enemy["x"])
            y = int(enemy["y"])

            width = enemy["width"]
            height = enemy["height"]

            # -------------------------
            # NORMAL ENEMY
            # -------------------------

            if enemy["type"] == "normal":

                pygame.draw.rect(
                    screen,
                    (255, 60, 60),
                    (
                        x,
                        y,
                        width,
                        height
                    )
                )

                # Eyes

                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    (
                        x + 10,
                        y + 12
                    ),
                    5
                )

                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    (
                        x + width - 10,
                        y + 12
                    ),
                    5
                )

                pygame.draw.circle(
                    screen,
                    (0, 0, 0),
                    (
                        x + 10,
                        y + 12
                    ),
                    2
                )

                pygame.draw.circle(
                    screen,
                    (0, 0, 0),
                    (
                        x + width - 10,
                        y + 12
                    ),
                    2
                )

            # -------------------------
            # FAST ENEMY
            # -------------------------

            elif enemy["type"] == "fast":

                pygame.draw.polygon(
                    screen,
                    (180, 70, 255),
                    [
                        (x + width // 2, y),
                        (x + width, y + height),
                        (x, y + height)
                    ]
                )

                pygame.draw.circle(
                    screen,
                    (255, 230, 40),
                    (
                        x + width // 2,
                        y + height // 2
                    ),
                    5
                )

            # -------------------------
            # LARGE ENEMY
            # -------------------------

            elif enemy["type"] == "large":

                pygame.draw.rect(
                    screen,
                    (255, 150, 40),
                    (
                        x,
                        y,
                        width,
                        height
                    ),
                    border_radius=8
                )

                pygame.draw.rect(
                    screen,
                    (180, 70, 255),
                    (
                        x + 10,
                        y + 10,
                        width - 20,
                        height - 20
                    ),
                    border_radius=6
                )

                pygame.draw.circle(
                    screen,
                    (255, 230, 40),
                    (
                        x + width // 2,
                        y + height // 2
                    ),
                    8
                )

                if enemy["hp"] == 2:

                    pygame.draw.rect(
                        screen,
                        (60, 255, 100),
                        (
                            x,
                            y - 6,
                            width,
                            4
                        )
                    )

            # -------------------------
            # SHOOTER ENEMY
            # -------------------------

            elif enemy["type"] == "shooter":

                # Outer body

                pygame.draw.rect(
                    screen,
                    (60, 220, 180),
                    (
                        x,
                        y,
                        width,
                        height
                    ),
                    border_radius=10
                )

                # Inner body

                pygame.draw.rect(
                    screen,
                    (20, 70, 80),
                    (
                        x + 7,
                        y + 7,
                        width - 14,
                        height - 14
                    ),
                    border_radius=7
                )

                # Central cannon

                pygame.draw.rect(
                    screen,
                    (255, 230, 40),
                    (
                        x + width // 2 - 6,
                        y + height - 2,
                        12,
                        18
                    ),
                    border_radius=4
                )

                # Core

                pygame.draw.circle(
                    screen,
                    (255, 60, 60),
                    (
                        x + width // 2,
                        y + height // 2
                    ),
                    8
                )

        # =========================
        # DRAW SHOOTER PROJECTILES
        # =========================

        for projectile in self.projectiles:

            projectile_x = int(
                projectile["x"]
            )

            projectile_y = int(
                projectile["y"]
            )

            pygame.draw.rect(
                screen,
                (255, 60, 60),
                (
                    projectile_x
                    - projectile["width"] // 2,
                    projectile_y,
                    projectile["width"],
                    projectile["height"]
                ),
                border_radius=5
            )

            pygame.draw.circle(
                screen,
                (255, 150, 40),
                (
                    projectile_x,
                    projectile_y
                ),
                4
            )

    # =========================
    # GET ENEMY RECTANGLE
    # =========================

    def get_rect(self, enemy):

        return pygame.Rect(
            int(enemy["x"]),
            int(enemy["y"]),
            enemy["width"],
            enemy["height"]
        )

    # =========================
    # DAMAGE ENEMY
    # =========================

    def damage(self, enemy):

        enemy["hp"] -= 1

        if enemy["hp"] <= 0:

            points = enemy["points"]

            if enemy in self.enemies:

                self.enemies.remove(
                    enemy
                )

            return points

        return 0

    # =========================
    # CLEAR ENEMIES
    # =========================

    def clear(self):

        self.enemies.clear()

        self.projectiles.clear()
