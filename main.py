import pygame
import math


from config import (
    WIDTH,
    HEIGHT,
    FPS,
    WHITE,
    BLACK
)

from sounds import SoundManager
from stars import Starfield
from explosions import ExplosionManager
from bullets import BulletManager
from enemies import EnemyManager
from powerups import PowerUpManager
from player import Player
from hand_tracker import HandTracker
from menu import MenuManager
from boss import Boss


# ==================================================
# INITIALIZE PYGAME
# ==================================================

pygame.init()
pygame.mixer.init()


# ==================================================
# GAME WINDOW
# ==================================================

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Gesture Space Shooter"
)

clock = pygame.time.Clock()


# ==================================================
# GAME OBJECTS
# ==================================================

sounds = SoundManager()

stars = Starfield(
    WIDTH,
    HEIGHT,
    100
)

explosions = ExplosionManager()

bullets = BulletManager()

enemies = EnemyManager(
    WIDTH,
    HEIGHT
)

powerups = PowerUpManager(
    WIDTH,
    HEIGHT
)

player = Player(
    WIDTH,
    HEIGHT
)

hand_tracker = HandTracker()

menu = MenuManager(
    WIDTH,
    HEIGHT
)

boss = Boss(
    WIDTH,
    HEIGHT
)


# ==================================================
# FONTS
# ==================================================

score_font = pygame.font.Font(
    None,
    28
)

info_font = pygame.font.Font(
    None,
    22
)

warning_font = pygame.font.Font(
    None,
    42
)

special_font = pygame.font.Font(
    None,
    26
)


# ==================================================
# GAME STATES
# ==================================================

MENU = 0
PLAYING = 1
GAME_OVER = 2

game_state = MENU


# ==================================================
# GAME VARIABLES
# ==================================================

score = 0
lives = 3

difficulty = 1

spawn_timer = 0
spawn_delay = 40

powerup_timer = 0
powerup_delay = 600

shoot_timer = 0
shoot_delay = 12

rapid_fire_timer = 0

# Shield: 5 seconds active + 5 seconds cooldown
SHIELD_DURATION = 5 * FPS
SHIELD_COOLDOWN = 5 * FPS

shield_timer = 0
shield_cooldown_timer = 0

hand_detected = False


# ==================================================
# SPECIAL ATTACK
# ==================================================

# 7 seconds at 60 FPS

SPECIAL_COOLDOWN = 7 * FPS

special_timer = 0

# Prevents repeated activation while
# the three-finger gesture is held.

special_gesture_was_active = False


# Special bullets

special_bullets = []

SPECIAL_BULLET_SPEED = 12

SPECIAL_BULLET_RADIUS = 5


# ==================================================
# BOSS SETTINGS
# ==================================================

next_boss_score = 300

boss_reward = 100

boss_warning_distance = 50


# ==================================================
# GAME OVER SOUND
# ==================================================

game_over_sound_played = False


# ==================================================
# RESET GAME
# ==================================================

def reset_game():

    global score
    global lives
    global difficulty
    global spawn_timer
    global spawn_delay
    global powerup_timer
    global shoot_timer
    global rapid_fire_timer
    global shield_timer
    global shield_cooldown_timer
    global next_boss_score
    global game_over_sound_played
    global special_timer
    global special_gesture_was_active

    score = 0
    lives = 3

    difficulty = 1

    spawn_timer = 0
    spawn_delay = 40

    powerup_timer = 0

    shoot_timer = 0

    rapid_fire_timer = 0

    shield_timer = 0
    shield_cooldown_timer = 0

    next_boss_score = 300

    game_over_sound_played = False

    special_timer = 0

    special_gesture_was_active = False

    special_bullets.clear()

    bullets.clear()

    enemies.clear()

    powerups.clear()

    explosions.clear()

    boss.reset()

    player.x = (
        WIDTH // 2
        - player.width // 2
    )

    player.set_shield(False)


# ==================================================
# CREATE SPECIAL BULLETS
# ==================================================

