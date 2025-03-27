from ClientData import mailbox

def Voting(players, type):
    global mailbox
    if type == 'werewolf': 
        votetype = 'zum töten durch Werwölfe: '
    elif type == 'mayor':
        votetype = 'zur Bürgermeisterwahl: '
    elif type == 'hanging':
        votetype = 'zum Anklagen: '
    elif type == 'alpha': 
        votetype = 'zum töten durch den ALPHA: '
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
    mailbox.append(Vote)

def Nominate(players, type):
    if nominateactive:
        if type == 'mayor': print('Nominiere einen Spieler zum Bürgermeister:')
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
        while notyetvoted:
            Vote = input('Hier den Namen eingeben: ')
            for i in players:
                if Vote == i: notyetvoted = False
            if notyetnominated: print('Name nicht erkannt')
        mailbox.append(Vote)

        