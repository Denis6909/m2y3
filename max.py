from socket import *

client_socket = socket(AF_INET, SOCK_STREAM)

name = input("Введіть своє імя:")

client_socket.bind(("localhost", 12345))
client_socket.send(name.encode())

while True:
    try:
        print(client_socket.recv(1024).decode())
    except:
        break