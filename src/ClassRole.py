from enum import Enum

class grouptypes(Enum):
    """
    Definiert Arten von Gruppen, welche als solche gewinnen können
    """
    villager = 1
    werewolf = 2
    lovers = 3
    fluted = 4
    fluter = 5
    alpha = 6

class Role():
    def __init__(self, name, description, group, hp_start, id, maxPlayerCount : int = 999999):
        """
        Konstruktoraufruf für Role-Klasse
        """
        self.__name = name
        self.__description = description
        self.__group = group
        self.__hp_start = hp_start
        self.__id = id
        self.__maxPlayerCount = maxPlayerCount

    # def __repr__(self):
    #     return (f'(name="{self.__name}", description="{self.__description}", '
    #             f'group="{self.__group}", hp_start={self.__hp_start})')
    
    def getname(self):
        return self.__name
    
    def getdescription(self):
        return self.__description
    
    def getgroup(self):
        return self.__group
    
    def gethp_start(self):
        return self.__hp_start

    def getId(self):
        return self.__id
    
    def getMaxPlayerCount(self):
        return self.__maxPlayerCount
    
    def setgroup(self, group):
        self.__group = group
    
    def __str__(self):
        group_type = "Gut" if self.__group == grouptypes.villager else \
                     "Böse" if self.__group == grouptypes.werewolf else \
                     "Spielt allein"
        return f"{self.__name}: {self.__description} {group_type}."

    def action(self, player, target=None):
        raise NotImplementedError('Diese Methode sollte in Unterklassen implementiert werden.')
    
    
"""    
# Test:
r1 = Role("Werwolf", "Kann Dorfbewohner fressen", "Böse", 2)
repr_string = repr(r1)
print(repr_string)  # Ausgabe prüfen

# Rekonstruktion mit eval:
r2 = eval(repr_string)
print(r2)  # Sollte das gleiche anzeigen
"""