def fire_special_attack():

    center_x = (
        player.x
        + player.width / 2
    )

    center_y = (
        player.y
        + player.height / 2
    )

    # 8 directions

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1)
    ]

    for dx, dy in directions:

        length = math.sqrt(
            dx * dx + dy * dy
        )

        dx /= length
        dy /= length

        special_bullets.append({

            "x": center_x,

            "y": center_y,

            "dx": dx,

            "dy": dy
        })


# ==================================================
# UPDATE SPECIAL BULLETS
# ==================================================

def update_special_bullets():

    for bullet in special_bullets[:]:

        bullet["x"] += (
            bullet["dx"]
            * SPECIAL_BULLET_SPEED
        )

        bullet["y"] += (
            bullet["dy"]
            * SPECIAL_BULLET_SPEED
        )

        # Remove bullets outside screen

        if (
            bullet["x"] < -20
            or bullet["x"] > WIDTH + 20
            or bullet["y"] < -20
            or bullet["y"] > HEIGHT + 20
        ):

            special_bullets.remove(
                bullet
            )


# ==================================================
# DRAW SPECIAL BULLETS
# ==================================================

def draw_special_bullets():

    for bullet in special_bullets:

        x = int(
            bullet["x"]
        )

        y = int(
            bullet["y"]
        )

        pygame.draw.circle(
            screen,
            (255, 230, 40),
            (x, y),
            SPECIAL_BULLET_RADIUS
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (x, y),
            2
        )


# ==================================================
# SPECIAL BULLET RECT
# ==================================================

def get_special_bullet_rect(
    bullet
):

    return pygame.Rect(
        int(
            bullet["x"]
            - SPECIAL_BULLET_RADIUS
        ),
        int(
            bullet["y"]
            - SPECIAL_BULLET_RADIUS
        ),
        SPECIAL_BULLET_RADIUS * 2,
        SPECIAL_BULLET_RADIUS * 2
    )


# ==================================================
# DRAW HUD
# ==================================================

def draw_hud():

    # -------------------------
    # Score
    # -------------------------

    score_text = score_font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (20, 20)
    )


    # -------------------------
    # Lives
    # -------------------------

    lives_text = score_font.render(
        f"Lives: {lives}",
        True,
        WHITE
    )

    screen.blit(
        lives_text,
        (20, 55)
    )


    # -------------------------
    # Difficulty
    # -------------------------

    difficulty_text = info_font.render(
        f"Level: {difficulty}",
        True,
        WHITE
    )

    screen.blit(
        difficulty_text,
        (
            WIDTH - 120,
            25
        )
    )


    # -------------------------
    # Rapid Fire
    # -------------------------

    if rapid_fire_timer > 0:

        rapid_text = info_font.render(
            "RAPID FIRE",
            True,
            (60, 255, 100)
        )

        screen.blit(
            rapid_text,
            (
                WIDTH - 150,
                55
            )
        )


    # -------------------------
    # Shield
    # -------------------------

    if shield_timer > 0:

        shield_seconds = math.ceil(
            shield_timer / FPS
        )

        shield_text = info_font.render(
            f"SHIELD: {shield_seconds}s",
            True,
            (60, 240, 255)
        )

    elif shield_cooldown_timer > 0:

        cooldown_seconds = math.ceil(
            shield_cooldown_timer / FPS
        )

        shield_text = info_font.render(
            f"SHIELD CD: {cooldown_seconds}s",
            True,
            (255, 180, 60)
        )

    else:

        shield_text = info_font.render(
            "SHIELD READY",
            True,
            (60, 240, 255)
        )

    screen.blit(
        shield_text,
        (
            WIDTH - 155,
            80
        )
    )


    # -------------------------
    # Boss
    # -------------------------

    if boss.active:

        boss_text = info_font.render(
            "BOSS BATTLE",
            True,
            (255, 60, 60)
        )

        screen.blit(
            boss_text,
            (
                WIDTH // 2 - 65,
                20
            )
        )


    # -------------------------
    # Special Attack
    # -------------------------

    if special_timer <= 0:

        special_text = special_font.render(
            "SPECIAL READY",
            True,
            (255, 230, 40)
        )

    else:

        seconds = math.ceil(
            special_timer / FPS
        )

        special_text = special_font.render(
            f"SPECIAL: {seconds}s",
            True,
            (180, 70, 255)
        )

    screen.blit(
        special_text,
        (
            20,
            HEIGHT - 65
        )
    )


    # -------------------------
    # Gesture Status
    # -------------------------

    if not hand_detected:

        gesture_text = "NO HAND"

        gesture_color = (
            150,
            150,
            150
        )

    elif hand_tracker.is_three_finger():

        gesture_text = "SPECIAL"

        gesture_color = (
            180,
            70,
            255
        )

    elif hand_tracker.is_open_palm():

        gesture_text = "SHIELD"

        gesture_color = (
            60,
            240,
            255
        )

    elif hand_tracker.is_index_folded():

        gesture_text = "SHOOT"

        gesture_color = (
            255,
            230,
            40
        )

    else:

        gesture_text = "MOVE"

        gesture_color = (
            40,
            150,
            255
        )

    gesture_surface = info_font.render(
        f"Gesture: {gesture_text}",
        True,
        gesture_color
    )

    screen.blit(
        gesture_surface,
        (
            WIDTH // 2 - 70,
            HEIGHT - 35
        )
    )


