import pygame
import os
import datetime
from Camera import Camera
from Player import Player
from Block import Block
from BlockManager import BlockManager
from Constants import *
from Helpers import *

pygame.init()

# Initialize the mixer module
pygame.mixer.init()

# Load music
music_file = os.path.join(os.getcwd(), "sound/music.mp3")
pygame.mixer.music.load(music_file)

# Load sound effects
jump_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), "sound/jump.wav"))
land_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), "sound/land.wav"))
achievement_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), "sound/achievement.wav"))
gameover_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), "sound/gameover.wav"))
coin_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), "sound/coin.wav"))
purchase_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), "sound/purchase.wav"))

# Start music
pygame.mixer.music.play(-1)

game_display = pygame.display.set_mode(res)
pygame.display.set_caption(GAME_CAPTION)

# Load and set window icon
icon_image = load_image('icon.png')
pygame.display.set_icon(icon_image)

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (177, 5, 14)

# Settings
music_enabled = True
sound_enabled = True

# Initialize game objects
def reinit(previous_state=None):
	global player, block_manager, floor, camera
	if previous_state:
		coins, jump_boosts, extra_lives = previous_state
	else:
		coins, jump_boosts, extra_lives = load_player_data("player_data.xml")

	player = Player(jump_sound if sound_enabled else None,
					land_sound if sound_enabled else None,
					achievement_sound if sound_enabled else None,
					coins=coins, jump_boosts=jump_boosts, extra_lives=extra_lives)
	player.achievements.load_achievements()
	player.set_color_from_achievements()
	block_manager = BlockManager(coin_sound, sound_enabled)
	floor = Block(0, SCREEN_HEIGHT - 36, SCREEN_WIDTH, 36)
	camera = Camera(player)

reinit()

# Load resources
arrow_image = load_image("arrow.png")
arrow_image.set_colorkey(black)
Sky = load_image('Sky.jpg')
title_image = load_image('logo.png')
title_image.set_colorkey(black)

# Game variables
selected_option = 0.30
game_state = 'Menu'
game_loop = True
clock = pygame.time.Clock()
fps = 60
ACHIEVEMENTS = 'Achievements'
SETTINGS = 'Settings'
HIGHSCORES = 'Highscores'
STORE_OPTIONS = ["JUMP BOOST 5 Coins", "EXTRA LIFE 10 Coins", "Confirm purchase"]
JUMP_BOOST_COST = 5
EXTRA_LIFE_COST = 10
settings_selected_option = 0.40

highscores = []

store_selected_option = 0
store_items = {"JUMP BOOST": 0, "EXTRA LIFE": 0}

def load_highscores():
	global highscores
	if os.path.exists("highscores.html"):
		with open("highscores.html", "r") as file:
			highscores = []
			lines = file.readlines()
			for line in lines[1:]:
				try:
					score, date = line.strip().split(',')
					highscores.append((int(score), date))
				except ValueError:
					continue

def save_highscore(score):
	date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	highscores.append((score, date))
	highscores.sort(key=lambda x: x[0], reverse=True)  # Sort by score

	with open("highscores.html", "w") as file:
		file.write("<html><body><h1>Highscores</h1><table border='1'>")
		file.write("<tr><th>Score</th><th>Date</th></tr>")
		for score, date in highscores:
			file.write(f"<tr><td>{score}</td><td>{date}</td></tr>")
		file.write("</table></body></html>")

load_highscores()

def handle_events():
	global game_loop, game_state, selected_option, music_enabled, sound_enabled, settings_selected_option, store_selected_option

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_loop = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if game_state in ['Playing', 'Game Over', 'About', ACHIEVEMENTS, SETTINGS, HIGHSCORES, 'Store']:
					game_state = 'Menu'
			elif game_state == 'Game Over' and event.key == pygame.K_RETURN:
				game_state = 'Store'
			elif game_state == 'Game Over' and event.key == pygame.K_SPACE:
				previous_state = (player.coins, player.jump_boosts, player.extra_lives)
				reinit(previous_state)
				game_state = 'Playing'
			elif game_state == 'Menu':
				handle_menu_events(event)
			elif game_state == SETTINGS:
				handle_settings_events(event)
			elif game_state == 'Store':
				handle_store_events(event)

def handle_menu_events(event):
	global selected_option, game_state, game_loop
	if event.key == pygame.K_DOWN:
		selected_option = 0.30 if selected_option >= 0.65 else selected_option + 0.10
	elif event.key == pygame.K_UP:
		selected_option = 0.70 if selected_option <= 0.35 else selected_option - 0.10
	elif event.key == pygame.K_RETURN:
		if selected_option < 0.35:
			previous_state = (player.coins, player.jump_boosts, player.extra_lives)
			reinit(previous_state)
			game_state = 'Playing'
		elif selected_option == 0.40:
			game_state = HIGHSCORES
		elif selected_option == 0.50:
			game_state = ACHIEVEMENTS
		elif selected_option == 0.60:
			game_state = SETTINGS
		elif selected_option == 0.70:
			game_loop = False

