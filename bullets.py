import pygame


# =========================
# BULLET MANAGER
# =========================

class BulletManager:

    def __init__(
        self,
        bullet_width=6,
        bullet_height=18,
        bullet_speed=16
    ):

        self.bullets = []

        self.width = bullet_width
        self.height = bullet_height
        self.speed = bullet_speed


    # =========================
    # CREATE BULLET
    # =========================

    def shoot(self, player_x, player_width, player_y):

        bullet = {
            "x":
                player_x +
                player_width // 2 -
                self.width // 2,

            "y":
                player_y
        }

        self.bullets.append(bullet)


    # =========================
    # UPDATE BULLETS
    # =========================

    def update(self):

        for bullet in self.bullets[:]:

            bullet["y"] -= self.speed

            # Remove bullet when it
            # leaves the screen

            if bullet["y"] < 0:

                self.bullets.remove(
                    bullet
                )


    # =========================
    # DRAW BULLETS
    # =========================

    def draw(self, screen):

        for bullet in self.bullets:

            pygame.draw.rect(

                screen,

                (255, 230, 40),

                (
                    bullet["x"],
                    bullet["y"],
                    self.width,
                    self.height
                )
            )


    # =========================
    # GET BULLET RECTANGLE
    # =========================

    def get_rect(self, bullet):

        return pygame.Rect(

            bullet["x"],
            bullet["y"],
            self.width,
            self.height
        )


    # =========================
    # REMOVE BULLET
    # =========================

    def remove(self, bullet):

        if bullet in self.bullets:

            self.bullets.remove(
                bullet
            )


    # =========================
    # CLEAR BULLETS
    # =========================

    def clear(self):

        self.bullets.clear()