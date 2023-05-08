import pygame, math, copy, time

VELOCITY_FACTOR = 600
THRESHOLD = 30

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

            # UPDATE POSITIONS
                stone.rect.x += (stone.vel_x * dt)
                stone.rect.y += (stone.vel_y * dt)

            # APPLY FRICTION
                print(f"BEFORE FRICTION: vel_x: {stone.vel_x}, vel_y: {stone.vel_y}")
                stone.vel_x *= (friction)
                stone.vel_y *= (friction)
                print(f"AFTER FRICTION: vel_x: {stone.vel_x}, vel_y: {stone.vel_y}")
                #if stone.vel_x**2 + stone.vel_y**2 < THRESHOLD**2:
                #   stone.vel, stone.vel_x, stone.vel_y = 0, 0, 0 
                if stone.vel_x < THRESHOLD: stone.vel_x = 0
                if stone.vel_y < THRESHOLD: stone.vel_y = 0

                # UPDATE SCREEN
                all_sprites.draw(self.screen)
                pygame.display.flip()

            # BREAKOUT 
            count = 0
            for stone in no_board_sprites:
                if stone.vel_x == 0 and stone.vel_y == 0: count += 1
            if count == 3: 
                print("END")
                break

    def draw_arrow(self, size=None, angle=None):
        # UNDRAW CURRENT ARROW
        all_sprites = self.groups()[0]
        all_sprites.draw(self.screen)
        self.highlight_only()
        
        # DRAW NEW ARROW, ONLY UPDATE X
        x = self.rect.center[0]

        if size is not None:
            self.line_start, self.line_end = dilation(self.line_start, self.line_end, size=size)

        if angle is not None:
            self.line_start = rotation(angle=angle, point=self.line_start, center=self.rect.center)
            self.line_end = rotation(angle=angle, point=self.line_end, center=self.rect.center)

        pygame.draw.line(self.screen, 'green', self.line_start, self.line_end, width=3)
        pygame.draw.circle(self.screen, 'green', self.line_end, radius=5)
        pygame.display.flip()
    
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

    def arrow_upsize(self, all_sprites):
        pass

    def arrow_downsize(self):
        pass

    def arrow_rotate(self):
        pass

def momentum_conservation(obj1, obj2, angle=None): 
    m1, m2, mT = obj1.mass, obj2.mass, (obj1.mass + obj2.mass)
    x1, y1 = obj1.rect.x, obj1.rect.y
    x2, y2 = obj2.rect.x, obj2.rect.y
    v1x, v1y = obj1.vel_x, obj1.vel_y
    v2x, v2y = obj2.vel_x, obj2.vel_y
    k = ((x1-x2)**2 + (y1-y2)**2)
    dp1 = (v1x-v2x)*(x1-x2) + (v1y-v2y)*(y1-y2)
    dp2 = (v2x-v1x)*(x2-x1) + (v2y-v1y)*(y2-y1)

    f_v1x = v1x - 2*m2/mT * (dp1) * (x1-x2) / k 
    f_v1y = v1y - 2*m2/mT * (dp1) * (y1-y2) / k 
    f_v2x = v2x - 2*m1/mT * (dp2) * (x2-x1) / k 
    f_v2y = v2y - 2*m1/mT * (dp2) * (y2-y1) / k 

    return f_v1x + 5, f_v1y + 5, f_v2x + 5, f_v2y + 5

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



















