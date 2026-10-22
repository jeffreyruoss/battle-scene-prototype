#!/usr/bin/python
import pygame
import pygame.mixer
import development
pygame.mixer.init()


class Info(pygame.sprite.Sprite): # parent class for all text based sprites in this module
	def __init__(self, game):
		pygame.sprite.Sprite.__init__(self, game.scene_selector.scene.layer_2)

	def build(self, game):
		self.font_type = development.Path.root + 'font/8-bit Madness.ttf'
		self.font = pygame.font.Font(self.font_type, 35)
		self.image = self.font.render(self.text, 1, (255, 255, 255, 0))
		self.rect = self.image.get_rect()		


class NamePlayer(Info):
	positions_list = [(785, 610), (785, 670), (785, 730)]
	def __init__(self, game, name, player_ID):
		self.name = name
		self.ID = player_ID
		self.text = self.name
		Info.build(self, game)
		self.rect.left, self.rect.top = NamePlayer.positions_list[self.ID]
		Info.__init__(self, game)


class NameEnemy(Info):
	positions_list = [(35, 610), (35, 670)]
	def __init__(self, game, name, enemy_ID):
		self.name = name
		self.ID = enemy_ID
		self.text = self.name
		Info.build(self, game)
		self.rect.left, self.rect.top = NameEnemy.positions_list[self.ID]
		Info.__init__(self, game)		


class Stats(Info):
	def __init__(self, game):
		self.text = ''
		self.value = 0
		self.max_value = 0
		Info.__init__(self, game)

	def update(self):
		text = str(self.value) + ' / ' + str(self.max_value) # needs to be a string for font.render
		self.image = self.font.render(text, 1, self.color) # update the value


class HPplayer(Stats):
	positions_list = [(950, 610), (950, 670), (950, 730)]
	def __init__(self, game, player_ID):
		self.ID = player_ID
		self.color = (0, 173, 33, 0)
		Stats.__init__(self, game)
		Info.build(self, game)
		self.rect.left, self.rect.top = HPplayer.positions_list[self.ID]


class MPplayer(Stats):
	positions_list = [(1100, 610), (1100, 670), (1100, 730)]
	def __init__(self, game, player_ID):
		self.ID = player_ID
		self.color = (0, 126, 255, 0)
		Stats.__init__(self, game)
		Info.build(self, game)
		self.rect.left, self.rect.top = MPplayer.positions_list[self.ID]


class HPenemy(Stats):
	positions_list = [(245, 610), (245, 670)]
	def __init__(self, game, enemy_ID):
		self.ID = enemy_ID
		self.color = (0, 173, 33, 0)
		Stats.__init__(self, game)
		Info.build(self, game)
		self.rect.left, self.rect.top = HPenemy.positions_list[self.ID]


class ActionBar(pygame.sprite.Sprite):
	def __init__(self, game, speed):
		self.image = pygame.Surface([0, 10])
		self.color = ((0, 129, 247))
		self.image.fill(self.color)
		self.rect = self.image.get_rect()
		self.width = 0
		self.width_percent = self.max_width * 0.01 # calculate 1% of the max width for incrementation purposes
		self.set_speed(speed)
		self.flash_counter = 0 # for timing the flash when the bar is full
		pygame.sprite.Sprite.__init__(self, game.scene_selector.scene.layer_2)

	def update(self):
		if self.width < self.max_width and self.flash_counter >= 5:
			self.flash_counter = 0
		elif self.width < self.max_width:
			self.progress()
		elif self.width > self.max_width and self.flash_counter < 5: 
			self.flash()
		else:
			self.image.fill((0, 227, 240)) # highlight color indicating action bar is full

	def progress(self): # incremental increase action bar width
		self.width += self.speed
		self.image = pygame.Surface([self.width, 10])
		self.image.fill(self.color)		

	def flash(self): # quick flash when action bar becomes full
		if self.flash_counter % 2 == 0: # if even
			self.image.fill((255, 255, 255))
		else: # if odd
			self.image.fill(self.color)
		self.flash_counter += 1

	# check for a change in speed for the entity
	def set_speed(self, speed):
		self.speed = self.width_percent * speed # can add/multiply here to adjust speed for different entities


class ActionBarPlayer(ActionBar):
	positions_list = [(785, 640), (785, 700), (785, 760)]
	full_sound_path = development.Path.root + 'sounds/player_action_bar_full.wav'
	full_sound = pygame.mixer.Sound(full_sound_path)
	def __init__(self, game, player_ID, speed):
		self.max_width = 460
		ActionBar.__init__(self, game, speed)
		self.ID = player_ID
		self.rect.left, self.rect.top = ActionBarPlayer.positions_list[self.ID]


class ActionBarEnemy(ActionBar):
	positions_list = [(35, 640), (35, 700)]
	full_sound_path = development.Path.root + 'sounds/enemy_action_bar_full.wav'
	full_sound = pygame.mixer.Sound(full_sound_path)
	def __init__(self, game, enemy_ID, speed):
		self.max_width = 300
		ActionBar.__init__(self, game, speed)
		self.ID = enemy_ID
		self.rect.left, self.rect.top = ActionBarEnemy.positions_list[self.ID]