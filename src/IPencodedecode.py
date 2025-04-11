def encodeIP(ip: str):
    """
    Verschlüsselt eine IP in eine Abfolge von Buchstaben.
    """
    encodedIP = ''
    numbers = ip.split('.',3)
    for i in numbers:
        temp1 = int(i)//26
        temp2 = int(i)%26
        temp1 = chr(65 + temp1)
        temp2 = chr(65 + temp2)
        encodedIP = encodedIP + temp1 + temp2
    return encodedIP


def decodeIP(ip):
    """
    Hebt die Verschlüsselung einer Buchstabenfolge auf, gibt IP wieder aus.
    """
    decodedIP = ''
    chars = list(ip)
    for i in range(8):
        if i % 2 == 0:
            temp = chars[i]
            temp = int(ord(temp)) - 65
            temp1 = temp * 26
            
        else:
            tempadd = chars[i]
            tempadd = int(ord(tempadd)) - 65
            number = temp1 + tempadd
            if decodedIP == '':
                decodedIP += str(number) 
            else: 
                decodedIP += '.' + str(number) 
    return decodedIP

tmp = input("in: ")
tmp = encodeIP(tmp)
print(tmp)
print(decodeIP(tmp))