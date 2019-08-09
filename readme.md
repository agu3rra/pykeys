[![Known Vulnerabilities](https://snyk.io//test/github/agu3rra/pykeys/badge.svg?targetFile=requirements.txt)](https://snyk.io//test/github/agu3rra/pykeys?targetFile=requirements.txt)
# pykeys: Securely store and use your API keys

The purpose of this package is to offer a secure way to store and retrieve API tokens when interacting with such interfaces in Python code. Once you register a key in the vault you can reuse it in any of your Python programs. All keys are encrypted and stored in the library's install path.

It uses Python's `criptography` library to encrypt all token values that are stored in the local vault.

## Use example
```Python
>>> import pykeys as pk
>>> app='Google API'
>>> secrets={'token':'mysupersecrettoken'}
>>> pk.add(app,secrets)
>>> pk.view()
{
    "Google API": {
        "token": "gAAAAABcFPOMUOyFhnchp6u6j8v0J7lzcY_0ZtCdgrToHpv2Vtsr44Lb9BRDfoMWuNXQNbnBiXIBxYsHjXRAkyuf9VJYZbR_E7tY1AeKjpYglpk0NSC_NN0="
    }
}
>>> pk.get('Google API', 'token')
'mysupersecrettoken'
```

Subsequent code executions can use the previously saved tokens:
```Python
>>> import pykeys as pk
>>> pk.view()
{
    "Google API": {
        "token": "gAAAAABcFPyihLHc4NuJk2SymYcmTZgGO0gHeSjEbDWy6GugrlTHJ7o0kjQ6tduHdHsSuquD0lgGlRQij02f47uYCyvWEfBE4o2j5KV5yP7t3qCADl-Ou9o="
    }
}
```

PS: this is what a Fernet key looks like: `7MHyRPCy5TrVwYsKULvCMzUe5ha9-34ZaPTcw98PxyE=`

## Install
```bash
$ pip install pykeys
```
