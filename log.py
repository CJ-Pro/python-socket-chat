from cryptography.fernet import Fernet
import json
from os import path


class Log:
    _chat_log = {}

    @staticmethod
    def initialize_file():

        if path.exists('log.txt'):
            log_file = open('log.txt')
            Log._chat_log = json.load(log_file)
            log_file.close()
        else:
            with open('log.txt', 'w') as log_file:
                json.dump({}, log_file)
                log_file.close()

    @staticmethod
    def add(username, chat):

        if username in Log._chat_log.keys():
            Log._chat_log[username].append(chat)
        else:
            Log._chat_log[username] = [chat]

    @staticmethod
    def close():
        with open('log.txt', 'w') as log_file:
            json.dump(Log._chat_log, log_file, indent=4)
            log_file.close()