# -*- coding:utf-8 -*-
"""
Description:
    Authenticated Client for the Switcheo decentralized exchange.
    This API extends the PublicClient by offering API endpoints that require signatures from the
    users private key.
    Deposit, Withdrawal, Trading, and Cancellations on the exchange are accessible through this class.
Usage:
    from switcheo.authenticated_client import AuthenticatedClient
"""

from functools import partial
from switcheo.public_client import PublicClient
from switcheo.utils import get_epoch_milliseconds
from switcheo.neo.utils import to_neo_asset_amount
from switcheo.neo.signatures import sign_create_deposit as sign_create_deposit_neo,\
    sign_execute_deposit as sign_execute_deposit_neo, sign_create_order as sign_create_order_neo,\
    sign_execute_order as sign_execute_order_neo, sign_create_withdrawal as sign_create_withdrawal_neo,\
    sign_execute_withdrawal as sign_execute_withdrawal_neo, sign_create_cancellation as sign_create_cancellation_neo,\
    sign_execute_cancellation as sign_execute_cancellation_neo
from switcheo.ethereum.signatures import sign_create_deposit as sign_create_deposit_eth,\
    sign_execute_deposit as sign_execute_deposit_eth, sign_create_order as sign_create_order_eth,\
    sign_execute_order as sign_execute_order_eth, sign_create_withdrawal as sign_create_withdrawal_eth,\
    sign_execute_withdrawal as sign_execute_withdrawal_eth, sign_create_cancellation as sign_create_cancellation_eth,\
    sign_execute_cancellation as sign_execute_cancellation_eth
from eth_utils import to_wei


