import pygame, math, copy, time

VELOCITY_FACTOR = 600
THRESHOLD = 55
DISTANCE_TO_STRENGTH = 1/40
FRICTION = 0.93 # 작을수록 마찰 세짐       
FPS = 100

# DEFINE CLASSES
class Board(pygame.sprite.Sprite):
    def __init__(self, x, y, image, screen):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.screen = screen
        
class Stone(pygame.sprite.Sprite):

    def __init__(self, x, y, image, screen):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.center_x = self.rect.x + self.rect.width/2
        self.center_y = self.rect.y + self.rect.height/2
        # NOTE: rect.x, rect.y are coordinates of TOP LEFT CORNER 
        self.vel = 0
        self.angle = 0
        self.vel_x = self.vel * math.cos(self.angle)
        self.vel_y = -1 * self.vel * math.sin(self.angle)
        self.screen = screen
        self.mass = 1
        self.radius = max([self.rect.width//2, self.rect.height//2]) 
        self.prev_center = self.rect.center
        self.line_start = (self.rect.center[0], self.rect.center[1] + self.radius)
        self.line_end = (self.rect.center[0], self.rect.center[1] - self.radius)
        
    def shoot(self, strength, angle, friction, all_sprites, no_board_sprites, frame):
        self.angle = math.radians(angle)
        self.vel = strength * VELOCITY_FACTOR
        self.vel_x = self.vel * math.cos(self.angle)
        self.vel_y = -1 * self.vel * math.sin(self.angle)

        ### FRAME STUFF
        CLOCK = pygame.time.Clock()

        while True:
            # UPDATE CLOCK
            dt = CLOCK.tick(frame) / 1000

            # CHECK COLLISION
            for stone in no_board_sprites:
                c_with = pygame.sprite.spritecollide(stone, no_board_sprites, False, pygame.sprite.collide_circle)
                c_with.remove(stone)
                if c_with:
                    print("before collision")
                    print(stone.vel_x, stone.vel_y, c_with[0].vel_x, c_with[0].vel_y)
                    stone.vel_x, stone.vel_y, c_with[0].vel_x, c_with[0].vel_y = momentum_conservation(stone, c_with[0])
                    print("after collision:")
                    print(stone.vel_x, stone.vel_y, c_with[0].vel_x, c_with[0].vel_y)

                    # 버그 방지 장치 1
                    if abs(stone.vel_x) <= THRESHOLD and abs(stone.vel_y) <= THRESHOLD and abs(c_with[0].vel_x) <= THRESHOLD and abs(c_with[0].vel_y) <= THRESHOLD:
                        stone.vel_x, stone.vel_y, c_with[0].vel_x, c_with[0].vel_y = 0,0,0,0
                        for stone in no_board_sprites:
                            if stone.vel_x == 0 and stone.vel_y == 0: count += 1
                            if count == len(list(no_board_sprites)): 
                                print("MOTION END")
                                break

                    # 버그 방지 장치 2
                    c_with[0].rect.centerx += round((c_with[0].vel_x * dt), 2)
                    c_with[0].rect.centery += round((c_with[0].vel_y * dt), 2)

            # UPDATE POSITIONS
                stone.rect.centerx += round((stone.vel_x * dt), 2)
                stone.rect.centery += round((stone.vel_y * dt), 2)

            # APPLY FRICTION
                print(f"BEFORE FRICTION: vel_x: {stone.vel_x}, vel_y: {stone.vel_y}")
                stone.vel_x *= (friction)
                stone.vel_y *= (friction)

                #print(f"AFTER FRICTION: vel_x: {stone.vel_x}, vel_y: {stone.vel_y}")
                if abs(stone.vel_x) <= THRESHOLD and abs(stone.vel_y) <= THRESHOLD:
                    stone.vel_x = 0; stone.vel_y = 0

                # UPDATE SCREEN
                all_sprites.draw(self.screen)
                pygame.display.flip()

            # BREAKOUT 
            count = 0
            for stone in no_board_sprites:
                if stone.vel_x == 0 and stone.vel_y == 0: count += 1
            if count == len(list(no_board_sprites)): 
                print("MOTION END")
                break

    def update_arrow(self):
        translation = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(self.prev_center)
        self.line_start = pygame.math.Vector2(self.line_start) + translation
        self.line_end = pygame.math.Vector2(self.line_end) + translation
        self.prev_center = self.rect.center

    def draw_arrow(self, size=None, angle=None):
        # UNDRAW CURRENT ARROW
        all_sprites = self.groups()[0]
        all_sprites.draw(self.screen)
        self.highlight_only()
        pygame.display.flip()
        
        # DRAW NEW ARROW
        self.update_arrow()

        if size is not None:
            self.line_start, self.line_end = dilation(self.line_start, self.line_end, size=size)

        if angle is not None:
            self.line_start = rotation(angle=angle, point=self.line_start, center=self.rect.center)
            self.line_end = rotation(angle=angle, point=self.line_end, center=self.rect.center)

        pygame.draw.line(self.screen, 'green', self.line_start, self.line_end, width=3)
        pygame.draw.circle(self.screen, 'green', self.line_end, radius=5)
    
    def highlight(self, size=None, angle=None):
        # DRAW A CIRCLE AROUND IT
        x, y = self.rect.center
        pygame.draw.circle(self.screen, 'red', (x, y), self.radius, width=3)
        self.draw_arrow(size, angle)
        pygame.display.flip()

    def highlight_only(self):
        x, y = self.rect.center
        pygame.draw.circle(self.screen, 'red', (x, y), self.radius, width=3)
        pygame.display.flip()

    def dishighlight(self, all_sprites):
        all_sprites.draw(self.screen)
        pygame.display.flip()

    def get_str(self):
        p1 = pygame.math.Vector2(self.line_start)
        p2 = pygame.math.Vector2(self.line_end)
        return p1.distance_to(p2) * DISTANCE_TO_STRENGTH
    
    def get_angle(self):
        self.update_arrow()
        p1 = pygame.math.Vector2(self.line_start)
        p2 = pygame.math.Vector2(self.line_end)
        mid = p1*0.5 + p2*0.5
        v = p2 - p1

        print(f"p1: {p1.x}, {p1.y}")
        print(f"p2: {p2.x}, {p2.y}")
        print(f"mid: {mid.x}, {mid.y}")

        e1 = pygame.math.Vector2(1, 0)
        angle = e1.angle_to(v)

        '''
        if p2.x >= mid.x and p2.y <= mid.y: return angle
        elif p2.x <= mid.x and p2.y <= mid.y: return angle
        elif p2.x <= mid.x and p2.y >= mid.y: return angle
        elif p2.x >= mid.x and p2.y >= mid.y: return angle
        '''
        return -1*angle

class game_state:
    def __init__(self):
        screen, bstone1, bstone2, bstone3, wstone1, wstone2, wstone3, all_sprites, no_board_sprites = board_init()
        player1_stones, player2_stones = [bstone1, bstone2, bstone3], [wstone1, wstone2, wstone3]
        self.state = 'intro'
        self.selected_map_index = 0
        self.all_sprites = all_sprites
        self.no_board_sprites = no_board_sprites
        self.player1_stones = player1_stones
        self.player2_stones = player2_stones
        self.screen = screen
        self.player1_index = 0
        self.player2_index = 0
        self.turn = 1
        self.curr = self.player1_stones[self.player1_index]
        self.play_initiated = False

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = 'quit'
            elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                self.state = 'map_select'
                time.sleep(0.1)
        
        font1 = pygame.font.SysFont('arial',50)
        text1 = font1.render("Alkkagi",True, "blue")
        text1_rect = text1.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height()*1/4))
        self.screen.blit(text1, text1_rect)

        font2 = pygame.font.SysFont('arial',50)
        text2 = font2.render("Press Enter to Start",True, "blue")
        text2_rect = text2.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height()*3/4))
        self.screen.blit(text2, text2_rect)
        pygame.display.flip()

    def map_select(self):
        map_images = []
        map1 = pygame.image.load("board.png")
        map1 = pygame.transform.scale(map1, (160,160))
        map_images.append(map1)
        map2 = pygame.image.load("board.png")
        map2 = pygame.transform.scale(map2, (160,160))
        map_images.append(map2)
        map3 = pygame.image.load("board.png")
        map3 = pygame.transform.scale(map3, (160,160))
        map_images.append(map3)

        x = 40
        y = 100
        for i in range(len(map_images)):
            self.screen.blit(map_images[i],(x,y))
            x += 200
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = 'quit'
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.selected_map_index = (self.selected_map_index - 1) % 3
                elif event.key == pygame.K_RIGHT:
                    self.selected_map_index = (self.selected_map_index + 1) % 3
                elif event.key == pygame.K_RETURN:
                    self.state = 'play_init' 

        # Highlight the selected map with a rectangle
        if self.selected_map_index == 0:
            pygame.draw.rect(self.screen, (255, 0, 0), ((40, 100),(160,160)),10)
        elif self.selected_map_index == 1:
            pygame.draw.rect(self.screen, (255, 0, 0), ((240, 100),(160,160)),10)
        elif self.selected_map_index == 2:
            pygame.draw.rect(self.screen, (255, 0, 0), ((440, 100),(160,160)),10)

        font = pygame.font.SysFont('arial',50)
        text = font.render("Map select",True, "blue")
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(text, text_rect)
        
        pygame.display.flip()

    def play(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = 'quit'
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                
                if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP, pygame.K_a, pygame.K_b]:
                    if event.key == pygame.K_a: # UPSIZE
                        self.curr.highlight(size=1)
                    if event.key == pygame.K_b: # DOWNSIZE
                        self.curr.highlight(size=-1)

                    if event.key == pygame.K_DOWN:
                        self.curr.highlight(angle=1)
                    if event.key == pygame.K_UP:
                        self.curr.highlight(angle=-1)
                    if event.key == pygame.K_LEFT:
                        self.curr.highlight(angle=1)
                    if event.key == pygame.K_RIGHT:
                        self.curr.highlight(angle=-1)

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_TAB:
                    self.curr.dishighlight(all_sprites=self.all_sprites)
                    if self.turn == 1: 
                        self.player1_index = (self.player1_index + 1 ) % len(self.player1_stones)
                        self.curr = self.player1_stones[self.player1_index]
                    elif self.turn == 2: 
                        self.player2_index = (self.player2_index + 1) % len(self.player2_stones)
                        self.curr = self.player2_stones[self.player2_index]
                    self.curr.highlight()

                if event.key == pygame.K_SPACE:
                    strength = self.curr.get_str(); print(strength)
                    angle = self.curr.get_angle(); print(f"angle: {angle}")
                    self.curr.shoot(frame=FPS, all_sprites=self.all_sprites, strength=strength, angle=angle, friction=FRICTION, no_board_sprites=self.no_board_sprites)

                    for stone in self.no_board_sprites:
                        if in_boundary(stone) is False: 
                            print(f"OUT OF GAME: {stone}")
                            
                            if stone in self.player1_stones: self.player1_stones.remove(stone)
                            elif stone in self.player2_stones: self.player2_stones.remove(stone)
                            self.all_sprites.remove(stone); self.no_board_sprites.remove(stone)
                            self.all_sprites.draw(self.curr.screen)
                            pygame.display.flip()
                            del stone
                    
                    # END CONDITION 
                    if len(self.player1_stones) * len(self.player2_stones) == 0:
                        if len(self.player1_stones) == 0: 
                            print("PLAYER 2 WON!")
                        else: 
                            print("PLAYER 1 WON!")
                        #break -> FIX HERE!

                    
                    self.turn = 2 if self.turn == 1 else 1
                    if self.turn == 1: self.curr = self.player1_stones[self.player1_index % len(self.player1_stones)]
                    elif self.turn == 2: self.curr = self.player2_stones[self.player2_index % len(self.player2_stones)]
                    self.curr.highlight()

        pygame.display.flip()

        # END CONDITION 
        if len(self.player1_stones) * len(self.player2_stones) == 0:
            if len(self.player1_stones) == 0: 
                print("PLAYER 2 WON!")
            else: 
                print("PLAYER 1 WON!")

            #break -> FIX HERE

    def play_init(self):
        self.reset()
        self.all_sprites.draw(self.screen)
        self.curr.highlight()
        pygame.display.flip()
        self.play_initiated = True
        self.state = 'play'

    def reset(self):
        screen, bstone1, bstone2, bstone3, wstone1, wstone2, wstone3, all_sprites, no_board_sprites = board_init()
        player1_stones, player2_stones = [bstone1, bstone2, bstone3], [wstone1, wstone2, wstone3]
        self.all_sprites = all_sprites
        self.no_board_sprites = no_board_sprites
        self.player1_stones = player1_stones
        self.player2_stones = player2_stones
        self.screen = screen
        self.player1_index = 0
        self.player2_index = 0
        self.turn = 1
        self.curr = self.player1_stones[self.player1_index]
        self.play_initiated = False

    def state_manage(self):
        if self.state == 'intro': 
            self.intro()
        elif self.state == 'map_select':
            self.map_select()
        elif self.state == 'play_init' and self.play_initiated == False:
            self.play_init()
        elif self.state == 'play':
            self.play()
        elif self.state == 'quit':
            pygame.quit()

