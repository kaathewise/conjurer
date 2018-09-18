import os
import subprocess
import sys
import tempfile

from absl import flags

FLAGS = flags.FLAGS


def get_pem(source, *args):
    """Generate an RSA pair and export it in PEM format."""
    return _get_key(source).export_key(format='PEM')


def get_gpg_key(source, *args):
    """Generate an RSA pair and export it in GPG format."""
    pem = get_pem(source)
    my_env = os.environ.copy()
    my_env['PEM2OPENPGP_TIMESTAMP'] = '0'
    my_env['PEM2OPENPGP_USAGE_FLAGS'] = 'certify,sign,encrypt,authenticate'
    user_id = FLAGS.id
    pem2openpgp = subprocess.Popen(['pem2openpgp', user_id],
                                   env=my_env,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
    return pem2openpgp.communicate(pem)[0]


def get_public_key(source, *args):
    """Generate an (RSA) GPG key and export the public key in ASCII."""
    return _run_gpg_with_source(source, None,
                                ['--armor', '--export', FLAGS.id])


def encrypt(source, buf):
    """Generate an (RSA) GPG key and use it to encrypt STDIN to STDOUT."""
    return _run_gpg_with_source(source, buf, [
        '--encrypt', '--recipient', FLAGS.id, '--trust-model', 'always',
        '--armor'
    ])


def decrypt(source, buf):
    """Generate an (RSA) GPG key and use it to decrypt STDIN to STDOUT."""
    return _run_gpg_with_source(source, buf, [
        '--decrypt', '--recipient', FLAGS.id, '--trust-model', 'always',
        '--armor'
    ])


def _get_key(random_source):
    from Crypto.PublicKey import RSA
    return RSA.generate(4096, random_source)


def _run_gpg_with_source(source, buf, cmd):
    gpg_key = get_gpg_key(source)
    inp = buf.read() if buf else None
    with tempfile.TemporaryDirectory() as tmpdirname:
        subprocess.run(['gpg', '--homedir', tmpdirname, '--import'],
                       input=gpg_key,
                       check=True)
        gpg = subprocess.Popen(
            ['gpg', '--homedir', tmpdirname] + cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        return gpg.communicate(inp)[0]