def handle_settings_events(event):
	global music_enabled, sound_enabled, settings_selected_option
	if event.key == pygame.K_DOWN:
		settings_selected_option = 0.50 if settings_selected_option == 0.40 else 0.40
	elif event.key == pygame.K_UP:
		settings_selected_option = 0.40 if settings_selected_option == 0.50 else 0.50
	elif event.key == pygame.K_RETURN:
		if settings_selected_option == 0.40:
			music_enabled = not music_enabled
			if music_enabled:
				pygame.mixer.music.play(-1)
			else:
				pygame.mixer.music.stop()
		elif settings_selected_option == 0.50:
			sound_enabled = not sound_enabled
			reinit()

def handle_store_events(event):
	global store_selected_option, store_items, game_state
	if event.key == pygame.K_DOWN:
		store_selected_option = (store_selected_option + 1) % len(STORE_OPTIONS)
	elif event.key == pygame.K_UP:
		store_selected_option = (store_selected_option - 1) % len(STORE_OPTIONS)
	elif event.key == pygame.K_RETURN:
		if store_selected_option == 0:  # Jump Boost
			if player.coins >= JUMP_BOOST_COST:
				store_items["JUMP BOOST"] += 1
				player.coins -= JUMP_BOOST_COST
		elif store_selected_option == 1:  # Extra Life
			if player.coins >= EXTRA_LIFE_COST:
				store_items["EXTRA LIFE"] += 1
				player.coins -= EXTRA_LIFE_COST
		elif store_selected_option == 2:  # Confirm purchase
			player.jump_boosts += store_items["JUMP BOOST"]
			player.extra_lives += store_items["EXTRA LIFE"]
			store_items = {"JUMP BOOST": 0, "EXTRA LIFE": 0}
			game_state = 'Game Over'
			if sound_enabled:
				purchase_sound.play()

def update_player(keys_pressed):
	if keys_pressed[pygame.K_LEFT]:
		player.vel_x = max(player.vel_x - player.acceleration, -player.max_vel_x)
		player.sprite_index_y = 2
	elif keys_pressed[pygame.K_RIGHT]:
		player.vel_x = min(player.vel_x + player.acceleration, player.max_vel_x)
		player.sprite_index_y = 1
	else:
		player.vel_x += (player.acceleration if player.vel_x < 0 else -player.acceleration)
		player.vel_x = max(0, player.vel_x - GRASS_RESISTANCE) if player.vel_x < 0 else min(0, player.vel_x + GRASS_RESISTANCE)

		if player.vel_y >= JUMP_VELOCITY / 2:
			player.sprite_index_y = 0

	if keys_pressed[pygame.K_SPACE] and player.on_any_block(block_manager, floor):
		player.sprite_index_y = 3
		if player.vel_y >= JUMP_VELOCITY / 2:
			player.jump()
	if keys_pressed[pygame.K_UP]:
		player.use_jump_boost()

def game_loop():
	global game_state

	while game_loop:
		handle_events()

		keys_pressed = pygame.key.get_pressed()
		if game_state == 'Playing':
			update_player(keys_pressed)
			player.update()
			player.combo()
			player.collide_block(floor, 0)
			block_manager.collide_set(player)

			block_manager.score = player.score
			camera.update(player.score)
			block_manager.generate_new_blocks(camera)

			if player.fallen_off_screen(camera):
				if player.use_extra_life():
					player.y = camera.y - 50
				else:
					game_state = 'Game Over'
					save_highscore(player.score)
					if sound_enabled:
						gameover_sound.play()

		draw()

		pygame.display.update()
		clock.tick(fps)

	player.achievements.save_achievements()
	player.save_data()

def draw():
	if game_state == 'Menu':
		draw_menu()
	elif game_state == 'Playing':
		draw_playing()
	elif game_state == 'Game Over':
		draw_game_over()
	elif game_state == ACHIEVEMENTS:
		draw_achievements()
	elif game_state == SETTINGS:
		draw_settings()
	elif game_state == HIGHSCORES:
		draw_highscores()
	elif game_state == 'Store':
		draw_store()

