from classes_v import game_state
import pygame

# INITS.
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(50, 10)
game = game_state()
run = True

while run:
    q = game.state_manage()
    if q==-1: break

pygame.quit()



