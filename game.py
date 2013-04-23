import pygame
from pygame.locals import *
from pygame import Color
import random, math
from random import *
from math import *

#enter screen dimensions here
WIDTH = 1280
HEIGHT = 720

class Ball(object):
    def __init__(self, screen, P1, P2, x=WIDTH/2,y=HEIGHT/2,vx=5,vy=5):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.diameter = 15        
        self.screen = screen
        self.p1 = P1
        self.p2 = P2
        self.maxspeed = 10
    def draw(self):
        pygame.draw.rect(self.screen, Color("white"), (self.x,self.y,self.diameter,self.diameter))
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        ##########################COLLISIONS################################################
        ## WALLS ##
        if self.x<=0:
            self.vx = -self.vx
            self.p2.score += 1
            self.x = WIDTH/2
            self.y = HEIGHT/2
        if self.x+self.diameter >= WIDTH:
            self.vx = -self.vx
            self.p1.score += 1
            self.x = WIDTH/2
            self.y = HEIGHT/2
        if self.y <=0:
            self.y = 0
            self.vy = -self.vy
        if self.y+self.diameter >= HEIGHT:
            self.y = HEIGHT-self.diameter
            self.vy = -self.vy
        ## PADDLES ##
        #p1 - Left Paddle #
        #detect collision
        if self.y <= self.p1.y+self.p1.height+5 and self.y+self.diameter >= self.p1.y-5 and self.x <= self.p1.x+self.p1.width and self.x >= self.p1.x: 
            self.vx = -self.vx
            #angle of rebound
            if self.y+(self.diameter/2) <= self.p1.y+(self.p1.height/2):
                self.vy = -(self.p1.y+(self.p1.height/2) - self.y+(self.diameter/2))/5
                if self.vy < -self.maxspeed:
                    self.vy = -self.maxspeed
            elif self.y+(self.diameter/2) >= self.p1.y+(self.p1.height/2):
                self.vy = (self.p1.y+(self.p1.height/2) + self.y+(self.diameter/2))/5
                if self.vy > self.maxspeed:
                    self.vy = self.maxspeed
            #speed up ball
                
        #move y speed in direction of area on paddle hit
        
        #p2 - right paddle#
        if self.y <= self.p2.y+self.p2.height+5 and self.y+self.diameter >= self.p2.y-5 and self.x+self.diameter >= self.p2.x and self.x <= self.p2.x+self.p2.width:
            self.vx = -self.vx
            #angle of rebound
            if self.y+(self.diameter/2) <= self.p2.y+(self.p2.height/2):
                self.vy = -(self.p2.y+(self.p2.height/2) - self.y+(self.diameter/2))/5
                if self.vy < -self.maxspeed:
                    self.vy = -self.maxspeed
            elif self.y+(self.diameter/2) >= self.p2.y+(self.p2.height/2):
                self.vy = (self.p2.y+(self.p2.height/2) + self.y+(self.diameter/2))/5
                if self.vy > self.maxspeed:
                    self.vy = self.maxspeed
            
            
        ## Player 2 AI
        ##GOING DOWN##
        ##assign new variables for easy seeing
        middleOfBall = float(self.y+(float(self.diameter/2)))
        paddleY = self.p2.y
        paddleHeight= self.p2.height
        paddleSpeed = self.p2.vy
        maxPaddleSpeed = self.p2.maxspeed
        middleOfPaddle = float(self.p2.y+(float(self.p2.height/2)))
        if middleOfBall > middleOfPaddle:
            #paddle vertical speed plus equals ball y coordinates minus middle of paddle
            paddleSpeed += middleOfBall-middleOfPaddle
            #cap the speed
            if paddleSpeed >= maxPaddleSpeed:
                paddleSpeed = maxPaddleSpeed
            #bottom paddle collision with wall
            if paddleY >= HEIGHT-paddleHeight:
                paddleY += 0
            #moves paddle y at given v, or vertical speed if not hitting bottom wall
            else:
                paddleY += paddleSpeed
        ##GOING UP##
        elif middleOfBall < (paddleY+middleOfPaddle):
            #paddle vertical speed plus equals ball y coordinates minus middle of paddle
            paddleSpeed -= middleOfPaddle-middleOfBall
            #cap the speed
            if paddleSpeed <= -maxPaddleSpeed:
                paddleSpeed = -maxPaddleSpeed
            #bottom paddle collision with wall
            if paddleY <= 0:
                paddleY -= 0
            #moves paddle y at given v, or vertical speed if not hitting bottom wall
            else:
                paddleY += paddleSpeed
        else:
            paddleSpeed = 0
        ##reassign new variables to original
        self.p2.y = paddleY
        self.p2.vy = paddleSpeed
        
