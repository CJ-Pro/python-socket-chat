from socket import socket, AF_INET, SOCK_STREAM
import platform
from threading import Thread
from user import User

buffer = 2048
server = socket(AF_INET, SOCK_STREAM)
server.bind(('localhost', 4444))  # For internet use '0.0.0.0' with port 80
encoding = 'utf8'


def start_server():

    while True:
        client, address = server.accept()

        while True:
            username = client.recv(buffer).decode()
            password = client.recv(buffer).decode()
            if User.user_validation(username, password, client):
                break

        chat_thread = Thread(target=start_chat, args=(client, username))
        chat_thread.start()


def start_chat(client, current_user):
    chat_type = client.recv(buffer).decode()
    if chat_type == 'private':
        private_chat(client, current_user)
    else:
        group_chat(client, current_user)


def receive_messages(client, current_user, is_group):

    while True:
        message = client.recv(buffer)
        if message == b'logout':
            User.logout(current_user)
            client.send(b'logout')
            client.close()
            break
        print(message)
        if is_group:
            User.broadcast(current_user, message)
        else:
            User.private_message(current_user, message)


def private_chat(client, current_user):
    while True:
        private_chat_receiver = client.recv(buffer).decode()
        if User.is_valid(current_user, private_chat_receiver, client):
            break

    receive_messages(client, current_user, False)


def group_chat(client, current_user):

    receive_messages(client, current_user, True)


if __name__ == '__main__':
    print(f"Welcome to {platform.system()} chat")
    print('All messages are encrypted on server.')
    print("Waiting for users to join...")
    server.listen()
    server_thread = Thread(target=start_server)
    server_thread.start()
    server_thread.join()
    server.close()
