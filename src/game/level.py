import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config as cfg
import colorlist as colors # manage list of colors easier instead of having a bunch of colors in code that are hardcoded
import translations as key
import config as cfg
import dialogue as d

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((cfg.WINDOW_HEIGHT, cfg.WINDOW_WIDTH))

# Set window title and translation language
pygame.display.set_caption(key.ROOT_TITLE)

# Import after pygame init and window mode set
import entities.player as player

font = pygame.font.SysFont(None, 36)

# Clock for controlling the frame rate
CLOCK = pygame.time.Clock()

# Main game loop
running = True
while running:
    dt = CLOCK.tick(cfg.DEFAULT_FPS) / 1000
    index = 0
    showing_dialogue = True
    # Event handling
    window.fill(colors.pastel_green)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    index += 1
                    if index >= len(d.dialogues):
                        showing_dialogue = False
                    else:
                        print("asddad")
                        d.draw_text_box(d.dialogues[index]["text"], font, window, 0, 0, 250)

    # Fill window with background color

    # fps = int(pygame.Clock.get_fps())
    # fps_text = font.render(f"FPS: {fps}", True, "#000000")   
    # window.blit(fps_text, (10, 10))
    
    keys = pygame.key.get_pressed()
    player.move_player(keys, player.player_pos, player.player_speed, dt)
    
    if player.current_sprite:
        window.blit(player.current_sprite, (player.player_pos[0], player.player_pos[1]))
    # Update the display
    pygame.display.update()


# Quit Pygame
pygame.quit()
sys.exit()