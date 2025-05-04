from IPencodedecode import encodeIP, decodeIP
from ClassPlayer import Player
from ClassRole import Role
from enum import Enum
from ClassButton import Button
import pygame
import pygame.freetype
from pygame.locals import *
import sys   
import socket
import json
from time import sleep
from ClientData import computePing, validName, getMailbox, setMailbox, getPlayerData
from Ping import fromData, toData
pygame.init() 
global answer 
global ownName
ownName = None
player = None

class windowtypes(Enum):
    login = 1
    lobby = 2
    game = 3
    win = 4
    lose = 5
testplayer = Player("Test")
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


# create rectangle 
background_rect = pygame.Rect(195, 195, 110, 42)
input_rect = pygame.Rect(200, 200, 140, 32) 
color_active = pygame.Color('lightskyblue3')

# color of input box. 
color_passive = pygame.Color('chartreuse4') 
color = color_passive
istesting = False
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
    global inputonscreen, input_rect, background_rect, ishosting
    # global ButtonStart, ButtonLeft, ButtonRight
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
            ButtonHost = Button((0, 255, 0), display.current_w // 2 + 25, display.current_h // 2 + 45, 110, 42, "Hosten")
            ButtonHost.draw(screen,"comicsans", outline=(0, 0, 0))
            ButtonJoin = Button((0, 255, 0), display.current_w // 2 - 135, display.current_h // 2 + 45, 110, 42, "Joinen")
            ButtonJoin.draw(screen,"comicsans", outline=(0, 0, 0))
            ButtonTest = Button((0, 255, 0), display.current_w // 2 - 135, display.current_h // 2 + 100, 110, 42, "Test")
            ButtonTest.draw(screen,"comicsans", outline=(0, 0, 0))
            pygame.display.flip()
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ButtonHost.isOver(event.pos):
                        
                        ishosting = True
                        print("Hosten")
                        # Hier Code für Hosten einfügen
                        undecided = False
                    elif ButtonJoin.isOver(event.pos):
                        # Joinen
                        print("Joinen")
                        # Hier Code für Joinen einfügen
                        undecided = False
                    elif ButtonTest.isOver(event.pos):
                        global playerData, testplayer, istesting
                        istesting = True
                        playerData = testplayer
                        undecided = False
                        filllogintext()
                        setstate(windowtypes.game)
        if not istesting:                
            drawover_rect = pygame.Rect(display.current_w // 2 - 250, display.current_h // 2-100 , 500, 300)
            pygame.draw.rect(screen, (255,255,255), drawover_rect)
            global background_rect 
            background_rect = pygame.Rect(display.current_w // 2 - 95, display.current_h // 2 + 45, 190, 42)
            global input_rect
            input_rect = pygame.Rect(display.current_w // 2 - 90, display.current_h // 2 + 50, 180, 32)

            inputonscreen = True
            pygame.draw.rect(screen, (0,0,0), background_rect)
            pygame.draw.rect(screen, color, input_rect)
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

        # Hier Code für Spielerliste einfügen
        if False: #RAUSGENOMMEN WEIL HOSTEN DURCH CONSOLE UND NICHT ÜBER GUI UND KEINE SPIELERMODELS    
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
        screen.fill((255,255,255))
        global ButtonHideRoleonscreen
        ButtonHideRoleonscreen = True
        ButtonHideRole.draw(screen,"comicsans", outline=(0,0,0))
        line_rect = pygame.Rect(display.current_w//6, 0, 5, display.current_h)
        pygame.draw.rect(screen, (0, 0, 0), line_rect)
        line_rect = pygame.Rect(display.current_w//6*5, 0, 5, display.current_h)
        pygame.draw.rect(screen, (0, 0, 0), line_rect)
        inputonscreen = True
        background_rect = pygame.Rect(display.current_w // 6 * 5 + 15, display.current_h // 8*6.5, display.current_w // 6 - 30, 42)
        input_rect = pygame.Rect(display.current_w // 6 * 5 + 20, display.current_h //8 *6.5+5, display.current_w // 6 - 40, 32)
        pygame.draw.rect(screen, (0,0,0), background_rect)
        pygame.draw.rect(screen, color, input_rect)
        print(background_rect)
        pygame.display.flip()
        displayrole()
        
        
        

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
    global ownName
    print("Joa 3")
    font = pygame.font.SysFont('comicsans', 30)
    text_surface = font.render("Spielernamen eingeben:", False, (0,0,0))
    text_rect = text_surface.get_rect(center=(display.current_w // 2, display.current_h // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    if name != '':
        print("Joa 4")
        # Spielernamen abfragen solange der Server diesen noch nicht validiert hat (z.B. bei Dopplung eines Namens)

        message = fromData("UsernamePing", str(name), ownName)
        b_message = json.dumps(message).encode('utf-8')    
        s.send(b_message)
        print("Name an Server gesendet")
        b_answer = s.recv(1024)
        print("[{}] {}".format(ip, b_answer.decode("utf-8")))
        print("")
        answer = json.loads(b_answer.decode("utf-8"))
        answertype, answer, _ = toData(answer)
        global usernameconfirmed
        if answertype == "UsernameValidationPing":
            if answer["valid"] == "True":
                usernameconfirmed = True
                ownName = name
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
    if data != []:
        for i in data:
            print("HHHHHHHHHHHHHHHH" + i)
        drawover_rect = pygame.Rect(0, 0, display.current_w//4-10 , display.current_h)
        pygame.draw.rect(screen, (255,255,255), drawover_rect)
        print("übergemalt")
        pygame.display.flip()
        font = pygame.font.SysFont('comicsans', 40)
        text_surface = font.render("Spieler", False, (0,0,0))
        text_rect = text_surface.get_rect(center=(display.current_w // 8, 100))
        screen.blit(text_surface, text_rect)
        font = pygame.font.SysFont('comicsans', 20)
        for i in data:
            text_surface = font.render(i, False, (0,0,0))
            text_rect = text_surface.get_rect(center=(display.current_w // 8, 150 + data.index(i) * 30))
            screen.blit(text_surface, text_rect)
            print("name gemacht und so")
        pygame.display.flip()

def hiderole():
    print("Hide Role")
    drawover_rect = pygame.Rect(0,0, display.current_w//6, display.current_h)
    pygame.draw.rect(screen, (255,255,255), drawover_rect)
    global ButtonHideRoleonscreen, ButtonShowRoleonscreen
    ButtonHideRoleonscreen = False
    ButtonShowRoleonscreen = True
    ButtonShowRole.draw(screen,"comic-sans", outline=(0,0,0))
    pygame.display.flip()

def showrole():
    print("Show Role")
    drawover_rect = pygame.Rect(0,0, display.current_w//6, display.current_h)
    pygame.draw.rect(screen, (255,255,255), drawover_rect)
    global ButtonHideRoleonscreen, ButtonShowRoleonscreen
    ButtonHideRoleonscreen = True
    ButtonShowRoleonscreen = False
    ButtonHideRole.draw(screen,"comic-sans", outline=(0,0,0))
    displayrole()
    pygame.display.flip()

def displayrole():
    global playerData
    font = pygame.font.SysFont('sans-serif', 20)
    if not istesting:
        playerData = getPlayerData()
    print(playerData)
    print(type(playerData))
    role = playerData.getrole()
    font = pygame.font.SysFont('comicsans', 25)
    text_surface = font.render("Rolle:", False, (0,0,0))
    text_rect = text_surface.get_rect(center=(display.current_w // 12, 200))
    screen.blit(text_surface, text_rect)
    text_surface = font.render(role.getname() , False, (0,0,0))
    text_rect = text_surface.get_rect(center=(display.current_w // 12, 240))
    screen.blit(text_surface, text_rect)
    font = pygame.font.SysFont('comicsans', 20)
    roledescription = role.getdescription()
    descriptionlist = list(roledescription)
    temp1 = []
    temp2 = []
    temp3 = ""
    j = 0
    for i in descriptionlist:
        temp1.append(i)
        j += 1
        if j >= 13:
            if i == " ":
                for k in range(j):
                    temp3 +=temp1[k]
                temp2.append(temp3)
                temp1 = []
                temp3 = ""
                j = 0
    for i in temp1:
        temp3 += i
    temp2.append(temp3)
    print(temp2)
    for i in temp2:            
        text_surface = font.render(i, False, (0,0,0))
        text_rect = text_surface.get_rect(center=(display.current_w // 12, 300 + temp2.index(i)*25))
        screen.blit(text_surface, text_rect) 
    pygame.display.flip()
    

def onquit():
    """
    beendet die Verbindung zum Server vor dem Beenden des Programms um nicht den Server zu Crashen
    """
    nameremoved = False
    message = fromData("LeaveLobbyPing", "", ownName) 
    b_mailbox = json.dumps(message).encode('utf-8')
    s.send(b_mailbox)
    mailbox.pop
    print("Mailbox an Server gesendet")
    while not nameremoved:
        b_answer = s.recv(1024)
        print(b_answer.decode())
        print("[{}] {}".format(ip, b_answer.decode()))
        print("")
        answer = json.loads(b_answer.decode("utf-8"))
        computePing(json.loads(b_answer.decode("utf-8")), ownName)
        answertype, answer, _ = toData(answer)
        if answertype == "EmptyPing":
            nameremoved = True
        sleep(1)
    s.close()
    pass

ButtonHideRole = Button((0,255,0), 25, 50, display.current_w//6-50, 42, "Rolle verstecken", 25 )
ButtonShowRole = Button((0,255,0), 25, 50, display.current_w//8-50, 42, "Rolle anzeigen", 25 )
ButtonHideRoleonscreen = False
ButtonShowRoleonscreen = False

setstate(windowtypes.login)
while True: 
    
    message = fromData("EmptyPing", "", ownName)

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
        computePing(json.loads(b_answer.decode("utf-8")), ownName)
        if windowstate == windowtypes.lobby:
            pingtype, playerlist, _ = toData(answer)
            if pingtype == "NewLobbyPing":
                updatePlayerList(playerlist)
        pingtype, data, _ = toData(answer)
        if pingtype == "GameStartPing":
            setstate(windowtypes.game)
            playerData = getPlayerData()

        sleep(1)
    for event in pygame.event.get(): 
  
      # if user types QUIT then the screen will close 
        if event.type == pygame.QUIT: 
            if not istesting:
                onquit()
            pygame.quit() 
            sys.exit() 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if windowstate == windowtypes.game:
                if ButtonHideRoleonscreen:
                    if ButtonHideRole.isOver(event.pos):
                        hiderole()
                if ButtonShowRoleonscreen:
                    if ButtonShowRole.isOver(event.pos):
                        showrole()
            if inputonscreen:
                if input_rect.collidepoint(event.pos): 
                    active = True
                else: 
                    active = False
                if active: 
                    color = color_active 
                else: 
                    color = color_passive 
                pygame.draw.rect(screen, (0,0,0), background_rect)
                pygame.draw.rect(screen, color, input_rect) 
                
                text_surface = base_font.render(user_text, True, (255, 255, 255)) 
                
                # render at position stated in arguments 
                screen.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
                pygame.display.flip()


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
                    
                # draw rectangle and argument passed which should be on screen
 
                pygame.draw.rect(screen, (0,0,0), background_rect)
                pygame.draw.rect(screen, color, input_rect) 
                
                text_surface = base_font.render(user_text, True, (255, 255, 255)) 
                
                # render at position stated in arguments 
                screen.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
                
                # set width of textfield so that text cannot get outside of user's text input 
                input_rect.w = max(180, text_surface.get_width()+10, input_rect.w) 
                if windowstate == windowtypes.lobby:
                    drawover_rect = pygame.Rect(display.current_w // 2 - 250, display.current_h // 2-400 , 500, 900)
                    pygame.draw.rect(screen, (255,25,255), drawover_rect)
                        
                
                pygame.display.flip()
                # clock.tick(60) means that for every second at most 
                # 60 frames should be passed. 
                clock.tick(60) 
