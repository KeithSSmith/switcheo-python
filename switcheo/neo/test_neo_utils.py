import unittest
from switcheo.neo.utils import create_offer_hash, encode_message, to_neo_asset_amount, private_key_to_hex, open_wallet,\
    neo_get_scripthash_from_address, neo_get_address_from_scripthash, neo_get_scripthash_from_private_key,\
    neo_get_public_key_from_private_key, sign_message, sign_transaction, sign_txn_array
from neocore.KeyPair import KeyPair


testnet_privatekey = b'p\xf6B\x89K\xc7=\xc5\x00\x13\xbem\x1d\xbe\x19\x8fC#~\xaf\x94X\xd1\x93\xc0\xb4\x16\xc58]\x97\x17'
kp = KeyPair(priv_key=testnet_privatekey)
testnet_privatekey_hexstring = '70f642894bc73dc50013be6d1dbe198f43237eaf9458d193c0b416c5385d9717'
testnet_scripthash = 'fea2b883725ef2d194c9060f606cd0a0468a2c59'
testnet_scripthash_uint160 = neo_get_scripthash_from_private_key(private_key=testnet_privatekey)
testnet_address = 'APuP9GsSCPJKrexPe49afDV8CQYubZGWd8'
testnet_publickey = '303231353534363535356234326164643737343933636332316462356461396639376163646666343966346433653739633239666363303361303661356539373662'

message = 'This is a test.'
encoded_message = '010001f0112254686973206973206120746573742e220000'
json_message = {"name": "John Smith", "age": 27, "siblings": ["Jane", "Joe"]}
json_encoded_message = '010001f0387b22616765223a32372c226e616d65223a224a6f686e20536d697468222c227369626c696e6773223a5b224a616e65222c224a6f65225d7d0000'

transaction_dict = {'hash': '72b74c96b9174e9b9e1b216f7e8f21a6475e6541876a62614df7c1998c6e8376',
                    'sha256': '2109cbb5eea67a06f5dd8663e10fcd1128e28df5721a25d993e05fe2097c34f3',
                    'type': 209,
                    'version': 1,
                    'attributes': [{'usage': 32, 'data': '592c8a46a0d06c600f06c994d1f25e7283b8a2fe'}],
                    'inputs': [{'prevHash': 'f09b3b697c580d1730cd360da5e1f0beeae00827eb2f0055cbc85a5a4dadd8ea', 'prevIndex': 0},
                               {'prevHash': 'c858e4d2af1e1525fa974fb2b1678caca1f81a5056513f922789594939ff713d', 'prevIndex': 31}],
                    'outputs': [{'assetId': '602c79718b16e442de58778e148d0b1084e3b2dffd5de6b7b16cee7969282de7', 'scriptHash': 'e707714512577b42f9a011f8b870625429f93573', 'value': 1e-08}],
                    'scripts': [],
                    'script': '0800e1f505000000001432e125258b7db0a0dffde5bd03b2b859253538ab14592c8a46a0d06c600f06c994d1f25e7283b8a2fe53c1076465706f73697467823b63e7c70a795a7615a38d1ba67d9e54c195a1',
                    'gas': 0}

