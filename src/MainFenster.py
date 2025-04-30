from IPencodedecode import encodeIP, decodeIP
from enum import Enum
from ClassButton import Button
import pygame
import pygame.freetype
from pygame.locals import *
import sys   
import socket
import json
from time import sleep
from ClientData import computePing, validName, getMailbox, setMailbox
from Ping import fromData, toData
pygame.init() 
global answer 

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
ip = ""

ishosting = False
firststart = True

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
    """
    ändert die windowstate, macht später vllt mehr
    """
    global windowstate
    windowstate = window
    onstatechange(windowstate)

def onstatechange(state):
    """
    führt die Hauptveränderungen auf dem Bildschirm durch
    """
    global inputonscreen
    global ishosting
    global ButtonStart, ButtonLeft, ButtonRight
    if state == windowtypes.login:
        screen.fill((255,255,255))
        # abfragen ob hosten oder joinen
        undecided = True
        
        ishosting = False
        while undecided:
            font = pygame.font.SysFont('comicsans', 30)
            text_surface = font.render("Hosten oder Joinen?", False, (0,0,0))
            text_rect = text_surface.get_rect(center=(display.current_w // 2, display.current_h // 2 - 80))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            ButtonStart = Button((0, 255, 0), display.current_w // 2 + 25, display.current_h // 2 + 45, 110, 42, "Hosten")
            ButtonStart.draw(screen,"comicsans", outline=(0, 0, 0))
            ButtonLeft = Button((0, 255, 0), display.current_w // 2 - 135, display.current_h // 2 + 45, 110, 42, "Joinen")
            ButtonLeft.draw(screen,"comicsans", outline=(0, 0, 0))
            pygame.display.flip()
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ButtonStart.isOver(event.pos):
                        
                        ishosting = True
                        print("Hosten")
                        # Hier Code für Hosten einfügen
                        undecided = False
                    elif ButtonLeft.isOver(event.pos):
                        # Joinen
                        print("Joinen")
                        # Hier Code für Joinen einfügen
                        undecided = False
        drawover_rect = pygame.Rect(display.current_w // 2 - 250, display.current_h // 2-100 , 500, 300)
        pygame.draw.rect(screen, (255,255,255), drawover_rect)
        global background_rect 
        background_rect = pygame.Rect(display.current_w // 2 - 95, display.current_h // 2 + 45, 190, 42)
        global input_rect
        input_rect = pygame.Rect(display.current_w // 2 - 90, display.current_h // 2 + 50, 180, 32)

        inputonscreen = True
        font = pygame.font.SysFont('comicsans', 30)
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
            IP = socket.gethostbyname(hostname)
            lobbycode = encodeIP(IP)
            text_surface = font.render(lobbycode, False, (0,0,0))
            text_rect = text_surface.get_rect(center=(display.current_w // 2 + 500, display.current_h // 2-40))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            confirmusername("")
        else:
            confirmip("")
    if state == windowtypes.lobby:
        inputonscreen = False
        drawover_rect = pygame.Rect(display.current_w // 2 - 250, display.current_h // 2-400 , 500, 900)
        pygame.draw.rect(screen, (255,255,255), drawover_rect)
        pygame.display.flip()
        font = pygame.font.SysFont('comicsans', 60)
        text_surface = font.render("Lobby", False, (0,0,0))
        text_rect = text_surface.get_rect(center=(display.current_w // 2, 100))
        screen.blit(text_surface, text_rect)
        pygame.draw.line(screen, (0, 0, 0), (display.current_w//4, 0), (display.current_w//4, display.current_h),5)
        font = pygame.font.SysFont('comicsans', 30)
        text_surface = font.render("Spieler", False, (0,0,0))
        text_rect = text_surface.get_rect(center=(display.current_w // 8, 100))
        screen.blit(text_surface, text_rect)
        # Hier Code für Spielerliste einfügen
        
        if ishosting:
            ButtonStart = Button((0, 255, 0), display.current_w // 2 - 55, display.current_h // 2 + 150, 110, 42, "Start")
            ButtonStart.draw(screen,"comicsans", outline=(0, 0, 0))
        # Hier Spielermodels einfügen
        ButtonLeft = Button((0, 255, 0), display.current_w // 2 - 40, display.current_h // 2 + 20, 40, 42, "<")
        ButtonLeft.draw(screen,"sans-serif", outline=(0, 0, 0))
        ButtonRight = Button((0, 255, 0), display.current_w // 2 , display.current_h // 2 + 20, 40, 42, ">")
        ButtonRight.draw(screen,"sans-serif", outline=(0, 0, 0))
        pygame.display.flip()
        
                    
                    # Hier Code für nächsten Spielermodel einfügen
    if state == windowtypes.game:
        global firststart
        if firststart:
            firststart = False
            screen.fill((255,255,255))
            ButtonHideRole.draw(screen,"sans-serif", outline=(0,0,0))
        
        
        

        

global ipconfirmed
ipconfirmed = False            

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def checkConnection(ip, port, timeout=2):
    """
    Prüfen, ob mit der gegebenen IP und dem gegebenen Port eine Verbindung aufgebaut werden kann
    """
    try:
        socket.setdefaulttimeout(timeout)
        s.connect((ip, port))
        return True
    except (socket.error, socket.timeout):
        return False
    finally:
        socket.setdefaulttimeout(None)

def filllogintext():
    """
    übermalt die Login anzeigen um platz für neuen Text zu machen
    """
    fill_rect1 = pygame.Rect(display.current_w // 2 - 550, display.current_h // 2-30 , 1100, 60)
    fill_rect2 = pygame.Rect(display.current_w // 2 - 550, display.current_h // 2 + 100, 1100, 120)
    pygame.draw.rect(screen, (255,255,255), fill_rect1)
    pygame.draw.rect(screen, (255,255,255), fill_rect2)

def confirmip(ip1):
    """
    überprüft, ob eine ip zugängig ist auf dem lokalen Netzwerk
    """
    global ipconfirmed
    print("Joa 1")
    global ip
    ip = ip1
    font = pygame.font.SysFont('comicsans', 30)
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
                ipconfirmed = True
            else:
                print(f"Verbindung fehlgeschlagen. Bitte probiere eine andere IP-Adresse.")
        except Exception as e:
            print(f"Der folgende Fehler ist aufgetreten: {e}\n Bitte versuche es erneut.")
        if ipconfirmed:
            return True
            filllogintext()
            confirmusername("")
        else:
            font = pygame.font.SysFont('comicsans', 30)
            text_surface = font.render("Lobby Code nicht gültig", False, (255,0,0))
            text_rect = text_surface.get_rect(center=(display.current_w // 2, display.current_h // 2 + 125))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()

global usernameconfirmed
usernameconfirmed = False

def confirmusername(name):
    """
    prüft ob ein username schon besetzt ist, loggt Spieler mit Namen ein
    """
    print("Joa 3")
    font = pygame.font.SysFont('comicsans', 30)
    text_surface = font.render("Spielernamen eingeben:", False, (0,0,0))
    text_rect = text_surface.get_rect(center=(display.current_w // 2, display.current_h // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    if name != '':
        print("Joa 4")
        # Spielernamen abfragen solange der Server diesen noch nicht validiert hat (z.B. bei Dopplung eines Namens)

        message = fromData("UsernamePing", str(name))
        b_message = json.dumps(message).encode('utf-8')    
        s.send(b_message)
        print("Name an Server gesendet")
        b_answer = s.recv(1024)
        print("[{}] {}".format(ip, b_answer.decode("utf-8")))
        print("")
        answer = json.loads(b_answer.decode("utf-8"))
        answertype, answer = toData(answer)
        global usernameconfirmed
        if answertype == "UsernameValidationPing":
            if answer["valid"] == "True":
                usernameconfirmed = True
            elif answer["error"] == "doppelt":
                font = pygame.font.SysFont('comicsans', 20)
                text_surface = font.render("Spielername schon verwendet, gebe einen anderen ein.", False, (255,0,0))
                text_rect = text_surface.get_rect(center=(display.current_w // 2, display.current_h // 2 + 125))
                screen.blit(text_surface, text_rect)
                pygame.display.flip
            elif answer["error"] == "bereits gestartet":
                font = pygame.font.SysFont('comicsans', 20)
                text_surface = font.render("Das Spiel, welchem du beitreten willst ist schon gestartet.", False, (255,0,0))
                text_rect = text_surface.get_rect(center=(display.current_w // 2, display.current_h // 2 + 125))
                screen.blit(text_surface, text_rect)
                pygame.display.flip
        if usernameconfirmed:
           filllogintext()
           setstate(windowtypes.lobby)

def updatePlayerList(data):
    for i in data:
        print("HHHHHHHHHHHHHHHH" + i)
    for i in data:
        pass

def hiderole():
    drawover_rect = pygame.Rect(0,0, 1100, 3000)
    pygame.draw.rect(screen, (255,255,255), fill_rect1)
def showrole():
    drawover_rect = pygame.Rect(0,0, 1100, 3000)
    pygame.draw.rect(screen, (255,255,255), fill_rect1)
def onquit():
    """
    beendet die Verbindung zum Server vor dem Beenden des Programms um nicht den Server zu Crashen
    """
    s.close()
    pass

ButtonHideRole = Button((0,255,0), 50, 100, 100, 42, "Rolle verstecken" )
ButtonShowRole = Button((0,255,0), 50, 100, 100, 42, "Rolle anzeigen" )
ButtonHideRoleonscreen = False
ButtonShowRoleonscreen = False

setstate(windowtypes.login)
while True: 
    
    message = fromData("EmptyPing", "")

    if ipconfirmed:
        global mailbox
        mailbox = getMailbox()

        if mailbox != []:
            b_mailbox = json.dumps(mailbox[0]).encode('utf-8')
            s.send(b_mailbox)
            mailbox.pop
            print("Mailbox an Server gesendet")
        else: 
            b_message = json.dumps(message).encode('utf-8')
            s.send(b_message)
            print("EmptyPing an Server gesendet")

        b_answer = s.recv(1024)
        print(b_answer.decode())
        print("[{}] {}".format(ip, b_answer.decode()))
        print("")
        answer = json.loads(b_answer.decode("utf-8"))
        computePing(json.loads(b_answer.decode("utf-8")))
        if windowstate == windowtypes.lobby:
            pingtype, playerlist = toData(answer)
            updatePlayerList(playerlist)
        sleep(1)
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
                if windowstate == windowtypes.lobby:
                    if ButtonStart.isOver(event.pos):
                        print("Spiel starten")
                        setstate(windowtypes.game)
                    elif ButtonLeft.isOver(event.pos):
                        pass
                        # Hier Code für vorherigen Spielermodel einfügen
                    elif ButtonRight.isOver(event.pos):
                        pass
                if windowstate == windowtypes.game:
                    if ButtonHideRoleonscreen:
                        if ButtonHideRole.isOver(event.pos):
                            hiderole()
                    if ButtonShowRoleonscreen:
                        if ButtonShowRole.isOver(event.pos):
                            showrole()


            if event.type == pygame.KEYDOWN: 
                if active:
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
                                if confirmip(user_text):
                                    filllogintext()
                                    confirmusername("")
                                    user_text = ""
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
                if not usernameconfirmed: 
                    pygame.draw.rect(screen, (0,0,0), background_rect)
                    pygame.draw.rect(screen, color, input_rect) 
                    
                    text_surface = base_font.render(user_text, True, (255, 255, 255)) 
                    
                    # render at position stated in arguments 
                    screen.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
                    
                    # set width of textfield so that text cannot get outside of user's text input 
                    input_rect.w = max(180, text_surface.get_width()+10) 
                    if windowstate == windowtypes.lobby:
                        drawover_rect = pygame.Rect(display.current_w // 2 - 250, display.current_h // 2-400 , 500, 900)
                        pygame.draw.rect(screen, (255,25,255), drawover_rect)
                        
                
                pygame.display.flip()
                # clock.tick(60) means that for every second at most 
                # 60 frames should be passed. 
                clock.tick(60) 
