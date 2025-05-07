from IPencodedecode import encodeIP, decodeIP
from ClassPlayer import Player
from ClassRole import Role
from Roles import *
from enum import Enum
from ClassButton import Button
import pygame
import pygame.freetype
from pygame.locals import *
import os
import math
import sys   
import socket
import json
from time import sleep
from ClientData import computePing, validName, getMailbox, setMailbox
from Ping import fromData, toData

class windowtypes(Enum):
    login = 1
    lobby = 2
    game = 3
    win = 4
    lose = 5

pygame.init() 
global answer 
global ownName
ownName = None
player = None
imagepositionsx= []
imagepositionsy= []
playerData = []
winnergroup = None


playerlist = []
alivelist = []
testplayer = Player("Test")
testplayerlist = ["p1","p2","p3","p4","p5","p6","p7","p8","p9","p10"]
testalivelist = [True, True, True, True, True, True, True, True, True, False]
testvoteoptionlist = ["p1","p2","p3","p4","p5","p6","p7","p8","p9","p10", True, False]

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
voteactive = False
fakevoteactive = False
witchvotephase = 1
ishosting = False
votetype = ""

# Definieren des Eingabefeldes
background_rect = pygame.Rect(195, 195, 110, 42)
input_rect = pygame.Rect(200, 200, 140, 32) 
color_active = pygame.Color('lightskyblue3')

# Definieren der Farbe des Eingabefeldes
color_passive = pygame.Color('chartreuse4') 
color = color_passive
istesting = False
active = False