class P1(object):
    def __init__(self,screen,y=HEIGHT/2,vy=10, score = 0):
        self.width = 20
        self.height = 80
        self.x = 20
        self.y = y
        self.vy = vy
        self.score = score
        self.screen = screen
    def draw(self):
        pygame.draw.rect(self.screen, Color("white"), (self.x,self.y,self.width,self.height))
        label = myfont.render(str(self.score), 1, Color('white'))
        self.screen.blit(label, (WIDTH/2-100, 50))
    def update(self):
        ## MOVEMENT ##
        # get all keys currently being pressed
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            self.y -= self.vy
        if keys[K_DOWN]:
            self.y += self.vy
        ##wall collision
        if self.y <= 0:
            self.y = 0
        elif self.y >= HEIGHT-self.height:
            self.y = HEIGHT-self.height
        
        
class P2(object):  

    def __init__(self,screen,y=HEIGHT/2,vy=0, score = 0):
        self.width = 20
        self.height = 80
        self.x = WIDTH-(self.width*2)
        self.y = y
        self.vy = vy
        self.maxspeed = 9
        self.score = score
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, Color("white"), (self.x,self.y,self.width,self.height))
        label = myfont.render(str(self.score), 1, Color('white'))
        self.screen.blit(label, (WIDTH/2+100, 50))
        
    def update(self):
        ## AI ##
        ##wall collision
        if self.y <= 0:
            self.y = 0
        elif self.y >= HEIGHT-self.height:
            self.y = HEIGHT-self.height

def Draw(ball, p1, p2):
    ball.draw()
    p1.draw()
    p2.draw()
    y = 0
    #net
    for i in range(20):
        pygame.draw.rect(screen,Color('white'),(WIDTH/2+10,y,10,20))
        y += HEIGHT/20
    #border
    borderStroke = 2
    #top
    pygame.draw.rect(screen,Color('white'),(0,0,WIDTH,borderStroke))
    #left
    pygame.draw.rect(screen,Color('white'),(0,0,borderStroke,HEIGHT))
    #bottom
    pygame.draw.rect(screen,Color('white'),(0,HEIGHT-borderStroke,WIDTH,borderStroke))
    #right
    pygame.draw.rect(screen,Color('white'),(WIDTH-borderStroke,0,borderStroke,HEIGHT))


def Update(ball, p1, p2):
    p1.update()
    p2.update()
    ball.update()
    
    
def init():
    #apply screen width and height to new pygame window. Available options for second parameter of set_mode: HWSURFACE|DOUBLEBUF|FULLSCREEN|RESIZABLE|NOFRAME
    global WIDTH, HEIGHT, screen, clock, windowDimensions
    pygame.init()
    windowDimensions = (WIDTH,HEIGHT)
    screen = pygame.display.set_mode(windowDimensions,FULLSCREEN|DOUBLEBUF|HWSURFACE)
    #set title of pygame window
    pygame.display.set_caption("Falldown") 
    #create a clock for fps
    clock = pygame.time.Clock()
    global myfont
    myfont = pygame.font.Font("emulogic.ttf", 30)
    global codeFont
    codeFont = pygame.font.Font("emulogic.ttf", 20)
    
def mainGame():    
    ##############GAME LOOP###############
    init()
    global screen
    global windowDimensions
    #Game objects
    p1 = P1(screen)
    p2 = P2(screen)
    ball = Ball(screen, p1, p2)
    
    while True: 
        #quits when escape is pressed
        for e in pygame.event.get():
            if e.type is KEYDOWN and e.key == K_ESCAPE or e.type == QUIT:
                return

        #function calls
        #clears the screen
        screen.fill(Color("black"))
        Draw(ball, p1, p2) 
        Update(ball, p1, p2)
        #frame rate
        fps = int(clock.get_fps())
        label = codeFont.render(str(fps)+" fps", 1, Color('green'))
        screen.blit(label, (20, 20))
        pygame.display.flip()
        clock.tick(60)

mainGame()
	
