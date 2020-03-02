from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import platform
from e2e import E2E

validated = False
user_valid = False
username = None
private_chat_receiver = None
logged_in = True
buffer = 2048
encoding = "utf8"
server = socket(AF_INET, SOCK_STREAM)


"""User will login if an account exists or they are registered automatically, The usernames are consistent as the 
first letters of the names are capitalized with the rest lower """


def user_login_registration():
    global validated
    global username

    print("Welcome to " + platform.system() + " Python Chat, Login or Register below:")

    while validated is not True:
        username = input('Enter username:')
        password = input("Enter password (If no entry 'password' will be used):")

        username = capitalize_first_letter(username)
        if not password:
            password = 'password'

        server.send(bytes(username, encoding))
        server.send(bytes(password, encoding))

        log = server.recv(buffer).decode()
        print(log)
        if log == 'Registered Successfully' or log == 'Logged in Successfully':
            validated = True

    start_chat()


"""Users can choose to start a private or group chat session"""


def start_chat():
    print('Enter private to start a private chat, otherwise enter any key to start group chat')
    chat_type = input()

    if chat_type == 'private':
        server.send(b'private')
        private_chat()
    else:
        server.send(b'group')
        if username == 'Admin':
            admin_chat()
        else:
            group_chat()


"""The private chat asks for a logged in user, if none is found, no session will be started"""


def private_chat():
    global user_valid
    global private_chat_receiver

    while user_valid is not True:

        private_chat_receiver = input('Enter username to send private messages to:')

        private_chat_receiver = capitalize_first_letter(private_chat_receiver)
        server.send(bytes(private_chat_receiver, encoding))

        is_valid = server.recv(buffer).decode()

        if is_valid == '{True}':
            user_valid = True
        else:
            print(is_valid)

    print(f"Started private chat with {private_chat_receiver}. Enter logout to logout")
    print('Type messages below:')

    receive_thread.start()
    send_messages()
    receive_thread.join()


def group_chat():
    print('Group Chat started. Enter logout to logout. Type messages below:')

    receive_thread.start()
    send_messages()
    receive_thread.join()


"""Function to allow consistency in username"""


def capitalize_first_letter(word):
    if word:
        word = word[0].upper() + word[1:].lower()
    else:
        word = ' '

    return word


"""Messages are encrypted before sending to the server"""


def send_messages():

    global logged_in

    while logged_in:
        try:
            message = input()
            encrypted_message = E2E.encrypt(username + '> ' + message)

            if message == 'logout':
                encrypted_logout_message = E2E.encrypt(username + ' has logged out from python chat')
                server.send(encrypted_logout_message)
                server.send(b'logout')
                break

            server.send(encrypted_message)

        except:
            pass


"""Also messages are decrypted when received on client, showing end to end encryption"""


def receive_messages():

    global logged_in

    while True:
        try:
            message = server.recv(buffer)
            if message == b'logout':
                logged_in = False
                print('<-Enter to dismiss')
                server.close()
                break

            if username == 'Admin' and b'logged in users:' in message:
                print(message.decode())
            elif b'Admin' in message:
                print(message.decode())
            else:
                decrypted_message = E2E.decrypt(message).decode()
                print(decrypted_message)
        except:
            pass


def admin_chat():

    receive_thread.start()
    send_admin_messages()
    receive_thread.join()


"""Admin has a separate function to send messages with priviledges"""


def send_admin_messages():

    print('Admin functions: view logged in users, warn, kick, ban')

    while True:
        try:
            message = input()
            if message == 'logout':
                server.send(b'logout')
                break

            elif message == 'view logged in users':
                server.send(message.encode())

            elif message == 'ban' or message == 'warn' or message == 'kick':
                message = capitalize_first_letter(input('Which User?')) + ' ' + message
                server.send(message.encode())

            else:
                encrypted_message = E2E.encrypt(username + '> ' + message)
                server.send(encrypted_message)

        except:
            pass


receive_thread = Thread(target=receive_messages)


if __name__ == '__main__':
    server.connect(('localhost', 9686))
    user_login_registration()
