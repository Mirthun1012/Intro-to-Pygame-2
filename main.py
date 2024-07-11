"""
	NOTE:
		
		Adding the intro screen!
 
		Updating this game as a project from a single file!! (completed)

		------------------

		In the proces of making intro screen func in game manager!

		Before that.. Solve the bugs in the Game Manager class with main and outro screen! (completed)
	
"""

import pygame
import os
from random import randint, choice
from Timers import Timer

pygame.init()


# Screen
WIDTH, HEIGHT = 900, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Sounds
HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "Hit.mp3"))
FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "Fire.mp3"))
DEAD_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "Dead.wav"))
CLAIM_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "Claiming Sound.mp3"))
SPAWN_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "Spawning Sound.mp3"))


# Timers
SPAWN_POWERUP_RED = pygame.USEREVENT + 1
SPAWN_POWERUP_YELLOW = pygame.USEREVENT + 2

pygame.time.set_timer(SPAWN_POWERUP_RED, randint(8*1000, 20*1000))    # TEST
pygame.time.set_timer(SPAWN_POWERUP_YELLOW, randint(8*1000, 20*1000))  # TEST


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# FPS
CLOCK = pygame.time.Clock()
FPS = 60

# Font
HEALTH_FONT = pygame.font.SysFont("comicsans", 30)
WIN_FONT = pygame.font.SysFont("comicsans", 100)
TITLE_FONT = pygame.font.SysFont("fixedsys", 50)


# BG
BG = pygame.image.load(os.path.join("Assets", "space.png"))
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))


# Border
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)


# Spaceships
SPAWNING_LOC = [ ((WIDTH//2)-300, HEIGHT//2), ((WIDTH//2)+300 , HEIGHT//2) ] # For Center Argument 

class SpaceShip(pygame.sprite.Sprite):

	def __init__(self, surface, pos, type):
		super().__init__()

		self.position = pos
		self.type = type
		self.health = 10
		self.velocity = 3		
		self.max_bullets = 3

		# for powerups
		self.OG_HEALTH = 10
		self.OG_VELOCITY = 3
		self.OG_MAX_BULLETS = 3

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
			if keys_pressed[pygame.K_d] and self.rect.right + self.velocity < BORDER.left:
				self.rect.right += self.velocity
			# UP
			if keys_pressed[pygame.K_w] and self.rect.top - self.velocity > 0:
				self.rect.top -= self.velocity

		else:
			# LEFT
			if keys_pressed[pygame.K_LEFT] and self.rect.left - self.velocity > BORDER.right:
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
				HIT_SOUND.play()

	def update(self, Red_bullets, Yellow_bullets, game_state):
		if game_state == "playing":
			self.movement()
			self.checking_collision(Red_bullets, Yellow_bullets)
		else:
			self.__init__(self.image, SPAWNING_LOC[0] if self.type == "yellow" else SPAWNING_LOC[1], self.type)

YELLOW_SPACESHIP = SpaceShip(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "spaceship_yellow.png")), 90), SPAWNING_LOC[0], "yellow")
YELLOW_SPACESHIP = pygame.sprite.GroupSingle(sprite = YELLOW_SPACESHIP)

RED_SPACESHIP = SpaceShip(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "spaceship_red.png")), -90), SPAWNING_LOC[1], "red")
RED_SPACESHIP = pygame.sprite.GroupSingle(sprite = RED_SPACESHIP)


# Bullets
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

Red_bullets = pygame.sprite.Group()
Yellow_bullets = pygame.sprite.Group()


# Power Ups
MAX_POWERUPS = 3

class Power_Up(pygame.sprite.Sprite):

	def __init__(self, spaceship):
		super().__init__()

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
				x, y = randint(0, BORDER.left-self.size), randint(0, HEIGHT-self.size)
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

Power_Ups_Red = pygame.sprite.Group()
Power_Ups_Yellow = pygame.sprite.Group()


