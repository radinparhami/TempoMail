from setuptools import find_packages, setup

setup(
    name='TempoMail',
    packages=find_packages(include=['TempoMail']),
    version='1.0.0',
    description='python temp-mail liberary',
    author='Radin',
    install_requires=['requests'],
)
