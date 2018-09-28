from click.testing import CliRunner
from Crypto.Hash import SHA256

from .. import gpg
from conjurer.core.testing.fake_context import FakeContextProvider

fingerprint_generators = {}


def fingerprint(cmd):
    def decorator(f):
        def wrapped(source):
            result = f(source, CliRunner(), cmd)
            if result.exception:
                raise result.exception
            output = result.output
            if isinstance(output, str):
                output = output.encode('utf8')
            return SHA256.new(data=output).hexdigest()

        fingerprint_generators[cmd] = wrapped
        return wrapped

    return decorator


@fingerprint(gpg.pem)
def _gpg_pem(source, runner, cmd):
    return runner.invoke(cmd, obj=FakeContextProvider(source=source))


@fingerprint(gpg.key)
def _gpg_key(source, runner, cmd):
    return runner.invoke(
        cmd, obj=FakeContextProvider(source=source, user='You Know Who'))


@fingerprint(gpg.public)
def _gpg_public(source, runner, cmd):
    return runner.invoke(
        cmd, obj=FakeContextProvider(source=source, user='You Know Who'))
