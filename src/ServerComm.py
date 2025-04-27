import json
import os
import selectors
import socket
import time

# from ServerData import computePing, resolveIPtoPlayerID, getServerState
import ServerState
import IPencodedecode

# siehe https://openbook.rheinwerk-verlag.de/python/34_001.html

PORT = 65432


def startServer():
    print("Server wird gestartet...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", PORT))
    ip = socket.gethostbyname(socket.gethostname())
    print(f"Server listening on IP [{ip}] at port [{PORT}]")
    print("Lobbycode:", IPencodedecode.encodeIP(ip))
    server.setblocking(False)
    server.listen(1)

    global selector
    selector = selectors.DefaultSelector()
    selector.register(server, selectors.EVENT_READ, accept)


def accept(selector, sock):
    """
    Verbindungsanfrage akzeptieren
    """
    connection, addr = sock.accept()
    connection.setblocking(False)
    selector.register(connection, selectors.EVENT_READ, ping)


def ping(selector, client):
    """
    Ping von Client empfangen und beantworten
    """
    message = client.recv(1024)
    ip = client.getpeername()[0]
    # Wenn die Nachricht einen Inhalt hat
    if message:
        # if getServerState() == "PreGame":
        #     print("\nGot Ping from IP [{}] with the following data: \n {}".format(ip, message.decode()))
        # else:
        #     print("\nGot Ping from player with ID [{}] at IP [{}] with the following data: \n {}".format(resolveIPtoPlayerID(ip), ip, message.decode()))

        pingData = json.loads(message.decode())
        
        # answer = computePing(ip, pingData)
        answer = ServerState.computePing(ip, pingData)

        encodedPingBackMessage = json.dumps(answer).encode('utf-8')

        client.send(encodedPingBackMessage)
    else:
        print("+++ Verbindung zu {} beendet".format(ip))
        selector.unregister(client)
        client.close()


if __name__ == '__main__':
    startServer()
    while True:
        for key, mask in selector.select():
            key.data(selector, key.fileobj)