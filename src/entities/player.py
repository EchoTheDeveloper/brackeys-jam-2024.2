import pygame
import config as cfg
import math
import os

def get_animated_sprites_from_sheet(sheet, sprite_width, sprite_height, sprite_positions, num_frames, idle_frames=1):
    sprites = {}
    for direction, row in sprite_positions.items():
        direction_sprites = []
        # Add idle frame
        rect = pygame.Rect(0, row * sprite_height, sprite_width, sprite_height)
        direction_sprites.append(sheet.subsurface(rect))
        # Add animation frames
        for i in range(1, num_frames + 1):
            rect = pygame.Rect(0, row * sprite_height + i * sprite_height, sprite_width, sprite_height)
            direction_sprites.append(sheet.subsurface(rect))
        sprites[direction] = direction_sprites
    return sprites

# Setup player sprites
sprite_positions = {
    "S": 0,
    "N": 1,
    "E": 2,
    "W": 3,
    "SE": 4,
    "SW": 5,
    "NE": 6,
    "NW": 7
}
num_frames = 7 # check dsicord
idle_frames = 1
# SPRITE SHEET LAYOUT 
# N1 N2 N3
#
sprite_sheet = pygame.image.load(os.path.join('resources', 'textures', 'entities', 'player.png')).convert_alpha()
                                                            #  VV  VV TEMPORARY SIZES
player_sprites = get_animated_sprites_from_sheet(sprite_sheet, 16, 16, sprite_positions, num_frames, idle_frames)
# Set up player variables
player_pos = [cfg.WINDOW_HEIGHT // 2, cfg.WINDOW_WIDTH // 2]
player_speed = cfg.PLAYER_SPEED

current_sprite = None
current_frame = 0
frame_rate = 10  # Number of frames per second
frame_timer = 0

def move_player(keys, pos, speed, dt):
    global current_sprite, current_frame, frame_timer

    x, y = pos
    dx, dy = 0, 0

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx -= 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx += 1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy += 1
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy -= 1

    length = math.sqrt(dx**2 + dy**2)
    if length != 0:
        dx /= length
        dy /= length

    pos[0] += dx * speed
    pos[1] += dy * speed

    # Determine direction
    if dx > 0 and dy > 0:
        direction = "SE"
    elif dx > 0 and dy < 0:
        direction = "NE"
    elif dx < 0 and dy > 0:
        direction = "SW"
    elif dx < 0 and dy < 0:
        direction = "NW"
    elif dx > 0:
        direction = "E"
    elif dx < 0:
        direction = "W"
    elif dy > 0:
        direction = "S"
    elif dy < 0:
        direction = "W"
    else:
        direction = None  # Idle state

    # Update sprite frame
    if direction and direction in player_sprites:
        current_sprite = player_sprites[direction][current_frame]
    elif direction is None:
        # Set idle frame
        for dir_key in sprite_positions:
            if current_sprite in player_sprites[dir_key]:
                direction = dir_key
                break
        current_sprite = player_sprites[direction][0]  # Idle frame

    frame_timer += dt
    if direction and frame_timer >= 1 / frame_rate:
        frame_timer = 0
        current_frame = (current_frame + 1) % len(player_sprites[direction])