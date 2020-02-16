from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import platform
from e2e import E2E

validated = False
user_valid = False
username = None
private_chat_receiver = None
buffer = 2048
encoding = "utf8"
server = socket(AF_INET, SOCK_STREAM)


def user_login_registration():
    global validated
    global username

    print(f"Welcome to {platform.system()} Python Chat, Login or Register below:")

    while validated is not True:
        username = input('Enter username:')
        password = input("Enter password (If no entry 'password' will be used):")

        if username:
            username = username[0].upper() + username[1:].lower()  # Capitalize first letter
        else:
            username = ' '

        if not password:
            password = 'password'

        server.send(bytes(username, encoding))
        server.send(bytes(password, encoding))

        log = server.recv(buffer).decode()
        print(log)
        if log == 'Registered Successfully' or log == 'Logged in Successfully':
            validated = True

    start_chat()
    #  TODO separate admin chat
    #  TODO Database plus file logs (Database then push to file)
    #  TODO Broadcast Logout (public and private chat)


def start_chat():
    print('Enter private to start a private chat, otherwise enter any key to start group chat')
    chat_type = input()

    if chat_type == 'private':
        server.send(b'private')
        private_chat()
    else:
        server.send(b'group')
        group_chat()


def private_chat():
    global user_valid
    global private_chat_receiver

    while user_valid is not True:

        private_chat_receiver = input('Enter username to send private messages to:')

        if private_chat_receiver:
            private_chat_receiver = private_chat_receiver[0].upper() + private_chat_receiver[1:].lower()  #
            # Capitalize first letter
        else:
            private_chat_receiver = ' '

        server.send(bytes(private_chat_receiver, encoding))

        is_valid = server.recv(buffer).decode()

        if is_valid == '{True}':
            user_valid = True
        else:
            print(is_valid)

    print(f"Started private chat with {private_chat_receiver}. Enter logout to logout")
    print('Type messages below:')

    receive_thread = Thread(target=receive_messages)
    receive_thread.start()

    send_messages()

    receive_thread.join()


def group_chat():
    print('Enter logout to logout. Type messages below:')

    receive_thread = Thread(target=receive_messages)
    receive_thread.start()

    send_messages()
    receive_thread.join()


def send_messages():
    while True:
        try:
            message = input()
            encrypted_message = E2E.encrypt(username + '> ' + message)
            if message == 'logout':
                server.send(b'logout')
                break
            server.send(encrypted_message)
        except Exception as e:
            print(e)


def receive_messages():
    while True:
        try:
            message = server.recv(buffer)
            if message == b'logout':
                server.close()
                break
            decrypted_message = E2E.decrypt(message).decode()
            print(decrypted_message)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    server.connect(('localhost', 4444))
    user_login_registration()
