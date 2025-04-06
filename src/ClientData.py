from ClassPlayer import Player

clientPlayerData = None

mailbox = [""]
validName = False
errorName = ""

def computePing(message: dict):
    if message["type"] == "InitPing":
        global clientPlayerData
        clientPlayerData = eval(message["data"])

        print(clientPlayerData)
        print("")

    if message["type"] == "TestPing":
        test = True

    if message["type"] == "EmptyPing":
        pass

    if message["type"] == "SetMode":
        type = eval(message["data"]["eventType"])
        data = eval(message["data"]["data"])
        # if eventType == 
        # hier später pygame Funktion aufrufen
        
    if message["type"] == "DeathPing":
        username = eval(message["data"]["username"])
        role =  eval(message["data"]["role"])
        # hier später pygame Funktion aufrufen
        
    if message["type"] == "UsernameValidationPing":
        global validName
        validName = eval(message["data"]["valid"])

        global errorName
        errorName = eval(message["data"]["error"])
        if errorName == "doppelt": 
            print("Dieser Name wird schon benutzt")

        print(validName)
        print(errorName)

    if mailbox != "":
        return mailbox[0]

