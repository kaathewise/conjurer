from . import gpg

from collections import OrderedDict

modes = OrderedDict([('gpg-pem', gpg.get_pem), ('gpg-key', gpg.get_gpg_key),
                     ('gpg-public', gpg.get_public_key),
                     ('gpg-encrypt', gpg.encrypt), ('gpg-decrypt',
                                                    gpg.decrypt)])
