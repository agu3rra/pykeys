# pykeys: Securely store and use your API keys

The purpose of this package is to offer a secure way to store and retrieve API tokens when interacting with such interfaces in Python code. Once you register a key in the vault you can reuse it in any of your Python programs. All keys are encrypted and stored in the library's install path.

It uses Python's `criptography` library to encrypt all token values that are stored in the local vault.

## Use example
```Python
>>> import pykeys as pk
>>> vault = pk.vault()
"""
This is a brand new vault. Please select one of the options below:
1. Generate new key.
2. Enter an existing Fernet key you wish to use.
"""
>>> 1
"""
This is your vault key. Take note of it if you ever wish to reuse it in a different vault.
Key: dasdsad2dded==
"""
>>> app = 'Google API'
>>> secrets = {'token':'13213-DSdSD3-3e2Sad3ad'}
>>> vault.add(app, secrets)
"""
The new token has been added to the vault.
"""
>>> vault.view()
>>> vault.get(app='Google API',entry='token')
'13213-DSdSD3-3e2Sad3ad'
```

## Install
```bash
$ pip install pykeys
```
