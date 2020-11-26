# Dupla:
# Caio Henrici - 92558
# Rodrigo Chichorro - 92535

import socket
import time
import threading
import random
import os

class Cliente:
    def __init__(self):
        self.HOST = '127.0.0.1' #Servidor está na própria máquina
        self.PORT = 20000
        self.dest = (self.HOST,self.PORT)
        self.nome = ''
        self.clientes = []
        self.arquivo = ''
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.arq_pedido = ''
        self.aberto = True
        self.server_aberto = True

    def send (self):
        while self.aberto:
            msg = input()
            
            if msg == '/list':
                self.udp.sendto('LIST'.encode(), self.dest)

            elif msg == '/bye':
                self.udp.sendto('BYE'.encode(), self.dest)
                break

            elif msg.startswith('/file '):
                filename = msg.split('/file ')[1]
                if not os.path.isfile(filename):
                    print('ERRO: arquivo pedido não existe. Tente novamente.')
                    continue
                msg = msg.replace('/file ', 'FILE:', 1)
                self.udp.sendto(msg.encode(), self.dest)
                self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tcp.connect(self.dest)
                with open(filename, 'rb') as file:
                    pacote = file.read(1024)
                    while pacote:
                        self.tcp.send(pacote)
                        pacote = file.read(1024)
                self.tcp.close()
                print('Terminou de enviar ' + filename)

            elif msg.startswith('/get '):
                filename = msg.split('/get ')[1]
                if self.arq_pedido != '':
                    print('Um arquivo de cada vez, afobado!')
                elif filename == '' or filename != self.arquivo:
                    print('ERRO:get inválido')
                else:
                    self.arq_pedido = filename
                    msg = msg.replace('/get ', 'GET:', 1)
                    self.udp.sendto(msg.encode(), self.dest)
                # Recebimento do arquivo implementado abaixo na função receive (diretiva FILE)

            else:
                msg = 'MSG:'+msg
                self.udp.sendto(msg.encode(), self.dest)
        

    def receive (self):
        while self.aberto:
            encoded_msg, serv = self.udp.recvfrom(1024)
            msg = (encoded_msg.decode()).split(':')

            if msg[0] == 'LIST':
                self.clientes = msg[1].split(',')
                print('Clientes conectados:\n'+msg[1])

            elif msg[0] == 'MSG':
                print(msg[1] + ' disse: ' + msg[2])

            elif msg[0] == 'INFO':
                if msg[1] == 'ARQ':
                    self.arquivo = msg[3]
                    print(msg[2] + ' enviou ' + msg[3])
                elif msg[1] == 'ENTROU':
                    self.clientes.append(msg[2])
                    print(msg[2] + ' entrou')
                elif msg[1] == 'SAIU':
                    self.clientes.append(msg[2])
                    print(msg[2] + ' saiu')
                    if msg[2] in self.clientes:
                        self.clientes.remove(msg[2])
            
            elif msg[0] == 'BYE':
                self.aberto = False
                break

            elif msg[0] == 'FILE':
                if msg[1] == 'ERRO':
                    print('Erro no recebimento de arquivo: nome inválido')
                elif msg[1] == self.arq_pedido:
                    self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.tcp.connect(self.dest)
                    with open(self.nome + '/' + self.arq_pedido, 'wb') as file:
                        print('Recebendo ' + self.arq_pedido)
                        pacote = self.tcp.recv(1024)
                        while pacote:
                            file.write(pacote)
                            pacote = self.tcp.recv(1024)
                    self.tcp.close()
                    print(self.arq_pedido + ' recebido')
                    self.arq_pedido = ''
        self.udp.close()

    def start(self):
        inp = input("Nome de usuário:")
        self.nome = inp.split(sep=':')[0]
        while self.nome == ''  or ':' in self.nome:
            inp = input('Nome inválido, digite novamente:')
            self.nome = inp.split(sep=':')[0]
        if not os.path.exists(self.nome):
            os.makedirs(self.nome)
        msg = 'USER:'+self.nome
        self.udp.sendto (msg.encode(), self.dest)
        self.clientes = [inp.split(sep=':')[0]]
        t1 = threading.Thread(target=self.send)
        t1.start()
        t2 = threading.Thread(target=self.receive)
        t2.start()

cli = Cliente()
cli.start()
