import unittest
from switcheo.neo.transactions import serialize_transaction, serialize_transaction_attribute,\
    serialize_transaction_input, serialize_transaction_output, serialize_witness, serialize_claim_exclusive,\
    serialize_contract_exclusive, serialize_invocation_exclusive


transaction_dict = {'hash': '72b74c96b9174e9b9e1b216f7e8f21a6475e6541876a62614df7c1998c6e8376',
                    'sha256': '2109cbb5eea67a06f5dd8663e10fcd1128e28df5721a25d993e05fe2097c34f3',
                    'type': 209,
                    'version': 1,
                    'attributes': [{'usage': 32, 'data': '592c8a46a0d06c600f06c994d1f25e7283b8a2fe'},
                                   {'usage': 32, 'data': '6a3d9b359fc17d711017daa6c0e14d6172a791ed'}],
                    'inputs': [{'prevHash': 'f09b3b697c580d1730cd360da5e1f0beeae00827eb2f0055cbc85a5a4dadd8ea', 'prevIndex': 0},
                               {'prevHash': 'c858e4d2af1e1525fa974fb2b1678caca1f81a5056513f922789594939ff713d', 'prevIndex': 31}],
                    'outputs': [{'assetId': '602c79718b16e442de58778e148d0b1084e3b2dffd5de6b7b16cee7969282de7', 'scriptHash': 'e707714512577b42f9a011f8b870625429f93573', 'value': 1e-08}],
                    'scripts': [],
                    'script': '0800e1f505000000001432e125258b7db0a0dffde5bd03b2b859253538ab14592c8a46a0d06c600f06c994d1f25e7283b8a2fe53c1076465706f73697467823b63e7c70a795a7615a38d1ba67d9e54c195a1',
                    'gas': 0}


class TestTransactions(unittest.TestCase):

    def test_serialize_transaction(self):
        serialized_transaction = 'd101520800e1f505000000001432e125258b7db0a0dffde5bd03b2b859253538ab14592c8a46a0d06c600f06c994d1f25e7283b8a2fe53c1076465706f73697467823b63e7c70a795a7615a38d1ba67d9e54c195a100000000000000000220592c8a46a0d06c600f06c994d1f25e7283b8a2fe206a3d9b359fc17d711017daa6c0e14d6172a791ed02ead8ad4d5a5ac8cb55002feb2708e0eabef0e1a50d36cd30170d587c693b9bf000003d71ff3949598927923f5156501af8a1ac8c67b1b24f97fa25151eafd2e458c81f0001e72d286979ee6cb1b7e65dfddfb2e384100b8d148e7758de42e4168b71792c6001000000000000007335f929546270b8f811a0f9427b5712457107e7'
        self.assertEqual(serialize_transaction(transaction=transaction_dict, signed=False), serialized_transaction)

    def test_serialize_transaction_attribute(self):
        serialized_attributes = []
        serialized_attribute_expected_list = ['20592c8a46a0d06c600f06c994d1f25e7283b8a2fe',
                                              '206a3d9b359fc17d711017daa6c0e14d6172a791ed']
        for attribute in transaction_dict['attributes']:
            serialized_attributes.append(serialize_transaction_attribute(attr=attribute))
        self.assertListEqual(serialized_attributes, serialized_attribute_expected_list)

    def test_serialize_transaction_input(self):
        serialized_inputs = []
        serialized_input_expected_list = ['ead8ad4d5a5ac8cb55002feb2708e0eabef0e1a50d36cd30170d587c693b9bf00000',
                                          '3d71ff3949598927923f5156501af8a1ac8c67b1b24f97fa25151eafd2e458c81f00']
        for txn_input in transaction_dict['inputs']:
            serialized_inputs.append(serialize_transaction_input(txn_input=txn_input))
        self.assertListEqual(serialized_inputs, serialized_input_expected_list)

    def test_serialize_transaction_output(self):
        serialized_outputs = []
        serialized_output_expected_list = ['e72d286979ee6cb1b7e65dfddfb2e384100b8d148e7758de42e4168b71792c6001000000000000007335f929546270b8f811a0f9427b5712457107e7']
        for txn_output in transaction_dict['outputs']:
            serialized_outputs.append(serialize_transaction_output(txn_output=txn_output))
        self.assertListEqual(serialized_outputs, serialized_output_expected_list)

    def test_serialize_witness(self):
        # This is not used by Switcheo and I can't find a good test transaction for this, will pass for now.
        pass

    def test_serialize_claim_exclusive(self):
        with self.assertRaises(ValueError):
            serialize_claim_exclusive(transaction=transaction_dict)
        # Switcheo will not be allowing for GAS claims so this should never be necessary.
        # transaction_claim_dict = transaction_dict.copy()
        # transaction_claim_dict['type'] = 2
        # self.assertEqual(serialize_claim_exclusive(transaction=transaction_claim_dict), '')

    def test_serialize_contract_exclusive(self):
        with self.assertRaises(ValueError):
            serialize_contract_exclusive(transaction=transaction_dict)
        transaction_contract_dict = transaction_dict.copy()
        transaction_contract_dict['type'] = 128
        self.assertEqual(serialize_contract_exclusive(transaction=transaction_contract_dict), '')

    def test_serialize_invocation_exclusive(self):
        serialized_invocation = '520800e1f505000000001432e125258b7db0a0dffde5bd03b2b859253538ab14592c8a46a0d06c600f06c994d1f25e7283b8a2fe53c1076465706f73697467823b63e7c70a795a7615a38d1ba67d9e54c195a10000000000000000'
        self.assertEqual(serialize_invocation_exclusive(transaction=transaction_dict), serialized_invocation)
        transaction_invocation_dict = transaction_dict.copy()
        transaction_invocation_dict['type'] = 128
        with self.assertRaises(ValueError):
            serialize_invocation_exclusive(transaction=transaction_invocation_dict)
