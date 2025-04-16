from ClassPlayer import Player
from Roles import *

EMPTYPING = {
    "type": "EmptyPing",
    "data": "",
}

playerNamesPreGame = []

ipToPlayerID = dict()

"""
ipToPlayerID["10.4.14.25"] = "luki"
ipToPlayerID["10.4.14.24"] = "p2"
ipToPlayerID["10.4.14.23"] = "p3"
# ipToPlayerID["192.168.2.160"] = "luki"
"""
def resolveIPtoPlayerID(ip : str) -> str:
    return ipToPlayerID.get(ip)

playerDatabase = {
    # "p1" : Player("Spieler 1", "Villager()"),
    "p2" : Player("Spieler 2", "Villager()"),
    "p3" : Player("Spieler 3", "Villager()"),
    "luki" : Player("Lukas", "Witch(True)"),
}

def isPlayernameValid(ip, playername : str):
    global playerNamesPreGame
    if playername in playerNamesPreGame:
        return (False, "doppelt")
    # TODO: check for politeness
    playerNamesPreGame.append(playername)
    print(f"Added Playername [{playername}] to the PreGameList of Players.\n ")
    ipToPlayerID[ip] = playername
    mailbox[playername] = []
    return (True, "")
 
"""
mailbox = {
    player : [] for player in playerDatabase
}"""
mailbox = dict()

mailbox["console"] = []

"""
mailbox["luki"].append( {
     "type" : "InitPing",
     "data" : repr(playerDatabase["luki"])
} )
"""

ServerState = "PreGame"

def getServerState():
    global ServerState
    return ServerState


def computePlayernamePing(ip, data):
    valid, errorMsg = isPlayernameValid(ip, data)
    return {
        "type":"UsernameValidationPing",
        "data": {
            "valid": "True" if valid else "False",
            "error": repr(errorMsg)
        }
    }

def computeCommand(cmd):
    """
    Verarbeiten eines Konsolenbefehls

    Args:
        cmd (str): Einheitlicher Befehlstyp
    """
    global ServerState
    
    match cmd:
        case "gameStartCMD":
            if ServerState != "PreGame":
                return {
                    "type": "ConsoleError",
                    "data": "Das Spiel ist bereits gestartet.",
                }
            ServerState = "Initializing"
            print("Changed SterverState to [Initializing].")
            print(f"Initializing the game with the following players: {str(playerNamesPreGame)} ...")
            return {
                "type": "consoleGameInit",
                "data": repr(playerNamesPreGame),
            }

        case "voteTrigger":
            vote = dict()
            vote["type"] = "mayor"
            vote["players"] = playerNamesPreGame
            for player in mailbox.keys():
                if player == "console": continue
                mailbox[player].append({
                        "type": "VotePing",
                        "data": repr(vote),
                    })
            # print(mailbox)
    return EMPTYPING

def computePing(ip : str, data : dict) -> dict:
    playerID = resolveIPtoPlayerID(ip)
    # playerName = players[playerID].getname()

    match data['type']:
        case 'EmptyPing':
            pass
        case 'EmptyConsolePing':
            pass
        case 'ConsoleInitPing':
            ipToPlayerID[ip] = "console"
            playerID = "console"
            print("Console connected!")
        case 'ConsoleCommand':
            cmd = data['data']
            return computeCommand(cmd)
        case 'UsernamePing':
            if ServerState == 'PreGame':
                return computePlayernamePing(ip, data["data"])
            else:
                # TODO: Dem Spieler die aktuellen Daten senden, da davon auzugehen ist, dass er dem Spiel gerejoined ist
                raise Exception(f"Got [UsernamePing] from IP [{ip}], but the game has already been started.") 
        case _:
            raise Exception("Unknown ping Type from IP ["+ip+"]")
        
    if mailbox.get(playerID):
        return mailbox[playerID].pop()
    else: 
        return EMPTYPING
        