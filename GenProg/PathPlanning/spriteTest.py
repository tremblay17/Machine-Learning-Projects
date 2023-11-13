import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("X-shaped Sprite")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Define the X-shaped sprite
sprite_size = 100
x_sprite = [
    (width // 2 - sprite_size // 2, height // 2 - sprite_size // 2),
    (width // 2 + sprite_size // 2, height // 2 + sprite_size // 2),
    (width // 2 - sprite_size // 2, height // 2 + sprite_size // 2),
    (width // 2 + sprite_size // 2, height // 2 - sprite_size // 2),
]

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(white)

    # Draw the X-shaped sprite
    pygame.draw.line(screen, black, x_sprite[0], x_sprite[1], 2)
    pygame.draw.line(screen, black, x_sprite[2], x_sprite[3], 2)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(30)
