from ClassRole import Role, grouptypes

#Werwolf: kennt andere werwölfe, spieler (nicht-werwolf) auswählen töten (countdown später?)
#Dorfbewohner: nix?
#Hexe: 1* töten (nicht hexe)  und heilen (-> muss wissen, wer gestorben ist)

class Werewolf(Role):
    def __init__(self):
        super().__init__('Werwolf', 'kann mit anderen Werwölfen Gegner in der Nacht töten', grouptypes.werewolf, 2 )

"""
    def vote_kill(target):
        if target.getrole() != grouptypes.werewolf:
            target.werewolfvote()
"""        


class Villager(Role):
    def __init__(self):
        super().__init__('Dorfbewohner', 'keine besonderen Fähigkeiten', grouptypes.villager, 1 )
    
    def __repr__(self):
        return "Villager()"

class Witch(Role):
    def __init__(self, hasHealed = False, hasKilled = False, awakens = True):
        super().__init__('Hexe', 'kann je 1x töten und heilen im ganzen Spiel, in der Nacht', grouptypes.villager, 1 )
        self.__hasHealed = hasHealed
        self.__hasKilled = hasKilled
        self.__awakens = awakens

        def sethealed(self, boolean):
            self.__healed == boolean
    
    def __repr__(self):
        return f"Witch(hasHealed={self.__hasHealed}, hasKilled={self.__hasKilled}, awakens={self.__awakens})"
            
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
