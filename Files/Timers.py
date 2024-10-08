"""
	Post-Conditions:
		1. Ensure that the func `activate` get called only one time!
		2. Check for deactivation in a following way:
			`if <Timer>.update() == False:
				<body>`
			(When using this, The `False` will be emitated only one time next it starts to emit `None`)
		
"""

from pygame.time import get_ticks

class Timer():

	def __init__(self, duration, auto_start = False):

		self.start_time = 0
		self.duration = duration
		self.active = False

		if auto_start:
			self.activate()

	def activate(self):
		self.start_time = get_ticks()
		self.active = True

	def deactivate(self):
		self.start_time = 0
		self.active = False

	def update(self):
		if self.active:
			current_time = get_ticks()

			if current_time - self.start_time >= self.duration:
				self.deactivate()

			return self.active
	
