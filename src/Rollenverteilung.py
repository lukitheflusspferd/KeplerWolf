import random

from Roles import SPECIAL_ROLES_LIST

def askForRolesCount(players : list):
    """
    Fragt in der Konsole für jede Rolle nach deren Anzahl und gibt eine Liste zurück
    
    Args:
        players (list): Liste der Spielernamen (z. B. ["Alice", "Bob", "Charlie"])
        rolesConfig (dict(str -> int)): Dictionary mit Rollen und deren Anzahl (z. B. {'Werewolf':2, 'Witch':1})
    
    Returns:
        dict: Dictionary mit Spielernamen als Schlüssel und Rollen als Werte
              oder eine Fehlermeldung (str), falls nicht genug Spieler vorhanden sind.
    """
    
    print("Angemeldete Spieler:", players)
    print(f"""Es gibt {len(players)} Spieler. Bitte gib für jede Rolle die Anzahl an Spielern an, welche diese Rolle bekommen sollen.
          Die restlichen Spieler bekommen die Rolle "Dorfbewohner".\n""")
    rolesCount = dict()
    
    print("Es gibt die folgenden Rollen:")
    # Für jede Sonderrolle
    for role in SPECIAL_ROLES_LIST:
        print(str(role))
    
    print()
    
    for role in SPECIAL_ROLES_LIST:
        valid = False
        max = role.getMaxPlayerCount()
        while not valid:
            try:
                n = int(input(f"Bitte gib ein, wie viele Spieler die Rolle {role.getname()} bekommen sollen: "))
                if n >= 0: 
                    if max >= n:
                        rolesCount[role.getId()] = n
                        valid = True
                    else:
                        raise Exception("zu viel")
                else:
                    raise Exception("negativ")
            except ValueError:
                print("Bitte gib eine gültige Zahl ein!")
            except Exception as e:
                if e.args == ("negativ",):
                    print("Bitte gib eine Zahl größergleich 0 ein!")
                elif e.args == ("zu viel",):
                    print(f"Für diese Rolle  maximal {max} Spieler zulässig.")
                else:
                    print("Es ist ein Fehler aufgetreten. Bitte versuche es erneut!")
                    print(e)
    
    return rolesCount

def assignRoles(players : list, rolesConfig : dict):
    """
    Weist Spielern die Rollen basierend der in der Konsole eingegebenen Verteilung zu.
    Übrigen Spielern wir die Rolle "Dorfbewohner" zugewiesen
    
    Args:
        players (list): Liste der Spielernamen (z. B. ["Alice", "Bob", "Charlie"])
        rolesConfig (dict(str -> int)): Dictionary mit Rollen und deren Anzahl (z. B. {'Werewolf':2, 'Witch':1})
    
    Returns:
        dict: Dictionary mit Spielernamen als Schlüssel und Rollen als Werte
              oder eine Fehlermeldung (str), falls nicht genug Spieler vorhanden sind.
    """
    # Berechne die benötigte Anzahl an Spezialrollen
    specialRolesCount = sum(rolesConfig.values())
    
    # Überprüfen, ob genug Spieler vorhanden sind
    if specialRolesCount > len(players):
        return (f"Fehler: Zu wenige Spieler für die angegebenen Rollen. Es werden mindestens {specialRolesCount} Spieler benötigt.")
    
    # Erstellen einer Liste aller einzelnen Rollen (z. B. ["Werewolf", "Witch", ...])
    roles = []
    for role, count in rolesConfig.items():
        roles.extend([role] * count)
    
    # Auffüllen der Rollenliste mit "Dorfbewohner" für die restlichen Spieler
    roles.extend(["villager"] * (len(players) - len(roles)))
    
    # Rollen zufällig mischen
    random.shuffle(roles)
    
    # Weise jedem Spieler eine Rolle zu (iteriert über die Spielerliste und kombiniert jeden mit zip() mit einer Rolle)
    return {player: role for player, role in zip(players, roles)}

'''
# --- Beispielaufruf ---
if __name__ == "__main__":
    # Beispiel-Eingabe
    #players = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace"]
    players= ast.literal_eval(input('player als liste  '))
    #roles_config = {
       # 'Werewolf': 2,
       # 'Witch': 1,
        #'Seer': 1,
        #'Hunter': 0,
       # 'Littlegirl': 0,
       # 'Alpha': 0,
       # 'Tree': 0
   # }
    roles_config=ast.literal_eval(input('rollen als dict  '))
    
    # Rollen zuweisen
    game_roles = assignRoles(players, roles_config)
    
    # Ausgabe
    if isinstance(game_roles, str):
        print(game_roles)  # Fehlermeldung
    else:
        for player, role in game_roles.items():
            print(f"{player}: {role}")
'''

    
# print(assignRoles(players= ast.literal_eval(input('player als liste  ')),roles_config=ast.literal_eval(input('rollen als dict  '))))

askForRolesCount(["p1", "p2", "p3", "p4", "p5", "p6", "p7"])