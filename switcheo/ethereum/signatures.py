# -*- coding:utf-8 -*-
"""
Description:
    Functions for signing data to send to the Switcheo API by using Ethereum Utilities to cryptographically sign
    data that gets authenticated on the Ethereum network.
Usage:
    from switcheo.ethereum.signatures import <function_name>
"""

import binascii
from switcheo.utils import stringify_message
from switcheo.ethereum.utils import sign_txn_array
from eth_utils import to_checksum_address, to_normalized_address
from eth_account.messages import defunct_hash_message
from eth_account.account import Account
from web3 import Web3, HTTPProvider


def sign_create_cancellation(cancellation_params, private_key):
    """
    Function to sign the parameters required to create a cancellation request from the Switcheo Exchange.
    Execution of this function is as follows::

        sign_create_cancellation(cancellation_params=signable_params, private_key=eth_private_key)

    The expected return result for this function is as follows::

        {
            'order_id': '3125550a-04f9-4475-808b-42b5f89d6693',
            'timestamp': 1542088842108,
            'address': '0x32c46323b51c977814e05ef5e258ee4da0e4c3c3',
            'signature': 'dac70ca711bcfbeefbdead2158ef8b15fab1a1....'
        }

    :param cancellation_params: Dictionary with Order ID and timestamp to sign for creating the cancellation.
    :type cancellation_params: dict
    :param private_key: The Ethereum private key to sign the deposit parameters.
    :type private_key: str
    :return: Dictionary of signed message to send to the Switcheo API.
    """
    hash_message = defunct_hash_message(text=stringify_message(cancellation_params))
    hex_message = binascii.hexlify(hash_message).decode()
    signed_message = binascii.hexlify(Account.signHash(hex_message, private_key=private_key)['signature']).decode()
    create_params = cancellation_params.copy()
    create_params['address'] = to_normalized_address(Account.privateKeyToAccount(private_key=private_key).address)
    create_params['signature'] = signed_message
    return create_params


def sign_execute_cancellation(cancellation_params, private_key):
    """
    Function to sign the parameters required to execute a cancellation request on the Switcheo Exchange.
    Execution of this function is as follows::

        sign_execute_cancellation(cancellation_params=signable_params, private_key=eth_private_key)

    The expected return result for this function is as follows::

        {
            'signature': '0x65986ed2cb631d4999ce8b9c895a43f....'
        }

    :param cancellation_params: Parameters the Switcheo Exchange returns from the create cancellation.
    :type cancellation_params: dict
    :param private_key: The Ethereum private key to sign the deposit parameters.
    :type private_key: str
    :return: Dictionary of signed message to send to the Switcheo API.
    """
    cancellation_sha256 = cancellation_params['transaction']['sha256']
    signed_sha256 = binascii.hexlify(
        Account.signHash(cancellation_sha256, private_key=private_key)['signature']).decode()
    return {'signature': '0x' + signed_sha256}


def sign_create_deposit(deposit_params, private_key):
    """
    Function to sign the deposit parameters required by the Switcheo API.
    Execution of this function is as follows::

        sign_create_deposit(deposit_params=signable_params, private_key=eth_private_key)

    The expected return result for this function is as follows::

        {
            'blockchain': 'eth',
            'asset_id': 'ETH',
            'amount': '10000000000000000',
            'timestamp': 1542089346249,
            'contract_hash': '0x607af5164d95bd293dbe2b994c7d8aef6bec03bf',
            'address': '0x32c46323b51c977814e05ef5e258ee4da0e4c3c3',
            'signature': 'd4b8491d6514bff28b9f2caa440f51a93f31d....'
        }

    :param deposit_params: Parameters needed to deposit to the Switcheo API and signed in this function.
    :type deposit_params: dict
    :param private_key: The Ethereum private key to sign the deposit parameters.
    :type private_key: str
    :return: Dictionary of signed message to send to the Switcheo API.
    """
    hash_message = defunct_hash_message(text=stringify_message(deposit_params))
    hex_message = binascii.hexlify(hash_message).decode()
    signed_message = binascii.hexlify(Account.signHash(hex_message, private_key=private_key)['signature']).decode()
    create_params = deposit_params.copy()
    create_params['address'] = to_normalized_address(Account.privateKeyToAccount(private_key=private_key).address)
    create_params['signature'] = signed_message
    return create_params


def sign_execute_deposit(deposit_params, private_key, infura_url):
    """
    Function to execute the deposit request by signing the transaction generated from the create deposit function.
    Execution of this function is as follows::

        sign_execute_deposit(deposit_params=create_deposit, private_key=eth_private_key)

    The expected return result for this function is as follows::

        {
            'transaction_hash': '0xcf3ea5d1821544e1686fbcb1f49d423b9ea9f42772ff9ecdaf615616d780fa75'
        }

    :param deposit_params: The parameters generated by the create function that now requires a signature.
    :type deposit_params: dict
    :param private_key: The Ethereum private key to sign the deposit parameters.
    :type private_key: str
    :param infura_url: The URL used to broadcast the deposit transaction to the Ethereum network.
    :type infura_url: str
    :return: Dictionary of the signed transaction to initiate the deposit of ETH via the Switcheo API.
    """
    create_deposit_upper = deposit_params.copy()
    create_deposit_upper['transaction']['from'] = to_checksum_address(create_deposit_upper['transaction']['from'])
    create_deposit_upper['transaction']['to'] = to_checksum_address(create_deposit_upper['transaction']['to'])
    create_deposit_upper['transaction'].pop('sha256')
    signed_create_txn = Account.signTransaction(create_deposit_upper['transaction'], private_key=private_key)
    execute_signed_txn = binascii.hexlify(signed_create_txn['hash']).decode()

    # Broadcast transaction to Ethereum Network.
    Web3(HTTPProvider(infura_url)).eth.sendRawTransaction(signed_create_txn.rawTransaction)

    return {'transaction_hash': '0x' + execute_signed_txn}


