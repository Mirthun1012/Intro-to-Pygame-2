"""
	NOTE:

		REMEMBER: 1. SAVE/CLOSE THE FILES BEFORE COMMITING
				  2. I AM UPLOADING THIS GAME TO ITCH.IO (AS THIS IS MY FIRST WEALTH THROUGH CODE-LEVERAGE)
		
		TO DO:
			1. Understanding My Outline of this game!
			2. Update the files in Git-Hub, to make it up-to-date!
			3. Resolving the health-text-bug in main screen
		
"""

import pygame
import os

from Files.Game_Variables import *


def main():

	pygame.init()

	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Space Shooters")

	from Files.Main_Screen.Main_Screens import Main_Screen
	from Files.Outro_Screen.Outro_Screens import Outro_Screen
	from Files.Intro_Screen.Intro_Screens import Intro_Screen

	current_screen = Intro_Screen(screen)

	# Game loop
	while current_screen.run:

		# getting events
		events = pygame.event.get()
		

		# Getting signals to change the current screen!
		for signal in events:

			# Changing to Outro screen			
			if signal.type == CHANGE_TO_OUTRO:
				current_screen = Outro_Screen(signal.won_spaceship, screen)

			# Changing to Main screen
			elif signal.type == CHANGE_TO_MAIN:
				current_screen = Main_Screen(screen)

			elif signal.type == CHANGE_TO_INTRO:
				current_screen = Intro_Screen(screen)


		current_screen.update(events)


		CLOCK.tick(FPS)


	pygame.quit()


if __name__ == "__main__":
	main()