# ==================================================
# BOSS WARNING
# ==================================================

def draw_boss_warning():

    warning_start = (
        next_boss_score
        - boss_warning_distance
    )

    if (
        score >= warning_start
        and score < next_boss_score
        and not boss.active
    ):

        # Flash warning

        if (
            pygame.time.get_ticks()
            // 500
        ) % 2 == 0:

            warning_text = (
                warning_font.render(
                    "WARNING: BOSS INCOMING!",
                    True,
                    (255, 60, 60)
                )
            )

            warning_rectangle = (
                warning_text.get_rect(
                    center=(
                        WIDTH // 2,
                        HEIGHT // 2 - 60
                    )
                )
            )

            screen.blit(
                warning_text,
                warning_rectangle
            )


        remaining = (
            next_boss_score
            - score
        )

        remaining_text = info_font.render(
            (
                f"BOSS AT SCORE "
                f"{next_boss_score}"
                f"  |  {remaining} POINTS"
            ),
            True,
            (255, 230, 40)
        )

        remaining_rectangle = (
            remaining_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2
                )
            )
        )

        screen.blit(
            remaining_text,
            remaining_rectangle
        )


# ==================================================
# SHIELD ACTIVATION
# ==================================================

def activate_shield():
    global shield_timer

    # Shield can only activate when both active time
    # and cooldown have finished.
    if shield_timer <= 0 and shield_cooldown_timer <= 0:

        shield_timer = SHIELD_DURATION

        sounds.shield.play()

        return True

    return False


# ==================================================
# MAIN GAME LOOP
# ==================================================

running = True


