"""
	NOTE:
		
		
	
"""

import pygame
import os
from random import randint, choice
from Timers import Timer

pygame.init()


# Screen
WIDTH, HEIGHT = 900, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# FPS
CLOCK = pygame.time.Clock()
FPS = 60


# BG
BG = pygame.image.load(os.path.join("Assets", "space.png"))
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))


class SpaceShip(pygame.sprite.Sprite):

	def __init__(self, surface, pos, type, BORDER):
		super().__init__()

		self.position = pos
		self.type = type
		self.health = 10
		self.velocity = 3		
		self.max_bullets = 3

		# For powerups
		self.OG_HEALTH = 10
		self.OG_VELOCITY = 3
		self.OG_MAX_BULLETS = 3

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

	def update(self, Red_bullets, Yellow_bullets, game_state):
		if game_state == "playing":
			self.movement()
			self.checking_collision(Red_bullets, Yellow_bullets)
		else:
			self.__init__(self.image, SPAWNING_LOC[0] if self.type == "yellow" else SPAWNING_LOC[1], self.type)

class Bullet(pygame.sprite.Sprite):

	def __init__(self, position, bullet_type):
		super().__init__()

		self.position = position
		self.bullet_type = bullet_type

		self.VELOCITY = 7

		self.image = pygame.image.load(os.path.join("Assets", "Bullet.png")).convert_alpha()
		self.rect = self.image.get_rect(center = self.position)

	def movement(self):
		if self.bullet_type == "yellow":
			self.rect.x += self.VELOCITY

			if self.rect.x > WIDTH:
				self.kill()

		elif self.bullet_type == "red":
			self.rect.x -= self.VELOCITY

			if self.rect.right < 0:
				self.kill()

	def update(self):
		self.movement()

class Power_Up(pygame.sprite.Sprite):

	def __init__(self, spaceship):
		super().__init__()

		# Sound
		self.CLAIM_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "Claiming Sound.mp3"))

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
			x, y = randint(0, self.BORDER.left-self.size), randint(0, HEIGHT-self.size)
			self.rect.topleft = (x, y)

			while self.is_overlap():
				x, y = randint(0, self.BORDER.left-self.size), randint(0, HEIGHT-self.size)
				self.rect.topleft = (x, y)

		elif self.group == "red":
			x, y = randint(self.BORDER.right, WIDTH-self.size), randint(0, HEIGHT-self.size)
			self.rect.topleft = (x, y)

			while self.is_overlap():
				x, y = randint(self.BORDER.right, WIDTH-self.size), randint(0, HEIGHT-self.size)
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
				CLAIM_SOUND.play()
				return True

		elif self.group == "yellow":
			if self.rect.colliderect(YELLOW_SPACESHIP.sprite.rect):
				CLAIM_SOUND.play()
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


# Signals
CHANGE_TO_OUTRO = pygame.event.custom_type()



class Screen():

	def __init__(self):
		self.run = True

	def event_manager(self, events):
		pass

	def changes(self):
		pass

	def draw_and_display(self):
		pass

	def update(self, events):
		self.event_manager(events)
		self.changes()
		self.draw_and_display()

