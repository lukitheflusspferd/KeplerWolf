import sys
import json
from time import sleep
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def computeCommand(cmd):
    """
    Verarbeitung des eingegebenen Commands

    Args:
        cmd (str): zu verarbeitender Command
    """
    match cmd:
        case "start game":
            return {
            "type": "ConsoleCommand",
            "data": "gameStart"
        }
        case _:
            print("Fehler: Unbekannter Befehl")
            return {
            "type": "EmptyConsolePing",
            "data": ""
        }
    

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

initMessage = {
    "type": "ConsoleInitPing",
    "data": "",
}

initMessage = json.dumps(initMessage).encode('utf-8')

s.send(initMessage)

temp = s.recv(1024)

try:
    while True:
        message = computeCommand(input(">>> "))

        message = json.dumps(message).encode('utf-8')
        s.send(message)
        
        answer = s.recv(1024)
        answer = json.loads(answer)
        # print("[{}] {}".format(ip, answer.decode()))
        if answer["type"] == "ConsoleError":
            print("Fehler:", answer["data"])
        
        sleep(1)
finally:
    print("Verbindung beendet")
    s.close()
