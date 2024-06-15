import pygame
import math
from random import randrange, random, getrandbits
from Block import Block
from Constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAX_JUMP
from Coin import Coin

pygame.init()

class BlockManager:
	def __init__(self, coin_sound, sound_enabled):
		self.block_set = []
		self.index = 10
		self.last_x = MAX_JUMP
		self.score = 0
		self.coins = []
		self.coin_sound = coin_sound
		self.sound_enabled = sound_enabled
		self.generate_initial_platform()
		for i in range(1, self.index):
			self.block_set.append(self.generate_block(i, self.score, allow_coins=True))

	def generate_initial_platform(self):
		initial_block = Block(0, SCREEN_HEIGHT - 36, SCREEN_WIDTH, 36)
		self.block_set.append(initial_block)

	def generate_block(self, index, score, allow_coins=True):
		if score < MAX_JUMP * MAX_JUMP:
			change = int(math.sqrt(score))
		else:
			change = MAX_JUMP - 1
		width = 200 - randrange(change, change + 60)
		height = 20
		y = 600 - index * 100
		while True:
			side = bool(getrandbits(1))
			if side:
				x = randrange(self.last_x - MAX_JUMP, self.last_x - change)
			else:
				x = randrange(self.last_x + width + change, self.last_x + MAX_JUMP + width)
			if x >= 0 and x <= SCREEN_WIDTH - width:
				break
		self.last_x = x

		block = Block(x, y, width, height)

		if allow_coins and random() < 0.1:
			coin_x = x + (width // 2) - 10
			coin_y = y - 30
			self.coins.append(Coin(coin_x, coin_y))

		return block

	def draw(self, game_display, camera):
		for p in self.block_set:
			p.draw(game_display, camera)
		for coin in self.coins:
			coin.draw(game_display, camera)

	def collide_set(self, player):
		for i, p in enumerate(self.block_set):
			player.collide_block(p, i)
		for coin in self.coins:
			if not coin.collected and player.get_rect().colliderect(coin.rect):
				coin.collected = True
				player.coins += 1
				if self.sound_enabled:
					self.coin_sound.play()

	def generate_new_blocks(self, camera):
		if self.block_set[-1].y - camera.y > -50:
			for i in range(self.index, self.index + 10):
				self.block_set.append(self.generate_block(i, self.score))
			self.index += 10
