import pygame
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src.config as cfg
import src.colorlist as colors # manage list of colors easier instead of having a bunch of colors in code that are hardcoded
import src.config as cfg
import src.dialogue as d
import src.translations as key
from pytmx.util_pygame import load_pygame

try:
    os.chdir('../../')
    print(f'Changed to directory: {os.getcwd()}')
except OSError as e:
    print(f'Error: {e}')

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((cfg.WINDOW_HEIGHT, cfg.WINDOW_WIDTH))

base_dir = os.path.dirname(os.path.abspath(__file__))
tmx_path = os.path.join(base_dir, '..', '..', 'resources', 'tilemaps', 'test.tmx')

# Load the TMX file using the absolute path
tmx_data = load_pygame(tmx_path)

# print objs
for obj in tmx_data.objectgroups: print(obj)

Ground = tmx_data.get_layer_by_name('Ground')
Front = tmx_data.get_layer_by_name('Front')
Front2 = tmx_data.get_layer_by_name('Front2')

Collision = tmx_data.get_layer_by_name('Collision')
Interact = tmx_data.get_layer_by_name('Interact')

for col in Collision:
    if col.type == 'Shape':
        if obj.name == 'Rectangle':
            print(obj)


# Set window title and translation language
pygame.display.set_caption(key.ROOT_TITLE)

# Import after pygame init and window mode set
import src.entities.player as player

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