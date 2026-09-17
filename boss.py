import pygame


# =========================
# BOSS
# =========================

class Boss:

    def __init__(self, width, height):

        self.screen_width = width
        self.screen_height = height

        # Boss size

        self.width = 180
        self.height = 100

        # Starting position

        self.x = (
            self.screen_width // 2
            - self.width // 2
        )

        self.y = 70

        # =========================
        # BOSS MOVEMENT
        # =========================

        self.speed = 6
        self.direction = 1

        # =========================
        # BOSS HEALTH
        # =========================

        self.max_hp = 50
        self.hp = self.max_hp

        self.active = False
        self.defeated = False

        # =========================
        # BOSS ATTACK
        # =========================

        self.attack_timer = 0

        # Lower value = attacks more frequently
        self.attack_delay = 35

        # Faster boss projectiles
        self.projectile_speed = 15

        self.projectiles = []

    # =========================
    # START BOSS
    # =========================

    def start(self):

        self.active = True
        self.defeated = False

        self.hp = self.max_hp

        self.x = (
            self.screen_width // 2
            - self.width // 2
        )

        self.y = 70

        self.attack_timer = 0

        self.projectiles.clear()

    # =========================
    # UPDATE BOSS
    # =========================

    def update(self):

        if not self.active:
            return

        # =========================
        # BOSS MOVEMENT
        # =========================

        self.x += (
            self.speed
            * self.direction
        )

        # Left boundary

        if self.x <= 20:

            self.x = 20

            self.direction = 1

        # Right boundary

        if self.x >= (
            self.screen_width
            - self.width
            - 20
        ):

            self.x = (
                self.screen_width
                - self.width
                - 20
            )

            self.direction = -1

        # =========================
        # BOSS ATTACK TIMER
        # =========================

        self.attack_timer += 1

        if self.attack_timer >= self.attack_delay:

            self.attack()

            self.attack_timer = 0

        # =========================
        # UPDATE PROJECTILES
        # =========================

        for projectile in self.projectiles[:]:

            projectile["y"] += (
                self.projectile_speed
            )

            # Remove projectile
            # after leaving screen

            if projectile["y"] > self.screen_height:

                self.projectiles.remove(
                    projectile
                )

    # =========================
    # BOSS ATTACK
    # =========================

    def attack(self):

        positions = [

            self.x + 30,

            self.x + self.width // 2,

            self.x + self.width - 30

        ]

        for x in positions:

            projectile = {

                "x": x,

                "y":
                    self.y
                    + self.height,

                "width": 12,

                "height": 24
            }

            self.projectiles.append(
                projectile
            )

    # =========================
    # DAMAGE BOSS
    # =========================

    def damage(self, amount=1):

        if not self.active:

            return False

        self.hp -= amount

        if self.hp <= 0:

            self.hp = 0

            self.active = False
            self.defeated = True

            self.projectiles.clear()

            return True

        return False

    # =========================
    # GET BOSS RECTANGLE
    # =========================

    def get_rect(self):

        return pygame.Rect(

            int(self.x),

            int(self.y),

            self.width,

            self.height
        )

    # =========================
    # DRAW BOSS
    # =========================

    def draw(self, screen):

        if not self.active:

            return

        x = int(self.x)
        y = int(self.y)

        # =========================
        # BOSS BODY
        # =========================

        pygame.draw.rect(

            screen,

            (180, 70, 255),

            (
                x,
                y,
                self.width,
                self.height
            ),

            border_radius=15
        )

        # Inner body

        pygame.draw.rect(

            screen,

            (40, 40, 80),

            (
                x + 10,
                y + 10,
                self.width - 20,
                self.height - 20
            ),

            border_radius=10
        )

        # =========================
        # LEFT WEAPON
        # =========================

        pygame.draw.rect(

            screen,

            (255, 60, 60),

            (
                x + 15,
                y + 65,
                35,
                20
            ),

            border_radius=5
        )

        # =========================
        # RIGHT WEAPON
        # =========================

        pygame.draw.rect(

            screen,

            (255, 60, 60),

            (
                x + self.width - 50,
                y + 65,
                35,
                20
            ),

            border_radius=5
        )

        # =========================
        # BOSS CORE
        # =========================

        pygame.draw.circle(

            screen,

            (255, 230, 40),

            (
                x + self.width // 2,
                y + self.height // 2
            ),

            25
        )

        pygame.draw.circle(

            screen,

            (255, 255, 255),

            (
                x + self.width // 2,
                y + self.height // 2
            ),

            12
        )

        # =========================
        # HEALTH BAR
        # =========================

        bar_width = self.width
        bar_height = 10

        pygame.draw.rect(

            screen,

            (80, 80, 80),

            (
                x,
                y - 20,
                bar_width,
                bar_height
            )
        )

        health_width = int(

            bar_width
            * (
                self.hp
                / self.max_hp
            )
        )

        pygame.draw.rect(

            screen,

            (60, 255, 100),

            (
                x,
                y - 20,
                health_width,
                bar_height
            )
        )

        # =========================
        # BOSS LABEL
        # =========================

        font = pygame.font.Font(

            None,

            22
        )

        text = font.render(

            "BOSS",

            True,

            (255, 255, 255)
        )

        text_rect = text.get_rect(

            center=(

                x + self.width // 2,

                y - 35
            )
        )

        screen.blit(

            text,

            text_rect
        )

        # =========================
        # BOSS PROJECTILES
        # =========================

        for projectile in self.projectiles:

            projectile_x = int(

                projectile["x"]
            )

            projectile_y = int(

                projectile["y"]
            )

            # Main projectile

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

            # Projectile glow

            pygame.draw.circle(

                screen,

                (255, 150, 40),

                (
                    projectile_x,

                    projectile_y
                ),

                5
            )

    # =========================
    # RESET BOSS
    # =========================

    def reset(self):

        self.active = False
        self.defeated = False

        self.hp = self.max_hp

        self.x = (

            self.screen_width // 2
            - self.width // 2
        )

        self.y = 70

        self.attack_timer = 0

        self.projectiles.clear()