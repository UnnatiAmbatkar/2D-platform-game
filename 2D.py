import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Platformer Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Create player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - 70
        self.velocity_y = 0
        self.on_ground = True

    def update(self):
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -15
            self.on_ground = False

        # Gravity
        self.velocity_y += 0.5
        self.rect.y += self.velocity_y

        # Stop at ground level
        if self.rect.y > SCREEN_HEIGHT - 70:
            self.rect.y = SCREEN_HEIGHT - 70
            self.velocity_y = 0
            self.on_ground = True

# Create platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Groups for sprites
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Create player object
player = Player()
all_sprites.add(player)

# Create platforms
platform1 = Platform(200, 300, 100, 10)
platform2 = Platform(400, 250, 150, 10)
platforms.add(platform1, platform2)
all_sprites.add(platform1, platform2)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Check for collisions
    for platform in platforms:
        if player.rect.colliderect(platform.rect) and player.velocity_y > 0:
            player.rect.bottom = platform.rect.top
            player.velocity_y = 0
            player.on_ground = True

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Refresh the display
    pygame.display.flip()

    # Maintain frame rate
    clock.tick(FPS)

pygame.quit()
