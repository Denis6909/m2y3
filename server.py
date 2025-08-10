from socket import *
from time import sleep
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("localhost", 12345))
server_socket.setblocking(False)
server_socket.listen(5)
clients = []
while True:
    try:
        connection, address = server_socketaccept()
        client_name = connection.recv(1024).decode()
        print("Підключився клієнт ",client_name)
        connection.setblocking(False)
        clints.append((connection, client_name))
    except:
        pass
    for client in clients:
        try:
            client[0],send(f'Онлайн: {client[1]}'.encode())
        except:
            prit(f'Відключився від сервера: {client[1]}')
            clients.remove(client)
sleep(0.5)