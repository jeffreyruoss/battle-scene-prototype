#!/usr/bin/python
import pygame
import entities
import random


class Behavior(object):
	def __init__(self, scene, enemy):
		self.scene = scene
		self.enemy = enemy
		self.pre_action_delay = 0

	def update(self):
		if self.enemy.HP <= 0:
			return
		if self.scene.enemy_delay == True: # if another enemy is actioning
			self.other_enemy_delay()
		elif self.enemy.ready == True and self.pre_action_delay < 30: # delay 30 frames before action
			self.pre_action_delay += 1
		elif self.enemy.ready == True and self.pre_action_delay >= 30:
			self.scene.enemy_delay = True
			self.scene.enemy_delay_counter = 120 # if another enemy just actioned, delay Enemy's for 120 frames
			target = self.choose_target('player')
			if target != 'no valid targets':
				self.enemy.attack(target)
			self.pre_action_delay = 0

	def other_enemy_delay(self):
		if self.scene.enemy_delay_counter > 0:
			self.scene.enemy_delay_counter -= 1
		if self.scene.enemy_delay_counter <= 0:
			self.scene.enemy_delay = False

	def choose_target(self, entity_type):
		if entity_type == 'player':
			if not self.scene.players_list:
				return 'no valid targets'
			for player in self.scene.players_list:
				if player.agro_status == True: # if this is a player with agro, target that player
					target = player
					return target
				else: # else target a player randomly
					target = random.choice(self.scene.players_list)
		elif entity_type == 'enemy':
			pass
		return target