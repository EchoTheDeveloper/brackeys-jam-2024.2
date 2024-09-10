import pygame
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src.colorlist as colors
import src.config as cfg
import src.dialogue as d
import src.translations as key
from pytmx.util_pygame import load_pygame

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((cfg.WINDOW_HEIGHT, cfg.WINDOW_WIDTH))

# Load the TMX file
base_dir = os.path.dirname(os.path.abspath(__file__))
tmx_path = os.path.join(base_dir, '..', '..', 'resources', 'tilemaps', 'test.tmx')
tmx_data = load_pygame(tmx_path)
sprite_group = pygame.sprite.Group()

TILE_SCALE_FACTOR = 2

# Initialize sprite layers
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
import src.entities.player as player

font = pygame.font.SysFont(None, 36)
CLOCK = pygame.time.Clock()

# Store all dialogue objects
dialogue_objects = [
    {
        'rect': pygame.Rect(obj.x, obj.y, obj.width * TILE_SCALE_FACTOR, obj.height * TILE_SCALE_FACTOR),
        'dialogue': obj.properties.get('Dialogue', ''),
        'speaker': obj.properties.get('Speaker', 'TEST')
    }
    for obj in tmx_data.objects if obj.name == 'DLG'
]

# Initialize flags and variables
dialogue_active = False
current_dialogue = None  # Store the current dialogue object

running = True
while running:
    dt = CLOCK.tick(cfg.DEFAULT_FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right-click
            for dialogue_obj in dialogue_objects:
                if dialogue_obj['rect'].collidepoint(event.pos):
                    dialogue_active = True
                    current_dialogue = dialogue_obj
                    player.can_move = False
                    break
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left-click
            if dialogue_active:
                dialogue_active = False
                current_dialogue = None
                player.can_move = True

    LEFTCLICK, MIDDLECLICK, RIGHTCLICK = pygame.mouse.get_pressed(3)
    MOUSE_POS = pygame.mouse.get_pos()

    keys = pygame.key.get_pressed()
    player.move_player(keys, player.player_pos, player.player_speed, dt, object_colliders)

    window.fill(colors.pastel_green)

    # Draw tiles and sprites
    sprite_group.draw(window)

    if cfg.DEBUG:
        for obj in tmx_data.objects:
            if obj.name == 'COL':
                pygame.draw.rect(window, 'Red', pygame.Rect(obj.x, obj.y, obj.width * TILE_SCALE_FACTOR, obj.height * TILE_SCALE_FACTOR), 0)
            elif obj.name == 'DLG':
                pygame.draw.rect(window, 'Blue', pygame.Rect(obj.x, obj.y, obj.width * TILE_SCALE_FACTOR, obj.height * TILE_SCALE_FACTOR), 0)
            elif obj.name == 'TREE':
                pygame.draw.rect(window, 'Green', pygame.Rect(obj.x, obj.y, obj.width * TILE_SCALE_FACTOR, obj.height * TILE_SCALE_FACTOR), 0)

    if player.current_sprite:
        window.blit(player.current_sprite, (player.player_pos[0], player.player_pos[1]))

    # Handle active dialogue
    if dialogue_active and current_dialogue:
        d.draw_dialogue_box(
            current_dialogue['dialogue'],
            current_dialogue['speaker'],
            font,
            window,
            cfg.WINDOW_HEIGHT // 2,
            cfg.WINDOW_WIDTH // 2,
            400
        )

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