transaction_array = [{
                        'id': 'e30a7fdf-779c-4623-8f92-8a961450d843',
                        'offer_hash': None,
                        'available_amount': None,
                        'offer_asset_id': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
                        'offer_amount': '2000000',
                        'want_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                        'want_amount': '10000000000',
                        'filled_amount': None,
                        'txn': {
                            'offerHash': 'b45ddfb97ade5e0363d9e707dac9ad1c530448db263e86494225a0025006f968',
                            'hash': '5c4cb1e73b9f2e608b6e768e0654649a4d15e08a7fe63fc536c454fa563a2f0f',
                            'sha256': 'f0b70640627947584a2976edeb055a124ae85594db76453532b893c05618e6ca',
                            'invoke': {
                                'scriptHash': 'a195c1549e7da61b8da315765a790ac7e7633b82',
                                'operation': 'makeOffer',
                                'args': [
                                    '592c8a46a0d06c600f06c994d1f25e7283b8a2fe',
                                    '9b7cffdaa674beae0f930ebe6085af9093e5fe56b34a5c220ccdcf6efc336fc5',
                                    2000000,
                                    '32e125258b7db0a0dffde5bd03b2b859253538ab',
                                    10000000000,
                                    '65333061376664662d373739632d343632332d386639322d386139363134353064383433'
                                ]
                            },
                            'type': 209,
                            'version': 1,
                            'attributes': [
                                {
                                    'usage': 32,
                                    'data': '592c8a46a0d06c600f06c994d1f25e7283b8a2fe'
                                }, {
                                    'usage': 129,
                                    'data': '592c8a46a0d06c600f06c994d1f25e7283b8a2fe'
                                }, {
                                    'usage': 144,
                                    'data': '592c8a46a0d06c600f06c994d1f25e7283b8a2fe'
                                }, {
                                    'usage': 2,
                                    'data': '592c8a46a0d06c600f06c994d1f25e7283b8a2fe'
                                }
                            ],
                            'inputs': [
                                {
                                    'prevHash': '0fcfd792a9d20a7795255d1d3d3927f5968b9953e80d16ffd222656edf8fedbc',
                                    'prevIndex': 0
                                }, {
                                    'prevHash': 'c858e4d2af1e1525fa974fb2b1678caca1f81a5056513f922789594939ff713d',
                                    'prevIndex': 35
                                }
                            ],
                            'outputs': [
                                {
                                    'assetId': '602c79718b16e442de58778e148d0b1084e3b2dffd5de6b7b16cee7969282de7',
                                    'scriptHash': 'e707714512577b42f9a011f8b870625429f93573',
                                    'value': 1e-08
                                }
                            ],
                            'scripts': [],
                            'script': '0800e1f505000000001432e125258b7db0a0dffde5bd03b2b859253538ab14592c8a46a0d06c600f06c994d1f25e7283b8a2fe53c1076465706f73697467823b63e7c70a795a7615a38d1ba67d9e54c195a1',
                            'gas': 0
                        },
                        'cancel_txn': None,
                        'price': '0.0002',
                        'status': 'pending',
                        'created_at': '2018-08-05T10:38:37.731Z',
                        'transaction_hash': '5c4cb1e73b9f2e608b6e768e0654649a4d15e08a7fe63fc536c454fa563a2f0f',
                        'trades': []
                    }, {
                        'id': '7dac087c-3709-48ea-83e1-83eadfc4cbe5',
                        'offer_hash': None,
                        'available_amount': None,
                        'offer_asset_id': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
                        'offer_amount': '2000000',
                        'want_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                        'want_amount': '10000000000',
                        'filled_amount': None,
                        'txn': {
                            'offerHash': 'b45ddfb97ade5e0363d9e707dac9ad1c530448db263e86494225a0025006f968',
                            'hash': '5c4cb1e73b9f2e608b6e768e0654649a4d15e08a7fe63fc536c454fa563a2f0f',
                            'sha256': 'f0b70640627947584a2976edeb055a124ae85594db76453532b893c05618e6ca',
                            'invoke': {
                                'scriptHash': 'a195c1549e7da61b8da315765a790ac7e7633b82',
                                'operation': 'makeOffer',
                                'args': [
                                    '592c8a46a0d06c600f06c994d1f25e7283b8a2fe',
                                    '9b7cffdaa674beae0f930ebe6085af9093e5fe56b34a5c220ccdcf6efc336fc5',
                                    2000000,
                                    '32e125258b7db0a0dffde5bd03b2b859253538ab',
                                    10000000000,
                                    '65333061376664662d373739632d343632332d386639322d386139363134353064383433'
                                ]
                            },
                            'type': 209,
                            'version': 1,
                            'attributes': [
                                {
                                    'usage': 32,
                                    'data': '592c8a46a0d06c600f06c994d1f25e7283b8a2fe'
                                }
                            ],
                            'inputs': [
                                {
                                    'prevHash': '0fcfd792a9d20a7795255d1d3d3927f5968b9953e80d16ffd222656edf8fedbc',
                                    'prevIndex': 0
                                }, {
                                    'prevHash': 'c858e4d2af1e1525fa974fb2b1678caca1f81a5056513f922789594939ff713d',
                                    'prevIndex': 35
                                }
                            ],
                            'outputs': [
                                {
                                    'assetId': '602c79718b16e442de58778e148d0b1084e3b2dffd5de6b7b16cee7969282de7',
                                    'scriptHash': 'e707714512577b42f9a011f8b870625429f93573',
                                    'value': 1e-08
                                }
                            ],
                            'scripts': [],
                            'script': '0800e1f505000000001432e125258b7db0a0dffde5bd03b2b859253538ab14592c8a46a0d06c600f06c994d1f25e7283b8a2fe53c1076465706f73697467823b63e7c70a795a7615a38d1ba67d9e54c195a1',
                            'gas': 0
                        },
                        'cancel_txn': None,
                        'price': '0.0002',
                        'status': 'pending',
                        'created_at': '2018-08-05T10:38:37.731Z',
                        'transaction_hash': '5c4cb1e73b9f2e608b6e768e0654649a4d15e08a7fe63fc536c454fa563a2f0f',
                        'trades': []
                    }]


