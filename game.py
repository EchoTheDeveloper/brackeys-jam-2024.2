import pygame
import sys

# Initialize Pygame
pygame.init()

# Set window dimensions
window_width, window_height = 640, 480
window = pygame.display.set_mode((window_width, window_height))

# Set window title
pygame.display.set_caption('Simple Pygame Window')

# Define colors
background_color = (100, 149, 237)  # Cornflower blue

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill window with background color
    window.fill(background_color)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
