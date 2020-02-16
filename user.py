class User:
    _users = {}  # users is private to class
    _private_sockets = []
    _encoding = "utf8"

    @staticmethod
    def user_validation(username, password, socket):

        if username in User._users.keys():
            if User._users[username]['socket'] is not None:
                socket.send(b'User already logged in')
                return False
            elif User._users[username]['password'] != password:
                socket.send(b'Password Incorrect!')
                return False

            User._users[username]['socket'] = socket
            socket.send(b'Logged in Successfully')
            return True
        else:
            if ' ' not in username:
                details = {'password': password, 'socket': socket, 'private_message_socket': None}
                User._users[username] = details
                socket.send(b'Registered Successfully')
                return True

            socket.send(b'Please enter a valid username, no space')
            return False

    @staticmethod
    def broadcast(current_user, message):
        for user in User._users.keys():
            if user != current_user:
                socket = User._users[user]['socket']
                if socket is not None and socket not in User._private_sockets:
                    socket.send(message)

    @staticmethod
    def is_valid(current_user, private_chat_receiver, socket):

        if current_user != private_chat_receiver:
            receiver = User._users.get(private_chat_receiver)
            if receiver is not None:
                socket.send(b'{True}')
                current = User._users.get(current_user)
                current['private_message_socket'] = receiver['socket']
                User._private_sockets.append(current['socket'])
                return True

            socket.send(b'User not found')
            return False

        socket.send(b'You cannot private message yourself')
        return False

    @staticmethod
    def private_message(current_user, message):
        private_message_socket = User._users[current_user]['private_message_socket']
        if private_message_socket is not None:
            private_message_socket.send(message)

    @staticmethod
    def logout(current_user):
        user = User._users.get(current_user)
        socket = user['socket']
        for username in User._users.keys():
            if socket == User._users[username]['private_message_socket']:
                User._users[username]['private_message_socket'] = None

        user['socket'] = None
        user['private_message_socket'] = None
