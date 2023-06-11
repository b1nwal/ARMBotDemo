import pygame

pygame.init()
drag = False
zoomval = 1
root = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clock = pygame.time.Clock()
dragpoint = (0,0)
deltaX,deltaY = 0,0
w, h = pygame.display.get_surface().get_size()
running = True


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
            
        

# george = Square(10,10,150,[3, 83, 164])
# paul = Square(400,75,175,[185, 214, 242])
# jeff = Conga(0,0,gridimg)
# petunia = Conga(0,-1000,gridimg)
PJGP = EPICConga(0,0,gridimg)
bes = Square(400,400,100,[185,214,242])

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
    pygame.display.flip()
    clock.tick(60)
pygame.quit()