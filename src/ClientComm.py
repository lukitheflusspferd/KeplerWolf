import json
from time import sleep
import socket

from ClientData import computePing

ip = "10.4.14.26"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, 65432))

try:
    while True:
        message = {
        "type":"emptyPing",
        "data":"",
        }

        b_message = json.dumps(message).encode('utf-8')
        s.send(b_message)

        b_answer = s.recv(1024)
        computePing(json.loads(b_answer))
        print("[{}] {}".format(ip, b_answer.decode()))
        
        sleep(1)
finally:
    s.close()