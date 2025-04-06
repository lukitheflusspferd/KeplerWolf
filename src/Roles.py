
from ClassRole import Role, grouptypes
from random import randint
# name, description, group, hp_start


class Armor(Role):
    def __init__(self, hasCoupled = False, awakens = True):
        super().__init__('Armor', 'Ja kann Leute verlieben', grouptypes.villager, 1)
        self.__hasCoupled = hasCoupled
        self.__awakens = awakens

    def __repr__(self):
        return f"Armor(hasCoupled={self.__hasCoupled}, awakens={self.__awakens})"
    
    
"""
    def setlovers(target1, target2):   
        target1.setgroup(grouptypes.lovers)
        target2.setgroup(grouptypes.lovers)
"""

class Seer(Role):
    def __init__(self):
        super().__init__('Seher', 'Kann Rollen anschauen', grouptypes.villager, 1)

    def __repr__(self):
        return "Seer()"
"""
    def lookatrole(target):
        return target.getrole()
"""

class Littlegirl(Role):
    def __init__(self):
        super().__init__('Blinzelmädchen', 'Kann in der Nacht eine Rolle herausfinden, aber mit einem Risiko', grouptypes.villager, 1)

    def __repr__(self):
        return "Littlegirl()"
"""
    def peek(target1, target2):
        chance = 0.2
        hit = randint(0,1)
        if hit <= chance:
            Player.kill()
        else:
            return target1.getrole(), target2.getrole()
"""

class Hunter(Role):
    def __init__(self):
        super().__init__('Jäger', 'Nimmt eine Person in den Tod mit', grouptypes.villager, 1)
        
    def __repr__(self):
        return "Hunter()"
"""
    def ondeath():
        if Player.getisdead():
            target = input()
            target.kill()
"""

class Tree(Role): 
    def __init__(self):
        super().__init__('Baum', 'Hat 2 HP, wenn er stirbt werden alle Rollen deaktiviert', grouptypes.villager, 2)

    def __repr__(self):
        return "Tree()"
"""
    def ondeath():
        if Player.getisdead():
            for i in Playerlist:
                if i.getgroup == grouptypes.villager or grouptypes.fluted or grouptypes.fluter:
                    i.setrole(villager)
"""

class Alpha(Role):
    def __init__(self):
        super().__init__('Alphawolf', 'Wacht jede 2. Nacht einzeln auf und muss alleine gewinnen', grouptypes.alpha, 1)

    def __repr__(self):
        return "Alpha()"
"""
    def vote_kill(target):
        if target.getrole() != grouptypes.werewolf:
            target.werewolfvote()    
"""
"""    
    def alphakill(target):
        target.kill()
"""


class Werewolf(Role):
    def __init__(self):
        super().__init__('Werwolf', 'kann mit anderen Werwölfen Gegner in der Nacht töten', grouptypes.werewolf, 2 )

    def __repr__(self):
        return "Werewolf()"

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