#class ServerSubState():
#    def __init__(self, onEnter, onPing, onFinish):
#        self.__onEnter = onEnter
#        self.__onPing = onPing

from Roles import ROLES_LIST

def computeNightVoteCycle(playerDatabase, nightCounter):
    rolesToPlayers = dict()
    print(playerDatabase)
    for role in ROLES_LIST:
        rolesToPlayers[role.getname] = []
    for player, data in playerDatabase:
        print(data.getrole())
        rolesToPlayers[data.getrole().getname()].append(player.getname)
    
    nightVoteCycle = []

    if rolesToPlayers["werewolf"]:
        nightVoteCycle.append(VoteState("werewolf", rolesToPlayers["werewolf"]))


class VoteState():
    def __init__(self, voteType : str, players):
        self.__voteType = voteType
        self.__players = players
        self.__stateType = "vote"
    
    def getStateType(self):
        return self.__stateType

    def onEnter(self, mailbox):
        for player in self.__players:
            mailbox[player].append({
                        "type": "VotePing",
                        "data": repr(self.__vote),
                    })
        return mailbox