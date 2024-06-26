"""
	NOTE:
		Added the states to display the winning message!
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

		self.image = surface
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


Red_bullets = pygame.sprite.Group()
Yellow_bullets = pygame.sprite.Group()


# BG
BG = pygame.image.load(os.path.join("Assets", "space.png"))
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))


# Border
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)


def draw():
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


def main():

	game_state = "playing" # It carries the winning message when it is != "playing"

	countdown = 20

	run = True

	# Game loop
	while run:
		
		# Event loop
		for eve in pygame.event.get():

			if eve.type == pygame.QUIT:
				run = False


			elif game_state == "playing":

				# Firing!
				if eve.type == pygame.KEYDOWN:
					if eve.key == pygame.K_LCTRL and len(Yellow_bullets.sprites()) < MAX_BULLETS:
						Yellow_bullets.add( Bullet(YELLOW_SPACESHIP.sprite.rect.midright, "yellow") )
						FIRE_SOUND.play()

					if eve.key == pygame.K_RCTRL and len(Red_bullets.sprites()) < MAX_BULLETS:
						Red_bullets.add( Bullet(RED_SPACESHIP.sprite.rect.midleft, "red") )
						FIRE_SOUND.play()


		if game_state == "playing":
			# Updates
			Red_bullets.update()
			Yellow_bullets.update()

			RED_SPACESHIP.update(Red_bullets, Yellow_bullets, "playing")
			YELLOW_SPACESHIP.update(Red_bullets, Yellow_bullets, "playing")

			# checking if anybody wins
			if RED_SPACESHIP.sprite.health == 0:
				game_state = "Yellow Wins"

			elif YELLOW_SPACESHIP.sprite.health == 0:
				game_state = "Red Wins"


			# Draw
			draw()

		# Somebody wins
		else:
			# drawing the winning message
			WIN = WIN_FONT.render(game_state, True, RED if game_state[0] == "R" else YELLOW)
			WIN_RECT = WIN.get_rect(center = (WIDTH/2, HEIGHT/2))

			screen.blit(WIN, WIN_RECT)

			# countdown mechanics
			countdown -= 0.1
			
			# restart mechanics
			if countdown < 0:
				countdown = 20

				Red_bullets.empty()
				Yellow_bullets.empty()

				RED_SPACESHIP.update(Red_bullets, Yellow_bullets, "restart")
				YELLOW_SPACESHIP.update(Red_bullets, Yellow_bullets, "restart")

				game_state = "playing"


		# Display Everything that have been drawn
		pygame.display.update()


		CLOCK.tick(FPS)


	pygame.quit()


if __name__ == "__main__":
	main()