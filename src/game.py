import pygame
import sys
import colorlist as colors # manage list of colors easier instead of having a bunch of colors in code that are hardcoded
import translations as key
import config as cfg
import entities.player as player
# Initialize Pygame
pygame.init()

window = pygame.display.set_mode((cfg.WINDOW_HEIGHT, cfg.WINDOW_WIDTH))

# Set window title and translation language
key.CURR_LANG = 'dr_dr'
pygame.display.set_caption(key.ROOT_TITLE)
# how do i test
# Clock for controlling the frame rate
CLOCK = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    player.move_player(keys, player.player_pos, player.player_speed)
    # Fill window with background color
    window.fill(colors.cornflower_blue)
    
    CLOCK.tick(144)
    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()