import pygame
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((cfg.WINDOW_HEIGHT, cfg.WINDOW_WIDTH))

base_dir = os.path.dirname(os.path.abspath(__file__))
tmx_path = os.path.join(base_dir, '..', '..', 'resources', 'tilemaps', 'test.tmx')

# Load the TMX file using the absolute path
tmx_data = load_pygame(tmx_path)
sprite_group = pygame.sprite.Group()


Ground = tmx_data.get_layer_by_name('Ground')
Front = tmx_data.get_layer_by_name('Front')
Front2 = tmx_data.get_layer_by_name('Front2')

Collision = tmx_data.get_layer_by_name('Collision')
Interact = tmx_data.get_layer_by_name('Interact')

TILE_SCALE_FACTOR = 2

# Cycle through all layers
for layer in tmx_data.visible_layers:
    if layer.name in cfg.LAYERS:
        for x, y, surf in layer.tiles():
            pos = (x * 16, y * 16)
            scaled_surf = pygame.transform.scale(surf, ((surf.get_width() * TILE_SCALE_FACTOR), (surf.get_height() * TILE_SCALE_FACTOR)))
            Tile(pos = pos, surf = scaled_surf, groups = sprite_group)
    for obj in tmx_data.objects:
        pos = obj.x, obj.y
        surf = obj.image
        if obj.image:
            scaled_surf = pygame.transform.scale(surf, (surf.get_width() * TILE_SCALE_FACTOR), (surf.get_height() * TILE_SCALE_FACTOR))
            Tile(pos = pos, surf = scaled_surf, groups = sprite_group)



# Set window title and translation language
pygame.display.set_caption(key.ROOT_TITLE)

# Import after pygame init and window mode set
import src.entities.player as player

font = pygame.font.SysFont(None, 36)

# Clock for controlling the frame rate
CLOCK = pygame.time.Clock()


object_colliders = [pygame.Rect(obj.x, obj.y, obj.width * TILE_SCALE_FACTOR, obj.height * TILE_SCALE_FACTOR)
                    for obj in tmx_data.objects if obj.name in ['COL', 'DLG', 'TREE']]


# Initialize flags
# Initialize flags
dialogue_printed = False
dialogue_active = False
right_click_pressed = False

# Main game loop
# Main game loop
running = True
while running:
    dt = CLOCK.tick(cfg.DEFAULT_FPS) / 1000

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                cfg.DEBUG = not cfg.DEBUG
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if dialogue_active and event.button == 1:  # Left mouse button
                dialogue_active = False
                player.can_move = True

    LEFTCLICK, MIDDLECLICK, RIGHTCLICK = pygame.mouse.get_pressed(3)
    MOUSE_POS = pygame.mouse.get_pos()
    MOUSE_RECT = pygame.Rect(0, 0, 25, 25)
    MOUSE_RECT.center = MOUSE_POS

    DIALOGUE_RECT = pygame.Rect(0, 0, 25, 25)
    DIALOGUE_OUTPUT = ''
    DIALOGUE_SPEAKER = ''

    keys = pygame.key.get_pressed()
    player.move_player(keys, player.player_pos, player.player_speed, dt, object_colliders)

    window.fill(colors.pastel_green)  # Fill the background color

    # Draw game elements
    sprite_group.draw(window)  # Draw tiles and other sprites

    for obj in tmx_data.objects:
        pos = obj.x, obj.y
        surf = obj.image
        if obj.name == 'COL':
            if cfg.DEBUG:
                pygame.draw.rect(window, 'Red',
                                 (obj.x, obj.y, obj.width * TILE_SCALE_FACTOR, obj.height * TILE_SCALE_FACTOR), 0)
        if obj.name == 'DLG':
            DIALOGUE_RECT = pygame.Rect(obj.x, obj.y, obj.width * TILE_SCALE_FACTOR, obj.height * TILE_SCALE_FACTOR)
            DIALOGUE_OUTPUT = obj.properties['Dialogue']
            try:
                DIALOGUE_SPEAKER = obj.properties['Speaker']
            except:
                pass
            if cfg.DEBUG:
                pygame.draw.rect(window, 'Blue', DIALOGUE_RECT, 0)
        if obj.name == 'TREE':
            if cfg.DEBUG:
                pygame.draw.rect(window, 'Green',
                                 (obj.x, obj.y, obj.width * TILE_SCALE_FACTOR, obj.height * TILE_SCALE_FACTOR), 0)

    # Draw player sprite
    if player.current_sprite:
        window.blit(player.current_sprite, (player.player_pos[0], player.player_pos[1]))

    # Handle right-click for dialogue activation
    if MOUSE_RECT.colliderect(DIALOGUE_RECT):
        if RIGHTCLICK:
            dialogue_active = True

    if dialogue_active:
        if DIALOGUE_SPEAKER == '':
            DIALOGUE_SPEAKER = "TEST"
        d.draw_dialogue_box(DIALOGUE_OUTPUT, DIALOGUE_SPEAKER, font, window, cfg.WINDOW_HEIGHT // 2, cfg.WINDOW_WIDTH // 2, 400)
        player.can_move = False

    if MOUSE_RECT.colliderect(DIALOGUE_RECT) and cfg.DEBUG:
        pygame.draw.rect(window, 'Red', MOUSE_RECT)
    elif cfg.DEBUG and not MOUSE_RECT.colliderect(DIALOGUE_RECT):
        pygame.draw.rect(window, 'Green', MOUSE_RECT)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
