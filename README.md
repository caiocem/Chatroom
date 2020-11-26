# Chatroom
Trabalho pratico de INF 452

Dupla:
Caio Henrici - 92558
Rodrigo Chichorro - 92535

Quanto ao arquivo armazenado pelo servidor:
O servidor guarda todos os arquivos que recebe em uma pasta arquivos/ criada pelo mesmo.
Apesar do servidor poder guardar múltiplos arquivos, foi implementado apenas o envio do último arquivo recebido pelo mesmo, conforme escrito na especificação.
O cliente pode enviar para o servidor qualquer arquivo dentro da máquina, desde que o caminho fornecido esteja correto.
Um cliente, ao ser inicializado, criará uma pasta com seu nome de usuário para armazenar os arquivos que receber. Note, porém que se mais de um cliente possuir o mesmo nome de usuário, eles compartilharão a mesma pasta.
