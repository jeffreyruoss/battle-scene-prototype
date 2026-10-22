#!/usr/bin/python
import pygame
import pygame.mixer
import entity_stats
import battle_menu
import effects
import ai
import random
import message_panel
import status_icons
import development
pygame.mixer.init()


class Entity(pygame.sprite.Sprite):
	attack_sound_path = development.Path.root + 'sounds/hit1.wav'
	attack_sound = pygame.mixer.Sound(attack_sound_path)
	defeated_sound_path = development.Path.root + 'sounds/defeated.wav'
	defeated_sound = pygame.mixer.Sound(defeated_sound_path)
	defend_sound_path = development.Path.root + 'sounds/defend.wav'
	defend_sound = pygame.mixer.Sound(defend_sound_path)
	miss_sound_path = development.Path.root + 'sounds/miss.wav'
	miss_sound = pygame.mixer.Sound(miss_sound_path)
	def __init__(self, game):
		self.game = game
		self.scene = self.game.scene_selector.scene
		image_path = development.Path.root + 'images/' + self.image_file_name
		self.image = pygame.image.load(image_path).convert_alpha()
		self.rect = pygame.rect.Rect((0, 0), self.image.get_size())
		self.w = self.image.get_width() / self.num_frames
		self.h = self.image.get_height()
		self.build_sprite_frames()
		self.position()
		self.attack_animate_running = False
		self.attack_animate_counter = 0
		self.is_defeated = False
		self.defeated_animate_duration = 30
		self.defeated_animate_counter = 0
		self.cast_animate_running = False
		self.cast_animate_duration = 30
		self.cast_animate_counter = 0
		self.ready = False
		self.HP_scrolling = False
		self.HP_scrolling_amount = 0

		# modes
		# 	modes last for on turn and their can only be one mode at a time for the entity
		self.mode = ''

		# statuses
		#		statuses last until they expire or until they are removed by something else
		self.statuses = []

		# number of status and mode icons they currently have
		self.num_icons = 0

		self.breakdef_status = False

		pygame.sprite.Sprite.__init__(self, game.scene_selector.scene.layer_2)

	def update(self):
		self.animations()
		self.check_if_ready()
		self.scroll_HP()

	def build_sprite_frames(self):
		self.frames_list = []
		current_img_x = 0
		for i in xrange(self.num_frames):
			frame = self.image.subsurface(current_img_x, 0, self.w, self.h)
			self.frames_list.append(frame)
			current_img_x += self.w
		self.image = self.frames_list[0]
		self.rect = self.image.get_rect()

	def animations(self):
		# attack animation
		if self.attack_animate_running == True and self.attack_animate_counter < self.num_frames - 1:
			self.attack_animate_counter += 1
			self.image = self.frames_list[self.attack_animate_counter]
		else:
			self.attack_animate_counter = 0
			self.image = self.frames_list[0]
			self.attack_animate_running = False
		# defeated fade out animation
		if self.HP <= 0: 
			self.defeated(self.game)
		if self.cast_animate_running == True and self.cast_animate_counter < self.cast_animate_duration:
			self.cast_animate_counter += 1
			self.image = self.frames_list[3]
		elif self.cast_animate_running == True and self.cast_animate_counter >= self.cast_animate_duration:
			self.cast_animate_counter = 0
			self.image = self.frames_list[0]
			self.cast_animate_running = False

	def position(self): # positioning manually for now. 
		if self.entity_type == 'player':
			self.rect.left, self.rect.top = Player.positions_list[self.ID]
		if self.entity_type == 'enemy':
			self.rect.left, self.rect.top = Enemy.positions_list[self.ID]

	def check_if_ready(self): # check if the entities action bar is full
		if self.stats_action_bar.width >= self.stats_action_bar.max_width and self.ready == False:
			self.stats_action_bar.full_sound.play()
			self.ready = True

	def complete_turn(self, battle_menu): # run when entity action is complete
		self.clear_mode()
		self.stats_action_bar.width = 0
		self.ready = False
		if self.entity_type == 'player':
			battle_menu.level = 1
			battle_menu.reset()
			battle_menu.change_level()

	def scroll_HP(self): # when an entity gets damaged their HP scrolls down
		if self.HP <= 0:
			self.HP = 0
		elif self.HP_scrolling and self.HP_scrolling_amount > 0:
			self.HP -= 1
			self.HP_scrolling_amount -= 1
		else:
			self.HP_scrolling = False

	""" Adjust for Defense
	Reduce physical damage by the entity's DEF value
	Radomized amount slightly for variation
	"""
	def adjust_for_DEF(self, damage):
		DEF_amount = self.DEF * 0.01 # convert percent to decimal
		damage_reduction = damage * DEF_amount
		damage -= damage_reduction
		damage = int(damage) # round the value
		return damage

	def clear_mode(self):
		if self.mode == '':
			return
		else:
			if self.mode == 'Defend':
				self.defend_end()			
			self.current_mode_icon.remove_self()
			self.mode = ''			

	""" Defend action (defend mode initiate)
	While an entity is in defense mode their DEF is increased significantly
	"""
	def defend(self, battle_menu):
		Entity.defend_sound.play()
		self.current_mode_icon = status_icons.DefendModeIcon(self, self.game)
		panel_message = self.name + ' is in defend mode '
		self.DEF_bonus = 50 # plus percent
		overlay_message = '+ ' + str(self.DEF_bonus) + '% DEF'
		self.DEF = self.DEF + self.DEF_bonus # add DEF bonus
		effects.TextAndNumbersOverlay(self.game, self, overlay_message)
		self.scene.message_panel.create_message(panel_message)
		self.complete_turn(battle_menu)
		self.mode = 'Defend'

	# restore to normal DEF
	def defend_end(self): 
		self.DEF = self.DEF / self.DEF_bonus

	""" Defeated
	Fade out entity image and remove entity from the game
	"""
	def defeated(self, game):
		if self.defeated_animate_counter == 0:
			self.is_defeated = True
			Entity.defeated_sound.play()
			self.defeated_animate_counter += 1
			self.alpha = 255
			self.fade_increment = self.alpha / self.defeated_animate_duration
		elif self.defeated_animate_counter < self.defeated_animate_duration: 
			self.alpha -= self.fade_increment
			self.image.fill((255, 255, 255, self.alpha), None, pygame.BLEND_RGBA_MULT)
			self.defeated_animate_counter += 1
		else:
			self.stats_name.kill()
			self.stats_HP.kill()
			self.stats_action_bar.kill()
			if self.entity_type == 'player':
				self.stats_MP.kill()
				self.game.scene_selector.scene.players_list.remove(self)
			elif self.entity_type == 'enemy':
				self.game.scene_selector.scene.enemies_list.remove(self)
			self.kill()


