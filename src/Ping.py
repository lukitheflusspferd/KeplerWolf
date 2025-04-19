def fromData(type: str, data: any) -> dict[str, str]:
    """
    Gibt einen einheitlich formatierten Ping als Wörterbuch zurück, welches später in ein json-Objekt umgewandelt werden muss

    Args:
        type (str): Typ des Pings
        data (any): Daten des Pings, kann alles sein, also ein Wörterbuch, eine Liste, etc.. Die Daten müssen je nach Typ aber immer gleich sein

    Returns:
        dict: Ein Wörterbuch mit den Schlüsseln 'type' und 'data', welche beide eine Zk sind, das ist bei data über 'repr' erzeugt worden
    """
    
    ping = {
        "type" : type,
        "data" : repr(data)
    }
    return ping

def toData(ping: dict) -> tuple[str, any]:
    """
    Extrahiert aus einem erhaltenen Ping dessen Typ und evaluiert dessen Daten

    Args:
        ping (dict): json-objekt, welches erhalten wurde

    Returns:
          tuple[str, any]: Typ des Pings und dessen Daten
    """
    pingType = ping["type"]
    pingData = eval(ping["data"])
    return pingType, pingData