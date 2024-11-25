import pygame
import time
import random


pygame.init()
pygame.font.init()
pygame.mixer.init()

def play_music():
    pygame.mixer.music.load(".venv/spotifydown.com - The Mandalorian.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)



# Screen dimensions
WIDTH, HEIGHT = 500, 700
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE SHOOTER")

# Assets
PLAYER_IMAGE = pygame.image.load(r"C:\Users\adars\OneDrive\Desktop\mosh\gameygame2\.venv\pngwing2.com.png")
ENEMY_IMAGE = pygame.image.load(r"C:\Users\adars\OneDrive\Desktop\mosh\gameygame2\.venv\pngwing.com.png")
PROJECTILE_IMAGE = pygame.image.load(r"C:\Users\adars\OneDrive\Desktop\mosh\gameygame2\.venv\pngwing3.com.png")
BACKGROUND_IMAGE = pygame.image.load(r"C:\Users\adars\OneDrive\Desktop\mosh\gameygame2\.venv\vertical-outer-space-2zwgell1rn5edyul.jpg")

icon = pygame.image.load(r"C:\Users\adars\OneDrive\Desktop\mosh\gameygame2\.venv\rocket-space-logo-design-template_173356-81.jpg  ")
pygame.display.set_icon(icon)


# Scaling assets
SCALE_FACTOR = 0.1
PLAYER_IMAGE = pygame.transform.scale(
    PLAYER_IMAGE, (int(PLAYER_IMAGE.get_width() * SCALE_FACTOR), int(PLAYER_IMAGE.get_height() * SCALE_FACTOR))
)
ENEMY_IMAGE = pygame.transform.scale(
    ENEMY_IMAGE, (int(ENEMY_IMAGE.get_width() * SCALE_FACTOR), int(ENEMY_IMAGE.get_height() * SCALE_FACTOR))
)
PROJECTILE_SCALE = 0.05
PROJECTILE_IMAGE = pygame.transform.scale(
    PROJECTILE_IMAGE, (int(PROJECTILE_IMAGE.get_width() * PROJECTILE_SCALE), int(PROJECTILE_IMAGE.get_height() * PROJECTILE_SCALE))
)

# Player properties
PLAYER_RECT = PLAYER_IMAGE.get_rect(midbottom=(WIDTH // 2, HEIGHT - 50))
PLAYER_VEL = 5
PLAYER_PROJECTILE_VEL = -10

# Enemy properties
ENEMY_VEL = 3
ENEMY_SPAWN_INTERVAL = 2000  # Spawn every 2 seconds
ENEMIES = []

# Projectiles
ENEMY_PROJECTILES = []
PLAYER_PROJECTILES = []
ENEMY_PROJECTILE_VEL = 6

# Font
FONT = pygame.font.SysFont("comicsans", 30)

# Functions
def spawn_enemy():
    """Spawns an enemy at a random x-coordinate at the top of the screen."""
    x_pos = random.randint(0, WIDTH - ENEMY_IMAGE.get_width())
    ENEMIES.append(ENEMY_IMAGE.get_rect(topleft=(x_pos, -ENEMY_IMAGE.get_height())))


def shoot_projectile(rect, projectiles, direction):
    """Creates a projectile from a given rect."""
    proj_rect = PROJECTILE_IMAGE.get_rect(midtop=rect.midbottom if direction > 0 else rect.midtop)
    projectiles.append(proj_rect)


def handle_movement(projectiles, velocity, boundary_check):
    """Handles movement for projectiles and removes those out of bounds."""
    for projectile in projectiles[:]:
        projectile.y += velocity
        if boundary_check(projectile):
            projectiles.remove(projectile)


def draw(elapsed_time):
    """Draws all elements on the screen."""
    DISPLAY.blit(BACKGROUND_IMAGE, (0, 0))
    time_text = FONT.render(f"TIME: {round(elapsed_time)}s", 1, "white")
    DISPLAY.blit(time_text, (10, 10))
    DISPLAY.blit(PLAYER_IMAGE, PLAYER_RECT)

    for enemy in ENEMIES:
        DISPLAY.blit(ENEMY_IMAGE, enemy)
    for projectile in PLAYER_PROJECTILES:
        DISPLAY.blit(PROJECTILE_IMAGE, projectile)
    for projectile in ENEMY_PROJECTILES:
        DISPLAY.blit(PROJECTILE_IMAGE, projectile)

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    start_time = time.time()
    last_enemy_spawn = 0
    running = True

    play_music()

    while running:
        clock.tick(60)
        elapsed_time = time.time() - start_time

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and PLAYER_RECT.left > 0:
            PLAYER_RECT.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and PLAYER_RECT.right < WIDTH:
            PLAYER_RECT.x += PLAYER_VEL
        if keys[pygame.K_UP] and PLAYER_RECT.top > 0:
            PLAYER_RECT.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and PLAYER_RECT.bottom < HEIGHT:
            PLAYER_RECT.y += PLAYER_VEL
        if keys[pygame.K_SPACE]:  # Player shooting
            if len(PLAYER_PROJECTILES) < 5:  # Limit projectiles
                shoot_projectile(PLAYER_RECT, PLAYER_PROJECTILES, -1)

        # Spawn enemies
        if pygame.time.get_ticks() - last_enemy_spawn > ENEMY_SPAWN_INTERVAL:
            spawn_enemy()
            last_enemy_spawn = pygame.time.get_ticks()

        # Enemies shooting projectiles
        for enemy in ENEMIES:
            if random.random() < 0.02:  # 2% chance per frame
                shoot_projectile(enemy, ENEMY_PROJECTILES, 1)

        # Update positions
        handle_movement(PLAYER_PROJECTILES, PLAYER_PROJECTILE_VEL, lambda p: p.bottom < 0)
        handle_movement(ENEMY_PROJECTILES, ENEMY_PROJECTILE_VEL, lambda p: p.top > HEIGHT)
        for enemy in ENEMIES[:]:
            enemy.y += ENEMY_VEL
            if enemy.top > HEIGHT:
                ENEMIES.remove(enemy)

        # Collision detection
        for enemy in ENEMIES[:]:
            if PLAYER_RECT.colliderect(enemy):
                running = False
            for projectile in PLAYER_PROJECTILES[:]:
                if projectile.colliderect(enemy):
                    PLAYER_PROJECTILES.remove(projectile)
                    if enemy in ENEMIES:
                        ENEMIES.remove(enemy)

        for projectile in ENEMY_PROJECTILES[:]:
            if PLAYER_RECT.colliderect(projectile):
                running = False


        if not running:
            lost_text = FONT.render("YOU LOST!", 1 , "white")
            DISPLAY.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(elapsed_time)


if __name__ == "__main__":
    main()
