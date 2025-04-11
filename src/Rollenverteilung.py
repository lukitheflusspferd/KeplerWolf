import random, ast

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
        return (f"Error: Not enough players. You need at least {specialRolesCount} players for the given roles.")
    
    # Erstellen einer Liste aller einzelnen Rollen (z. B. ["Werewolf", "Witch", ...])
    roles = []
    for role, count in rolesConfig.items():
        roles.extend([role] * count)
    
    # Auffüllen der Rollenliste mit "Dorfbewohner" für die restlichen Spieler
    roles.extend(["Villager"] * (len(players) - len(roles)))
    
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