def draw_menu():
	game_display.blit(Sky, (0, 0))
	title_image_rect = title_image.get_rect(center=(SCREEN_WIDTH // 2, 150))
	game_display.blit(title_image, title_image_rect)
	game_display.blit(arrow_image, (MENU_START_X + ARROW_HALF_WIDTH, MENU_START_Y + SCREEN_HEIGHT * selected_option - ARROW_HALF_HEIGHT))
	if pygame.font:
		message_display(game_display, "Play", 0, MENU_START_Y + round(SCREEN_HEIGHT * 0.30), 50, red, True)
		message_display(game_display, "Highscores", 0, MENU_START_Y + round(SCREEN_HEIGHT * 0.40), 50, red, True)
		message_display(game_display, "Achievements", 0, MENU_START_Y + round(SCREEN_HEIGHT * 0.50), 50, red, True)
		message_display(game_display, "Settings", 0, MENU_START_Y + round(SCREEN_HEIGHT * 0.60), 50, red, True)
		message_display(game_display, "Quit", 0, MENU_START_Y + round(SCREEN_HEIGHT * 0.70), 50, red, True)

def draw_playing():
	game_display.blit(Sky, (0, 0))
	floor.draw(game_display, camera)
	block_manager.draw(game_display, camera)
	player.draw(game_display, camera)
	message_display(game_display, str(player.score), 25, 30, 36, red)

def draw_game_over():
	game_display.blit(Sky, (0, 0))
	if pygame.font:
		message_display(game_display, "GAME OVER", 0, 200, 70, red, True)
		message_display(game_display, "Score: %d" % player.score, 0, 300, 50, red, True)
		message_display(game_display, "Coins: %d" % player.coins, 0, 350, 50, red, True)
		message_display(game_display, "Press SPACE to play again", 0, 400, 50, red, True)
		message_display(game_display, "Press ENTER to go to the store", 0, 450, 50, red, True)
		message_display(game_display, "Press ESC to return to menu", 0, 500, 50, red, True)

def draw_achievements():
	game_display.blit(Sky, (0, 0))
	if pygame.font:
		achievements = player.achievements.get_achievements()
		for index, (key, achievement) in enumerate(achievements.items()):
			status = "Unlocked" if achievement["unlocked"] else "Locked"
			message_display(game_display, f"{achievement['description']}: {status}", 0, MENU_START_Y + index * 35, 30, achievement["color"], True)
		message_display(game_display, "Press ESC to return to menu!", 160, 20, 40, red, True)

def draw_settings():
	global settings_selected_option
	game_display.blit(Sky, (0, 0))
	if pygame.font:
		message_display(game_display, "Settings", 0, 100, 60, red, True)
		message_display(game_display, f"Music: {'On' if music_enabled else 'Off'}", 0, 200, 50, red, True)
		message_display(game_display, f"Sound: {'On' if sound_enabled else 'Off'}", 0, 250, 50, red, True)
		message_display(game_display, "Press ESC to return to menu!", 0, 500, 40, red, True)

	# Calculate arrow position based on selected option
	arrow_y_positions = [200, 250]
	selected_index = 0 if settings_selected_option == 0.40 else 1
	arrow_y_position = arrow_y_positions[selected_index]

	game_display.blit(arrow_image, (MENU_START_X + ARROW_HALF_WIDTH, arrow_y_position - ARROW_HALF_HEIGHT))

def draw_highscores():
	game_display.blit(Sky, (0, 0))
	if pygame.font:
		message_display(game_display, "Highscores", 0, 100, 60, red, True)
		latest_highscores = highscores[:8]
		for index, (score, date) in enumerate(latest_highscores):
			message_display(game_display, f"{score} on {date}", 0, 200 + index * 35, 30, red, True)
		message_display(game_display, "Press ESC to return to menu!", 0, 500, 40, red, True)

def draw_store():
	game_display.blit(Sky, (0, 0))
	message_display(game_display, "Store", 0, 50, 60, red, True)
	for i, option in enumerate(STORE_OPTIONS):
		color = red
		if i < 2:
			item_name = option.split()[0] + ' ' + option.split()[1]
			message_display(game_display, f"{option}: {store_items[item_name]}", 0, 150 + i * 50, 40, color, True)
		else:
			message_display(game_display, option, 0, 150 + i * 50, 40, color, True)
	message_display(game_display, f"Available Coins: {player.coins}", 0, 400, 40, red, True)
	message_display(game_display, "Press ESC to return to menu", 0, 500, 30, red, True)

	arrow_y_positions = [150 + i * 50 for i in range(len(STORE_OPTIONS))]
	arrow_y_position = arrow_y_positions[store_selected_option]

	arrow_x_position = MENU_START_X - 50

	game_display.blit(arrow_image, (arrow_x_position, arrow_y_position - ARROW_HALF_HEIGHT))

if __name__ == "__main__":
	game_loop()
	pygame.quit()
	quit()
