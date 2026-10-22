#!/usr/bin/python
import pygame
import development


class MessagePanel(object):
	#---- configurable values ----
	y_spacing = 25      # the vertical space between the messages
	animation_steps = 5 # determines the speed of the message animation
	x = 55              # left x position of the messages
	y_start = 120       # y position of a newly create message
	limit = 4    				# number of messages shown at one time
	font_size = 28      # font size of the message
	font_type = development.Path.root + 'font/8-bit Madness.ttf'
	#-----------------------------

	y_spacing_increment = y_spacing / animation_steps
	alpha_increment = 255 / limit

	all_messages = pygame.sprite.Group()

	def __init__(self, game):
		self.game = ''

	def staging(self, game):
		self.game = game
		self.scene = game.scene_selector.scene

	def events(self, event):
		# FOR TESTING: press 'n' to create a test message
		if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
			self.create_message('This is a test message')

	# increment each messages history level attribute and trigger is move animation
	def progress_message_history(self):
		for message in MessagePanel.all_messages:
			message.move_animate_cycles += 1
			message.history_level += 1

	# create a new message object and call progress message history 
	def create_message(self, text):
		text = str(text)
		message = Message(self.game, text)
		self.progress_message_history()


class Message(pygame.sprite.Sprite):
	def __init__(self, game, text):
		self.text = str(text)
		self.alpha = 0
		self.color = ((255, 255, 255))
		self.render_alpha_text()
		self.x = MessagePanel.x
		self.y = MessagePanel.y_start
		self.rect = self.image.get_rect()
		self.rect.left = self.x
		self.rect.top = self.y

		self.history_level = 0
		self.move_animate_cycles = 0
		self.move_animate_counter = 0
		self.fade_in_counter = 0
		self.fade_in_increment = 255 / MessagePanel.animation_steps # full alpha value divided by steps in the animation
		self.fade_out_counter = 0
		self.fade_out_increment = 50 / MessagePanel.animation_steps # last alpha value divided by steps in the animation		

		pygame.sprite.Sprite.__init__(self)
		self.add(MessagePanel.all_messages)
		self.add(game.scene_selector.scene.layer_3)

	def update(self):
		if self.move_animate_cycles > 0:
			self.move_animate()

		# if the limit of messages to show is reached, fade out the message complete
		if self.history_level > MessagePanel.limit:
			self.fade_out()

		# reduce the alpha somewhat as the message degresses in the message history
		elif self.history_level >= 2:
			self.alpha = 255 - MessagePanel.alpha_increment * (self.history_level - 1)
			self.image.set_alpha(self.alpha)

	# blit text onto a surface so alpha can be used
	def render_alpha_text(self):
		self.font = pygame.font.Font(MessagePanel.font_type, MessagePanel.font_size)
		self.font_rendered = self.font.render(self.text, 1, self.color)
		self.image = pygame.Surface(self.font.size(self.text))
		self.image.set_colorkey((0, 0, 0))
		self.image.blit(self.font_rendered, (0, 0))
		self.image.set_alpha(self.alpha)					

	# animate the message upward in the message panel history
	def move_animate(self):
		if self.move_animate_counter < MessagePanel.animation_steps:
			self.move_animate_counter += 1
			self.y -= MessagePanel.y_spacing_increment
			self.rect.top = self.y
			self.fade_in()
		elif self.move_animate_counter >= MessagePanel.animation_steps:
			self.move_animate_cycles -= 1
			self.move_animate_counter = 0

	# fade in after being created
	def fade_in(self):
		if self.fade_in_counter < MessagePanel.animation_steps:
			self.fade_in_counter += 1
			self.alpha += self.fade_in_increment
			self.image.set_alpha(self.alpha)

	# fade out and remove
	def fade_out(self):
		if self.fade_out_counter < MessagePanel.animation_steps:
			self.fade_out_counter += 1
			self.alpha -= self.fade_out_increment
			self.image.set_alpha(self.alpha)
		else:
			self.kill()