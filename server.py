# Dupla:
# Caio Henrici - XXXXX
# Rodrigo Chichorro - 92535

import socket
import time
import threading
import random
import os

class Servidor:
    def __init__(self):
        self.HOST = '127.0.0.1' #Servidor está na própria máquina
        self.PORT = 20000
        self.orig = (self.HOST,self.PORT)
        self.clientes = {}
        self.arquivo = ''
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.bind(self.orig)
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp.bind(self.orig)
        self.tcp.listen(1)
        self.aberto = True
        self.block = False
        if not os.path.exists('arquivos'):
            os.makedirs('arquivos')
    
    def listen(self):
        while self.aberto:
            encoded_msg, cliente = self.udp.recvfrom(1024)
            msg = (encoded_msg.decode()).split(':',1)
            
            if msg[0] == 'USER':
                self.clientes[cliente] = msg[1]
                resp = 'INFO:ENTROU:' + msg[1]
                print(resp)
                for cli in self.clientes:
                    if cli != cliente:
                        self.udp.sendto(resp.encode(), cli)

            elif msg[0] == 'MSG':
                resp = 'MSG:' + self.clientes[cliente] + ':' + msg[1]
                print(self.clientes[cliente] + ':MSG:' + msg[1])
                for cli in self.clientes:
                    if cli != cliente:
                        self.udp.sendto(resp.encode(), cli)

            elif msg[0] == 'LIST':
                resp = 'LIST:'
                for cli in self.clientes:
                    resp += self.clientes[cli] + ','
                resp = resp[:-1]
                print(self.clientes[cliente] + ':LIST')
                self.udp.sendto(resp.encode(), cliente)

            elif msg[0] == 'FILE':
                self.block = True
                con, tcpCli = self.tcp.accept()
                filename = (msg[1].split('/'))[-1]
                with open('arquivos/' + filename, 'wb') as file:
                    print('Recebendo ' + msg[1] + ' de ' + self.clientes[cliente])
                    pacote = con.recv(1024)
                    while pacote:
                        file.write(pacote)
                        pacote = con.recv(1024)
                con.close()
                print(msg[1] + ' recebido')
                self.block = False
                self.arquivo = filename
                resp = 'INFO:ARQ:'+self.clientes[cliente]+':'+self.arquivo
                for cli in self.clientes:
                    if cli != cliente:
                        self.udp.sendto(resp.encode(), cli)
            
            elif msg[0] == 'GET':
                print(self.clientes[cliente] + ':GET:' + msg[1])
                if msg[1] != self.arquivo:
                    self.udp.sendto('FILE:ERRO'.encode(), cliente)
                else:
                    self.block = True
                    self.udp.sendto(('FILE:'+msg[1]).encode(), cliente)
                    con, tcpCli = self.tcp.accept()
                    with open('arquivos/'+self.arquivo, 'rb') as file:
                        pacote = file.read(1024)
                        while pacote:
                            con.send(pacote)
                            pacote = file.read(1024)
                    con.close()
                    print(msg[1] + ' enviado')
                    self.block = False
            
            elif msg[0] == 'BYE':
                resp = 'INFO:SAIU:' + self.clientes[cliente]
                print(resp)
                for cli in self.clientes:
                    if cli != cliente:
                        self.udp.sendto(resp.encode(), cli)
                self.udp.sendto('BYE'.encode(), cliente)
                del self.clientes[cliente]
        print('Listen')
        
    def fechar(self):
        while self.aberto:
            inp = input()
            if inp == '/bye':
                if self.block:
                    print('Não posso fechar agora')
                else:
                    for cli in self.clientes:
                        self.udp.sendto('BYE'.encode(), cli)
                    self.aberto = False
        self.udp.close()
        print('Saí')

    def start(self):
        t1 = threading.Thread(target=self.listen)
        t1.start()
        t2 = threading.Thread(target=self.fechar)
        t2.start()

ser = Servidor()
ser.start()
