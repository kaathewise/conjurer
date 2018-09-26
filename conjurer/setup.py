from setuptools import setup

setup(
    name='conjurer',
    version='0.1',
    py_modules=['conjurer'],
    install_requires=[
        'argon2',
        'Click',
        'pycryptodome',
    ],
    entry_points='''
        [console_scripts]
        conjurer=main:cli
    ''',
)
