import pygame

class ImageButton():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

class TextButton:
    def __init__(self, x, y, text, font, text_color, button_color, scale):
        self.font = font
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.scale = scale

        # Render the text to get the size
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (x, y)

        # Create a button rect around the text
        width = self.text_rect.width * self.scale
        height = self.text_rect.height * self.scale
        self.rect = pygame.Rect(self.text_rect.centerx - width // 2, self.text_rect.centery - height // 2, width, height)

        self.clicked = False

    def draw(self, surface):
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw the button background
        pygame.draw.rect(surface, self.button_color, self.rect)

        # Draw the text on top of the button
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        surface.blit(self.text_surface, text_rect)

        return action