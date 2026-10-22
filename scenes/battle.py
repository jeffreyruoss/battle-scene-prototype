#!/usr/bin/python
import pygame
import pygame.mixer
from modules import cursor
from modules import entities
from modules import battle_menu
from modules import scene_fade
from modules import message_panel
import development


class BattleScene(object):
	def __init__(self, game):
		self.active = False
		self.background = ''
		music_path = development.Path.root + 'sounds/main_battle_loop.wav'
		self.music = pygame.mixer.Sound(music_path)
		victory_music_path = development.Path.root + 'sounds/victory.wav'
		self.victory_music = pygame.mixer.Sound(victory_music_path)
		defeat_music_path = development.Path.root + 'sounds/defeat_music.wav'
		self.defeat_music = pygame.mixer.Sound(defeat_music_path)
		self.layer_1 = pygame.sprite.Group()
		self.layer_2 = pygame.sprite.Group()
		self.layer_3 = pygame.sprite.Group()
		self.players_list = []
		self.enemies_list = []
		self.start_message_shown = False
		self.enemy_delay = False
		self.enemy_delay_counter = 0
		self.battle_over = False
		self.victorious = False
		self.defeated = False
		self.battle_menu = battle_menu.BattleMenu(game)
		self.message_panel = message_panel.MessagePanel(game)
		self.cursor_sprite_group = pygame.sprite.Group()
		self.fade_sprite_group = pygame.sprite.Group()

	def events(self, event, game):
		if self.battle_over == False:
			self.battle_menu.events(event)
		self.message_panel.events(event)

	def staging(self, game):
		self.cursor = cursor.Cursor(game)
		self.player_ID = 0
		self.player1 = entities.Knight('Bob', game)
		self.player2 = entities.Mage('Steve', game)
		self.player3 = entities.Ranger('Jack', game)
		self.enemy_ID = 0
		self.ogre1 = entities.Ogre('Grog', game)
		self.ogre2 = entities.Ogre('Trog', game)
		self.load_background(game)
		self.scene_fade = scene_fade.SceneFade(self, 50)
		self.battle_menu.staging(game)
		self.message_panel.staging(game)

	def update(self, game):
		if not self.enemies_list: # if no enemies left
			self.victory()
		elif not self.players_list: # if no players left
			self.defeat()
		elif not self.battle_over: # if battle is not over, run updates
			self.battle_menu.update(game)
			if self.scene_fade.complete: # when fade is complete, start the sprite group updating
				if not self.start_message_shown:
					self.start_message()
				self.layer_1.update()
				self.layer_2.update()
			self.fade_sprite_group.update()
		self.layer_3.update()
		self.cursor_sprite_group.update()
		if self.battle_over:
			self.battle_menu.hide_all_current_items() # if battle over, clear battle menu		

	def load_background(self, game):
		if self.background == '':
			background_path = development.Path.root + 'images/background-battle.jpg'
			self.background = pygame.image.load(background_path).convert()
			game.screen.blit(self.background, (0, 0))
		else:
			game.screen.blit(self.background, (0, 0))

	def start_message(self):
		self.message_panel.create_message('You have encountered enemies!')
		self.start_message_shown = True

	def victory(self):
		if self.victorious == False:
			self.message_panel.create_message('Victory!')
			self.music.stop()
			self.victory_music.play()
			self.victorious = True
			self.battle_over = True

	def defeat(self):
		if self.defeated == False:
			self.message_panel.create_message('Defeat!')
			self.music.stop()
			self.defeat_music.play()
			self.defeated = True
			self.battle_over = True


