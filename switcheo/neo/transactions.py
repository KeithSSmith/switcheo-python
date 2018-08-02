#
# switcheo/neo/transactions.py
# Keith Smith
#
# For testnet requests to the Switcheo exchange


from switcheo.utils import reverse_hex, num2hexstring, num2varint
from switcheo.Fixed8 import Fixed8, num2fixed8


max_transaction_attribute_size = 65535


def serialize_transaction(transaction, signed=True):
    serialized_txn = ''
    serialized_txn += str(num2hexstring(transaction['type']))
    serialized_txn += str(num2hexstring(transaction['version']))
    serialized_txn += str(serialize_exclusive[transaction['type']](transaction))
    serialized_txn += str(num2varint(len(transaction['attributes'])))
    for attribute in transaction['attributes']:
        serialized_txn += serialize_transaction_attribute(attribute)
    serialized_txn += str(num2varint(len(transaction['inputs'])))
    for txn_input in transaction['inputs']:
        serialized_txn += serialize_transaction_input(txn_input)
    serialized_txn += str(num2varint(len(transaction['outputs'])))
    for txn_output in transaction['outputs']:
        serialized_txn += serialize_transaction_output(txn_output)
    if signed and transaction['scripts'] and len(transaction['scripts']) > 0:
        serialized_txn += str(num2varint(len(transaction['scripts'])))
        for script in transaction['scripts']:
            serialized_txn += serialize_witness(script)
    return serialized_txn


def serialize_transaction_attribute(attr):
    if len(attr['data']) > max_transaction_attribute_size:
        exit()
    out = num2hexstring(attr['usage'])
    if attr['usage'] == 0x81:
        out += num2hexstring(len(attr['data']) / 2)
    elif attr['usage'] == 0x90 or attr['usage'] >= 0xf0:
        out += num2varint(len(attr['data']) / 2)
    if attr['usage'] == 0x02 or attr['usage'] == 0x03:
        out += attr['data'][2:64]
    else:
        out += attr['data']
    return out


def serialize_transaction_input(txn_input):
    return reverse_hex(txn_input['prevHash']) + reverse_hex(num2hexstring(txn_input['prevIndex'], 2))


def serialize_transaction_output(txn_output):
    value = Fixed8(float(txn_output['value'])).toReverseHex()
    return reverse_hex(txn_output['assetId']) + value + reverse_hex(txn_output['scriptHash'])


def serialize_witness(witness):
    invocation_len = num2varint(len(witness['invocationScript']) / 2)
    verification_len = num2varint(len(witness['verificationScript']) / 2)
    return invocation_len + witness['invocationScript'] + verification_len + witness['verificationScript']


def serialize_claim_exclusive(transaction):
    print("serialize claim exclusive")
    # pass


def serialize_contract_exclusive(transaction):
    if hex(transaction['type']) != 0x80:
        exit(4)
    return ''


def serialize_invocation_exclusive(transaction):
    if transaction['type'] != 0xd1:
        exit(4)
    out = num2varint(int(len(transaction['script'])/2))
    out += transaction['script']
    if transaction['version'] >= 1:
        out += num2fixed8(transaction['gas'])
    return out


serialize_exclusive = {
  2: serialize_claim_exclusive,
  128: serialize_contract_exclusive,
  209: serialize_invocation_exclusive
}
