from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from user import User, sockets

buffer = 2048
server = socket(AF_INET, SOCK_STREAM)
server.bind(('localhost', 9686))  # For internet use '0.0.0.0' with port 80
encoding = 'utf8'


"""Start server and validate users"""


def start_server():

    while True:
        client, address = server.accept()

        while True:
            username = client.recv(buffer).decode()
            password = client.recv(buffer).decode()
            if User.user_validation(username, password, client):
                break

        sockets[username] = client
        chat_thread = Thread(target=start_chat, args=(client, username))
        chat_thread.start()


"""Start group or private chat receiver on server"""


def start_chat(client, current_user):
    chat_type = client.recv(buffer).decode()
    if chat_type == 'private':
        private_chat(client, current_user)
    else:
        group_chat(client, current_user)



"""Special server admin functions"""


def execute_admin_functions(client, message):

    decoded_message = message.decode()

    if message == b'view logged in users':
        logged_in_users = User.get_logged_in_users()
        message = 'logged in users: ' + logged_in_users
        client.send(message.encode())

    elif 'ban' in decoded_message or 'warn' in decoded_message or 'kick' in decoded_message:

        user = decoded_message.split()[0]
        users_socket = User.get_socket(user)

        if 'warn' in decoded_message and user in sockets:
            User.broadcast('Admin', bytes('Admin> ' + user + ' was warned', 'utf8'))

        elif 'kick' in decoded_message and user in sockets:
            users_socket.send(b'logout')
            User.broadcast('Admin', bytes('Admin> ' + user + ' was kicked out', 'utf8'))
            User.logout(user)

        elif 'ban' in decoded_message and user in sockets:
            users_socket.send(b'logout')
            User.broadcast('Admin', bytes('Admin> ' + user + ' was banned', 'utf8'))
            User.ban(user)

    else:
        User.broadcast('Admin', message)


def receive_messages(client, current_user, is_group):

    while True:
        try:
            message = client.recv(buffer)
            if message == b'logout':
                client.send(b'logout')
                User.logout(current_user)
                break

            if current_user == 'Admin':
                execute_admin_functions(client, message)
            else:
                if len(message.decode()) > 0:
                    print(message)
                if is_group:
                    User.broadcast(current_user, message)
                else:
                    User.private_message(current_user, message)
        except:
            pass


def private_chat(client, current_user):
    while True:
        private_chat_receiver = client.recv(buffer).decode()
        if User.is_valid(current_user, private_chat_receiver, client):
            break

    receive_messages(client, current_user, False)


def group_chat(client, current_user):

    receive_messages(client, current_user, True)


if __name__ == '__main__':
    print('All messages are encrypted on server.')
    print("Waiting for users to join...")
    server.listen()
    server_thread = Thread(target=start_server)
    server_thread.start()
    server_thread.join()
    server.close()
