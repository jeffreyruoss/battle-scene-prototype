#!/usr/bin/python
import pygame
import development


class Icon(pygame.sprite.Sprite):
	def __init__(self):
		status_icon_path = development.Path.root + 'images/status-icons/'
		self.image = pygame.image.load(status_icon_path + self.image_file_name)
		self.target.num_icons += 1
		self.get_position()
		self.rect = pygame.rect.Rect((self.left, self.top), self.image.get_size())
		pygame.sprite.Sprite.__init__(self, self.game.scene_selector.scene.layer_2)

	def update(self):
		if self.target.is_defeated == True:
			self.remove_self()
		elif self.expire_counter != False and self.expire_counter > 900:
			self.target.statuses.remove(self.name)
			self.end()
			self.remove_self()
		elif self.expire_counter != False:
			self.expire_counter += 1

	# get postion based on how many icons are already there at the entity
	def get_position(self):
		if self.target.num_icons == 1 or self.target.num_icons == 4 or self.target.num_icons == 7:
			self.top = self.target.rect.top
		elif self.target.num_icons == 2 or self.target.num_icons == 5 or self.target.num_icons == 8:
			self.top = self.target.rect.top + self.image.get_height()
		elif self.target.num_icons == 3 or self.target.num_icons == 6 or self.target.num_icons == 9:
			self.top = self.target.rect.top + self.image.get_height() * 2

		if self.target.num_icons <= 3:
			self.left = self.target.rect.right
		elif self.target.num_icons > 3 and self.target.num_icons <= 6:
			self.left = self.target.rect.right + self.image.get_width()
		elif self.target.num_icons > 6 and self.target.num_icons <= 9:
			self.left = self.target.rect.right + self.image.get_width() * 2

		if self.target.num_icons > 9:
			print 'too many statuses to show'
			self.top = - self.image.get_height()
			self.left = - self.image.get_width()

	def remove_self(self):
		self.target.num_icons -= 1
		self.kill()


class DefendModeIcon(Icon):
	def __init__(self, target, game):
		self.game = game
		self.target = target
		self.image_file_name = 'defend.png'
		self.expire_counter = False
		Icon.__init__(self)


class AgroStatusIcon(Icon):
	def __init__(self, target, game):
		self.game = game
		self.target = target
		self.name = 'agro'
		self.image_file_name = 'agro.png'
		self.expire_counter = 1
		Icon.__init__(self)

	def end(self):
		self.target.agro_status = False


class BreakDefIcon(Icon):
	def __init__(self, target, game):
		self.game = game
		self.target = target
		self.name = 'breakdef'
		self.image_file_name = 'breakdef.png'
		self.expire_counter = 1
		Icon.__init__(self)

	def end(self):
		self.target.breakdef = False

class HasteStatusIcon(Icon):
	def __init__(self, target, game):
		self.game = game
		self.target = target
		self.name = 'haste'
		self.image_file_name = 'haste.png'
		self.expire_counter = 1
		Icon.__init__(self)

	def end(self):
		self.target.haste_end()