import pygame
import os

from random import choice, randint

from Files.Timers import Timer

from Files.Game_Variables import *
from Files.Main_Screen.Main_Screen_Variables import *

class Power_Up(pygame.sprite.Sprite):

	def __init__(self, spaceship):
		super().__init__()

		# Sound
		self.CLAIM_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "Claiming Sound.mp3"))
		self.CLAIM_SOUND.set_volume(0.3)

		self.group = spaceship
		self.type = choice(["Health", "Ammo", "Speed Up"])
	
		self.timers = { "Ammo": Timer(5*1000), "Speed Up": Timer(6*1000) }
 
		self.image = pygame.image.load(os.path.join("Assets", "Power_Ups", self.type+".png")).convert_alpha()
		self.rect = self.image.get_rect( topleft = (WIDTH, HEIGHT)) # Hiding it!

		# Positioning it!
		self.size = self.rect.width 	# width == height
		self.positioning()

	def positioning(self): 
		# topleft coordinates
		x, y = 0, 0

		if self.group == "yellow":
			x, y = randint(0, BORDER.left-self.size), randint(0, HEIGHT-self.size)
			self.rect.topleft = (x, y)

			while self.is_overlap():
				x, y = randint(0, self.BORDER.left-self.size), randint(0, HEIGHT-self.size)
				self.rect.topleft = (x, y)

		elif self.group == "red":
			x, y = randint(BORDER.right, WIDTH-self.size), randint(0, HEIGHT-self.size)
			self.rect.topleft = (x, y)

			while self.is_overlap():
				x, y = randint(BORDER.right, WIDTH-self.size), randint(0, HEIGHT-self.size)
				self.rect.topleft = (x, y)

	def is_overlap(self):

		if self.group == "yellow":

			# Checking with its own spaceship
			if self.rect.colliderect(YELLOW_SPACESHIP.sprite.rect):
				return True

			# checking with other powerups
			if pygame.sprite.spritecollide(self, Power_Ups_Yellow, False):
				return True

		elif self.group == "red":

			# Checking with its own spaceship
			if self.rect.colliderect(RED_SPACESHIP.sprite.rect):
				return True

			# checking with other powerups
			if pygame.sprite.spritecollide(self, Power_Ups_Red, False):
				return True

		# collide with nothing
		return False		

	# Effects
	def is_claiming(self):
		if self.group == "red": 
			if self.rect.colliderect(RED_SPACESHIP.sprite.rect):
				self.CLAIM_SOUND.play()
				return True

		elif self.group == "yellow":
			if self.rect.colliderect(YELLOW_SPACESHIP.sprite.rect):
				self.CLAIM_SOUND.play()
				return True

	def activate(self):

		if self.group== "red":
			# Claiming the powerup
			if self.is_claiming():
				
				# Which Powerup
				if self.type == "Health":
					RED_SPACESHIP.sprite.health += 2
					if RED_SPACESHIP.sprite.health > RED_SPACESHIP.sprite.OG_HEALTH:
						RED_SPACESHIP.sprite.health = RED_SPACESHIP.sprite.OG_HEALTH
					self.kill()

				if self.type == "Ammo":
					RED_SPACESHIP.sprite.max_bullets = RED_SPACESHIP.sprite.OG_MAX_BULLETS + 2
					self.timers[self.type].activate()
					self.rect = self.image.get_rect( topleft = (WIDTH+5, HEIGHT+5) ) # Hide

				if self.type == "Speed Up":
					RED_SPACESHIP.sprite.velocity = RED_SPACESHIP.sprite.OG_VELOCITY + 2
					self.timers[self.type].activate()
					self.rect = self.image.get_rect( topleft = (WIDTH+5, HEIGHT+5) ) # Hide

		elif self.group == "yellow":
			# Claiming the powerup
			if self.is_claiming():

				# Which Powerup
				if self.type == "Health":
					YELLOW_SPACESHIP.sprite.health += 2
					if YELLOW_SPACESHIP.sprite.health > YELLOW_SPACESHIP.sprite.OG_HEALTH:
						YELLOW_SPACESHIP.sprite.health = YELLOW_SPACESHIP.sprite.OG_HEALTH
					self.kill()

				if self.type == "Ammo":
					YELLOW_SPACESHIP.sprite.max_bullets = YELLOW_SPACESHIP.sprite.OG_MAX_BULLETS + 2
					self.timers[self.type].activate()
					self.rect = self.image.get_rect( topleft = (WIDTH+5, HEIGHT+5) ) # Hide

				if self.type == "Speed Up":
					YELLOW_SPACESHIP.sprite.velocity = YELLOW_SPACESHIP.sprite.OG_VELOCITY + 2
					self.timers[self.type].activate()
					self.rect = self.image.get_rect( topleft = (WIDTH+5, HEIGHT+5) ) # Hide

	def deactivate(self):
		self.timers[self.type].update()

		# Deactivating
		if not self.timers[self.type].active:

			if self.group == "red":

				if self.type == "Ammo":
					RED_SPACESHIP.sprite.max_bullets = RED_SPACESHIP.sprite.OG_MAX_BULLETS
					self.kill()

				if self.type == "Speed Up":
					RED_SPACESHIP.sprite.velocity = RED_SPACESHIP.sprite.OG_VELOCITY
					self.kill()

			elif self.group == "yellow":
				
				if self.type == "Ammo":
					YELLOW_SPACESHIP.sprite.max_bullets = YELLOW_SPACESHIP.sprite.OG_MAX_BULLETS
					self.kill()

				if self.type == "Speed Up":
					YELLOW_SPACESHIP.sprite.velocity = YELLOW_SPACESHIP.sprite.OG_VELOCITY
					self.kill()

	def update(self):
		self.activate()
		if self.type != "Health" and self.timers[self.type].active:
			self.deactivate()