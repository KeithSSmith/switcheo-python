import unittest
import time
from switcheo.public_client import PublicClient
from switcheo.utils import get_epoch_milliseconds


pc = PublicClient(blockchain='neo')


class TestPublicClient(unittest.TestCase):

    def test_get_exchange_status(self):
        exchange_status_dict = {'status': 'ok'}
        self.assertDictEqual(pc.get_exchange_status(), exchange_status_dict)

    def test_get_exchange_time(self):
        exchange_time_dict = {'timestamp': 1533362081336}
        self.assertGreater(pc.get_exchange_time()['timestamp'], exchange_time_dict['timestamp'])

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
            'SWTH': ['GAS', 'NEO'],
            'GAS': ['NEO'],
            'NEO': ['SWTH'],
            'RHTC': ['NEO']
        }
        last_price_request = pc.get_last_price()
        for pair in last_price_request:
            last_price_request[pair] = list(last_price_request[pair].keys())
        self.assertTrue(last_price_request.keys() == last_price_request.keys())
        for pair in last_price_request:
            self.assertTrue(set(last_price_request[pair]).issubset(set(last_price_dict[pair])))

    def test_get_offers(self):
        offers_list = [{
            'id': '023bff30-ca83-453c-90e9-95502b52f492',
            'offer_asset': 'GAS',
            'want_asset': 'NEO',
            'available_amount': 9509259,
            'offer_amount': 9509259,
            'want_amount': 9509259}]
        offers_set_list = set(offers_list[0].keys())
        offered_list = pc.get_offers()
        self.assertTrue(set(offered_list[0].keys()).issubset(offers_set_list))
        offered_set_list = set()
        for offer in offered_list:
            for key in offer.keys():
                offered_set_list.add(key)
        self.assertTrue(offered_set_list.issubset(offers_set_list))

        offered_list = pc.get_offers(pair="GAS_NEO")
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
            pc.get_trades(pair="SWTH_NEO", limit=1000000)

    def test_get_pairs(self):
        all_pairs = ['GAS_NEO', 'SWTH_NEO', 'ACAT_NEO', 'APH_NEO', 'AVA_NEO', 'COUP_NEO', 'CPX_NEO', 'DBC_NEO',
                     'EFX_NEO', 'GALA_NEO', 'LRN_NEO', 'MCT_NEO', 'NKN_NEO', 'NRVE_NEO', 'OBT_NEO', 'ONT_NEO',
                     'PKC_NEO', 'QLC_NEO', 'RHT_NEO', 'RPX_NEO', 'SDS_NEO', 'SDT_NEO', 'SOUL_NEO', 'TKY_NEO', 'TNC_NEO',
                     'TOLL_NEO', 'ZPT_NEO', 'MCTP_NEO', 'NRVEP_NEO', 'RHTC_NEO', 'SWTH_GAS', 'ACAT_GAS', 'APH_GAS',
                     'AVA_GAS', 'COUP_GAS', 'CPX_GAS', 'DBC_GAS', 'EFX_GAS', 'GALA_GAS', 'LRN_GAS', 'MCT_GAS',
                     'NKN_GAS', 'NRVE_GAS', 'OBT_GAS', 'ONT_GAS', 'PKC_GAS', 'QLC_GAS', 'RHT_GAS', 'RPX_GAS', 'SDS_GAS',
                     'SDT_GAS', 'SOUL_GAS', 'TKY_GAS', 'TNC_GAS', 'TOLL_GAS', 'ZPT_GAS', 'MCTP_GAS', 'NRVEP_GAS',
                     'RHTC_GAS', 'ACAT_SWTH', 'APH_SWTH', 'AVA_SWTH', 'COUP_SWTH', 'CPX_SWTH', 'DBC_SWTH', 'EFX_SWTH',
                     'GALA_SWTH', 'LRN_SWTH', 'MCT_SWTH', 'NKN_SWTH', 'NRVE_SWTH', 'OBT_SWTH', 'ONT_SWTH', 'PKC_SWTH',
                     'QLC_SWTH', 'RHT_SWTH', 'RPX_SWTH', 'SDS_SWTH', 'SDT_SWTH', 'SOUL_SWTH', 'TKY_SWTH', 'TNC_SWTH',
                     'TOLL_SWTH', 'ZPT_SWTH', 'MCTP_SWTH', 'NRVEP_SWTH', 'RHTC_SWTH']
        switcheo_pairs = ['ACAT_SWTH', 'APH_SWTH', 'AVA_SWTH', 'COUP_SWTH', 'CPX_SWTH', 'DBC_SWTH', 'EFX_SWTH',
                          'GALA_SWTH', 'LRN_SWTH', 'MCT_SWTH', 'NKN_SWTH', 'NRVE_SWTH', 'OBT_SWTH', 'ONT_SWTH',
                          'PKC_SWTH', 'QLC_SWTH', 'RHT_SWTH', 'RPX_SWTH', 'SDS_SWTH', 'SDT_SWTH', 'SOUL_SWTH',
                          'TKY_SWTH', 'TNC_SWTH', 'TOLL_SWTH', 'ZPT_SWTH', 'MCTP_SWTH', 'NRVEP_SWTH', 'RHTC_SWTH']
        self.assertTrue(set(pc.get_pairs()).issuperset(set(all_pairs)))
        self.assertTrue(set(pc.get_pairs(base="SWTH")).issuperset(set(switcheo_pairs)))

    def test_get_contracts(self):
        contracts_dict = {
            'NEO': {
                'V1': '0ec5712e0f7c63e4b0fea31029a28cea5e9d551f',
                'V1_5': 'c41d8b0c30252ce7e8b6d95e9ce13fdd68d2a5a8',
                'V2': 'a195c1549e7da61b8da315765a790ac7e7633b82'},
            'ETH': {
                'V1': '0x0000000000000000000000000000000000000000'}}
        self.assertDictEqual(pc.get_contracts(), contracts_dict)

    def test_get_orders(self):
        orders_list = [{
            'id': 'ecb6ee9e-de8d-46d6-953b-afcc976be1ae',
            'blockchain': 'neo',
            'contract_hash': 'a195c1549e7da61b8da315765a790ac7e7633b82',
            'address': 'fea2b883725ef2d194c9060f606cd0a0468a2c59',
            'side': 'buy',
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
            'fills': [],
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
                                'GAS': str(float(int(float(first_balance_dict['confirmed']['GAS'])) + int(
                                    float(second_balance_dict['confirmed']['GAS'])))),
                                'NEO': str(float(int(float(first_balance_dict['confirmed']['NEO'])) + int(
                                    float(second_balance_dict['confirmed']['NEO'])))),
                                'SWTH': str(float(int(float(first_balance_dict['confirmed']['SWTH'])) + int(
                                    float(second_balance_dict['confirmed']['SWTH'])))),
                            }}
        self.assertDictEqual(all_balance_dict['confirmed'], sum_balance_dict['confirmed'])
