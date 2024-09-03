import pygame
import os

from Files.Buttons import Button
from Files.Screens import Screen
from Files.Game_Variables import *


class Outro_Screen(Screen):

	def __init__(self, won_spaceship, screen):
		super().__init__(screen)

		self.run = True
		self.events = None
		self.screen = screen

		# Variables
		self.won_spaceship = won_spaceship

		# Fonts
		self.WIN_FONT = pygame.font.Font(os.path.join("Assets", "Font.ttf"), 150)

		# Winning message ( Will Update in `changes` func )
		self.win_message = None
		self.win_message_rect = None

		# Buttons
		self.RESTART_BUTTON = Button((450, 291), "Restart", pygame.font.Font(os.path.join("Assets", "Font.ttf"), 50))
		self.MENU_BUTTON = Button((450, 291+116), "Menu", pygame.font.Font(os.path.join("Assets", "Font.ttf"), 50))

		self.buttons = pygame.sprite.Group(self.RESTART_BUTTON, self.MENU_BUTTON)

	def event_manager(self):
		
		for event in self.events:

			if event.type == pygame.QUIT:
				self.run = False

	def changes(self):
		
		# Wining Message
		self.win_message = self.WIN_FONT.render(self.won_spaceship+" Wins", True, RED if self.won_spaceship == "Red" else YELLOW)
		self.win_message_rect = self.win_message.get_rect(center = ( (WIDTH/2 + 12) if self.won_spaceship == "Red" else (WIDTH/2 + 3) , HEIGHT/2 - 100))

		# Buttons
		self.buttons.update(self.events)

		if self.RESTART_BUTTON.is_clicked:
			pygame.event.post(pygame.event.Event(CHANGE_TO_MAIN))

		elif self.MENU_BUTTON.is_clicked:
			pass


	def draw_and_display(self):

		# Win Message
		self.screen.blit(self.win_message, self.win_message_rect)

		# Buttons
		self.buttons.draw(self.screen)
		
		pygame.display.update()

	def update(self, events):
		self.events = events

		self.event_manager()
		self.changes()
		self.draw_and_display()