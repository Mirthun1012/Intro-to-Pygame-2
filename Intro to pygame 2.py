"""
	NOTE:
		Making my second game in pygame to learn much more new stuff and to practice once again the known stuff!
"""


import pygame
import os

pygame.init()


# Screen
WIDTH, HEIGHT = 900, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Sounds
HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Hit.mp3"))
FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Fire.mp3"))


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

# Spaceships
SPAWNING_LOC = [ ((WIDTH//2)-300, HEIGHT//2), ((WIDTH//2)+300 , HEIGHT//2) ] # For Center Argument 

class SpaceShip(pygame.sprite.Sprite):

	def __init__(self, surface, pos, type):
		super().__init__()

		self.position = pos
		self.type = type
		self.health = 10

		self.VELOCITY = 3

		self.image = pygame.transform.rotate(surface, 90 if self.type == "yellow" else -90)
		self.rect = self.image.get_rect(center = self.position)

	def movement(self):
		keys_pressed = pygame.key.get_pressed()

		if self.type == "yellow":
			# LEFT
			if keys_pressed[pygame.K_a] and self.rect.left - self.VELOCITY > 0:
				self.rect.left -= self.VELOCITY
			# DOWN
			if keys_pressed[pygame.K_s] and self.rect.bottom + self.VELOCITY < HEIGHT:
				self.rect.bottom += self.VELOCITY
			# RIGHT
			if keys_pressed[pygame.K_d] and self.rect.right + self.VELOCITY < BORDER.left:
				self.rect.right += self.VELOCITY
			# UP
			if keys_pressed[pygame.K_w] and self.rect.top - self.VELOCITY > 0:
				self.rect.top -= self.VELOCITY

		else:
			# LEFT
			if keys_pressed[pygame.K_LEFT] and self.rect.left - self.VELOCITY > BORDER.right:
				self.rect.left -= self.VELOCITY
			# DOWN
			if keys_pressed[pygame.K_DOWN] and self.rect.bottom + self.VELOCITY < HEIGHT:
				self.rect.bottom += self.VELOCITY
			# RIGHT
			if keys_pressed[pygame.K_RIGHT] and self.rect.right + self.VELOCITY < WIDTH:
				self.rect.right += self.VELOCITY
			# UP
			if keys_pressed[pygame.K_UP] and self.rect.top - self.VELOCITY > 0:
				self.rect.top -= self.VELOCITY

	def checking_collision(self, Red_bullets, Yellow_bullets):

		group = Yellow_bullets if self.type == "red" else Red_bullets

		if pygame.sprite.spritecollide(self, group, True):
			if self.health > 0:
				self.health -= 1
				HIT_SOUND.play()

	def update(self, Red_bullets, Yellow_bullets):
		self.movement()
		self.checking_collision(Red_bullets, Yellow_bullets)


# Bullets
MAX_BULLETS = 3

class Bullet(pygame.sprite.Sprite):

	def __init__(self, position, bullet_type):
		super().__init__()

		self.position = position
		self.bullet_type = bullet_type

		self.VELOCITY = 7

		self.image = pygame.image.load(os.path.join("Assets", "Bullet.png"))
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


# BG
BG = pygame.image.load(os.path.join("Assets", "space.png"))
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))


# Border
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)


def checking_wining(RED_SPACESHIP, YELLOW_SPACESHIP):

	wining_text = ""

	if RED_SPACESHIP.sprite.health == 0:
		wining_text = "YELLOW WINS"

	elif YELLOW_SPACESHIP.sprite.health == 0:
		wining_text = "RED WINS"

	if wining_text != "":
		
		WIN = WIN_FONT.render(wining_text, True, RED if wining_text[0] == "R" else YELLOW)
		WIN_RECT = WIN.get_rect(center = (WIDTH/2, HEIGHT/2)) 
		
		screen.blit(WIN, WIN_RECT)
		pygame.display.update()
		
		pygame.time.delay(5*1000)
		main()


def main():

	# Global vars
	run = True

	# Space Ships
	YELLOW_SPACESHIP = SpaceShip(pygame.image.load(os.path.join("Assets", "spaceship_yellow.png")), SPAWNING_LOC[0], "yellow")
	YELLOW_SPACESHIP = pygame.sprite.GroupSingle(sprite = YELLOW_SPACESHIP)

	RED_SPACESHIP = SpaceShip(pygame.image.load(os.path.join("Assets", "spaceship_red.png")), SPAWNING_LOC[1], "red")
	RED_SPACESHIP = pygame.sprite.GroupSingle(sprite = RED_SPACESHIP)

	# Bullets
	Red_bullets = pygame.sprite.Group()
	Yellow_bullets = pygame.sprite.Group()


	# Game loop
	while run:
		
		# Event loop
		for eve in pygame.event.get():

			if eve.type == pygame.QUIT:
				run = False

			# Firing!
			elif eve.type == pygame.KEYDOWN:
				if eve.key == pygame.K_LCTRL and len(Yellow_bullets.sprites()) < MAX_BULLETS:
					Yellow_bullets.add( Bullet(YELLOW_SPACESHIP.sprite.rect.midright, "yellow") )
					FIRE_SOUND.play()

				if eve.key == pygame.K_RCTRL and len(Red_bullets.sprites()) < MAX_BULLETS:
					Red_bullets.add( Bullet(RED_SPACESHIP.sprite.rect.midleft, "red") )
					FIRE_SOUND.play()		


		# Changes
		Red_bullets.update()
		Yellow_bullets.update()

		RED_SPACESHIP.update(Red_bullets, Yellow_bullets)
		YELLOW_SPACESHIP.update(Red_bullets, Yellow_bullets)

		checking_wining(RED_SPACESHIP, YELLOW_SPACESHIP)


		# Draw

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

		# spaceships
		RED_SPACESHIP.draw(screen)
		YELLOW_SPACESHIP.draw(screen)


		# Update
		pygame.display.update()


		CLOCK.tick(FPS)


	pygame.quit()


if __name__ == "__main__":
	main()