#!/usr/bin/python
import pygame
import development

class BattleMenu(object):
	font_type = development.Path.root + 'font/8-bit Madness.ttf'
	all_items = []
	player_names = []
	actions = []
	targets = []
	def __init__(self, game):
		self.level = 1
		self.game = ''
		self.scene = ''
		self.active_player = ''
		self.active_action = ''
		self.active_target = ''

	def staging(self, game):
		self.game = game
		self.scene = game.scene_selector.scene
		self.change_level()

	def events(self, event):
		if self.level == 1 \
		and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			for player_name in BattleMenu.player_names:
				player_name.check_clicked(self)
		elif self.level >= 2 \
		and (self.back.box.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) \
		or (self.level == 2 and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			self.back.clicked(self)
		elif self.level == 2 \
		and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			for action in BattleMenu.actions:
				action.check_clicked(self)
		elif self.level == 3 \
		and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			for target in BattleMenu.targets:
				target.check_clicked()

	def update(self, game):
		pass

	def change_level(self):
		self.hide_all_current_items()
		if self.level == 1:
			self.show_player_names()
		elif self.level == 2:
			self.show_actions()
		elif self.level == 3:
			pass

	def show_player_names(self):
		for player in self.scene.players_list:
			PlayerName(self.game, player);

	def show_actions(self):
		self.back = Back(self.game)
		self.header = Header(self.game, self.active_player.name)
		x = 1010
		y = 270
		for action in self.active_player.actions:
			Action(self.game, self, action, x, y)
			y += 40

	def show_targets(self, type):
		self.change_level()
		self.back = Back(self.game)
		self.header = Header(self.game, 'Target')
		x = 1010
		y = 270
		y_space = 50 # space between menu items
		if type == 'enemy':
			for enemy in self.scene.enemies_list:
				Target(self.game, self, enemy, x, y)
				y += y_space
		elif type == 'player':
			for player in self.scene.players_list:
				Target(self.game, self, player, x, y)
				y += y_space

	def hide_all_current_items(self):
		for item in BattleMenu.all_items:
			item.kill()
		BattleMenu.all_items = []
		for player_name in BattleMenu.player_names:
			player_name.kill()
		BattleMenu.player_names = []
		for action in BattleMenu.actions:
			action.kill()
		BattleMenu.actions = []
		for target in BattleMenu.targets:
			target.kill()
		BattleMenu.targets = []		

	def reset(self):
		self.active_player = ''
		self.active_action = ''
		self.active_target = ''


class Text(pygame.sprite.Sprite):
	def __init__(self):
		self.font_type = BattleMenu.font_type
		self.font = pygame.font.Font(self.font_type, self.font_size)
		self.image = self.font.render(self.text, 1, self.color)
		self.rect = self.image.get_rect()
		self.rect.left = self.x
		self.rect.top = self.y
		BattleMenu.all_items.append(self)
		self.create_box()
		pygame.sprite.Sprite.__init__(self, self.game.scene_selector.scene.layer_2)

	def create_box(self):
		if hasattr(self, 'has_box'):
			self.box = Box(self.game, self.rect)


class Box(pygame.sprite.Sprite):
	def __init__(self, game, rect):
		padding = 15
		rect.left += padding # offset position
		rect.top += padding # offset position
		w = rect.w + (padding * 2)
		h = rect.h + (padding * 2)
		x = rect.left - padding
		y = rect.top - padding  - 2
		self.image = pygame.Surface((w, h))
		self.image.set_alpha(150)
		self.image.fill((0, 0, 0))
		self.rect = pygame.Rect(x, y, w, h)
		BattleMenu.all_items.append(self)
		pygame.sprite.Sprite.__init__(self, game.scene_selector.scene.layer_1)


class Header(Text):
	def __init__(self, game, text):
		self.game = game
		self.text = str(text)
		self.x, self.y = 1010, 215
		self.font_size = 45
		self.color = (0, 171, 182)
		Text.__init__(self)


class Item(Text):
	def __init__(self):
		self.font_size = 35
		self.color = (100, 100, 100)
		self.enabled = False
		Text.__init__(self)

	def update(self):
		pass

	def enable(self):
		self.image = self.font.render(self.text, 1, (255, 255, 255))
		self.enabled = True

	def disable(self):
		self.image = self.font.render(self.text, 1, (100, 100, 100))
		self.enabled = False

			
class Back(Text):
	def __init__(self, game):
		self.has_box = True
		self.game = game
		self.text = 'BACK (ESC)'
		self.x, self.y = 1010, 150
		self.font_size = 28
		self.color = (175, 175, 175)
		Text.__init__(self)

	def clicked(self, battle_menu):
		battle_menu.level -= 1
		battle_menu.change_level()


class PlayerName(Item):
	positions_list = [(1010, 180), (1010, 280), (1010, 380)]
	def __init__(self, game, player):
		self.game = game
		self.player = player
		self.text = player.name
		self.x, self.y = PlayerName.positions_list[player.ID]
		BattleMenu.player_names.append(self)
		Item.__init__(self)

	def update(self):
		self.check_player_ready()

	def check_player_ready(self):
		if self.player.ready == True and self.enabled == False:
			self.enable()

	def check_clicked(self, battle_menu):
		if self.rect.collidepoint(pygame.mouse.get_pos()) and self.enabled == True:
			battle_menu.active_player = self.player
			battle_menu.level += 1
			battle_menu.change_level()


class Action(Item):
	def __init__(self, game, battle_menu, action, x, y):
		self.game = game
		self.action_name = action[0]

		# if there is no MP cost to display
		if len(action) == 2:
			self.cost = False
			self.text = action[0]
		# if there is an MP cost to display
		elif len(action) == 3:
			self.cost = action[2]
			self.text = action[0] + ' - ' + str(self.cost) + ' MP'

		self.x = x
		self.y = y
		Item.__init__(self)

		# check if there is sufficent MP to cast
		if self.sufficent_MP(battle_menu) or self.cost == False:
			self.enable()
		else:
			self.disable()

		# check if it is a mode that is currently enabled
		if battle_menu.active_player.mode == self.action_name:
			self.disable()

		BattleMenu.actions.append(self)

	def check_clicked(self, battle_menu):
		if self.rect.collidepoint(pygame.mouse.get_pos()) and self.enabled == True:
			battle_menu.level += 1
			self.call_action_on_player(battle_menu, self.action_name)

	def call_action_on_player(self, battle_menu, action_called):
		player = battle_menu.active_player

		# loop through the players actions to find the one choosen and call that action's method
		for action in player.actions:
			if action[0] == action_called:
				action[1](battle_menu)
				return

	def sufficent_MP(self, battle_menu):
		if battle_menu.active_player.MP >= self.cost:
			return True
		else:
			return False


class Target(Item):
	def __init__(self, game, battle_menu, entity, x, y):
		self.game = game
		self.battle_menu = battle_menu
		self.entity = entity
		self.text = entity.name
		self.x = x
		self.y = y
		Item.__init__(self)
		self.enable()
		BattleMenu.targets.append(self)

	def check_clicked(self):
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.set_target_and_call_back()

	def set_target_and_call_back(self):
		active_player = self.battle_menu.active_player
		active_action = self.battle_menu.active_action
		self.battle_menu.active_target = self.entity
		getattr(active_player, active_action)(self.battle_menu) # call the active action on the active player

