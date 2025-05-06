from Roles import *

class Player():
    def __init__(self, name, role = "Villager()", isdead=False, isvictim=False, ismayor=False, isawake=False, playervotesleft=0, votesforplayer=0, currenthp=1, coupledWith = ""):
        self.__name = name
        self.__role = eval(role)
        self.__isdead = isdead
        self.__isvictim = isvictim
        self.__ismayor = ismayor
        self.__isawake = isawake
        self.__playervotesleft = playervotesleft
        self.__votesforplayer = votesforplayer
        self.__currenthp = currenthp
        self.__coupledWith = coupledWith

    def __repr__(self):
        return (f"Player(name='{self.__name}', role='{repr(self.__role)}', isdead={self.__isdead}, "
                f"isvictim={self.__isvictim}, ismayor={self.__ismayor}, isawake={self.__isawake}, "
                f"playervotesleft={self.__playervotesleft}, votesforplayer={self.__votesforplayer}, "
                f"currenthp={self.__currenthp}, coupledWith = {repr(self.__coupledWith)})")
    

    def setisdead(self, dead: bool):
        self.__isdead = dead 

    def setisvictim(self, victim: bool):
        self.__isvictim = victim

    def setrole(self, role):
        self.__role = role

    def setisawake(self, awake: bool):
        self.__isawake = awake

    def setismayor(self, mayor: bool):
        self.__ismayor = mayor

    def setname(self, name):
        self.__name = name

    def setvotes(self):
        if self.__ismayor:
            self.__playervotesleft = 2
        else: 
            self.__playervotesleft = 1

    def resetvotesforplayer(self):
        self.__votesforplayer = 0

    def setvotesforplayer(self, votes: int):
        self.__votesforplayer += votes 
    
    def resetcurrenthp(self, hp_start):
        self.__currenthp = hp_start

    def setcurrenthp(self, dmg):
        self.__currenthp -= dmg
        if self.__currenthp <= 0:
            Player.setisdead(True)
            Player.getrole().ondeath()

    def setCoupledWith(self, partner : str):
        self.__coupledWith = partner
    
    def getname(self):
        return self.__name

    def getisdead(self):
        return self.__isdead
    
    def getisvictim(self):
        return self.__isvictim

    def getrole(self):
        return self.__role

    def getismayor(self):
        return self.__ismayor

    def getisawake(self):
        return self.__isawake

    def getvotesleft(self):
        return self.__playervotesleft

    def getcurrenthp(self):
        return self.__currenthp
    
    def getvotesforplayer(self):
        return self.__votesforplayer
    
    def getCoupledWith(self) -> str:
        return self.__coupledWith
    
'''

# Test:
p1 = Player("Alice", "Witch()")
repr_string = repr(p1)
print(repr_string)  # Ausgabe prüfen

# Rekonstruktion mit eval:
p2 = eval(repr_string)
print(p2)  # Sollte das gleiche anzeigen, aber nur, wenn für die Klasse kein __str__ definiert ist, da dann __repr__ benutzt wird.
print("\n------------\n")

'''