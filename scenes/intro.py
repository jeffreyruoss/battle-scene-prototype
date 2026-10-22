#!/usr/bin/python
import pygame
import pygame.mixer
from modules import cursor
from modules import scene_fade
import development


class IntroScene(object):
	def __init__(self, game):
		self.active = False
		self.background = ''
		music_path = development.Path.root + 'sounds/intro_loop.wav'
		self.music = pygame.mixer.Sound(music_path)
		self.layer_1 = pygame.sprite.Group()
		self.layer_2 = pygame.sprite.Group()
		self.layer_3 = pygame.sprite.Group()
		self.cursor_sprite_group = pygame.sprite.Group()
		self.fade_sprite_group = pygame.sprite.Group()

	def events(self, event, game):
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # for testing
			print 'doing stuff on the intro game stage'
		# Start
		elif self.start.rect.collidepoint(pygame.mouse.get_pos()) and \
			event.type == pygame.MOUSEBUTTONDOWN and \
			event.button == 1:
				self.start_sound.play()
				pygame.time.wait(750)
				game.scene_selector.load_scene(game, 'battle')
		# How to Play
		elif self.how_to_play.rect.collidepoint(pygame.mouse.get_pos()) and \
			event.type == pygame.MOUSEBUTTONDOWN and \
			event.button == 1:
				self.start.kill()
				self.how_to_play.kill()
				self.quit.kill()
				self.load_how_to_play_info(game)
		# Quit
		elif self.quit.rect.collidepoint(pygame.mouse.get_pos()) and \
			event.type == pygame.MOUSEBUTTONDOWN and \
			event.button == 1:
				self.start_sound.play()
				pygame.time.wait(750)
				game.running = False;
		# How to Play back button
		elif hasattr(self, 'how_to_play_back') and \
			self.how_to_play_back.rect.collidepoint(pygame.mouse.get_pos()) and \
			event.type == pygame.MOUSEBUTTONDOWN and \
			event.button == 1:
				self.load_how_to_play_close()
				self.load_menu(game)

	def staging(self, game): # runs once when this scene is initiated
		self.cursor = cursor.Cursor(game)
		self.load_background(game)
		self.load_logo(game)
		self.load_menu(game)
		self.scene_fade = scene_fade.SceneFade(self, 10)
		start_sound_path = development.Path.root + "sounds/start_game.wav"
		self.start_sound = pygame.mixer.Sound(start_sound_path)
		battle_cry_sound_path = development.Path.root + "sounds/battle_cry.wav"
		self.battle_cry_sound = pygame.mixer.Sound(battle_cry_sound_path)
		self.battle_cry_sound.play()

	def update(self, game):
		self.fade_sprite_group.update()
		self.layer_1.update()
		self.layer_2.update()
		self.layer_3.update()
		self.cursor_sprite_group.update()

	def load_background(self, game):
		if self.background == '':
			background_path = development.Path.root + 'images/background-intro.jpg'
			self.background = pygame.image.load(background_path).convert()
			game.screen.blit(self.background, (0, 0))
		else:
			game.screen.blit(self.background, (0, 0))

	def load_logo(self, game):
		self.logo = Logo(game)

	def load_menu(self, game):
		start_y = 500
		# options_y = 540
		how_to_play_y = 540
		quit_y = 580
		self.start = MenuButton(game, 'Start', start_y)
		# self.options = MenuButton(game, 'Options', options_y)
		self.how_to_play = MenuButton(game, 'How To Play', how_to_play_y)
		self.quit = MenuButton(game, 'Quit', quit_y)

	def load_how_to_play_info(self, game):
		white = (255, 255, 255)
		gray = (120, 120, 120)
		self.how_to_play_screenshot = HowToPlayScreenshot(game)
		self.how_to_play_text_1 = Text(game, '1. The action menu is on the right.', 410, white)
		self.how_to_play_text_2 = Text(game, '    Use the mouse to choose what actions', 440, white)
		self.how_to_play_text_3 = Text(game, '    each of your characters will do.', 470, white)
		self.how_to_play_text_4 = Text(game, '2. A characters can act when', 530, white)
		self.how_to_play_text_5 = Text(game, '    their action bar is full', 560, white)
		self.how_to_play_text_6 = Text(game, 'Don\'t get dead!', 620, white)
		self.how_to_play_back = Text(game, 'BACK', 680, gray)

	def load_how_to_play_close(self):
		self.how_to_play_screenshot.kill()
		self.how_to_play_text_1.kill()
		self.how_to_play_text_2.kill()
		self.how_to_play_text_3.kill()
		self.how_to_play_text_4.kill()
		self.how_to_play_text_5.kill()
		self.how_to_play_text_6.kill()
		self.how_to_play_back.kill()


class Logo(pygame.sprite.Sprite):
	def __init__(self, game):
		pygame.sprite.Sprite.__init__(self)
		logo_image_path = development.Path.root + 'images/logo.png'
		self.image = pygame.image.load(logo_image_path).convert_alpha()
		x = 390
		y = 150
		self.rect = (x, y)
		self.add(game.scene_selector.scene.layer_2)		


class MenuButton(pygame.sprite.Sprite):
	def __init__(self, game, text, y):
		pygame.sprite.Sprite.__init__(self)
		self.font_type = development.Path.root + 'font/8-bit Madness.ttf'
		font_size = 40
		self.font = pygame.font.Font(self.font_type, font_size)
		self.image = self.font.render(text, False, (255, 255, 255, 0))
		self.rect = self.image.get_rect()
		self.rect.top = y
		self.rect.centerx = game.screen.get_width() / 2
		self.add(game.scene_selector.scene.layer_2)


class Text(pygame.sprite.Sprite):
	def __init__(self, game, text, y, color):
		pygame.sprite.Sprite.__init__(self)
		self.font_type = development.Path.root + 'font/8-bit Madness.ttf'
		font_size = 28
		self.font = pygame.font.Font(self.font_type, font_size)
		self.image = self.font.render(text, False, (color))
		self.rect = self.image.get_rect()
		self.rect.top = y
		self.rect.left = 690
		# self.rect.centerx = game.screen.get_width() / 2
		self.add(game.scene_selector.scene.layer_2)


class HowToPlayScreenshot(pygame.sprite.Sprite):
	def __init__(self, game):
		pygame.sprite.Sprite.__init__(self)
		logo_image_path = development.Path.root + 'images/how-to-play-screenshot.png'
		self.image = pygame.image.load(logo_image_path).convert_alpha()
		x = 50
		y = 400
		self.rect = (x, y)
		self.add(game.scene_selector.scene.layer_2)				