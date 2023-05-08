import pygame, math
from classes_v import Stone, Board

def dot(v1, v2):
    temp = [v1[i]*v2[i] for i in range(0, len(v1))]
    return sum(temp)

def mag(v1):
    temp = [c**2 for c in v1]
    return sum(temp)**0.5

def board_init():
    pygame.init()
    WINDOW = (640, 640)
    GRID = (19, 19)
    UNIT = WINDOW[0]//GRID[0]
    screen = pygame.display.set_mode(WINDOW)
    screen.fill('white')

    # CREATE BOARD, STONE OBJECTS
    board = Board(x=0, y=0, image="board.png", screen=screen)
    bstone1 = Stone(x=UNIT*3, y=UNIT*3, image="black_stone.png", screen=screen)
    bstone2 = Stone(x=UNIT*9, y=UNIT*3, image="black_stone.png", screen=screen)
    bstone3 = Stone(x=UNIT*15, y=UNIT*3, image="black_stone.png", screen=screen)

    # ADD TO SPRITE GROUP
    all_sprites = pygame.sprite.Group()
    all_sprites.add(board)
    all_sprites.add(bstone1)
    all_sprites.add(bstone2)
    all_sprites.add(bstone3)
    all_sprites.draw(screen)

    no_board_sprites = pygame.sprite.Group()
    no_board_sprites.add(bstone1)
    no_board_sprites.add(bstone2)
    no_board_sprites.add(bstone3)

    return screen, bstone1, bstone2, bstone3, all_sprites, no_board_sprites

def in_boundary(obj):
    screen = obj.screen
    w, h = screen.get_size()

    x_lower_boundary = 0
    x_upper_boundary = w

    y_lower_boundary = 0
    y_upper_boundary = h

    if (obj.rect.right < x_lower_boundary) or (obj.rect.left > x_upper_boundary):
        return False
    
    if (obj.rect.bottom < y_lower_boundary) or (obj.rect.top > y_upper_boundary):
        return False
    
    return True

def momentum_conservation(obj1, obj2, angle): 
    m1, m2, mT = obj1.mass, obj2.mass, (obj1.mass + obj2.mass)
    x1, y1 = obj1.center_x, obj1.center_y
    x2, y2 = obj2.center_x, obj2.center_y
    v1x, v1y = obj1.vel_x, obj1.vel_y
    v2x, v2y = obj2.vel_x, obj2.vel_y
    k = mag([x1-x2, y1-y2])**2
    dp1 = (v1x-v2x)*(x1-x2) + (v1y-v2y)*(y1-y2)
    dp2 = (v2x-v1x)*(x2-x1) + (v2y-v1y)*(y2-y1)

    f_v1x = v1x - 2*m2/mT * (dp1) * (x1-x2) / k 
    f_v1y = v1y - 2*m2/mT * (dp1) * (y1-y2) / k 
    f_v2x = v2x - 2*m1/mT * (dp2) * (x2-x1) / k 
    f_v2y = v2y - 2*m1/mT * (dp2) * (y2-y1) / k 

    return f_v1x, f_v1y, f_v2x, f_v2y

def multi_movement(collision_list, all_sprites, frame, friction, no_board_sprites):
    # LIST OF OBJECTS NEEDING UPDATE
    moving_list = collision_list
    
    obj1, obj2 = collision_list[0], collision_list[1]
    obj1.vel_x, obj1.vel_y, obj2.vel_x, obj2.vel_y = momentum_conservation(obj1, obj2, obj1.angle)
    obj1.vel = mag([obj1.vel_x, obj1.vel_y]) 
    obj2.vel = mag([obj2.vel_x, obj2.vel_y])

    obj_vel_dict = {obj1: obj1.vel, obj2: obj2.vel}
    
    ### TODO: IMPLEMENT HERE

    CLOCK = pygame.time.Clock()
    while True:
        CLOCK.tick(frame)

        for obj in moving_list:

            obj.vel *= friction
            obj.vel_x *= friction
            obj.vel_y *= friction
            
            # UPDATE POSITIONS
            obj.update(frame=frame)

            # DETECT ANY NEW COLLISIONS
            ### TODO: FIX HERE
            '''
            if pygame.sprite.spritecollide(obj, no_board_sprites, False):
                new_obj = pygame.sprite.spritecollide(obj, no_board_sprites, False)[0]
                obj.vel_x, obj.vel_y, new_obj.vel_x, new_obj.vel_y = momentum_conservation(obj, new_obj, obj.angle)
                obj.vel = mag([obj.vel_x, obj.vel_y]) 
                new_obj.vel = mag([new_obj.vel_x, new_obj.vel_y])
                moving_list.append(new_obj)
                obj_vel_dict.update({obj: obj.vel, new_obj: new_obj.vel})
                continue   
            '''
            # UPDATE SCREEN
            all_sprites.draw(obj.screen)
            pygame.display.flip()

            # APPLY FRICTION
            if obj.vel < 0.1 * obj_vel_dict[obj]:
                obj.vel, obj.vel_x, obj.vel_y = 0, 0, 0
                moving_list.remove(obj)

        if len(moving_list) == 0: break
        

            


    

        
        

