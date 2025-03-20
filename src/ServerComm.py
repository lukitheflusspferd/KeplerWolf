import json
import selectors
import socket
import time

from ServerData import computePing

# siehe https://openbook.rheinwerk-verlag.de/python/34_001.html

PORT = 65432


def startServer():
    print("Starting server...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", PORT))
    print("Server listening at port", PORT)
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
    print(connection)
    selector.register(connection, selectors.EVENT_READ, ping)

def message_legacy(selector, client):
    """
    Ping von Client empfangen und beantworten
    """
    nachricht = client.recv(1024)
    ip = client.getpeername()[0]
    if nachricht:
        print("[{}] {}".format(ip, nachricht.decode()))
        client.send(nachricht)
    else:
        print("+++ Verbindung zu {} beendet".format(ip))
        selector.unregister(client)
        client.close()

def ping(selector, client):
    """
    Ping von Client empfangen und beantworten
    """
    message = client.recv(1024)
    ip = client.getpeername()[0]
    # Wenn die Nachricht einen Inhalt hat
    if message:
        print("\nGot Ping from IP [{}] with the following data: \n {}".format(ip, message.decode()))
        pingData = json.loads(message)
        
        answer = computePing(ip, pingData)

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