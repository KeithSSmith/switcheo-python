import unittest
import time
from switcheo.public_client import PublicClient


pc = PublicClient(blockchain='neo')
pc_eth = PublicClient(blockchain='eth', contract_version='V2')


class TestPublicClient(unittest.TestCase):

    def test_get_exchange_status(self):
        exchange_status_dict = {'status': 'ok'}
        self.assertDictEqual(pc.get_exchange_status(), exchange_status_dict)

    def test_get_exchange_time(self):
        exchange_time_dict = {'timestamp': 1533362081336}
        self.assertGreater(pc.get_exchange_time()['timestamp'], exchange_time_dict['timestamp'])

    def test_get_token_details(self):
        exchange_token_list = ['NEO', 'GAS', 'SWTH', 'ETH']
        exchange_token_request = pc.get_token_details()
        self.assertTrue(set(exchange_token_request.keys()).issuperset(set(exchange_token_list)))

    def test_get_candlesticks(self):
        candles_key_list = ['time', 'open', 'close', 'high', 'low', 'volume', 'quote_volume']
        candles_request = pc.get_candlesticks(pair="SWTH_NEO",
                                              start_time=round(time.time()) - 360000,
                                              end_time=round(time.time()),
                                              interval=60)
        for candle in candles_request:
            candles_request = list(candle.keys())
        self.assertTrue(set(candles_request).issubset(set(candles_key_list)))

    def test_get_last_24_hours(self):
        last_stats_list = ['pair', 'open', 'close', 'high', 'low', 'volume', 'quote_volume']
        last_24_hours_request = pc.get_last_24_hours()
        for pair in last_24_hours_request:
            last_24_hours_request = list(pair.keys())
        self.assertTrue(set(last_24_hours_request).issubset(set(last_stats_list)))

    def test_get_last_price(self):
        last_price_dict = {
            'SWTH': ['ETH', 'NEO']
        }
        last_price_request = pc.get_last_price()
        for pair in last_price_request:
            last_price_request[pair] = list(last_price_request[pair].keys())
        self.assertTrue(set(last_price_request.keys()).issuperset(set(last_price_dict.keys())))
        for pair in last_price_dict:
            self.assertTrue(set(last_price_request[pair]).issubset(set(last_price_dict[pair])))

    def test_get_offers(self):
        offers_list = [{
            'id': '023bff30-ca83-453c-90e9-95502b52f492',
            'offer_asset': 'SWTH',
            'want_asset': 'NEO',
            'available_amount': 9509259,
            'offer_amount': 9509259,
            'want_amount': 9509259,
            'address': '7f345d1a031c4099540dbbbc220d4e5640ab2b6f'}]
        offers_set_list = set(offers_list[0].keys())
        offered_list = pc.get_offers()
        self.assertTrue(set(offered_list[0].keys()).issubset(offers_set_list))
        offered_set_list = set()
        for offer in offered_list:
            for key in offer.keys():
                offered_set_list.add(key)
        self.assertTrue(offered_set_list.issubset(offers_set_list))

        offered_list = pc_eth.get_offers(pair="JRC_ETH")
        self.assertTrue(set(offered_list[0].keys()).issubset(offers_set_list))
        offered_set_list = set()
        for offer in offered_list:
            for key in offer.keys():
                offered_set_list.add(key)
        self.assertTrue(offered_set_list.issubset(offers_set_list))

    def test_get_trades(self):
        trades_key_list = ['id', 'fill_amount', 'take_amount', 'event_time', 'is_buy']
        trades_list = pc.get_trades(pair="SWTH_NEO",
                                    limit=1,
                                    start_time=int(round(time.time())) - 2419200,
                                    end_time=int(round(time.time())))
        trades_list = trades_list[0].keys()
        self.assertTrue(set(trades_list).issubset(set(trades_key_list)))
        with self.assertRaises(ValueError):
            pc.get_trades(pair="SWTH_NEO", limit=0)
        with self.assertRaises(ValueError):
            pc.get_trades(pair="SWTH_NEO", limit=1000000)

    def test_get_pairs(self):
        all_pairs = ['GAS_NEO', 'SWTH_NEO', 'TMN_NEO', 'TKY_NEO', 'LEO_ETH', 'MKR_ETH', 'ETH_WBTC']
        neo_pairs = ['GAS_NEO', 'SWTH_NEO', 'ACAT_NEO', 'ASA_NEO', 'AVA_NEO', 'FTWX_NEO', 'MCT_NEO',
                     'NOS_NEO', 'NRVE_NEO', 'PHX_NEO', 'QLC_NEO', 'SOUL_NEO', 'TKY_NEO', 'TMN_NEO']
        self.assertTrue(set(pc.get_pairs(show_inactive=True)).issuperset(set(all_pairs)))
        self.assertTrue(set(pc.get_pairs(base="NEO", show_inactive=True)).issuperset(set(neo_pairs)))

    def test_get_contracts(self):
        contracts_dict = {
            'NEO': {
                'V1': '0ec5712e0f7c63e4b0fea31029a28cea5e9d551f',
                'V1_5': 'c41d8b0c30252ce7e8b6d95e9ce13fdd68d2a5a8',
                'V2': 'a195c1549e7da61b8da315765a790ac7e7633b82',
                'V3': '58efbb3cca7f436a55b1a05c0f36788d2d9a032e'
            },
            'ETH': {
                'V1': '0x4dcf0244742e72309666db20d367f6dd196e884e',
                'V2': '0x4d19fd42e780d56ff6464fe9e7d5158aee3d125d'
            },
            'EOS': {
                'V1': 'toweredbyob2'
            },
            'QTUM': {
                'V1': 'fake_qtum_contract_hash'
            }
        }
        self.assertDictEqual(pc.get_contracts(), contracts_dict)

    def test_get_orders(self):
        orders_list = [{
            'id': 'ecb6ee9e-de8d-46d6-953b-afcc976be1ae',
            'blockchain': 'neo',
            'contract_hash': 'a195c1549e7da61b8da315765a790ac7e7633b82',
            'address': 'fea2b883725ef2d194c9060f606cd0a0468a2c59',
            'pair': 'SWTH_NEO',
            'side': 'buy',
            'price': '0.000001',
            'quantity': '1000000',
            'offer_asset_id': 'c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b',
            'want_asset_id': 'ab38352559b8b203bde5fddfa0b07d8b2525e132',
            'offer_amount': '6000000',
            'want_amount': '30000000000',
            'transfer_amount': '0',
            'priority_gas_amount': '0',
            'use_native_token': True,
            'native_fee_transfer_amount': 0,
            'deposit_txn': None,
            'created_at': '2018-08-08T18:39:13.864Z',
            'status': 'processed',
            'order_status': 'processed',
            'txn': None,
            'offer_asset_blockchain': 'neo',
            'want_asset_blockchain': 'neo',
            'broadcast_cutoff_at': '2019-05-04T15:53:04.809Z',
            'scheduled_cancellation_at': None,
            'counterpart_swap': None,
            "unlock_swap_txn": None,
            'fills': [],
            'fill_groups': [],
            'makes': []
        }]
        switcheo_orders_list = orders_list.copy()
        orders_list = orders_list[0].keys()
        testnet_scripthash = 'fea2b883725ef2d194c9060f606cd0a0468a2c59'
        all_orders = pc.get_orders(address=testnet_scripthash)
        switcheo_orders = pc.get_orders(address=testnet_scripthash, pair="SWTH_NEO")
        self.assertGreaterEqual(len(all_orders), len(switcheo_orders))
        self.assertTrue(set(all_orders[0].keys()).issubset(set(orders_list)))
        switcheo_orders_list_set = set()
        switcheo_orders_set = set()
        for order in switcheo_orders_list:
            switcheo_orders_list_set.add(order['offer_asset_id'])
            switcheo_orders_list_set.add(order['want_asset_id'])
        for order in switcheo_orders:
            switcheo_orders_set.add(order['offer_asset_id'])
            switcheo_orders_set.add(order['want_asset_id'])
        self.assertTrue(switcheo_orders_set.issubset(switcheo_orders_list_set))

    def test_get_balance(self):
        balance_dict = {
            'confirming': {},
            'confirmed': {
                'GAS': '90000000.0',
                'SWTH': '73580203956.0',
                'NEO': '113073528.0'},
            'locked': {
                'GAS': '9509259.0',
                'NEO': '4000000.0'}}
        balance_dict_set = set(balance_dict.keys())
        first_address = ['ca7316f459db1d3b444f57fe1ab875b3a607c200']
        second_address = ['fea2b883725ef2d194c9060f606cd0a0468a2c59']
        all_addresses = ['ca7316f459db1d3b444f57fe1ab875b3a607c200', 'fea2b883725ef2d194c9060f606cd0a0468a2c59']
        contracts = pc.get_contracts()
        all_contracts = []
        for chain in contracts:
            for contract in contracts[chain]:
                if chain == 'NEO':
                    all_contracts.append(contracts[chain][contract])
        first_balance_dict = pc.get_balance(addresses=first_address, contracts=all_contracts)
        first_balance_dict_set = set(first_balance_dict.keys())
        second_balance_dict = pc.get_balance(addresses=second_address, contracts=all_contracts)
        second_balance_dict_set = set(second_balance_dict.keys())
        all_balance_dict = pc.get_balance(addresses=all_addresses, contracts=all_contracts)
        all_balance_dict_set = set(all_balance_dict.keys())
        self.assertTrue(first_balance_dict_set.issubset(balance_dict_set))
        self.assertTrue(second_balance_dict_set.issubset(balance_dict_set))
        self.assertTrue(all_balance_dict_set.issubset(balance_dict_set))

        sum_balance_dict = {'confirmed': {
                                'GAS': str(int(float(first_balance_dict['confirmed']['GAS'])) + int(
                                    float(second_balance_dict['confirmed']['GAS']))),
                                'NEO': str(int(float(first_balance_dict['confirmed']['NEO'])) + int(
                                    float(second_balance_dict['confirmed']['NEO']))),
                                'SWTH': str(int(float(first_balance_dict['confirmed']['SWTH'])) + int(
                                    float(second_balance_dict['confirmed']['SWTH']))),
                            }}
        self.assertDictEqual(all_balance_dict['confirmed'], sum_balance_dict['confirmed'])
