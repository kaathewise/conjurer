import sys

from pseudorandom_source import get_source
from generators import *

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string(
    'passphrase',
    None,
    'Passphrase for generation. It is the main source of enthropy. (required)',
    short_name='p')
flags.mark_flag_as_required('passphrase')
flags.DEFINE_string(
    'id',
    '', 'Username, UserId, or any kind of virtual identity.'
    ' Used for generation, but also as the identity for certificates.',
    short_name='i')

flags.DEFINE_enum(
    'mode',
    None,
    modes.keys(),
    'The part of the identity that needs to be created. (required)\n' +
    "\n".join("%-15s: %s" % (k, v.__doc__) for k, v in modes.items()),
    short_name='m')
flags.mark_flag_as_required('mode')


def _main(argv):
    del argv  # Unused

    seedphrase = '%s$%s' % (FLAGS.passphrase, FLAGS.id)
    print(seedphrase)
    method = gpg.modes[FLAGS.gpg_mode]
    s = get_source(seedphrase)
    sys.stdout.buffer.write(method(s, sys.stdin.buffer))


if __name__ == '__main__':
    app.run(_main)
