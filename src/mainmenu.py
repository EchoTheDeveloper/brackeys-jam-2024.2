import pygame
import sys
import src.colorlist as colors # manage list of colors easier instead of having a bunch of colors in code that are hardcoded
import src.translations as key
import src.config as cfg
import src.button as btn
import os
# Initialize Pygame
pygame.init()

window = pygame.display.set_mode((cfg.WINDOW_HEIGHT, cfg.WINDOW_WIDTH))

# Set window title and translation language
pygame.display.set_caption(key.ROOT_TITLE)

menu_state = "main"

# Clock for controlling the frame rate
CLOCK = pygame.time.Clock()

# Text stuff
TEXT_COLOR = (255, 255, 255)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    window.blit(img, (x, y))

# Set the font for text
# font = pygame.font.Font(pygame.font.match_font('calibri'), 30)
# play_button = btn.TextButton(320, 340, "Play", font, "#ffffff", "#000000", 1)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(project_root)

play_img = pygame.image.load("resources/textures/UI/MainMenu/play.png").convert_alpha()
play_button = btn.ImageButton(170, 100, play_img, 1)

quit_img = pygame.image.load("resources/textures/UI/MainMenu/quit.png").convert_alpha()
quit_button = btn.ImageButton(170, 350, quit_img, 1)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed

    # Fill window with background color
    window.fill(colors.cornflower_blue)

    if menu_state == "main":
        if play_button.draw(window):
            import src.game.level as lvl
        elif quit_button.draw(window):
            pygame.quit()
    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
