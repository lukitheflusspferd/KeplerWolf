from enum import Enum

import Ping

class announcementtypes(Enum):
    werewolf = 1
    mayor = 2
    hanging = 3
    alpha = 4
    lovers = 5
    hunter = 6

def Voting(players, voteType, ownName, dummy):
    print("Voting wird ausgeführt")
    
    if dummy == "True":
        _ = input(f"Dummy-Voting des Typs [{voteType}]. Bitte mit Enter bestätigen")
        return Ping.fromData("VoteAnswerPing", "", ownName)
    
    if voteType == "werewolf": 
        voteSuffix = 'zum töten durch Werwölfe: '
    elif voteType == "mayor":
        voteSuffix = 'zur Bürgermeisterwahl: '
    elif voteType == "hanging":
        voteSuffix = 'zum Hinrichten: '
    elif voteType == "alpha": 
        voteSuffix = 'zum töten durch den ALPHA: '
    elif voteType == "hunter":
        voteSuffix = 'zum Töten durch den Jäger: '
    elif voteType == "see":
        voteSuffix = 'zum Ansehen der Rolle: '
    elif voteType == "witch_kill":
        voteSuffix = 'zum Töten durch die Hexe: '
    elif voteType == "witch_heal":
        voteSuffix = 'zum Heilen durch die Hexe: '
    elif voteType == "love1":
        voteSuffix = 'als erster Liebespartner: '
    elif voteType == "love2":
        voteSuffix = 'als zweiter Liebespartner: '
    namesavailable = 'Spieler verfügbar ' + voteSuffix
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
        vote = input('Hier den Namen eingeben: ')
        for i in players:
            if vote == i: notyetvoted = False
        if notyetvoted: print('Name nicht erkannt')
    return Ping.fromData("VoteAnswerPing", vote, ownName)

def Nominate(players, type, ownName):
    if type == "nominate_mayor": print('Nominiere einen Spieler zum Bürgermeister:')
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
    return Ping.fromData("VoteAnswerPing", Vote, ownName)

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