def momentum_conservation(obj1, obj2, angle=None): 

    CONST = 1.00

    m1, m2, mT = obj1.mass, obj2.mass, (obj1.mass + obj2.mass)
   #x1, y1 = obj1.rect.x, obj1.rect.y
   #x2, y2 = obj2.rect.x, obj2.rect.y

    x1, y1 = obj1.rect.center[0], obj1.rect.center[1]
    x2, y2 = obj2.rect.center[0], obj2.rect.center[1]
    v1x, v1y = obj1.vel_x, obj1.vel_y
    v2x, v2y = obj2.vel_x, obj2.vel_y
    k = ((x1-x2)**2 + (y1-y2)**2)
    dp1 = (v1x-v2x)*(x1-x2) + (v1y-v2y)*(y1-y2)
    dp2 = (v2x-v1x)*(x2-x1) + (v2y-v1y)*(y2-y1)

    f_v1x = (v1x - 2*m2/mT * (dp1) * (x1-x2) / k) * CONST
    f_v1y = (v1y - 2*m2/mT * (dp1) * (y1-y2) / k) * CONST
    f_v2x = (v2x - 2*m1/mT * (dp2) * (x2-x1) / k) * CONST
    f_v2y = (v2y - 2*m1/mT * (dp2) * (y2-y1) / k) * CONST

    f_v1x, f_v1y, f_v2x, f_v2y = filt([f_v1x, f_v1y, f_v2x, f_v2y])

    return f_v1x, f_v1y, f_v2x, f_v2y

