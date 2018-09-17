import os
import subprocess
import sys
import tempfile

from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_enum(
    'gpg_mode', 'pem', ['pem', 'gpg', 'decrypt', 'encrypt'],
    '''The way generated GPG is used:
    pem -- is exported in PEM format
    encrypt -- used to encrypt STDIN
    decrypt -- used to decrypt STDIN''')

_modes = {
    'pem': _get_pem,
    'gpg': _get_gpg,
    'decrypt': lambda key: _run_gpg_with_key(key, '--decrypt'),
    'encrypt': lambda key: _run_gpg_with_key(key, '--encrypt')
}


def generate(random_source):
    from Crypto.PublicKey import RSA
    key = RSA.generate(4096, random_source)
    return _modes[FLAGS.gpg_mode](key)


def _get_pem(key):
    return key.export_key(format='PEM')


def _get_gpg(key):
    pem = _get_pem(key)
    my_env = os.environ.copy()
    my_env['PEM2OPENPGP_TIMESTAMP'] = '0'
    my_env['PEM2OPENPGP_USAGE_FLAGS'] = 'certify,sign,encrypt,authenticate'
    user_id = FLAGS.id
    pem2openpgp = subprocess.Popen(['pem2openpgp', user_id],
                                   env=my_env,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
    return pem2openpgp.communicate(pem)[0]


def _run_gpg_with_key(key, cmd):
    gpg_key = _get_gpg(key)
    with tempfile.TemporaryDirectory() as tmpdirname:
        gpg_import = subprocess.Popen(
            ['gpg', '--homedir', tmpdirname, '--import'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        gpg_import.communicate(gpg_key)
        gpg_decrypt = subprocess.Popen([
            'gpg', '--homedir', tmpdirname, cmd, '--recipient', FLAGS.id,
            '--trust-model', 'always', '--armor'
        ],
                                       stdin=sys.stdin,
                                       stdout=sys.stdout)
        gpg_decrypt.communicate()
    return b''
