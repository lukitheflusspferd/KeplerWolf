from ClassPlayer import Player
import copy
import Ping
from Vote import Voting

clientPlayerData = None
playerData = None

mailbox = []
validName = False
errorName = ""

def getMailbox():
    return mailbox

def setMailbox(newMailbox):
    global mailbox
    mailbox = newMailbox

def computePing(message: dict, ownName):
    global mailbox
    
    messageType, messageData, _ = Ping.toData(message)
    # print("PingTyp:", messageType, "PingData:", messageData)
    
    if messageType == "InitPing":
        global clientPlayerData
        clientPlayerData = messageData

        print(clientPlayerData)
        print("")

    if messageType == "EmptyPing":
        pass

    if messageType == "VotePing":
        messageData = messageData
        voteType = messageData["type"]
        players = messageData["players"]

        vote = Voting(players, voteType, ownName)
        mailbox.append(vote)
        # print(mailbox)

    if messageType == "GameStartPing":
        global playerData
        spielerliste = messageData["players"]
        playerData = eval(messageData["data"])
        # playerData ist nun ein Objekt der Klasse Player
        
    #if messageType == "UsernameValidationPing":
    #    global validName
    #    validName = messageData["valid"]
    #
    #    global errorName
    #    errorName = messageData["error"]
    #    if errorName == "doppelt": 
    #        print("Dieser Name wird schon benutzt")
    #
    #    print(validName)
    #    print(errorName)
