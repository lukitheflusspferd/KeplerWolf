import copy
import json
import socket
# from time import sleep

import Ping
from Rollenverteilung import assignRoles
from Roles import ROLES_LIST

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def computeCommand(cmd):
    """
    Verarbeitung des eingegebenen Commands

    Args:
        cmd (str): zu verarbeitender Command
    """
    match cmd:
        case "start game":
            return Ping.fromData("ConsoleCommandPing", "gameStartCMD")
        #    return {
        #    "type": "ConsoleCommandPing",
        #    "data": "gameStartCMD"
        #}
        case "trigger vote":
            return Ping.fromData("ConsoleCommandPing", "voteTrigger")
        #    return {
        #    "type": "ConsoleCommandPing",
        #    "data": "voteTrigger"
        #}
        case _:
            print("Fehler: Unbekannter Befehl")
            return Ping.fromData("EmptyPing", "")
            #return {
            #    "type": "EmptyPing",
            #    "data": ""
            #}
    
def computePing(data: dict):
    """
    Verarbeitung der Antwort des Servers

    Args:
        data (dict): zu verarbeitender Ping
    """
    
    pingType, pingData = Ping.toData(data)
    
    match pingType:
        case 'EmptyPing':
            pass
        case 'ConsoleError':
            print("Fehler:", pingData)
        case 'ConsoleGameInit':
            players = pingData
            print("Angemeldete Spieler:", players)
            print("Es gibt", len(players), """Spieler. Bitte gib für jede Rolle die Anzahl an Spielern an, welche diese Rolle bekommen sollen.
                  Die restlichen Spieler bekommen die Rolle "Dorfbewohner".\n""")
            
            roles = assignRoles(players, {
                'Werewolf': 2,
                'Witch': 1,
                'Seer': 0,
                'Hunter': 0,
                'Littlegirl': 0,
                'Alpha': 0,
                'Tree': 0
            })
            print("Rollenverteilung:", roles)
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

#initMessage = {
#    "type": "ConsoleInitPing",
#    "data": "",
#}

initMessage = json.dumps(Ping.fromData("ConsoleInitPing", "")).encode('utf-8')

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
