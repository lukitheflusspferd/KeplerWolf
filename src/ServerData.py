
ipToPlayername = dict()


def resolveIPtoPlayerName(ip : str) -> str:
    return ipToPlayername.get(ip)

def computePing(ip : str, data : dict) -> dict:
    playerName = resolveIPtoPlayerName(ip)

    match data['type']:
        case 'emptyPing':
            return {
                "type":"emptyPing",
                "data":"",
            }
        case _:
            raise Exception("Unknown ping Type from IP ["+ip+"]")