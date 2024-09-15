import pygame
import os

from random import randint

from Files.Screens import Screen

from Files.Game_Variables import *
from Files.Main_Screen.Main_Screen_Variables import *

from Files.Main_Screen.Bullets import Bullet
from Files.Main_Screen.Power_Ups import Power_Up


class Main_Screen(Screen):

	def __init__(self, screen):
		super().__init__(screen)

		self.run = True
		self.events = None
		self.screen = screen

		# Restarting Spaceship and Power ups
		RED_SPACESHIP.sprite.restart(SPAWNING_LOC[1])
		YELLOW_SPACESHIP.sprite.restart(SPAWNING_LOC[0])

		Power_Ups_Red.empty()
		Power_Ups_Yellow.empty()

		# Sounds
		self.FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "Fire.mp3"))
		self.DEAD_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "Dead.wav"))
		self.SPAWN_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "Spawning Sound.mp3"))

		# BG Music
		self.BG_MUSIC = pygame.mixer.music.load(os.path.join("Assets", "Musics", "For Main Screen.ogg"))
		pygame.mixer.music.set_volume(0.3)
		pygame.mixer.music.play(-1)

		# Timers
		self.SPAWN_POWERUP_RED = pygame.event.custom_type()
		self.SPAWN_POWERUP_YELLOW = pygame.event.custom_type()

		pygame.time.set_timer(self.SPAWN_POWERUP_RED, randint(8*1000, 20*1000))    
		pygame.time.set_timer(self.SPAWN_POWERUP_YELLOW, randint(8*1000, 20*1000))

		# Font
		self.HEALTH_FONT = pygame.font.Font(os.path.join("Assets", "Font.ttf"), 100)

		# BG
		self.BG = pygame.image.load(os.path.join("Assets", "space.jpg")).convert()
		self.BG = pygame.transform.scale(self.BG, (WIDTH, HEIGHT))

		# Bullets
		self.Red_bullets = pygame.sprite.Group()
		self.Yellow_bullets = pygame.sprite.Group()

		# Health
		self.YELLOW_HEALTH = self.HEALTH_FONT.render(str(YELLOW_SPACESHIP.sprite.health), True, YELLOW)
		self.RED_HEALTH = self.HEALTH_FONT.render(str(RED_SPACESHIP.sprite.health), True, RED)

		self.RED_HEALTH_RECT = self.RED_HEALTH.get_rect( center = SPAWNING_LOC[1] )
		self.YELLOW_HEALTH_RECT = self.YELLOW_HEALTH.get_rect( center = SPAWNING_LOC[0] )

		

	def event_manager(self):

		for eve in self.events:

			# Quitting
			if eve.type == pygame.QUIT:
				self.run = False

			# Firing!
			if eve.type == pygame.KEYDOWN:
				if eve.key == pygame.K_LCTRL and len(self.Yellow_bullets.sprites()) < YELLOW_SPACESHIP.sprite.max_bullets:
					self.Yellow_bullets.add( Bullet(YELLOW_SPACESHIP.sprite.rect.midright, "yellow") )
					self.FIRE_SOUND.play()

				if eve.key == pygame.K_RCTRL and len(self.Red_bullets.sprites()) < RED_SPACESHIP.sprite.max_bullets:
					self.Red_bullets.add( Bullet(RED_SPACESHIP.sprite.rect.midleft, "red") )
					self.FIRE_SOUND.play()

			# Spawning Power Ups!
			if eve.type == self.SPAWN_POWERUP_RED:
				if len(Power_Ups_Red.sprites()) < MAX_POWERUPS:
					Power_Ups_Red.add(Power_Up("red"))
					self.SPAWN_SOUND.play()

			if eve.type == self.SPAWN_POWERUP_YELLOW:
				if len(Power_Ups_Yellow.sprites()) < MAX_POWERUPS:
					Power_Ups_Yellow.add(Power_Up("yellow"))
					self.SPAWN_SOUND.play()

	def changes(self):

		# Updates
		self.Red_bullets.update()
		self.Yellow_bullets.update()

		RED_SPACESHIP.update(self.Red_bullets, self.Yellow_bullets)
		YELLOW_SPACESHIP.update(self.Red_bullets, self.Yellow_bullets)

		Power_Ups_Red.update()
		Power_Ups_Yellow.update()

		# healths
		self.YELLOW_HEALTH = self.HEALTH_FONT.render(str(YELLOW_SPACESHIP.sprite.health), True, YELLOW)
		self.RED_HEALTH = self.HEALTH_FONT.render(str(RED_SPACESHIP.sprite.health), True, RED)

		# checking if anybody wins
		if RED_SPACESHIP.sprite.health == 0:
			self.DEAD_SOUND.play()
			pygame.mixer.music.unload()
			pygame.event.post(pygame.event.Event(CHANGE_TO_OUTRO, {"won_spaceship": "Yellow"}))
		
		elif YELLOW_SPACESHIP.sprite.health == 0:
			self.DEAD_SOUND.play()
			pygame.mixer.music.unload()
			pygame.event.post(pygame.event.Event(CHANGE_TO_OUTRO, {"won_spaceship": "Red"}))
			
	def draw_and_display(self):
		# BG
		self.screen.blit(self.BG, (0,0))
		pygame.draw.rect(self.screen, BLACK, BORDER)

		# bullets
		self.Yellow_bullets.draw(self.screen)
		self.Red_bullets.draw(self.screen)

		# healths
		self.screen.blit(self.YELLOW_HEALTH, self.YELLOW_HEALTH_RECT)
		self.screen.blit(self.RED_HEALTH, self.RED_HEALTH_RECT)

		# power ups
		Power_Ups_Red.draw(self.screen)
		Power_Ups_Yellow.draw(self.screen)

		# spaceships
		RED_SPACESHIP.draw(self.screen)
		YELLOW_SPACESHIP.draw(self.screen)

		# Displaying
		pygame.display.update()

	def update(self, events):
		self.events = events

		self.event_manager()
		self.changes()
		self.draw_and_display()