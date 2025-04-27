import Ping

#class ServerSubState():
#    def __init__(self, onEnter, onPing, onFinish):
#        self.__onEnter = onEnter
#        self.__onPing = onPing

from Roles import ROLES_LIST

EMPTYPING = Ping.fromData("EmptyPing", "")

class ServerGame():
    def __init__(self):
        self.__playerNamesPreGame = ["p1", "p2"]
        self.__ipToPlayerName = dict()
        self.__mailbox = dict()
        
        self.__mailbox["console"] = []
        
        self.__serverState = "PreGame"
    
    
    ### Verwaltung von Spielernamen ###
    
    def __resolveIPtoPlayerName(self, ip : str) -> str | None:
        """
        Gibt für eine IP den Spielername oder, falls nicht existent, None zurück

        Args:
            ip (str): Ip-Adresse

        Returns:
              str | None: Spielername oder None
        """
        return self.__ipToPlayerName.get(ip)
    
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
        self.__ipToPlayerName[ip] = playername
        self.__mailbox[playername] = []
        
        self.__broadcastPing(Ping.fromData("NewLobbyPing", self.__playerNamesPreGame), [])
        
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
                    return Ping.fromData("ConsoleError", "Das Spiel ist bereits gestartet.")
                
                self.__serverState = "GameInit"
                print("Neuer Serverzustand: [GameInit].")
                print(f"Initialisierung des Spiels mit den folgenden Spielern: {str(self.__playerNamesPreGame)} ...")
                return Ping.fromData("ConsoleGameInit", self.__playerNamesPreGame)
            
            case "voteTrigger":
                vote = dict()
                vote["type"] = "mayor"
                vote["players"] = self.__playerNamesPreGame
                self.__broadcastPing(Ping.fromData("VotePing", vote), [])
                    
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
        return Ping.fromData("UsernameValidationPing", data)
    
    def computePing(self, ip : str, data : dict) -> dict:
        """
        Verarbeitung des empfangenen Pings

        Args:
            ip (str): Quell-IP des Pings
            data (dict): Inhalt des Pings

        Returns:
            dict: neuer Ping
        """
        
        if self.__serverState == "PreGame":
            print("\nPing von IP [{}] mit dem folgenden Inhalt empfangen: \n {}".format(ip, data))
        else:
            print("\nPing von Spieler [{}] an IP [{}] mit dem folgenden Inhalt empfangen: \n {}".format(self.__resolveIPtoPlayerName(ip), ip, data))

        playerID = self.__resolveIPtoPlayerName(ip)

        pingType, pingData = Ping.toData(data)

        match pingType:
            case 'EmptyPing':
                pass
            case 'ConsoleInitPing':
                self.__ipToPlayerName[ip] = "console"
                playerID = "console"
                print("Konsole verbunden!")
            case 'ConsoleCommandPing':
                return self.__computeCommand(pingData)
            case 'UsernamePing':
                if self.__serverState == 'PreGame':
                    return self.__computePlayernamePing(ip, pingData)
                else:
                    # TODO: Dem Spieler die aktuellen Daten senden, da davon auzugehen ist, dass er dem Spiel gerejoined ist
                    #raise Exception(f"Got [UsernamePing] from IP [{ip}], but the game has already been started.")
                    print(f"Anmeldeversuch von IP [{ip}] fehlgeschlagen. Das Spiel wurde bereits gestartet.")
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