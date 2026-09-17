import pygame


# =========================
# PLAYER / SPACESHIP
# =========================

class Player:

    def __init__(self, width, height):

        self.screen_width = width
        self.screen_height = height

        # Player size

        self.width = 60
        self.height = 60

        # Starting position

        self.x = (
            self.screen_width // 2
            - self.width // 2
        )

        self.y = (
            self.screen_height
            - self.height
            - 30
        )

        # Movement speed

        self.speed = 8

        # Smooth hand movement

        self.hand_smoothing = 0.20

        # Shield state

        self.shield_active = False

    # =========================
    # MOVE WITH HAND
    # =========================

    def move_with_hand(self, hand_x):

        HAND_LEFT = 0.15
        HAND_RIGHT = 0.85

        # Keep hand position
        # inside calibrated range

        hand_x = max(
            HAND_LEFT,
            min(
                HAND_RIGHT,
                hand_x
            )
        )

        # Convert hand position
        # into screen position

        normalized_x = (
            hand_x - HAND_LEFT
        ) / (
            HAND_RIGHT - HAND_LEFT
        )

        target_x = (
            normalized_x
            * (
                self.screen_width
                - self.width
            )
        )

        # Smooth movement

        self.x += (
            target_x - self.x
        ) * self.hand_smoothing

        self.keep_inside_screen()

    # =========================
    # MOVE WITH KEYBOARD
    # =========================

    def move_keyboard(self, keys):

        if keys[pygame.K_LEFT]:

            self.x -= self.speed

        if keys[pygame.K_RIGHT]:

            self.x += self.speed

        self.keep_inside_screen()

    # =========================
    # KEEP PLAYER ON SCREEN
    # =========================

    def keep_inside_screen(self):

        if self.x < 0:

            self.x = 0

        if self.x > (
            self.screen_width
            - self.width
        ):

            self.x = (
                self.screen_width
                - self.width
            )

    # =========================
    # GET PLAYER RECTANGLE
    # =========================

    def get_rect(self):

        return pygame.Rect(

            int(self.x),

            int(self.y),

            self.width,

            self.height
        )

    # =========================
    # DRAW SPACESHIP
    # =========================

    def draw(self, screen):

        x = int(self.x)
        y = int(self.y)

        # =========================
        # SHIELD
        # =========================

        if self.shield_active:

            pygame.draw.circle(

                screen,

                (60, 240, 255),

                (
                    x + self.width // 2,
                    y + self.height // 2
                ),

                42,

                3
            )

            pygame.draw.circle(

                screen,

                (100, 220, 255),

                (
                    x + self.width // 2,
                    y + self.height // 2
                ),

                38,

                1
            )

        # =========================
        # SHIP BODY
        # =========================

        pygame.draw.polygon(

            screen,

            (40, 150, 255),

            [
                (
                    x + self.width // 2,
                    y
                ),

                (
                    x,
                    y + self.height
                ),

                (
                    x + self.width // 2,
                    y + self.height - 15
                ),

                (
                    x + self.width,
                    y + self.height
                )
            ]
        )

        # =========================
        # INNER BODY
        # =========================

        pygame.draw.polygon(

            screen,

            (100, 220, 255),

            [
                (
                    x + self.width // 2,
                    y + 10
                ),

                (
                    x + 15,
                    y + self.height - 10
                ),

                (
                    x + self.width // 2,
                    y + self.height - 20
                ),

                (
                    x + self.width - 15,
                    y + self.height - 10
                )
            ]
        )

        # =========================
        # COCKPIT
        # =========================

        pygame.draw.circle(

            screen,

            (255, 255, 255),

            (
                x + self.width // 2,
                y + 25
            ),

            7
        )

        pygame.draw.circle(

            screen,

            (40, 150, 255),

            (
                x + self.width // 2,
                y + 25
            ),

            4
        )

        # =========================
        # ENGINE GLOW
        # =========================

        pygame.draw.polygon(

            screen,

            (255, 230, 40),

            [
                (
                    x + 22,
                    y + self.height - 5
                ),

                (
                    x + 30,
                    y + self.height + 12
                ),

                (
                    x + 38,
                    y + self.height - 5
                )
            ]
        )

    # =========================
    # SET SHIELD
    # =========================

    def set_shield(self, active):

        self.shield_active = active