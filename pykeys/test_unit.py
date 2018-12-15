import pytest
from cryptography.fernet import Fernet
from .encryption import Encryption
from .vault import Vault

class TestEncryption():

    def setup(self):
        self.key = Fernet.generate_key()
        self.cript = Encryption(self.key)

    def test_encryption(self):
        plain_text = 'This is a secret message!'
        cipher_text = self.cript.encrypt(plain_text)
        assert cipher_text != plain_text

    def test_decryption(self):
        plain_text = 'This is a secret message!'
        cipher_text = self.cript.encrypt(plain_text)
        decrypted = self.cript.decrypt(cipher_text)
        assert plain_text == decrypted

class TestVault():
    def setup(self):
        self.vault = Vault() # cannot be tested in the very first run

    def test_add(self):
        # Add
        secrets = {'client_id':'123456',
                   'client_secret':'iveseenbetter'}
        self.vault.add('that_app', secrets)
        self.vault.add('another_app', secrets)
        self.vault.add('yet_another_app', secrets)
        
        # Get
        value = self.vault.get('that_app', 'client_secret')
        assert value == 'iveseenbetter'

        with pytest.raises(TypeError):
            value = self.vault.get(2,4)
            self.vault.add(4.2,4)
            self.vault.remove(1321)

        value = self.vault.get('madeupapp','madeupitem')
        assert value is None

        with pytest.raises(ValueError):
            self.vault.add('that_app', secrets)


        # View
        print('Showing you the vault to eyeball validation of .view():')
        self.vault.view()

        # Remove
        assert self.vault.remove('that_app')
        assert self.vault.remove('madeupapp') == False