class Player(Entity):
	positions_list = [(760, 165), (760, 315), (760, 465)]
	players_list = []
	def __init__(self, name, game):
		self.entity_type = 'player'
		self.name = name
		self.ID = game.scene_selector.scene.player_ID
		self.HP = 100
		self.max_HP = 100
		self.MP = 80
		self.max_MP = 80
		# self.ATK = 20
		self.ATK = 25 # for testing
		self.ATK = 20
		self.DEF = 15 # defense (percentage reduced)
		self.speed = 0.35
		self.stats_name = entity_stats.NamePlayer(game, self.name, self.ID)
		self.stats_HP = entity_stats.HPplayer(game, self.ID)
		self.stats_MP = entity_stats.MPplayer(game, self.ID)
		self.stats_action_bar = entity_stats.ActionBarPlayer(game, self.ID, self.speed)
		self.actions = [('Attack', self.attack), ('Defend', self.defend)]
		self.agro_status = False
		game.scene_selector.scene.player_ID += 1
		Entity.__init__(self, game)
		Player.players_list.append(self)
		game.scene_selector.scene.players_list.append(self)

	def update(self):
		self.stats_HP.value = self.HP # push value to the stat objects
		self.stats_HP.max_value = self.max_HP
		self.stats_MP.value = self.MP
		self.stats_MP.max_value = self.max_MP
		Entity.update(self)

	def attack(self, battle_menu):
		# before target is chosen
		if battle_menu.active_target == '':
			battle_menu.active_action = 'attack'
			battle_menu.show_targets('enemy')
		# after target is chosen
		else:
			target = battle_menu.active_target

			# attack
			damage = target.adjust_for_DEF(self.ATK)
			target.HP_scrolling = True
			target.HP_scrolling_amount += damage
			self.attack_animate_running = True
			effects.Slash(battle_menu.game, target)
			Entity.attack_sound.play()
			effects.TextAndNumbersOverlay(battle_menu.game, target, damage, 'damage')
			message = self.name + ' does ' + str(damage) + ' damage to ' + target.name
			self.scene.message_panel.create_message(message)
			self.complete_turn(battle_menu)

	def potion(self, battle_menu):
		print self.name, ' potion'