class Main_Screen(Screen):

	def __init__(self):
		super().__init__()

		self.run = True

		# Sounds
		self.FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "Fire.mp3"))
		self.DEAD_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "Dead.wav"))
		self.SPAWN_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "Spawning Sound.mp3"))

		# Timers
		self.SPAWN_POWERUP_RED = pygame.event.custom_type()
		self.SPAWN_POWERUP_YELLOW = pygame.event.custom_type()

		# Font
		self.HEALTH_FONT = pygame.font.SysFont("comicsans", 30)
		self.WIN_FONT = pygame.font.SysFont("comicsans", 100)
		self.TITLE_FONT = pygame.font.SysFont("fixedsys", 50)

		# Border
		self.BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)

		# Spaceships
		self.SPAWNING_LOC = [ ((WIDTH//2)-300, HEIGHT//2), ((WIDTH//2)+300 , HEIGHT//2) ] # For Center Argument 

		self.YELLOW_SPACESHIP = SpaceShip(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "spaceship_yellow.png")), 90), self.SPAWNING_LOC[0], "yellow", self.BORDER)
		self.YELLOW_SPACESHIP = pygame.sprite.GroupSingle(sprite = self.YELLOW_SPACESHIP)
		self.RED_SPACESHIP = SpaceShip(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "spaceship_red.png")), -90), self.SPAWNING_LOC[1], "red", self.BORDER)
		self.RED_SPACESHIP = pygame.sprite.GroupSingle(sprite = self.RED_SPACESHIP)

		# Bullets
		self.Red_bullets = pygame.sprite.Group()
		self.Yellow_bullets = pygame.sprite.Group()

		# Power Ups
		self.MAX_POWERUPS = 3

		self.Power_Ups_Red = pygame.sprite.Group()
		self.Power_Ups_Yellow = pygame.sprite.Group()

	def event_manager(self, events):

		for eve in events:

			# Quitting
			if eve.type == pygame.QUIT:
				self.run = False

			# Firing!
			if eve.type == pygame.KEYDOWN:
				if eve.key == pygame.K_LCTRL and len(self.Yellow_bullets.sprites()) < self.YELLOW_SPACESHIP.sprite.max_bullets:
					self.Yellow_bullets.add( Bullet(self.YELLOW_SPACESHIP.sprite.rect.midright, "yellow") )
					self.FIRE_SOUND.play()

				if eve.key == pygame.K_RCTRL and len(self.Red_bullets.sprites()) < self.RED_SPACESHIP.sprite.max_bullets:
					self.Red_bullets.add( Bullet(self.RED_SPACESHIP.sprite.rect.midleft, "red") )
					self.FIRE_SOUND.play()

			# Spawning Power Ups!
			# if eve.type == SPAWN_POWERUP_RED:
			# 	if len(self.Power_Ups_Red.sprites()) < self.MAX_POWERUPS:
			# 		self.Power_Ups_Red.add(Power_Up("red"))
			# 		self.SPAWN_SOUND.play()

			# if eve.type == SPAWN_POWERUP_YELLOW:
			# 	if len(self.Power_Ups_Yellow.sprites()) < self.MAX_POWERUPS:
			# 		self.Power_Ups_Yellow.add(Power_Up("yellow"))
			# 		self.SPAWN_SOUND.play()

	def changes(self):

		# Updates
		self.Red_bullets.update()
		self.Yellow_bullets.update()

		self.RED_SPACESHIP.update(self.Red_bullets, self.Yellow_bullets, "playing")
		self.YELLOW_SPACESHIP.update(self.Red_bullets, self.Yellow_bullets, "playing")

		self.Power_Ups_Red.update()
		self.Power_Ups_Yellow.update()

		# checking if anybody wins
		if RED_SPACESHIP.sprite.health == 0:
			DEAD_SOUND.play()
			pygame.event.post(pygame.event.Event(CHANGE_TO_OUTRO, {"won_spaceship": "Yellow"}))
		
		elif YELLOW_SPACESHIP.sprite.health == 0:
			DEAD_SOUND.play()
			pygame.event.post(pygame.event.Event(CHANGE_TO_OUTRO, {"won_spaceship": "Red"}))
			
	def draw_and_display(self):
		# BG
		screen.blit(BG, (0,0))
		pygame.draw.rect(screen, BLACK, self.BORDER)

		# bullets
		self.Yellow_bullets.draw(screen)
		self.Red_bullets.draw(screen)

		# healths
		YELLOW_HEALTH = self.HEALTH_FONT.render("Health: "+str(self.YELLOW_SPACESHIP.sprite.health), True, WHITE)
		RED_HEALTH = self.HEALTH_FONT.render("Health: "+str(self.RED_SPACESHIP.sprite.health), True, WHITE)

		RED_HEALTH_RECT = RED_HEALTH.get_rect( topright = (WIDTH-10, 10) ) # For ease the access of positioning

		screen.blit(YELLOW_HEALTH, (10, 10))
		screen.blit(RED_HEALTH, RED_HEALTH_RECT)

		# power ups
		self.Power_Ups_Red.draw(screen)
		self.Power_Ups_Yellow.draw(screen)

		# spaceships
		self.RED_SPACESHIP.draw(screen)
		self.YELLOW_SPACESHIP.draw(screen)

		# Displaying
		pygame.display.update()

	def update(self, events):
		self.event_manager(events)
		self.changes()
		self.draw_and_display()

# pygame.time.set_timer(SPAWN_POWERUP_RED, randint(8*1000, 20*1000))    # TEST
# pygame.time.set_timer(SPAWN_POWERUP_YELLOW, randint(8*1000, 20*1000))  # TEST




# Outro Screen
# def outro(self):

# 	#drawing the winning message
# 	WIN = WIN_FONT.render(self.won_spaceship+" Wins", True, RED if self.won_spaceship == "Red" else YELLOW)
# 	WIN_RECT = WIN.get_rect(center = (WIDTH/2, HEIGHT/2))

# 	screen.blit(WIN, WIN_RECT)

# 	self.outro_wait.update()

# 	# restart mechanics
# 	if not self.outro_wait.active:

# 		Red_bullets.empty()
# 		Yellow_bullets.empty()

# 		RED_SPACESHIP.update(Red_bullets, Yellow_bullets, "restart")
# 		YELLOW_SPACESHIP.update(Red_bullets, Yellow_bullets, "restart")

# 		Power_Ups_Red.empty()
# 		Power_Ups_Yellow.empty()

# 		self.state = "Main Screen"



	


def main():

	intro_screen = None
	main_screen = Main_Screen()
	outro_screen = None

	current_screen = main_screen
	

	# Game loop
	while current_screen.run:

		# getting events
		events = pygame.event.get()
		

		# Getting signals to change the current screen!
		for signal in events:
			pass


		current_screen.update(events)


		CLOCK.tick(FPS)


	pygame.quit()


if __name__ == "__main__":
	main()