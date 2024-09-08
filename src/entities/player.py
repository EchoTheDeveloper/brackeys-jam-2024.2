import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config as cfg
import pygame
import math

SCALING_FACTOR = 8

def get_animated_sprites_from_sheet(sheet, sprite_width, sprite_height, sprite_positions, num_frames, idle_frames=1):
    sprites = {}
    for direction, row in sprite_positions.items():
        direction_sprites = []
        # Add idle frame
        rect = pygame.Rect(0, row * sprite_height, sprite_width, sprite_height)
        idle_frame = sheet.subsurface(rect)
        # Scale idle frame
        idle_frame = pygame.transform.scale(idle_frame, (sprite_width * SCALING_FACTOR, sprite_height * SCALING_FACTOR))
        direction_sprites.append(idle_frame)

        # Add animation frames
        for i in range(1, num_frames + 1):
            rect = pygame.Rect(i * sprite_width, row * sprite_height, sprite_width, sprite_height)
            frame = sheet.subsurface(rect)
            # Scale each frame
            frame = pygame.transform.scale(frame, (sprite_width * SCALING_FACTOR, sprite_height * SCALING_FACTOR))
            direction_sprites.append(frame)
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
num_frames = 6
idle_frames = 1

sprite_sheet = pygame.image.load(os.path.join('resources', 'textures', 'entities', 'GuyWalk.png')).convert_alpha()

# Use the original sprite dimensions for extraction
sprite_width = 15
sprite_height = 15

# Get the animated sprites, then scale them individually
player_sprites = get_animated_sprites_from_sheet(sprite_sheet, sprite_width, sprite_height, sprite_positions, num_frames, idle_frames)
# Set up player variables
player_pos = [cfg.WINDOW_HEIGHT // 2, cfg.WINDOW_WIDTH // 2]
player_speed = cfg.PLAYER_SPEED

# Global variables
current_sprite = None
current_frame = 0
frame_rate = 15  # Number of frames per second can u do git pull
frame_timer = 0
last_direction = "S"  # Initialize last_direction to a default value (e.g., "S" for south)

def move_player(keys, pos, speed, dt):
    global current_sprite, current_frame, frame_timer, last_direction

    x, y = pos
    dx, dy = 0, 0
    moving = False  # Flag to check if player is moving

    # Check movement keys
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx -= 1
        moving = True
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx += 1
        moving = True
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy += 1
        moving = True
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy -= 1
        moving = True

    length = math.sqrt(dx**2 + dy**2)
    if length != 0:
        dx /= length
        dy /= length

    # Update position
    pos[0] += dx * speed
    pos[1] += dy * speed

    # Determine direction based on movement
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
        direction = "N"
    else:
        direction = last_direction  # If no movement, use last direction

    # Update last direction if moving
    if moving:
        last_direction = direction

    # Ensure direction is valid
    if direction is None or direction not in player_sprites:
        direction = last_direction  # Fallback to last direction if current is invalid

    # Update sprite frame
    if direction and direction in player_sprites:
        if moving:
            current_sprite = player_sprites[direction][current_frame]
        else:
            current_sprite = player_sprites[direction][0]  # Idle frame (first frame)
    else:
        # Fallback to idle frame if direction is invalid
        direction = last_direction if last_direction else "S"  # Use a default direction if last_direction is also None
        current_sprite = player_sprites.get(direction, [player_sprites["S"][0]])[0]  # Default to "S" idle frame if everything fails

    # Update animation frame if moving
    frame_timer += dt
    if moving and frame_timer >= 1 / frame_rate:
        frame_timer = 0
        current_frame = (current_frame + 1) % len(player_sprites[direction])
