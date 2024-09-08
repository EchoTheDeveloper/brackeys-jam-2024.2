import pygame
import game
import config as cfg
import math

# Set up player variables
player_pos = [cfg.WINDOW_HEIGHT // 2, cfg.WINDOW_WIDTH // 2]
player_speed = cfg.PLAYER_SPEED

def move_player(keys, pos, speed):
    x, y = pos
    dx, dy = 0, 0
    
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx -= 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx += 1
    if keys[pygame.K_UP] or keys[pygame.K_s]:
        dy -= 1
    if keys[pygame.K_DOWN] or keys[pygame.K_w]:
        dy += 1
    
    length = math.sqrt(dx**2 + dy**2)
    if length != 0:
        dx /= length
        dy /= length
        
    pos[0] += dx * speed
    pos[1] += dy * speed