class Enemy(Entity):
	positions_list = [(300, 200), (300, 375)]
	def __init__(self, name, game):
		self.entity_type = 'enemy'
		self.name = name
		self.ID = game.scene_selector.scene.enemy_ID
		self.HP = 50
		self.max_HP = 50
		self.MP = 0
		self.max_MP = 0
		self.ATK = 25
		self.DEF = 15 # defense (percentage reduced)
		self.speed = random.uniform(0.2, 0.3)
		self.stats_name = entity_stats.NameEnemy(game, self.name, self.ID)
		self.stats_HP = entity_stats.HPenemy(game, self.ID)
		self.stats_action_bar = entity_stats.ActionBarEnemy(game, self.ID, self.speed)
		game.scene_selector.scene.enemy_ID += 1
		Entity.__init__(self, game)
		self.AI = ai.Behavior(self.scene, self)
		game.scene_selector.scene.enemies_list.append(self)

	def update(self):
		self.stats_HP.value = self.HP # push value to the stat objects
		self.stats_HP.max_value = self.max_HP
		self.AI.update()
		Entity.update(self)

	def AI(self):
		self.AI.update()

	def attack(self, target):
		damage = target.adjust_for_DEF(self.ATK)
		target.HP_scrolling = True
		target.HP_scrolling_amount += damage
		self.attack_animate_running = True
		effects.Slash(self.game, target)
		Entity.attack_sound.play()
		message = self.name + ' does ' + str(damage) + ' damage to ' + target.name
		effects.TextAndNumbersOverlay(self.game, target, damage, 'damage')
		self.scene.message_panel.create_message(message)
		self.complete_turn(self.scene.battle_menu)


class Knight(Player):
	argo_sound_path = development.Path.root + 'sounds/agro.wav'
	agro_sound = pygame.mixer.Sound(argo_sound_path)
	breakdef_sound_path = development.Path.root + 'sounds/breakdef.wav'
	breakdef_sound = pygame.mixer.Sound(breakdef_sound_path)
	def __init__(self, name, game):
		self.num_frames = 6
		self.image_file_name = 'knight.png'
		Player.__init__(self, name, game)
		self.HP = 160
		self.max_HP = 160
		self.MP = 0
		self.max_MP = 0
		self.DEF = 35
		self.speed = 0.4
		self.stats_action_bar.set_speed(self.speed)
		self.actions.extend([('Break Defense', self.breakdef), ('Agro', self.agro)])

	def breakdef(self, battle_menu):
		# before target is chosen
		if battle_menu.active_target == '':
			battle_menu.active_action = 'breakdef'
			battle_menu.show_targets('enemy')
		# after target is chosen
		else:
			target = battle_menu.active_target

			# breakdef
			Knight.breakdef_sound.play()
			target.breakdef_status = True
			target.current_status_icon = status_icons.BreakDefIcon(target, self.game)
			self.attack_animate_running = True
			effects.Slash(battle_menu.game, target)
			effects.TextAndNumbersOverlay(battle_menu.game, target, 'Defense Broken')
			message = self.name + ' has temporarily broken the defense of ' + target.name
			self.scene.message_panel.create_message(message)
			target.statuses.append('breakdef')
			self.complete_turn(battle_menu)

	def agro(self, battle_menu):
		Knight.agro_sound.play()
		self.current_status_icon = status_icons.AgroStatusIcon(self, self.game)
		panel_message = self.name + ' has increased agro'
		overlay_message = 'AGRO UP'
		effects.TextAndNumbersOverlay(self.game, self, overlay_message)
		self.scene.message_panel.create_message(panel_message)
		self.statuses.append('agro')
		self.agro_status = True
		self.complete_turn(battle_menu)


