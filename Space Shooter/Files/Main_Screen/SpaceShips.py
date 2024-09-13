import pygame
import os

from Files.Game_Variables import *

pygame.init()

class SpaceShip(pygame.sprite.Sprite):

	def __init__(self, surface, pos, type, BORDER):
		super().__init__()

		self.position = pos
		self.type = type
		self.health = 10
		self.velocity = 3		
		self.max_bullets = 3

		# For powerups and restarting
		self.OG_HEALTH = 10
		self.OG_VELOCITY = 3
		self.OG_MAX_BULLETS = 3
		self.OG_POSITION = pos

		# For border
		self.BORDER = BORDER

		# Sounds
		self.HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "Hit.mp3"))

		self.image = surface.convert_alpha()
		self.rect = self.image.get_rect(center = self.position)

	def movement(self):
		keys_pressed = pygame.key.get_pressed()

		if self.type == "yellow":
			# LEFT
			if keys_pressed[pygame.K_a] and self.rect.left - self.velocity > 0:
				self.rect.left -= self.velocity
			# DOWN
			if keys_pressed[pygame.K_s] and self.rect.bottom + self.velocity < HEIGHT:
				self.rect.bottom += self.velocity
			# RIGHT
			if keys_pressed[pygame.K_d] and self.rect.right + self.velocity < self.BORDER.left:
				self.rect.right += self.velocity
			# UP
			if keys_pressed[pygame.K_w] and self.rect.top - self.velocity > 0:
				self.rect.top -= self.velocity

		else:
			# LEFT
			if keys_pressed[pygame.K_LEFT] and self.rect.left - self.velocity > self.BORDER.right:
				self.rect.left -= self.velocity
			# DOWN
			if keys_pressed[pygame.K_DOWN] and self.rect.bottom + self.velocity < HEIGHT:
				self.rect.bottom += self.velocity
			# RIGHT
			if keys_pressed[pygame.K_RIGHT] and self.rect.right + self.velocity < WIDTH:
				self.rect.right += self.velocity
			# UP
			if keys_pressed[pygame.K_UP] and self.rect.top - self.velocity > 0:
				self.rect.top -= self.velocity

	def checking_collision(self, Red_bullets, Yellow_bullets):

		group = Yellow_bullets if self.type == "red" else Red_bullets

		if pygame.sprite.spritecollide(self, group, True):
			if self.health > 0:
				self.health -= 1
				self.HIT_SOUND.play()

	def update(self, Red_bullets, Yellow_bullets):
		self.movement()
		self.checking_collision(Red_bullets, Yellow_bullets)

	def restart(self, pos):
		self.health = self.OG_HEALTH
		self.velocity = self.OG_VELOCITY
		self.max_bullets = self.OG_MAX_BULLETS
		self.position = pos

		self.rect = self.image.get_rect(center = self.position)