def filt(lis):
    for i in range(0, len(lis)):
        lis[i] = lis[i] if abs(lis[i]) >= THRESHOLD//2.3 else 0

    return tuple(lis) 


def rotation(point, center, angle):
    angle = math.degrees(angle)/20
    center_V = pygame.math.Vector2(center)
    point_V = pygame.math.Vector2(point)
    t_point_V = point_V - center_V
    rotated_point = t_point_V.rotate(angle)
    ret = rotated_point + center_V

    x_, y_ = ret.x, ret.y
    return x_, y_

def dilation(point1, point2, size):
    size = 1.02 if size > 0 else 0.98

    p1_V = pygame.math.Vector2(point1)
    p2_V = pygame.math.Vector2(point2)
    midp_V = 0.5*p1_V + 0.5*p2_V

    if p1_V.distance_to(p2_V) > 60 and size > 1: size = 1
    elif p1_V.distance_to(p2_V) < 25 and size < 1: size = 1

    p1_V_ = midp_V + size * (p1_V - midp_V)
    p2_V_ = midp_V + size * (p2_V - midp_V)

    ret1 = p1_V_.x, p1_V_.y
    ret2 = p2_V_.x, p2_V_.y

    return ret1, ret2

def in_boundary(obj):
    screen = obj.screen
    w, h = screen.get_size()

    x_lower_boundary = 0
    x_upper_boundary = w

    y_lower_boundary = 0
    y_upper_boundary = h

    if (obj.rect.center[0] < x_lower_boundary) or (obj.rect.center[0] > x_upper_boundary):
        return False
    
    if (obj.rect.center[1] < y_lower_boundary) or (obj.rect.center[1] > y_upper_boundary):
        return False
    
    return True

def board_init():
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
    wstone1 = Stone(x=UNIT*3, y=UNIT*15, image="white_stone.png", screen=screen)
    wstone2 = Stone(x=UNIT*9, y=UNIT*15, image="white_stone.png", screen=screen)
    wstone3 = Stone(x=UNIT*15, y=UNIT*15, image="white_stone.png", screen=screen)
    stones = [bstone1, bstone2, bstone3, wstone1, wstone2, wstone3]

    # ADD TO SPRITE GROUP
    all_sprites = pygame.sprite.Group()
    all_sprites.add(board)
    for s in stones: all_sprites.add(s)
    #all_sprites.draw(screen)
    no_board_sprites = pygame.sprite.Group()
    for s in stones: no_board_sprites.add(s)

    return screen, bstone1, bstone2, bstone3, wstone1, wstone2, wstone3, all_sprites, no_board_sprites
