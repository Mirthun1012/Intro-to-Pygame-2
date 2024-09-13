import pygame
import os

# Screen
WIDTH, HEIGHT = 900, 500


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# FPS
CLOCK = pygame.time.Clock()
FPS = 60


# Signals
CHANGE_TO_OUTRO = pygame.event.custom_type()
CHANGE_TO_MAIN = pygame.event.custom_type()
CHANGE_TO_INTRO = pygame.event.custom_type()