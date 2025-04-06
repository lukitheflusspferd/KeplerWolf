from ClassPlayer import Player
from Roles import *

playerNamesPreGame = []

ipToPlayerID = dict()

ipToPlayerID["10.4.14.25"] = "luki"
ipToPlayerID["10.4.14.24"] = "p2"
ipToPlayerID["10.4.14.23"] = "p3"
# ipToPlayerID["192.168.2.160"] = "luki"

def resolveIPtoPlayerID(ip : str) -> str:
    return ipToPlayerID.get(ip)

playerDatabase = {
    # "p1" : Player("Spieler 1", "Villager()"),
    "p2" : Player("Spieler 2", "Villager()"),
    "p3" : Player("Spieler 3", "Villager()"),
    "luki" : Player("Lukas", "Witch(True)"),
}

def isPlayernameValid(playername : str):
    global playerNamesPreGame
    if playername in playerNamesPreGame:
        return (False, "doppelt")
    # TODO: check for politeness
    playerNamesPreGame.append(playername)
    print(f"Added Playername [{playername}] to the PreGameList of Players.\n ")
    return (True, "")
 

mailbox = {
    player : [] for player in playerDatabase
}

mailbox["luki"].append( {
     "type" : "InitPing",
     "data" : repr(playerDatabase["luki"])
} )

ServerState = "PreGame"

def computePlayernamePing(data):
    valid, errorMsg = isPlayernameValid(data)
    return {
        "type":"UsernameValidationPing",
        "data": {
            "valid": "True" if valid else "False",
            "error": repr(errorMsg)
        }
    }

def computePing(ip : str, data : dict) -> dict:
    playerID = resolveIPtoPlayerID(ip)
    # playerName = players[playerID].getname()

    match data['type']:
        case 'EmptyPing':
            pass
        case 'UsernamePing':
            if ServerState == 'PreGame':
                return computePlayernamePing(data["data"])
            else:
                raise Exception("Unknown ping Type from IP ["+ip+"]") 
        case _:
            raise Exception("Unknown ping Type from IP ["+ip+"]")
        
    if mailbox[playerID] != []:
            return mailbox[playerID].pop()
    else: 
        return {
            "type":"EmptyPing",
            "data":"",
        }
        