import pygame, os

pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
run = True

#Constants

PATH = os.path.dirname(__file__)
RESOLUTION = (1280,720)
GRAVITY = -9.8

class Void:
    def update(self, win):
        pygame.draw.rect(win, (0,0,0), (0,0,RESOLUTION[0],RESOLUTION[1]))

class Particle:
    def __init__(self, win, x, y, width, height, mass, colour, xVelocity, yVelocity, isFalling):
        self.win = win

        self.x = x
        self.y = y

        self.width = width
        self.height = height
        self.mass = mass
        self.colour = colour

        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        self.isFalling = isFalling

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def collideCheck(self):
        for rect in rectList:
            if self.rect.colliderect(rect):
                self.isFalling = False
                print("test")
                self.yVelocity = 0
            else:
                self.isFalling = True
                

    def render(self):
        self.rect = pygame.draw.rect(self.win, self.colour, (self.x, self.y, self.width, self.height))
    
    def update(self):
        self.collideCheck()
        if self.isFalling:
            self.yVelocity -= GRAVITY
            self.y += self.yVelocity/60
        self.render()

particle = Particle(win=win, x=1000, y=10, width=50, height=50, mass=100, colour=(0,255,255), xVelocity=0, yVelocity=0, isFalling=False)
void = Void()

rectList = []
rectList.append(pygame.draw.rect(win, (255,0,0), (0,600,1280,50)))
rectList.append(pygame.draw.rect(win, (255,0,0), (100,200,50,50)))

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    void.update(win)

    rectList = []
    rectList.append(pygame.draw.rect(win, (255,0,0), (0,600,1280,50)))
    rectList.append(pygame.draw.rect(win, (255,0,0), (100,200,50,50)))

    particle.update()

    clock.tick(60)
    pygame.display.update()