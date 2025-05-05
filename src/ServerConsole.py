import atexit
import copy
import json
import socket
# from time import sleep

import Ping
import Rollenverteilung

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def onClose():
    global s
    s.close()
    print("Verbindung beendent")

atexit.register(onClose)


def computeCommand(cmd):
    """
    Verarbeitung des eingegebenen Commands

    Args:
        cmd (str): zu verarbeitender Command
    """
    match cmd:
        case "start game":
            return Ping.fromData("ConsoleCommandPing", "gameStartCMD", "console")
        case "trigger vote":
            return Ping.fromData("ConsoleCommandPing", "voteTrigger", "console")
        case "trigger vote 2":
            return Ping.fromData("ConsoleCommandPing", "voteTrigger2", "console")
        case _:
            print("Fehler: Unbekannter Befehl")
            return Ping.fromData("EmptyPing", "", "console")

def computePing(data: dict):
    """
    Verarbeitung der Antwort des Servers

    Args:
        data (dict): zu verarbeitender Ping
    """
    
    pingType, pingData, _ = Ping.toData(data)
    
    match pingType:
        case 'EmptyPing':
            pass
        case 'ConsoleError':
            print("Fehler:", pingData)
        case 'ConsoleGameInit':
            return Rollenverteilung.getRolesCount(pingData)
            
        case _:
            print("Fehler: Unbekannter Ping-Typ:", pingType)

    return None

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

connected = False

while not connected:
    """
    Solange keine Verbindung aufgebaut ist, wird immer wieder eine neue IP-Adresse abgefragt
    """
    ip = input("Bitte die IP-Adresse des Servers eingeben:\n")
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

initMessage = json.dumps(Ping.fromData("ConsoleInitPing", "", "console")).encode('utf-8')

s.send(initMessage)

temp = s.recv(1024)

messageOverride = None

try:
    while True:
        if messageOverride == None:
            # Wenn es keine zu versendende Nachricht gibt, wird ein neuer Befehl abgefragt
            message = computeCommand(input(">>> "))
        else: 
            message = copy.deepcopy(messageOverride)
        message = json.dumps(message).encode('utf-8')
        s.send(message)
        
        answer = s.recv(1024)
        answer = json.loads(answer)
        
        messageOverride = computePing(answer)
        
finally:
    print("Verbindung beendet")
    s.close()
