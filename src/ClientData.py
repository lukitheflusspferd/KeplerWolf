from ClassPlayer import Player
from Vote import Voting

clientPlayerData = None

mailbox = []
validName = False
errorName = ""

def getMailbox():
    return mailbox

def setMailbox(newMailbox):
    global mailbox
    mailbox = newMailbox

def computePing(message: dict):
    if message["type"] == "InitPing":
        global clientPlayerData
        clientPlayerData = eval(message["data"])

        print(clientPlayerData)
        print("")

    if message["type"] == "TestPing":
        test = True

    if message["type"] == "EmptyPing":
        pass

    if message["type"] == "SetMode":
        type = eval(message["data"]["eventType"])
        data = eval(message["data"]["data"])
        # hier später pygame Funktion aufrufen

    if message["type"] == "VotePing":
        messageData = eval(message["data"])
        voteType = messageData["type"]
        players = messageData["players"]

        vote = Voting(players, voteType)
        mailbox.append(vote)
        print(mailbox)

    if message["type"] == "DeathPing":
        username = eval(message["data"]["username"])
        role =  eval(message["data"]["role"])
        # hier später pygame Funktion aufrufen
        
    if message["type"] == "UsernameValidationPing":
        global validName
        validName = eval(message["data"]["valid"])

        global errorName
        errorName = eval(message["data"]["error"])
        if errorName == "doppelt": 
            print("Dieser Name wird schon benutzt")

        print(validName)
        print(errorName)