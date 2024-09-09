import pygame
import sys

dialogues = [
    {"speaker": "NPC", "text": "Hello, traveler!"},
    {"speaker": "Player", "text": "Hi there!"},
    {"speaker": "NPC", "text": "How can I help you today?"}
]

def draw_text_box(text, font, screen, x, y, width):
    print(text)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x, y))
    pygame.draw.rect(surface=screen, color=(0, 0, 0), rect=(x - width // 2, y - 50, width, 100))
    screen.blit(text_surface, text_rect)

def check_interaction(player, npcs):
    for npc in npcs:
        if player.rect.colliderect(npc.rect.inflate(100, 100)):  # Adjust interaction range
            return True
    return False