class TestNeoUtils(unittest.TestCase):

    def test_sign_message(self):
        signed_message = 'f60f6896a87d6d35e62668958e08fb5a7c26c1c381c5ed6ad5b1ad9f6f6e826b1ab7695ad4ddd337438da1cd802b5e19dc6861700f4bd87a58dfa002cde11a3a'
        self.assertEqual(sign_message(encoded_message=encoded_message,private_key_hex=testnet_privatekey_hexstring),
                         signed_message)

    def test_sign_transaction(self):
        signed_transaction = 'cb511f7acf269d22690cf656b2f868fc10d12baff2f398ad175ae7e5a1e599f02d63a52d13aa3f3a6b57eaa0231e9fc4f1ab7900c34240033232c5a9f6b8214b'
        self.assertEqual(sign_transaction(transaction=transaction_dict, private_key_hex=testnet_privatekey_hexstring),
                         signed_transaction)

    def test_sign_array(self):
        pass
#         signed_array = {'e30a7fdf-779c-4623-8f92-8a961450d843': 'b1b821d7aa3c3d388370eba8e910de5c3605fcae2d584b0e89e932658f6b335a6aac65c52928e6eebf85919464897b8966a5a4dbcfd92eb28a3ae88299533f2c', '7dac087c-3709-48ea-83e1-83eadfc4cbe5': 'b1b821d7aa3c3d388370eba8e910de5c3605fcae2d584b0e89e932658f6b335a6aac65c52928e6eebf85919464897b8966a5a4dbcfd92eb28a3ae88299533f2c'}
#         self.assertEqual(sign_txn_array(messages=transaction_array, private_key_hex=testnet_privatekey_hexstring)['e30a7fdf-779c-4623-8f92-8a961450d843'],
#                          signed_array['e30a7fdf-779c-4623-8f92-8a961450d843'])

    def test_encode_message(self):
        self.assertEqual(encode_message(message=message), encoded_message)
        self.assertEqual(encode_message(message=json_message), json_encoded_message)

    def test_to_neo_asset_amount(self):
        self.assertEqual(to_neo_asset_amount(10), '1000000000')
        self.assertEqual(to_neo_asset_amount(.01), '1000000')
        with self.assertRaises(ValueError):
            to_neo_asset_amount(0.0000000000001)
        with self.assertRaises(ValueError):
            to_neo_asset_amount(100000000)

    def test_private_key_to_hex(self):
        self.assertEqual(private_key_to_hex(key_pair=kp), testnet_privatekey_hexstring)

    def test_neo_get_scripthash_from_address(self):
        self.assertEqual(neo_get_scripthash_from_address(address=testnet_address), testnet_scripthash)

    def test_neo_get_address_from_scripthash(self):
        self.assertEqual(neo_get_address_from_scripthash(scripthash=testnet_scripthash), testnet_address)

    def test_neo_get_public_key_from_private_key(self):
        self.assertEqual(neo_get_public_key_from_private_key(private_key=testnet_privatekey).ToString(), testnet_publickey)

    def test_neo_get_scripthash_from_private_key(self):
        self.assertEqual(str(neo_get_scripthash_from_private_key(private_key=testnet_privatekey)), testnet_scripthash)

    def test_open_wallet(self):
        self.assertEqual(open_wallet(testnet_privatekey_hexstring).PublicKey, kp.PublicKey)
        self.assertEqual(open_wallet(testnet_privatekey_hexstring).PrivateKey, kp.PrivateKey)
        self.assertEqual(open_wallet(testnet_privatekey_hexstring).GetAddress(), kp.GetAddress())

    def test_create_offer_hash(self):
        self.assertEqual(create_offer_hash(neo_address='APuP9GsSCPJKrexPe49afDV8CQYubZGWd8',
                                           offer_asset_amt=6000000,
                                           offer_asset_hash='c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
                                           want_asset_amt=30000000000,
                                           want_asset_hash='ab38352559b8b203bde5fddfa0b07d8b2525e132',
                                           txn_uuid='ecb6ee9e-de8d-46d6-953b-afcc976be1ae'),
                         '95a9502f11c62b85cf790b83104c89d3198a3b4dac6ba8a0e19090a8ee2207c7')
