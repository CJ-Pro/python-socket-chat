import user_database

users = {}
sockets = {}
private_receiver_sockets = {}
private_user_sockets = []
encoding = "utf8"


class User:

    @staticmethod
    def user_validation(username, password, socket):

        global users
        users = user_database.initialize()

        if username in sockets.keys():
            socket.send(b'User already logged in')
            return False

        if username in users.keys():
            if users[username] != password:
                socket.send(b'Password Incorrect!')
                return False

            socket.send(b'Logged in Successfully')
            return True

        else:
            if ' ' in username:
                socket.send(b'Please enter a valid username, no space')
                return False

            users[username] = password
            user_database.add(users)
            socket.send(b'Registered Successfully')
            return True

    @staticmethod
    def broadcast(current_user, message):
        for socket in sockets.values():
            if socket != sockets[current_user] and socket not in private_user_sockets:
                socket.send(message)

    @staticmethod
    def is_valid(current_user, private_chat_receiver, socket):

        if private_chat_receiver == 'Admin':
            socket.send(b'You cannot private message Admin')
            return False

        if current_user != private_chat_receiver:

            if private_chat_receiver in sockets.keys():
                private_receiver_sockets[current_user] = sockets[private_chat_receiver]
                private_user_sockets.append(socket)
                socket.send(b'{True}')
                return True

            socket.send(b'User not found')
            return False

        socket.send(b'You cannot private message yourself')
        return False

    @staticmethod
    def private_message(current_user, message):
        private_message_socket = private_receiver_sockets.get(current_user)
        if private_message_socket:
            private_message_socket.send(message)

    @staticmethod
    def logout(current_user):

        socket = sockets[current_user]

        if socket in private_user_sockets:
            private_user_sockets.remove(socket)

        if private_receiver_sockets.get(current_user):
            private_receiver_sockets.pop(current_user)

        users.pop(current_user)
        sockets.pop(current_user)
