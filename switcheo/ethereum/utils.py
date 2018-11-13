import binascii
from eth_account.account import Account


def sign_txn_array(messages, private_key):
    message_dict = {}
    for message in messages:
        signed_message =\
            binascii.hexlify(Account.signHash(message['txn']['sha256'], private_key=private_key)['signature']).decode()
        message_dict[message['id']] = '0x' + signed_message
    return message_dict