while running:

    clock.tick(FPS)


    # ==================================================
    # EVENTS
    # ==================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


        if event.type == pygame.KEYDOWN:

            # -------------------------
            # MENU
            # -------------------------

            if game_state == MENU:

                if event.key == pygame.K_RETURN:

                    reset_game()

                    game_state = PLAYING


            # -------------------------
            # GAME OVER
            # -------------------------

            elif game_state == GAME_OVER:

                if event.key == pygame.K_r:

                    reset_game()

                    game_state = PLAYING

                elif event.key == pygame.K_m:

                    game_state = MENU

                elif event.key == pygame.K_ESCAPE:

                    running = False


    # ==================================================
    # MENU
    # ==================================================

    if game_state == MENU:

        menu.draw_menu(
            screen
        )

        pygame.display.flip()

        continue


    # ==================================================
    # GAME OVER
    # ==================================================

    if game_state == GAME_OVER:

        menu.draw_game_over(
            screen,
            score
        )

        pygame.display.flip()

        continue


    # ==================================================
    # CAMERA / HAND TRACKING
    # ==================================================

    camera_frame = (
        hand_tracker.update()
    )

    if camera_frame is None:

        hand_detected = False

    else:

        hand_detected = (
            hand_tracker.is_hand_detected()
        )


    # ==================================================
    # KEYBOARD
    # ==================================================

    keys = pygame.key.get_pressed()


    # ==================================================
    # PLAYER MOVEMENT
    # ==================================================

    if hand_detected:

        player.move_with_hand(
            hand_tracker.get_index_x()
        )

    else:

        player.move_keyboard(
            keys
        )


    # ==================================================
    # SHIELD
    # ==================================================

    if hand_detected:

        if hand_tracker.is_open_palm():

            activate_shield()


    # Shield active timer
    if shield_timer > 0:

        shield_timer -= 1

        # When the 5-second shield ends, start the
        # 5-second cooldown.
        if shield_timer <= 0:

            shield_timer = 0
            shield_cooldown_timer = SHIELD_COOLDOWN

        player.set_shield(True)

    else:

        player.set_shield(False)


    # Shield cooldown timer
    if shield_cooldown_timer > 0:

        shield_cooldown_timer -= 1

        if shield_cooldown_timer < 0:

            shield_cooldown_timer = 0


    # ==================================================
    # NORMAL SHOOTING
    # ==================================================

    shooting = False


    if hand_detected:

        if hand_tracker.is_index_folded():

            shooting = True


    # Keyboard backup

    if keys[pygame.K_SPACE]:

        shooting = True


    if shoot_timer > 0:

        shoot_timer -= 1


    if (
        shooting
        and shoot_timer <= 0
    ):

        bullets.shoot(
            player.x,
            player.width,
            player.y
        )

        sounds.shoot.play()


        if rapid_fire_timer > 0:

            shoot_timer = 4

        else:

            shoot_timer = shoot_delay


    # ==================================================
    # SPECIAL GESTURE
    # ==================================================

    three_finger_active = False


    if hand_detected:

        three_finger_active = (
            hand_tracker.is_three_finger()
        )


    # Activate only when gesture changes
    # from OFF → ON.

    if three_finger_active:

        if not special_gesture_was_active:

            if special_timer <= 0:

                fire_special_attack()

                special_timer = (
                    SPECIAL_COOLDOWN
                )

                sounds.shoot.play()


        special_gesture_was_active = True

    else:

        special_gesture_was_active = False


    # ==================================================
    # SPECIAL TIMER
    # ==================================================

    if special_timer > 0:

        special_timer -= 1


    # ==================================================
    # RAPID FIRE TIMER
    # ==================================================

    if rapid_fire_timer > 0:

        rapid_fire_timer -= 1


    # ==================================================
    # STARS
    # ==================================================

    stars.update()


    # ==================================================
    # NORMAL BULLETS
    # ==================================================

    bullets.update()


    # ==================================================
    # SPECIAL BULLETS
    # ==================================================

    update_special_bullets()


    # ==================================================
    # BOSS ACTIVATION
    # ==================================================

    if (
        score >= next_boss_score
        and not boss.active
    ):

        # Clear normal enemies
        # only when boss actually starts.

        enemies.clear()

        boss.start()


    # ==================================================
    # BOSS UPDATE
    # ==================================================

    if boss.active:

        boss.update()


    # ==================================================
    # NORMAL ENEMY SPAWNING
    # ==================================================

    # IMPORTANT:
    #
    # Boss warning DOES NOT stop spawning.
    #
    # Normal enemies continue spawning
    # until the boss actually activates.

    if not boss.active:

        spawn_timer += 1

        if spawn_timer >= spawn_delay:

            enemies.spawn(
                difficulty
            )

            spawn_timer = 0


    # ==================================================
    # NORMAL ENEMY MOVEMENT
    # ==================================================

    if not boss.active:

        enemies.update(
            player.x,
            player.y
        )


    # ==================================================
    # POWER-UP SPAWNING
    # ==================================================

    powerup_timer += 1

    if powerup_timer >= powerup_delay:

        powerups.spawn()

        powerup_timer = 0


    # ==================================================
    # POWER-UP MOVEMENT
    # ==================================================

    powerups.update()


    # ==================================================
    # EXPLOSIONS
    # ==================================================

    explosions.update()


    # ==================================================
    # NORMAL BULLET VS ENEMY
    # ==================================================

    if not boss.active:

        for bullet in bullets.bullets[:]:

            bullet_rect = (
                bullets.get_rect(
                    bullet
                )
            )


            for enemy in enemies.enemies[:]:

                enemy_rect = (
                    enemies.get_rect(
                        enemy
                    )
                )


                if bullet_rect.colliderect(
                    enemy_rect
                ):

                    bullets.remove(
                        bullet
                    )


                    enemy_x = (
                        enemy["x"]
                        + enemy["width"] / 2
                    )

                    enemy_y = (
                        enemy["y"]
                        + enemy["height"] / 2
                    )


                    points = (
                        enemies.damage(
                            enemy
                        )
                    )


                    explosions.create(
                        enemy_x,
                        enemy_y
                    )


                    sounds.explosion.play()


                    score += points

                    break


    # ==================================================
    # SPECIAL BULLET VS ENEMY
    # ==================================================

    if not boss.active:

        for bullet in special_bullets[:]:

            bullet_rect = (
                get_special_bullet_rect(
                    bullet
                )
            )


            for enemy in enemies.enemies[:]:

                enemy_rect = (
                    enemies.get_rect(
                        enemy
                    )
                )


                if bullet_rect.colliderect(
                    enemy_rect
                ):

                    special_bullets.remove(
                        bullet
                    )


                    enemy_x = (
                        enemy["x"]
                        + enemy["width"] / 2
                    )

                    enemy_y = (
                        enemy["y"]
                        + enemy["height"] / 2
                    )


                    points = (
                        enemies.damage(
                            enemy
                        )
                    )


                    explosions.create(
                        enemy_x,
                        enemy_y,
                        0.7
                    )


                    sounds.explosion.play()


                    score += points

                    break


    # ==================================================
    # NORMAL BULLET VS BOSS
    # ==================================================

    if boss.active:

        boss_rect = (
            boss.get_rect()
        )


        for bullet in bullets.bullets[:]:

            bullet_rect = (
                bullets.get_rect(
                    bullet
                )
            )


            if bullet_rect.colliderect(
                boss_rect
            ):

                bullets.remove(
                    bullet
                )


                defeated = (
                    boss.damage()
                )


                explosions.create(
                    bullet_rect.centerx,
                    bullet_rect.centery,
                    0.5
                )


                if defeated:

                    score += boss_reward

                    next_boss_score = (
                        score + 300
                    )


                    explosions.create(
                        boss.x
                        + boss.width / 2,

                        boss.y
                        + boss.height / 2,

                        3
                    )


                    sounds.explosion.play()


    # ==================================================
    # SPECIAL BULLET VS BOSS
    # ==================================================

    if boss.active:

        boss_rect = (
            boss.get_rect()
        )


        for bullet in special_bullets[:]:

            bullet_rect = (
                get_special_bullet_rect(
                    bullet
                )
            )


            if bullet_rect.colliderect(
                boss_rect
            ):

                special_bullets.remove(
                    bullet
                )


                defeated = (
                    boss.damage()
                )


                explosions.create(
                    bullet["x"],
                    bullet["y"],
                    0.7
                )


                sounds.explosion.play()


                if defeated:

                    score += boss_reward

                    next_boss_score = (
                        score + 300
                    )


                    explosions.create(
                        boss.x
                        + boss.width / 2,

                        boss.y
                        + boss.height / 2,

                        3
                    )


                    sounds.explosion.play()


    # ==================================================
    # BOSS PROJECTILE VS PLAYER
    # ==================================================

    if boss.active:

        player_rect = (
            player.get_rect()
        )


        for projectile in (
            boss.projectiles[:]
        ):

            projectile_rect = pygame.Rect(

                int(
                    projectile["x"]
                    - projectile["width"] / 2
                ),

                int(
                    projectile["y"]
                ),

                projectile["width"],

                projectile["height"]
            )


            if projectile_rect.colliderect(
                player_rect
            ):

                boss.projectiles.remove(
                    projectile
                )


                if shield_timer > 0:

                    explosions.create(
                        projectile["x"],
                        projectile["y"],
                        0.5
                    )

                    sounds.shield.play()

                else:

                    lives -= 1


                    explosions.create(
                        player.x
                        + player.width / 2,

                        player.y
                        + player.height / 2,

                        0.8
                    )


                    sounds.explosion.play()


    # ==================================================
    # SHOOTER PROJECTILE VS PLAYER
    # ==================================================

    if not boss.active:

        player_rect = (
            player.get_rect()
        )


        for projectile in (
            enemies.projectiles[:]
        ):

            projectile_rect = pygame.Rect(

                int(
                    projectile["x"]
                    - projectile["width"] / 2
                ),

                int(
                    projectile["y"]
                ),

                projectile["width"],

                projectile["height"]
            )


            if projectile_rect.colliderect(
                player_rect
            ):

                enemies.projectiles.remove(
                    projectile
                )


                if shield_timer > 0:

                    explosions.create(
                        projectile["x"],
                        projectile["y"],
                        0.5
                    )

                    sounds.shield.play()

                else:

                    lives -= 1


                    explosions.create(
                        player.x
                        + player.width / 2,

                        player.y
                        + player.height / 2,

                        0.8
                    )


                    sounds.explosion.play()


    # ==================================================
    # PLAYER VS NORMAL ENEMY
    # ==================================================

    player_rect = (
        player.get_rect()
    )


    if not boss.active:

        for enemy in enemies.enemies[:]:

            enemy_rect = (
                enemies.get_rect(
                    enemy
                )
            )


            if player_rect.colliderect(
                enemy_rect
            ):

                enemies.enemies.remove(
                    enemy
                )


                explosions.create(
                    player.x
                    + player.width / 2,

                    player.y
                    + player.height / 2,

                    1.2
                )


                if shield_timer > 0:

                    sounds.shield.play()

                else:

                    lives -= 1

                    sounds.explosion.play()


    # ==================================================
    # PLAYER VS POWER-UP
    # ==================================================

    for powerup in powerups.powerups[:]:

        powerup_rect = (
            powerups.get_rect(
                powerup
            )
        )


        if player_rect.colliderect(
            powerup_rect
        ):

            powerup_type = (
                powerups.collect(
                    powerup
                )
            )


            if powerup_type == "rapid":

                rapid_fire_timer = 300

                sounds.rapid.play()


            elif powerup_type == "shield":

                # Shield power-up follows the same 5-second
                # duration and 5-second cooldown rules.
                activate_shield()


            elif powerup_type == "life":

                lives += 1

                sounds.life.play()


    # ==================================================
    # DIFFICULTY
    # ==================================================

    new_difficulty = (
        score // 100
    ) + 1


    if new_difficulty != difficulty:

        difficulty = new_difficulty


        spawn_delay = max(
            15,
            40
            - (
                difficulty - 1
            ) * 2
        )


    # ==================================================
    # GAME OVER
    # ==================================================

    if lives <= 0:

        game_state = GAME_OVER


        if not game_over_sound_played:

            sounds.gameover.play()

            game_over_sound_played = True


    # ==================================================
    # DRAW
    # ==================================================

    screen.fill(
        BLACK
    )


    # -------------------------
    # Stars
    # -------------------------

    stars.draw(
        screen
    )


    # -------------------------
    # Normal bullets
    # -------------------------

    bullets.draw(
        screen
    )


    # -------------------------
    # Special bullets
    # -------------------------

    draw_special_bullets()


    # -------------------------
    # Enemies
    # -------------------------

    enemies.draw(
        screen
    )


    # -------------------------
    # Power-ups
    # -------------------------

    powerups.draw(
        screen
    )


    # -------------------------
    # Boss
    # -------------------------

    boss.draw(
        screen
    )


    # -------------------------
    # Player
    # -------------------------

    player.draw(
        screen
    )


    # -------------------------
    # Explosions
    # -------------------------

    explosions.draw(
        screen
    )


    # -------------------------
    # HUD
    # -------------------------

    draw_hud()


    # -------------------------
    # Boss warning
    # -------------------------

    draw_boss_warning()


    pygame.display.flip()


# ==================================================
# CLEANUP
# ==================================================

hand_tracker.release()

pygame.quit()