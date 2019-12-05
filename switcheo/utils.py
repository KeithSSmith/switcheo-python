#
# switcheo/utils.py
# Keith Smith
#
# For testnet requests to the Switcheo exchange

import json
import requests
import time
import hashlib


def get_epoch_milliseconds():
    return int(round(time.time() * 1000))


def stringify_message(message):
    """Return a JSON message that is alphabetically sorted by the key name

    Args:
        message
    """
    return json.dumps(message, sort_keys=True, separators=(',', ':'))


def sha1_hash_digest(message):
    """
    Converts Stringified (JavaScript) JSON to a SHA-1 Hash.

    Args:
        message
    """
    return hashlib.sha1(message.encode()).hexdigest()


def reverse_hex(message):
    return "".join([message[x:x + 2] for x in range(0, len(message), 2)][::-1])


def num2hexstring(number, size=1, little_endian=False):
    """
    Converts a number to a big endian hexstring of a suitable size, optionally little endian
    :param {number} number
    :param {number} size - The required size in hex chars, eg 2 for Uint8, 4 for Uint16. Defaults to 2.
    :param {boolean} little_endian - Encode the hex in little endian form
    :return {string}
    """
    # if (type(number) != = 'number') throw new Error('num must be numeric')
    # if (num < 0) throw new RangeError('num is unsigned (>= 0)')
    # if (size % 1 !== 0) throw new Error('size must be a whole integer')
    # if (!Number.isSafeInteger(num)) throw new RangeError(`num (${num}) must be a safe integer`)
    size = size * 2
    hexstring = hex(number)[2:]
    if len(hexstring) % size != 0:
        hexstring = ('0' * size + hexstring)[len(hexstring):]
    if little_endian:
        hexstring = reverse_hex(hexstring)
    return hexstring


def num2varint(num):
    """
    Converts a number to a variable length Int. Used for array length header

    :param: {number} num - The number
    :return: {string} hexstring of the variable Int.
    """
    # if (typeof num !== 'number') throw new Error('VarInt must be numeric')
    # if (num < 0) throw new RangeError('VarInts are unsigned (> 0)')
    # if (!Number.isSafeInteger(num)) throw new RangeError('VarInt must be a safe integer')
    if num < 0xfd:
        return num2hexstring(num)
    elif num <= 0xffff:
        # uint16
        return 'fd' + num2hexstring(number=num, size=2, little_endian=True)
    elif num <= 0xffffffff:
        # uint32
        return 'fe' + num2hexstring(number=num, size=4, little_endian=True)
    else:
        # uint64
        return 'ff' + num2hexstring(number=num, size=8, little_endian=True)


def current_contract_hash(contracts):
    contract_dict = {}
    for chain in contracts:
        max_key = 1
        for key in contracts[chain].keys():
            if float(key[1:].replace('_', '.')) > max_key:
                max_key = float(key[1:].replace('_', '.'))
        max_key_str = 'V' + str(max_key).replace('.', '_').replace('_0', '')
        contract_dict[chain] = contracts[chain][max_key_str]
    return contract_dict


def current_contract_version(contract, contracts):
    contract_dict = {}
    for chain in contracts:
        for key in contracts[chain].keys():
            contract_hash = contracts[chain][key]
            contract_dict[contract_hash] = key
    return contract_dict[contract]


class SwitcheoApiException(Exception):

    def __init__(self, error_code, error_message, error):
        super(SwitcheoApiException, self).__init__(error_message)
        self.error_code = error_code
        self.error = error
        

class Request(object):

    def __init__(self, api_url='https://test-api.switcheo.network/', api_version="/v2", timeout=30):
        self.base_url = api_url.rstrip('/')
        self.url = self.base_url + api_version
        self.timeout = timeout

    def get(self, path, params=None):
        """Perform GET request"""
        r = requests.get(url=self.url + path, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def post(self, path, data=None, json_data=None, params=None):
        """Perform POST request"""
        r = requests.post(url=self.url + path, data=data, json=json_data, params=params, timeout=self.timeout)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            raise SwitcheoApiException(r.json().get('error_code'), r.json().get('error_message'), r.json().get('error'))
        return r.json()

    def status(self):
        r = requests.get(url=self.base_url)
        r.raise_for_status()
        return r.json()
