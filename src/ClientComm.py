import json
from time import sleep
import socket

from ClientData import computePing, validName

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

connected = False

while not connected:
    """
    Solange keine Verbindung aufgebaut ist, wird immer wieder eine neue IP-Adresse vom Spieler abgefragt
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

'''
ip = "10.4.14.26"
# ip = "192.168.2.160"
'''

# Spielernamen abfragen solange der Server diesen noch nicht validiert hat (z.B. bei Dopplung eines Namens)
try:
    while not validName:
        message = {
            "type":"UsernamePing",
            "data": input('Bitte gib deinen Namen ein:')
        }

        b_message = json.dumps(message).encode('utf-8')
        s.send(b_message)
        print("Name an Server gesendet")

        b_answer = s.recv(1024)
        print("[{}] {}".format(ip, b_answer.decode("utf-8")))
        print("")
        answer = eval(b_answer.decode())

        validName = True     
finally:
    pass


try:
    while True:
        message = {
        "type":"EmptyPing",
        "data":"",
        }

        b_message = json.dumps(message).encode('utf-8')
        s.send(b_message)
        print("EmptyPing an Server gesendet!")

        b_answer = s.recv(1024)
        print("[{}] {}".format(ip, b_answer.decode()))
        print("")

        computePing(json.loads(b_answer))
        
        sleep(1)
finally:
    s.close()