import pygame


# =========================
# MENU MANAGER
# =========================

class MenuManager:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        # -------------------------
        # Fonts
        # -------------------------

        self.title_font = pygame.font.Font(
            None,
            64
        )

        self.large_font = pygame.font.Font(
            None,
            42
        )

        self.medium_font = pygame.font.Font(
            None,
            28
        )

        self.small_font = pygame.font.Font(
            None,
            22
        )

    # =========================
    # DRAW TEXT
    # =========================

    def draw_centered_text(
        self,
        screen,
        text,
        font,
        y,
        color
    ):

        surface = font.render(
            text,
            True,
            color
        )

        rectangle = surface.get_rect(
            center=(
                self.width // 2,
                y
            )
        )

        screen.blit(
            surface,
            rectangle
        )

    # =========================
    # START MENU
    # =========================

    def draw_menu(self, screen):

        screen.fill(
            (0, 0, 0)
        )

        # -------------------------
        # Title
        # -------------------------

        self.draw_centered_text(
            screen,
            "GESTURE SPACE SHOOTER",
            self.title_font,
            120,
            (40, 150, 255)
        )

        # -------------------------
        # Subtitle
        # -------------------------

        self.draw_centered_text(
            screen,
            "Control the spaceship with your hand",
            self.medium_font,
            190,
            (255, 255, 255)
        )

        # -------------------------
        # Controls
        # -------------------------

        self.draw_centered_text(
            screen,
            "Move  :  Move your index finger",
            self.small_font,
            270,
            (150, 150, 150)
        )

        self.draw_centered_text(
            screen,
            "Shoot :  Fold your index finger",
            self.small_font,
            310,
            (150, 150, 150)
        )

        self.draw_centered_text(
            screen,
            "Shield:  Open your palm",
            self.small_font,
            350,
            (150, 150, 150)
        )

        self.draw_centered_text(
            screen,
            "Keyboard: ← →   |   Space",
            self.small_font,
            390,
            (150, 150, 150)
        )

        # -------------------------
        # Start instruction
        # -------------------------

        self.draw_centered_text(
            screen,
            "PRESS ENTER TO START",
            self.large_font,
            490,
            (255, 230, 40)
        )

    # =========================
    # GAME OVER SCREEN
    # =========================

    def draw_game_over(
        self,
        screen,
        score
    ):

        screen.fill(
            (0, 0, 0)
        )

        # -------------------------
        # Game Over
        # -------------------------

        self.draw_centered_text(
            screen,
            "GAME OVER",
            self.title_font,
            150,
            (255, 60, 60)
        )

        # -------------------------
        # Final score
        # -------------------------

        self.draw_centered_text(
            screen,
            f"FINAL SCORE: {score}",
            self.large_font,
            250,
            (255, 255, 255)
        )

        # -------------------------
        # Restart
        # -------------------------

        self.draw_centered_text(
            screen,
            "PRESS R TO RESTART",
            self.medium_font,
            350,
            (60, 255, 100)
        )

        # -------------------------
        # Main menu
        # -------------------------

        self.draw_centered_text(
            screen,
            "PRESS M FOR MAIN MENU",
            self.medium_font,
            410,
            (100, 220, 255)
        )

        # -------------------------
        # Quit
        # -------------------------

        self.draw_centered_text(
            screen,
            "PRESS ESC TO QUIT",
            self.small_font,
            480,
            (150, 150, 150)
        )