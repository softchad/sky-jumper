# Helpers.py
import pygame
from Constants import SCREEN_WIDTH, SCREEN_HEIGHT
import os
from pygame.locals import RLEACCEL
import xml.etree.ElementTree as ET

# Text
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(game_display, text, x, y, font_size, color, centered_x=False, centered_y=False, align_right=False):
    font = pygame.font.Font(None, font_size)
    TextSurf, TextRect = text_objects(text, font, color)
    if centered_x and centered_y:
        TextRect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    elif centered_x:
        TextRect.center = ((SCREEN_WIDTH / 2), y)
    elif centered_y:
        TextRect.center = (x, (SCREEN_HEIGHT / 2))
    elif align_right:
        TextRect.topright = (x, y)
    else:
        TextRect.center = (x, y)
    game_display.blit(TextSurf, TextRect)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print(f'Cannot load image: {name}')
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def save_player_data(filename, coins, jump_boosts, extra_lives):
    root = ET.Element("player_data")
    ET.SubElement(root, "coins").text = str(coins)
    ET.SubElement(root, "jump_boosts").text = str(jump_boosts)
    ET.SubElement(root, "extra_lives").text = str(extra_lives)

    tree = ET.ElementTree(root)
    tree.write(filename)

def load_player_data(filename):
    if not os.path.exists(filename):
        return 0, 0, 0

    tree = ET.parse(filename)
    root = tree.getroot()

    coins = int(root.find("coins").text)
    jump_boosts = int(root.find("jump_boosts").text)
    extra_lives = int(root.find("extra_lives").text)

    return coins, jump_boosts, extra_lives
