Import Statements
^^^^^^^^^^^^^^^^^

Clients
"""""""

Import the desired Switcheo Clients into your project:

::

    from switcheo.authenticated_client import AuthenticatedClient
    from switcheo.public_client import PublicClient

Helpers
"""""""

There are also helper functions to help transform inputs and wallet addresses into the correct format.

::

    from switcheo.neo.utils import private_key_to_hex, neo_get_scripthash_from_private_key, neo_get_address_from_scripthash, open_wallet

3rd Party Helpers
"""""""""""""""""

Much of the underlying code relies on the ``neo-python-core`` package.  These can also be used as helper functions by importing them as follows:

::

    from neocore.KeyPair import KeyPair
    from neocore.Cryptography.Helper import scripthash_to_address
