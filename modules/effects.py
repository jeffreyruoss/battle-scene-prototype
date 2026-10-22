#!/usr/bin/python
import pygame
import pygame.mixer
import random
import development


class Effect(pygame.sprite.Sprite):
	def __init__(self):
		self.build_sprite_frames()
		self.rect.centery = self.centery
		self.rect.centerx = self.centerx
		pygame.sprite.Sprite.__init__(self, self.game.scene_selector.scene.layer_3)

	def build_sprite_frames(self):
		self.frames_list = []
		current_img_x = 0
		for i in xrange(self.num_frames):
			frame = self.image.subsurface(current_img_x, 0, self.w, self.h)
			self.frames_list.append(frame)
			current_img_x += self.w
		self.image = self.frames_list[0]
		self.rect = self.image.get_rect()


# slash effect when an entity gets hit with an attack
class Slash(Effect):
	def __init__(self, game, target):
		self.game = game
		slash_image_path = development.Path.root + 'images/slash.png'
		self.image = pygame.image.load(slash_image_path).convert_alpha()
		self.num_frames = 5
		self.w = 60
		self.h = 82
		self.rect = pygame.rect.Rect((0, 0), self.image.get_size())
		self.centery = target.rect.centery
		self.centerx = target.rect.centerx
		self.animate_counter = 0
		Effect.__init__(self)

	def update(self):
		self.animate()

	def animate(self):
		if self.animate_counter >= self.num_frames:
			self.kill()
		else:
			self.image = self.frames_list[self.animate_counter]
			self.animate_counter += 1


""" Text and Numbers Overlays
Text overlay over entities that can by used for damage numbers, crit hit text, etc
Type parameter:
	None: white
	'damage': orange
	'heal': green
"""
class TextAndNumbersOverlay(pygame.sprite.Sprite):
	def __init__(self, game, target, text, type=None):
		self.game = game
		self.text = str(text)
		self.centerx = target.rect.centerx
		self.y = target.rect.y -40
		self.alpha = 255
		if type == 'heal':
			self.color = ((0, 173, 33))
		elif type == 'damage':
			self.color = ((255, 174, 0))
		else:
			self.color = ((255, 255, 255))
		self.initial_color = self.color
		self.render_alpha_text()
		self.rect = self.image.get_rect()
		self.rect.centerx = self.centerx
		self.rect.top = self.y
		pygame.sprite.Sprite.__init__(self, self.game.scene_selector.scene.layer_3)
		self.expiration = 30
		self.flash_counter = 4
		
	def update(self):
		if self.flash_counter > 0:
			self.flash()
		elif self.expiration > 0:
			self.expiration -= 1
		elif self.expiration <= 0:
			self.fade_out()
			self.move_up()

	# blit text onto a surface so alpha can be used
	def render_alpha_text(self):
		font_path = development.Path.root + 'font/8-bit Madness.ttf'
		self.font = pygame.font.Font(font_path, 36)
		self.font_rendered = self.font.render(self.text, 1, self.color)
		self.image = pygame.Surface(self.font.size(self.text))
		self.image.set_colorkey((0, 0, 0))
		self.image.blit(self.font_rendered, (0, 0))
		self.image.set_alpha(self.alpha)		

	def flash(self):
		if self.flash_counter > 0:
			self.flash_counter -= 1
			if self.flash_counter % 2 == 0: # if even
				self.color = self.initial_color # change color back and then...
				self.render_alpha_text() # re-render text/surface with different color
			else:
				self.color = ((255, 255, 255)) # change color to white and then...
				self.render_alpha_text() # re-render text/surface with white

	def fade_out(self):
		if self.alpha > 0:
			self.alpha -= 15
			self.image.set_alpha(self.alpha)
		elif self.alpha <= 0:
			self.kill()

	def move_up(self):
		self.y -= 1
		self.rect.top = self.y


""" Particle System
Particle System is not spritesheet based so it doesn't use the Effect class as parent
"""
class ParticleSystem(pygame.sprite.Sprite):
	total_particles = 200 # count how many particles should be generated before ending the instance

	def __init__(self, target):
		self.x = target.rect.x
		self.y = target.rect.y - 30
		self.width = target.image.get_width()
		self.height = target.image.get_height()
		self.image = pygame.Surface((self.width, self.height)) # image/surface needed for it to function as a sprite
		self.image.set_colorkey((0, 0, 0)) # make image transparent
		self.particles = 0 # count how many particles that have existed 
		for x in xrange(self.starting_particles):
			self.generate_particle() # generate starting particles
		self.rect = pygame.rect.Rect((self.x, self.y), self.image.get_size())
		pygame.sprite.Sprite.__init__(self, self.game.scene_selector.scene.layer_3)

	def update(self):
		# if the total number of particles to exist is reached, remove instance
		if self.particles >= self.total_particles:
			self.kill()