class AuthenticatedClient(PublicClient):

    def __init__(self,
                 blockchain='neo',
                 contract_version='V3',
                 api_url='https://test-api.switcheo.network/',
                 api_version='/v2'):
        PublicClient.__init__(self,
                              blockchain=blockchain,
                              contract_version=contract_version,
                              api_url=api_url,
                              api_version=api_version)
        self.infura_dict = {
            'https://api.switcheo.network': 'https://infura.io/',
            'https://api.switcheo.network/': 'https://infura.io/',
            'api.switcheo.network': 'https://infura.io/',
            'api.switcheo.network/': 'https://infura.io/',
            'https://test-api.switcheo.network': 'https://ropsten.infura.io/',
            'https://test-api.switcheo.network/': 'https://ropsten.infura.io/',
            'test-api.switcheo.network': 'https://ropsten.infura.io/',
            'test-api.switcheo.network/': 'https://ropsten.infura.io/'
        }
        self.infura_url = self.infura_dict[api_url]
        self.blockchain_amount = {
            'eth': partial(to_wei, unit='ether'),
            'neo': to_neo_asset_amount
        }
        self.sign_create_cancellation_function = {
            'eth': sign_create_cancellation_eth,
            'neo': sign_create_cancellation_neo
        }
        self.sign_execute_cancellation_function = {
            'eth': sign_execute_cancellation_eth,
            'neo': sign_execute_cancellation_neo
        }
        self.sign_create_deposit_function = {
            'eth': sign_create_deposit_eth,
            'neo': sign_create_deposit_neo
        }
        self.sign_execute_deposit_function = {
            'eth': partial(sign_execute_deposit_eth, infura_url=self.infura_url),
            'neo': sign_execute_deposit_neo
        }
        self.sign_create_order_function = {
            'eth': sign_create_order_eth,
            'neo': sign_create_order_neo
        }
        self.sign_execute_order_function = {
            'eth': sign_execute_order_eth,
            'neo': sign_execute_order_neo
        }
        self.sign_create_withdrawal_function = {
            'eth': sign_create_withdrawal_eth,
            'neo': sign_create_withdrawal_neo
        }
        self.sign_execute_withdrawal_function = {
            'eth': sign_execute_withdrawal_eth,
            'neo': sign_execute_withdrawal_neo
        }

    def cancel_order(self, order_id, private_key):
        """
        This function is a wrapper function around the create and execute cancellation functions to help make this
        processes simpler for the end user by combining these requests in 1 step.
        Execution of this function is as follows::

            cancel_order(order_id=order['id'], private_key=kp)
            cancel_order(order_id=order['id'], private_key=eth_private_key)

        The expected return result for this function is the same as the execute_cancellation function::

            {
                'id': 'b8e617d5-f5ed-4600-b8f2-7d370d837750',
                'blockchain': 'neo',
                'contract_hash': 'a195c1549e7da61b8da315765a790ac7e7633b82',
                'address': 'fea2b883725ef2d194c9060f606cd0a0468a2c59',
                'side': 'buy',
                'offer_asset_id': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
                'want_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                'offer_amount': '2000000',
                'want_amount': '10000000000',
                'transfer_amount': '0',
                'priority_gas_amount': '0',
                'use_native_token': True,
                'native_fee_transfer_amount': 0,
                'deposit_txn': None,
                'created_at': '2018-08-05T11:16:47.021Z',
                'status': 'processed',
                'fills': [],
                'makes': [
                    {
                        'id': '6b9f40de-f9bb-46b6-9434-d281f8c06b74',
                        'offer_hash': '6830d82dbdda566ab32e9a8d9d9d94d3297f67c10374d69bb35d6c5a86bd3e92',
                        'available_amount': '0',
                        'offer_asset_id': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
                        'offer_amount': '2000000',
                        'want_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                        'want_amount': '10000000000',
                        'filled_amount': '0.0',
                        'txn': None,
                        'cancel_txn': None,
                        'price': '0.0002',
                        'status': 'cancelling',
                        'created_at': '2018-08-05T11:16:47.036Z',
                        'transaction_hash': 'e5b08c4a55c7494f1ec7dd93ac2bb2b4e84e77dec9e00e91be1d520cb818c415',
                        'trades': []
                    }
                ]
            }

        :param order_id: The order ID of the open transaction on the order book that you want to cancel.
        :type order_id: str
        :param private_key: The KeyPair that will be used to sign the transaction sent to the blockchain.
        :type private_key: KeyPair
        :return: Dictionary of the transaction details and state after sending the signed transaction to the blockchain.
        """
        create_cancellation = self.create_cancellation(order_id=order_id, private_key=private_key)
        return self.execute_cancellation(cancellation_params=create_cancellation, private_key=private_key)

    def create_cancellation(self, order_id, private_key):
        """
        Function to create a cancellation request for the order ID from the open orders on the order book.
        Execution of this function is as follows::

            create_cancellation(order_id=order['id'], private_key=kp)

        The expected return result for this function is as follows::

            {
                'id': '6b9f40de-f9bb-46b6-9434-d281f8c06b74',
                'transaction': {
                    'hash': '50d99ebd7e57dbdceb7edc2014da5f446c8f44cc0a0b6d9c762a29e8a74bb051',
                    'sha256': '509edb9888fa675988fa71a27600b2655e63fe979424f13f5c958897b2e99ed8',
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
                            'prevHash': '9eaca1adcbbc0669a936576cb9ad03c11c99c356347aae3037ce1f0e4d330d85',
                            'prevIndex': 0
                        }, {
                            'prevHash': 'c858e4d2af1e1525fa974fb2b1678caca1f81a5056513f922789594939ff713d',
                            'prevIndex': 37
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
                    'script': '....',
                    'gas': 0
                },
                'script_params': {
                    'scriptHash': 'a195c1549e7da61b8da315765a790ac7e7633b82',
                    'operation': 'cancelOffer',
                    'args': [
                        '923ebd865a6c5db39bd67403c1677f29d3949d9d8d9a2eb36a56dabd2dd83068'
                    ]
                }
            }

        :param order_id: The order ID of the open transaction on the order book that you want to cancel.
        :type order_id: str
        :param private_key: The KeyPair that will be used to sign the transaction sent to the blockchain.
        :type private_key: KeyPair
        :return: Dictionary that contains the cancellation request along with blockchain transaction information.
        """
        cancellation_params = {
            "order_id": order_id,
            "timestamp": get_epoch_milliseconds()
        }
        api_params = self.sign_create_cancellation_function[self.blockchain](cancellation_params, private_key)
        return self.request.post(path='/cancellations', json_data=api_params)

    def execute_cancellation(self, cancellation_params, private_key):
        """
        This function executes the order created before it and signs the transaction to be submitted to the blockchain.
        Execution of this function is as follows::

            execute_cancellation(cancellation_params=create_cancellation, private_key=kp)

        The expected return result for this function is as follows::

            {
                'id': 'b8e617d5-f5ed-4600-b8f2-7d370d837750',
                'blockchain': 'neo',
                'contract_hash': 'a195c1549e7da61b8da315765a790ac7e7633b82',
                'address': 'fea2b883725ef2d194c9060f606cd0a0468a2c59',
                'side': 'buy',
                'offer_asset_id': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
                'want_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                'offer_amount': '2000000',
                'want_amount': '10000000000',
                'transfer_amount': '0',
                'priority_gas_amount': '0',
                'use_native_token': True,
                'native_fee_transfer_amount': 0,
                'deposit_txn': None,
                'created_at': '2018-08-05T11:16:47.021Z',
                'status': 'processed',
                'fills': [],
                'makes': [
                    {
                        'id': '6b9f40de-f9bb-46b6-9434-d281f8c06b74',
                        'offer_hash': '6830d82dbdda566ab32e9a8d9d9d94d3297f67c10374d69bb35d6c5a86bd3e92',
                        'available_amount': '0',
                        'offer_asset_id': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
                        'offer_amount': '2000000',
                        'want_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                        'want_amount': '10000000000',
                        'filled_amount': '0.0',
                        'txn': None,
                        'cancel_txn': None,
                        'price': '0.0002',
                        'status': 'cancelling',
                        'created_at': '2018-08-05T11:16:47.036Z',
                        'transaction_hash': 'e5b08c4a55c7494f1ec7dd93ac2bb2b4e84e77dec9e00e91be1d520cb818c415',
                        'trades': []
                    }
                ]
            }

        :param cancellation_params: Parameters generated from the Switcheo API to cancel an order on the order book.
        :type cancellation_params: dict
        :param private_key: The KeyPair that will be used to sign the transaction sent to the blockchain.
        :type private_key: KeyPair
        :return: Dictionary of the transaction details and state after sending the signed transaction to the blockchain.
        """
        cancellation_id = cancellation_params['id']
        api_params = self.sign_execute_cancellation_function[self.blockchain](cancellation_params, private_key)
        return self.request.post(path='/cancellations/{}/broadcast'.format(cancellation_id), json_data=api_params)

    def deposit(self, asset, amount, private_key):
        """
        This function is a wrapper function around the create and execute deposit functions to help make this
        processes simpler for the end user by combining these requests in 1 step.
        Execution of this function is as follows::

            deposit(asset="SWTH", amount=1.1, private_key=KeyPair)
            deposit(asset="SWTH", amount=1.1, private_key=eth_private_key)

        The expected return result for this function is the same as the execute_deposit function::

            {
                'result': 'ok'
            }

        :param asset: Symbol or Script Hash of asset ID from the available products.
        :type asset: str
        :param amount: The amount of coins/tokens to be deposited.
        :type amount: float
        :param private_key: The Private Key (ETH) or KeyPair (NEO) for the wallet being used to sign deposit message.
        :type private_key: KeyPair or str
        :return: Dictionary with the result status of the deposit attempt.
        """
        create_deposit = self.create_deposit(asset=asset, amount=amount, private_key=private_key)
        return self.execute_deposit(deposit_params=create_deposit, private_key=private_key)

    def create_deposit(self, asset, amount, private_key):
        """
        Function to create a deposit request by generating a transaction request from the Switcheo API.
        Execution of this function is as follows::

            create_deposit(asset="SWTH", amount=1.1, private_key=KeyPair)
            create_deposit(asset="ETH", amount=1.1, private_key=eth_private_key)

        The expected return result for this function is as follows::

            {
                'id': '768e2079-1504-4dad-b688-7e1e99ec0a24',
                'transaction': {
                    'hash': '72b74c96b9174e9b9e1b216f7e8f21a6475e6541876a62614df7c1998c6e8376',
                    'sha256': '2109cbb5eea67a06f5dd8663e10fcd1128e28df5721a25d993e05fe2097c34f3',
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
                            'prevHash': 'f09b3b697c580d1730cd360da5e1f0beeae00827eb2f0055cbc85a5a4dadd8ea',
                            'prevIndex': 0
                        }, {
                            'prevHash': 'c858e4d2af1e1525fa974fb2b1678caca1f81a5056513f922789594939ff713d',
                            'prevIndex': 31
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
                    'script': '....',
                    'gas': 0
                },
                'script_params': {
                    'scriptHash': 'a195c1549e7da61b8da315765a790ac7e7633b82',
                    'operation': 'deposit',
                    'args': [
                        '592c8a46a0d06c600f06c994d1f25e7283b8a2fe',
                        '32e125258b7db0a0dffde5bd03b2b859253538ab',
                        100000000
                    ]
                }
            }

        :param asset: Symbol or Script Hash of asset ID from the available products.
        :type asset: str
        :param amount: The amount of coins/tokens to be deposited.
        :type amount: float
        :param private_key: The Private Key (ETH) or KeyPair (NEO) for the wallet being used to sign deposit message.
        :type private_key: KeyPair or str
        :return: Dictionary response of signed deposit request that is ready to be executed on the specified blockchain.
        """
        signable_params = {
            'blockchain': self.blockchain,
            'asset_id': asset,
            'amount': str(self.blockchain_amount[self.blockchain](amount)),
            'timestamp': get_epoch_milliseconds(),
            'contract_hash': self.contract_hash
        }
        api_params = self.sign_create_deposit_function[self.blockchain](signable_params, private_key)
        return self.request.post(path='/deposits', json_data=api_params)

    def execute_deposit(self, deposit_params, private_key):
        """
        Function to execute the deposit request by signing the transaction generated by the create deposit function.
        Execution of this function is as follows::

            execute_deposit(deposit_params=create_deposit, private_key=KeyPair)
            execute_deposit(deposit_params=create_deposit, private_key=eth_private_key)

        The expected return result for this function is as follows::

            {
                'result': 'ok'
            }

        :param deposit_params: Parameters from the API to be signed and deposited to the Switcheo Smart Contract.
        :type deposit_params: dict
        :param private_key: The Private Key (ETH) or KeyPair (NEO) for the wallet being used to sign deposit message.
        :type private_key: KeyPair or str
        :return: Dictionary with the result status of the deposit attempt.
        """
        deposit_id = deposit_params['id']
        api_params = self.sign_execute_deposit_function[self.blockchain](deposit_params, private_key)
        return self.request.post(path='/deposits/{}/broadcast'.format(deposit_id), json_data=api_params)

    def order(self, pair, side, price, quantity, private_key, use_native_token=True, order_type="limit"):
        """
        This function is a wrapper function around the create and execute order functions to help make this processes
        simpler for the end user by combining these requests in 1 step.
        Execution of this function is as follows::

            order(pair="SWTH_NEO", side="buy",
                  price=0.0002, quantity=100, private_key=kp,
                  use_native_token=True, order_type="limit")

        The expected return result for this function is the same as the execute_order function::

            {
                'id': '4e6a59fd-d750-4332-aaf0-f2babfa8ad67',
                'blockchain': 'neo',
                'contract_hash': 'a195c1549e7da61b8da315765a790ac7e7633b82',
                'address': 'fea2b883725ef2d194c9060f606cd0a0468a2c59',
                'side': 'buy',
                'offer_asset_id': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
                'want_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                'offer_amount': '2000000',
                'want_amount': '10000000000',
                'transfer_amount': '0',
                'priority_gas_amount': '0',
                'use_native_token': True,
                'native_fee_transfer_amount': 0,
                'deposit_txn': None,
                'created_at': '2018-08-05T10:38:37.714Z',
                'status': 'processed',
                'fills': [],
                'makes': [
                    {
                        'id': 'e30a7fdf-779c-4623-8f92-8a961450d843',
                        'offer_hash': 'b45ddfb97ade5e0363d9e707dac9ad1c530448db263e86494225a0025006f968',
                        'available_amount': '2000000',
                        'offer_asset_id': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
                        'offer_amount': '2000000',
                        'want_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                        'want_amount': '10000000000',
                        'filled_amount': '0.0',
                        'txn': None,
                        'cancel_txn': None,
                        'price': '0.0002',
                        'status': 'confirming',
                        'created_at': '2018-08-05T10:38:37.731Z',
                        'transaction_hash': '5c4cb1e73b9f2e608b6e768e0654649a4d15e08a7fe63fc536c454fa563a2f0f',
                        'trades': []
                    }
                ]
            }

        :param pair: The trading pair this order is being submitted for.
        :type pair: str
        :param side: The side of the trade being submitted i.e. buy or sell
        :type side: str
        :param price: The price target for this trade.
        :type price: float
        :param quantity: The amount of the asset being exchanged in the trade.
        :type quantity: float
        :param private_key: The Private Key (ETH) or KeyPair (NEO) for the wallet being used to sign deposit message.
        :type private_key: KeyPair or str
        :param use_native_token: Flag to indicate whether or not to pay fees with the Switcheo native token.
        :type use_native_token: bool
        :param order_type: The type of order being submitted, currently this can only be a limit order.
        :type order_type: str
        :return: Dictionary of the transaction on the order book.
        """
        create_order = self.create_order(private_key=private_key, pair=pair, side=side, price=price,
                                         quantity=quantity, use_native_token=use_native_token,
                                         order_type=order_type)
        return self.execute_order(order_params=create_order, private_key=private_key)

    def create_order(self, pair, side, price, quantity, private_key, use_native_token=True, order_type="limit",
                     otc_address=None):
        """
        Function to create an order for the trade pair and details requested.
        Execution of this function is as follows::

            create_order(pair="SWTH_NEO", side="buy", price=0.0002, quantity=100, private_key=kp,
                         use_native_token=True, order_type="limit")

        The expected return result for this function is as follows::

            {
                'id': '4e6a59fd-d750-4332-aaf0-f2babfa8ad67',
                'blockchain': 'neo',
                'contract_hash': 'a195c1549e7da61b8da315765a790ac7e7633b82',
                'address': 'fea2b883725ef2d194c9060f606cd0a0468a2c59',
                'side': 'buy',
                'offer_asset_id': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
                'want_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                'offer_amount': '2000000',
                'want_amount': '10000000000',
                'transfer_amount': '0',
                'priority_gas_amount': '0',
                'use_native_token': True,
                'native_fee_transfer_amount': 0,
                'deposit_txn': None,
                'created_at': '2018-08-05T10:38:37.714Z',
                'status': 'pending',
                'fills': [],
                'makes': [
                    {
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
                            'script': '....',
                            'gas': 0
                        },
                        'cancel_txn': None,
                        'price': '0.0002',
                        'status': 'pending',
                        'created_at': '2018-08-05T10:38:37.731Z',
                        'transaction_hash': '5c4cb1e73b9f2e608b6e768e0654649a4d15e08a7fe63fc536c454fa563a2f0f',
                        'trades': []
                    }
                ]
            }

        :param pair: The trading pair this order is being submitted for.
        :type pair: str
        :param side: The side of the trade being submitted i.e. buy or sell
        :type side: str
        :param price: The price target for this trade.
        :type price: float
        :param quantity: The amount of the asset being exchanged in the trade.
        :type quantity: float
        :param private_key: The Private Key (ETH) or KeyPair (NEO) for the wallet being used to sign deposit message.
        :type private_key: KeyPair or str
        :param use_native_token: Flag to indicate whether or not to pay fees with the Switcheo native token.
        :type use_native_token: bool
        :param order_type: The type of order being submitted, currently this can only be a limit order.
        :type order_type: str
        :param otc_address: The address to trade with for Over the Counter exchanges.
        :type otc_address: str
        :return: Dictionary of order details to specify which parts of the trade will be filled (taker) or open (maker)
        """
        if side.lower() not in ["buy", "sell"]:
            raise ValueError("Allowed trade types are buy or sell, you entered {}".format(side.lower()))
        if order_type.lower() not in ["limit", "market", "otc"]:
            raise ValueError("Allowed order type is limit, you entered {}".format(order_type.lower()))
        if order_type.lower() == "otc" and otc_address is None:
            raise ValueError("OTC Address is required when trade type is otc (over the counter).")
        order_params = {
            "blockchain": self.blockchain,
            "pair": pair,
            "side": side,
            "price": '{:.8f}'.format(price) if order_type.lower() != "market" else None,
            "quantity": str(self.blockchain_amount[self.blockchain](quantity)),
            "use_native_tokens": use_native_token,
            "order_type": order_type,
            "timestamp": get_epoch_milliseconds(),
            "contract_hash": self.contract_hash
        }
        api_params = self.sign_create_order_function[self.blockchain](order_params, private_key)
        return self.request.post(path='/orders', json_data=api_params)

    def execute_order(self, order_params, private_key):
        """
        This function executes the order created before it and signs the transaction to be submitted to the blockchain.
        Execution of this function is as follows::

            execute_order(order_params=create_order, private_key=kp)

        The expected return result for this function is the same as the execute_order function::

            {
                'id': '4e6a59fd-d750-4332-aaf0-f2babfa8ad67',
                'blockchain': 'neo',
                'contract_hash': 'a195c1549e7da61b8da315765a790ac7e7633b82',
                'address': 'fea2b883725ef2d194c9060f606cd0a0468a2c59',
                'side': 'buy',
                'offer_asset_id': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
                'want_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                'offer_amount': '2000000',
                'want_amount': '10000000000',
                'transfer_amount': '0',
                'priority_gas_amount': '0',
                'use_native_token': True,
                'native_fee_transfer_amount': 0,
                'deposit_txn': None,
                'created_at': '2018-08-05T10:38:37.714Z',
                'status': 'processed',
                'fills': [],
                'makes': [
                    {
                        'id': 'e30a7fdf-779c-4623-8f92-8a961450d843',
                        'offer_hash': 'b45ddfb97ade5e0363d9e707dac9ad1c530448db263e86494225a0025006f968',
                        'available_amount': '2000000',
                        'offer_asset_id': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
                        'offer_amount': '2000000',
                        'want_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                        'want_amount': '10000000000',
                        'filled_amount': '0.0',
                        'txn': None,
                        'cancel_txn': None,
                        'price': '0.0002',
                        'status': 'confirming',
                        'created_at': '2018-08-05T10:38:37.731Z',
                        'transaction_hash': '5c4cb1e73b9f2e608b6e768e0654649a4d15e08a7fe63fc536c454fa563a2f0f',
                        'trades': []
                    }
                ]
            }

        :param order_params: Dictionary generated from the create order function.
        :type order_params: dict
        :param private_key: The Private Key (ETH) or KeyPair (NEO) for the wallet being used to sign deposit message.
        :type private_key: KeyPair or str
        :return: Dictionary of the transaction on the order book.
        """
        order_id = order_params['id']
        api_params = self.sign_execute_order_function[self.blockchain](order_params, private_key)
        return self.request.post(path='/orders/{}/broadcast'.format(order_id), json_data=api_params)

    def withdrawal(self, asset, amount, private_key):
        """
        This function is a wrapper function around the create and execute withdrawal functions to help make this
        processes simpler for the end user by combining these requests in 1 step.
        Execution of this function is as follows::

            withdrawal(asset="SWTH", amount=1.1, private_key=kp))

        The expected return result for this function is the same as the execute_withdrawal function::

            {
                'event_type': 'withdrawal',
                'amount': -100000,
                'asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                'status': 'confirming',
                'id': '96e5f797-435b-40ab-9085-4e95c6749218',
                'blockchain': 'neo',
                'reason_code': 9,
                'address': 'fea2b883725ef2d194c9060f606cd0a0468a2c59',
                'transaction_hash': None,
                'created_at': '2018-08-05T10:03:58.885Z',
                'updated_at': '2018-08-05T10:03:59.828Z',
                'contract_hash': 'a195c1549e7da61b8da315765a790ac7e7633b82'
            }

        :param asset: Script Hash of asset ID from the available products.
        :type asset: str
        :param amount: The amount of coins/tokens to be withdrawn.
        :type amount: float
        :param private_key: The Private Key (ETH) or KeyPair (NEO) for the wallet being used to sign deposit message.
        :type private_key: KeyPair or str
        :return: Dictionary with the status of the withdrawal request and blockchain details.
        """
        create_withdrawal = self.create_withdrawal(asset=asset, amount=amount, private_key=private_key)
        return self.execute_withdrawal(withdrawal_params=create_withdrawal, private_key=private_key)

    def create_withdrawal(self, asset, amount, private_key):
        """
        Function to create a withdrawal request by generating a withdrawal ID request from the Switcheo API.
        Execution of this function is as follows::

            create_withdrawal(asset="SWTH", amount=1.1, private_key=kp)

        The expected return result for this function is as follows::

            {
                'id': 'a5a4d396-fa9f-4191-bf50-39a3d06d5e0d'
            }

        :param asset:  Script Hash of asset ID from the available products.
        :type asset: str
        :param amount: The amount of coins/tokens to be withdrawn.
        :type amount: float
        :param private_key: The Private Key (ETH) or KeyPair (NEO) for the wallet being used to sign deposit message.
        :type private_key: KeyPair or str
        :return: Dictionary with the withdrawal ID generated by the Switcheo API.
        """
        signable_params = {
            'blockchain': self.blockchain,
            'asset_id': asset,
            'amount': str(self.blockchain_amount[self.blockchain](amount)),
            'timestamp': get_epoch_milliseconds(),
            'contract_hash': self.contract_hash
        }
        api_params = self.sign_create_withdrawal_function[self.blockchain](signable_params, private_key)
        return self.request.post(path='/withdrawals', json_data=api_params)

    def execute_withdrawal(self, withdrawal_params, private_key):
        """
        This function is to sign the message generated from the create withdrawal function and submit it to the
        blockchain for transfer from the smart contract to the owners address.
        Execution of this function is as follows::

            execute_withdrawal(withdrawal_params=create_withdrawal, private_key=kp)

        The expected return result for this function is as follows::

            {
                'event_type': 'withdrawal',
                'amount': -100000,
                'asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                'status': 'confirming',
                'id': '96e5f797-435b-40ab-9085-4e95c6749218',
                'blockchain': 'neo',
                'reason_code': 9,
                'address': 'fea2b883725ef2d194c9060f606cd0a0468a2c59',
                'transaction_hash': None,
                'created_at': '2018-08-05T10:03:58.885Z',
                'updated_at': '2018-08-05T10:03:59.828Z',
                'contract_hash': 'a195c1549e7da61b8da315765a790ac7e7633b82'
            }

        :param withdrawal_params: Dictionary from the create withdrawal function to sign and submit to the blockchain.
        :type withdrawal_params: dict
        :param private_key: The Private Key (ETH) or KeyPair (NEO) for the wallet being used to sign deposit message.
        :type private_key: KeyPair or str
        :return: Dictionary with the status of the withdrawal request and blockchain transaction details.
        """
        withdrawal_id = withdrawal_params['id']
        api_params = self.sign_execute_withdrawal_function[self.blockchain](withdrawal_params, private_key)
        return self.request.post(path='/withdrawals/{}/broadcast'.format(withdrawal_id), json_data=api_params)
