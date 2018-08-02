#
# switcheo/neo/utils.py
# Keith Smith
#
# For testnet requests to the Switcheo exchange

import math
import binascii
import base58
from neocore.Cryptography.Crypto import Crypto
from neocore.KeyPair import KeyPair
from switcheo.utils import stringify_message, reverse_hex
from switcheo.neo.transactions import serialize_transaction


def sign_message(encoded_message, private_key_hex):
    return Crypto.Sign(message=encoded_message.strip(), private_key=private_key_hex).hex()


def sign_transaction(transaction, private_key_hex):
    serialized_transaction = serialize_transaction(transaction=transaction, signed=False)
    return sign_message(encoded_message=serialized_transaction, private_key_hex=private_key_hex)


def encode_message(message):
    message_hex = binascii.hexlify(stringify_message(message).encode('utf-8')).decode()
    message_hex_length = hex(int(len(message_hex) / 2))[2:]
    return '010001f0' + message_hex_length + message_hex + '0000'


def to_neo_asset_amount(amount):
    return "{:.0f}".format(amount * math.pow(10, 8))


def private_key_to_hex(key_pair):
    return bytes(key_pair.PrivateKey).hex()


def neo_get_address_from_scripthash(address):
    """
    Core methods for manipulating keys
    NEP2 <=> WIF <=> Private => Public => ScriptHash <=> Address
    Keys are arranged in order of derivation.
    Arrows determine the direction.
    """
    hex58_substring = base58.b58decode(v=address).hex()[2:42]
    return reverse_hex(hex58_substring)


def neo_get_public_key_from_private_key(private_key):
    kp = KeyPair(priv_key=private_key)
    return kp.PublicKey


def neo_get_scripthash_from_private_key(private_key):
    script = b'21' + neo_get_public_key_from_private_key(private_key).encode_point(True) + b'ac'
    return Crypto.ToScriptHash(data=script)
