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
    def __init__(self, name, description, group, hp_start):
        """
        Konstruktoraufruf für Role-Klasse
        """
        self.__name = name
        self.__description = description
        self.__group = group
        self.__hp_start = hp_start

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

    def setgroup(self, group):
        self.__group = group
    
    def __str__(self):
        group_type = "gut" if self.__group == grouptypes.villager else \
                     "böse" if self.__group == grouptypes.werewolf else \
                     "unabhängig"
        return f"{self.__name}: {self.__description} und ist {group_type}."

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