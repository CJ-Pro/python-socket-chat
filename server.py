from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from user import User

buffer = 2048
server = socket(AF_INET, SOCK_STREAM)
server.bind(('localhost', 2222))  # For internet use '0.0.0.0' with port 80
encoding = 'utf8'


def start_server():
    while True:
        client, address = server.accept()

        while True:
            username = client.recv(buffer).decode()
            password = client.recv(buffer).decode()
            if User.user_validation(username, password, client):
                print(username + " has joined")
                break

        chat = Thread(target=start_chat, args=(client, username))
        chat.start()


def start_chat(client, current_user):
    chat_type = client.recv(buffer).decode()
    if chat_type == 'private':
        private_chat(client, current_user)
    else:
        group_chat(client, current_user)


def private_chat(client, current_user):
    while True:
        private_chat_receiver = client.recv(buffer).decode()
        if User.is_valid(current_user, private_chat_receiver, client):
            break

    while True:
        message = client.recv(buffer).decode()
        User.get_private_socket(current_user).send(bytes(current_user + '> ' + message, encoding))


def group_chat(client, current_user):
    while True:
        message = client.recv(buffer).decode()
        print(current_user + '> ' + message)
        User.broadcast(current_user, message)


if __name__ == '__main__':
    print("Waiting for users to join...")
    server.listen()
    server_thread = Thread(target=start_server)
    server_thread.start()
    server_thread.join()
    print('closed')
