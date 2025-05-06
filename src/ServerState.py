
#class ServerSubState():
#    def __init__(self, onEnter, onPing, onFinish):
#        self.__onEnter = onEnter
#        self.__onPing = onPing

import copy

import ClassPlayer
import Ping
import Roles

EMPTYPING = Ping.fromData("EmptyPing", "", "server")

class ServerGame():
    def __init__(self):
        self.__playerNamesPreGame = []#["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10"]
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

        self.__playerDataBase : dict[str, ClassPlayer.Player] = dict()
        
        self.__currentVoting = None
        self.__computeThisVotePing = lambda playerName, voting : None
        """
        Verarbeitung eines Votes eines Spielers

        Args:
            playerName (str): Name des abstimmenden Spielers
            voting (str): Name des Spielers, für den abgestimmt wurde, oder leerer String
        """
        
        self.__checkForThisVotingsEnd : function = None
        self.__countThisVotes : function = None
        self.__pendingVotingPlayers = set()
        self.__votings = dict()
        
        self.__voteStorage = None
        
        self.__pendingKills : set[str] = set()
        """
        Menge der Spieler, welche in der Nacht gestorben sind
        """
    
    
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
        if playername in {""}:
            return (False, "leer")
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
                self.__initVoting("nominate_hanging")
                
            case "voteTrigger2":
                self.__initVoting("hanging")
                
                    
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
            case 'VoteAnswerPing':
                if self.__serverState == "Voting":
                    self.__computeThisVotePing(playerID, pingData)
                    if self.__checkForThisVotingsEnd():
                        self.__countThisVotes()
                    if self.__serverState == "FullNomination":
                        print(f"VoteAnswerPing von [{playerID}] übersprungen, da die Nominierung bereits voll ist.")
                elif self.__serverState == "FullNomination":
                    print(f"VoteAnswerPing von [{playerID}] übersprungen, da die Nominierung bereits voll ist.")
                else: print(f"VoteAnswerPing von [{playerID}] übersprungen, da kein Voting stattfindet. (Der aktuelle State ist [{self.__serverState}])")
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
        
        # print(self.__mailbox)
        
    ### Voting Logik ###
    
    def __initVoting(self, voteType: str):
        """
        Initialisiert die für eine Abstimmung notwendigen Methoden und Variablen

        Args:
            voteType (str): Typ des Votings
        """
        self.__currentVoting = voteType
        self.__serverState = "InitVoting"
        
        self.__votings = dict()
        
        self.__pendingVotingPlayers = set()
        
        for player in self.__playerDataBase.values():
            if not player.getisdead():
                self.__pendingVotingPlayers.add(player.getname())
        
        votePing = dict()
        votePing["type"] = voteType
        votePing["dummy"] = "False"
        
        match voteType:
            case 'werewolf':
                self.__computeThisVotePing = lambda playerName, voting : self.__computeVotePing(playerName, voting)
                self.__checkForThisVotingsEnd = self.__checkForVotingsEnd
                
                possiblePlayers = []
                votingPlayers = []
                
                for k, v in self.__rolesToPlayernames.items():
                    if k in {"werewolf", "alpha"}:
                        votingPlayers.extend(v)
                    else:
                        possiblePlayers.extend(v)
                
                self.__countThisVotes = lambda : self.__countVotes(votingPlayers)
                
                votePing["players"] = possiblePlayers
                self.__broadcastPing(Ping.fromData("VotePing", votePing, "server"), votingPlayers)
                votePing["dummy"] = "True"
                self.__broadcastPing(Ping.fromData("VotePing", votePing, "server"), [], votingPlayers)
                
            case 'nominate_mayor' | 'nominate_hanging':
                self.__computeThisVotePing = lambda playerName, voting : self.__computeVotePing(playerName, voting)
                self.__checkForThisVotingsEnd = self.__checkForNominationsEnd
                
                self.__countThisVotes = self.__countNominations
                
                possiblePlayers = []
                
                for player in self.__playerDataBase.values():
                    if not player.getisdead():
                        possiblePlayers.append(player.getname())
                
                votePing["players"] = possiblePlayers
                self.__broadcastPing(Ping.fromData("VotePing", votePing, "server"), possiblePlayers)
                
            case 'mayor' | 'hanging':
                self.__computeThisVotePing = lambda playerName, voting : self.__computeVotePing(playerName, voting)
                self.__checkForThisVotingsEnd = self.__checkForVotingsEnd
                
                votingPlayers = []
                
                for player in self.__playerDataBase.values():
                    if not player.getisdead():
                        votingPlayers.append(player.getname())
                
                self.__countThisVotes = lambda : self.__countVotes(votingPlayers)
                
                possiblePlayers = self.__voteStorage
                
                votePing["players"] = possiblePlayers
                self.__broadcastPing(Ping.fromData("VotePing", votePing, "server"), votingPlayers)
            
            case _:
                raise Exception(f"Unbekannter Vote-Typ: {voteType}")
                
                
        self.__serverState = "Voting"

    ## VotePing Verarbeitung ##
    
    def __computeVotePing(self, playerName, voting):
        """
        Verarbeitet den VotePing eines Spielers

        Args:
            playerName (str): Spieler, welcher abgestimmt hat
            voting (str): Spieler, für den abgestimmt wurde, oder leerer String
        """
        try:
            self.__pendingVotingPlayers.remove(playerName)
            self.__votings[playerName] = voting
        except KeyError:
            pass
        self.__votings[playerName] = voting
        
    ## Ende des Votings überprüfen ##
    
    def __checkForVotingsEnd(self) -> bool:
        """
        Prüft, ob alle Spieler gevotet haben

        Returns:
            bool: True wenn alle Spieler eine Antwort gesendet haben
        """
        return self.__pendingVotingPlayers == set()
    
    def __checkForNominationsEnd(self) -> bool:
        """
        Prüft, ob alle Spieler gevotet haben

        Returns:
            bool: True wenn alle Spieler eine Antwort gesendet haben
        """
        if len(self.__votings.keys()) >= 3:
            self.__serverState = "FullNomination"
        return self.__pendingVotingPlayers == set()
    
    ## Voting auszählen ##
    
    def __countVotes(self, revealFor : list | str, resultAction = None):
        """
        Zählt die Abstimmung aus und sendet das Ergebnis an die ausgewählten Spieler

        Args:
            revealFor (list | str): Liste der Spieler, an die gesendet werden soll, wenn leer, dann an niemanden, wenn für alle dann stattdessen der String "alle"
            resultAction (function): Funktion, welche die Argumente (resultPlayerId : str, cause : str) hat, also mit dem gewinnenden Spieler und dem Grund (also z.B. Todesursache oder Bürgermeisterwahl) aufgerufen wird. 
        """
        self.__serverState = "CountVote"
        
        resultList = dict()
        
        for vote in self.__votings.values():
            if vote == "": continue
            if not vote in resultList:
                resultList[vote] = 1
            else: resultList[vote] += 1
        
        highestResult = (None, 0)
        for playerName, voteResult in resultList.items():
            if voteResult > highestResult[1]:
                highestResult = (playerName, voteResult)
        
        # Folgeaktion ausführen
        if (highestResult != None) and (resultAction != None):
            resultAction(highestResult)
        
        
        resultPing = {
            "names": [highestResult[0]],
            "type": self.__currentVoting
        }
        
        if revealFor != []:
            if revealFor == "all": revealFor = []
            self.__broadcastPing(Ping.fromData("VoteResultPing", resultPing, "server"), revealFor)
        
        self.__serverState = "Game"
    
    def __countNominations(self):
        """
        Nimmt die (theoretisch) höchstens drei vorhandenen Nominierungen und sendet diese an alle Spieler und speichert das Ergebnis in self.__voteStorage
        """
        self.__serverState = "CountVote"
        
        nominations = []
        
        for vote in self.__votings.values():
            if vote == "": continue
            if not vote in nominations:
                nominations.append(vote)
                
        if len(nominations) > 3:
            nominations = nominations[:3]
        
        resultPing = {
            "names": nominations,
            "type": self.__currentVoting
        }
        
        self.__broadcastPing(Ping.fromData("VoteResultPing", resultPing, "server"), [])
        
        self.__voteStorage = copy.deepcopy(nominations)
        
        print(self.__voteStorage)
        
        self.__serverState = "Game"
    
    
    
    ## Aktionen, welche auf ein Voting folgen ##
    
    def __killPlayer(self, playerId : str, cause : str):
        """
        Tötet einen Spieler, sendet diesem die neuen Spielerdaten und informiert die Spieler über den Tod

        Args:
            playerId (str): Name des Spielers
            cause (str): Grund des Todes
        """
        playerData = self.__playerDataBase[playerId]
        playerData.setisdead(True)
        
        self.__playerDataBase[playerId] = copy.deepcopy(playerData)
        
        self.__mailbox[playerId].append(Ping.fromData("stateChangePing", repr(playerData), "server"))
        
        pingData = {
            "names" : [playerId],
            "type" : cause 
        }
        
        
        self.__broadcastPing(Ping.fromData("eliminationPing", pingData, "server"), [])
    
    def __killPlayerAtNight(self, playerId : str):
        """
        Fügt den Spieler der globalen Menge self.__pendingKills hinzu.

        Args:
            playerId (str): Name des Spielers
            cause (str): Grund des Todes
        """
        self.__pendingKills.add(playerId)
    
    def __healPlayer(self, playerID : str):
        """
        Entfernt einen Spieler aus der globalen Menge self.__pendingKills.

        Args:
            playerID (str): Name des Spielers
        """
        self.__pendingKills.remove(playerID)
    
    def __couplePlayers(self, secondPlayerID : str):
        """
        Verliebt zwei Spieler, der erste befindet sich im VoteStorage, der zweite wird als Argument übergeben

        Args:
            secondPLayerID (str): zweiter Spieler
        """
        firstPlayerID = self.__voteStorage.pop()
        firstPlayerData = self.__playerDataBase[firstPlayerID]
        
        secondPlayerData = self.__playerDataBase[secondPlayerID]
    
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