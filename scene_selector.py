#!/usr/bin/python
import pygame
from scenes import intro
from scenes import battle
import development


class SceneSelector(object):
	def __init__(self, game):
		self.construct_scenes(game)
		self.scene = ''

	def construct_scenes(self, game):
		self.scenes = '' # clears old instances of scenes
		self.scenes = { # create fresh new scenes
			'intro': intro.IntroScene(game),
			'battle': battle.BattleScene(game)
		}

	def events(self, game, event):
		if event.type == pygame.KEYDOWN and event.key == pygame.K_i: # switch to intro scene (set to press i right now for testing)
			self.load_scene(game, 'intro')

		if event.type == pygame.KEYDOWN and event.key == pygame.K_b: # switch to battle scene (set to press b right now for testing)
			self.load_scene(game, 'intro')
		
		self.scene.events(event, game) # run the events for the current scene

	def update(self, game):
		self.scene.update(game) # run the updates for the current scene

	def initial_scene_load(self, game):
		if development.Config.start_scene and development.Config.start_scene != '': # if scene is set in development.py...
			self.load_scene(game, development.Config.start_scene) # skip ahead right to that scene
			print 'skipped to', development.Config.start_scene, 'scene, as set in development.py'
		else:
			self.load_scene(game, 'intro') # load intro scene at app launch as normal			

	def load_scene(self, game, new_scene):
		if (self.scene != self.scenes[new_scene]):
			if (self.scene != ''): # if it's not the first time a scene loads
				self.scene.music.stop() # stop music of last scene
				self.construct_scenes(game) # this clears out the scenes instances and creates fresh ones
			self.scene = self.scenes[new_scene] 
			self.scene.active = True
			self.music(game)
			self.scene.staging(game) # staging runs once when a new scene is initiated

	def music(self, game):
		if development.Config.mute_music: # is set to mute in development.py, don't play music
			print 'mute_music is set to True in development.py'
		else:
			self.scene.music.play(-1) # play music