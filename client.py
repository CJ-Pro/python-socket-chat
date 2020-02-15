from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from log import Log

validated = False
user_valid = False
username = None
private_chat_receiver = None
buffer = 2048
encoding = "utf8"
server = socket(AF_INET, SOCK_STREAM)

#  TODO Add fernet (https://cryptography.io/en/latest/fernet/) message should be converted to bytes first


def user_login_registration():
    global validated
    global username

    print("Welcome to Python Chat, Login or Register below:")

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

    Log.initialize_file()
    start_chat()
    Log.close()


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
            server.send(bytes(message, encoding))
            if message == 'logout':
                break
            Log.add(username, message)
        except:
            pass


def receive_messages():
    while True:
        try:
            message = server.recv(buffer).decode()
            if message == 'logout':
                server.close()
                break
            print(message)
        except:
            pass


if __name__ == '__main__':
    server.connect(('localhost', 3333))
    user_login_registration()
