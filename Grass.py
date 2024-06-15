import pygame 
from Helpers import * 

class Grass(pygame.sprite.Sprite):
	image = None

	def __init__(self, location):
		pygame.sprite.Sprite.__init__(self)

		if Grass.image is None:
			Grass.image = load_image("Grass.png")
		
		self.image = Grass.image

		self.rect = self.image.get_rect()
		self.rect.topleft = location