buttonHideResultonscreen = False

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
            font = pygame.font.SysFont('comicsans', 80)
            text_surface = font.render("KeplerWolf", False, (0,0,0))
            text_rect = text_surface.get_rect(center=(display.current_w // 2, display.current_h // 6))
            screen.blit(text_surface, text_rect)
            font = pygame.font.SysFont('comicsans', 30)
            text_surface = font.render("Willst du einem Spiel beitreten oder selbst eins hosten?", False, (0,0,0))
            text_rect = text_surface.get_rect(center=(display.current_w // 2, display.current_h // 2 - 80))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            ButtonHost = Button((0, 255, 0), display.current_w // 2 + 25, display.current_h // 2 + 45, 110, 42, "Hosten")
            ButtonHost.draw(screen,"comicsans", outline=(0, 0, 0))
            ButtonJoin = Button((0, 255, 0), display.current_w // 2 - 135, display.current_h // 2 + 45, 110, 42, "Beitreten", 23)
            ButtonJoin.draw(screen,"comicsans", outline=(0, 0, 0))
            ButtonTest = Button((0, 255, 0), display.current_w // 2 - 135, display.current_h // 2 + 120, 110, 42, "Test")
            ButtonTest.draw(screen,"comicsans", outline=(0, 0, 0))
            ButtonTestWin = Button((0,255,0), display.current_w // 2 + 25, display.current_h // 2 + 120, 110, 42, "TestWin", 26)
            ButtonTestWin.draw(screen,"comicsans", outline=(0, 0, 0))
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
                    elif ButtonTestWin.isOver(event.pos):
                        istesting = True
                        filllogintext()
                        undecided = False
                        setstate(windowtypes.win)
        if not istesting:                

            drawover_rect = pygame.Rect(display.current_w // 2 - 500, display.current_h // 2-100 , 1000, 300)
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
        if istesting:
            displayrole()
            displayresults("test", "Vote")     #NUR ZUM   
            displayplayerpictures(testplayerlist, testalivelist)
            triggerfakevote() #TESTEN
        else:
            displayrole()
            displayplayerpictures(playerlist, alivelist)
    if state == windowtypes.win or windowstate == windowtypes.lose:
        screen.fill((255,255,255))
        font = pygame.font.SysFont('comicsans', 40)
        if state == windowtypes.lose:
            text = "Du hast verloren!"
        else:
            text = "Du hast gewonnen!"
        text_surface = font.render(text, False, (0,0,0))
        text_rect = text_surface.get_rect(center=(display.current_w // 2, display.current_h // 3))
        screen.blit(text_surface, text_rect)
        if istesting:
            winnergroup = grouptypes.werewolf
        if winnergroup == grouptypes.alpha:
            text = "Der Alpha-Werwolf hat gewonnen"
        elif winnergroup == grouptypes.werewolf:
            text = "Die Werwölfe haben gewonnen"
        #elif winnergroup == grouptypes.fluter: ist nicht implementiert als rolle
        elif winnergroup == grouptypes.villager:
            text = "Das Dorf hat gewonnen"
        elif winnergroup == grouptypes.lovers:
            text = "Die verliebten haben gewonnen"        
        font = pygame.font.SysFont("comicsans", 20)
        text_surface = font.render(text, False, (0,0,0))
        text_rect = text_surface.get_rect(center=(display.current_w//2, display.current_h // 3 + 60))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        if istesting:
            displayallroles(playerlist)
        else:
            displayallroles(endplayerlist)

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
    übermalt die Login anzeigen um Platz für neuen Text zu machen
    """
    fill_rect1 = pygame.Rect(display.current_w // 2 - 1100, 0 , 2200, display.current_h // 2+90)
    fill_rect2 = pygame.Rect(display.current_w // 2 - 1100, display.current_h // 2 + 100, 2200, 120)
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
    """
    Zeigt die aktuelle Spielerliste in der Lobby an
    """
    if data != []:
        global playerlist, alivelist, istesting
        drawover_rect = pygame.Rect(0, 0, display.current_w//4-10 , display.current_h)
        pygame.draw.rect(screen, (255,255,255), drawover_rect)
        print("übergemalt")
        pygame.display.flip()
        font = pygame.font.SysFont('comicsans', 40)
        text_surface = font.render("Spieler", False, (0,0,0))
        text_rect = text_surface.get_rect(center=(display.current_w // 8, 100))
        screen.blit(text_surface, text_rect)
        font = pygame.font.SysFont('comicsans', 20)
        temp = []
        print("HHHHHHHHAAAAAAAAAHHH" + str(data))
        for i in data:
            text_surface = font.render(i, False, (0,0,0))
            text_rect = text_surface.get_rect(center=(display.current_w // 8, 150 + data.index(i) * 30))
            screen.blit(text_surface, text_rect)
            temp.append(i)
            print("name gemacht und so")
        pygame.display.flip()
        playerlist = temp
        temp = []
        for i in playerlist:
            temp.append(True)
        alivelist = temp


def hiderole():
    """
    übermalt die eigene Rolle um sie zu verstecken, zeigt "Rolle anzeigen" Button an
    """
    print("Hide Role")
    drawover_rect = pygame.Rect(0,0, display.current_w//6, display.current_h)
    pygame.draw.rect(screen, (255,255,255), drawover_rect)
    global ButtonHideRoleonscreen, ButtonShowRoleonscreen
    ButtonHideRoleonscreen = False
    ButtonShowRoleonscreen = True
    ButtonShowRole.draw(screen,"comic-sans", outline=(0,0,0))
    pygame.display.flip()

def showrole():
    """
    ruft die Funktion auf um die Rolle anzuzeigen, zeigt "Rolle verstecken" Button an
    """
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
    """
    zeigt die Rolle des Spielers an
    """
    global playerData
    font = pygame.font.SysFont('sans-serif', 20)
    print(playerData)
    print(type(playerData))
    role = playerData.getrole()
    font = pygame.font.SysFont('comicsans', 25)
    text_surface = font.render("Rolle:", False, (0,0,0))
    text_rect = text_surface.get_rect(center=(display.current_w // 12, 150))
    screen.blit(text_surface, text_rect)
    text_surface = font.render(role.getname() , False, (0,0,0))
    text_rect = text_surface.get_rect(center=(display.current_w // 12, 180))
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
        text_rect = text_surface.get_rect(center=(display.current_w // 12, 230 + temp2.index(i)*25))
        screen.blit(text_surface, text_rect) 
    pygame.display.flip()

def statechange(data):
    """
    verändert die Spielerdaten, leitet Todesnachricht ein
    """
    data = eval(data)
    global playerData
    if not playerData.getisdead() and data.getisdead():
        pass #TODESSCREEN EINFÜGEN SO EINE MESSAGE OBEN DAS MAN TOT IST
    playerData = data

def triggervote(data):
    """
    stellt Text für die Abstimmung zusammen, leitet Abstimmung ein
    """
    global voteactive, voteoptionlist, witchvotephase, votetype
    voteactive = True
    votetype = data["type"]
    playerlist = data["players"]
    playerlisttext = ""
    if len(playerlist) != 1:
        for i in data["players"]:
            if data["players"].index(i) != len(data["players"]) - 1:
                playerlisttext += i + ", "
            else:
                playerlisttext += i + "."
    else:
        playerlisttext = data["players"][0]
    if data["type"] == "witch_heal" or data["type"] == "witch_kill":
        if witchvotephase == 1:
            voteoptionlist = ["Ja", "Nein"]
            if data["type"] == "witch_heal":
                displayrequesttext("Willst du das Opfer, " + playerlisttext + " heilen? (Ja/Nein)")
            elif data["type"] == "witch_kill":
                displayrequesttext("Willst du einen Spieler Töten? (Ja/Nein)")
        elif witchvotephase == 2:
            voteoptionlist = data["players"]
    else: 
        voteoptionlist = data["players"]
        if data["type"] == "love1":
            displayrequesttext("Schreibe den Namen eines Spielers, den du verlieben willst: " + playerlisttext)
        elif data["type"] == "love2":
            displayrequesttext("Schreibe einen weiteren Namen eines Spielers, den du verlieben willst: " + playerlisttext)
        elif data["type"] == "see":
            displayrequesttext("Schreibe den Namen des Spielers, wessen Rolle du sehen willst: " + playerlisttext)
        elif data["type"] == "hunter":
            displayrequesttext("Schreibe den Namen des Spielers, den du mit in den Tod nehmen willst: " + playerlisttext)
        elif data["type"] == "werewolf":
            displayrequesttext("Schreibe den Namen des Spielers, den du töten willst: " + playerlisttext)
        elif data["type"] == "alpha":
            displayrequesttext("Schreibe den Namen des Spielers, den du als Alpha töten willst: " + playerlisttext)
        elif data["type"] == "nominate_mayor":
            displayrequesttext("Schreibe den Namen des Spielers, den du als Bürgermeister nominieren willst: " + playerlisttext)
        elif data["type"] == "mayor":
            displayrequesttext("Schreibe den Namen des Spielers, den du zum Bürgermeister wählen willst: " + playerlisttext)
        elif data["type"] == "nominate_hanging":
            displayrequesttext("Schreibe den Namen des Spielers, den du zum erhängen nominieren willst: " + playerlisttext)
        elif data["type"] == "hanging":
            displayrequesttext("Schreibe den Namen des Spielers, den du erhängen willst: " + playerlisttext)

def triggerfakevote():
    """
    stellt Text für die Fake Abstimmung zusammen, leitet Fake Abstimmung ein, genutzt um Rollen nicht vom tippen aus zu hören
    """
    global fakevoteactive, playerlist, testplayerlist
    temp = ""
    fakevoteactive = True
    if not istesting:
        playerlist1 = playerlist
    else:
        playerlist1 = testplayerlist
    for i in playerlist1:
        if playerlist1.index(i) != len(playerlist1) - 1:
            temp += i + ", "
        else:
            temp += i + "."
    text = "Schreibe einen der Spielernamen in das Textfeld: " + temp
    displayrequesttext(text)

def displayrequesttext(text, error = False):
    """
    zeigt die Abstimmungsinformationen an
    """
    fillrequesttext()
    font = pygame.font.SysFont('comicsans', 20)
    chars = list(text)
    temp1 = []
    temp2 = []
    temp3 = ""
    j = 0
    for i in chars:
        temp1.append(i)
        j += 1
        if j >= 17:
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
    if error:
        for i in temp2:            
            text_surface = font.render(i, False, (255,0,0))
            text_rect = text_surface.get_rect(center=(display.current_w // 12 * 11, display.current_h// 8 * 6.5 - len(temp2)*25 + temp2.index(i)*25))
            screen.blit(text_surface, text_rect)
    else:
        for i in temp2:            
            text_surface = font.render(i, False, (0,0,0))
            text_rect = text_surface.get_rect(center=(display.current_w // 12 * 11, display.current_h// 8 * 6.5 - len(temp2)*25 - 4*25 + temp2.index(i)*25))
            screen.blit(text_surface, text_rect) 
    pygame.display.flip()

def displaywronganswer():
    """
    stellt Fehlermeldung zusammen, wenn die Antwort nicht richtig ist
    """
    text = "Die Antwort wurde nicht erkannt, gebe etwas anderes ein."
    displayrequesttext(text, True)
    
def fillrequesttext():
    """
    übermalt die Abstimmungsinformationen um Platz für neuen Text zu machen oder das Ende einer Abstimmung zu signalisieren
    """
    drawover_rect = pygame.Rect(display.current_w // 6 * 5 + 10, display.current_h//2 , display.current_w//6-10, display.current_h//8*3.25-102)
    pygame.draw.rect(screen, (255,255,255), drawover_rect)
    pygame.display.flip()

def displayresults(data, resulttype):
    """
    zeigt die Ergebnisse einer Abstimmung oder einer Tötung an
    """
    global buttonHideResultonscreen, ButtonHideResult, alivelist, playerlist
    hideresults()
    ButtonHideResult = Button((0, 255, 0), display.current_w //6*5 +25, 50, display.current_w//6-50, 42, "Ergebnis verstecken", 21)
    ButtonHideResult.draw(screen,"comicsans", outline=(0, 0, 0))
    print("HHHHHHHHHHHHHHHHHH")
    buttonHideResultonscreen = True
    if not istesting:
        if resulttype == "Vote":
            votetype = data["type"]
        elif resulttype == "Elimination":
            deathtype = data["type"]
        playerlist1 = data["names"]
    else:
        votetype = "love"
        playerlist1 = testplayerlist
    if resulttype == "See" or resulttype == "Elimination":
        seerole = eval(data["role"])
        role = seerole.getname()
    text = ""
    amount = len(playerlist1)
    if resulttype == "Vote":
        if votetype == "witch_kill":
            text = "Du hast " + playerlist1[0] + " getötet."
        elif votetype == "witch_heal":
            text = "Du hast " + playerlist1[0] + " geheilt."
        elif votetype == "werewolf":
            text = "Die Werwölfe haben " + playerlist1[0] + " getötet."
        elif votetype == "alpha":
            text = "Du als Alpha hast " + playerlist1[0] + " getötet."
        elif votetype == "love":
            text = "Du hast " + playerlist1[0] + " und " + playerlist1[1] + " verliebt."
        elif votetype == "nominate_mayor":
            text = "Diese Spieler wurden zum Bürgermeister nominiert:"
            for i in range(amount): 
                if i != amount:
                    text += playerlist1[i-1] +", "
                else: 
                    text += playerlist[i-1] + "."
        elif votetype == "mayor":
            text = playerlist1[0] + " wurde zum Bürgermeister gewählt."
        elif votetype == "nominate_hanging":
            text = "Diese Spieler wurden zum erhängen nominiert:"
            for i in range(amount): 
                if i != amount:
                    text += playerlist1[i-1] +", "
                else: 
                    text += playerlist[i-1] + "."
    if resulttype == "See":
        if votetype == "see":
            text = "Du hast die Rolle von " + playerlist1[0] + " gesehen. " + playerlist1[0] + " hatte die Rolle " + role + "."
        
    if resulttype == "Elimination":
        if deathtype == "night":
            text = playerlist1[0] + " wurde in der Nacht getötet. " + playerlist1[0] + " hatte die Rolle " + role + "."
        elif deathtype == "hanging":
            text = playerlist1[0] + " wurde erhängt. " + playerlist1[0] + " hatte die Rolle " + role + "."
        elif deathtype == "hunter":
            text = playerlist1[0] + " wurde vom Jäger mit in den Tod genommen. " + playerlist1[0] + " hatte die Rolle " + role + "."
        alivelist[playerlist.index(playerlist1[0])] = False
        displayplayerpictures(playerlist, alivelist)
    if text != "":
        
        textlist = list(text)
        temp1 = []
        temp2 = []
        temp3 = ""
        j = 0
        for i in textlist:
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
        font = pygame.font.SysFont('comicsans', 25)
        text_surface = font.render("Ergebnis:", False, (0,0,0))
        text_rect = text_surface.get_rect(center=(display.current_w // 12 * 11, 190))
        screen.blit(text_surface, text_rect)
        font = pygame.font.SysFont('comicsans', 20)
        for i in temp2:            
            text_surface = font.render(i, False, (0,0,0))
            text_rect = text_surface.get_rect(center=(display.current_w // 12*11, 230 + temp2.index(i)*25))
            screen.blit(text_surface, text_rect) 
    pygame.display.flip()

def hideresults():
    """
    übermalt die Ergebnisse um Platz für neuen Text zu machen
    """
    global buttonHideResultonscreen
    drawover_rect = pygame.Rect(display.current_w//6*5+10,0, display.current_w//6-10, display.current_h//2)
    pygame.draw.rect(screen, (255,255,255), drawover_rect)
    buttonHideResultonscreen = False
    pygame.display.flip()

def displaypicture(x, y, image):
    """
    zeigt ein Bild an
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir,"..", "assets\\")
    image = pygame.image.load(image_path + image)
    #image = pygame.image.load(image)
    image = pygame.transform.scale(image,(100, 100))
    screen.blit(image, (x-50, y-50))
    pygame.display.flip()

def calculateimagepositions(playerlist):
    global imagepositionsx, imagepositionsy
    imagepositionsx = []
    imagepositionsy = []
    amount = len(playerlist)
    for i in range(amount):
        angle = 2 * math.pi * i / amount  
        x = display.current_w // 2 + 275 * math.cos(-angle)  
        y = display.current_h // 2 + 275 * math.sin(-angle)  
        imagepositionsx.append(x)
        imagepositionsy.append(y)
    return imagepositionsx, imagepositionsy

def displayplayerpictures(playerlist, alivelist):
    imagepositionsx, imagepositionsy = calculateimagepositions(playerlist)
    for i in range(len(playerlist)):
        print(imagepositionsx[i], imagepositionsy[i])
        if alivelist[i]:
            displaypicture(imagepositionsx[i],imagepositionsy[i], "Player1.png")
        else:
            displaypicture(imagepositionsx[i],imagepositionsy[i], "Player1dead.png")
        print(playerlist)
        print(playerlist[i])
        text = playerlist[i]
        font = pygame.font.SysFont('comicsans', 20)
        text_surface = font.render(text, False, (0,0,0))
        text_rect = text_surface.get_rect(center=(imagepositionsx[i], imagepositionsy[i]+70))
        screen.blit(text_surface, text_rect)

def displayallroles(endplayerlist):
    global istesting
    
    if istesting:
        endplayerlist = ["p1","p2","p3","p4","p5","p6","p7","p8","p9","p10"]
        endrolelist = ["Werwolf","Werwolf","Werwolf","Armor","Blinzelmädchen","Dorfbewohner","Alphawolf","Jäger","Dorfbewohner", "Hexe"]
    for i in range(len(endplayerlist)):
        if istesting:
            text = endplayerlist[i] +" Rolle:"+ endrolelist[i]
        else:
            text = endplayerlist[i]["name"] +" Rolle:"+ endplayerlist[i]["role"]
        font = pygame.font.SysFont('comicsans', 20)
        text_surface = font.render(text, False, (0,0,0))
        text_rect = text_surface.get_rect(center=(display.current_w//2, display.current_h//2+25 * i))
        screen.blit(text_surface, text_rect)
    text = "Spieler:"
    text_surface = font.render(text, False, (0,0,0))
    text_rect = text_surface.get_rect(center=(display.current_w//2, display.current_h//2-25))
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
ButtonShowRole = Button((0,255,0), 25, 50, display.current_w//6-50, 42, "Rolle anzeigen", 25 )
ButtonHideRoleonscreen = False
ButtonShowRoleonscreen = False

setstate(windowtypes.login)
while True: 
    
    message = fromData("EmptyPing", "", ownName)

    if ipconfirmed:
        global mailbox
        mailbox = getMailbox()

        if mailbox != []:
            b_mailbox = json.dumps(mailbox.pop(0)).encode('utf-8')
            s.send(b_mailbox)
            #mailbox.pop(0)
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
        # computePing(json.loads(b_answer.decode("utf-8")), ownName)
        if windowstate == windowtypes.lobby:
            pingtype, pingData, _ = toData(answer)
            if pingtype == "NewLobbyPing":
                updatePlayerList(pingData)
        pingtype, data, _ = toData(answer)
        if pingtype == "GameStartPing":
            playerData = eval(data["data"])
            setstate(windowtypes.game)
        if pingtype == "StateChangePing":
            statechange(data)
        if pingtype == "VotePing":
            if data["dummy"] == "False":
                triggervote(data)
            elif data["dummy"] == "True":
                triggerfakevote()
            
        if pingtype == "VoteResultPing":
            displayresults(data, "Vote")
        if pingtype == "GameEndPing":
            winnergroup = data["group"]
            endplayerlist = data["players"]
            if winnergroup == endplayerlist[playerData.getname()["won"]]:
                setstate(windowtypes.win)
            else:
                setstate(windowtypes.lose)
        if pingtype == "EliminationPing":
            displayresults(data, "Elimination")
        if pingtype == "RevealRolePing":
            displayresults(data, "See")


        sleep(1)
    for event in pygame.event.get(): 
  
      # Beendet vor dem Schließen des Fensters die Programme und ggf. die Verbindung mit dem Server 
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
                        print(event)
                        
                elif ButtonShowRoleonscreen:
                    if ButtonShowRole.isOver(event.pos):
                        showrole()

                if buttonHideResultonscreen:
                    if ButtonHideResult.isOver(event.pos):
                        hideresults()
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
                
                screen.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
                pygame.display.flip()


        if event.type == pygame.KEYDOWN: 
            if active:
                # prüft ob die Backspace-Taste gedrückt wird 
                if event.key == pygame.K_BACKSPACE:  
                    user_text = user_text[:-1] 
                elif event.key != pygame.K_RETURN: 
                    user_text += event.unicode
                # gibt usertext aus wenn die Enter-Taste gedrückt wird               
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
                            user_text = ""
                    elif windowstate == windowtypes.game:
                        pass
                    if fakevoteactive:
                        if not istesting:
                            playerlist1 = playerlist
                        else:
                            playerlist1 = testplayerlist
                        if user_text in playerlist1:
                            message = fromData("VoteAnswerPing", "", ownName)
                            mailbox.append(message)
                            fakevoteactive = False
                            fillrequesttext()
                            message = fromData("EmptyPing", "", ownName)
                            user_text = ""
                        else:
                            displaywronganswer()
                    if voteactive:
                        if not istesting:
                            optionlist = voteoptionlist
                        else:
                            optionlist = testvoteoptionlist
                        if user_text in optionlist:
                            if witchvotephase == 1 and votetype == "witch_kill" and user_text == "Ja":
                                witchvotephase = 2
                                user_text = ""
                            elif witchvotephase == 1 and votetype == "witch_kill" and user_text == "Nein":
                                message = fromData("VoteAnswerPing", user_text, ownName)
                                mailbox.append(message)
                                voteactive = False    
                                fillrequesttext()
                                message = fromData("EmptyPing", "", ownName)
                                user_text = ""
                            else:      
                                message = fromData("VoteAnswerPing", user_text, ownName)
                                mailbox.append(message)
                                voteactive = False
                                fillrequesttext()
                                message = fromData("EmptyPing", "", ownName)
                                user_text = ""
                        else:
                            displaywronganswer()
                    
                pygame.draw.rect(screen, (0,0,0), background_rect)
                pygame.draw.rect(screen, color, input_rect) 
                
                text_surface = base_font.render(user_text, True, (255, 255, 255)) 
                
                screen.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
                
                # passt die Breite des Textfeldes an, damit der Text nicht über das Eingabefeld hinausgehen kann
                input_rect.w = max(180, text_surface.get_width()+28, input_rect.w) 
                background_rect.w = max(190, text_surface.get_width()+38, background_rect.w)
                if windowstate == windowtypes.lobby or windowstate == windowtypes.game:
                    drawover_rect = pygame.Rect(display.current_w // 2 - 250, display.current_h // 2-400 , 500, 900)
                    pygame.draw.rect(screen, (255,255,255), drawover_rect)
                        
                
                pygame.display.flip()
                # Begrenzung auf 60 FPS
                clock.tick(60) 
