from util_functions import board_init, in_boundary
from classes_v import Stone
import pygame, math, time

# GLOBAL CONSTANTS
FRICTION = 0.968 # 작을수록 마찰 세짐       
FPS = 120

# INITS.
pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(50, 10)
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

        if event.type == pygame.KEYDOWN:
            
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP, pygame.K_a, pygame.K_b]:
                if event.key == pygame.K_a: # UPSIZE
                    curr.highlight(size=1)
                if event.key == pygame.K_b: # DOWNSIZE
                    curr.highlight(size=-1)

                if event.key == pygame.K_DOWN:
                    curr.highlight(angle=1)
                if event.key == pygame.K_UP:
                    curr.highlight(angle=-1)
                if event.key == pygame.K_LEFT:
                    curr.highlight(angle=1)
                if event.key == pygame.K_RIGHT:
                    curr.highlight(angle=-1)

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_TAB:
                curr.dishighlight(all_sprites=all_sprites)
                player_index = (player_index + 1 ) % len(player_stones)
                curr = player_stones[player_index]
                curr.highlight()

            if event.key == pygame.K_SPACE:
                strength = curr.get_str(); print(strength)
                angle = curr.get_angle(); print(f"angle: {angle}")
                curr.shoot(frame=FPS, all_sprites=all_sprites, strength=strength, angle=angle, friction=FRICTION, no_board_sprites=no_board_sprites)
            
                if in_boundary(curr) is False: 
                    player_stones.remove(curr)
                    del curr
                    player_index = (player_index + 1 ) % len(player_stones)
                    curr = player_stones[player_index]

                    
    pygame.display.flip()


pygame.quit()
