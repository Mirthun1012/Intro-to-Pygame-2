import pygame
import os

from Files.Buttons import Button
from Files.Screens import Screen
from Files.Game_Variables import *


class Intro_Screen(Screen):

	def __init__(self, screen):
		super().__init__(screen)

		self.run = True
		self.events = None
		self.screen = screen

		# Back Ground
		self.BG = pygame.image.load(os.path.join("Assets", "space.png")).convert()  
		self.BG = pygame.transform.scale(self.BG, (WIDTH, HEIGHT))

		# Title
		self.S = pygame.font.Font(os.path.join("Assets", "Font.ttf"), 300).render("S", False, WHITE)
		self.S_RECT = self.S.get_rect( topleft=(180, -40) )

		self.space = pygame.font.Font(os.path.join("Assets", "Font.ttf"), 100).render("PACE", True, WHITE)
		self.SPACE_RECT = self.space.get_rect( topleft = (self.S_RECT.right+10, self.S_RECT.top+83) )

		self.shooters = pygame.font.Font(os.path.join("Assets", "Font.ttf"), 100).render("HOOTERS", True, WHITE)
		self.SHOOTERS_RECT = self.shooters.get_rect(midleft = (self.S_RECT.right+12, self.SPACE_RECT.bottom+22))
		
		# Buttons
		self.Start_Button = Button((450, 341), "Start Game", pygame.font.Font(os.path.join("Assets", "Font.ttf"), 67))
		self.Exit_Button = Button((450, 449), "Exit", pygame.font.Font(os.path.join("Assets", "Font.ttf"), 50))

		self.buttons = pygame.sprite.Group(self.Start_Button, self.Exit_Button)

	def event_manager(self):
		
		for event in self.events:

			if event.type == pygame.QUIT:
				self.run = False

	def changes(self):
		
		# Buttons
		self.buttons.update(self.events)

		if self.Start_Button.is_clicked:
			pygame.event.post(pygame.event.Event(CHANGE_TO_MAIN))

		elif self.Exit_Button.is_clicked:
			self.run = False
		

	def draw_and_display(self):

		self.screen.blit(self.BG, (0, 0))

		# Title
		self.screen.blit(self.S, self.S_RECT)
		self.screen.blit(self.space, self.SPACE_RECT)
		self.screen.blit(self.shooters, self.SHOOTERS_RECT)

		self.buttons.draw(self.screen)

		pygame.display.update()

	def update(self, events):
		self.events = events

		self.event_manager()
		self.changes()
		self.draw_and_display()
