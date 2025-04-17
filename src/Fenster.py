
from enum import Enum
import pygame
import pygame.freetype
from pygame.locals import *
pygame.init()

class windowtypes(Enum):
    login = 1
    game = 2
    win = 3
    lose = 4

display = pygame.display.Info()
screen = pygame.display.set_mode((display.current_w, display.current_h - 60), 0,0,0)
pygame.display.set_caption('Keplerwolf')
screen.fill((255,255,255))
pygame.display.flip()

windowstate = 0
def setstate(window):
    windowstate = window
    onstatechange(windowstate)

def onstatechange(windowstate):
    if windowstate == windowtypes.login:
        pygame.freetype.init()
        font = pygame.font.SysFont('Consolas', 30)
        text_surface = font.render("Login", False, (255, 255, 0))
        screen.blit(text_surface,(display.current_w//2 - 20, 50), (0, 0, 200, 50), 0)
        
def onquit():
    #s.close()
    pass


running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            onquit()
            running = False
    setstate(windowtypes.login)
