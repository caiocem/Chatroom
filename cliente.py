import socket
import time
import threading
import random 

HOST = '127.0.0.1' #Servidor está na própria máquina
PORT = 20000
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST,PORT)
inp = input("Nome de usuário:")
msg = 'User:'+inp.split(sep=':')[0]
udp.sendto (msg.encode(), dest)
#msg = input()
clientes = [inp.split(sep=':')[0]]

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect(dest)

def send ():
    while True:
        msg = input()
        if '/file' in msg:
            tcp.send(msg.encode())
            filename = msg.split(sep='/file ')[0]
            pacote = filename.read(1024)
            while pacote:
                tcp.send(pacote)
                pacote = filename.read(1024)
        else:
            udp.sendto (msg.encode(), dest) 
            if msg == '/bye':
                tcp.send(msg.encode())
                break

def receiv (clientes):
    while True:
        msg, serv = udp.recvfrom(1024)
        if msg.decode() == '/bye':
            udp.close()
            break
        elif msg.decode() != 'ack':
           print(msg.decode()) 
        elif 'Clientes conectados: \n' in msg.decode():
            clientes = (msg.decode().split(sep=':')[0]).split(sep=',')


t1 = threading.Thread(target=send)
t1.start()
t2 = threading.Thread(target=receiv(clientes))
t2.start()
