import pygame
import numpy as np
import serial

pygame.init()
drag = False
paint = False
root = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clock = pygame.time.Clock()
dragpoint = (0,0)
deltaX,deltaY = 0,0
w, h = pygame.display.get_surface().get_size()
running = True
targetpoint = (400,200)
centrepoint = (400,400)
prev_point = (0,0)
mode = "drag"
l_ts = 0
tss = [l_ts]

seg1 = 400
seg2 = 300
reach = seg1+seg2

gridimg = pygame.image.load("C:\\Users\\Reilley Pfrimmer\\source\\repos\\ARMBotDemo\\grid.png").convert()
moveimg = pygame.image.load("C:\\Users\\Reilley Pfrimmer\\source\\repos\\ARMBotDemo\\move.png").convert()
pointimg = pygame.image.load("C:\\Users\\Reilley Pfrimmer\\source\\repos\\ARMBotDemo\\point.png").convert()
paintimg = pygame.image.load("C:\\Users\\Reilley Pfrimmer\\source\\repos\\ARMBotDemo\\paint.png").convert()
closeimg = pygame.image.load("C:\\Users\\Reilley Pfrimmer\\source\\repos\\ARMBotDemo\\close.png").convert()
uniobj = []

# port='COM4'

# print("Attempting to connect on port", port)

# try:
#     com = serial.Serial(port)
# except serial.SerialException:
#     print("Port unreachable.")
#     exit()

# class Motor:
#     def __init__(self, ID):
#         self.state = 0
#         self.ID = ID
#         write(self) # calibrate
#     def rotate(self, angle):
#         self.state = angle
#         write(self)

# def write(motor: Motor):
#     com.write('w {ID} {ANGLE}'.format(ID=motor.ID,ANGLE=motor.state).encode('utf-8'))

# m0 = Motor(0)
# m1 = Motor(1)

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
            
class ArmRep(Object):
    def __init__(self,x,y,colour,a,b,arad,brad):
        super().__init__(x,y,colour)
        self.arad = arad
        self.brad = brad
        self.a = a
        self.b = b
        self.aendpoint = (self.x+(self.a*np.cos(self.arad)),self.y+(self.a*np.sin(self.arad)))
        self.bendpoint = (self.aendpoint[0]+(self.b*np.cos(self.brad)),self.aendpoint[1]+(self.b*np.sin(self.brad)))
    def draw(self):
        pygame.draw.lines(root, self.colour, False, [[self.x,self.y],[self.aendpoint[0],self.aendpoint[1]],[self.bendpoint[0],self.bendpoint[1]]],width=30)
        self.aendpoint = (self.x+(self.a*np.cos(self.arad)),self.y+(self.a*np.sin(self.arad)))
        self.bendpoint = (self.aendpoint[0]+(self.b*np.cos(self.brad)),self.aendpoint[1]+(self.b*np.sin(self.brad)))
class Point(Object):
    def __init__(self,x,y,colour,a):
        super().__init__(x,y,colour)
        self.a = a
    def updatepos(self):
        self.x = targetpoint[0]
        self.y = targetpoint[1]
    def draw(self):
        pygame.draw.circle(root,self.colour,(self.x,self.y),self.a)

class PaintPoint(Object):
    def __init__(self,x,y):
        global l_ts
        super().__init__(x,y,[172, 236, 161])
        self.a = 10
        l_ts += 1
    def draw(self):
        pygame.draw.circle(root,self.colour,(self.x,self.y),self.a)

class OriginPoint(Object):
    def __init__(self,x,y):
        super().__init__(x,y,[0,0,0])
    def draw(self):
        pass # dont draw the origin point

origin = OriginPoint(centrepoint[0],centrepoint[1])
PJGP = EPICConga(0,0,gridimg)
arm = ArmRep(centrepoint[0],centrepoint[1],[185, 214, 242],seg1,seg2,-14.438,87.586)
target = Point(centrepoint[0]+targetpoint[0],centrepoint[1]-targetpoint[1],[255, 0, 0],10)

