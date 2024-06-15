import pygame
from Helpers import load_image

class Coin:
    def __init__(self, x, y):
        self.image = load_image('coin.png', colorkey=(0, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collected = False

    def draw(self, game_display, camera):
        if not self.collected:
            rect = self.rect.copy()
            rect.top -= camera.y
            game_display.blit(self.image, rect)
