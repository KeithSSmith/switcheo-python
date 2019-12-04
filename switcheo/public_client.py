# -*- coding:utf-8 -*-
"""
Description:
    Public Client for the Switcheo decentralized exchange.
    It is not required to use your private key or WIF to interact with these endpoints which can be used
    to track the exchange state.
Usage:
    from switcheo.public_client import PublicClient
"""

from switcheo.utils import Request


class PublicClient(object):
    """
    This class allows the user to interact with the Switcheo decentralized exchange API to retrieve information about
    the available options on the exchange, including system health, time, trade offers, etc.
    """

    def __init__(self,
                 blockchain="neo",
                 contract_version='V3',
                 api_url='https://test-api.switcheo.network/',
                 api_version='/v2'):
        """

        :param blockchain: Choose which blockchain to trade on.  Allowed value are neo (future eth and qtum)
        :type blockchain: str
        :param api_url: The URL for the Switcheo API endpoint.
        :type api_url: str
        :param api_version: Choose the version of the Switcho API to use.
        :type api_version: str
        """
        self.request = Request(api_url=api_url, api_version=api_version, timeout=30)
        self.blockchain = blockchain
        self.blockchain_key = blockchain.upper()
        self.contracts = self.get_contracts()
        self.contract_version = contract_version.upper()
        self.contract_hash = self.contracts[self.blockchain_key][self.contract_version]
        self.current_contract_hash = self.get_latest_contracts()[self.blockchain_key]

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
        Function to fetch the time on the exchange in to synchronized server time.
        Execution of this function is as follows::

            get_exchange_time()

        The expected return result for this function is as follows::

            {
                'timestamp': 1533362081336
            }

        :return: Dictionary in the form of a JSON message with the exchange epoch time in milliseconds.
        """
        return self.request.get(path='/exchange/timestamp')
    
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
        return self.request.get(path='/exchange/contracts')

    def get_latest_contracts(self):
        """
        Function to fetch the active contract hash for each smart contract deployed on the defined blockchain.
        Execution of this function is as follows::

            get_latest_contracts()

        The expected return result for this function is as follows::

            {
                "NEO": "d524fbb2f83f396368bc0183f5e543cae54ef532",
                "ETH": "0x6ee18298fd6bc2979df9d27569842435a7d55e65",
                "EOS": "oboluswitch4",
                "QTUM": "0x2b25406b0000c3661e9c88890690fd4b5c7b4234"
            }

        :return: Dictionary containing the latest smart contract hash for each blockchain.
        """
        return self.request.get(path='/exchange/latest_contracts')
    
    def get_pairs(self, base=None, show_details=False, show_inactive=False):
        """
        Function to fetch a list of trading pairs offered on the Switcheo decentralized exchange.
        Execution of this function is as follows::

            get_pairs()                  # Fetch all pairs
            get_pairs(base="SWTH")       # Fetch only SWTH base pairs
            get_pairs(show_details=True) # Fetch all pairs with extended information !Attention return value changes!

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

        If you use the show_details parameter the server return a list with dictionaries as follows::

             [
                {'name': 'GAS_NEO', 'precision': 3},
                {'name': 'SWTH_NEO', 'precision': 6},
                {'name': 'ACAT_NEO', 'precision': 8},
                {'name': 'APH_NEO', 'precision': 5},
                {'name': 'ASA_NEO', 'precision': 8},
                ....
            ]

        :param base: The base trade pair to optionally filter available trade pairs.
        :type base: str
        :param show_details: Extended information for the pairs.
        :type show_details: bool
        :return: List of trade pairs available for trade on Switcheo.
        """
        api_params = {}
        if show_details:
            api_params["show_details"] = show_details
        if show_inactive:
            api_params["show_inactive"] = show_inactive
        if base is not None and base in ["NEO", "GAS", "SWTH", "USD", "ETH"]:
            api_params["bases"] = [base]
        return self.request.get(path='/exchange/pairs', params=api_params)
    
    def get_token_details(self, show_listing_details=False, show_inactive=False):
        """
        Function to fetch the available tokens available to trade on the Switcheo exchange.
        Execution of this function is as follows::

            get_token_details()
            get_token_details(show_listing_details=True)
            get_token_details(show_inactive=True)
            get_token_details(show_listing_details=True, show_inactive=True)

        The expected return result for this function is as follows::

            {
                'NEO': {
                    'hash': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
                    'decimals': 8
                },
                'GAS': {
                    'hash': '602c79718b16e442de58778e148d0b1084e3b2dffd5de6b7b16cee7969282de7',
                    'decimals': 8
                },
                'SWTH': {
                    'hash': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
                    'decimals': 8
                },
                ...
            }

        :param show_listing_details: Parameter flag to indicate whether or not to show the token listing details.
        :type show_listing_details: bool
        :param show_inactive: Flag to return the tokens that are no longer traded on the Switcheo Exchange.
        :type show_inactive: bool
        :return: Dictionary in the form of a JSON message with the available tokens for trade on the Switcheo exchange.
        """
        api_params = {
            "show_listing_details": show_listing_details,
            "show_inactive": show_inactive
        }
        return self.request.get(path='/exchange/tokens', params=api_params)

    def get_exchange_message(self):
        """
        Function to fetch the Switcheo Exchange message to ensure pertinent information is handled gracefully.
        Execution of this function is as follows::

            get_exchange_message()

        The expected return result for this function is as follows::

            {
                'message': 'Welcome to Switcheo Beta.',
                'message_type': 'info'
            }

        :return: Dictionary containing the sum of all addresses smart contract balances by processing state.
        """
        return self.request.get(path='/exchange/announcement_message')
    
    def get_exchange_fees(self):
        """
        Function to fetch the Switcheo Exchange fees to assist with automated trading calculations.
        Execution of this function is as follows::

            get_exchange_fees()

        The expected return result for this function is as follows::

            [
                {
                    "maker": {
                        "default": 0
                    },
                    "taker": {
                        "default": 0.002
                    },
                    "network_fee_subsidy_threshold": {
                        "neo": 0.1,
                        "eth": 0.1
                    },
                    "max_taker_fee_ratio": {
                        "neo": 0.005,
                        "eth": 0.1
                    },
                    "native_fee_discount": 0.75,
                    "native_fee_asset_id": "ab38352559b8b203bde5fddfa0b07d8b2525e132",
                    "enforce_native_fees": [
                        "RHT",
                        "RHTC"
                    ],
                    "native_fee_exchange_rates": {
                        "NEO": "952.38095238",
                        "GAS": "297.14285714",
                        ...
                        "ETH": "0",
                        "JRC": "0",
                        "SWC": "0"
                    },
                    "network_fees": {
                        "eth": "2466000000000000",
                        "neo": "200000"
                    },
                    "network_fees_for_wdl": {
                        "eth": "873000000000000",
                        "neo": "0"
                    }
                }
            ]

        :return: Dictionary containing the sum of all addresses smart contract balances by processing state.
        """
        return self.request.get(path='/fees')
    
    def get_exchange_swap_pairs(self):
        """
        Function to fetch the Switcheo Exchange list of atomic swap pairs.
        Execution of this function is as follows::

            get_exchange_swap_pairs()

        The expected return result for this function is as follows::

            [
                "SWTH_ETH",
                "NEO_ETH",
                "EOS_ETH",
                "NEO_DAI",
                "SDUSD_DAI",
                "EOS_NEO",
                "NEO_WBTC"
            ]

        :return: Dictionary containing the sum of all addresses smart contract balances by processing state.
        """
        return self.request.get(path='/exchange/swap_pairs')
    
    def get_exchange_swap_pricing(self, pair):
        """
        Function to fetch the swap pricing for the pair requested.
        Execution of this function is as follows::

            get_exchange_swap_pricing(pair="SWTH_ETH")

        The expected return result for this function is as follows::

            {
                "buy": {
                    "x": "740144428000000",
                    "y": "96969492513000000000",
                    "k": "71771429569484667564000000000000000"
                },
                "sell": {
                    "x": "96969492513000000000",
                    "y": "740144428000000",
                    "k": "71771429569484667564000000000000000"
                }
            }

        :param pair: The trading pair used to request candle statistics.
        :type pair: str
        :return: List of dictionaries containing the candles statistics based on the parameter filters.
        """
        api_params = {
            "pair": pair
        }
        return self.request.get(path='/exchange/swap_pricing', params=api_params)
    
    def get_exchange_swap_contracts(self):
        """
        Function to fetch the Switcheo Exchange list of atomic swap contracts.
        Execution of this function is as follows::

            get_exchange_swap_contracts()

        The expected return result for this function is as follows::

            {
                "ETH": {
                    "V1": "0xeab64b2320a1fc1e65f4c7253385ec18e4b4313b"
                }
            }

        :return: Dictionary containing the sum of all addresses smart contract balances by processing state.
        """
        return self.request.get(path='/exchange/atomic_swap_contracts')

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
        api_params = {
            "pair": pair,
            "interval": interval,
            "start_time": start_time,
            "end_time": end_time,
            "contract_hash": self.contract_hash
        }
        return self.request.get(path='/tickers/candlesticks', params=api_params)

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

    def get_last_price(self, symbols=None, bases=None):
        """
        Function to fetch the most recently executed trade on the order book for each trading pair.
        Execution of this function is as follows::

            get_last_price()
            get_last_price(symbols=['SWTH','GAS'])
            get_last_price(bases=['NEO'])
            get_last_price(symbols=['SWTH','GAS'], bases=['NEO'])

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

        :param symbols: The trading symbols to retrieve the last price on the Switcheo Exchange.
        :type symbols: list
        :param bases: The base pair to retrieve the last price of symbols on the Switcheo Exchange.
        :type bases: list
        :return: Dictionary of trade symbols with the most recently executed trade price.
        """
        api_params = {}
        if symbols is not None:
            api_params['symbols'] = symbols
        if bases is not None:
            api_params['bases'] = bases
        return self.request.get(path='/tickers/last_price', params=api_params)

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
                'want_amount': 300000000,
                'address': '7f345d1a031c4099540dbbbc220d4e5640ab2b6f'
            }, {
                ....
            }]

        :param pair: The trading pair that will be used to request open offers on the order book.
        :type pair: str
        :return: List of dictionaries consisting of the open offers for the requested trading pair.
        """
        api_params = {
            "pair": pair,
            "contract_hash": self.contract_hash
        }
        return self.request.get(path='/offers', params=api_params)

    def get_offer_book(self, pair="SWTH_NEO"):
        """
        Function to fetch the open orders formatted on the order book for the trade pair requested.
        Execution of this function is as follows::

            get_offer_book(pair="SWTH_NEO")

        The expected return result for this function is as follows::

            {
                'asks': [{
                    'price': '0.00068499',
                    'quantity': '43326.8348443'
                }, {
                    'price': '0.000685',
                    'quantity': '59886.34'
                }, {
                    ....
                }],
                'bids': [{
                    'price': '0.00066602',
                    'quantity': '3255.99999999'
                }, {
                    'price': '0.00066601',
                    'quantity': '887.99999999'
                }, {
                    ....
                }]
            }

        :param pair: The trading pair that will be used to request open offers on the order book.
        :type pair: str
        :return: List of dictionaries consisting of the open offers for the requested trading pair.
        """
        api_params = {
            "pair": pair,
            "contract_hash": self.contract_hash
        }
        return self.request.get(path='/offers/book', params=api_params)

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
        :return: List of dictionaries consisting of filled orders that meet requirements of the parameters passed to it.
        """
        if limit > 10000 or limit < 1:
            raise ValueError("Attempting to request more trades than allowed by the API.")
        api_params = {
            "blockchain": self.blockchain,
            "pair": pair,
            "contract_hash": self.contract_hash
        }
        if start_time is not None:
            api_params['from'] = start_time
        if end_time is not None:
            api_params['to'] = end_time
        if limit != 5000:
            api_params['limit'] = limit
        return self.request.get(path='/trades', params=api_params)

    def get_recent_trades(self, pair="SWTH_NEO"):
        """
        Function to fetch a list of the 20 most recently filled trades for the parameters requested.
        Execution of this function is as follows::

            get_recent_trades(pair="SWTH_NEO")

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
            }, ...., {
                'id': '7a308ccc-b7f5-46a3-bf6b-752ab076cc9f',
                'fill_amount': 1001117,
                'take_amount': 2050000000,
                'event_time': '2018-08-03T02:32:50.703Z',
                'is_buy': True
            }]

        :param pair: The trading pair that will be used to request filled trades.
        :type pair: str
        :return: List of 20 dictionaries consisting of filled orders for the trade pair.
        """
        api_params = {
            "pair": pair
        }
        return self.request.get(path='/trades/recent', params=api_params)

    def get_orders(self, address, chain_name='NEO', contract_version='V3', pair=None, from_epoch_time=None,
                   order_status=None, before_id=None, limit=50):
        """
        Function to fetch the order history of the given address.
        Execution of this function is as follows::

            get_orders(address=neo_get_scripthash_from_address(address=address))

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
        :param pair: The trading pair to filter order requests on.
        :type pair: str
        :param chain_name: The name of the chain to find orders against.
        :type chain_name: str
        :param contract_version: The version of the contract to find orders against.
        :type contract_version: str
        :param from_epoch_time: Only return orders that are last updated at or after this time.
        :type from_epoch_time: int
        :param order_status: Only return orders have this status. Possible values are open, cancelled, completed.
        :type order_status: str
        :param before_id: Only return orders that are created before the order with this id.
        :type before_id: str
        :param limit: Only return up to this number of orders (min: 1, max: 200, default: 50).
        :type limit: int
        :return: List of dictionaries containing the orders for the given NEO address and (optional) trading pair.
        """
        api_params = {
            "address": address,
            "contract_hash": self.get_contracts()[chain_name.upper()][contract_version.upper()],
            "limit": limit
        }
        if pair is not None:
            api_params['pair'] = pair
        if from_epoch_time is not None:
            api_params['from_epoch_time'] = from_epoch_time
        if order_status is not None:
            api_params['order_status'] = order_status
        if before_id is not None:
            api_params['before_id'] = before_id
        return self.request.get(path='/orders', params=api_params)

    def get_balance(self, addresses, contracts):
        """
        Function to fetch the current account balance for the given address in the Switcheo smart contract.
        Execution of this function is as follows::

            get_balance(address=neo_get_scripthash_from_address(address=address))

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

        :param addresses: The ScriptHash of the address(es) to retrieve its Smart Contract balance.
        :type addresses: list
        :param contracts: The contract hash(es) to retrieve all addresses Smart Contract balance.
        :type contracts: list
        :return: Dictionary containing the sum of all addresses smart contract balances by processing state.
        """
        api_params = {
            "addresses[]": addresses,
            "contract_hashes[]": contracts
        }
        return self.request.get(path='/balances', params=api_params)
