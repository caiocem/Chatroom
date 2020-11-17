import socket
import time
import threading
import random 

HOST = '127.0.0.1'#Servidor está na própria máquina
PORT = 20000
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST,PORT)
inp = input("Nome de usuário:")
msg = 'User:'+inp.split(sep=':')[0]
udp.sendto (msg.encode(), dest)
#msg = input()

def send ():
    while True:
        msg = input()
        udp.sendto (msg.encode(), dest) 
        if msg == '/bye':
            break   

def receiv ():
    while True:
        msg, serv = udp.recvfrom(1024)
        if msg.decode() != 'ack':
           print(msg.decode()) 
        if msg.decode() == '/bye':
            udp.close
            break   

t1 = threading.Thread(target=send)
t1.start()
t2 = threading.Thread(target=receiv)
t2.start()
