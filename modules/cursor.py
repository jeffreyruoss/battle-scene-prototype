#!/usr/bin/python
import pygame
import pygame.mixer
import development


class Cursor(pygame.sprite.Sprite):
	def __init__(self, game):
		pygame.mouse.set_visible(0)
		cursor_img_path = development.Path.root + 'images/cursor.png'
		self.image = pygame.image.load(cursor_img_path).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.top = 0
		self.rect.left = 0
		pygame.sprite.Sprite.__init__(self, game.scene_selector.scene.cursor_sprite_group)

	def update(self):
		mouse_position = pygame.mouse.get_pos()
		self.rect = mouse_position
