from ClassPlayer import Player

clientPlayerData = None

mailbox = ["mailboxtest"]

def computePing(message: dict):
    if message["type"] == "initPing":
        global clientPlayerData
        clientPlayerData = eval(message["data"])
        print(clientPlayerData)

    if message["type"] == "testPing":
        test = True

    if message["type"] == "emptyPing":
        pass

    if message["type"] == "setMode":
        msg = eval(message)
        type = msg["data"]["eventType"]
        data = msg["data"]["data"]

    if mailbox != "":
        return mailbox[0]

