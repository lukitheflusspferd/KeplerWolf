from IPencodedecode import encodeIP, decodeIP
from enum import Enum
from ClassButton import Button
import pygame
import pygame.freetype
from pygame.locals import *
import sys   
import socket
import json
pygame.init() 


class windowtypes(Enum):
    login = 1
    lobby = 2
    game = 3
    win = 4
    lose = 5

global inputonscreen
clock = pygame.time.Clock() 
display = pygame.display.Info()
screen = pygame.display.set_mode((display.current_w, display.current_h - 60), 0,0,0)
pygame.display.set_caption('Keplerwolf')
screen.fill((255,255,255))
pygame.display.flip()

inputonscreen = False
base_font = pygame.font.Font(None, 32) 
global user_text
user_text = '' 

# create rectangle 
background_rect = pygame.Rect(195, 195, 110, 42)
input_rect = pygame.Rect(200, 200, 140, 32) 
color_active = pygame.Color('lightskyblue3')

# color of input box. 
color_passive = pygame.Color('chartreuse4') 
color = color_passive
  
active = False

windowstate = 0
def setstate(window):
    windowstate = window
    onstatechange(windowstate)

def onstatechange(state):
    global inputonscreen
    if state == windowtypes.login:
        screen.fill((255,255,255))
        global windowstate
        windowstate = windowtypes.login
        # abfragen ob hosten oder joinen
        undecided = True
        global ishosting
        ishosting = False
        while undecided:
            font = pygame.font.SysFont('Comic Sans', 30)
            text_surface = font.render("Hosten oder Joinen?", False, (0,0,0))
            text_rect = text_surface.get_rect(center=(display.current_w // 2, display.current_h // 2 - 80))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            Button1 = Button((0, 255, 0), display.current_w // 2 + 25, display.current_h // 2 + 45, 110, 42, "Hosten")
            Button1.draw(screen, outline=(0, 0, 0))
            Button2 = Button((0, 255, 0), display.current_w // 2 - 135, display.current_h // 2 + 45, 110, 42, "Joinen")
            Button2.draw(screen, outline=(0, 0, 0))
            pygame.display.flip()
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Button1.isOver(event.pos):
                        ishosting = True
                        print("Hosten")
                        # Hier Code für Hosten einfügen
                        undecided = False
                    elif Button2.isOver(event.pos):
                        # Joinen
                        print("Joinen")
                        # Hier Code für Joinen einfügen
                        undecided = False
        drawover_rect = pygame.Rect(display.current_w // 2 - 250, display.current_h // 2-100 , 500, 300)
        pygame.draw.rect(screen, (255,255,255), drawover_rect)
        global background_rect 
        background_rect = pygame.Rect(display.current_w // 2 - 55, display.current_h // 2 + 45, 110, 42)
        global input_rect
        input_rect = pygame.Rect(display.current_w // 2 - 50, display.current_h // 2 + 50, 100, 32)

        inputonscreen = True
        font = pygame.font.SysFont('Comic Sans', 30)
        text_surface = font.render("Login", False, (0,0,0))
        text_rect = text_surface.get_rect(center=(display.current_w // 2, display.current_h // 2 - 80))        
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        if ishosting:
            # Hier Code für Hosten einfügen
            text_surface = font.render("Lobby Code:", False, (0,0,0))
            text_rect = text_surface.get_rect(center=(display.current_w // 2 + 500, display.current_h // 2-80))
            screen.blit(text_surface, text_rect)
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            lobbycode = encodeIP(IPAddr)
            text_surface = font.render(lobbycode, False, (0,0,0))
            text_rect = text_surface.get_rect(center=(display.current_w // 2 + 500, display.current_h // 2-40))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pass
            confirmusername("")
        else:
            confirmip("")
    if state == windowtypes.lobby:
        if inputonscreen:
            inputonscreen = False
            onstatechange(windowtypes.lobby)
        else:   
            drawover_rect = pygame.Rect(display.current_w // 2 - 250, display.current_h // 2-400 , 500, 900)
            pygame.draw.rect(screen, (255,25,255), drawover_rect)
            pygame.display.flip()
            font = pygame.font.SysFont('Comic Sans', 30)
            text_surface = font.render("Lobby", False, (0,0,0))
            text_rect = text_surface.get_rect(center=(display.current_w // 2, display.current_h // 2 - 80))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            

global ipconfirmed
ipconfirmed = False            

def checkConnection(ip, port):
    pass # DAS IST EIN PLACEHOLDER BIS WIR CLIENTCOMM IMPORTIEREN KÖNNEN

def confirmip(ip):
    global ipconfirmed #VON HIER
    ipconfirmed = True
    filllogintext()
    confirmusername("")
        # BIS HIER RAUSNEHMEN WENN WIR DAS RICHTIG LAUFEN LASSEN, das nur weil ip ja nicht aktiv ist
    print("Joa 1")
    font = pygame.font.SysFont('Comic Sans', 30)
    text_surface = font.render("Lobby Code eingeben:", False, (0,0,0))
    text_rect = text_surface.get_rect(center=(display.current_w // 2, display.current_h // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    if ip != '':
        print("Joa 2")
        ip = decodeIP(ip)         
        port = 65432
        # Check connection
        print(f"Versuche, Server an IP [{ip}] zu erreichen...")
        try:
            if checkConnection(ip, port):
                print("Erfolgreich verbunden!")
                connected = True
            else:
                print(f"Verbindung fehlgeschlagen. Bitte probiere eine andere IP-Adresse.")
        except Exception as e:
            print(f"Der folgende Fehler ist aufgetreten: {e}\n Bitte versuche es erneut.")
        ipvalid = False
        if ipvalid:
            return True
            filllogintext()
            confirmusername("")
        else:
            font = pygame.font.SysFont('Comic Sans', 30)
            text_surface = font.render("Lobby Code nicht gültig", False, (255,0,0))
            text_rect = text_surface.get_rect(center=(display.current_w // 2, display.current_h // 2 + 125))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()

global usernameconfirmed
usernameconfirmed = False

def confirmusername(name):
    print("Joa 3")
    font = pygame.font.SysFont('Comic Sans', 30)
    text_surface = font.render("Spielernamen eingeben:", False, (0,0,0))
    text_rect = text_surface.get_rect(center=(display.current_w // 2, display.current_h // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    if name != '':
        print("Joa 4")
        # Spielernamen abfragen solange der Server diesen noch nicht validiert hat (z.B. bei Dopplung eines Namens)

        message = {
            "type":"UsernamePing",
            "data": name
        }
        b_message = json.dumps(message).encode('utf-8')     #BEIM AUSFÜHREN KOMMENTARE WEGMACHEN, NUR FÜR TESTEN
        #s.send(b_message)
        print("Name an Server gesendet")
        #b_answer = s.recv(1024)
        #print("[{}] {}".format(ip, b_answer.decode("utf-8")))
        #print("")
        #answer = eval(b_answer.decode())
        #global usernameconfirmed
        #usernameconfirmed = answer
        #if usernameconfirmed:
        #   filllogintext()
        #   onstatechange(windowtypes.lobby)
        filllogintext()
        onstatechange(windowtypes.lobby)     
def filllogintext():
    fill_rect1 = pygame.Rect(display.current_w // 2 - 250, display.current_h // 2-30 , 500, 60)
    fill_rect2 = pygame.Rect(display.current_w // 2 - 250, display.current_h // 2 + 100, 500, 120)
    pygame.draw.rect(screen, (255,255,255), fill_rect1)
    pygame.draw.rect(screen, (255,255,255), fill_rect2)

def onquit():
    #s.close()
    pass

onstatechange(windowtypes.login)
while True: 
    for event in pygame.event.get(): 
  
      # if user types QUIT then the screen will close 
        if event.type == pygame.QUIT: 
            pygame.quit() 
            onquit()
            sys.exit() 
        if inputonscreen:
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if input_rect.collidepoint(event.pos): 
                    active = True
                else: 
                    active = False

            if event.type == pygame.KEYDOWN: 

                # Check for backspace 
                if event.key == pygame.K_BACKSPACE: 
                    # get text input from 0 to -1 i.e. end. 
                    user_text = user_text[:-1] 
                # Unicode standard is used for string formation 
                elif event.key != pygame.K_RETURN: 
                    user_text += event.unicode
                # print usertext when enter is pressed                
                elif event.key == pygame.K_RETURN:
                    print(user_text)
                    if windowstate == windowtypes.login:
                        if not ipconfirmed and not ishosting:
                            confirmip(user_text)
                        elif not usernameconfirmed:
                            confirmusername(user_text)
                    elif windowstate == windowtypes.game:
                        pass
            if windowstate != windowtypes.lobby:
                if active: 
                    color = color_active 
                else: 
                    color = color_passive 
                    
                # draw rectangle and argument passed which should be on screen 
                pygame.draw.rect(screen, (0,0,0), background_rect)
                pygame.draw.rect(screen, color, input_rect) 
                
                text_surface = base_font.render(user_text, True, (255, 255, 255)) 
                
                # render at position stated in arguments 
                screen.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
                
                # set width of textfield so that text cannot get outside of user's text input 
                input_rect.w = max(100, text_surface.get_width()+10) 
                if windowstate == windowtypes.lobby:
                    drawover_rect = pygame.Rect(display.current_w // 2 - 250, display.current_h // 2-400 , 500, 900)
                    pygame.draw.rect(screen, (255,25,255), drawover_rect)
                    
                
                pygame.display.flip()
                # clock.tick(60) means that for every second at most 
                # 60 frames should be passed. 
                clock.tick(60) 
