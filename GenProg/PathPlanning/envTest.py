import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Crop Plot Environment")

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
brown = (139, 69, 19)
light_blue = (50, 175, 200)
black = (0, 0, 0)
red = (255,0,0)

# Define the X-shaped sprite
sprite_size = 15
x_sprite = [
    (width // 2 - sprite_size // 2, height // 2 - sprite_size // 2),
    (width // 2 + sprite_size // 2, height // 2 + sprite_size // 2),
    (width // 2 - sprite_size // 2, height // 2 + sprite_size // 2),
    (width // 2 + sprite_size // 2, height // 2 - sprite_size // 2),
]
x_sprite2 = [
    (10, height - 10),
    (sprite_size + 10, height - sprite_size - 10),
    (10, height - sprite_size - 10),
    (sprite_size + 10, height - 10),
]
vision_radius = 10
vision_center = (width // 2, height // 2)
vision_center2 = (vision_radius + 8, height - vision_radius - 8)

# Define the fence and crop plot
outside_area = pygame.Rect(0, 0, 1400, 1000)
fence_rect = pygame.Rect(50, 50, 700, 500)
space_between_fence_and_plot = 15 # Adjust the space here
spacing_rect = pygame.Rect(
    fence_rect.x + space_between_fence_and_plot,
    fence_rect.y + space_between_fence_and_plot,
    fence_rect.width - 2 * space_between_fence_and_plot,
    fence_rect.height - 2 * space_between_fence_and_plot,
)
crop_plot_rect = pygame.Rect(
    spacing_rect.x + space_between_fence_and_plot,
    spacing_rect.y + space_between_fence_and_plot,
    spacing_rect.width - 2 * space_between_fence_and_plot,
    spacing_rect.height - 2 * space_between_fence_and_plot,
)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(white)

    #Draw outer area
    pygame.draw.rect(screen, light_blue, outside_area)
    
    # Draw fence
    pygame.draw.rect(screen, brown, fence_rect)

    # Draw spacing
    pygame.draw.rect(screen, white, spacing_rect)

    # Draw crop plot
    pygame.draw.rect(screen, green, crop_plot_rect)

    # Draw the vision
    pygame.draw.circle(screen, red, vision_center, vision_radius)

    #Draw Sprite
    pygame.draw.line(screen, black, x_sprite[0], x_sprite[1], 2)
    pygame.draw.line(screen, black, x_sprite[2], x_sprite[3], 2)
   
    #Draw Vision2
    pygame.draw.circle(screen, red, vision_center2, vision_radius)

    #Draw Sprite2
    pygame.draw.line(screen, black, x_sprite2[0], x_sprite2[1], 2)
    pygame.draw.line(screen, black, x_sprite2[2], x_sprite2[3], 2)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(30)
