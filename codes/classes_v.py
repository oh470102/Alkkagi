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

    def highlight(self):
        pygame.draw.circle(self.screen, 'red', (self.center_x, self.center_y), self.radius, width=3)
        pygame.display.flip()

    def dishighlight(self, all_sprites):
        all_sprites.draw(self.screen)
        pygame.display.flip()

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

    return f_v1x + 15, f_v1y + 15, f_v2x + 15, f_v2y + 15



























