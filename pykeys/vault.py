import os
import json
from cryptography.fernet import Fernet
from .encryption import Encryption
from pkg_resources import resource_filename

class Vault():

    def __init__(self):
        self.master_key_file = resource_filename('pykeys', 'master_key.json')
        self.keys_file = resource_filename('pykeys', 'keys.json')
        self.master_key = self._check_master_key()
        self.vault = self._read_persistent_vault()

    def _check_master_key(self):
        """Verifies if there's already a master key"""
        if os.path.exists(self.master_key_file):
            # read master key from file and return it
            with open(self.master_key_file) as file_handler:
                data = json.load(file_handler)
                key = data['key']
            print('Master key read from file.')
            return key

        else: # we need a new master key
            selection = self._key_selection()
            if selection == 1: # autogenerate key
                key = Fernet.generate_key()
                key = key.decode('utf-8')
            elif selection == 2: # get key from user
                key = input('Please enter the master encryption key: ')
            else:
                raise ValueError('Invalid selection.')
            
            # store key and return it
            data = {'key': key}
            with open(self.master_key_file, 'w') as file_handler:
                file_handler.write(json.dumps(data))
            return key

    def _key_selection(self):
        """Asks the user for a valid option"""
        valid_options = {1: '1. Generate master key.',
                         2: '2. Provide existing Fernet key.'}
        while True:
            print('Please select one of the options below:')
            for _, value in valid_options.items():
                print(value)
            user_selection = input()
            user_selection = int(user_selection)
            if user_selection in valid_options.keys():
                return user_selection

    def _read_persistent_vault(self):
        """Returns existing data in the keys file."""
        if os.path.exists(self.keys_file):
            with open(self.keys_file) as file_handler:
                data = json.load(file_handler)
            return data
        else: # create empty
            with open(self.keys_file, 'w') as file_handler:
                data = {}
                file_handler.write(json.dumps(data))
            return data


    def _update_persistent_vault(self):
        """Overwrites data in the keys file with vault's instance values."""
        with open(self.keys_file, 'w') as file_handler:
            file_handler.write(json.dumps(self.vault))

    def burn(self):
        """Deletes master key and keys file. Package returns to install state.
        """
        os.remove(self.master_key_file)
        os.remove(self.keys_file)
        print('package master key and keys files deleted from disk.')
        print('Please create a new vault instance as this one became useless.')

    def view(self):
        """Prints encrypted values stored in disk."""
        print(json.dumps(self.vault, indent=4))

    def add(self, app, secrets):
        """
        Encrypts secrets and adds them under a new application.

        :param app: (str) name of the app to add.
        :param secrets: (dict) a Python dictionary containing all key, value
                        pairs to store.

        Example:
        secrets = {'client_id':'123456',
                   'client_secret':'iveseenbetter'}
        vault.add('that_app', secrets)
        """
        if type(app) != str or type(secrets) != dict:
            raise TypeError('Unexpected parameter type.')

        if app in self.vault.keys():
            raise ValueError('This app already exists. Pick a different name.')

        # Encrypt secrets and store added values
        encrypted_secrets = {}
        for key, value in secrets.items():
            cript = Encryption(self.master_key)
            encrypted_secrets[key] = cript.encrypt(value)
        self.vault.update({app: encrypted_secrets})
        self._update_persistent_vault()

    def remove(self, app):
        """Removes and app entry from the vault. Returns True if value was 
        removed and False otherwise (pehaps item or app don't exist.)
        
        :param app: (str) name of the app entry to remove.
                    You can view existing entries by using vault.view()
        """
        if type(app) != str: raise TypeError('Unexpected app value.')
        if app in self.vault.keys():
            self.vault.pop(app, None)
            self._update_persistent_vault()
            print('App removed from the vault.')
            return True
        else:
            print('No app by that name found in the vault. No action taken.')
            return False

    def get(self, app, item):
        """
        Return the decrypted value of an item in the vault.

        :param app: (str) name of the app in the vault.
        :param item: (str) item identifier in the vault.
        """
        if type(app) != str or type(item) != str:
            raise TypeError('Invalid types.')

        if app not in self.vault.keys():
            print('App not found. No value returned.')
            return None

        items = self.vault[app]
        if item not in items.keys():
            print('Item not registered for this app. No value returned.')
            return None

        cripto = Encryption(self.master_key)
        return cripto.decrypt(self.vault[app][item])