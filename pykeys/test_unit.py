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
        self.vault = Vault()
        self.secrets = {'client_id':'123456',
                        'client_secret':'iveseenbetter'}

    def test_add(self):
        
        self.vault.add('that_app', self.secrets)
        self.vault.add('another_app', self.secrets)
        self.vault.add('yet_another_app', self.secrets)
        
        value = self.vault.get('that_app', 'client_secret')
        assert value == 'iveseenbetter'

    def test_invalid_ops(self):
        with pytest.raises(TypeError):
            self.vault.get(2,4)
            self.vault.add(4.2,4)
            self.vault.remove(1321)

        with pytest.raises(ValueError):
            self.vault.add('that_app', self.secrets)
            self.vault.add('that_app', self.secrets) # repeated app

    def test_retrive_undefined_app(self):
        value = self.vault.get('madeupapp','madeupitem')
        assert value is None

    def test_removal(self):
        self.vault.add('that_app', self.secrets)
        assert self.vault.remove('that_app')
        assert self.vault.remove('madeupapp') == False

    def test_master_key_update_ok(self):
        new_key = Fernet.generate_key()
        assert self.vault.replace_master_key(new_key)
    
    def test_master_key_update_fail(self):
        with pytest.raises(ValueError):
            new_key = 'invalidfernetkey'
            self.vault.replace_master_key(new_key)

    def teardown(self):
        self.vault.burn()