def sign_create_order(order_params, private_key):
    """
    Function to sign the create order parameters and send to the Switcheo API.
    Execution of this function is as follows::

        sign_create_order(order_params=signable_params, private_key=eth_private_key)

    The expected return result for this function is as follows::

        {
            'blockchain': 'eth',
            'pair': 'JRC_ETH',
            'side': 'buy',
            'price': '0.00000003',
            'want_amount': '3350000000000000000000000',
            'use_native_tokens': False,
            'order_type': 'limit',
            'timestamp': 1542089785915,
            'contract_hash': '0x607af5164d95bd293dbe2b994c7d8aef6bec03bf',
            'signature': '536306a2f2aee499ffd6584027029ee585293b3686....',
            'address': '0x32c46323b51c977814e05ef5e258ee4da0e4c3c3'
        }

    :param order_params: Parameters to create an order to be submitted to the Switcheo Order Book.
    :type order_params: dict
    :param private_key: The Ethereum private key to sign the deposit parameters.
    :type private_key: str
    :return: Dictionary of signed message to send to the Switcheo API.
    """
    hash_message = defunct_hash_message(text=stringify_message(order_params))
    hex_message = binascii.hexlify(hash_message).decode()
    create_params = order_params.copy()
    signed_message = binascii.hexlify(Account.signHash(hex_message, private_key=private_key)['signature']).decode()
    create_params['signature'] = signed_message
    create_params['address'] = to_normalized_address(Account.privateKeyToAccount(private_key=private_key).address)
    return create_params


def sign_execute_order(order_params, private_key):
    """
    Function to execute the order request by signing the transaction generated from the create order function.
    Execution of this function is as follows::

        sign_execute_order(order_params=signable_params, private_key=eth_private_key)

    The expected return result for this function is as follows::

        {
            'signatures': {
                'fill_groups': {},
                'fills': {},
                'makes': {
                    '392cd607-27ed-4702-880d-eab8d67a4201': '0x5f62c585e0978454cc89aa3b86d3ea6afbd80fc521....'
                }
            }
        }

    :param order_params: The parameters generated by the create function that now require signing.
    :type order_params: dict
    :param private_key: The Ethereum private key to sign the deposit parameters.
    :type private_key: str
    :return: Dictionary of the signed transaction to place an order on the Switcheo Order Book.
    """
    execute_params = {
        'signatures': {
            'fill_groups': sign_txn_array(messages=order_params['fill_groups'], private_key=private_key),
            'fills': {},
            'makes': sign_txn_array(messages=order_params['makes'], private_key=private_key),
        }
    }
    return execute_params


def sign_create_withdrawal(withdrawal_params, private_key):
    """
    Function to create a withdrawal from the Switcheo Smart Contract.
    Execution of this function is as follows::

        sign_create_withdrawal(withdrawal_params=signable_params, private_key=eth_private_key)

    The expected return result for this function is as follows::

        {
            'blockchain': 'eth',
            'asset_id': 'ETH',
            'amount': '10000000000000000',
            'timestamp': 1542090476102,
            'contract_hash': '0x607af5164d95bd293dbe2b994c7d8aef6bec03bf',
            'address': '0x32c46323b51c977814e05ef5e258ee4da0e4c3c3',
            'signature': '375ddce62e5b3676d5e94ebb9f9a8af5963b....'
        }

    :param withdrawal_params: The parameters to be signed and create a withdraw from Switcheo.
    :type withdrawal_params: dict
    :param private_key: The Ethereum private key to sign the deposit parameters.
    :type private_key: str
    :return: Dictionary of the signed transaction to initiate the withdrawal of ETH via the Switcheo API.
    """
    hash_message = defunct_hash_message(text=stringify_message(withdrawal_params))
    hex_message = binascii.hexlify(hash_message).decode()
    signed_message = binascii.hexlify(Account.signHash(hex_message, private_key=private_key)['signature']).decode()
    create_params = withdrawal_params.copy()
    create_params['address'] = to_normalized_address(Account.privateKeyToAccount(private_key=private_key).address)
    create_params['signature'] = signed_message
    return create_params


def sign_execute_withdrawal(withdrawal_params, private_key):
    """
    Function to execute the withdrawal request by signing the transaction generated from the create withdrawal function.
    Execution of this function is as follows::

        sign_execute_withdrawal(withdrawal_params=signable_params, private_key=eth_private_key)

    The expected return result for this function is as follows::

        {
            'signature': '0x33656f88b364d344e5b04f6aead01cdd3ac084489c39a9efe88c9873249bf1954525b1....'
        }

    :param withdrawal_params: The parameters generated by the create function that now require signing.
    :type withdrawal_params: dict
    :param private_key: The Ethereum private key to sign the deposit parameters.
    :type private_key: str
    :return: Dictionary of the signed transaction hash and initiate the withdrawal of ETH via the Switcheo API.
    """
    withdrawal_sha256 = withdrawal_params['transaction']['sha256']
    signed_sha256 = binascii.hexlify(Account.signHash(withdrawal_sha256, private_key=private_key)['signature']).decode()
    return {'signature': '0x' + signed_sha256}
