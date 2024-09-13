
class Screen():

	def __init__(self, screen):
		self.run = True
		self.events = None
		self.screen = screen

	def event_manager(self):
		
		for event in self.events:

			if event.type == pygame.QUIT:
				self.run = False

	def changes(self):
		pass

	def draw_and_display(self):
		pygame.display.update()

	def update(self, events):
		self.events = events

		self.event_manager()
		self.changes()
		self.draw_and_display()