from enum import Enum

class announcementtypes(Enum):
    werewolf = 1
    mayor = 2
    hanging = 3
    alpha = 4
    lovers = 5
    hunter = 6

def Voting(players, type):
    print("Voting wird ausgeführt")
    
    if type == "werewolf": 
        votetype = 'zum töten durch Werwölfe: '
    elif type == "mayor":
        votetype = 'zur Bürgermeisterwahl: '
        print("votetype")
    elif type == "hanging":
        votetype = 'zum Anklagen: '
    elif type == "alpha": 
        votetype = 'zum töten durch den ALPHA: '
    elif type == "hunter":
        votetype = 'zum töten durch den Jäger: '
    namesavailable = 'Spieler verfügbar ' + votetype
    j = 0
    for i in players:
        if j == 0:
            namesavailable +=  (i)
        else: 
            namesavailable +=  (', ' + i)
        j += 1 
    print(namesavailable)
    notyetvoted = True
    while notyetvoted:
        print('Für wen votest du?')
        Vote = input('Hier den Namen eingeben: ')
        for i in players:
            if Vote == i: notyetvoted = False
        if notyetvoted: print('Name nicht erkannt')
    return Vote

def Nominate(players, type):
    global mailbox
    if type == announcementtypes.mayor: print('Nominiere einen Spieler zum Bürgermeister:')
    else: print('Klage einen Spieler an')
    namesavailable = 'Spieler verfügbar: '
    j = 0
    for i in players:
        if j == 0:
            namesavailable +=  (i)
        else: 
            namesavailable +=  (', ' + i)
        j += 1 
    print(namesavailable)
    notyetnominated = True
    while notyetnominated:
        Vote = input('Hier den Namen eingeben: ')
        for i in players:
            if Vote == i: notyetnominated = False
        if notyetnominated: print('Name nicht erkannt')
    mailbox.append(Vote)

# ARRAY SLOTS JE NACH FINALER FORMATIERUNG ANPASSEN
def displaydirectresults(player, type):
    if type == announcementtypes.mayor: print(player[0] + ' wurde zum Bürgermeister gewählt.')
    elif type == announcementtypes.werewolf: print(player[0] + ' wurde von den Werwölfen getötet.')    
    elif type == announcementtypes.hanging: print(player[0] + ' wurde vom Dorf zu Tode verurteilt. '+ player[0] + ' hatte die Rolle ' + player[4] + '.')
    elif type == announcementtypes.alpha: print(player[0] + ' wurde vom Alpha Werwolf getötet.')
    elif type == announcementtypes.lovers: print(player[0] + ' war mit dem Spieler verliebt und ist mit gestorben.')
    elif type == announcementtypes.hunter: print(player[0] + ' wurde vom Jäger erschossen. ')

def displaynightresults(players):
    for i in players:
        print(i[0] + ' ist in der Nacht gestorben. ' + i[0] + ' hatte die rolle ' + i[4] + '.')