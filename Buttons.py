
"""
	Defaults:
		1. The default "text color" is 'white' with transparent background
"""

import os

from pygame import draw 	# To draw a border around the button
from pygame import Rect 	# To work with the rectangle
from pygame import mouse 	# To work with mouse
from pygame import mixer  	# To work with sound
from pygame import sprite  	# To work with groups
from pygame.locals import *  # To work with events

class Button(sprite.Sprite):

	def __init__(self, center_pos, txt=None, font=None, img=None):
		super().__init__()

		# Arguments
		self.position = center_pos
		self.text = txt
		self.font = font
		self.img = img

		# Colors
		self.text_color = "white"

		# State/Signal
		self.is_clicked = False

		# Sounds
		self.CLICK_SOUND = mixer.Sound(os.path.join("Assets", "Sounds", "Clicking Sound.wav"))
		self.CLICK_SOUND.set_volume(0.1)

		# Button
		self.image = self.img.convert_alpha() if self.img else self.font.render(self.text, True, self.text_color)
		self.rect = self.image.get_rect( center=self.position )	

	def update(self, events):
		
		for event in events:

			# Checking Hovering
			if self.img:
				if event.type == MOUSEMOTION and self.rect.collidepoint(event.pos):
					pass
				else:
					pass
			else:
				if event.type == MOUSEMOTION and self.rect.collidepoint(event.pos):
					self.set_text_color("green")
				else:
					self.set_text_color("white")

			# Checking Clicking
			if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
				self.set_text_color("green")
				self.CLICK_SOUND.play()
				self.is_clicked = True

	# For text 
	def set_text_color(self, new_color):
		self.text_color = new_color
		self.image = self.font.render(self.text, True, self.text_color)



