from ClassPlayer import Player
from Roles2 import *

ipToPlayerID = dict()

ipToPlayerID["10.4.14.25"] = "p1"
ipToPlayerID["10.4.14.24"] = "p2"
ipToPlayerID["10.4.14.23"] = "p3"

def resolveIPtoPlayerID(ip : str) -> str:
    return ipToPlayerID.get(ip)

players = {
    "p1" : Player("Spieler 1", villager()),
    "p2" : Player("Spieler 2", villager()),
    "p3" : Player("Spieler 3", villager()),
}

mailbox = {
    player : [] for player in players
}

mailbox["p2"].append( {
     "type" : "initPing",
     "data" : repr(players["p2"])
} )

# ServerState = "PrePlay"

def computePing(ip : str, data : dict) -> dict:
    playerID = resolveIPtoPlayerID(ip)
    # playerName = players[playerID].getname()

    match data['type']:
        case 'emptyPing':
            pass
        case _:
            raise Exception("Unknown ping Type from IP ["+ip+"]")
        
    if mailbox[playerID] != []:
            return mailbox[playerID].pop()
    else: 
        return {
            "type":"emptyPing",
            "data":"",
        }
        