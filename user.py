users = {}  # users is private to class
sockets = {}
private_sockets = {}
encoding = "utf8"


class User:

    @staticmethod
    def user_validation(username, password, socket):

        if username in sockets.keys():
            socket.send(b'User already logged in')
            return False

        if username in users.keys():
            if users[username] != password:
                socket.send(b'Password Incorrect!')
                return False

            sockets[username] = socket
            socket.send(b'Logged in Successfully')
            return True

        else:
            if ' ' in username:
                socket.send(b'Please enter a valid username, no space')
                return False

            users[username] = password
            sockets[username] = socket
            socket.send(b'Registered Successfully')
            return True

    @staticmethod
    def broadcast(current_user, message):
        for socket in sockets.values():
            if socket != sockets[current_user] and socket not in private_sockets.values():
                socket.send(message)

    @staticmethod
    def is_valid(current_user, private_chat_receiver, socket):

        if current_user != private_chat_receiver:

            if private_chat_receiver in sockets.keys():
                private_sockets[current_user] = sockets[private_chat_receiver]
                socket.send(b'{True}')
                return True

            socket.send(b'User not found')
            return False

        socket.send(b'You cannot private message yourself')
        return False

    @staticmethod
    def private_message(current_user, message):
        private_message_socket = private_sockets[current_user]
        if private_message_socket is not None:
            private_message_socket.send(message)

    @staticmethod
    def logout(current_user):
        users.pop(current_user)
        sockets.pop(current_user)
        if current_user in private_sockets.keys():
            private_sockets.pop(current_user)