def roundline(start, end): # Credit where credit is due: I copied this from GFG
    Xaxis = end[0]-start[0]
    Yaxis = end[1]-start[1]
    dist = max(abs(Xaxis), abs(Yaxis))
    for i in range(dist):
        x = int(start[0]+float(i)/dist*Xaxis)
        y = int(start[1]+float(i)/dist*Yaxis)
        PaintPoint(x, y)

def checkCollision(x,y,rect):
    if (x > rect.x and x < rect.x+rect.w) and (y > rect.y and y < rect.y+rect.h):
        return True
    else:
        return False

def calculateAngles(a,b,x,y):
    c = np.sqrt(x**2 + y**2)
    B = (np.arccos((a**2+c**2-b**2)/(2*a*c)) - np.arctan(y/x)) * -1
    C = np.pi - np.arccos((a**2 + b**2 - c**2)/(2*a*b)) + B
    return B,C


while running: # main loop
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if checkCollision(mpos[0],mpos[1],dragmodebutton_border):
                mode = "drag"
                continue
            elif checkCollision(mpos[0], mpos[1], placemodebutton_border):
                mode = "point"
                continue
            elif checkCollision(mpos[0], mpos[1], paintmodebutton_border):
                mode = "paint"
                continue
            elif checkCollision(mpos[0], mpos[1], closemodebutton_border):
                running = False
                continue
            if mode == "drag":
                drag = True
                dragpoint = pygame.mouse.get_pos()
            elif mode == "point":
                originoffset = (centrepoint[0]-(origin.x),centrepoint[1]-(origin.y))
                targetpoint = list(pygame.mouse.get_pos())
                ctargetpoint = list(targetpoint)
                ctargetpoint[0] += originoffset[0]-centrepoint[0]
                ctargetpoint[1] += originoffset[1]-centrepoint[1]   
                if (np.sqrt((ctargetpoint[0])**2 + (ctargetpoint[1])**2) > reach):
                    if ctargetpoint[0] == 0:
                        ctargetpoint[0] += 0.01
                    th = np.arctan(ctargetpoint[1]/ctargetpoint[0])
                    ctargetpoint[0],ctargetpoint[1] = (reach*np.cos(th)),(reach*np.sin(th))
                    targetpoint[0] = ctargetpoint[0] + centrepoint[0] - originoffset[0]
                    targetpoint[1] = ctargetpoint[1] + centrepoint[1] - originoffset[1]
                B,C = calculateAngles(seg1,seg2,-ctargetpoint[0],-ctargetpoint[1])
                arm.arad = B
                arm.brad = C
                target.updatepos()  
                print(np.degrees(B),np.degrees(C-B)+90) # REPLACE with Serial Communication Code
            elif mode == "paint":
                paint = True
        if event.type == pygame.MOUSEBUTTONUP:
            if mode == "drag":
                drag = False
            if mode == "paint":
                tss.append(l_ts)
                l_ts = 0
                paint = False
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_LCTRL] and keys[pygame.K_z]:
                if tss[-1] > 0:
                    uniobj = uniobj[:-tss.pop(-1)]
    if paint == True:
        PaintPoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        roundline(pygame.mouse.get_pos(), prev_point)
    prev_point = pygame.mouse.get_pos()
    if drag == True:
        deltaX,deltaY = [x-y for x,y in zip(pygame.mouse.get_pos(),dragpoint)]
        for i in uniobj:
            i.move(deltaX,deltaY)
        dragpoint = pygame.mouse.get_pos()  
    root.fill("#061A40")
    for i in uniobj:
        i.draw()
    dragmodebutton_border = pygame.Rect(20,20,80,80)
    placemodebutton_border = pygame.Rect(20, 120, 80, 80)
    paintmodebutton_border = pygame.Rect(20,220,80,80)
    closemodebutton_border = pygame.Rect(20,320,80,80)
    root.blit(moveimg, (25,25))
    root.blit(pointimg, (25,125))
    root.blit(paintimg, (25,225))
    root.blit(closeimg, (25,325))
    pygame.draw.rect(root, [185, 214, 242], dragmodebutton_border, 5,2)
    pygame.draw.rect(root, [185, 214, 242], placemodebutton_border, 5,2)
    pygame.draw.rect(root, [185, 214, 242], paintmodebutton_border, 5,2)
    pygame.draw.rect(root, [185, 214, 242], closemodebutton_border, 5,2)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()