class Mage(Player):
	def __init__(self, name, game):
		self.num_frames = 5
		self.image_file_name = 'wizard.png'
		Player.__init__(self, name, game)
		self.HP = 70
		self.max_HP = 70
		self.MP = 200
		self.max_MP = 200
		self.DEF = 10
		self.speed = 0.5
		self.stats_action_bar.set_speed(self.speed)
		self.actions.extend([('Fire', self.fire, 30), ('Heal', self.heal, 30)])

	def bolt(self, battle_menu):
		print self.name, ' bolt'

	def fire(self, battle_menu):
		# before target is chosen
		if battle_menu.active_target == '':
			battle_menu.active_action = 'fire'
			battle_menu.show_targets('enemy')
		# after target is chosen
		else:
			target = battle_menu.active_target

			# heal
			self.cast_animate_running = True
			effects.Fire(self.game, target)
			self.MP -= 30
			damage_amount = 50
			target.HP -= damage_amount
			effects.TextAndNumbersOverlay(battle_menu.game, target, damage_amount, 'damage')
			message = target.name + ' takes ' + str(damage_amount) + ' fire damage from ' + self.name
			self.scene.message_panel.create_message(message)
			self.complete_turn(battle_menu)

	def heal(self, battle_menu):
		# before target is chosen
		if battle_menu.active_target == '':
			battle_menu.active_action = 'heal'
			battle_menu.show_targets('player')
		# after target is chosen
		else:
			target = battle_menu.active_target

			# heal
			self.cast_animate_running = True
			effects.Heal(self.game, target)
			self.MP -= 30
			heal_amount = 50
			if target.HP + heal_amount <= target.max_HP:
				target.HP += heal_amount
			else:
				target.HP = target.max_HP
			effects.TextAndNumbersOverlay(battle_menu.game, target, heal_amount, 'heal')
			message = target.name + ' is healed for ' + str(heal_amount) + ' by ' + self.name
			self.scene.message_panel.create_message(message)
			self.complete_turn(battle_menu)


class Ranger(Player):
	kostrike_sound_path = development.Path.root + 'sounds/kostrike.wav'
	kostrike_sound = pygame.mixer.Sound(kostrike_sound_path)
	haste_sound_path = development.Path.root + 'sounds/haste.wav'
	haste_sound = pygame.mixer.Sound(haste_sound_path)
	def __init__(self, name, game):
		self.num_frames = 6
		self.image_file_name = 'ranger.png'
		Player.__init__(self, name, game)
		self.speed = 0.6
		self.stats_action_bar.set_speed(self.speed)
		self.actions.extend([('Haste', self.haste), ('KO strike', self.kostrike)])

	def haste(self, battle_menu):
		Ranger.haste_sound.play()
		self.speed = self.speed * 2
		self.stats_action_bar.set_speed(self.speed)
		self.current_status_icon = status_icons.HasteStatusIcon(self, self.game)
		panel_message = self.name + ' has cast Haste'
		overlay_message = 'SPEED UP'
		effects.TextAndNumbersOverlay(self.game, self, overlay_message)
		self.scene.message_panel.create_message(panel_message)
		self.statuses.append('haste')
		self.complete_turn(battle_menu)

	def haste_end(self):
		self.speed = self.speed / 2
		self.stats_action_bar.set_speed(self.speed)

	def kostrike(self, battle_menu):
		# before target is chosen
		if battle_menu.active_target == '':
			battle_menu.active_action = 'kostrike'
			battle_menu.show_targets('enemy')
		# after target is chosen
		else:
			target = battle_menu.active_target

			# kostrike
			# damage = target.adjust_for_DEF(self.ATK - self.ATK * 0.5)
			# target.HP_scrolling = True
			# target.HP_scrolling_amount += damage
			if target.breakdef_status == True:
				self.attack_animate_running = True
				Ranger.kostrike_sound.play()
				effects.Slash(battle_menu.game, target)
				target.HP = 0
				effects.TextAndNumbersOverlay(battle_menu.game, target, 'KO Strike')
				message = self.name + ' has performed a KO Strike on ' + target.name
			else:
				self.attack_animate_running = True
				Entity.miss_sound.play()
				effects.TextAndNumbersOverlay(battle_menu.game, target, 'Missed')
				message = 'Defense of ' + target.name + ' is unbroken so KO Strike by ' + self.name + ' has failed.'
			self.scene.message_panel.create_message(message)
			self.complete_turn(battle_menu)


class Ogre(Enemy):
	def __init__(self, name, game):
		self.num_frames = 4
		self.image_file_name = 'ogre.png'
		Enemy.__init__(self, name, game)
		self.HP = 200
		self.max_HP = 200
		self.DEF = 25
		self.speed = random.uniform(0.4, 0.5)
		self.stats_action_bar.set_speed(self.speed)