import pygame


# =========================
# SOUND MANAGER
# =========================

class SoundManager:

    def __init__(self):

        self.shoot = pygame.mixer.Sound(
            "sounds/shoot.wav"
        )

        self.explosion = pygame.mixer.Sound(
            "sounds/explosion.wav"
        )

        self.shield = pygame.mixer.Sound(
            "sounds/shield.wav"
        )

        self.rapid = pygame.mixer.Sound(
            "sounds/rapid.wav"
        )

        self.life = pygame.mixer.Sound(
            "sounds/life.wav"
        )

        self.gameover = pygame.mixer.Sound(
            "sounds/gameover.wav"
        )

        # Volume settings

        self.shoot.set_volume(0.35)

        self.explosion.set_volume(0.45)

        self.shield.set_volume(0.40)

        self.rapid.set_volume(0.40)

        self.life.set_volume(0.40)

        self.gameover.set_volume(0.45)