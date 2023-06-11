import pygame
import numpy as np

pygame.init()
drag = False
zoomval = 1
root = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clock = pygame.time.Clock()
dragpoint = (0,0)
deltaX,deltaY = 0,0
w, h = pygame.display.get_surface().get_size()
running = True
targetpoint = (200,300)


gridimg = pygame.image.load("C:\\Users\\Reilley Pfrimmer\\source\\repos\\ARMBotDemo\\grid.png").convert()

uniobj = []

class Object:
    def __init__(self,x,y,colour):
        self.x = x
        self.y = y
        self.colour = colour
        uniobj.append(self)
    def move(self,ox, oy):
        self.x += ox
        self.y += oy
class Square(Object):
    def __init__(self,x,y,a,colour):
        super().__init__(x,y,colour)
        self.a = a
    def draw(self):
        if type(self.colour) == pygame.surface.Surface:
            root.blit(self.colour, (self.x,self.y))
        else:
            pygame.draw.rect(root, self.colour, [self.x,self.y,self.a,self.a])
class Conga(Object):
    def __init__(self,x,y,colour):
        super().__init__(x,y,colour)
        self.a = 1000
        self.s = 4
        self.line = [Square(self.x+(self.a)*sx,self.y,self.a,self.colour) for sx in range(self.s)]
    def draw(self):
        for i in self.line:
            i.y = self.y
        if self.line[-1].x > w+450:
            self.line.insert(0,self.line.pop(-1))
            self.line[0].x = self.line[1].x - (self.a)
        if self.line[0].x < -(self.a):
            self.line.insert(len(self.line),self.line.pop(0))
            self.line[-1].x = self.line[-2].x + (self.a)

class EPICConga(Object):
    def __init__(self,x,y,colour):
        super().__init__(x,y,colour)
        self.a = 1000
        self.s = 4
        self.line = [Conga(0,self.y+(1000*sx),self.colour) for sx in range(self.s)]
    def draw(self):
        if self.line[-1].y < -128:
            self.line.insert(len(self.line),self.line.pop(0))
            self.line[-1].y = self.line[-2].y + (self.a)
        if self.line[0].y > 0:
            self.line.insert(0,self.line.pop(-1))
            self.line[0].y = self.line[1].y - (self.a)
            
class ArmSegment(Object):
    def __init__(self,x,y,colour,a,rad):
        super().__init__(x,y,colour)
        self.rad = np.deg2rad(rad) * -1
        self.a = a
        self.endpoint = (self.x+(self.a*np.cos(self.rad)),self.y+(self.a*np.sin(self.rad)))
    def draw(self):
        pygame.draw.line(root, self.colour, (self.x,self.y), self.endpoint,width=30)
        self.endpoint = (self.x+(self.a*np.cos(self.rad)),self.y+(self.a*np.sin(self.rad)))

PJGP = EPICConga(0,0,gridimg)
a0 = ArmSegment(400,400,[185, 214, 242],200,45) # i am legitimately retarded REPLACE 45 with value A
a1 = ArmSegment(a0.endpoint[0],a0.endpoint[1],[185, 214, 242],200,90) # REPLACE 90 with value B

while running: # main loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            drag = True
            dragpoint = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            drag = False
    if drag == True:
        deltaX,deltaY = [x-y for x,y in zip(pygame.mouse.get_pos(),dragpoint)]
        for i in uniobj:
            i.move(deltaX,deltaY)
        dragpoint = pygame.mouse.get_pos()   
    root.fill("#061A40")
    for i in uniobj:
        i.draw()
    pygame.draw.circle() # TODO Continue building this
    pygame.display.flip()
    clock.tick(60)
pygame.quit()