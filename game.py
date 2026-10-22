#!/usr/bin/python
import pygame
import scene_selector


class Game(object):
	def __init__(self):
		self.running = True
		self.screen = screen
		self.scene_selector = scene_selector.SceneSelector(self) # create the scene selector

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:	
				self.running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
				self.running = False
			
			self.scene_selector.events(self, event) # run events from scene_selector and the current scene

	def clear(self):
		scene = self.scene_selector.scene
		background = scene.background

		scene.layer_1.clear(self.screen, background) # clear layer 1 sprites with background of current scene
		scene.layer_2.clear(self.screen, background) # clear layer 2 sprites with background of current scene
		scene.layer_3.clear(self.screen, background) # clear layer 3 sprites with background of current scene
		scene.fade_sprite_group.clear(self.screen, background) # clear cursor sprite with background of the scene
		scene.cursor_sprite_group.clear(self.screen, background) # clear cursor sprite with background of the scene

	def update(self):
		self.scene_selector.update(self) #run updates from the current scene

	def render(self):
		scene = self.scene_selector.scene

		scene.layer_1.draw(self.screen) # draw layer 1 sprites from current scene
		scene.layer_2.draw(self.screen) # draw layer 2 sprites from current scene
		scene.layer_3.draw(self.screen) # draw layer 3 sprites from current scene
		scene.fade_sprite_group.draw(self.screen) # draw the cursor sprites of the current scene
		scene.cursor_sprite_group.draw(self.screen) # draw the cursor sprites of the current scene

	def main(self, screen):
		clock = pygame.time.Clock()
		self.scene_selector.initial_scene_load(game) # first scene load

		### Main Game Loop ###
		while self.running:
			clock.tick(30)

			self.events()

			self.clear() # clear the sprites

			self.update() # run updates from the current scene

			self.render() # draw the updated sprites

			pygame.display.flip()

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((1280, 800))
	pygame.display.set_caption('BATTLE SCENE Prototype')
	game = Game()
	game.main(screen)