from pseudorandom_source import get_source
from generators import gpg

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string(
    'seed',
    None,
    'Passphrase for generation. It is the main source of enthropy.',
    short_name='s')
flags.mark_flag_as_required('seed')
flags.DEFINE_string(
    'id', '', 'Username, UserId, or any kind of virtual identity.'
    ' Used for generation, but also as the identity for certificates.')


def _main(argv):
    del argv  # Unused

    seedphrase = '%s$%s' % (FLAGS.seed, FLAGS.id)
    s = get_source(seedphrase)
    gpg.generate(s)


if __name__ == '__main__':
    app.run(_main)
