import cryptography
from cryptography.fernet import Fernet
import base64
import binascii

def check_valid_fernet(value):
    """
    Returns true if value is a valid Fernet key
    Fernet key must be 32 url-safe base64-encoded bytes

    :param value: (str) a string representing a Fernet key
    """
    try:
        decoded = base64.urlsafe_b64decode(value)
        if len(decoded) != 32: return False
        return True
    except binascii.Error:
        return False

class Encryption():
    """
    A class that provides simple encryption and decryption tasks
    """
    def __init__(self, key):
        """
        :param key: (str) a Fernet key to be used in encryption/decryption 
                    tasks
        """
        self.cipher_suite = Fernet(key)

    def _execute(self, value, task='encrypt'):
        # Check encoding
        if type(value) != bytes:
            value = value.encode('utf-8')

        # Execute task
        if (task == 'encrypt'):
            return self.cipher_suite.encrypt(value).decode('utf-8')
        else:
            return self.cipher_suite.decrypt(value).decode('utf-8')

    def encrypt(self, value):
        """
        Returns cipher-text for the given input value in plain-text.
        :param value: (str) a value to be encrypted.
        """
        return self._execute(value)

    def decrypt(self, value):
        """
        Returns plain-text for the given input value in cipher-text.
        :param value: (str) a value to be decrypted.
        """
        return self._execute(value, task='decrypt')
    