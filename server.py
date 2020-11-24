import socket
import time
import threading
import random 

HOST = '127.0.0.1'#Servidor está na própria máquina
PORT = 20000
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST,PORT)
udp.bind(orig)
dic = {} 

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp.bind(orig)
tcp.listen(1)

aberto = True

def listenUDP(aberto):
    while aberto:
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
            resp = '/bye'
            udp.sendto(resp.encode(), cliente)
            del dic[cliente]


def listenTCP(con, cliente, aberto):
    while aberto:
        msg = con.recv(1024).decode()
        if '/file' in msg:
            filename = msg.split(sep='/file ')[0]
            with open(filename, 'wb') as file:
            print(cliente, msg)
            while True:
                pacote = con.recv(1024)
                if not pacote:
                    break
                file.write(pacote)
            print('Arquivo recebido')
        elif msg == '/bye':
            break
    
    con.close()
    return

# def fechar(aberto):
#     inp = input()
#     if inp == '/bye':
#         for cliente in dic:
#             udp.sendto('/bye'.encode(), cliente)
#     aberto = False


# tFechar = threading.Thread(target=fechar, args=(aberto,))
# tFechar.start()

t1 = threading.Thread(target=listenUDP, args=(aberto,))
t1.start()
while aberto:
    con, cliente = tcp.accept()
    print(cliente,' conectar')
    t2 = threading.Thread(target=listenTCP, args=(con, cliente, aberto))
    t2.start()

udp.close()
tcp.close()