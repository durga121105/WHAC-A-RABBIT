import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BURROW_SIZE = 120  # Increased burrow size
RABBIT_SIZE = 80   # Increased rabbit size
MOLE_POP_UP_TIME = 5000  # milliseconds
FONT_SIZE = 36
NUM_BURROWS = 9
ROWS = 3
COLS = 3
ANIMATION_FRAMES = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Whac-A-Rabbit')

# Load images
rabbit_image = pygame.image.load('rabbit3.png')
rabbit_image = pygame.transform.scale(rabbit_image, (RABBIT_SIZE, RABBIT_SIZE))

burrow_image = pygame.image.load('burrow.png')
burrow_image = pygame.transform.scale(burrow_image, (BURROW_SIZE, BURROW_SIZE))

grass_image = pygame.image.load('grass4.png')  # Load grass background image
grass_image = pygame.transform.scale(grass_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Font
font = pygame.font.Font(None, FONT_SIZE)

# Burrow positions (organized in a grid)
burrow_positions = []
margin_x = (SCREEN_WIDTH - (COLS * BURROW_SIZE)) // 2
margin_y = (SCREEN_HEIGHT - (ROWS * BURROW_SIZE)) // 2
for row in range(ROWS):
    for col in range(COLS):
        x = margin_x + col * BURROW_SIZE
        y = margin_y + row * BURROW_SIZE
        burrow_positions.append((x, y))

# Rabbit class
class Rabbit:
    def __init__(self):
        self.rect = rabbit_image.get_rect()
        self.reset()
        self.animation_frame = 0
        self.popping_up = True

    def reset(self):
        self.rect.topleft = random.choice(burrow_positions)
        self.animation_frame = 0
        self.popping_up = True

    def draw(self, screen):
        if self.popping_up:
            if self.animation_frame < ANIMATION_FRAMES:
                scale_factor = self.animation_frame / ANIMATION_FRAMES
                scaled_size = int(RABBIT_SIZE * scale_factor)
                scaled_image = pygame.transform.scale(rabbit_image, (scaled_size, scaled_size))
                scaled_rect = scaled_image.get_rect(center=self.rect.center)
                screen.blit(scaled_image, scaled_rect.topleft)
                self.animation_frame += 1
            else:
                self.popping_up = False
                screen.blit(rabbit_image, self.rect.topleft)
        else:
            screen.blit(rabbit_image, self.rect.topleft)

# Main game loop
def main():
    clock = pygame.time.Clock()
    rabbit = Rabbit()
    score = 0
    last_pop_up_time = pygame.time.get_ticks()

    running = True
    while running:
        screen.blit(grass_image, (0, 0))  # Draw grass background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rabbit.rect.collidepoint(event.pos):
                    score += 1
                    rabbit.reset()

        # Rabbit pop-up logic
        current_time = pygame.time.get_ticks()
        if current_time - last_pop_up_time > MOLE_POP_UP_TIME:
            rabbit.reset()
            last_pop_up_time = current_time

        # Draw burrows
        for pos in burrow_positions:
            screen.blit(burrow_image, pos)

        rabbit.draw(screen)

        # Draw score
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
