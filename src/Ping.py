def fromData(type: str, data: any, origin: str) -> dict[str, str]:
    """
    Gibt einen einheitlich formatierten Ping als Wörterbuch zurück, welches später in ein json-Objekt umgewandelt werden muss

    Args:
        type (str): Typ des Pings
        data (any): Daten des Pings, kann alles sein, also ein Wörterbuch, eine Liste, etc.. Die Daten müssen je nach Typ aber immer gleich sein
        origin (str): Ursprung des Pings, also Spielername oder 'server' oder 'console'

    Returns:
        dict: Ein Wörterbuch mit den Schlüsseln 'type', 'data', und 'playerId', welche sämtlich Zk sind, welche bei data über 'repr' erzeugt worden sind
    """
    
    ping = {
        "type" : type,
        "data" : repr(data),
        "origin" : origin
    }
    return ping

def toData(ping: dict) -> tuple[str, any, str]:
    """
    Extrahiert aus einem erhaltenen Ping dessen Typ und evaluiert dessen Daten

    Args:
        ping (dict): json-objekt, welches erhalten wurde

    Returns:
          tuple[str, any, str]: Typ des Pings, dessen Daten und der Ursprung des Pings
    """
    pingType = ping["type"]
    pingData = eval(ping["data"])
    pingOrigin = ping["origin"]
    return pingType, pingData, pingOrigin