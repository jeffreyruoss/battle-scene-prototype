#!/usr/bin/python
import pygame


class SceneFade(pygame.sprite.Sprite):
	def __init__(self, scene, speed):
		self.complete = False
		self.speed = speed # 1 is the slowest and higher num is faster (255 total increments)
		self.image = pygame.Surface([1440, 900], flags=pygame.SRCALPHA)
		self.rect = pygame.rect.Rect((0, 0), self.image.get_size())
		self.alpha = 255
		self.image.fill([0, 0, 0, self.alpha])
		pygame.sprite.Sprite.__init__(self, scene.fade_sprite_group)

	def update(self):
		self.alpha -= 10
		if self.complete == True:
			self.kill()
		elif self.alpha > 0:
			self.image.fill([0, 0, 0, self.alpha])
		else:
			self.complete = True