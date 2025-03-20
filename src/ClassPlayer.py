class Player():
    def __init__(self, name, villager) -> None:
        self.__name
        self.__isdead = False
        self.__isvictim = False
        self.__role = villager
        self.__ismayor = False
        self.__isawake = False
        self.__playervotesleft = 0
        self.__votesforplayer = 0
        self.__currenthp = 1

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