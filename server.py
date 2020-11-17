import socket
import time
import random 

HOST = '127.0.0.1'#Servidor está na própria máquina
PORT = 20000
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST,PORT)
udp.bind(orig)
dic = {} 
while True:
    msg, cliente = udp.recvfrom(1024)
    msg1 = msg.decode()

    if msg1.split(sep=':')[0] == 'User':
        dic[cliente] = msg1.split(sep=':')[1]
        print('INFO:' + msg1.split(sep=':')[1] + ' entrou')
        resp = msg1.split(sep=':')[1] + ' entrou'
        for x in dic:
            if x != cliente:
                udp.sendto(resp.encode(), x)

    elif msg1[0] != '/' :#and msg1.split(sep=':')[0] != 'User':
        print('MSG:'+ dic[cliente] + ':'+msg1)
        resp = dic[cliente] + ' disse: ' + msg1
        for x in dic:
            if x != cliente:
                udp.sendto(resp.encode(), x)

    elif msg1 == '/list':
        resp = 'Clientes conectados: \n'
        for x in dic:
            resp += dic[x] + ', '
        resp = resp[:-2]
        udp.sendto(resp.encode(), cliente)
    
    elif msg1 == '/bye':
        resp = dic[cliente] + ' saiu'
        for x in dic:
            if x != cliente:
                udp.sendto(resp.encode(), x)
        del dic[cliente]
        udp.sendto(resp.encode(), cliente)
    
    #/get /file

udp.close()