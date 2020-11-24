import pygame, os, random

pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
run = True

#Constants

PATH = os.path.dirname(__file__)
RESOLUTION = (1280,720)
GRAVITY = -9.8
WIND = 0 

PHYSICS_BUFFER_OFFSET = 3

PARTICAL_SPAWN_COUNT = 1000
PHYSICS_ACCURACY = 1 #1 = perfect, 99 = worse
MAX_PHYSICS_SIZE_CALC = 5


WIND_RANDOM = True
WIND_AGRESSIVENESS = 2
WIND_LIMIT = 5
WIND_FLIP_CHANGE = 0.05
WIND_MANUAL = True


class Void:
    def __init__(self, colour):
        self.colour = colour
    def update(self, win):
        pygame.draw.rect(win, self.colour, (0,0,RESOLUTION[0],RESOLUTION[1]))

class ElementHandler:
    def update():
        pass

class Particle:
    def __init__(self, win, x, y, width, height, mass, colour, xVelocity, yVelocity, isFalling):
        self.win = win

        self.x = x
        self.y = y

        self.bufferedY = self.y
        self.bufferedX = self.x

        self.width = width
        self.height = height
        self.mass = mass
        self.colour = colour

        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        self.isFalling = isFalling

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def bufferedRectCalculations(self):
        self.rect = (self.x, self.y, self.width, self.height)
        self.bufferedY += self.yVelocity/60 
        self.bufferedX += self.xVelocity/60 
        self.bufferedRect = pygame.Rect(self.bufferedX + PHYSICS_BUFFER_OFFSET, self.bufferedY + PHYSICS_BUFFER_OFFSET, self.width, self.height)


    def collideCheck(self):
        self.bufferedRectCalculations()
        for rect in rectList:
            if self.bufferedRect.colliderect(rect):
                self.isFalling = False
                self.yVelocity = 0
                self.xVelocity = 0
                break
            else:      
                self.isFalling = True
                
    def render(self):
        self.rect = pygame.draw.rect(self.win, self.colour, (self.x, self.y, self.width, self.height))
        realismOffset = random.randint(0,100)
        if realismOffset > PHYSICS_ACCURACY:
            if self.width < MAX_PHYSICS_SIZE_CALC and self.height < MAX_PHYSICS_SIZE_CALC:
                rectList.append(self.rect)

    def update(self):
        self.collideCheck()
        if self.isFalling:
            self.yVelocity -= GRAVITY
            self.y += self.yVelocity/60

            self.xVelocity += WIND
            self.x += self.xVelocity/60
        
        self.render()

particleList = []

def generateParticals():
    rectList = []
    for x in range(PARTICAL_SPAWN_COUNT):
        rectList.append(pygame.draw.rect(win, (255,0,0), (0,600,1280,50)))
        rectList.append(pygame.draw.rect(win, (255,0,0), (100,200,50,50)))  
        particleList.append(Particle(win=win, x=random.randint(0, 1280), y=random.randint(1, 10), width=random.randint(2, 7), height=random.randint(2, 7), mass=100, colour=(random.randint(0, 255),255,255), xVelocity=0, yVelocity=0, isFalling=False))

void = Void(colour=(100,100,100))

rectList = []
generateParticals()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    cursor = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if click[0]:
        particleList.append(Particle(win=win, x=cursor[0], y=cursor[1], width=random.randint(1, 7), height=random.randint(1, 7), mass=100, colour=(random.randint(0, 255),255,255), xVelocity=0, yVelocity=0, isFalling=False))

    if WIND_MANUAL:
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            WIND += 1
            
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            WIND -= 1

    if keys[pygame.K_r]:
        particleList = []
        generateParticals()

    if WIND_RANDOM:
        WIND += random.randint(int(WIND_AGRESSIVENESS * -1), int(WIND_AGRESSIVENESS))
        if WIND > 5:
            WIND = 5
        if WIND < -5:
            WIND = -5

        windFlip = random.randint(0,1000)
        if windFlip < WIND_FLIP_CHANGE * 100: 
            WIND = WIND * -1

    void.update(win)

    rectList = []
    rectList.append(pygame.draw.rect(win, (255,0,0), (0,600,1280,50)))
    rectList.append(pygame.draw.rect(win, (255,0,0), (100,200,50,50)))

    for item in particleList:
        item.update()

    clock.tick(60)
    pygame.display.update()