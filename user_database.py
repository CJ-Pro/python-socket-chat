from cryptography.fernet import Fernet
from os import path
import pickle

e2e = Fernet(b'M1FvtMIU5xp4vQ7pwFMzh8qJ-5xHhTl7V6csoxJvy8g=')


def add(users):
    with open('user_database.txt', 'w') as user_database:
        user_database.write(e2e.encrypt(pickle.dumps(users)).decode())
        user_database.close()


def initialize():
    if path.exists('user_database.txt'):
        with open('user_database.txt') as user_database:
            users = pickle.loads(e2e.decrypt(user_database.read().encode()))
            user_database.close()
            return users
    return {}