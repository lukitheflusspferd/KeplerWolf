from enum import Enum

class grouptypes(Enum):
    villager = 1
    werewolf = 2
    lovers = 3
    fluted = 4
    fluter = 5
    alpha = 6

class Role():
    def __init__(self, name, description, group, hp_start):
        """
        Konstruktoraufruf für Role-klasse
        """
        self.__name = name
        self.__description = description
        self.__group = group
        self.__hp_start = hp_start
    
    def getname(self):
        return self.__name
    
    def getdescription(self):
        return self.__description
    
    def getgroup(self):
        return self.__group
    
    def gethp_start(self):
        return self.__hp_start

    def setgroup(self, group):
        self.__group = group
    
    def __str__(self):
        return f"{self.__name}: {self.__description}"

    def action(self, player, target=None):
        raise NotImplementedError('Diese Methode sollte in Unterklassen implementiert werden.')