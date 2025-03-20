from ClassPlayer import Player
from ClassRole import Role, grouptypes
from random import randint
# name, description, group, hp_start


class Armor(Role):
    def __init__(self):
        super().__init__('Armor', 'Ja kann Leute verlieben', grouptypes.villager, 1)
"""
    def setlovers(target1, target2):   
        target1.setgroup(grouptypes.lovers)
        target2.setgroup(grouptypes.lovers)
"""

class Seer(Role):
    def __init__(self):
        super().__init__('Seher', 'Kann Rollen anschauen', grouptypes.villager, 1)
"""
    def lookatrole(target):
        return target.getrole()
"""

class Littlegirl(Role):
    def __init__(self):
        super().__init__('Blinzelmädchen', 'Kann in der Nacht eine Rolle herausfinden, aber mit einem Risiko', grouptypes.villager, 1)
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
"""
    def ondeath():
        if Player.getisdead():
            target = input()
            target.kill()
"""

class Tree(Role): 
    def __init__(self):
        super().__init__('Baum', 'Hat 2 HP, wenn er stirbt werden alle Rollen deaktiviert', grouptypes.villager, 2)
"""
    def ondeath():
        if Player.getisdead():
            for i in Playerlist:
                if i.getgroup == grouptypes.villager or grouptypes.fluted or grouptypes.fluter:
                    i.setrole(villager)
"""

class Alpha(Role):
    def __init__(self):
        super().__init__('Alphawolf', 'Wacht jede 2. Nacht einzeln auf, muss alleine gewinnen', grouptypes.alpha, 1)
"""
    def vote_kill(target):
        if target.getrole() != grouptypes.werewolf:
            target.werewolfvote()    
"""
"""    
    def alphakill(target):
        target.kill()
"""