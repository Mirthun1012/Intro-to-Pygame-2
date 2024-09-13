import pygame
import os

from Files.Game_Variables import *

from Files.Main_Screen.SpaceShips import SpaceShip

# Border
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)

# Spaceships
SPAWNING_LOC = [ ((WIDTH//2)-250, HEIGHT//2), ((WIDTH//2)+250 , HEIGHT//2) ] # For Center Argument 

YELLOW_SPACESHIP = SpaceShip(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "spaceship_yellow.png")), 90), SPAWNING_LOC[0], "yellow", BORDER)
YELLOW_SPACESHIP = pygame.sprite.GroupSingle(sprite = YELLOW_SPACESHIP)
RED_SPACESHIP = SpaceShip(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "spaceship_red.png")), -90), SPAWNING_LOC[1], "red", BORDER)
RED_SPACESHIP = pygame.sprite.GroupSingle(sprite = RED_SPACESHIP)

# Power Ups
MAX_POWERUPS = 3

Power_Ups_Red = pygame.sprite.Group()
Power_Ups_Yellow = pygame.sprite.Group()