# Game Manager
class Game_Manager():

	def __init__(self):
		self.state = "Intro"
		self.run = True

		# Signals for Outro
		self.won_spaceship = ""
		self.outro_wait = Timer(3*1000)

	def event_loop(self):

		for eve in pygame.event.get():

			if eve.type == pygame.QUIT:
				self.run = False

			elif self.state == "Main Screen":

				# Firing!
				if eve.type == pygame.KEYDOWN:
					if eve.key == pygame.K_LCTRL and len(Yellow_bullets.sprites()) < YELLOW_SPACESHIP.sprite.max_bullets:
						Yellow_bullets.add( Bullet(YELLOW_SPACESHIP.sprite.rect.midright, "yellow") )
						FIRE_SOUND.play()

					if eve.key == pygame.K_RCTRL and len(Red_bullets.sprites()) < RED_SPACESHIP.sprite.max_bullets:
						Red_bullets.add( Bullet(RED_SPACESHIP.sprite.rect.midleft, "red") )
						FIRE_SOUND.play()

				# Spawning Power Ups!
				if eve.type == SPAWN_POWERUP_RED:
					if len(Power_Ups_Red.sprites()) < MAX_POWERUPS:
						Power_Ups_Red.add(Power_Up("red"))
						SPAWN_SOUND.play()

				if eve.type == SPAWN_POWERUP_YELLOW:
					if len(Power_Ups_Yellow.sprites()) < MAX_POWERUPS:
						Power_Ups_Yellow.add(Power_Up("yellow"))
						SPAWN_SOUND.play()


	def intro(self):
		
		# BG
		screen.blit(BG, (0, 0))

		TITLE_FONT.render("SPACE", True, WHITE)


	# Main Screen
	def main_screen(self):

		# Updates
		Red_bullets.update()
		Yellow_bullets.update()

		RED_SPACESHIP.update(Red_bullets, Yellow_bullets, "playing")
		YELLOW_SPACESHIP.update(Red_bullets, Yellow_bullets, "playing")

		Power_Ups_Red.update()
		Power_Ups_Yellow.update()

		# checking if anybody wins
		if RED_SPACESHIP.sprite.health == 0:
			self.state = "Outro"
			self.won_spaceship = "Yellow"
			self.outro_wait.activate()
			DEAD_SOUND.play()

		elif YELLOW_SPACESHIP.sprite.health == 0:
			self.state = "Outro"
			self.won_spaceship = "Red"
			self.outro_wait.activate()
			DEAD_SOUND.play()

		# drawing
		self.main_screen_draw()

	def main_screen_draw(self):
		# BG
		screen.blit(BG, (0,0))
		pygame.draw.rect(screen, BLACK, BORDER)

		# bullets
		Yellow_bullets.draw(screen)
		Red_bullets.draw(screen)

		# healths
		YELLOW_HEALTH = HEALTH_FONT.render("Health: "+str(YELLOW_SPACESHIP.sprite.health), True, WHITE)
		RED_HEALTH = HEALTH_FONT.render("Health: "+str(RED_SPACESHIP.sprite.health), True, WHITE)

		RED_HEALTH_RECT = RED_HEALTH.get_rect( topright = (WIDTH-10, 10) ) # For ease the access of positioning

		screen.blit(YELLOW_HEALTH, (10, 10))
		screen.blit(RED_HEALTH, RED_HEALTH_RECT)

		# power ups
		Power_Ups_Red.draw(screen)
		Power_Ups_Yellow.draw(screen)

		# spaceships
		RED_SPACESHIP.draw(screen)
		YELLOW_SPACESHIP.draw(screen)


	# Outro Screen
	def outro(self):

		#drawing the winning message
		WIN = WIN_FONT.render(self.won_spaceship+" Wins", True, RED if self.won_spaceship == "Red" else YELLOW)
		WIN_RECT = WIN.get_rect(center = (WIDTH/2, HEIGHT/2))

		screen.blit(WIN, WIN_RECT)

		self.outro_wait.update()

		# restart mechanics
		if not self.outro_wait.active:

			Red_bullets.empty()
			Yellow_bullets.empty()

			RED_SPACESHIP.update(Red_bullets, Yellow_bullets, "restart")
			YELLOW_SPACESHIP.update(Red_bullets, Yellow_bullets, "restart")

			Power_Ups_Red.empty()
			Power_Ups_Yellow.empty()

			self.state = "Main Screen"


	def update(self):

		# Event loop
		self.event_loop()

		# Changes
		if self.state == "Intro":
			self.intro()

		elif self.state == "Main Screen":
			self.main_screen()

		elif self.state == "Outro":
			self.outro()

		# Display Everything that have been drawn
		pygame.display.flip()


def main():

	game_manager = Game_Manager()

	# Game loop
	while game_manager.run:

		game_manager.update()

		CLOCK.tick(FPS)


	pygame.quit()


if __name__ == "__main__":
	main()