from cryptography.fernet import Fernet
import json


class Log:
    _chat_log = {}
    _data_file = None

    @staticmethod
    def _initialize_file():
        try:
            Log._data_file = open('log.txt', 'w')
            Log._chat_log = json.load(Log._data_file)
        except:
            pass

    @staticmethod
    def add(username, chat):

        Log._initialize_file()

        if username in Log._chat_log.keys():
            Log._chat_log[username].append(chat)
        else:
            Log._chat_log[username] = [chat]

        json.dump(Log._chat_log, Log._data_file, index=4)