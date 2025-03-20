from ClassRole import Role, grouptypes

#Werwolf: kennt andere werwölfe, spieler (nicht-werwolf) auswählen töten (countdown später?)
#Dorfbewohner: nix?
#Hexe: 1* töten (nicht hexe)  und heilen (-> muss wissen, wer gestorben ist)

class werewolf(Role):
    def __init__(self):
        super().__init__('Werwolf', 'kann mit anderen Werwölfen Gegner in der Nacht töten', grouptypes.werewolf, 2 )

"""
    def vote_kill(target):
        if target.getrole() != grouptypes.werewolf:
            target.werewolfvote()
"""        


class villager(Role):
    def __init__(self):
        super().__init__('Dorfbewohner', 'keine besonderen Fähigkeiten', grouptypes.villager, 1 )

class witch(Role):
    def __init__(self, has_healed, has_killed, awakens):
        super().__init__('Hexe', 'kann je 1x töten und heilen im ganzen Spiel, in der Nacht', grouptypes.villager, 1 )
        self.__healed = False
        self.__killed = False
        self.__awakens =True

        def sethealed(self, boolean):
            self.__healed == boolean
            
'''
    def show_victims():
        #print players . isvictim???
'''

'''
    def heal(target):
        if Player.healed == False:
            target = input()
            target.kill
            Player.getrole().sethealed = True
'''
       

"""
    def kill(target):
        if witch.killed==False:
            target = input()
            target.kill()

    # wenn has_killed and has_healed == True: hexe erwacht nicht mehr
"""
