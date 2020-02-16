from cryptography.fernet import Fernet


class E2E:

    _key = b'M1FvtMIU5xp4vQ7pwFMzh8qJ-5xHhTl7V6csoxJvy8g='

    @staticmethod
    def encrypt(data):
        return Fernet(E2E._key).encrypt(bytes(data, 'utf8'))

    @staticmethod
    def decrypt(data):
        return Fernet(E2E._key).decrypt(data)