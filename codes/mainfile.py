from util_functions import board_init, in_boundary
from classes_v import Stone
import pygame, math, time

# GLOBAL CONSTANTS
FRICTION = 0.97 # 작을수록 마찰 세짐       
FPS = 120

# INITS.
pygame.init()
clock = pygame.time.Clock()
screen, bstone1, bstone2, bstone3, all_sprites, no_board_sprites = board_init()
player_stones = [bstone1, bstone2, bstone3]
player_index = 0
run = True

# GAME START
curr = player_stones[player_index]
curr.highlight()

# MAIN LOOP
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
              
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_TAB:
                curr.dishighlight(all_sprites=all_sprites)
                player_index = (player_index + 1 ) % len(player_stones)
                curr = player_stones[player_index]
                curr.highlight()

            if event.key == pygame.K_SPACE:
                curr.shoot(frame=FPS, all_sprites=all_sprites, strength=1.1, angle=-15, friction=FRICTION, no_board_sprites=no_board_sprites)
            
                if in_boundary(curr) is False: 
                    player_stones.remove(curr)
                    del curr
                    player_index = (player_index + 1 ) % len(player_stones)
                    curr = player_stones[player_index]

                    
    pygame.display.flip()


pygame.quit()