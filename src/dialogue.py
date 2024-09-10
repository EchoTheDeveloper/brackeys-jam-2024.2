import pygame
import sys


def draw_dialogue_box(text, speaker, font, screen, x, y, width):
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x, y+200))
    speaker_surface = font.render(speaker, True, (255, 255, 255))
    speaker_rect = speaker_surface.get_rect(center=(x-143, y+155))
    pygame.draw.rect(surface=screen, color=(0, 0, 0), rect=(x - width // 2, y+130, width, 100))
    screen.blit(text_surface, text_rect)
    screen.blit(speaker_surface, speaker_rect)
