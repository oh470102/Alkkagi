from util_functions import board_init, in_boundary
from classes_v import Stone
import pygame, math, time

### TODO: implement smoother motion, sound

# GLOBAL CONSTANTS
FRICTION = 0.97 # 작을수록 마찰 세짐       
FPS = 120

# INITS.
pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(50, 10)
screen, bstone1, bstone2, bstone3, wstone1, wstone2, wstone3, all_sprites, no_board_sprites = board_init()
player1_index, player2_index = 0, 0
player1_stones, player2_stones = [bstone1, bstone2, bstone3], [wstone1, wstone2, wstone3]
turn = 1
run = True

# GAME START
curr = player1_stones[player1_index]
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
                if turn == 1: 
                    player1_index = (player1_index + 1 ) % len(player1_stones)
                    curr = player1_stones[player1_index]
                elif turn == 2: 
                    player2_index = (player2_index + 1) % len(player2_stones)
                    curr = player2_stones[player2_index]
                curr.highlight()

            if event.key == pygame.K_SPACE:
                strength = curr.get_str(); print(strength)
                angle = curr.get_angle(); print(f"angle: {angle}")
                curr.shoot(frame=FPS, all_sprites=all_sprites, strength=strength, angle=angle, friction=FRICTION, no_board_sprites=no_board_sprites)

                for stone in no_board_sprites:
                    if in_boundary(stone) is False: 
                        print(f"OUT OF GAME: {stone}")
                        
                        if stone in player1_stones: player1_stones.remove(stone)
                        elif stone in player2_stones: player2_stones.remove(stone)
                        all_sprites.remove(stone); no_board_sprites.remove(stone)
                        all_sprites.draw(curr.screen)
                        pygame.display.flip()
                        del stone
                
                turn = 2 if turn == 1 else 1
                if turn == 1: curr = player1_stones[player1_index % len(player1_stones)]
                elif turn == 2: curr = player2_stones[player2_index % len(player2_stones)]
                curr.highlight()

    pygame.display.flip()

    # END CONDITION
    if len(player1_stones) * len(player2_stones) == 0:
        if len(player1_stones) == 0: 
            print("PLAYER 2 WON!")
        else: 
            print("PLAYER 1 WON!")
        break

pygame.quit()
