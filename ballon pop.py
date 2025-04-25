import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Popping Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
balloon_image = pygame.image.load("ballon.png")
background_image = pygame.image.load("bg1.png")

# Scale images
balloon_image = pygame.transform.scale(balloon_image, (50, 70))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Balloon class
class Balloon:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 50)
        self.y = random.randint(-HEIGHT, -50)
        self.speed = random.uniform(0.5, 1.5)  # Initial slower speed
        self.rect = pygame.Rect(self.x, self.y, 50, 70)

    def draw(self, screen):
        screen.blit(balloon_image, (self.x, self.y))

    def move(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def slow_down(self):
        self.speed = max(0.1, self.speed - 0.1)  # Decrease speed but ensure it doesn't go below 0.1

# Game variables
balloons = [Balloon() for _ in range(10)]
score = 0
font = pygame.font.Font(None, 74)
game_over = False
start_time = time.time()
slow_down_interval = 5  # Time interval in seconds to slow down balloons

# Main game loop
running = True
while running:
    screen.blit(background_image, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            for balloon in balloons:
                if balloon.rect.collidepoint(event.pos):
                    score += 1
                    balloon.y = random.randint(-HEIGHT, -50)
                    balloon.x = random.randint(0, WIDTH - 50)
                    balloon.speed = random.uniform(0.5, 1.5)  # Reset balloon speed to initial slower speed

    if not game_over:
        # Slow down balloons every slow_down_interval seconds
        current_time = time.time()
        if current_time - start_time > slow_down_interval:
            for balloon in balloons:
                balloon.slow_down()
            start_time = current_time  # Reset the start time

        # Move and draw balloons
        for balloon in balloons:
            balloon.move()
            balloon.draw(screen)
            if balloon.y > HEIGHT:
                game_over = True

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
    else:
        # Draw game over screen
        game_over_text = font.render("Game Over", True, BLACK)
        final_score_text = font.render(f"Final Score: {score}", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        screen.blit(final_score_text, (WIDTH // 2 - 150, HEIGHT // 2 + 10))

    # Update display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
