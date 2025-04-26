import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Game settings
FPS = 60

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Adventure")

clock = pygame.time.Clock()

# Load assets
def load_image(name):
    return pygame.image.load(os.path.join('assets', 'images', name)).convert_alpha()

player_img = load_image('player.png')
player_mini_img = load_image('player_mini.png')
bullet_img = load_image('bullet.png')
enemy_imgs = [load_image(f'enemy{i}.png') for i in range(1, 4)]
powerup_imgs = {
    'shield': load_image('powerup_shield.png'),
    'power': load_image('powerup_power.png')
}
explosion_imgs = [load_image(f'explosion{i}.png') for i in range(1, 6)]

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = 0
        self.power_level = 1
        self.power_timer = 0

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = SCREEN_WIDTH // 2
            self.rect.bottom = SCREEN_HEIGHT - 10

        if self.power_level > 1 and pygame.time.get_ticks() - self.power_timer > 5000:
            self.power_level -= 1
            self.power_timer = pygame.time.get_ticks()

        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -8
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 8

        self.rect.x += self.speed_x
        self.rect.right = min(self.rect.right, SCREEN_WIDTH)
        self.rect.left = max(self.rect.left, 0)

    def shoot(self):
        if not self.hidden:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            if self.power_level >= 2:
                bullet2 = Bullet(self.rect.centerx - 15, self.rect.top)
                all_sprites.add(bullet2)
                bullets.add(bullet2)

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT + 200)

    def powerup(self):
        self.power_level += 1
        self.power_timer = pygame.time.get_ticks()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(enemy_imgs)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -100)
        self.speedy = random.randint(2, 6)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT or self.rect.left < -30 or self.rect.right > SCREEN_WIDTH + 30:
            self.rect.y = random.randint(-100, -40)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Function to draw shield bar
def draw_shield_bar(surface, x, y, percentage):
    pygame.draw.rect(surface, GREEN, (x, y, (percentage / 100) * 100, 10))

# Function to draw lives
def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(img, img_rect)

# Game loop
def main_game():
    global all_sprites, bullets, enemies
    
    running = True
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    
    player = Player()
    all_sprites.add(player)

    for _ in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    score = 0

    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()

        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, SCREEN_WIDTH - 100, 5, player.lives, player_mini_img)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main_game()
