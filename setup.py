from setuptools import setup, find_packages

setup(
    name='pykeys',
    version='18.12.3',
    packages=find_packages(),
    install_requires=['cryptography'],
    author='Andre Guerra',
    author_email='agu3rra@gmail.com',
    description='pykeys: secure API keys use',
    long_description='Securely store and use your API keys.',
    url='https://github.com/agu3rra/pykeys/',
    license='MIT',
    keywords='encryption secure coding api key token secret'
)