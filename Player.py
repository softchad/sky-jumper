# Player.py
import pygame
from Constants import GRAVITY, SCREEN_WIDTH, SCREEN_HEIGHT, JUMP_VELOCITY
from Helpers import load_image, message_display, save_player_data, load_player_data
from Achievements import Achievements

class Player:
	width = 30
	height = 50

	vel_x = 0
	vel_y = 0
	max_falling_speed = 20

	acceleration = 0.5
	max_vel_x = 7

	color = (255, 0, 0)
	speed = 5

	def __init__(self, jump_sound=None, land_sound=None, achievement_sound=None, coins=0, jump_boosts=0, extra_lives=0):
		self.x = 30
		self.y = 500
		self.score = -10

		# Initialize player data
		self.coins = coins
		self.jump_boosts = jump_boosts
		self.extra_lives = extra_lives

		self.spritesheet_images = [
			load_image(f'spritesheet_{i}.png') for i in range(1, 16)
		]
		for img in self.spritesheet_images:
			img.set_colorkey((0, 0, 0))

		self.spritesheet = []
		self.current_spritesheet = self.spritesheet_images[0]

		# Initialize sprites
		self.update_sprites(self.current_spritesheet)

		self.sprite_index_x = 0
		self.sprite_index_y = 0
		self.frame_counter = 0
		self.frame_delay = 9
		self.achievements = Achievements()

		# Sound effects
		self.jump_sound = jump_sound
		self.land_sound = land_sound
		self.achievement_sound = achievement_sound

	def update_sprites(self, spritesheet_image):
		self.spritesheet = []

		# Idle
		self.cropped = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
		self.cropped.blit(spritesheet_image, (0, 0), (0, 0, 33, 57))
		self.cropped2 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
		self.cropped2.blit(spritesheet_image, (0, 0), (37, 0, 33, 57))
		self.cropped3 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
		self.cropped3.blit(spritesheet_image, (0, 0), (75, 0, 33, 57))
		self.spritesheet.extend([self.cropped, self.cropped2, self.cropped3])

		# Going right
		self.cropped4 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
		self.cropped4.blit(spritesheet_image, (0, 0), (0, 56, 33, 57))
		self.cropped5 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
		self.cropped5.blit(spritesheet_image, (0, 0), (37, 56, 33, 57))
		self.cropped6 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
		self.cropped6.blit(spritesheet_image, (0, 0), (75, 56, 33, 57))
		self.spritesheet.extend([self.cropped4, self.cropped5, self.cropped6])

		# Going left
		self.spritesheet.extend([pygame.transform.flip(self.cropped4, True, False),
								 pygame.transform.flip(self.cropped5, True, False),
								 pygame.transform.flip(self.cropped6, True, False)])

		# Jumping
		self.cropped7 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
		self.cropped7.blit(spritesheet_image, (0, 0), (75, 112, 33, 57))
		self.spritesheet.extend([self.cropped7, self.cropped7, self.cropped7])

	def draw(self, game_display, camera):
		game_display.blit(self.spritesheet[self.sprite_index_y * 3 + self.sprite_index_x], (self.x, self.y - camera.y))

		self.frame_counter += 1
		if self.frame_counter >= self.frame_delay:
			self.sprite_index_x += 1
			if self.sprite_index_x > 2:
				self.sprite_index_x = 0
			self.frame_counter = 0

		# Display HUD
		hud_color = (177, 5, 14)
		message_display(game_display, f"COINS: {self.coins}", 780, 20, 24, hud_color, align_right=True)
		message_display(game_display, f"JUMP BOOST: {self.jump_boosts}", 780, 50, 24, hud_color, align_right=True)
		message_display(game_display, f"EXTRA LIFE: {self.extra_lives}", 780, 80, 24, hud_color, align_right=True)

	def jump(self):
		if self.vel_y >= JUMP_VELOCITY / 2:
			self.vel_y = -JUMP_VELOCITY
			if self.jump_sound:
				self.jump_sound.play()

	def update(self):
		self.x += self.vel_x
		self.y += self.vel_y

		self.vel_y += GRAVITY
		if self.vel_y > self.max_falling_speed:
			self.vel_y = self.max_falling_speed
		if self.x <= 0:
			self.x = 0
		if self.x + self.width >= SCREEN_WIDTH:
			self.x = SCREEN_WIDTH - self.width

		self.achievements.progress["score"] = self.score
		self.check_achievements()

	def check_achievements(self):
		initial_achievement = self.achievements.last_unlocked_achievement
		self.achievements.check_achievements()
		if self.achievements.last_unlocked_achievement != initial_achievement:
			if self.achievement_sound:
				self.achievement_sound.play()
		self.update_sprite_based_on_achievements()

	def update_sprite_based_on_achievements(self):
		unlocked_achievements = [key for key, value in self.achievements.get_achievements().items() if value["unlocked"]]
		if unlocked_achievements:
			highest_achievement = sorted(unlocked_achievements, key=lambda x: int(x.split('_')[1]))[-1]
			achievement_index = int(highest_achievement.split('_')[1]) // 100 - 1
			self.current_spritesheet = self.spritesheet_images[achievement_index]
			self.update_sprites(self.current_spritesheet)

	def combo(self):
		if self.x == 0:
			if self.vel_y < 0 and self.vel_x < 0:
				self.vel_y -= 10
				self.vel_x *= -2.5
		if self.x + self.width >= SCREEN_WIDTH:
			if self.vel_y < 0 and self.vel_x > 0:
				self.vel_y -= 10
				self.vel_x *= -2.5

	def on_block(self, block):
		return block.rect.collidepoint((self.x, self.y + self.height)) or \
			block.rect.collidepoint((self.x + self.width, self.y + self.height))

	def on_any_block(self, block_controller, floor):
		for p in block_controller.block_set:
			if self.on_block(p):
				return True
		if self.on_block(floor):
			return True
		return False

	def collide_block(self, block, index):
		for i in range(0, self.vel_y):
			if pygame.Rect(self.x, self.y - i, self.width, self.height).colliderect(block.rect):
				if block.rect.collidepoint((self.x, self.y + self.height - i)) or \
						block.rect.collidepoint((self.x + self.width, self.y + self.height - i)):
					self.y = block.y - self.height
					if not block.collected_score:
						self.score += 10
						if self.score < index * 10:
							self.score = index * 10
						block.collected_score = True
						if self.land_sound:
							self.land_sound.play()

	def get_rect(self):
		return pygame.Rect(self.x, self.y, self.width, self.height)

	def fallen_off_screen(self, camera):
		return self.y - camera.y + self.height >= SCREEN_HEIGHT

	def set_color_from_achievements(self):
		if self.achievements.last_unlocked_achievement:
			key = self.achievements.last_unlocked_achievement
			self.current_spritesheet = self.spritesheet_images[int(key.split('_')[1]) // 100 - 1]
			self.update_sprites(self.current_spritesheet)

	def use_jump_boost(self):
		if self.jump_boosts > 0:
			self.jump_boosts -= 1
			self.vel_y = -JUMP_VELOCITY * 3

	def use_extra_life(self):
		if self.extra_lives > 0:
			self.extra_lives -= 1
			return True
		return False

	def save_data(self):
		save_player_data("player_data.xml", self.coins, self.jump_boosts, self.extra_lives)
