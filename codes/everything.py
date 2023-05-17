from classes_v import game_state
import pygame, sys

# INITS.
pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(50, 10)
game = game_state()
run = True

while run:
    game.state_manage()