""" Particle
This is an individual particle of the Particle System Effect
Not entirely sure on the performance at the moment
	Have to use a workaround instead of image fade with set_alpha
		Each frame, it needs to re-apply the original image and redo the transform, then fade
"""
class Particle(pygame.sprite.Sprite):
	def __init__(self, game, particle_system_instance):
		self.game = game
		self.particle_system_instance = particle_system_instance # grab the main ParticleSystem instance so it can reference back to it
		self.image = self.image_orginal # keep unmodified image for last use
		self.alpha = 0

		self.rect = pygame.rect.Rect((self.x, self.y), (self.size, self.size))

		self.fade_state = 'in' # will toggle 'in' and 'out'
		self.process_image()
		pygame.sprite.Sprite.__init__(self, game.scene_selector.scene.layer_3)

	def update(self):
		if self.fade_state == 'in':
			self.fade_in();
		elif self.fade_state == 'out':
			self.fade_out();
		self.move()

	# Need to re-apply the original image and transform for each fade increment as a work-around
	def process_image(self):
		self.image = self.image_orginal
		self.image = pygame.transform.scale(self.image, (self.size, self.size))
		self.image.fill((255, 255, 255, self.alpha), None, pygame.BLEND_RGBA_MULT)		

	# fade to max and then set to fade out
	def fade_in(self):
		if self.alpha < 255:
			self.alpha += self.fade_speed
		if self.alpha >= 255:
			self.alpha = 255
			self.fade_state = 'out'
		self.process_image()

	# fade out to 0, then create a new particle in it's place, then remove itself
	def fade_out(self):
		if self.alpha > 0:
			self.alpha -= self.fade_speed
		if self.alpha <= 0:
			self.alpha = 0
			self.particle_system_instance.generate_particle()
			self.kill()
		self.process_image()

	# movement animation
	def move(self):
		self.y += self.y_move_speed
		self.rect.y = self.y
		self.x += self.x_move_speed * self.x_move_direction
		self.rect.x = self.x


""" Heal Effect
This is the main Heal effect area
"""
class Heal(ParticleSystem):
	heal_sound_path = development.Path.root + 'sounds/heal.wav'
	heal_sound = pygame.mixer.Sound(heal_sound_path)
	total_particles = 200 # count how many particles should be generated before ending the instance

	def __init__(self, game, target):
		self.game = game
		Heal.heal_sound.play()
		self.starting_particles = 70 # number of starting particles and number of particles to exist at one time
		ParticleSystem.__init__(self, target)

	def generate_particle(self):
		# if the total number of particles to exist is not reached, create one and add to the particle number 
		if self.particles <= self.total_particles:
			HealParticle(self.game, self)
			self.particles += 1


""" Heal Particle
This is an individual particle of the Heal effect
"""
class HealParticle(Particle):
	def __init__(self, game, heal_instance):
		self.particle_system_instance = heal_instance
		heal_particle_image_path = development.Path.root + 'images/heal-particle.png'
		self.image_orginal = pygame.image.load(heal_particle_image_path).convert_alpha()

		# random move speed
		self.y_move_speed = random.uniform(0.5, 2)
		self.x_move_speed = random.uniform(0.1, 0.35)

		# randomize position based on the size of the main ParticleSystem instance
		self.x = self.particle_system_instance.x + random.uniform(0, self.particle_system_instance.width)
		self.y = self.particle_system_instance.y + random.uniform(0, self.particle_system_instance.height)

		# randomize size - range: 33% of the image src size to 100% of the image size
		self.size = random.uniform((self.image_orginal.get_width() / 3), self.image_orginal.get_width())
		self.size = int(round(self.size)) # transform doesn't like floats

		#random fade speed - range can be 1 to 255 (255 would be instance)
		self.fade_speed = random.uniform(20, 45)

		# random direction (1 is left, -1 is right)
		self.x_move_direction = random.choice([2, -2])		

		Particle.__init__(self, game, heal_instance)


""" Fire Effect
This is the main Fire effect area
"""
class Fire(ParticleSystem):
	fire_sound = pygame.mixer.Sound('sounds/fire.wav')
	total_particles = 500 # count how many particles should be generated before ending the instance

	def __init__(self, game, target):
		self.game = game
		Fire.fire_sound.play()
		self.starting_particles = 70 # number of starting particles and number of particles to exist at one time
		ParticleSystem.__init__(self, target)

	def generate_particle(self):
		# if the total number of particles to exist is not reached, create one and add to the particle number 
		if self.particles <= self.total_particles:
			FireParticle(self.game, self)
			self.particles += 1


""" Fire Particle
This is an individual particle of the Fire effect
"""
class FireParticle(Particle):
	def __init__(self, game, fire_instance):
		self.particle_system_instance = fire_instance
		fire_particle_image_path = development.Path.root + 'images/fire-particle.png'
		self.image_orginal = pygame.image.load(fire_particle_image_path).convert_alpha()

		# random move speed
		self.y_move_speed = random.uniform(-1, -4)
		self.x_move_speed = random.uniform(0.1, 0.15)

		# randomize position based on the size of the main ParticleSystem instance
		self.x = self.particle_system_instance.x + random.uniform(0, self.particle_system_instance.width)
		self.y = self.particle_system_instance.y + random.uniform(0, self.particle_system_instance.height + 30)

		# randomize size - range: 33% of the image src size to 100% of the image size
		self.size = random.uniform((self.image_orginal.get_width() / 3), self.image_orginal.get_width())
		self.size = int(round(self.size)) # transform doesn't like floats

		#random fade speed - range can be 1 to 255 (255 would be instance)
		self.fade_speed = random.uniform(40, 90)

		# random direction (1 is left, -1 is right)
		self.x_move_direction = random.choice([0.1, -0.1])

		Particle.__init__(self, game, fire_instance)		