import Ping

#class ServerSubState():
#    def __init__(self, onEnter, onPing, onFinish):
#        self.__onEnter = onEnter
#        self.__onPing = onPing

import ClassPlayer
import Roles
import ClassPlayer

EMPTYPING = Ping.fromData("EmptyPing", "", "server")

class ServerGame():
    def __init__(self):
        self.__playerNamesPreGame = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10"]
        self.__consoleIP = None
        self.__mailbox = dict()
        
        self.__mailbox["console"] = []

        # Für Tests alle vorgegebenen Spieler der Mailbox hinzufügen
        for name in self.__playerNamesPreGame: self.__mailbox[name] = []
        
        self.__serverState = "PreGame"

        self.__rolesToPlayernames = dict()
        for role in Roles.SPECIAL_ROLES_LIST:
            self.__rolesToPlayernames[role.getId()] = []
        self.__rolesToPlayernames["villager"] = []

        self.__playerDataBase = dict()
        
        self.__computeVote = None
        self.__checkForVoteEnd = None
        self.__countVotings = None
        self.__votings = dict()
    
    
    ### Verwaltung von Spielernamen ###
    
    def __isPlayernameValid(self, ip : str, playername : str):
        """
        Prüft, ob ein Spielername bereits vorhanden ist

        Args:
            ip (str): Ip-Adresse der Anfrage
            playername (str): ângefragter Name

        Returns:
            tuple: (bool valide, Fehlernachricht)
        """
        if playername in self.__playerNamesPreGame:
            return (False, "doppelt")
        # TODO: check for politeness
        self.__playerNamesPreGame.append(playername)
        print(f"Spieler mit dem Namen [{playername}] zur Liste der Spielernamen vor dem Spiel hinzugefügt.\n ")
        self.__mailbox[playername] = []
        
        self.__broadcastPing(Ping.fromData("NewLobbyPing", self.__playerNamesPreGame, "server"), [])
        
        return (True, "")
    
    
    ### Verarbeitung von Pings ###
    
    def __computeCommand(self, cmd: str):
        """
        Verarbeitung eines Konsolenbefehls

        Args:
            cmd (str): Einheitlicher Befehlstyp
        """

        match cmd:
            case "gameStartCMD":
                if self.__serverState != "PreGame":
                    return Ping.fromData("ConsoleError", "Das Spiel ist bereits gestartet.", "server")
                
                self.__serverState = "GameInit"
                print("Neuer Serverzustand: [GameInit].")
                print(f"Initialisierung des Spiels mit den folgenden Spielern: {str(self.__playerNamesPreGame)} ...")
                return Ping.fromData("ConsoleGameInit", self.__playerNamesPreGame, "server")
            
            case "voteTrigger":
                vote = dict()
                vote["type"] = "mayor"
                vote["players"] = self.__playerNamesPreGame
                self.__broadcastPing(Ping.fromData("VotePing", vote, "server"), [])
                    
        return EMPTYPING
    
    def __computePlayernamePing(self, ip: str, name: str) -> dict:
        """
        Prüft von Spielern angefragte Namen und generiert den Antwortping

        Args:
            ip (str): Quell-IP der Anfrage
            name (str): angefragter Name

        Returns:
            dict: Antwortping
        """
        
        valid, errorMsg = self.__isPlayernameValid(ip, name)
        data = {
                "valid": "True" if valid else "False",
                "error": errorMsg
            }
        return Ping.fromData("UsernameValidationPing", data, "server")
    
    def computePing(self, ip : str, data : dict) -> dict:
        """
        Verarbeitung des empfangenen Pings

        Args:
            ip (str): Quell-IP des Pings
            data (dict): Inhalt des Pings

        Returns:
            dict: neuer Ping
        """
        pingType, pingData, playerID = Ping.toData(data)
        
        if self.__serverState == "PreGame":
            print("\nPing von IP [{}] mit dem folgenden Inhalt empfangen: \n {}".format(ip, data))
        else:
            print("\nPing von Spieler [{}] an IP [{}] mit dem folgenden Inhalt empfangen: \n {}".format(playerID, ip, data))

        match pingType:
            case 'EmptyPing':
                pass
            case 'ConsoleInitPing':
                # Wenn noch keine Konsole verbunden ist oder von der gleichen IP eine neue Konsole verbunden wird
                if self.__consoleIP == None or self.__consoleIP == ip:
                    self.__consoleIP = ip
                    print(f"Konsole an IP [{ip}] verbunden!")
                else:
                    print(f"Versuch von IP [{ip}], eine Konsole zu verbinden. Abgelehnt, da bereits eine Konsole von einer anderen IP verbunden ist.")
                    return Ping.fromData("ConsoleError", "Zugriff auf den Server verweigert, da bereits eine andere Konsole auf einem anderen Computer mit dem Server verbunden ist. ", "server")
            case 'ConsoleCommandPing':
                return self.__computeCommand(pingData)
            case 'UsernamePing':
                if self.__serverState == 'PreGame':
                    return self.__computePlayernamePing(ip, pingData)
                else:
                    # TODO: Dem Spieler die aktuellen Daten senden, da davon auzugehen ist, dass er dem Spiel gerejoined ist
                    print(f"Anmeldeversuch von IP [{ip}] fehlgeschlagen. Das Spiel wurde bereits gestartet.")
                    return Ping.fromData("UsernameValidationPing", {"valid": False, "error" : "bereits gestartet"}, "server")
            case 'LeaveLobbyPing':
                if self.__serverState == 'PreGame' and playerID != None:
                    self.__playerNamesPreGame.remove(playerID)
                    self.__broadcastPing(Ping.fromData("NewLobbyPing", self.__playerNamesPreGame, "server"), [])
                    return EMPTYPING
            case 'ConsoleGameInit':
                for playerName, roleId in pingData.items():
                    self.__rolesToPlayernames[roleId].append(playerName)
                    match roleId:
                        case "armor": role = Roles.Armor()
                        case "seer": role = Roles.Seer()
                        case "littlegirl": role = Roles.Littlegirl()
                        case "hunter": role = Roles.Hunter()
                        case "tree": role = Roles.Tree()
                        case "alpha": role = Roles.Alpha()
                        case "werewolf": role = Roles.Werewolf()
                        case "villager": role = Roles.Villager()
                        case "witch": role = Roles.Witch()
                        case _: 
                            raise Exception("Dieser Fehler sollte nicht passieren können.")
                    self.__playerDataBase[playerName] = ClassPlayer.Player(playerName, repr(role))
                    ping = Ping.fromData("GameStartPing", {"data": repr(self.__playerDataBase[playerName]), "players": list(pingData.keys())}, "server")
                    self.__mailbox[playerName].append(ping)
                    

                print("Datenbank initialisiert. Spiel gestartet.")
                print(self.__mailbox)
                self.__serverState = "Game"
            case _:
                print(f"Ping von {playerID} übersprungen da Typ unbekannt: {pingType}")
                # raise Exception("Unknown ping Type from IP ["+ip+"]")

        if self.__mailbox.get(playerID):
            return self.__mailbox[playerID].pop()
        else: 
            return EMPTYPING
    
    def __broadcastPing(self, ping : dict, targetPlayers: list, exceptPlayers: list = []):
        """
        Sendet einen Ping an alle angegebenen Spieler (alle wenn leere Liste), außer die, die in der Ausnahmenliste übergeben werden

        Args:
            ping (dict): Ping, bereits verarbeitet mit Ping.fromData
            targetPlayers (list): Liste von Spielernamen, wenn leer werden alle bekannten als Ziel angenommen
            exceptPlayers (list, optional): Spieler, an welche nicht gesendet werden soll. Nur sinnvoll, wenn an alle gesendet wird. Defaults to [].
        """
        if targetPlayers == []:
            for player in self.__mailbox.keys():
                if player == "console": continue
                if player in exceptPlayers: continue
                self.__mailbox[player].append(ping)
        else:
            for player in targetPlayers:
                self.__mailbox[player].append(ping)
        
        print(self.__mailbox)
        
    
    
    #def computeNightVoteCycle(playerDatabase, nightCounter):
    #    rolesToPlayers = dict()
    #    print(playerDatabase)
    #    for role in ROLES_LIST:
    #        rolesToPlayers[role.getname] = []
    #    for player, data in playerDatabase:
    #        print(data.getrole())
    #        rolesToPlayers[data.getrole().getname()].append(player.getname)
    #
    #    nightVoteCycle = []
    #
    #    if rolesToPlayers["werewolf"]:
    #        nightVoteCycle.append(VoteState("werewolf", rolesToPlayers["werewolf"]))



# Initialisierung des Servers
Server = ServerGame()


def computePing(ip : str, ping : dict):
    """
    Ping an den Server übergeben

    Args:
        ip (str): Die Quell-IP des Pings
        ping (dict): Der emfangene Ping
    """
    return Server.computePing(ip, ping)

#class VoteState():
#    def __init__(self, voteType : str, players):
#        self.__voteType = voteType
#        self.__players = players
#        self.__stateType = "vote"
#    def getStateType(self):
#        return self.__stateType
#    def onEnter(self, mailbox):
#        for player in self.__players:
#            mailbox[player].append({
#                        "type": "VotePing",
#                        "data": repr(self.__vote),
#                    })
#        return mailbox