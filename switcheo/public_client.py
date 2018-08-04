# -*- coding:utf-8 -*-
"""
Description:
    Public Client for the Switcheo decentralized exchange.  It is not required to use your private key or WIF to interact with these endpoints which can be used to track the exchange state.
Usage:
    from switcheo.public_client import PublicClient
"""

from switcheo.utils import Request


class PublicClient(object):
    """
    This class allows the user to interact with the Switcheo decentralized exchange API to retrieve information about
    the available options on the exchange, including system health, time, trade offers, etc.
    """

    def __init__(self, blockchain="neo"):
        """

        :param blockchain: Choose which blockchain to trade on.  Allowed value are neo (future eth and qtum)
        :type blockchain: str
        """
        self.request = Request(api_url='https://test-api.switcheo.network/', api_version="/v2", timeout=30)
        self.blockchain = blockchain

    def get_exchange_status(self):
        """
        Function to fetch the state of the exchange.
        Execution of this function is as follows::

            get_exchange_status()

        The expected return result for this function is as follows::

            {
                'status': 'ok'
            }

        :return: Dictionary in the form of a JSON message with the exchange status.
        """
        return self.request.status()

    def get_exchange_time(self):
        """
        Function to fetch the time on the exchange in case clocks need to be synchronized or trades need to be aware of server time.
        Execution of this function is as follows::

            get_exchange_time()

        The expected return result for this function is as follows::

            {
                'timestamp': 1533362081336
            }

        :return: Dictionary in the form of a JSON message with the exchange epoch time in milliseconds.
        """
        return self.request.get(path='/exchange/timestamp')

    def get_candlesticks(self, pair, start_time, end_time, interval):
        """
        Function to fetch trading metrics from the past 24 hours for all trading pairs offered on the exchange.
        Execution of this function is as follows::

            get_candlesticks(pair="SWTH_NEO",
                             start_time=round(time.time()) - 350000,
                             end_time=round(time.time()),
                             interval=360))

        The expected return result for this function is as follows::

            [{
                'time': '1533168000',
                'open': '0.00046835',
                'close': '0.00046835',
                'high': '0.00046835',
                'low': '0.00046835',
                'volume': '240315335.0',
                'quote_volume': '513110569018.0'
            },{
                'time': '1533081600',
                'open': '0.00046835',
                'close': '0.00046835',
                'high': '0.00046835',
                'low': '0.00046835',
                'volume': '1170875.0',
                'quote_volume': '2500000000.0'
            },
            ...
            ]

        :param pair: The trading pair used to request candle statistics.
        :type pair: str
        :param start_time: The start time (in epoch seconds) range for collecting candle statistics.
        :type start_time: int
        :param end_time: The end time (in epoch seconds) range for collecting candle statistics.
        :type end_time: int
        :param interval: The time interval (in minutes) for candle statistics.  Allowed values: 1, 5, 30, 60, 360, 1440
        :type interval: int
        :return: List of dictionaries containing the candles statistics based on the parameter filters.
        """
        candle_params = {
            "pair": pair,
            "interval": interval,
            "start_time": start_time,
            "end_time": end_time
        }
        return self.request.get(path='/tickers/candlesticks', params=candle_params)

    def get_last_24_hours(self):
        """
        Function to fetch trading metrics from the past 24 hours for all trading pairs offered on the exchange.
        Execution of this function is as follows::

            get_last_24_hours()

        The expected return result for this function is as follows::

            [{
                'pair': 'SWTH_NEO',
                'open': '0.000407',
                'close': 0.00040911',
                'high': '0.00041492',
                'low': '0.00036',
                'volume': '34572662197.0',
                'quote_volume': '86879788270667.0'
            },{
                'pair': 'GAS_NEO',
                'open': '0.3',
                'close': '0.30391642',
                'high': '0.352',
                'low': '0.2925',
                'volume': '4403569005.0',
                'quote_volume': '14553283004.0'
            },{
            ....
            }]

        :return: List of dictionaries containing the statistics of each trading pair over the last 24 hours.
        """
        return self.request.get(path='/tickers/last_24_hours')

    def get_last_price(self):
        """
        Function to fetch the most recently executed trade on the order book for each trading pair.
        Execution of this function is as follows::

            get_last_price()

        The expected return result for this function is as follows::

            {
                'SWTH': {
                    'GAS': '0.0015085',
                    'NEO': '0.00040911'
                },
                'GAS': {
                    'NEO': '0.30391642'
                },
                ....
            }

        :return: Dictionary of trade symbols with the most recently executed trade price.
        """
        return self.request.get(path='/tickers/last_price')

    def get_offers(self, pair="SWTH_NEO"):
        """
        Function to fetch the open orders on the order book for the trade pair requested.
        Execution of this function is as follows::

            get_offers(pair="SWTH_NEO")

        The expected return result for this function is as follows::

            [{
                'id': '2716c0ca-59bb-4c86-8ee4-6b9528d0e5d2',
                'offer_asset': 'GAS',
                'want_asset': 'NEO',
                'available_amount': 9509259,
                'offer_amount': 30000000,
                'want_amount': 300000000
            }, {
                ....
            }]

        :param pair: The trading pair that will be used to request open offers on the order book.
        :type pair: str
        :return: List of dictionaries consisting of the open offers for the requested trading pair.
        """
        offer_params = {
            "blockchain": self.blockchain,
            "pair": pair,
            "contract_hash": self.get_contracts()["NEO"]["V2"]
        }
        return self.request.get(path='/offers', params=offer_params)

    def get_trades(self, pair="SWTH_NEO", start_time=None, end_time=None, limit=5000):
        """
        Function to fetch a list of filled trades for the parameters requested.
        Execution of this function is as follows::

            get_trades(pair="SWTH_NEO", limit=3)

        The expected return result for this function is as follows::

            [{
                'id': '15bb16e2-7a80-4de1-bb59-bcaff877dee0',
                'fill_amount': 100000000,
                'take_amount': 100000000,
                'event_time': '2018-08-04T15:00:12.634Z',
                'is_buy': True
            }, {
                'id': 'b6f9e530-60ff-46ff-9a71-362097a2025e',
                'fill_amount': 47833882,
                'take_amount': 97950000000,
                'event_time': '2018-08-03T02:44:47.706Z',
                'is_buy': True
            }, {
                'id': '7a308ccc-b7f5-46a3-bf6b-752ab076cc9f',
                'fill_amount': 1001117,
                'take_amount': 2050000000,
                'event_time': '2018-08-03T02:32:50.703Z',
                'is_buy': True
            }]

        :param pair: The trading pair that will be used to request filled trades.
        :type pair: str
        :param start_time: Only return trades after this time (in epoch seconds).
        :type start_time: int
        :param end_time: Only return trades before this time (in epoch seconds).
        :type end_time: int
        :param limit: The number of filled trades to return. Min: 1, Max: 10000, Default: 5000
        :type limit: int
        :return: List of dictionaries consisting of the filled orders that meet the requirements of the parameters passed to it.
        """
        if limit > 10000 or limit < 1:
            exit()
        trades_params = {
            "blockchain": self.blockchain,
            "pair": pair,
            "contract_hash": self.get_contracts()["NEO"]["V2"]
        }
        if start_time is not None:
            trades_params['from'] = start_time
        if end_time is not None:
            trades_params['to'] = end_time
        if limit != 5000:
            trades_params['limit'] = limit
        return self.request.get(path='/trades', params=trades_params)

    def get_pairs(self, base=None):
        """
        Function to fetch a list of trading pairs offered on the Switcheo decentralized exchange.
        Execution of this function is as follows::

            get_pairs()              # Fetch all pairs
            get_pairs(base="SWTH")   # Fetch only SWTH base pairs

        The expected return result for this function is as follows::

            [
                'GAS_NEO',
                'SWTH_NEO',
                'MCT_NEO',
                'NKN_NEO',
                ....
                'SWTH_GAS',
                'MCT_GAS',
                'NKN_GAS',
                ....
                'MCT_SWTH',
                'NKN_SWTH'
            ]

        :param base: The base trade pair to optionally filter available trade pairs.
        :type base: str
        :return: List of trade pairs available for trade on Switcheo.
        """
        if base is not None and base in ["NEO", "GAS", "SWTH", "USD"]:
            base_params = {
                "bases": [
                    base
                ]
            }
            return self.request.get(path='/pairs', params=base_params)
        else:
            return self.request.get(path='/pairs')

    def get_contracts(self):
        """
        Function to fetch the contract hashes for each smart contract deployed on the defined blockchain.
        Execution of this function is as follows::

            get_contracts()

        The expected return result for this function is as follows::

            {
                'NEO': {
                    'V1': '0ec5712e0f7c63e4b0fea31029a28cea5e9d551f',
                    'V1_5': '01bafeeafe62e651efc3a530fde170cf2f7b09bd',
                    'V2': '91b83e96f2a7c4fdf0c1688441ec61986c7cae26'
                },
                'ETH': {
                    'V1': '0x0000000000000000000000000000000000000000'
                }
            }

        :return: Dictionary containing the list of smart contract hashes per blockchain and version.
        """
        return self.request.get(path='/contracts')

    def get_orders(self, address):
        """
        Function to fetch the order history of the given address.
        Execution of this function is as follows::

            get_orders(address=neo_get_scripthash_from_private_key(private_key=prikey))

        The expected return result for this function is as follows::

            [{
                'id': '7cbdf481-6acf-4bf3-a1ed-4773f31e6931',
                'blockchain': 'neo',
                'contract_hash': 'a195c1549e7da61b8da315765a790ac7e7633b82',
                'address': 'fea2b883725ef2d194c9060f606cd0a0468a2c59',
                'side': 'buy',
                'offer_asset_id': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
                'want_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                'offer_amount': '53718500',
                'want_amount': '110000000000',
                'transfer_amount': '0',
                'priority_gas_amount': '0',
                'use_native_token': True,
                'native_fee_transfer_amount': 0,
                'deposit_txn': None,
                'created_at': '2018-08-03T02:44:47.692Z',
                'status': 'processed',
                'fills': [{
                    'id': 'b6f9e530-60ff-46ff-9a71-362097a2025e',
                    'offer_hash': '95b3b03be0bff8f58aa86a8dd599700bbaeaffc05078329d5b726b6b995f4cda',
                    'offer_asset_id': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
                    'want_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                    'fill_amount': '47833882',
                    'want_amount': '97950000000',
                    'filled_amount': '',
                    'fee_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                    'fee_amount': '73462500',
                    'price': '0.00048835',
                    'txn': None,
                    'status': 'success',
                    'created_at': '2018-08-03T02:44:47.706Z',
                    'transaction_hash': '694745a09e33845ec008cfb79c73986a556e619799ec73274f82b30d85bda13a'
                }],
                'makes': [{
                    'id': '357088a0-cc80-49ab-acdd-980589c2d7d8',
                    'offer_hash': '420cc85abf02feaceb1bcd91489a0c1949c972d2a9a05ae922fa15d79de80c00',
                    'available_amount': '0',
                    'offer_asset_id': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
                    'offer_amount': '5884618',
                    'want_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                    'want_amount': '12050000000',
                    'filled_amount': '0.0',
                    'txn': None,
                    'cancel_txn': None,
                    'price': '0.000488350041493775933609958506224066390041494',
                    'status': 'cancelled',
                    'created_at': '2018-08-03T02:44:47.708Z',
                    'transaction_hash': '1afa946546550151bbbd19f197a87cec92e9be58c44ec431cae42076298548b7',
                    'trades': []
                }]
            }, {
            ....
            }]

        :param address: The ScriptHash of the address to filter orders for.
        :type address: str
        :return: List of dictionaries containing the orders for the given NEO address.
        """
        order_params = {
            "address": address,
            "contract_hash": self.get_contracts()["NEO"]["V2"]
        }
        return self.request.get(path='/orders', params=order_params)

    def get_balance(self, address):
        """
        Function to fetch the current account balance for the given address in the Switcheo smart contract (i.e. deposited to the trading contract balance).
        Execution of this function is as follows::

            get_balance(address=neo_get_scripthash_from_private_key(private_key=prikey))

        The expected return result for this function is as follows::

            {
                'confirming': {},
                'confirmed': {
                    'GAS': '100000000.0',
                    'SWTH': '97976537500.0',
                    'NEO': '52166118.0'
                },
                'locked': {}
            }

        :param address: The ScriptHash of the address to retrieve its Smart Contract balance.
        :type address: str
        :return: Dictionary containing the smart contract account balance by state of deposit.
        """
        balance_params = {
            "addresses": [
                address
            ],
            "contract_hashes": [
                self.get_contracts()["NEO"]["V2"]
            ]
        }
        return self.request.get(path='/balances', params=balance_params)
